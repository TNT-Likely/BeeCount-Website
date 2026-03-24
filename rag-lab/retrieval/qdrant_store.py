from __future__ import annotations

import hashlib
from typing import Iterable

from qdrant_client import QdrantClient
from qdrant_client.http import models

from common.config import Settings
from common.models import ChunkRecord
from retrieval.types import SearchHit


class QdrantStore:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = QdrantClient(url=settings.qdrant_url, timeout=60)

    @property
    def client(self) -> QdrantClient:
        return self._client

    def ensure_collection(self, vector_size: int, recreate: bool = False) -> None:
        collection = self._settings.qdrant_collection
        if recreate and self._client.collection_exists(collection):
            self._client.delete_collection(collection)

        if not self._client.collection_exists(collection):
            self._client.create_collection(
                collection_name=collection,
                vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
            )
            self._client.create_payload_index(collection, 'locale', models.PayloadSchemaType.KEYWORD)
            self._client.create_payload_index(collection, 'doc_id', models.PayloadSchemaType.KEYWORD)

    def upsert_chunks(self, chunks: list[ChunkRecord], vectors: list[list[float]]) -> None:
        if not chunks:
            return

        points: list[models.PointStruct] = []
        for chunk, vector in zip(chunks, vectors, strict=True):
            point_id = int(hashlib.md5(chunk.chunk_id.encode('utf-8')).hexdigest()[:16], 16)
            payload = chunk.model_dump(mode='json')
            payload['updated_at'] = chunk.updated_at.isoformat()
            points.append(models.PointStruct(id=point_id, vector=vector, payload=payload))

        self._client.upsert(collection_name=self._settings.qdrant_collection, points=points)

    def delete_by_doc_ids(self, doc_ids: Iterable[str]) -> None:
        for doc_id in doc_ids:
            self._client.delete(
                collection_name=self._settings.qdrant_collection,
                points_selector=models.FilterSelector(
                    filter=models.Filter(
                        must=[
                            models.FieldCondition(
                                key='doc_id',
                                match=models.MatchValue(value=doc_id),
                            )
                        ]
                    )
                ),
            )

    def search_dense(self, query_vector: list[float], limit: int, locale: str | None = None) -> list[SearchHit]:
        query_filter = None
        if locale:
            query_filter = models.Filter(
                must=[models.FieldCondition(key='locale', match=models.MatchValue(value=locale))]
            )

        results = self._client.search(
            collection_name=self._settings.qdrant_collection,
            query_vector=query_vector,
            limit=limit,
            with_payload=True,
            query_filter=query_filter,
        )

        hits: list[SearchHit] = []
        for item in results:
            payload = dict(item.payload or {})
            payload['updated_at'] = payload.get('updated_at') or '1970-01-01T00:00:00Z'
            hits.append(
                SearchHit(
                    chunk=ChunkRecord.model_validate(payload),
                    score=float(item.score),
                    source_mode='dense',
                )
            )
        return hits

    def all_chunks(self) -> list[ChunkRecord]:
        points: list[models.Record] = []
        offset = None
        while True:
            batch, offset = self._client.scroll(
                collection_name=self._settings.qdrant_collection,
                offset=offset,
                limit=256,
                with_payload=True,
                with_vectors=False,
            )
            points.extend(batch)
            if offset is None:
                break

        chunks: list[ChunkRecord] = []
        for record in points:
            payload = dict(record.payload or {})
            payload['updated_at'] = payload.get('updated_at') or '1970-01-01T00:00:00Z'
            chunks.append(ChunkRecord.model_validate(payload))
        return chunks

    def count(self) -> int:
        res = self._client.count(self._settings.qdrant_collection, exact=False)
        return int(res.count)

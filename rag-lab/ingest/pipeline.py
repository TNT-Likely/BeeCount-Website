from __future__ import annotations

import json
import logging
import time
from pathlib import Path

from common.config import Settings
from common.models import ChunkRecord
from common.paths import manifest_path
from ingest.chunker import HeadingAwareChunker
from ingest.parser import DocumentParser
from retrieval.embedding import Embedder
from retrieval.qdrant_store import QdrantStore
from retrieval.service import RetrievalService

logger = logging.getLogger(__name__)


class IngestionPipeline:
    def __init__(
        self,
        settings: Settings,
        parser: DocumentParser,
        chunker: HeadingAwareChunker,
        embedder: Embedder,
        qdrant_store: QdrantStore,
        retrieval_service: RetrievalService,
    ) -> None:
        self._settings = settings
        self._parser = parser
        self._chunker = chunker
        self._embedder = embedder
        self._qdrant = qdrant_store
        self._retrieval = retrieval_service

    def rebuild(self) -> dict:
        started = time.perf_counter()
        docs = self._parser.discover()

        chunks: list[ChunkRecord] = []
        failures: list[str] = []
        for doc in docs:
            try:
                chunks.extend(self._chunker.chunk_document(doc))
            except Exception as exc:  # noqa: BLE001
                logger.exception('chunk failed: %s', doc.source_path)
                failures.append(f'{doc.source_path}: {exc}')

        if chunks:
            vectors = self._embedder.embed_documents([c.content for c in chunks])
            self._qdrant.ensure_collection(vector_size=len(vectors[0]), recreate=True)
            self._qdrant.upsert_chunks(chunks, vectors)
        else:
            # 初始化空集合时使用默认维度 1024（bge-m3）
            self._qdrant.ensure_collection(vector_size=1024, recreate=True)

        self._retrieval.refresh_bm25_from_qdrant()
        self._write_manifest(docs)

        latency_ms = int((time.perf_counter() - started) * 1000)
        return {
            'docs_total': len(docs),
            'chunks_total': len(chunks),
            'added_docs': len(docs),
            'updated_docs': 0,
            'deleted_docs': 0,
            'failed_files': failures,
            'latency_ms': latency_ms,
        }

    def incremental(self) -> dict:
        if not manifest_path(self._settings).exists():
            return self.rebuild()

        started = time.perf_counter()
        current_docs = self._parser.discover()
        previous = self._read_manifest().get('files', {})

        current_map = {doc.manifest_key: doc for doc in current_docs}

        added_keys = set(current_map) - set(previous)
        deleted_keys = set(previous) - set(current_map)
        changed_keys = {
            key
            for key in set(current_map) & set(previous)
            if previous[key].get('hash') != current_map[key].file_hash
        }

        affected_keys = sorted(added_keys | changed_keys)
        deleted_doc_ids = {previous[key]['doc_id'] for key in deleted_keys}
        affected_doc_ids = {current_map[key].doc_id for key in affected_keys}

        failures: list[str] = []
        chunks: list[ChunkRecord] = []
        for key in affected_keys:
            doc = current_map[key]
            try:
                chunks.extend(self._chunker.chunk_document(doc))
            except Exception as exc:  # noqa: BLE001
                logger.exception('incremental chunk failed: %s', doc.source_path)
                failures.append(f'{doc.source_path}: {exc}')

        self._qdrant.delete_by_doc_ids(sorted(deleted_doc_ids | affected_doc_ids))
        if chunks:
            vectors = self._embedder.embed_documents([c.content for c in chunks])
            self._qdrant.upsert_chunks(chunks, vectors)

        self._retrieval.refresh_bm25_from_qdrant()
        self._write_manifest(current_docs)

        latency_ms = int((time.perf_counter() - started) * 1000)
        return {
            'docs_total': len(current_docs),
            'chunks_total': self._qdrant.count(),
            'added_docs': len(added_keys),
            'updated_docs': len(changed_keys),
            'deleted_docs': len(deleted_keys),
            'failed_files': failures,
            'latency_ms': latency_ms,
        }

    def _read_manifest(self) -> dict:
        path = manifest_path(self._settings)
        if not path.exists():
            return {'files': {}}
        return json.loads(path.read_text(encoding='utf-8'))

    def _write_manifest(self, docs) -> None:
        path = manifest_path(self._settings)
        payload = {
            'files': {
                doc.manifest_key: {
                    'hash': doc.file_hash,
                    'doc_id': doc.doc_id,
                    'locale': doc.locale,
                    'url': doc.url,
                    'relative_path': doc.relative_path,
                }
                for doc in docs
            }
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')

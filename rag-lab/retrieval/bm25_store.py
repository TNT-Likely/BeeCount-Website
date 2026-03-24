from __future__ import annotations

import json
from pathlib import Path

from rank_bm25 import BM25Okapi

from common.models import ChunkRecord
from common.text import tokenize
from retrieval.types import SearchHit


class BM25Store:
    def __init__(self, index_path: Path) -> None:
        self._index_path = index_path
        self._chunks: list[ChunkRecord] = []
        self._tokenized_corpus: list[list[str]] = []
        self._bm25: BM25Okapi | None = None

    def is_ready(self) -> bool:
        return self._bm25 is not None and bool(self._chunks)

    def build(self, chunks: list[ChunkRecord]) -> None:
        self._chunks = chunks
        if not chunks:
            self._tokenized_corpus = []
            self._bm25 = None
            return
        self._tokenized_corpus = [tokenize(chunk.content) for chunk in chunks]
        self._bm25 = BM25Okapi(self._tokenized_corpus)

    def save(self) -> None:
        self._index_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            'chunks': [chunk.model_dump(mode='json') for chunk in self._chunks],
            'tokenized_corpus': self._tokenized_corpus,
        }
        self._index_path.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')

    def load(self) -> bool:
        if not self._index_path.exists():
            return False

        payload = json.loads(self._index_path.read_text(encoding='utf-8'))
        self._chunks = [ChunkRecord.model_validate(chunk) for chunk in payload.get('chunks', [])]
        self._tokenized_corpus = payload.get('tokenized_corpus', [])
        if not self._chunks or not self._tokenized_corpus:
            self._bm25 = None
            return True
        self._bm25 = BM25Okapi(self._tokenized_corpus)
        return True

    def search(self, query: str, limit: int, locale: str | None = None) -> list[SearchHit]:
        if self._bm25 is None:
            return []

        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        scores = self._bm25.get_scores(query_tokens)
        ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

        hits: list[SearchHit] = []
        for idx in ranked_indices:
            if len(hits) >= limit:
                break
            chunk = self._chunks[idx]
            if locale and chunk.locale != locale:
                continue
            score = float(scores[idx])
            if score <= 0:
                continue
            hits.append(SearchHit(chunk=chunk, score=score, source_mode='bm25'))
        return hits

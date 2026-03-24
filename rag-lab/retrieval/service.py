from __future__ import annotations

from common.config import Settings
from common.paths import bm25_index_path
from common.text import detect_locale
from retrieval.bm25_store import BM25Store
from retrieval.embedding import Embedder
from retrieval.hybrid import fuse_hits
from retrieval.qdrant_store import QdrantStore
from retrieval.reranker import Reranker
from retrieval.types import SearchHit


class RetrievalService:
    def __init__(self, settings: Settings, qdrant_store: QdrantStore, embedder: Embedder, reranker: Reranker) -> None:
        self._settings = settings
        self._qdrant = qdrant_store
        self._embedder = embedder
        self._reranker = reranker
        self._bm25 = BM25Store(index_path=bm25_index_path(settings))

    def ensure_bm25(self) -> None:
        if self._bm25.is_ready():
            return
        if self._bm25.load():
            return

        try:
            chunks = self._qdrant.all_chunks()
        except Exception:  # noqa: BLE001
            chunks = []
        self._bm25.build(chunks)
        self._bm25.save()

    def refresh_bm25_from_qdrant(self) -> None:
        try:
            chunks = self._qdrant.all_chunks()
        except Exception:  # noqa: BLE001
            chunks = []
        self._bm25.build(chunks)
        self._bm25.save()

    def retrieve(
        self,
        query: str,
        locale: str,
        mode: str,
        top_k: int,
        use_reranker: bool,
    ) -> tuple[list[SearchHit], str]:
        resolved_locale = detect_locale(query) if locale == 'auto' else locale

        dense_hits: list[SearchHit] = []
        bm25_hits: list[SearchHit] = []

        if mode in ('dense', 'hybrid'):
            query_vec = self._embedder.embed_query(query)
            dense_hits = self._qdrant.search_dense(query_vec, self._settings.top_k_dense, resolved_locale)

        if mode in ('bm25', 'hybrid'):
            self.ensure_bm25()
            bm25_hits = self._bm25.search(query, self._settings.top_k_bm25, resolved_locale)

        if mode == 'dense':
            hits = dense_hits[:top_k]
        elif mode == 'bm25':
            hits = bm25_hits[:top_k]
        else:
            hits = fuse_hits(dense_hits, bm25_hits, alpha=self._settings.hybrid_alpha, limit=top_k)

        if use_reranker and hits:
            hits = self._reranker.rerank(query, hits)

        return hits, resolved_locale

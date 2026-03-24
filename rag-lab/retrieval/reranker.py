from __future__ import annotations

import logging
from threading import Lock

from sentence_transformers import CrossEncoder

from common.config import Settings
from retrieval.types import SearchHit

logger = logging.getLogger(__name__)


class Reranker:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._model: CrossEncoder | None = None
        self._lock = Lock()

    def _get_model(self) -> CrossEncoder:
        if self._model is None:
            with self._lock:
                if self._model is None:
                    self._model = CrossEncoder(self._settings.reranker_model, max_length=512)
        return self._model

    def rerank(self, query: str, hits: list[SearchHit]) -> list[SearchHit]:
        if not hits:
            return hits

        try:
            model = self._get_model()
            pairs = [[query, hit.chunk.content] for hit in hits]
            scores = model.predict(pairs)

            reranked = []
            for hit, score in zip(hits, scores, strict=True):
                reranked.append(SearchHit(chunk=hit.chunk, score=float(score), source_mode='reranked'))

            return sorted(reranked, key=lambda h: h.score, reverse=True)
        except Exception as exc:  # noqa: BLE001
            logger.warning('reranker failed, fallback to original ranking: %s', exc)
            return hits

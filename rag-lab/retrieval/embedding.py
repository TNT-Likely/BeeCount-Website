from __future__ import annotations

from threading import Lock

from sentence_transformers import SentenceTransformer

from common.config import Settings


class Embedder:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._model: SentenceTransformer | None = None
        self._lock = Lock()

    def _get_model(self) -> SentenceTransformer:
        if self._model is None:
            with self._lock:
                if self._model is None:
                    self._model = SentenceTransformer(self._settings.embedding_model)
        return self._model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        model = self._get_model()
        vectors = model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
            batch_size=32,
        )
        return [v.tolist() for v in vectors]

    def embed_query(self, text: str) -> list[float]:
        model = self._get_model()
        vector = model.encode(text, normalize_embeddings=True, show_progress_bar=False)
        return vector.tolist()

from __future__ import annotations

from typing import Iterable

from retrieval.types import SearchHit


def _normalize(hits: list[SearchHit]) -> dict[str, float]:
    if not hits:
        return {}

    values = [hit.score for hit in hits]
    min_score = min(values)
    max_score = max(values)

    if max_score == min_score:
        return {hit.chunk.chunk_id: 1.0 for hit in hits}

    return {
        hit.chunk.chunk_id: (hit.score - min_score) / (max_score - min_score)
        for hit in hits
    }


def fuse_hits(dense_hits: list[SearchHit], bm25_hits: list[SearchHit], alpha: float, limit: int) -> list[SearchHit]:
    dense_norm = _normalize(dense_hits)
    bm25_norm = _normalize(bm25_hits)

    merged: dict[str, SearchHit] = {}
    for hit in dense_hits + bm25_hits:
        if hit.chunk.chunk_id not in merged:
            merged[hit.chunk.chunk_id] = SearchHit(chunk=hit.chunk, score=0.0, source_mode='hybrid')

    for chunk_id, hit in merged.items():
        hit.score = alpha * dense_norm.get(chunk_id, 0.0) + (1 - alpha) * bm25_norm.get(chunk_id, 0.0)

    ranked = sorted(merged.values(), key=lambda h: h.score, reverse=True)
    return ranked[:limit]

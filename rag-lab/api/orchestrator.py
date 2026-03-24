from __future__ import annotations

import hashlib
import json
import time
from collections import OrderedDict
from typing import TYPE_CHECKING

from common.cache import QueryCache
from common.models import Citation, QueryRequest, QueryResponse, RetrievedChunk

if TYPE_CHECKING:
    from generation.service import GenerationService
    from retrieval.service import RetrievalService


class RagOrchestrator:
    def __init__(
        self,
        retrieval_service: RetrievalService,
        generation_service: GenerationService,
        query_cache: QueryCache,
    ) -> None:
        self._retrieval = retrieval_service
        self._generation = generation_service
        self._cache = query_cache

    async def run_query(
        self,
        request: QueryRequest,
        trace_id: str,
        disable_cache: bool = False,
        *,
        system_prompt_override: str | None = None,
        fallback_provider: str | None = None,
    ) -> QueryResponse:
        started = time.perf_counter()
        cache_key = self._cache_key(
            request=request,
            system_prompt_override=system_prompt_override,
            fallback_provider=fallback_provider,
        )
        if not disable_cache:
            cached = self._cache.get(cache_key)
            if cached is not None:
                cached['trace_id'] = trace_id
                return QueryResponse.model_validate(cached)

        hits, resolved_locale = self._retrieval.retrieve(
            query=request.query,
            locale=request.locale,
            mode=request.mode,
            top_k=request.top_k,
            use_reranker=request.use_reranker,
        )

        answer, provider_used, fallback_used, fallback_reason = await self._generation.generate(
            query=request.query,
            locale=resolved_locale,
            hits=hits,
            generation_provider=request.generation_provider,
            system_prompt_override=system_prompt_override,
            fallback_provider=fallback_provider,
        )

        citations = self._build_citations(hits)
        retrieved_chunks = [
            RetrievedChunk(
                chunk_id=hit.chunk.chunk_id,
                doc_id=hit.chunk.doc_id,
                locale=hit.chunk.locale,
                title=hit.chunk.title,
                heading=hit.chunk.heading,
                url=hit.chunk.url,
                content=hit.chunk.content,
                score=round(hit.score, 6),
                source_mode=hit.source_mode,  # type: ignore[arg-type]
            )
            for hit in hits
        ]

        latency_ms = int((time.perf_counter() - started) * 1000)
        response = QueryResponse(
            answer=answer,
            citations=citations,
            retrieved_chunks=retrieved_chunks,
            latency_ms=latency_ms,
            trace_id=trace_id,
            provider_used=provider_used,  # type: ignore[arg-type]
            fallback_used=fallback_used,
            fallback_reason=fallback_reason,
        )

        if not disable_cache:
            self._cache.set(cache_key, response.model_dump(mode='json'))
        return response

    @staticmethod
    def _cache_key(
        request: QueryRequest,
        system_prompt_override: str | None,
        fallback_provider: str | None,
    ) -> str:
        payload = request.model_dump(mode='json')
        payload['_system_prompt_override'] = system_prompt_override or ''
        payload['_fallback_provider'] = fallback_provider or ''
        data = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        return hashlib.sha1(data.encode('utf-8')).hexdigest()

    @staticmethod
    def _build_citations(hits) -> list[Citation]:
        by_url: OrderedDict[str, Citation] = OrderedDict()
        for hit in hits:
            if hit.chunk.url in by_url:
                continue
            by_url[hit.chunk.url] = Citation(
                url=hit.chunk.url,
                title=hit.chunk.title,
                heading=hit.chunk.heading,
                chunk_id=hit.chunk.chunk_id,
                score=round(hit.score, 6),
                locale=hit.chunk.locale,
            )
        return list(by_url.values())[:5]

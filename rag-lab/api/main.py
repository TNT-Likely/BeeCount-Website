from __future__ import annotations

import asyncio
import logging
import uuid

import orjson
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import StreamingResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from api.openai_compat import create_openai_router
from api.orchestrator import RagOrchestrator
from common.cache import QueryCache
from common.config import get_settings
from common.logging import configure_logging
from common.models import EvalRequest, IngestResponse, QueryRequest, QueryResponse
from common.telemetry import REQUEST_COUNT, REQUEST_LATENCY
from common.trace import get_trace_id, set_trace_id
from eval.runner import EvalRunner
from generation.providers import GenerationProviders
from generation.service import GenerationService
from ingest.chunker import HeadingAwareChunker
from ingest.parser import DocumentParser
from ingest.pipeline import IngestionPipeline
from retrieval.embedding import Embedder
from retrieval.qdrant_store import QdrantStore
from retrieval.reranker import Reranker
from retrieval.service import RetrievalService

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger(__name__)

parser = DocumentParser(settings)
chunker = HeadingAwareChunker(settings)
embedder = Embedder(settings)
qdrant_store = QdrantStore(settings)
reranker = Reranker(settings)
retrieval_service = RetrievalService(settings, qdrant_store, embedder, reranker)
providers = GenerationProviders(settings)
generation_service = GenerationService(settings, providers)
query_cache = QueryCache(settings.query_cache_maxsize, settings.query_cache_ttl_seconds)
orchestrator = RagOrchestrator(retrieval_service, generation_service, query_cache)
ingestion_pipeline = IngestionPipeline(
    settings=settings,
    parser=parser,
    chunker=chunker,
    embedder=embedder,
    qdrant_store=qdrant_store,
    retrieval_service=retrieval_service,
)
eval_runner = EvalRunner(orchestrator)


app = FastAPI(title='BeeCount RAG Lab', version='0.1.0')
app.include_router(create_openai_router(orchestrator, settings))


@app.middleware('http')
async def trace_and_metrics_middleware(request: Request, call_next):
    trace_id = request.headers.get('x-trace-id', str(uuid.uuid4()))
    set_trace_id(trace_id)

    started = asyncio.get_event_loop().time()
    status = 'ok'
    response: Response | None = None
    try:
        response = await call_next(request)
        return response
    except Exception:  # noqa: BLE001
        status = 'error'
        raise
    finally:
        elapsed = asyncio.get_event_loop().time() - started
        path = request.url.path
        REQUEST_COUNT.labels(endpoint=path, status=status).inc()
        REQUEST_LATENCY.labels(endpoint=path).observe(elapsed)
        if response is not None:
            response.headers['x-trace-id'] = trace_id


def _stream_answer_chunks(answer: str) -> list[str]:
    if not answer:
        return []

    if ' ' in answer:
        words = answer.split(' ')
        return [word + (' ' if idx < len(words) - 1 else '') for idx, word in enumerate(words)]

    step = 12
    return [answer[i : i + step] for i in range(0, len(answer), step)]


@app.get('/healthz')
def healthz() -> dict:
    return {'status': 'ok'}


@app.get('/readyz')
def readyz() -> dict:
    try:
        qdrant_store.client.get_collections()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=f'qdrant unavailable: {exc}') from exc
    return {'status': 'ready'}


@app.get('/metrics')
def metrics() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post('/v1/query', response_model=QueryResponse)
async def query(request: QueryRequest):
    trace_id = get_trace_id()
    try:
        result = await orchestrator.run_query(request, trace_id=trace_id)

        if not request.stream:
            return result

        meta = result.model_dump(mode='json')
        answer = meta.pop('answer')

        async def event_stream():
            yield f"event: meta\ndata: {orjson.dumps(meta).decode('utf-8')}\n\n"
            for piece in _stream_answer_chunks(answer):
                yield f"event: token\ndata: {orjson.dumps({'token': piece}).decode('utf-8')}\n\n"
                await asyncio.sleep(0)
            yield f"event: done\ndata: {orjson.dumps({'answer': answer}).decode('utf-8')}\n\n"

        return StreamingResponse(event_stream(), media_type='text/event-stream')
    except Exception as exc:  # noqa: BLE001
        logger.exception('query failed')
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post('/v1/ingest/rebuild', response_model=IngestResponse)
async def ingest_rebuild():
    trace_id = get_trace_id()
    try:
        payload = await run_in_threadpool(ingestion_pipeline.rebuild)
        query_cache.clear()
        return IngestResponse(action='rebuild', trace_id=trace_id, **payload)
    except Exception as exc:  # noqa: BLE001
        logger.exception('rebuild failed')
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post('/v1/ingest/incremental', response_model=IngestResponse)
async def ingest_incremental():
    trace_id = get_trace_id()
    try:
        payload = await run_in_threadpool(ingestion_pipeline.incremental)
        query_cache.clear()
        return IngestResponse(action='incremental', trace_id=trace_id, **payload)
    except Exception as exc:  # noqa: BLE001
        logger.exception('incremental failed')
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post('/v1/eval/run')
async def eval_run(request: EvalRequest):
    trace_id = get_trace_id()
    try:
        return await eval_runner.run(request, trace_id=trace_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        logger.exception('eval failed')
        raise HTTPException(status_code=500, detail=str(exc)) from exc

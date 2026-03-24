from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ChunkRecord(BaseModel):
    doc_id: str
    chunk_id: str
    locale: Literal['zh', 'en']
    title: str
    heading: str
    url: str
    content: str
    tokens: int
    hash: str
    updated_at: datetime


class Citation(BaseModel):
    url: str
    title: str
    heading: str
    chunk_id: str
    score: float
    locale: Literal['zh', 'en']


class RetrievedChunk(BaseModel):
    chunk_id: str
    doc_id: str
    locale: Literal['zh', 'en']
    title: str
    heading: str
    url: str
    content: str
    score: float
    source_mode: Literal['dense', 'bm25', 'hybrid', 'reranked']


class QueryRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    locale: Literal['zh', 'en', 'auto'] = 'auto'
    top_k: int = Field(default=8, ge=1, le=50)
    mode: Literal['hybrid', 'dense', 'bm25'] = 'hybrid'
    use_reranker: bool = False
    generation_provider: Literal['cloud', 'local'] = 'cloud'
    stream: bool = False


class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
    retrieved_chunks: list[RetrievedChunk]
    latency_ms: int
    trace_id: str
    provider_used: Literal['cloud', 'local']
    fallback_used: bool = False
    fallback_reason: str | None = None


class IngestResponse(BaseModel):
    action: Literal['rebuild', 'incremental']
    docs_total: int
    chunks_total: int
    added_docs: int = 0
    updated_docs: int = 0
    deleted_docs: int = 0
    failed_files: list[str] = Field(default_factory=list)
    latency_ms: int
    trace_id: str


class EvalCase(BaseModel):
    case_id: str
    locale: Literal['zh', 'en', 'auto'] = 'auto'
    query: str
    expected_urls: list[str]


class EvalRequest(BaseModel):
    dataset_path: str | None = None
    mode: Literal['hybrid', 'dense', 'bm25'] = 'hybrid'
    top_k: int = Field(default=8, ge=1, le=50)
    use_reranker: bool = False
    generation_provider: Literal['cloud', 'local'] = 'cloud'


class EvalMetrics(BaseModel):
    total_cases: int
    recall_at_k: float
    mrr: float
    citation_precision: float
    latency_avg_ms: float
    latency_p95_ms: float


class EvalResponse(BaseModel):
    dataset_version: str
    metrics: EvalMetrics
    sampled_failures: list[dict]
    trace_id: str

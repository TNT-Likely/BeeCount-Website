from __future__ import annotations

try:
    from prometheus_client import Counter, Histogram
except Exception:  # noqa: BLE001
    class _NoopMetric:
        def labels(self, **kwargs):  # noqa: ANN003
            return self

        def inc(self, *args, **kwargs):  # noqa: ANN002, ANN003
            return None

        def observe(self, *args, **kwargs):  # noqa: ANN002, ANN003
            return None

    def Counter(*args, **kwargs):  # noqa: ANN002, ANN003
        return _NoopMetric()

    def Histogram(*args, **kwargs):  # noqa: ANN002, ANN003
        return _NoopMetric()


REQUEST_COUNT = Counter(
    'rag_requests_total',
    'Total number of RAG API requests',
    ['endpoint', 'status'],
)

REQUEST_LATENCY = Histogram(
    'rag_request_latency_seconds',
    'Request latency in seconds',
    ['endpoint'],
)

FALLBACK_COUNT = Counter(
    'rag_generation_fallback_total',
    'Number of generation fallback events across providers',
)

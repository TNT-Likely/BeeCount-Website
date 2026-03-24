from __future__ import annotations

from pathlib import Path

from api.orchestrator import RagOrchestrator
from common.models import EvalMetrics, EvalRequest, EvalResponse, QueryRequest
from common.paths import eval_dataset_path
from eval.dataset import load_eval_dataset
from eval.metrics import percentile


class EvalRunner:
    def __init__(self, orchestrator: RagOrchestrator) -> None:
        self._orchestrator = orchestrator

    async def run(self, request: EvalRequest, trace_id: str) -> EvalResponse:
        dataset_file = Path(request.dataset_path) if request.dataset_path else eval_dataset_path()
        if not dataset_file.exists():
            raise FileNotFoundError(f'dataset not found: {dataset_file}')

        dataset_version, cases = load_eval_dataset(dataset_file)

        recall_hits = 0
        reciprocal_rank_sum = 0.0
        citation_precision_sum = 0.0
        latencies: list[float] = []
        failures: list[dict] = []

        for case in cases:
            query_req = QueryRequest(
                query=case.query,
                locale=case.locale,
                top_k=request.top_k,
                mode=request.mode,
                use_reranker=request.use_reranker,
                generation_provider=request.generation_provider,
            )
            result = await self._orchestrator.run_query(query_req, trace_id=trace_id, disable_cache=True)
            latencies.append(float(result.latency_ms))

            expected = set(case.expected_urls)
            rank = None
            for idx, chunk in enumerate(result.retrieved_chunks, start=1):
                if chunk.url in expected:
                    rank = idx
                    break

            if rank is not None and rank <= request.top_k:
                recall_hits += 1
                reciprocal_rank_sum += 1.0 / rank
            elif len(failures) < 20:
                failures.append(
                    {
                        'case_id': case.case_id,
                        'query': case.query,
                        'expected_urls': case.expected_urls,
                        'top_retrieved_urls': [c.url for c in result.retrieved_chunks[:5]],
                    }
                )

            if result.citations:
                correct = sum(1 for c in result.citations if c.url in expected)
                citation_precision_sum += correct / len(result.citations)

        total = len(cases)
        metrics = EvalMetrics(
            total_cases=total,
            recall_at_k=(recall_hits / total) if total else 0.0,
            mrr=(reciprocal_rank_sum / total) if total else 0.0,
            citation_precision=(citation_precision_sum / total) if total else 0.0,
            latency_avg_ms=(sum(latencies) / len(latencies)) if latencies else 0.0,
            latency_p95_ms=percentile(latencies, 0.95),
        )

        return EvalResponse(
            dataset_version=dataset_version,
            metrics=metrics,
            sampled_failures=failures,
            trace_id=trace_id,
        )

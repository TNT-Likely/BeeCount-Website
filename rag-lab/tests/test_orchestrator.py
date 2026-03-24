import asyncio

from api.orchestrator import RagOrchestrator
from common.cache import QueryCache
from common.models import QueryRequest


class FakeRetrieval:
    def __init__(self) -> None:
        self.calls = 0

    def retrieve(self, **kwargs):
        self.calls += 1
        return [], 'zh'


class FakeGeneration:
    async def generate(self, **kwargs):
        return '我没有在文档中找到足够的信息来回答这个问题。', 'cloud', False, None


def test_orchestrator_uses_cache() -> None:
    retrieval = FakeRetrieval()
    generation = FakeGeneration()
    cache = QueryCache(maxsize=10, ttl_seconds=100)
    orchestrator = RagOrchestrator(retrieval, generation, cache)

    req = QueryRequest(query='test', locale='zh', mode='hybrid', generation_provider='cloud')
    asyncio.run(orchestrator.run_query(req, trace_id='t1'))
    asyncio.run(orchestrator.run_query(req, trace_id='t2'))

    assert retrieval.calls == 1

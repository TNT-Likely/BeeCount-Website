import asyncio
from datetime import datetime, timezone

from common.config import Settings
from generation.service import GenerationService
from retrieval.types import SearchHit
from common.models import ChunkRecord


def _hit() -> SearchHit:
    chunk = ChunkRecord(
        doc_id='zh:test',
        chunk_id='zh:test#0',
        locale='zh',
        title='T',
        heading='H',
        url='/docs/t',
        content='测试内容',
        tokens=2,
        hash='h',
        updated_at=datetime.now(timezone.utc),
    )
    return SearchHit(chunk=chunk, score=1.0, source_mode='hybrid')


class _Providers:
    def __init__(self, local_error: bool = False, cloud_error: bool = False) -> None:
        self.local_error = local_error
        self.cloud_error = cloud_error

    async def local_chat(self, messages):
        if self.local_error:
            raise RuntimeError('local failed')
        return 'local answer'

    async def cloud_chat(self, messages):
        if self.cloud_error:
            raise RuntimeError('cloud failed')
        return 'cloud answer'


def test_local_to_cloud_fallback() -> None:
    settings = Settings(local_fallback_enabled=True)
    service = GenerationService(settings, _Providers(local_error=True, cloud_error=False))

    text, provider, fallback_used, reason = asyncio.run(
        service.generate(
            query='q',
            locale='zh',
            hits=[_hit()],
            generation_provider='local',
            fallback_provider='cloud',
        )
    )

    assert text == 'cloud answer'
    assert provider == 'cloud'
    assert fallback_used is True
    assert reason is not None and 'local_error' in reason


def test_cloud_to_local_backward_compatible_fallback() -> None:
    settings = Settings(local_fallback_enabled=True)
    service = GenerationService(settings, _Providers(local_error=False, cloud_error=True))

    text, provider, fallback_used, reason = asyncio.run(
        service.generate(
            query='q',
            locale='zh',
            hits=[_hit()],
            generation_provider='cloud',
        )
    )

    assert text == 'local answer'
    assert provider == 'local'
    assert fallback_used is True
    assert reason is not None and 'cloud_error' in reason

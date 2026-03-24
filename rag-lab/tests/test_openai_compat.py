import pytest

pytest.importorskip('fastapi')

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.openai_compat import create_openai_router
from common.config import Settings
from common.models import QueryResponse


class _FakeOrchestrator:
    async def run_query(self, request, trace_id, disable_cache=False, **kwargs):
        return QueryResponse(
            answer='mock answer',
            citations=[],
            retrieved_chunks=[],
            latency_ms=10,
            trace_id=trace_id,
            provider_used='local',
            fallback_used=False,
            fallback_reason=None,
        )


def _create_app(settings: Settings) -> TestClient:
    app = FastAPI()
    app.include_router(create_openai_router(_FakeOrchestrator(), settings))
    return TestClient(app)


def test_models_endpoint_returns_local_and_cloud() -> None:
    client = _create_app(Settings())
    resp = client.get('/v1/models')
    assert resp.status_code == 200
    data = resp.json()['data']
    providers = {item['metadata']['provider'] for item in data}
    assert providers == {'local', 'cloud'}


def test_auth_when_key_set() -> None:
    client = _create_app(Settings(openai_compat_api_key='secret'))

    r1 = client.get('/v1/models')
    assert r1.status_code == 401

    r2 = client.get('/v1/models', headers={'Authorization': 'Bearer wrong'})
    assert r2.status_code == 401

    r3 = client.get('/v1/models', headers={'Authorization': 'Bearer secret'})
    assert r3.status_code == 200


def test_chat_completion_non_stream() -> None:
    client = _create_app(Settings())
    payload = {
        'model': 'beecount-rag',
        'messages': [{'role': 'user', 'content': 'hello'}],
        'stream': False,
    }
    resp = client.post('/v1/chat/completions', json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body['object'] == 'chat.completion'
    assert body['choices'][0]['message']['content'] == 'mock answer'


def test_chat_completion_stream() -> None:
    client = _create_app(Settings())
    payload = {
        'model': 'beecount-rag',
        'messages': [{'role': 'user', 'content': 'hello'}],
        'stream': True,
    }

    with client.stream('POST', '/v1/chat/completions', json=payload) as resp:
        assert resp.status_code == 200
        text = ''.join(resp.iter_text())

    assert 'chat.completion.chunk' in text
    assert 'data: [DONE]' in text

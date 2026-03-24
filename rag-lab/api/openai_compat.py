from __future__ import annotations

import time
import uuid

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse

from api.openai_types import (
    OpenAIChatCompletionRequest,
    OpenAIChatCompletionResponse,
    OpenAIChoice,
    OpenAIChoiceMessage,
    OpenAIModelListResponse,
    OpenAIModelObject,
    OpenAIStreamChoice,
    OpenAIStreamChunk,
    OpenAIStreamDelta,
    OpenAIUsage,
)
from api.openai_utils import estimate_usage, extract_query_and_system, split_answer_chunks
from common.config import Settings
from common.models import QueryRequest
from common.trace import get_trace_id


def create_openai_router(orchestrator, settings: Settings) -> APIRouter:
    router = APIRouter()

    def _error(status_code: int, message: str, code: str, error_type: str = 'invalid_request_error') -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={
                'error': {
                    'message': message,
                    'type': error_type,
                    'param': None,
                    'code': code,
                }
            },
        )

    def _validate_auth(request: Request) -> JSONResponse | None:
        expected = settings.openai_compat_api_key.strip()
        if not expected:
            return None

        auth = request.headers.get('authorization', '')
        if not auth.startswith('Bearer '):
            return _error(401, 'Missing bearer token.', 'invalid_api_key', 'authentication_error')

        token = auth[len('Bearer ') :].strip()
        if token != expected:
            return _error(401, 'Invalid API key provided.', 'invalid_api_key', 'authentication_error')
        return None

    def _normalize_provider(name: str, default: str) -> str:
        value = (name or '').strip().lower()
        if value in ('local', 'cloud'):
            return value
        return default

    @router.get('/v1/models')
    async def list_models(request: Request):
        auth_err = _validate_auth(request)
        if auth_err is not None:
            return auth_err

        now = int(time.time())
        response = OpenAIModelListResponse(
            data=[
                OpenAIModelObject(
                    id=settings.ollama_model,
                    created=now,
                    metadata={'provider': 'local'},
                ),
                OpenAIModelObject(
                    id=settings.cloud_model,
                    created=now,
                    metadata={'provider': 'cloud'},
                ),
            ]
        )
        return response.model_dump(mode='json')

    @router.post('/v1/chat/completions')
    async def chat_completions(payload: OpenAIChatCompletionRequest, request: Request):
        auth_err = _validate_auth(request)
        if auth_err is not None:
            return auth_err

        query, system_prompt = extract_query_and_system(payload.messages)
        if not query:
            return _error(400, 'No user message found in request.messages.', 'invalid_messages')

        default_provider = _normalize_provider(settings.openai_compat_default_provider, 'local')
        fallback_provider = _normalize_provider(settings.openai_compat_fallback_provider, 'cloud')
        if fallback_provider == default_provider:
            fallback_provider = None

        query_req = QueryRequest(
            query=query,
            locale='auto',
            top_k=8,
            mode='hybrid',
            use_reranker=False,
            generation_provider=default_provider,
        )

        trace_id = get_trace_id()
        try:
            rag_response = await orchestrator.run_query(
                query_req,
                trace_id=trace_id,
                system_prompt_override=system_prompt,
                fallback_provider=fallback_provider,
            )
        except Exception as exc:  # noqa: BLE001
            return _error(500, f'RAG execution failed: {exc}', 'rag_execution_failed', 'server_error')

        created = int(time.time())
        completion_id = f'chatcmpl-{uuid.uuid4().hex}'
        model_name = payload.model
        prompt_tokens, completion_tokens, total_tokens = estimate_usage(payload.messages, rag_response.answer)

        if payload.stream and settings.openai_compat_enable_stream:
            async def event_stream():
                first = OpenAIStreamChunk(
                    id=completion_id,
                    created=created,
                    model=model_name,
                    choices=[
                        OpenAIStreamChoice(
                            index=0,
                            delta=OpenAIStreamDelta(role='assistant'),
                            finish_reason=None,
                        )
                    ],
                )
                yield f'data: {first.model_dump_json()}\n\n'

                for piece in split_answer_chunks(rag_response.answer):
                    chunk = OpenAIStreamChunk(
                        id=completion_id,
                        created=created,
                        model=model_name,
                        choices=[
                            OpenAIStreamChoice(
                                index=0,
                                delta=OpenAIStreamDelta(content=piece),
                                finish_reason=None,
                            )
                        ],
                    )
                    yield f'data: {chunk.model_dump_json()}\n\n'

                final = OpenAIStreamChunk(
                    id=completion_id,
                    created=created,
                    model=model_name,
                    choices=[
                        OpenAIStreamChoice(
                            index=0,
                            delta=OpenAIStreamDelta(),
                            finish_reason='stop',
                        )
                    ],
                )
                yield f'data: {final.model_dump_json()}\n\n'
                yield 'data: [DONE]\n\n'

            return StreamingResponse(event_stream(), media_type='text/event-stream')

        resp = OpenAIChatCompletionResponse(
            id=completion_id,
            created=created,
            model=model_name,
            choices=[
                OpenAIChoice(
                    index=0,
                    message=OpenAIChoiceMessage(content=rag_response.answer),
                    finish_reason='stop',
                )
            ],
            usage=OpenAIUsage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
            ),
        )
        return resp.model_dump(mode='json')

    return router

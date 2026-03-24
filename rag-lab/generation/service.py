from __future__ import annotations

from common.config import Settings
from common.telemetry import FALLBACK_COUNT
from generation.prompts import build_system_prompt, build_user_prompt, fallback_message
from generation.providers import GenerationProviders
from retrieval.types import SearchHit


class GenerationService:
    def __init__(self, settings: Settings, providers: GenerationProviders) -> None:
        self._settings = settings
        self._providers = providers

    async def generate(
        self,
        query: str,
        locale: str,
        hits: list[SearchHit],
        generation_provider: str,
        *,
        system_prompt_override: str | None = None,
        fallback_provider: str | None = None,
    ) -> tuple[str, str, bool, str | None]:
        if not hits:
            return fallback_message(locale), generation_provider, False, None

        system_prompt = system_prompt_override or build_system_prompt(locale)
        user_prompt = build_user_prompt(
            query=query,
            hits=hits,
            max_chunks=self._settings.max_context_chunks,
        )

        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt},
        ]

        provider_chain = self._resolve_provider_chain(
            primary=generation_provider,
            fallback_provider=fallback_provider,
        )

        first_error: Exception | None = None
        first_provider: str | None = None

        for idx, provider in enumerate(provider_chain):
            try:
                text = await self._call_provider(provider, messages)
                if idx == 0:
                    return self._normalize_answer(text, locale), provider, False, None
                FALLBACK_COUNT.inc()
                reason = f'{first_provider}_error: {first_error}' if first_error else None
                return self._normalize_answer(text, locale), provider, True, reason
            except Exception as exc:  # noqa: BLE001
                if idx == 0:
                    first_error = exc
                    first_provider = provider
                    continue
                raise

        if first_error is not None:
            raise first_error
        raise RuntimeError('No generation provider available')

    @staticmethod
    def _normalize_answer(answer: str, locale: str) -> str:
        cleaned = answer.strip()
        if cleaned:
            return cleaned
        return fallback_message(locale)

    async def _call_provider(self, provider: str, messages: list[dict[str, str]]) -> str:
        if provider == 'local':
            return await self._providers.local_chat(messages)
        if provider == 'cloud':
            return await self._providers.cloud_chat(messages)
        raise RuntimeError(f'Unsupported generation provider: {provider}')

    def _resolve_provider_chain(self, primary: str, fallback_provider: str | None) -> list[str]:
        chain = [primary]

        if fallback_provider is not None and fallback_provider != primary:
            chain.append(fallback_provider)
            return chain

        # Backward compatibility for existing /v1/query behavior.
        if primary == 'cloud' and self._settings.local_fallback_enabled:
            chain.append('local')
        return chain

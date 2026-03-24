from __future__ import annotations

from typing import Any

import httpx

from common.config import Settings


class GenerationProviders:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def cloud_chat(self, messages: list[dict[str, str]]) -> str:
        if not self._settings.cloud_base_url or not self._settings.cloud_api_key:
            raise RuntimeError('CLOUD_BASE_URL or CLOUD_API_KEY is not configured')

        base_url = self._settings.cloud_base_url.rstrip('/')
        url = f'{base_url}/chat/completions'

        payload = {
            'model': self._settings.cloud_model,
            'messages': messages,
            'temperature': 0.2,
        }
        headers = {
            'Authorization': f'Bearer {self._settings.cloud_api_key}',
            'Content-Type': 'application/json',
        }

        async with httpx.AsyncClient(timeout=self._settings.http_timeout_seconds) as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()

        return self._extract_content(data)

    async def local_chat(self, messages: list[dict[str, str]]) -> str:
        base_url = self._settings.ollama_base_url.rstrip('/')
        url = f'{base_url}/api/chat'
        payload = {
            'model': self._settings.ollama_model,
            'messages': messages,
            'stream': False,
            'options': {'temperature': 0.2},
        }

        async with httpx.AsyncClient(timeout=self._settings.http_timeout_seconds) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()

        message = data.get('message') or {}
        return str(message.get('content', '')).strip()

    @staticmethod
    def _extract_content(data: dict[str, Any]) -> str:
        choices = data.get('choices') or []
        if not choices:
            return ''

        message = choices[0].get('message') or {}
        content = message.get('content', '')

        if isinstance(content, str):
            return content.strip()

        if isinstance(content, list):
            segments: list[str] = []
            for item in content:
                if isinstance(item, dict) and 'text' in item:
                    segments.append(str(item['text']))
            return ''.join(segments).strip()

        return str(content).strip()

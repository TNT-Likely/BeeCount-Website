from __future__ import annotations

from retrieval.types import SearchHit


def build_system_prompt(locale: str) -> str:
    if locale == 'en':
        return (
            'You are BeeCount documentation assistant. '\
            'Answer strictly based on provided context snippets. '\
            'If context is insufficient, explicitly say you are not sure and suggest checking docs. '\
            'Never fabricate product behavior or unsupported steps.'
        )
    return (
        '你是 BeeCount 文档助手。仅基于提供的文档片段回答。'
        '如果上下文不足，请明确说“不确定/未在文档中找到”。'
        '禁止编造产品功能或步骤。'
    )


def build_user_prompt(query: str, hits: list[SearchHit], max_chunks: int) -> str:
    selected = hits[:max_chunks]
    parts: list[str] = []
    for idx, hit in enumerate(selected, start=1):
        parts.append(
            f"[{idx}] {hit.chunk.title} | {hit.chunk.heading} | {hit.chunk.url}\n{hit.chunk.content}"
        )

    context = '\n\n'.join(parts)
    return (
        f'Question:\n{query}\n\n'
        f'Context:\n{context}\n\n'
        'Answer requirements:\n'
        '1) Use only context facts.\n'
        '2) Keep answer concise and actionable.\n'
        '3) If context is not enough, say unknown explicitly.'
    )


def fallback_message(locale: str) -> str:
    if locale == 'en':
        return 'I could not find enough information in the docs for this question.'
    return '我没有在文档中找到足够的信息来回答这个问题。'

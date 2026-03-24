from __future__ import annotations

from common.text import count_tokens


def _content_to_text(content: str | list[dict] | None) -> str:
    if content is None:
        return ''
    if isinstance(content, str):
        return content.strip()

    texts: list[str] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        if 'text' in item and isinstance(item['text'], str):
            texts.append(item['text'])
            continue
        if item.get('type') == 'text' and isinstance(item.get('text'), str):
            texts.append(item['text'])
    return '\n'.join(t for t in texts if t).strip()


def extract_query_and_system(messages) -> tuple[str, str | None]:
    latest_user = ''
    latest_system: str | None = None

    for message in messages:
        role = message.role
        text = _content_to_text(message.content)
        if role == 'system' and text:
            latest_system = text
        elif role == 'user' and text:
            latest_user = text

    return latest_user, latest_system


def split_answer_chunks(answer: str) -> list[str]:
    if not answer:
        return []
    if ' ' in answer:
        parts = answer.split(' ')
        return [p + (' ' if i < len(parts) - 1 else '') for i, p in enumerate(parts)]
    step = 12
    return [answer[i : i + step] for i in range(0, len(answer), step)]


def estimate_usage(prompt_messages, answer: str) -> tuple[int, int, int]:
    prompt_text = '\n'.join(_content_to_text(m.content) for m in prompt_messages)
    prompt_tokens = count_tokens(prompt_text)
    completion_tokens = count_tokens(answer)
    return prompt_tokens, completion_tokens, prompt_tokens + completion_tokens

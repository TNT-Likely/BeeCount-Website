import re
from typing import Iterable

TOKEN_RE = re.compile(r"[\u4e00-\u9fff]|[A-Za-z0-9_]+")
ZH_RE = re.compile(r"[\u4e00-\u9fff]")


def tokenize(text: str) -> list[str]:
    return [m.group(0).lower() for m in TOKEN_RE.finditer(text)]


def count_tokens(text: str) -> int:
    return len(tokenize(text))


def detect_locale(query: str) -> str:
    return 'zh' if ZH_RE.search(query) else 'en'


def sliding_chunks(text: str, chunk_size: int, overlap: int) -> Iterable[str]:
    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    step = max(1, chunk_size - overlap)
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start += step
    return chunks

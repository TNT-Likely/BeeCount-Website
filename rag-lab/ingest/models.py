from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(slots=True)
class ParsedSection:
    heading: str
    content: str


@dataclass(slots=True)
class SourceDocument:
    source_path: Path
    relative_path: str
    locale: str
    doc_id: str
    url: str
    title: str
    updated_at: datetime
    file_hash: str
    sections: list[ParsedSection]

    @property
    def manifest_key(self) -> str:
        return f'{self.locale}:{self.relative_path}'

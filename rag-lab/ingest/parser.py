from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path

from common.config import Settings
from ingest.models import ParsedSection, SourceDocument

HEADING_RE = re.compile(r'^(#{1,6})\s+(.+?)\s*$')


class DocumentParser:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def discover(self) -> list[SourceDocument]:
        docs: list[SourceDocument] = []
        docs.extend(self._discover_locale(self._settings.docs_zh_dir, 'zh'))
        docs.extend(self._discover_locale(self._settings.docs_en_dir, 'en'))
        return sorted(docs, key=lambda d: d.url)

    def _discover_locale(self, root: Path, locale: str) -> list[SourceDocument]:
        if not root.exists():
            return []

        result: list[SourceDocument] = []
        for file_path in sorted(root.rglob('*.md')):
            rel = file_path.relative_to(root).as_posix()
            url = self._build_url(rel, locale)
            slug = rel[:-3]
            doc_id = f'{locale}:{slug}'

            text = file_path.read_text(encoding='utf-8')
            normalized = text.replace('\r\n', '\n')
            body = self._strip_frontmatter(normalized)
            sections, title = self._split_sections(body, default_title=file_path.stem)
            file_hash = hashlib.sha1(normalized.encode('utf-8')).hexdigest()
            updated_at = datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc)

            result.append(
                SourceDocument(
                    source_path=file_path,
                    relative_path=rel,
                    locale=locale,
                    doc_id=doc_id,
                    url=url,
                    title=title,
                    updated_at=updated_at,
                    file_hash=file_hash,
                    sections=sections,
                )
            )
        return result

    @staticmethod
    def _strip_frontmatter(text: str) -> str:
        if text.startswith('---\n'):
            end = text.find('\n---\n', 4)
            if end != -1:
                return text[end + 5 :]
        return text

    @staticmethod
    def _split_sections(text: str, default_title: str) -> tuple[list[ParsedSection], str]:
        lines = text.splitlines()
        sections: list[ParsedSection] = []
        stack: list[str] = []
        buf: list[str] = []
        title = default_title

        def flush() -> None:
            content = '\n'.join(buf).strip()
            if not content:
                return
            heading = ' > '.join(stack) if stack else title
            sections.append(ParsedSection(heading=heading, content=content))

        for line in lines:
            m = HEADING_RE.match(line)
            if m:
                flush()
                buf.clear()
                level = len(m.group(1))
                heading_text = m.group(2).strip()
                if level == 1:
                    title = heading_text
                if len(stack) >= level:
                    stack[:] = stack[: level - 1]
                stack.append(heading_text)
            else:
                buf.append(line)

        flush()

        if not sections:
            sections = [ParsedSection(heading=title, content=text.strip())]
        return sections, title

    @staticmethod
    def _build_url(relative_md_path: str, locale: str) -> str:
        slug = relative_md_path[:-3] if relative_md_path.endswith('.md') else relative_md_path
        if slug.endswith('/index'):
            slug = slug[: -len('/index')]
        prefix = '/docs/' if locale == 'zh' else '/en/docs/'
        return f'{prefix}{slug}'.replace('//', '/')

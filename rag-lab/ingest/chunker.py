from __future__ import annotations

import hashlib

from common.config import Settings
from common.models import ChunkRecord
from common.text import count_tokens, sliding_chunks
from ingest.models import SourceDocument


class HeadingAwareChunker:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def chunk_document(self, doc: SourceDocument) -> list[ChunkRecord]:
        chunks: list[ChunkRecord] = []
        cursor = 0

        for section in doc.sections:
            section_text = section.content.strip()
            if not section_text:
                continue

            for part in sliding_chunks(
                section_text,
                chunk_size=self._settings.chunk_size,
                overlap=self._settings.chunk_overlap,
            ):
                content = part.strip()
                if not content:
                    continue
                chunk_id = f'{doc.doc_id}#{cursor}'
                payload_hash = hashlib.sha1(content.encode('utf-8')).hexdigest()
                chunks.append(
                    ChunkRecord(
                        doc_id=doc.doc_id,
                        chunk_id=chunk_id,
                        locale=doc.locale,  # type: ignore[arg-type]
                        title=doc.title,
                        heading=section.heading,
                        url=doc.url,
                        content=content,
                        tokens=count_tokens(content),
                        hash=payload_hash,
                        updated_at=doc.updated_at,
                    )
                )
                cursor += 1

        return chunks

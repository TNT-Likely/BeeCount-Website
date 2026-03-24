from datetime import datetime, timezone
from pathlib import Path

from common.config import Settings
from ingest.chunker import HeadingAwareChunker
from ingest.models import ParsedSection, SourceDocument


def test_chunker_respects_size_and_overlap(tmp_path: Path) -> None:
    settings = Settings(
        chunk_size=10,
        chunk_overlap=2,
        docs_zh_dir=tmp_path,
        docs_en_dir=tmp_path,
        data_dir=tmp_path / 'data',
    )
    chunker = HeadingAwareChunker(settings)

    doc = SourceDocument(
        source_path=tmp_path / 'a.md',
        relative_path='a.md',
        locale='zh',
        doc_id='zh:a',
        url='/docs/a',
        title='A',
        updated_at=datetime.now(timezone.utc),
        file_hash='x',
        sections=[ParsedSection(heading='A', content='0123456789abcdefghij')],
    )

    chunks = chunker.chunk_document(doc)
    assert len(chunks) >= 2
    assert chunks[0].content == '0123456789'
    assert chunks[1].content.startswith('89')

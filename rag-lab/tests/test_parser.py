from pathlib import Path

from common.config import Settings
from ingest.parser import DocumentParser


def test_parser_builds_locale_and_url(tmp_path: Path) -> None:
    zh_root = tmp_path / 'docs'
    en_root = tmp_path / 'en'
    zh_root.mkdir(parents=True)
    (en_root / 'cloud-sync').mkdir(parents=True)

    (zh_root / 'faq.md').write_text('# 常见问题\n\n内容', encoding='utf-8')
    (en_root / 'cloud-sync' / 's3.md').write_text('# S3 Sync\n\nBody', encoding='utf-8')

    settings = Settings(
        docs_zh_dir=zh_root,
        docs_en_dir=en_root,
        data_dir=tmp_path / 'data',
    )
    parser = DocumentParser(settings)
    docs = parser.discover()

    urls = {doc.url for doc in docs}
    assert '/docs/faq' in urls
    assert '/en/docs/cloud-sync/s3' in urls

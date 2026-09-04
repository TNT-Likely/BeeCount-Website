import sqlite3

import build_docs_index
from build_docs_index import DOCS_ZH, Chunk, collect_chunks, write_sqlite


def test_short_heading_section_is_indexed_with_document_title_context():
    """A short, actionable H2 must remain independently retrievable."""
    chunks = collect_chunks(DOCS_ZH, "zh")

    delete_attachment = next(
        chunk
        for chunk in chunks
        if chunk.doc_path == "record/attachment.md" and chunk.section == "删除附件"
    )

    assert delete_attachment.content == (
        "# 交易附件\n\n"
        "## 删除附件\n\n"
        "1. 进入交易编辑页面\n"
        "2. 长按要删除的附件图片\n"
        "3. 确认删除"
    )


def test_written_index_has_trigram_keyword_index_for_document_metadata(tmp_path):
    index_path = tmp_path / "docs-index.zh.sqlite"
    chunk = Chunk(
        content="# 交易附件\\n\\n## 删除附件\\n\\n确认删除。",
        doc_path="record/attachment.md",
        doc_title="交易附件",
        section="删除附件",
        url="https://count.beejz.com/docs/record/attachment",
        vector=[1.0, 0.0],
    )

    write_sqlite([chunk], index_path, dim=2)

    conn = sqlite3.connect(index_path)
    try:
        matched = conn.execute(
            "SELECT rowid FROM chunks_fts WHERE chunks_fts MATCH ?",
            ('"删除附件"',),
        ).fetchall()
    finally:
        conn.close()

    assert matched == [(1,)]


def test_corpus_hash_changes_when_index_format_version_changes(tmp_path, monkeypatch):
    docs_zh = tmp_path / "docs"
    docs_en = tmp_path / "en"
    docs_zh.mkdir()
    docs_en.mkdir()
    (docs_zh / "example.md").write_text("# 示例\n", encoding="utf-8")
    monkeypatch.setattr(build_docs_index, "ROOT", tmp_path)
    monkeypatch.setattr(build_docs_index, "DOCS_ZH", docs_zh)
    monkeypatch.setattr(build_docs_index, "DOCS_EN", docs_en)

    monkeypatch.setattr(build_docs_index, "INDEX_FORMAT_VERSION", "1")
    old_hash = build_docs_index.compute_corpus_hash()
    monkeypatch.setattr(build_docs_index, "INDEX_FORMAT_VERSION", "2")
    new_hash = build_docs_index.compute_corpus_hash()

    assert new_hash != old_hash

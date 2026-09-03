from pathlib import Path

from build_docs_index import DOCS_ZH, collect_chunks


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

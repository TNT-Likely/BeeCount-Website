from datetime import datetime, timezone

from common.models import ChunkRecord
from retrieval.hybrid import fuse_hits
from retrieval.types import SearchHit


def _chunk(cid: str) -> ChunkRecord:
    return ChunkRecord(
        doc_id='zh:test',
        chunk_id=cid,
        locale='zh',
        title='T',
        heading='H',
        url='/docs/t',
        content='abc',
        tokens=1,
        hash='h',
        updated_at=datetime.now(timezone.utc),
    )


def test_hybrid_fusion_prefers_combined_score() -> None:
    dense = [SearchHit(chunk=_chunk('a'), score=0.9, source_mode='dense')]
    bm25 = [
        SearchHit(chunk=_chunk('a'), score=2.0, source_mode='bm25'),
        SearchHit(chunk=_chunk('b'), score=3.0, source_mode='bm25'),
    ]

    merged = fuse_hits(dense, bm25, alpha=0.6, limit=5)
    assert merged
    assert merged[0].chunk.chunk_id == 'a'

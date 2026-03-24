from dataclasses import dataclass

from common.models import ChunkRecord


@dataclass(slots=True)
class SearchHit:
    chunk: ChunkRecord
    score: float
    source_mode: str

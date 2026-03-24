from pathlib import Path

from .config import Settings


def manifest_path(settings: Settings) -> Path:
    return settings.data_dir / 'ingest_manifest.json'


def bm25_index_path(settings: Settings) -> Path:
    return settings.data_dir / 'cache' / 'bm25_index.json'


def eval_dataset_path() -> Path:
    return Path(__file__).resolve().parent.parent / 'eval' / 'datasets' / 'qa_gold.json'

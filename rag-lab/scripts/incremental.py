#!/usr/bin/env python3
from __future__ import annotations

from common.config import get_settings
from ingest.chunker import HeadingAwareChunker
from ingest.parser import DocumentParser
from ingest.pipeline import IngestionPipeline
from retrieval.embedding import Embedder
from retrieval.qdrant_store import QdrantStore
from retrieval.reranker import Reranker
from retrieval.service import RetrievalService


def main() -> None:
    settings = get_settings()
    parser = DocumentParser(settings)
    chunker = HeadingAwareChunker(settings)
    embedder = Embedder(settings)
    qdrant_store = QdrantStore(settings)
    retrieval = RetrievalService(settings, qdrant_store, embedder, Reranker(settings))

    pipeline = IngestionPipeline(
        settings=settings,
        parser=parser,
        chunker=chunker,
        embedder=embedder,
        qdrant_store=qdrant_store,
        retrieval_service=retrieval,
    )

    result = pipeline.incremental()
    print(result)


if __name__ == '__main__':
    main()

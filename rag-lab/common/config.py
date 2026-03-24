from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        populate_by_name=True,
    )

    app_env: str = Field(default='dev', alias='APP_ENV')
    log_level: str = Field(default='INFO', alias='LOG_LEVEL')

    qdrant_url: str = Field(default='http://localhost:6333', alias='QDRANT_URL')
    qdrant_collection: str = Field(default='beecount_docs', alias='QDRANT_COLLECTION')

    docs_zh_dir: Path = Field(default=Path('../docs'), alias='DOCS_ZH_DIR')
    docs_en_dir: Path = Field(
        default=Path('../i18n/en/docusaurus-plugin-content-docs/current'),
        alias='DOCS_EN_DIR',
    )

    embedding_model: str = Field(default='BAAI/bge-m3', alias='EMBEDDING_MODEL')
    reranker_model: str = Field(default='BAAI/bge-reranker-base', alias='RERANKER_MODEL')

    cloud_base_url: str = Field(default='', alias='CLOUD_BASE_URL')
    cloud_api_key: str = Field(default='', alias='CLOUD_API_KEY')
    cloud_model: str = Field(default='glm-4-flash', alias='CLOUD_MODEL')

    ollama_base_url: str = Field(default='http://localhost:11434', alias='OLLAMA_BASE_URL')
    ollama_model: str = Field(default='qwen2.5:1.5b-instruct', alias='OLLAMA_MODEL')

    chunk_size: int = Field(default=450, alias='CHUNK_SIZE')
    chunk_overlap: int = Field(default=80, alias='CHUNK_OVERLAP')

    top_k_dense: int = Field(default=20, alias='TOP_K_DENSE')
    top_k_bm25: int = Field(default=20, alias='TOP_K_BM25')
    hybrid_alpha: float = Field(default=0.6, alias='HYBRID_ALPHA')
    max_context_chunks: int = Field(default=6, alias='MAX_CONTEXT_CHUNKS')

    data_dir: Path = Field(default=Path('./data'), alias='DATA_DIR')

    query_cache_ttl_seconds: int = Field(default=900, alias='QUERY_CACHE_TTL_SECONDS')
    query_cache_maxsize: int = Field(default=256, alias='QUERY_CACHE_MAXSIZE')

    local_fallback_enabled: bool = Field(default=True, alias='LOCAL_FALLBACK_ENABLED')
    http_timeout_seconds: int = Field(default=45, alias='HTTP_TIMEOUT_SECONDS')

    openai_compat_api_key: str = Field(default='', alias='OPENAI_COMPAT_API_KEY')
    openai_compat_default_provider: str = Field(default='local', alias='OPENAI_COMPAT_DEFAULT_PROVIDER')
    openai_compat_fallback_provider: str = Field(default='cloud', alias='OPENAI_COMPAT_FALLBACK_PROVIDER')
    openai_compat_enable_stream: bool = Field(default=True, alias='OPENAI_COMPAT_ENABLE_STREAM')


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    (settings.data_dir / 'cache').mkdir(parents=True, exist_ok=True)
    return settings

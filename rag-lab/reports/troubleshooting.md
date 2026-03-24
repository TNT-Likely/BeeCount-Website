# Troubleshooting

## Qdrant 不可用
- 现象：`/readyz` 返回 503
- 排查：`docker compose logs qdrant`
- 处理：重启 `docker compose restart qdrant`

## 云模型调用失败
- 现象：query 返回 fallback_used=true
- 排查：检查 `.env` 中 `CLOUD_BASE_URL/CLOUD_API_KEY`
- 处理：修正后重启 `rag-api`

## 本地 Ollama 调用失败
- 现象：cloud 失败后 local 也失败
- 排查：`curl $OLLAMA_BASE_URL/api/tags`
- 处理：确认模型已拉取，如 `ollama pull qwen2.5:1.5b-instruct`

## 检索结果不准
- 优先检查：
  1. 是否执行过 `/v1/ingest/rebuild`
  2. chunk 参数是否过大
  3. `mode` 是否使用 `hybrid`

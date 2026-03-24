# BeeCount RAG Lab

BeeCount 文档 RAG 学习工程（FastAPI + Qdrant + Hybrid Retrieval + Cloud/Ollama 双推理）。

## Quick Start

1. 复制环境变量：

```bash
cp .env.example .env
```

2. 启动服务：

```bash
docker compose up --build -d qdrant rag-api
```

3. 全量入库：

```bash
curl -X POST http://127.0.0.1:8008/v1/ingest/rebuild
```

4. 查询：

```bash
curl -X POST http://127.0.0.1:8008/v1/query \
  -H 'content-type: application/json' \
  -d '{"query":"如何配置WebDAV同步？","locale":"zh","mode":"hybrid","generation_provider":"cloud"}'
```

流式查询（SSE）：

```bash
curl -N -X POST http://127.0.0.1:8008/v1/query \
  -H 'content-type: application/json' \
  -d '{"query":"How to configure S3 sync?","locale":"en","stream":true,"generation_provider":"cloud"}'
```

5. 运行评测：

```bash
curl -X POST http://127.0.0.1:8008/v1/eval/run -H 'content-type: application/json' -d '{}'
```

6. OpenAI 兼容（Cherry Studio 直连）：

```bash
curl http://127.0.0.1:8008/v1/models

curl -X POST http://127.0.0.1:8008/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{"model":"beecount-rag","messages":[{"role":"user","content":"如何配置WebDAV同步？"}]}'
```

## Endpoints

- `POST /v1/query`
- `POST /v1/ingest/rebuild`
- `POST /v1/ingest/incremental`
- `POST /v1/eval/run`
- `GET /v1/models` (OpenAI compat)
- `POST /v1/chat/completions` (OpenAI compat)
- `GET /healthz`
- `GET /readyz`
- `GET /metrics`

## Notes

- NAS（N5105）建议只跑 `qdrant + rag-api`。
- 本地模型建议在 Mac 上运行 Ollama，再让 `rag-api` 通过 `OLLAMA_BASE_URL` 调用。
- 云模型失败时会按配置自动降级到本地模型（`LOCAL_FALLBACK_ENABLED=true`）。
- OpenAI 兼容层默认本地优先、云回退（`OPENAI_COMPAT_DEFAULT_PROVIDER=local` / `OPENAI_COMPAT_FALLBACK_PROVIDER=cloud`）。
- 如需鉴权，设置 `OPENAI_COMPAT_API_KEY`，客户端需携带 `Authorization: Bearer <key>`。

## Cherry Studio 配置

1. `Provider`: OpenAI
2. `Base URL`: `http://127.0.0.1:8008/v1`
3. `API Key`: 任意字符串（若配置了 `OPENAI_COMPAT_API_KEY` 则必须填一致值）
4. `Model`: 可填任意值（兼容层宽松映射，推荐 `beecount-rag`）

## Dev Check

```bash
pytest -q
```

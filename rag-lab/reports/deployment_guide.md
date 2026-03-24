# Deployment Guide

## 1. 环境
- Docker / Docker Compose
- 可选：本机 Ollama（用于 local provider）

## 2. 配置
1. `cp ../.env.example ../.env`
2. 填写 `CLOUD_BASE_URL` 与 `CLOUD_API_KEY`

## 3. 启动
```bash
cd ../
docker compose up --build -d qdrant rag-api
```

## 4. 初始化索引
```bash
curl -X POST http://127.0.0.1:8008/v1/ingest/rebuild
```

## 5. 验证
```bash
curl http://127.0.0.1:8008/healthz
curl http://127.0.0.1:8008/readyz
```

## 6. 更新文档后增量索引
```bash
curl -X POST http://127.0.0.1:8008/v1/ingest/incremental
```

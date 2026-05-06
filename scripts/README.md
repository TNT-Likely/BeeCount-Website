# Scripts

## `build_docs_index.py` — RAG 索引构建

为 BeeCount-Platform 的 ⌘K AI 文档搜索(A1)生成索引。

### 设计文档

`BeeCount-Platform/.docs/web-cmdk-ai-doc-search.md`

### 流程

1. 计算 `docs/` + `i18n/en/.../current/` 所有 markdown 内容的 sha256
2. 跟 `data/docs-index.hash` 比对 — 一致则 skip(可加 `--force` 强制重建)
3. 不一致 → 按 H2 / H3 切 chunks(每段 ~850 字),调 SiliconFlow embedding API,
   写 `data/docs-index.{zh,en}.sqlite`
4. 更新 `data/docs-index.hash`

### 本地跑

```bash
cd BeeCount-Website
pip install -r scripts/requirements.txt
EMBEDDING_API_KEY=sk-xxx python scripts/build_docs_index.py
# --force 跳过 hash 检查强制重建
```

### CI

`.github/workflows/build-rag-index.yml` — docs 改动时自动跑,产物提交回 main。

Repo secret 需要 `SILICONFLOW_KEY`(<https://siliconflow.cn> 注册)。

### 产出消费

BeeCount-Platform Cloud CI 会:

```bash
git clone --depth 1 https://github.com/TNT-Likely/BeeCount-Website ./external/website
cp ./external/website/data/docs-index.*.sqlite ./data/
```

把 sqlite 文件打进 docker image,server 端 `/api/v1/ai/ask` 直接读。

### 索引文件 schema

```sql
CREATE TABLE chunks (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,        -- chunk 完整文本(带 H2/H3 标题)
    doc_path TEXT NOT NULL,       -- 'security/two-factor.md'
    doc_title TEXT,               -- frontmatter title 或 H1
    section TEXT,                 -- 'A > B' 形式的 header path
    url TEXT,                     -- 'https://count.beejz.com/docs/...'
    vector BLOB NOT NULL          -- 1024-dim float32 raw bytes
);

CREATE TABLE meta (
    key TEXT PRIMARY KEY,
    value TEXT                    -- embedding_model / dim / build_time / chunk_count
);
```

Server 端 `numpy.frombuffer(vector, dtype=np.float32)` 读向量。

"""Build RAG docs index — Website 端的索引构建脚本。

用法:
    EMBEDDING_API_KEY=sk-xxx python scripts/build_docs_index.py

产出:
    data/docs-index.zh.sqlite      — 中文索引(默认 docs/)
    data/docs-index.en.sqlite      — 英文索引(i18n/en/.../current/)
    data/docs-index.hash           — corpus 内容 sha256(跳重复构建用)

设计:.docs/web-cmdk-ai-doc-search.md(BeeCount-Platform)
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

import frontmatter
import numpy as np
from openai import OpenAI


# 配置 ─────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DOCS_ZH = ROOT / "docs"
DOCS_EN = ROOT / "i18n/en/docusaurus-plugin-content-docs/current"
SITE_BASE = "https://count.beejz.com"

# 目标 chunk 大小:每段 ~250 tokens(中文 1.7 字/token → ~430 字)
# - SiliconFlow BGE-large-zh-v1.5 max input 512 tokens,得留余量给 H2/H3 标题前缀
# - BGE-M3 max 8192 tokens,完全够;但小 chunk 信号更纯,LLM 看完更准
# - 实测 chunk 越小,RAG 检索精度越高(单 chunk 主题集中)
TARGET_CHUNK_CHARS = 430
MIN_CHUNK_CHARS = 80       # 短于这个的 H2 不切,避免碎片
MAX_CHUNK_CHARS = 700      # 超过强切(留余量给 BGE-large 512-token 限制)

# BGE-M3:支持长 context(8K)+ 中英双语 + 跟 BGE-large-zh 同维度(1024)
# 比 BGE-large-zh-v1.5 兼容性更好(后者只支持 512 tokens 容易撞限),
# 是 SiliconFlow 默认推荐的免费 embedding 模型
EMBEDDING_BASE_URL = os.getenv("EMBEDDING_BASE_URL", "https://api.siliconflow.cn/v1")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
EMBEDDING_BATCH = int(os.getenv("EMBEDDING_BATCH", "16"))


# 数据结构 ─────────────────────────────────────────────────────────────────


@dataclass
class Chunk:
    content: str
    doc_path: str       # 'security/two-factor.md'
    doc_title: str      # frontmatter title 或 H1 或 文件名
    section: str        # '应用锁 > 开启应用锁'
    url: str            # 'https://count.beejz.com/docs/security/two-factor'
    vector: list[float] = field(default_factory=list)


# Hash / 缓存 ──────────────────────────────────────────────────────────────


def compute_corpus_hash() -> str:
    """所有 docs 文件内容的 sha256(中英都包括)。任意一篇改一个字符 → hash 变。"""
    h = hashlib.sha256()
    for base in (DOCS_ZH, DOCS_EN):
        if not base.exists():
            continue
        for md in sorted(base.rglob("*.md")):
            h.update(str(md.relative_to(ROOT)).encode("utf-8"))
            h.update(b"\0")
            h.update(md.read_bytes())
            h.update(b"\0")
    return h.hexdigest()


# Markdown 解析 + chunking ─────────────────────────────────────────────────


def doc_url_for(rel_path: Path, lang: str) -> str:
    """从 markdown 相对路径推 site URL。
    docs/security/two-factor.md → /docs/security/two-factor
    docs/intro.md → /docs/intro
    en 版 → /en/docs/...
    """
    parts = list(rel_path.with_suffix("").parts)
    prefix = "" if lang == "zh" else "/en"
    return f"{SITE_BASE}{prefix}/docs/{'/'.join(parts)}"


def split_to_chunks(body: str) -> Iterator[tuple[str, str]]:
    """按 H2 切;太长再按 H3 / 段落切;返回 (section_path, content)。

    body: markdown 正文(已剥 frontmatter)
    """
    # H2 split
    h2_pattern = re.compile(r"^##\s+(.+)$", re.MULTILINE)
    matches = list(h2_pattern.finditer(body))

    if not matches:
        # 没 H2 → 整篇当一个 chunk(短文档场景)
        yield "", body.strip()
        return

    # 开头到第一个 H2 之间的内容(intro 部分)
    if matches[0].start() > 0:
        intro = body[: matches[0].start()].strip()
        if len(intro) >= MIN_CHUNK_CHARS:
            yield "", intro

    for i, m in enumerate(matches):
        section = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        content = body[start:end].strip()
        if not content:
            continue

        # H2 section 太长 → 进一步按 H3 切
        if len(content) > MAX_CHUNK_CHARS:
            yield from _split_section(section, content)
        else:
            # 加 H2 标题让 LLM 看到上下文
            yield section, f"## {section}\n\n{content}"


def _split_section(section: str, content: str) -> Iterator[tuple[str, str]]:
    """H2 section 太长时,按 H3 进一步切;还太长按段落 cap。"""
    h3_pattern = re.compile(r"^###\s+(.+)$", re.MULTILINE)
    matches = list(h3_pattern.finditer(content))

    if not matches:
        # 没 H3 → 按段落硬切到 TARGET_CHUNK_CHARS
        for piece in _split_by_paragraph(content, TARGET_CHUNK_CHARS):
            yield section, f"## {section}\n\n{piece}"
        return

    if matches[0].start() > 0:
        intro = content[: matches[0].start()].strip()
        if len(intro) >= MIN_CHUNK_CHARS:
            yield section, f"## {section}\n\n{intro}"

    for i, m in enumerate(matches):
        sub_section = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        sub_content = content[start:end].strip()
        if not sub_content:
            continue
        full_section = f"{section} > {sub_section}"
        if len(sub_content) > MAX_CHUNK_CHARS:
            for piece in _split_by_paragraph(sub_content, TARGET_CHUNK_CHARS):
                yield full_section, f"## {section}\n### {sub_section}\n\n{piece}"
        else:
            yield full_section, f"## {section}\n### {sub_section}\n\n{sub_content}"


def _split_by_paragraph(text: str, target: int) -> Iterator[str]:
    """按 \\n\\n 切,累到 target 字符就 yield。"""
    paragraphs = re.split(r"\n\s*\n", text)
    buf = ""
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if buf and len(buf) + len(p) + 2 > target:
            yield buf
            buf = p
        else:
            buf = f"{buf}\n\n{p}" if buf else p
    if buf:
        yield buf


def parse_doc(md_path: Path, base: Path, lang: str) -> Iterator[Chunk]:
    """解析单篇 markdown → 多个 Chunk。"""
    fm = frontmatter.load(md_path)
    body = fm.content
    rel = md_path.relative_to(base)

    title = fm.metadata.get("title")
    if not title:
        # 没 frontmatter title → 用第一个 H1
        h1 = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        title = h1.group(1).strip() if h1 else md_path.stem

    url = doc_url_for(rel, lang)

    for section, content in split_to_chunks(body):
        if len(content.strip()) < MIN_CHUNK_CHARS:
            continue
        yield Chunk(
            content=content,
            doc_path=str(rel),
            doc_title=str(title),
            section=section,
            url=url,
        )


def collect_chunks(base: Path, lang: str) -> list[Chunk]:
    if not base.exists():
        return []
    chunks: list[Chunk] = []
    for md in sorted(base.rglob("*.md")):
        chunks.extend(parse_doc(md, base, lang))
    return chunks


# Embedding ─────────────────────────────────────────────────────────────────


def embed_chunks(chunks: list[Chunk], client: OpenAI) -> None:
    """批量 embedding 并填回 chunks[i].vector。

    SiliconFlow 免费 tier 默认 RPM ~60(已实名 ~600),所以 batch 之间 sleep。
    遇 403 / 429(rate limit)指数退避;遇 timeout 短退避;其它直接 raise。
    """
    print(f"  embedding {len(chunks)} chunks (model={EMBEDDING_MODEL}, batch={EMBEDDING_BATCH})...")
    throttle_s = float(os.getenv("EMBEDDING_THROTTLE_S", "1.2"))  # 默认 ~50 RPM,够安全
    for i in range(0, len(chunks), EMBEDDING_BATCH):
        batch = chunks[i : i + EMBEDDING_BATCH]
        for attempt in range(6):
            try:
                resp = client.embeddings.create(
                    model=EMBEDDING_MODEL,
                    input=[c.content for c in batch],
                )
                for c, item in zip(batch, resp.data):
                    c.vector = item.embedding
                break
            except Exception as e:
                if attempt == 5:
                    raise
                msg = str(e)
                # 限速 / 容量错误 → 长退避;其它 → 短重试
                is_rate_limit = (
                    "429" in msg or "403" in msg
                    or "rpm" in msg.lower() or "rate limit" in msg.lower()
                )
                wait = (5 ** (attempt + 1)) if is_rate_limit else (2 ** attempt)
                print(f"    batch {i // EMBEDDING_BATCH} attempt {attempt + 1} failed: {msg[:120]}; retry in {wait}s")
                time.sleep(wait)
        if (i // EMBEDDING_BATCH) % 5 == 0:
            print(f"    progress: {min(i + EMBEDDING_BATCH, len(chunks))}/{len(chunks)}")
        # batch 之间统一 throttle
        if i + EMBEDDING_BATCH < len(chunks):
            time.sleep(throttle_s)


# SQLite output ─────────────────────────────────────────────────────────────


def write_sqlite(chunks: list[Chunk], out_path: Path, dim: int) -> None:
    """写 sqlite — schema 见 web-cmdk-ai-doc-search.md。

    向量存为 raw float32 bytes(每个 chunk ~4KB),server 端 numpy.frombuffer 读。
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        out_path.unlink()

    conn = sqlite3.connect(out_path)
    try:
        conn.executescript(
            """
            CREATE TABLE chunks (
                id INTEGER PRIMARY KEY,
                content TEXT NOT NULL,
                doc_path TEXT NOT NULL,
                doc_title TEXT,
                section TEXT,
                url TEXT,
                vector BLOB NOT NULL
            );
            CREATE TABLE meta (
                key TEXT PRIMARY KEY,
                value TEXT
            );
            """
        )
        for chunk in chunks:
            vec = np.asarray(chunk.vector, dtype=np.float32).tobytes()
            conn.execute(
                "INSERT INTO chunks (content, doc_path, doc_title, section, url, vector) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (chunk.content, chunk.doc_path, chunk.doc_title, chunk.section, chunk.url, vec),
            )
        conn.execute(
            "INSERT INTO meta (key, value) VALUES (?, ?), (?, ?), (?, ?), (?, ?)",
            (
                "embedding_model", EMBEDDING_MODEL,
                "dim", str(dim),
                "build_time", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "chunk_count", str(len(chunks)),
            ),
        )
        conn.commit()
    finally:
        conn.close()
    print(f"  wrote {out_path} ({len(chunks)} chunks, {out_path.stat().st_size / 1024:.1f} KB)")


# Main ──────────────────────────────────────────────────────────────────────


def build_for_lang(lang: str, client: OpenAI) -> None:
    base = DOCS_ZH if lang == "zh" else DOCS_EN
    print(f"[{lang}] collecting chunks from {base}...")
    chunks = collect_chunks(base, lang)
    print(f"[{lang}] {len(chunks)} chunks total")
    if not chunks:
        print(f"[{lang}] skip (no chunks)")
        return
    embed_chunks(chunks, client)
    dim = len(chunks[0].vector)
    write_sqlite(chunks, DATA_DIR / f"docs-index.{lang}.sqlite", dim)


def main() -> int:
    DATA_DIR.mkdir(exist_ok=True)

    # 1. 内容 hash 检查
    current_hash = compute_corpus_hash()
    hash_file = DATA_DIR / "docs-index.hash"
    last_hash = hash_file.read_text().strip() if hash_file.exists() else ""

    force = "--force" in sys.argv
    if current_hash == last_hash and not force:
        print(f"docs unchanged ({current_hash[:8]}); skip rebuild (--force to override)")
        return 0

    print(f"corpus hash {last_hash[:8] or '<none>'} → {current_hash[:8]}; rebuilding...")

    # 2. embedding client
    api_key = os.getenv("EMBEDDING_API_KEY")
    if not api_key:
        print("ERROR: EMBEDDING_API_KEY not set", file=sys.stderr)
        return 1
    client = OpenAI(base_url=EMBEDDING_BASE_URL, api_key=api_key)

    # 3. 双语 build
    build_for_lang("zh", client)
    build_for_lang("en", client)

    # 4. 写 hash
    hash_file.write_text(current_hash + "\n")
    print(f"\ndone; new hash: {current_hash}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

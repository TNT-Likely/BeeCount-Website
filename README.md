# BeeCount Website &nbsp; [English](README_EN.md)

<div align="center">

蜜蜂记账官网与文档 · Docusaurus 3 · 中英双语 · 内置 RAG 索引

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Docusaurus](https://img.shields.io/badge/Docusaurus-3-2E8555?logo=docusaurus&logoColor=white)](https://docusaurus.io/)
[![Node](https://img.shields.io/badge/Node-18%2B-339933?logo=node.js&logoColor=white)](https://nodejs.org/)

[🌐 官网 count.beejz.com](https://count.beejz.com) · [📦 主仓库](https://github.com/TNT-Likely/BeeCount)

</div>

---

蜜蜂记账（BeeCount）的官方文档站点，包含使用指南、FAQ、更新日志，并为 BeeCount-Platform 的 ⌘K AI 文档搜索提供 RAG 索引。

- 📖 文档与多语言（中文 / English）
- 🔍 站内本地搜索（@easyops-cn/docusaurus-search-local）
- 🤖 RAG 索引产物（SiliconFlow embedding，供 Cloud 端 `/api/v1/ai/ask` 消费）
- 🚀 静态托管（Cloudflare Pages）

## 🚀 快速开始

```bash
pnpm install
pnpm start          # 中文（默认）→ http://localhost:3000
pnpm start:en       # 英文
pnpm build          # 生产构建
pnpm serve          # 预览构建产物
```

环境要求：Node 18+ · pnpm 8+

## 🤖 RAG 索引

本仓库为 BeeCount-Platform 的 AI 文档问答（⌘K → A1）维护向量索引。

**流程**：docs 改动 → CI 触发 → sha256 比对 → 按 H2/H3 切 chunk（~850 字）→ 调 SiliconFlow embedding → 写 `data/docs-index.{zh,en}.sqlite` → 提交回 main → Cloud CI clone 后打进 docker image。

```bash
# 本地构建索引
pip install -r scripts/requirements.txt
EMBEDDING_API_KEY=sk-xxx python scripts/build_docs_index.py
# --force 跳过 hash 检查
```

**CI**：`.github/workflows/build-rag-index.yml`，docs 改动时自动跑（需要 repo secret `SILICONFLOW_KEY`）。

详细说明：[`scripts/README.md`](scripts/README.md) · 设计文档：BeeCount-Platform `.docs/web-cmdk-ai-doc-search.md`

## 📁 目录结构

```
docs/                                              # 中文文档（一级目录 = sidebar 分类）
i18n/en/docusaurus-plugin-content-docs/current/    # 英文文档（结构对齐）
data/                                              # RAG 产物
├── docs-index.zh.sqlite                          #   中文向量索引
├── docs-index.en.sqlite                          #   英文向量索引
└── docs-index.hash                               #   corpus sha256（增量构建用）
scripts/build_docs_index.py                        # RAG 构建脚本
src/                                               # React 自定义页面 / 组件
static/img/preview/{zh,en}/                        # 中英截图
```

## 🛠 常用命令

| 命令 | 说明 |
|------|------|
| `pnpm start` / `start:en` | 启动开发服务器（zh / en） |
| `pnpm build` | 生产构建 → `build/` |
| `pnpm serve` | 预览构建产物 |
| `pnpm clear` | 清缓存 |
| `pnpm write-translations` | 生成 i18n 翻译模板 |

<details>
<summary><b>📝 开发指南（点击展开）</b></summary>

### 添加新文档

1. 在 `docs/<分类>/` 下创建 `.md`，加 frontmatter：
   ```markdown
   ---
   sidebar_position: 1
   ---

   # 标题
   ```
2. `sidebars.ts` 加路径
3. 在 `i18n/en/docusaurus-plugin-content-docs/current/<分类>/` 同名位置加英文版

### 文档规范

- 标准 Markdown / MDX（可嵌入 React 组件）
- 图片放 `static/img/`，引用用绝对路径 `/img/...`
- 截图：`static/img/preview/{zh,en}/01-home.png` 形式编号，竖屏 1080×1920
- 告示框：`:::tip` / `:::warning` / `:::danger` / `:::info`

### 国际化

```bash
pnpm write-translations           # 生成翻译模板
# 编辑 i18n/en/docusaurus-plugin-content-docs/current.json（UI 文案）
# 编辑 i18n/en/docusaurus-plugin-content-docs/current/**/*.md（文档正文）
```

### 注意

- 改 `docs/**` 或 `i18n/en/.../current/**` 会触发 RAG 重建 CI
- 大改结构请先确认 `sidebars.ts` 与英文目录同步，避免站内死链

</details>

<details>
<summary><b>🤝 贡献规范（点击展开）</b></summary>

### 流程

1. Fork → 切分支：`git checkout -b doc/<topic>`
2. 提交（commit 规范见下）
3. Push 到 fork → 创建 PR

### Commit 规范

中文 commit message，遵循 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/v1.0.0/)：

| 类型 | 用途 |
|------|------|
| `docs:` | 新增 / 修改文档内容 |
| `feat:` | 新功能（页面、组件） |
| `fix:` | 修复（拼写、链接、构建错误） |
| `style:` | 仅样式调整 |
| `refactor:` | 不改变行为的结构调整 |
| `chore:` | 依赖升级、CI、配置 |

不要在 commit message 包含 Claude Code 等 AI 工具相关信息。

### PR 检查清单

- [ ] 中英文档同步（如果改了 `docs/`，对应 `i18n/en/...` 也更新）
- [ ] 本地 `pnpm build` 通过（无 broken link / 编译错误）
- [ ] 截图放对目录（`zh/` vs `en/`）
- [ ] 不要提交 `data/docs-index.*.sqlite`（CI 自动重建）

</details>

## 📄 License

[MIT](LICENSE) © TNT-Likely · 主项目仓库 [TNT-Likely/BeeCount](https://github.com/TNT-Likely/BeeCount)

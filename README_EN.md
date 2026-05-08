# BeeCount Website &nbsp; [中文](README.md)

<div align="center">

Official website & docs for BeeCount · Docusaurus 3 · zh / en bilingual · ships RAG index

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Docusaurus](https://img.shields.io/badge/Docusaurus-3-2E8555?logo=docusaurus&logoColor=white)](https://docusaurus.io/)
[![Node](https://img.shields.io/badge/Node-18%2B-339933?logo=node.js&logoColor=white)](https://nodejs.org/)

[🌐 Site count.beejz.com](https://count.beejz.com) · [📦 Main Repo](https://github.com/TNT-Likely/BeeCount)

</div>

---

The official documentation site for BeeCount. Hosts the user docs (Chinese + English), and produces a vector index consumed by BeeCount-Platform's ⌘K AI doc search.

- 📖 Bilingual docs (zh / en)
- 🔍 Local site search (`@easyops-cn/docusaurus-search-local`)
- 🤖 RAG index artifacts (SiliconFlow embeddings, consumed by Cloud `/api/v1/ai/ask`)
- 🚀 Static hosting on Cloudflare Pages

## 🚀 Quick Start

```bash
pnpm install
pnpm start          # zh (default) → http://localhost:3000
pnpm start:en       # en
pnpm build          # production build
pnpm serve          # preview build
```

Requires Node 18+ and pnpm 8+.

## 🤖 RAG Index

This repo maintains the vector index for BeeCount-Platform's AI doc Q&A (⌘K → A1).

**Pipeline**: docs change → CI fires → sha256 diff → chunk by H2/H3 (~850 chars) → SiliconFlow embedding → write `data/docs-index.{zh,en}.sqlite` → commit back to main → Cloud CI clones into the docker image.

```bash
# Local build
pip install -r scripts/requirements.txt
EMBEDDING_API_KEY=sk-xxx python scripts/build_docs_index.py
# --force to skip hash check
```

**CI**: `.github/workflows/build-rag-index.yml` (requires `SILICONFLOW_KEY` repo secret).

See [`scripts/README.md`](scripts/README.md) for full details. Design doc: BeeCount-Platform `.docs/web-cmdk-ai-doc-search.md`.

## 📁 Layout

```
docs/                                              # Chinese docs (top-level dirs = sidebar categories)
i18n/en/docusaurus-plugin-content-docs/current/    # English docs (mirrored layout)
data/                                              # RAG artifacts
├── docs-index.zh.sqlite                          #   Chinese vector index
├── docs-index.en.sqlite                          #   English vector index
└── docs-index.hash                               #   corpus sha256 (incremental builds)
scripts/build_docs_index.py                        # RAG builder
src/                                               # React custom pages / components
static/img/preview/{zh,en}/                        # zh / en screenshots
```

## 🛠 Commands

| Command | Purpose |
|---------|---------|
| `pnpm start` / `start:en` | Dev server (zh / en) |
| `pnpm build` | Production build → `build/` |
| `pnpm serve` | Preview build |
| `pnpm clear` | Clear cache |
| `pnpm write-translations` | Generate i18n templates |

<details>
<summary><b>📝 Development guide (click to expand)</b></summary>

### Adding a doc

1. Create `docs/<category>/<slug>.md` with frontmatter:
   ```markdown
   ---
   sidebar_position: 1
   ---

   # Title
   ```
2. Register the path in `sidebars.ts`
3. Add the English mirror at `i18n/en/docusaurus-plugin-content-docs/current/<category>/<slug>.md`

### Conventions

- Standard Markdown / MDX (React components allowed)
- Images live in `static/img/`, referenced as `/img/...`
- Screenshots: `static/img/preview/{zh,en}/01-home.png`, portrait 1080×1920, PNG
- Admonitions: `:::tip` / `:::warning` / `:::danger` / `:::info`

### i18n

```bash
pnpm write-translations
# edit i18n/en/docusaurus-plugin-content-docs/current.json (UI strings)
# edit i18n/en/docusaurus-plugin-content-docs/current/**/*.md (doc body)
```

### Notes

- Changes under `docs/**` or `i18n/en/.../current/**` re-trigger the RAG build CI
- Keep `sidebars.ts` and the English mirror in sync to avoid broken links

</details>

<details>
<summary><b>🤝 Contributing (click to expand)</b></summary>

### Workflow

1. Fork → branch: `git checkout -b doc/<topic>`
2. Commit (message style below)
3. Push to your fork → open a PR

### Commit messages

Use Chinese, following [Conventional Commits](https://www.conventionalcommits.org/):

| Type | Purpose |
|------|---------|
| `docs:` | Doc content (add / modify) |
| `feat:` | New feature (page, component) |
| `fix:` | Fixes (typos, links, build errors) |
| `style:` | Style-only changes |
| `refactor:` | Behavior-preserving restructuring |
| `chore:` | Deps, CI, config |

Don't reference Claude Code / AI tools in commit messages.

### PR checklist

- [ ] zh and en docs are in sync (if you touched `docs/`, also update `i18n/en/...`)
- [ ] `pnpm build` passes locally (no broken links / compile errors)
- [ ] Screenshots placed under the correct locale dir (`zh/` vs `en/`)
- [ ] Do not commit `data/docs-index.*.sqlite` (CI rebuilds it)

</details>

## 📄 License

[MIT](LICENSE) © TNT-Likely · Main repo: [TNT-Likely/BeeCount](https://github.com/TNT-Likely/BeeCount)

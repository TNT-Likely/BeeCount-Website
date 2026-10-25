---
sidebar_position: 1
slug: /mcp
description: Use 55 MCP tools to query and manage BeeCount ledgers, import statements, reconcile accounts, preview receipts, and schedule Cloud recurring entries.
keywords: [BeeCount MCP, Claude Desktop bookkeeping, Cursor bookkeeping, LLM accounting, AI agent bookkeeping, MCP server]
---

# MCP

> Built into BeeCount Cloud since 1.2.0 · Integrates with Claude Desktop / Cursor / Cline

[Model Context Protocol (MCP)](https://modelcontextprotocol.io) is Anthropic's LLM tool-integration standard. BeeCount Cloud ships a built-in MCP server so you can manage your ledgers from inside Claude Desktop / Cursor / Cline through natural-language chat.

## What it feels like

In your favourite LLM client, just say:

> "How much did I spend on takeout last month? What were the top three categories?"

> "Change that 3pm Starbucks transaction from yesterday — it should be 42 instead of 38, and add a #coffee tag."

> "Quick note this for me: I just bought a bottle of water at the convenience store for 3.50."

The LLM selects tools to query or record transactions. It can also preview statement imports, compare account balances, record review questions, and create Cloud recurring rules after approval. See the [workflow guide](./workflows.md).

## Prerequisites

- ✅ **BeeCount Cloud** deployed (see [Self-hosted Cloud](../cloud-sync/beecount-cloud.md))
- ✅ At least one MCP-capable LLM client: Claude Desktop / Cursor / Cline / etc.
- ✅ Network reach: the LLM client must be able to reach your BeeCount Cloud URL (LAN, VPN, or public)

## Three-step setup

### 1. Create a Personal Access Token (PAT)

1. Log in to BeeCount Cloud's web console
2. Top-right avatar → **Settings → Developer** (`/app/settings/developer`)
3. Click **New token**:
   - **Name**: a label, e.g. `Claude Desktop`
   - **Scope**:
     - `mcp:read` — LLM can **only read**. **Start with this.**
     - `mcp:read + mcp:write` — LLM can **create, edit, delete** transactions. Grant carefully.
   - **Expiration**: 30 / 90 / 180 / 365 days or never (default 90)
4. **Copy the token immediately!** The plaintext `bcmcp_…` is shown only once — after you close the dialog only the prefix is recoverable.

:::warning The token is equivalent to your password
Only configure trusted clients. Never share it, never commit to git. If compromised, **revoke** it from the web settings page immediately.
:::

### 2. Configure the LLM client

:::tip About transports
The BeeCount Cloud server exposes a single **Streamable HTTP** endpoint (`/api/v1/mcp`).

**Clients that speak Streamable HTTP natively** (e.g. Claude Code) **connect directly** — no bridge:
```bash
claude mcp add --transport http --scope user beecount \
  https://your-beecount-cloud.com/api/v1/mcp \
  --header "Authorization:Bearer bcmcp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

The Claude Desktop / Cursor / Cline examples below use `npx mcp-remote` as a stdio bridge for clients that only speak stdio (the most compatible path); use the URL `/api/v1/mcp` (no longer `/sse`) — mcp-remote negotiates Streamable HTTP automatically.

> The legacy SSE endpoint (`/api/v1/mcp/sse`) has been replaced by Streamable HTTP and is no longer served.
:::

#### Claude Desktop

Config file:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "beecount": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://your-beecount-cloud.com/api/v1/mcp",
        "--header",
        "Authorization:Bearer bcmcp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      ]
    }
  }
}
```

Fully quit Claude Desktop (`Cmd+Q`) and relaunch. The 🔌 icon in the bottom-left should show "BeeCount" connected.

#### Cursor

Config file: `~/.cursor/mcp.json` (or Settings → Features → MCP UI editor)

```json
{
  "mcpServers": {
    "beecount": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://your-beecount-cloud.com/api/v1/mcp",
        "--header",
        "Authorization:Bearer bcmcp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      ]
    }
  }
}
```

Restart Cursor.

#### Cline (VS Code)

VS Code → Cline icon → top-right `…` → **Edit MCP Settings**

```json
{
  "mcpServers": {
    "beecount": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://your-beecount-cloud.com/api/v1/mcp",
        "--header",
        "Authorization:Bearer bcmcp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      ],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### 3. Verify

In your LLM client, start a new chat and ask:

> "How many ledgers do I have?"

The LLM calls `list_ledgers` and returns your ledgers. Before recording transactions, use `get_bookkeeping_context` to check the ledger, account/category IDs, role, and scopes. Choose explicitly when multiple ledgers exist and pass `ledger_id` in subsequent calls.

## The 55 tools

There are **26 read-scope tools and 29 write-scope tools**, plus 2 resource templates and 2 prompts. See [Import, reconciliation, and recurring entries](./workflows.md) for complete workflows.

:::info Version requirement for the complete toolset
The complete toolset requires **Cloud 1.9.0 or later** and Alembic migration `0021_mcp_workflows`. See the [Cloud Changelog](../cloud-changelog.md). Older versions provide only part of the toolset; reconnect clients after upgrading to discover the new tools.
:::

### Query and read (26 tools, `mcp:read`)

| Tool | Purpose |
|---|---|
| `list_ledgers` | List all ledgers |
| `get_active_ledger` | Legacy default-ledger lookup; use context to choose among multiple ledgers |
| `list_transactions` | Query transactions with date / category / account / keyword / amount filters |
| `get_transaction` | Single transaction detail |
| `list_categories` | List categories (optionally filtered by expense/income/transfer) |
| `list_accounts` | List accounts (optionally filtered by type) |
| `list_tags` | List tags |
| `list_budgets` | List budgets with current-month spent / remaining |
| `get_ledger_stats` | Counts: transactions / categories / accounts / tags / budgets |
| `get_analytics_summary` | Month / year / all-time income, expense, top spending categories |
| `search` | Full-text fuzzy search over notes, category names, account names |
| `get_bookkeeping_context` | Select a ledger; inspect dictionary IDs, currency, role, and PAT scopes |
| `list_ledger_members` | List ledger members and roles |
| `get_operation` | Inspect durable operation status and step results |
| `list_operations` | Find operations after lost responses |
| `list_changes` | Read incremental transaction changes and deletion tombstones |
| `get_account_balances` | Get account balances by currency with coverage |
| `get_net_worth_history` | Get per-currency net-worth history and rate coverage |
| `analyze_transactions` | Combine filters, groups, period comparisons, and drilldown |
| `list_attachments` | List ledger attachments |
| `read_attachment` | Read an image, small text, or original-file resource |
| `export_transactions` | Save a complete CSV snapshot of up to 50,000 transactions |
| `list_workflow_records` | Find import, review, rule, and reconciliation records |
| `get_workflow_record` | Read a saved workflow record and revision |
| `list_transaction_sources` | List source identities linked to transactions |
| `reconcile_account` | Compare calculated and actual balances at a cutoff |

### Writes and workflows (29 tools, `mcp:write`)

| Tool | Purpose | Notes |
|---|---|---|
| `upload_attachment` | Upload a receipt/image | Since Cloud 1.7.0; returns a file ID to link to a transaction |
| `create_transaction` | Create a transaction | Pass `attachments` to link uploaded files |
| `create_transactions` | Create many transactions | Up to 200, committed in chunks of up to 50; per-item attachments and idempotency keys |
| `update_transaction` | Edit a transaction | Only changes fields you pass; can update attachment links |
| `delete_transaction` | Delete a transaction | **Two-step confirmation** — first call returns a "needs confirmation" placeholder; only deletes on explicit second call |
| `create_category` | Create a category | |
| `update_budget` | Change a budget's amount | |
| `parse_and_create_from_text` | Natural-language to transaction | Uses BeeCount's own AI provider — you must configure one in web settings first |
| `manage_account` | Create, edit, or delete accounts | |
| `manage_category` | Manage categories and hierarchy | |
| `manage_tag` | Create, edit, or delete tags | |
| `manage_budget` | Create, edit, or delete budgets | |
| `manage_ledger` | Create, edit, or delete ledgers | |
| `retry_operation` | Resume eligible operation steps | |
| `parse_receipt` | Draft receipt transactions with the configured vision provider | |
| `preview_text_transactions` | Draft transactions from text | |
| `preview_import_file` | Map an original CSV / TSV / XLSX and save an import plan | |
| `preview_import` | Preview structured transactions and save an import plan | |
| `execute_import_plan` | Execute an approved import-plan revision | |
| `undo_import_plan` | Undo transactions created by a plan if unchanged since import | |
| `link_transaction_source` | Link a source identity to a transaction | |
| `unlink_transaction_source` | Remove a source link while keeping the transaction | |
| `save_reconciliation_checkpoint` | Save account, source, and time-coverage checkpoints | |
| `save_review_item` | Save review questions and user answers | |
| `save_classification_rule` | Save inferred or confirmed classification rules and exceptions | |
| `apply_classification_rule` | Save classification targets and a before/after preview | |
| `execute_classification_preview` | Execute an approved classification preview with per-item revision checks | |
| `manage_recurring_rule` | Preview, save, pause, or resume Cloud recurring rules | |
| `run_due_recurring_rules` | Run due recurring rules | |

## Record with Attachments via MCP

Since **Cloud 1.7.0**, call `upload_attachment` to upload a receipt, then pass the returned `file_id` list as `attachments` to `create_transaction` or `update_transaction`. This requires `mcp:write`; the files and transaction must belong to the same ledger.

- A new transaction can include the uploaded receipt. For an existing transaction, omitting `attachments` preserves its files, `[]` clears the links, and a list replaces all links. To append files, query and retain the existing file IDs first.
- **Direct HTTP connections** accept `content_base64`. To let AI use a file path on your computer, run the repository's **local stdio adapter**, `scripts/mcp_local_files.py`. The same upload tool accepts `file_path`; the program reads and uploads original bytes without making the model output Base64.
- Configure the adapter with your Cloud URL, PAT and an allowed `--allow-dir`. Paths refer to the client computer; Cloud does not read arbitrary server paths. See the [local file upload setup](https://github.com/TNT-Likely/BeeCount-Cloud/blob/main/docs/MCP.en.md).
- Uploading alone does not recognize the receipt or create a transaction. Call `parse_receipt` separately to draft entries with a configured vision provider, then create after confirmation. Bulk `create_transactions` also supports per-item attachments.

Linked images are visible in Web and the App. Upgrade Cloud before **App 3.8.6** to sync changes to existing attachment order and details.

### Local original-file adapter

To upload files from your computer, install the Cloud repository's Python requirements on the client and run `scripts/mcp_local_files.py`. Replace the Python, script, and receipt-directory paths below with local paths. Provide the PAT through the environment and keep it out of source control.

```sh
claude mcp add --transport stdio --scope user \
  --env BEECOUNT_MCP_PAT=bcmcp_xxx beecount -- \
  /absolute/path/to/python /absolute/path/to/BeeCount-Cloud/scripts/mcp_local_files.py \
  --endpoint https://your-beecount-cloud.com/api/v1/mcp \
  --allow-dir /absolute/path/to/receipts
```

The adapter reads and uploads original bytes from `file_path`, rejecting files outside allowed directories, symlink escapes, empty files, and special files. It retains all Cloud tools and forwards attachment/export resources and prompts. Images, CSV, TSV, and XLSX use the same upload entry point.

## Security model

| Aspect | Mitigation |
|---|---|
| Token storage | Server stores only `sha256` hash, constant-time comparison; plaintext is returned only on creation |
| Revocation | Deleting a token invalidates it immediately |
| Expiration | Optional at creation; expired tokens return 401 |
| Scope separation | `mcp:read` / `mcp:write` are independent checkboxes |
| Confirmation and concurrency | Deletion, import execution, and classification execution require explicit approval; `expected_revision` protects transaction edits from overwriting later changes |
| Roles and retries | Each call checks ledger access; idempotency keys and durable operations support safe continuation |
| Protocol isolation | PATs can only call `/api/v1/mcp`; regular APIs reject PATs. Conversely, regular access tokens cannot call MCP endpoints |
| Audit | Every use bumps `last_used_at` + `last_used_ip`, visible in the web settings page |

## FAQ

### Q: How is this different from BeeCount's built-in AI (text/photo bookkeeping)?

| | Built-in AI | MCP |
|---|---|---|
| Where | Inside the app | LLM client (Claude Desktop / Cursor / …) |
| LLM | You configure (GLM / OpenAI / self-hosted) | The LLM client picks |
| Scope | Parse one transaction at a time | Multi-turn dialogue, cross-ledger analysis, batch ops |
| Best for | One-shot logging | Conversational review and analysis |

They're complementary — use both.

### Q: Does BeeCount Cloud need to be on the public internet?

No. The LLM client just needs network reach — LAN IP (e.g. `http://192.168.1.100:8869`), Tailscale, ZeroTier all work fine.

### Q: I accidentally committed my token to git

Revoke it from the web settings page immediately and create a new one. Git history is irrelevant once it's revoked.

### Q: I want LLMs to never be able to delete things

Create a token with **only `mcp:read`** checked. Any write tool call will be denied with 403.

### Q: Can multiple LLM clients share one token?

Technically yes, but **don't**. Create one token per client (`Claude Desktop` / `Cursor work` / `Cline laptop`) so you can:
- See when each client last used it (`last_used_at`)
- Revoke one without affecting the others

## See also

- [Import, reconciliation, and recurring entries](./workflows.md)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [BeeCount Cloud GitHub](https://github.com/TNT-Likely/BeeCount-Cloud)
- [Server-side detailed docs](https://github.com/TNT-Likely/BeeCount-Cloud/blob/main/docs/MCP.en.md)

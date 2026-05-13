---
sidebar_position: 1
slug: /mcp
description: Let Claude Desktop, Cursor, Cline, and other LLM clients read and write your BeeCount ledgers via the Model Context Protocol (MCP).
keywords: [BeeCount MCP, Claude Desktop bookkeeping, Cursor bookkeeping, LLM accounting, AI agent bookkeeping, MCP server]
---

# MCP Server (Let LLMs operate your ledger directly)

> New in 3.2 · Built into BeeCount Cloud · Integrates with Claude Desktop / Cursor / Cline

[Model Context Protocol (MCP)](https://modelcontextprotocol.io) is Anthropic's LLM tool-integration standard. BeeCount Cloud ships a built-in MCP server so you can manage your ledgers from inside Claude Desktop / Cursor / Cline through natural-language chat.

## What it feels like

In your favourite LLM client, just say:

> "How much did I spend on takeout last month? What were the top three categories?"

> "Change that 3pm Starbucks transaction from yesterday — it should be 42 instead of 38, and add a #coffee tag."

> "Quick note this for me: I just bought a bottle of water at the convenience store for 3.50."

The LLM picks the right tool and queries/edits your data — no need to open BeeCount.

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
        "https://your-beecount-cloud.com/api/v1/mcp/sse",
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
        "https://your-beecount-cloud.com/api/v1/mcp/sse",
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
        "https://your-beecount-cloud.com/api/v1/mcp/sse",
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

The LLM will call `list_ledgers` and answer with your ledger list.

## The 17 tools

### Read (`mcp:read`)

| Tool | Purpose |
|---|---|
| `list_ledgers` | List all ledgers |
| `get_active_ledger` | Get the default ledger |
| `list_transactions` | Query transactions with date / category / account / keyword / amount filters |
| `get_transaction` | Single transaction detail |
| `list_categories` | List categories (optionally filtered by expense/income/transfer) |
| `list_accounts` | List accounts (optionally filtered by type) |
| `list_tags` | List tags |
| `list_budgets` | List budgets with current-month spent / remaining |
| `get_ledger_stats` | Counts: transactions / categories / accounts / tags / budgets |
| `get_analytics_summary` | Month / year / all-time income, expense, top spending categories |
| `search` | Full-text fuzzy search over notes, category names, account names |

### Write (`mcp:write`, opt-in)

| Tool | Purpose | Notes |
|---|---|---|
| `create_transaction` | Create a transaction | |
| `update_transaction` | Edit a transaction | Only changes fields you pass |
| `delete_transaction` | Delete a transaction | **Two-step confirmation** — first call returns a "needs confirmation" placeholder; only deletes on explicit second call |
| `create_category` | Create a category | |
| `update_budget` | Change a budget's amount | |
| `parse_and_create_from_text` | Natural-language to transaction | Uses BeeCount's own AI provider — you must configure one in web settings first |

## Security model

| Aspect | Mitigation |
|---|---|
| Token storage | Server stores only `sha256` hash, constant-time comparison; plaintext is returned only on creation |
| Revocation | Soft delete; revoked tokens fail immediately |
| Expiration | Optional at creation; expired tokens return 401 |
| Scope separation | `mcp:read` / `mcp:write` are independent checkboxes |
| Delete safety | `delete_transaction` requires explicit confirmation |
| Protocol isolation | PATs can only call `/api/v1/mcp/*`; regular APIs reject PATs. Conversely, regular access tokens cannot call MCP endpoints |
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

- [Model Context Protocol](https://modelcontextprotocol.io)
- [BeeCount Cloud GitHub](https://github.com/TNT-Likely/BeeCount-Cloud)
- [Server-side detailed docs](https://github.com/TNT-Likely/BeeCount-Cloud/blob/main/docs/MCP.md)

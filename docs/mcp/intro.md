---
sidebar_position: 1
slug: /mcp
description: 通过 MCP(Model Context Protocol)让 Claude Desktop、Cursor、Cline 等 LLM 客户端直接读写你的 BeeCount 账本。
keywords: [蜜蜂记账 MCP, Claude Desktop 记账, Cursor 记账, LLM 记账, AI agent 记账, MCP server]
---

# MCP

> BeeCount Cloud 1.2.0 起内置 · 跟 Claude Desktop / Cursor / Cline 集成

[Model Context Protocol (MCP)](https://modelcontextprotocol.io) 是 Anthropic 推出的 LLM 工具集成协议。BeeCount Cloud 内置 MCP server,让你直接在 Claude Desktop / Cursor / Cline 里跟 LLM 自然语言对话来管理账本。

## 是什么效果

跟 LLM 聊天时可以这样说:

> "上个月我在外卖上花了多少?支出最高的分类排名前三是什么?"

> "把昨天下午 3 点星巴克那笔 38 块改成 42 块,加个 #咖啡 tag。"

> "我说一句话你帮我记一笔:刚才在便利店买了瓶水 3 块 5。"

LLM 会自动选合适的 tool 帮你查询/记录,你不用打开 BeeCount。

## 前置条件

- ✅ 已部署 **BeeCount Cloud**(参考[自建云部署](../cloud-sync/beecount-cloud.md))
- ✅ 至少一个 LLM 客户端:Claude Desktop / Cursor / Cline / 其他支持 MCP 的应用
- ✅ 网络:LLM 客户端能访问到你的 BeeCount Cloud 地址(局域网 / 公网均可)

## 启用三步走

### 1. 创建访问令牌(PAT)

1. 浏览器登录 BeeCount Cloud Web 管理端
2. 右上角头像 → **设置 → 开发者**(`/app/settings/developer`)
3. 点 **新建 Token**:
   - **名称**:给这个 token 起个名,例如 `Claude Desktop`(便于以后区分)
   - **授权范围**
     - `mcp:read` — LLM **只能查**数据。**推荐先用这个**
     - `mcp:read + mcp:write` — LLM 可以**新建 / 修改 / 删除**交易等。请谨慎授权
   - **有效期**:30 / 90 / 180 / 365 天 或 永不过期(默认 90 天)
4. **立即复制 token**!明文 `bcmcp_…` 只显示一次,关闭弹窗后无法再次查看(列表只剩前缀)

:::warning Token 等同于账户密码
请只配置到信任的客户端,不要分享、不要提交到 git。怀疑泄露立即去 Web 设置页**撤销**。
:::

### 2. 在 LLM 客户端配置

:::tip 关于 transport
BeeCount Cloud server 暴露的是 **SSE** 端点(`/api/v1/mcp/sse`)。下面 Claude Desktop / Cursor / Cline 的示例都用 `npx mcp-remote` —— 这是个 **stdio↔SSE 桥**,给只支持 stdio 的客户端用(兼容性最广)。

**如果你的客户端原生支持 SSE**(如 Claude Code、新版 Cursor),可以**跳过桥直连 SSE**,更轻量:
```bash
claude mcp add --transport sse --scope user beecount \
  https://your-beecount-cloud.com/api/v1/mcp/sse \
  --header "Authorization:Bearer bcmcp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
两种方式 server 端看到的都是同一个 SSE 连接,行为完全一致,选你客户端支持的最简单那条。
:::

#### Claude Desktop

配置文件位置:
- macOS:`~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows:`%APPDATA%\Claude\claude_desktop_config.json`

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

完全退出 Claude Desktop(`Cmd+Q`)再启动 — 左下角看到 🔌 图标显示 "BeeCount" 已连接即可。

#### Cursor

配置文件位置:`~/.cursor/mcp.json`(或 Settings → Features → MCP UI 编辑)

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

重启 Cursor 即可。

#### Cline (VS Code)

VS Code → Cline 图标 → 右上角 `…` → **Edit MCP Settings**

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

### 3. 验证

在 LLM 客户端新建对话,输入:

> "查一下我有几个账本"

LLM 会调用 `list_ledgers` tool,返回你账本列表。

## 17 个可用 tool

### 查询(`mcp:read`)

| Tool | 用途 |
|---|---|
| `list_ledgers` | 列所有账本 |
| `get_active_ledger` | 当前默认账本 |
| `list_transactions` | 查交易,支持日期/分类/账户/关键词/金额范围筛选 |
| `get_transaction` | 单条交易详情 |
| `list_categories` | 列分类(可按 expense/income/transfer 筛) |
| `list_accounts` | 列账户(可按银行卡/信用卡/现金等筛) |
| `list_tags` | 列标签 |
| `list_budgets` | 列预算 + 当月已用进度 |
| `get_ledger_stats` | 账本统计(交易数/分类数/账户数/标签数/预算数) |
| `get_analytics_summary` | 月度/年度/全部范围的收入/支出/Top 分类 |
| `search` | 全文模糊搜交易备注、分类名、账户名 |

### 修改(`mcp:write`,需勾选)

| Tool | 用途 | 备注 |
|---|---|---|
| `create_transaction` | 新建交易 | |
| `update_transaction` | 改交易 | 只改传入的字段 |
| `delete_transaction` | 删交易 | **二次确认** — LLM 第一次调用返"待确认"占位符,你说"删"后才真删 |
| `create_category` | 新建分类 | |
| `update_budget` | 改预算金额 | |
| `parse_and_create_from_text` | 自然语言记账 | 让 BeeCount 自己的 AI 解析,需要先在 Web 配 AI provider |

## 安全模型

| 维度 | 措施 |
|---|---|
| Token 存储 | server 只存 `sha256` 哈希,常数时间比较;明文只在创建时返一次 |
| Token 撤销 | 软删除,被撤销后立即失效 |
| Token 过期 | 创建时可设,过期后自动 401 |
| Scope 分离 | `mcp:read` / `mcp:write` 独立勾选 |
| 删除保护 | `delete_transaction` 必须二次确认 |
| 协议隔离 | PAT 只能调 `/api/v1/mcp/*`,常规 API 拒绝 PAT。同样,普通 access token 也不能调 MCP endpoint |
| 审计 | 每次使用都记录 `last_used_at` + `last_used_ip`,Web 设置页可查 |

## 常见问题

### Q: 跟 BeeCount 自带的 AI(文字记账 / 拍照记账)有什么区别?

| | BeeCount 自带 AI | MCP |
|---|---|---|
| 触发位置 | App 内 | LLM 客户端(Claude Desktop / Cursor 等) |
| LLM 提供方 | 你配的 provider(GLM / OpenAI / 自部署) | LLM 客户端选的(Claude / GPT 等) |
| 能做的事 | 解析单笔文字/图片 → 创建交易 | 查询 + 多步对话 + 跨账本分析 + 批量操作 |
| 适合场景 | 单次记账 | 跟 LLM 多轮对话理解全局花销、做复盘 |

两者**互补**,可以同时用。

### Q: 必须公网部署 BeeCount Cloud 吗?

不必。只要 LLM 客户端跑的那台电脑能访问到 BeeCount Cloud 就行 — 局域网 IP(例如 `http://192.168.1.100:8869`)、Tailscale、ZeroTier 都可以。

### Q: token 不小心提交到 git 了

立即去 Web 设置页 **撤销**该 token,然后创建新的。即使 git 历史里有也没用了。

### Q: 想限制 LLM 不能删交易

创建 token 时**只勾选 `mcp:read`**,不勾 `mcp:write`。LLM 调任何 write tool 都会 403。

### Q: 多个 LLM 客户端能共用一个 token 吗?

可以,但**不推荐**。建议每个客户端单独建一个 token(`Claude Desktop` / `Cursor work` / `Cline laptop`),这样:
- 列表里能看到每个客户端最近什么时候用过
- 单独撤销某个客户端时不影响其他

## 相关链接

- [Model Context Protocol 官网](https://modelcontextprotocol.io)
- [BeeCount Cloud GitHub](https://github.com/TNT-Likely/BeeCount-Cloud)
- [服务端详细文档](https://github.com/TNT-Likely/BeeCount-Cloud/blob/main/docs/MCP.md)

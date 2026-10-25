---
sidebar_position: 1
slug: /mcp
description: 通过 MCP 的 55 个工具完成 BeeCount 账本查询、管理、导入、对账、小票草稿和 Cloud 周期记账。
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

LLM 会自动选择工具查询或记账。还可以让它预览对账单导入、比较账户余额、整理待核实项，或在确认后建立 Cloud 周期规则。具体步骤见 [工作流指南](./workflows.md)。

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
BeeCount Cloud server 暴露的是 **Streamable HTTP** 单端点(`/api/v1/mcp`)。

**原生支持 Streamable HTTP 的客户端**(如 Claude Code)**直连最省心**,不用桥:
```bash
claude mcp add --transport http --scope user beecount \
  https://your-beecount-cloud.com/api/v1/mcp \
  --header "Authorization:Bearer bcmcp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

下面 Claude Desktop / Cursor / Cline 的示例用 `npx mcp-remote` 给只支持 stdio 的客户端做桥接(兼容性最广);URL 用 `/api/v1/mcp`、不再带 `/sse`,mcp-remote 会自动协商 Streamable HTTP。

> 早期版本的老式 SSE 端点(`/api/v1/mcp/sse`)已被 Streamable HTTP 取代,不再提供。
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
        "https://your-beecount-cloud.com/api/v1/mcp",
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
        "https://your-beecount-cloud.com/api/v1/mcp",
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

### 3. 验证

在 LLM 客户端新建对话,输入:

> "查一下我有几个账本"

LLM 会调用 `list_ledgers` 返回账本列表。开始实际记账前，先用 `get_bookkeeping_context` 核对账本、账户/分类 ID、角色和 scope；有多个账本时让你选择，后续显式传 `ledger_id`。

## 55 个可用工具

共 **26 个读权限工具、29 个写权限工具**，另有 2 类资源模板和 2 个 Prompt。完整流程见 [导入、对账与自动记账](./workflows.md)。

:::info 完整工具集的版本要求
以下完整工具集对应 [Cloud #133](https://github.com/TNT-Likely/BeeCount-Cloud/pull/133)，需部署包含该变更的 Cloud，并完成 Alembic `0021_mcp_workflows` 迁移。Cloud 1.7.0 的原附件能力不包含全部新工具，以客户端连接后发现的工具为准。
:::

### 查询与读取（26 个，需要 `mcp:read`）

| Tool | 用途 |
|---|---|
| `list_ledgers` | 列所有账本 |
| `get_active_ledger` | 兼容默认账本查询；多账本先通过上下文选择 |
| `list_transactions` | 查交易,支持日期/分类/账户/关键词/金额范围筛选 |
| `get_transaction` | 单条交易详情 |
| `list_categories` | 列分类(可按 expense/income/transfer 筛) |
| `list_accounts` | 列账户(可按银行卡/信用卡/现金等筛) |
| `list_tags` | 列标签 |
| `list_budgets` | 列预算 + 当月已用进度 |
| `get_ledger_stats` | 账本统计(交易数/分类数/账户数/标签数/预算数) |
| `get_analytics_summary` | 月度/年度/全部范围的收入/支出/Top 分类 |
| `search` | 全文模糊搜交易备注、分类名、账户名 |
| `get_bookkeeping_context` | 选择账本，读取字典 ID、币种、角色与 PAT scope |
| `list_ledger_members` | 查看账本成员与角色 |
| `get_operation` | 查询持久化执行状态与逐步结果 |
| `list_operations` | 查找执行记录，找回丢失响应对应的操作 |
| `list_changes` | 增量读取交易变化与删除标记 |
| `get_account_balances` | 按账户和币种查询余额及覆盖范围 |
| `get_net_worth_history` | 分币种净值历史与明确的汇率覆盖 |
| `analyze_transactions` | 组合分析、分组、期间比较与明细追踪 |
| `list_attachments` | 列出账本附件 |
| `read_attachment` | 读取原图、小文本或原文件资源 |
| `export_transactions` | 保存完整 CSV 快照，最多 50,000 笔 |
| `list_workflow_records` | 查找导入、复核、规则与对账记录 |
| `get_workflow_record` | 读取持久化工作流及版本 |
| `list_transaction_sources` | 查看交易关联的来源凭证 |
| `reconcile_account` | 比较指定时点计算余额与实际余额 |

### 修改与工作流（29 个，需要 `mcp:write`）

| Tool | 用途 | 备注 |
|---|---|---|
| `upload_attachment` | 上传小票/图片 | Cloud 1.7.0 起，返回可关联到交易的文件 ID |
| `create_transaction` | 新建交易 | 可传 `attachments` 关联已上传文件 |
| `create_transactions` | 批量新建交易 | 最多 200 笔、每块最多 50 笔；支持逐笔附件与幂等键 |
| `update_transaction` | 改交易 | 只改传入的字段；可更新附件关联 |
| `delete_transaction` | 删交易 | **二次确认** — LLM 第一次调用返"待确认"占位符,你说"删"后才真删 |
| `create_category` | 新建分类 | |
| `update_budget` | 改预算金额 | |
| `parse_and_create_from_text` | 自然语言记账 | 让 BeeCount 自己的 AI 解析,需要先在 Web 配 AI provider |
| `manage_account` | 创建、修改或删除账户 | |
| `manage_category` | 管理分类与层级 | |
| `manage_tag` | 创建、修改或删除标签 | |
| `manage_budget` | 创建、修改或删除预算 | |
| `manage_ledger` | 创建、修改或删除账本 | |
| `retry_operation` | 续接允许重试的执行步骤 | |
| `parse_receipt` | 使用已配置视觉服务商生成小票草稿 | |
| `preview_text_transactions` | 生成文字记账草稿 | |
| `preview_import_file` | 映射原 CSV / TSV / XLSX 并保存导入计划 | |
| `preview_import` | 预览结构化交易并保存导入计划 | |
| `execute_import_plan` | 确认后执行指定版本的导入计划 | |
| `undo_import_plan` | 撤销本计划新建且未被后续修改的交易 | |
| `link_transaction_source` | 给交易关联来源身份 | |
| `unlink_transaction_source` | 移除来源关联，保留交易 | |
| `save_reconciliation_checkpoint` | 保存账户、来源与时间覆盖检查点 | |
| `save_review_item` | 保存待核实问题和用户答复 | |
| `save_classification_rule` | 保存推测或已确认分类规则及例外 | |
| `apply_classification_rule` | 保存目标集和修改前后预览 | |
| `execute_classification_preview` | 确认后执行带逐笔版本保护的分类预览 | |
| `manage_recurring_rule` | 预览、保存、暂停或恢复 Cloud 周期规则 | |
| `run_due_recurring_rules` | 执行到期周期规则 | |

## MCP 附件记账

从 **Cloud 1.7.0** 起，先调用 `upload_attachment` 上传小票，再将返回的 `file_id` 列表作为 `attachments` 传给 `create_transaction` 或 `update_transaction`。需要 `mcp:write` 权限，附件与交易必须在同一账本。

- 新建交易可以直接附上小票；修改已有交易时，不传 `attachments` 保留原附件，传 `[]` 清空关联，传列表替换全部关联。追加附件时先查询并保留原文件 ID。
- **HTTP 直连**接收 `content_base64`。若希望 AI 直接使用电脑上的文件路径，可在客户端运行仓库的 **本地 stdio 适配器** `scripts/mcp_local_files.py`，同名上传工具改为接收 `file_path`，程序读取并上传原始文件，模型无需输出 Base64。
- 本地适配器需配置 Cloud 地址、PAT 和允许读取的 `--allow-dir`；路径属于客户端电脑，Cloud 不会读取服务器任意路径。安装与配置见 [本地文件上传说明](https://github.com/TNT-Likely/BeeCount-Cloud/blob/main/docs/MCP.md)。
- 上传不会自动识别小票或创建交易。`parse_receipt` 可另行调用已配置视觉服务商生成草稿；确认后再创建交易。批量 `create_transactions` 同样支持逐笔附件。

上传关联后的图片可在 Web 和 App 查看。建议先升级 Cloud，再升级 **App 3.8.6**，以同步已有附件的顺序和信息变更。

### 本地原文件适配器

需要直接上传电脑里的原文件时，在客户端安装 Cloud 仓库的 Python 依赖，并运行 `scripts/mcp_local_files.py`。将下面的 Python、脚本和小票目录替换为本机实际路径，PAT 通过环境提供，不写入源码。

```sh
claude mcp add --transport stdio --scope user \
  --env BEECOUNT_MCP_PAT=bcmcp_xxx beecount -- \
  /absolute/path/to/python /absolute/path/to/BeeCount-Cloud/scripts/mcp_local_files.py \
  --endpoint https://your-beecount-cloud.com/api/v1/mcp \
  --allow-dir /absolute/path/to/receipts
```

适配器读取并上传 `file_path` 的原始字节，拒绝目录外文件、符号链接越界、空文件和特殊文件。它保留全部 Cloud 工具，并转发附件/导出资源与 Prompt。图片及 CSV、TSV、XLSX 都可以走同一个上传入口。

## 安全模型

| 维度 | 措施 |
|---|---|
| Token 存储 | server 只存 `sha256` 哈希,常数时间比较;明文只在创建时返一次 |
| Token 撤销 | 删除 token 后立即失效 |
| Token 过期 | 创建时可设,过期后自动 401 |
| Scope 分离 | `mcp:read` / `mcp:write` 独立勾选 |
| 确认与并发保护 | 删除、导入执行和分类执行等操作需要明确确认；交易修改可用 `expected_revision` 防止覆盖后续编辑 |
| 角色与重试 | 每次调用检查账本权限；幂等键和持久化执行记录支持安全续接 |
| 协议隔离 | PAT 只能调 `/api/v1/mcp`,常规 API 拒绝 PAT。同样,普通 access token 也不能调 MCP endpoint |
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

- [导入、对账与自动记账](./workflows.md)
- [Model Context Protocol 官网](https://modelcontextprotocol.io)
- [BeeCount Cloud GitHub](https://github.com/TNT-Likely/BeeCount-Cloud)
- [服务端详细文档](https://github.com/TNT-Likely/BeeCount-Cloud/blob/main/docs/MCP.md)

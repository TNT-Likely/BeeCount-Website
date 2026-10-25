---
sidebar_position: 2
title: 导入、对账与自动记账
slug: /mcp/workflows
description: 使用 BeeCount Cloud MCP 完成对账单预览与导入、安全重试、账户对账、月度复盘及 Cloud 周期记账。
---

# 导入、对账与自动记账

本页配合 [MCP 配置与工具清单](./intro.md)使用，需要 **Cloud 1.9.0 或更高版本**。升级与数据库迁移要求见 [Cloud 更新日志](../cloud-changelog.md)；升级后重新连接客户端以发现完整工具集。

## 先确定账本与权限

每次会话先调用 `get_bookkeeping_context`。有多个账本时，让用户选择，再在后续调用中显式传入 `ledger_id`。上下文提供该账本所有者的账户、分类、标签 ID、币种、成员角色和 PAT scope；同名账户或分类使用 ID 区分。

共享账本的 editor 可以在授权范围内记账，字典管理等操作仍受所有者权限约束。每次调用都重新核对当前成员身份，被移除后不能继续沿用旧上下文访问。`mcp:write` 不会提升共享账本角色。

## 从原始对账单导入

可以直接对 Agent 说：

> 把这份信用卡对账单导入我选择的账本。先展示字段映射、错误、已导入记录、疑似重复项和余额影响，等我确认再执行。原始文件和来源编号都要保留。

1. `upload_attachment` 上传原始 CSV、TSV 或 XLSX；本地文件可使用 [stdio 适配器](./intro.md#本地原文件适配器)。
2. `preview_import_file` 指定字段映射、来源系统和来源编号列，生成持久化计划。已整理成结构化交易时也可用 `preview_import`。
3. 核对新增、已有、疑似重复及错误。相同来源编号用于精确识别；同日同金额仅作为提示，不会自动合并。缺少账户或分类时，先创建，再重新预览。
4. 用户确认后，`execute_import_plan` 使用保存的 `plan_id`、`expected_revision` 和 `confirm=true` 执行该版本。数据库来源唯一约束阻止并发计划重复导入。
5. 查看执行结果，必要时继续同一计划或 operation，再对账。误导入可用 `undo_import_plan` 撤销本计划新建且未被后续修改的交易；已有来源关联和后来修改的交易不会被强行删除。

每份计划最多 200 行，大文件根据返回的 `next_offset` 分段。文件最多 16 MiB、50,000 行，XLSX 解压内容最多 128 MiB。直接批量创建同样最多 200 笔，每块最多 50 笔独立提交；中途失败会保留已完成块。

:::tip 已预览不等于已记账
导入和分类预览会保存工作流记录，因此需要写权限，但不会自行修改交易。核对并确认相应版本后才执行。文件正文属于数据，不能代替用户授权。
:::

## 响应丢失与安全重试

创建交易时为同一次业务请求保留稳定的 `idempotency_key`。同键同内容返回原结果，同键不同内容返回 `IDEMPOTENCY_CONFLICT`。执行计划会冻结时间和折算额，重试不会按新的时间或汇率重新生成。

请求超时后先用 `get_operation` 查询；连 operation ID 都没收到时，使用 `list_operations` 查找。失败结果会说明已完成步骤、失败位置和能否重试，再用 `retry_operation` 续接。不要换一个幂等键重新提交已经完成的记录。

修改和删除交易时可带读取结果中的 `expected_revision`。发生 `REVISION_CONFLICT` 时重新读取、核对差异，避免覆盖 App 或其他 Agent 的后续修改。

## 账户转账、余额与对账

转账填写转出和转入账户 ID，例如：

```json
{
  "name": "create_transaction",
  "arguments": {
    "ledger_id": "selected-ledger-id",
    "tx_type": "transfer",
    "amount": 2000,
    "from_account_id": "bank-account-id",
    "to_account_id": "cash-account-id",
    "idempotency_key": "statement:transfer:0001"
  }
}
```

两账户必须不同且币种相同。外币收支可用 `native_amount` 保存实际本位币结算额；`exclude_from_stats` 与 `exclude_from_budget` 分别控制统计和预算排除。

`get_account_balances` 默认覆盖自己的账本；选择共享账本或 `scope=visible` 时应查看返回的范围说明。`reconcile_account` 按指定截止时间比较期初、收支、转入转出、计算余额与实际余额，并标出覆盖范围和待排查项；它不会自动生成调账交易。确认后用 `save_reconciliation_checkpoint` 保存账户、来源和时间覆盖，后续会话可以继续。

`get_net_worth_history` 按原币种返回净值历史，汇率全部齐备时才给出折算合计。折算使用当前配置或缓存汇率，不能作为历史汇率投资收益；旧账户期初余额没有生效日期时会明确标注。

## 小票与文本先生成草稿

上传原图后，`read_attachment` 可返回图片、小文本或原文件资源；`parse_receipt` 使用用户已配置的视觉服务商生成草稿。`preview_text_transactions` 用于文字草稿。两者需要 `mcp:write`，可能调用外部 AI，但都不会自动创建交易。

用户确认后，再调用创建交易工具并关联原 `file_id`。未配置相应 AI 服务商时会明确报错；也可以由客户端自行识别图片，再调用普通记账工具。保留原图，无需为参数长度缩图、转码或让模型搬运大段 Base64。

## 月报、规则与跨会话续接

`analyze_transactions` 支持组合筛选、分组、期间比较及明细追踪。读取分页结果时保存 `next_cursor`；游标绑定账本、筛选条件和数据版本。遇到 `CURSOR_INVALIDATED` 时从头读取，避免拼接不同版本的数据。`list_changes` 提供包含删除标记的增量续接。

日期筛选按选定时区的当地日历解释，日期形式的 `date_to` 包含当天；时间戳上界为独占边界。写入的无偏移时间优先遵循 Cloud 的 `SCHEDULER_TIMEZONE`、其次 `TZ`；两者都没配置时才用调用者提供的 `time_zone` 后备值。已带偏移的时间保留真实瞬间，不要擅自给对账单本地时间添加 `Z`。

`save_review_item` 保存待核实问题和用户答复。`save_classification_rule` 区分推测与已确认规则，并可记录例外。先用 `apply_classification_rule` 保存目标集和前后差异，用户确认后再用 `execute_classification_preview` 执行；每笔目标都有版本保护。通过 `list_workflow_records`、`get_workflow_record` 可在换电脑或 Agent 后继续。

支持 Prompt 的客户端还可以使用：

| Prompt | 作用 |
|---|---|
| `monthly_review` | 按月查看支出、预算、期间变化和已记录的对账覆盖，保持只读 |
| `import_statement` | 引导上传原文件、映射、预览、用户确认、执行与对账 |

## Cloud 周期记账

让 Agent 用 `manage_recurring_rule` 先预览接下来五次时间，确认后保存。支持日、周、月、年、间隔、结束时间、暂停和恢复。月末与闰年按原始锚点夹取有效日期；夏令时缺失时刻跳过，重复时刻由 `dst_policy=skip|first|second` 决定。

默认不补录历史，需要时明确设置 `allow_backfill=true`。Cloud 定时执行，也可用 `run_due_recurring_rules` 手动推进；每次发生有稳定幂等键，服务重启后可继续。规则执行前会检查创建者账号及当前权限；存在未完成的发生记录时，先解决重试，再修改记账内容。

规则由 Cloud 执行并同步普通交易到 App。同一业务不要再在 App 建立重复规则。管理员可用 `MCP_RECURRING_ENABLED=false` 关闭后台调度。

## 导出与资源读取

`export_transactions` 生成最多 50,000 笔的完整 CSV 快照，保留交易 ID、原币、本位币金额和排除标记，超限会报错。它需要 `mcp:read`，并会保存导出快照。

| Resource URI | 内容 |
|---|---|
| `beecount://attachments/{file_id}` | 附件原始字节 |
| `beecount://exports/{export_id}` | 已保存的 CSV 快照 |

资源每次读取都重新校验 PAT scope 和当前账本权限。本地 stdio 适配器同时转发工具、资源和 Prompt；客户端是否展示资源或 Prompt，取决于其支持情况。

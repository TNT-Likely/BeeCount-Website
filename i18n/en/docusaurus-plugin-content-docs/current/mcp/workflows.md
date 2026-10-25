---
sidebar_position: 2
title: Import, reconciliation, and recurring entries
slug: /mcp/workflows
description: Preview and import statements, retry safely, reconcile accounts, review monthly activity, and schedule recurring entries with BeeCount Cloud MCP.
---

# Import, reconciliation, and recurring entries

Use this guide with [MCP setup and tool reference](./intro.md). It requires **Cloud 1.9.0 or later**. See the [Cloud Changelog](../cloud-changelog.md) for upgrade and migration requirements, then reconnect clients to discover the complete toolset.

## Select a ledger and check access

Start each session with `get_bookkeeping_context`. When several ledgers are available, ask the user to choose and pass that `ledger_id` in subsequent calls. Context includes the ledger owner's account, category and tag IDs, currency, membership role, and PAT scopes. Use IDs to distinguish identical names.

A shared-ledger editor can record transactions within their access, while dictionary management still requires the owner's permissions. Calls recheck membership, so removed members cannot continue using old context. `mcp:write` does not upgrade the member's role.

## Import an original statement

For example, ask your agent:

> Import this credit-card statement into the ledger I select. Show the field mapping, errors, existing records, possible duplicates, and balance effects before execution. Wait for my confirmation and retain the original file and source IDs.

1. Upload the original CSV, TSV, or XLSX with `upload_attachment`. For local files, use the [stdio adapter](./intro.md#local-original-file-adapter).
2. Call `preview_import_file` with the field mapping, source system, and source-ID column to save an import plan. Use `preview_import` for transactions already structured by the client.
3. Review new, existing, possibly duplicate, and invalid entries. Exact source IDs identify previously imported records; a matching date and amount only raises a review suggestion. Create missing accounts or categories, then preview again.
4. After user approval, call `execute_import_plan` with the saved `plan_id`, `expected_revision`, and `confirm=true`. Database source-identity constraints prevent concurrent plans from importing the same source twice.
5. Inspect results, continue the same plan or operation if needed, and reconcile. `undo_import_plan` removes only transactions newly created by that plan and unchanged since import. It preserves existing linked transactions and reports conflicts with later edits.

Each plan supports up to 200 rows. Follow `next_offset` for larger files. Files are limited to 16 MiB and 50,000 rows; uncompressed XLSX contents are limited to 128 MiB. Direct batch creation also supports at most 200 transactions, committed independently in chunks of up to 50. Completed chunks remain committed after a later failure.

:::tip A preview has not recorded transactions
Import and classification previews save workflow records and therefore need write scope. They change transactions only after the corresponding version is approved and executed. Statement contents are data and cannot authorize writes.
:::

## Recover from lost responses

Keep a stable `idempotency_key` for the same transaction-creation request. The same key and payload replay the original result; a different payload returns `IDEMPOTENCY_CONFLICT`. Saved plans freeze timestamps and settlement amounts, so retries do not regenerate them using a new time or exchange rate.

After a timeout, inspect `get_operation`. If the response containing the operation ID was lost, find it with `list_operations`. Results describe completed steps, failures, and retry eligibility; use `retry_operation` to continue. Do not switch keys and resubmit records that already succeeded.

For edits and deletions, pass the `expected_revision` returned when reading the transaction. On `REVISION_CONFLICT`, read again and review the difference to avoid overwriting later App or agent changes.

## Transfers, balances, and reconciliation

Provide both account IDs for a transfer:

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

Accounts must differ and use the same currency. For foreign-currency income or expenses, `native_amount` stores the actual settlement amount in the ledger's base currency. `exclude_from_stats` and `exclude_from_budget` independently control exclusion.

`get_account_balances` covers your own ledgers by default. Check the returned scope description when selecting a shared ledger or `scope=visible`. `reconcile_account` compares opening balance, income, expenses, transfers, calculated balance, and actual balance at a cutoff, including coverage and items needing investigation. It does not create adjustment transactions. After confirmation, use `save_reconciliation_checkpoint` to save account, source, and time coverage for future sessions.

`get_net_worth_history` returns history per original currency. A converted total is available only with complete rate coverage. Conversion uses currently configured or cached rates and is not historical FX investment return. Legacy opening balances without an effective date are explicitly identified.

## Preview receipts and text

After uploading the original image, `read_attachment` returns an image, small text, or an original-file resource. `parse_receipt` uses the configured vision provider to produce a draft; `preview_text_transactions` produces text-based drafts. Both require `mcp:write` and may call external AI, but neither creates transactions automatically.

After user confirmation, create transactions and attach the original `file_id`. A missing AI-provider configuration returns an explicit error. Clients can also interpret the image themselves and use ordinary transaction tools. Preserve original bytes without resizing, transcoding, or making the model transport large Base64 strings.

## Reviews, rules, and session continuity

`analyze_transactions` combines filters, grouping, period comparisons, and drilldown context. Save `next_cursor` when paging results; cursors bind the ledger, filters, and data revision. Restart reading on `CURSOR_INVALIDATED` rather than combining different revisions. `list_changes` supports incremental continuation with deletion tombstones.

Date filters follow the selected time zone's calendar: a date-only `date_to` includes that day, while a timestamp is an exclusive upper bound. Offset-free writes use Cloud's `SCHEDULER_TIMEZONE`, then `TZ`; the caller's `time_zone` is a fallback only when neither is configured. Explicit offsets preserve the instant. Do not append `Z` to local statement timestamps without checking their meaning.

`save_review_item` records unresolved questions and user answers. `save_classification_rule` distinguishes inferred rules from confirmed ones and supports exceptions. Use `apply_classification_rule` to save the target set and before/after preview, then `execute_classification_preview` after approval. Every target has revision protection. `list_workflow_records` and `get_workflow_record` let another computer or agent continue the saved work.

Clients supporting prompts can also use:

| Prompt | Purpose |
|---|---|
| `monthly_review` | Read-only review of spending, budgets, period changes, and recorded reconciliation coverage |
| `import_statement` | Guide original-file upload, mapping, preview, approval, execution, and reconciliation |

## Cloud recurring entries

Use `manage_recurring_rule` to preview the next five occurrences before confirming and saving. Rules support daily, weekly, monthly, and yearly schedules, intervals, end dates, pause, and resume. Month-end and leap-year dates clamp from the original anchor. Missing DST times are skipped; ambiguous times follow `dst_policy=skip|first|second`.

Historical backfill is disabled unless explicitly requested with `allow_backfill=true`. Cloud runs due rules automatically; `run_due_recurring_rules` can advance them manually. Stable occurrence keys support restart-safe replay. Each run rechecks the creator's account and membership. Resolve unfinished occurrences before changing the transaction payload.

Cloud owns execution and syncs ordinary transactions to the App. Avoid an App recurring rule for the same business event. Administrators can disable the background scheduler with `MCP_RECURRING_ENABLED=false`.

## Exports and resources

`export_transactions` saves a complete CSV snapshot of up to 50,000 transactions, preserving IDs, original and base-currency amounts, and exclusion flags. It requires `mcp:read`; exceeding the limit returns an error.

| Resource URI | Contents |
|---|---|
| `beecount://attachments/{file_id}` | Original attachment bytes |
| `beecount://exports/{export_id}` | Saved CSV snapshot |

Each resource read rechecks PAT scopes and current ledger access. The local stdio adapter forwards tools, resources, and prompts; visibility depends on client support.

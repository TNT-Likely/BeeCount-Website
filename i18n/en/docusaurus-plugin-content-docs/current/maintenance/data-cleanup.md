---
sidebar_position: 1
title: Data Cleanup
description: BeeCount Data Cleanup guide — clean up orphan local data in the App, clean up server-side orphan data in the Web admin console, scan / select / batch delete, reclaim disk space.
keywords: [data cleanup, orphan data, BeeCount maintenance, attachment cleanup, disk space, self-host admin]
---

# Data Cleanup

After long-term use, a finance app inevitably accumulates **"orphan data"** in its local database or attachment folders: tag links to deleted transactions, attachment files without DB rows, sub-categories whose parent was deleted… None of it breaks daily use, but it eats space, slows down sync, and becomes a time bomb long term.

Starting with App 3.2.0 / Cloud 1.3.0, BeeCount ships a **manual data cleanup tool**: it scans for all orphan data, lists them by group, and lets the user confirm before deleting — nothing runs automatically, nothing is silently removed. **Every cleanup is visible.**

There's one tool on the App side and one in the Web admin console, each responsible for its own data layer.

## App side: local data cleanup

### How to open

「Me」 → 「Data Management」 → 「Data Cleanup」

### Scope

Only cleans **data on the current device**: Drift / SQLite database rows + attachments / icon files in the app sandbox + `sync_queue` pending change records. Does **not** touch BeeCount Cloud server data.

### Workflow

1. The page starts scanning on open (you can also tap the refresh icon to rescan manually).
2. Detected orphans are listed in three groups:
   - **Database orphans** (Type A — 10 kinds)
   - **Disk file orphans** (Type B — 3 kinds)
   - **Sync queue orphans** (Type C — 1 kind)
3. Each record shows a title + subtitle (e.g. "Budget #5 · ¥3000 · ledger deleted"); records can be selected one by one or by group.
4. Footer shows "N selected, ~X MB reclaimable".
5. Tap "Clean Selected" → confirmation dialog → execute → auto rescan.

### App-side detection list

#### Type A: database reference broken

| ID | Type | Description |
|---|---|---|
| A1 | Budget pointing to deleted ledger | `budgets.ledger_id` no longer in `ledgers` |
| A2 | Attachment pointing to deleted tx | `transaction_attachments.transaction_id` missing |
| A3 | Tag link pointing to deleted tx | `transaction_tags.transaction_id` missing |
| A4 | Tag link pointing to deleted tag | `transaction_tags.tag_id` missing |
| A5 | Tx account missing | `tx.account_id` or `to_account_id` not in `accounts` |
| A6 | Tx category missing | `tx.category_id` not in `categories` |
| A7 | Sub-category parent missing | `categories.parent_id` not found |
| A8 | Budget category missing | `budgets.category_id` not found |
| A9 | Shared sub-category parent missing | `shared_ledger_categories.parent_sync_id` missing |
| A10 | Tag override missing tx | `transaction_tag_overrides` whose tx is gone |

#### Type B: disk file orphans

| ID | Type | Description |
|---|---|---|
| B1 | Attachment file with no DB ref | File under `attachments/` not referenced by any `transaction_attachments` row |
| B2 | Custom category icon with no DB ref | File under `category_icons/` not referenced by any `categories.custom_icon_path` |
| B3 | Shared category icon cache with no ref | Shared ledger icon sha256 cache no longer referenced |

#### Type C: sync state orphans

| ID | Type | Description |
|---|---|---|
| C1 | `sync_queue` orphan entity | `local_changes` row whose target entity has been deleted |

### Common situations

- **Lots of A2 / A3**: cascade cleanup never caught up after bulk-deleting transactions
- **B1 eating hundreds of MB**: attachment files left behind after deleting transactions (older versions didn't auto-clean)
- **A9 + B3**: you used a shared ledger and were kicked / left, but local mirror data still around

### Notes

:::warning Back up before cleaning
We recommend exporting CSV / triggering a cloud sync first. Cleanup is **irreversible** and is not uploaded to cloud backup.
:::

:::tip Failure handling
In rare cases (e.g. attachment file held by another process) a delete can fail. The failure list will show the specific reason — just rescan and try again.
:::

## Web side: admin data cleanup

### How to open

Top-right avatar dropdown → 「Admin · Data Cleanup」 (admin only)

Direct link: `https://your-deploy-domain/app/admin/data-cleanup`

:::warning Admin only
Regular users will not see this entry in the avatar menu. Self-host admins need to set their account's `is_admin = true`; see the [BeeCount Cloud deployment doc](../cloud-sync/beecount-cloud).
:::

### Scope

Cleans **server-side orphan data across all users**: Postgres / SQLite database rows + files under `/data/attachments` + `sync_changes` anomalies.

**Completely independent from the App tool** — the Web tool cleans the server, the App tool cleans the device. They neither conflict nor substitute for each other.

### Workflow

Same as the App side: scan → three groups → select → single / batch delete → confirmation → auto rescan.

### Web-side detection list

#### Type A: database reference broken

| ID | Type | Description |
|---|---|---|
| A1 | Tx category missing | `tx_missing_category` — `read_tx_projection` row whose category is deleted |
| A2 | Tx account missing | `tx_missing_account` |
| A3 | Tx from-account missing (transfer) | `tx_missing_from_account` |
| A4 | Tx to-account missing (transfer) | `tx_missing_to_account` |
| A5 | Budget category missing | `budget_missing_category` |
| A6 | sync_changes orphan entity | `sync_change_missing_entity` — drop subsequent LWW writes |

#### Type B: attachments / files

| ID | Type | Description |
|---|---|---|
| B1 | AttachmentFile with no ref | `AttachmentFile` row not referenced by any tx / category icon |
| B2 | Attachment file missing | `AttachmentFile.storage_path` points to a file no longer on disk |
| B3 | Disk file without DB row | File present under `/data/attachments` with no `AttachmentFile` row (auto-skips `profile-avatars/`) |
| B4 | Tx attachment reference broken | `fileId` in tx `attachments_json` does not exist in `AttachmentFile` |

### Notes

:::warning Affects all users
Web-side cleanup acts on **all users' data**. Deleting a `sync_changes` row is not propagated back to clients — it's equivalent to dropping that LWW write. Deleting a storage file makes any client request for that attachment return 404.
:::

:::tip Back up first
Admins should run a [data backup](../cloud-sync/beecount-cloud#backup) (rsync the whole `data/` directory, or `sqlite3 .backup` / `pg_dump`) before cleanup.
:::

### Profile-avatars protection

The tool auto-skips `profile-avatars/`, so user avatars will not be misidentified as orphan files. This is a fix shipped in 1.3.1 — older builds may have wrongly cleaned avatars, please upgrade if you're on an older version.

## Design principles

Both tools follow the same principles:

- **Manual trigger** — no auto-runs, no silent background cleanup. All deletes are explicit user actions.
- **Fully visible** — every orphan has a title + subtitle, so the user knows exactly what they're deleting.
- **Group + select** — single record or per-group select-all, fine-grained control.
- **Double confirmation** — tapping clean opens a confirmation dialog noting the action is irreversible.
- **Failure tolerance** — one failure in a batch doesn't stop the rest; the failure list shows each specific reason.
- **Size summary** — file orphans show size, helping decide "is it worth cleaning".

## When to use

Run it periodically (e.g. quarterly), or in these situations:

- App disk usage spiking noticeably without the actual dataset growing
- After bulk-deleting transactions / ledgers / categories
- After leaving / being kicked from a shared ledger and wanting to clear local mirrors
- Self-host admin notices the storage directory growing unexpectedly
- A sync after upgrade reports strange reference errors

## Privacy

- The App tool runs fully offline; scan results are not uploaded anywhere.
- The Web tool runs on your own BeeCount Cloud deployment; data stays on your server.
- The BeeCount team does not collect any user data via these tools — both are pure local / local-deploy computation.

---
sidebar_position: 102
description: "BeeCount version history and feature release notes. 3.0 introduces self-hosted BeeCount Cloud sync and Web access."
keywords: [BeeCount changelog, BeeCount releases, BeeCount versions]
---

# Changelog

View BeeCount's version update history.

👉 [GitHub Releases](https://github.com/TNT-Likely/BeeCount/releases)

All version details, release notes, and download links are available on the GitHub Releases page.

## Cloud 1.3.8 highlights

- 🐛 **Net-worth math fix**: the web Assets page used to sum `Math.abs(balance)` for every account, so overdrawn asset accounts (e.g. `cash` / `bank_card` with `balance < 0`) flipped sign and inflated total assets. Real-world data with 5 accounts (actual 89.5K) was showing 167K. Now sums signed balances, matching the mobile `getNetWorthBreakdown` convention
- 🎯 **Home Top cards now scope to current ledger**: previously OverviewPage fetched workspace accounts/tags without `ledger_id`, so `tx_count` / `balance` / `expense_total` were cross-ledger aggregates — out of sync with the rest of the home dashboard
- 🔀 **Detail dialogs gained an All-ledgers / Current-ledger toggle**: Account / Category / Tag detail dialogs now have a segmented toggle. Entering from the Assets / Categories / Tags top-level pages defaults to all ledgers with a ledger-name chip per row; entering from home Top cards or chart drilldowns defaults to current ledger
- 🖱 **Home "Top tags" / "Top accounts" cards now open detail dialogs**: previously they only navigated to the transactions search view; now clicking opens the corresponding detail dialog, matching mobile behavior

## Cloud 1.3.7 highlights

- 🧹 **New `scripts/compact_sync_changes.sh`**: one-shot compaction of historical duplicates in the `sync_changes` table (collapses rows with the same `user × entity_type × entity_id` down to the row with the largest `change_id`). Long-running instances accumulate redundant sync rows over time; running this once meaningfully shrinks the DB and speeds up fullPull

## Cloud 1.3.6 highlights

- 🤝 **Shared-ledger Editor delete now cleans up attachments**: when an Editor deleted a transaction with attachments, the server used to drop the tx row but leave the attachment files behind as orphans until the next cleanup pass. Delete now cascades immediately, matching Owner behavior
- 🗜 **Entity delete auto-compacts `sync_changes`**: when a delete row is written, prior `update` rows for the same entity are folded in, further capping sync-log growth

## 3.2.3 highlights

- 📅 **Calendar page: record on the selected date**: tap a date and add transactions directly without switching tabs first; page loads use skeleton screens for a smoother feel
- 🤖 **AI multi-transaction recognition**: image / voice / text entries all now support detecting **multiple** transactions in one shot — great for recording a batch at once
- 🛡 **Fixed sync log bloat across devices**: concurrent fullPush no longer pushes duplicates, so `sync_changes` won't grow unboundedly when multiple clients trigger sync at the same time

## 3.2.2 highlights

- 🤖 **Fixed AI custom prompt being ignored**: some entry points skipped init and always fell back to the default template; every code path now honors the user's custom prompt
- 💬 **More accurate AI failure messages**: no longer always reports "AI not configured" — the specific reason (network / API key / quota / model unsupported) surfaces in the UI and is logged for debugging
- 📲 **Fixed in-app updater picking the wrong APK architecture**: arm64 devices were occasionally installing the armv7 build, causing severe lag for the first-time install experience

## 3.2.1 highlights

- 📦 **Android APK shrunk by 77%** (70.2 MB → 16 MB): removed OCR, split per ABI (arm64 main / armv7 compat / x86_64 emulator / universal fallback), deleted tflite dead code
- 🤖 **OCR replaced by AI vision**: dropped `google_mlkit_text_recognition`, all image billing flows (UI, Android screenshot listener, iOS auto-billing) now use GLM-4V class LLM vision; clear fallback messages when AI is not configured
- ⚡ **Sync performance**: pulling 10k records via WebDAV/Supabase from a few minutes to seconds; CSV import with tags from tens of minutes to seconds
- 🛡 **Sync stability**: full-page rollback + cursor only advances after apply, e2e test infra with 32 cases, UI ↔ SyncEngine decoupled via SyncEvent stream — no more home flicker
- 🎯 **Default ledger optional**: welcome page adds a "Create default ledger" checkbox; the home pill becomes "+ New Ledger" when no ledger exists, tapping opens the ledger creator directly
- 🧭 **Menu reorg**: budget management moved to "Ledger Management → long press a ledger" (per-ledger budgeting); app lock moved into "Personalization" (low-frequency feature folded into app preferences); "Appearance" renamed to "Personalization"

## 3.2.0 highlights

- 🤝 **Shared ledgers**: collaborative bookkeeping across users. Owner invites Editors to a shared ledger; categories/accounts/tags are fanned out via server WebSocket to every member
- 🌐 Domain migrated to `beejz.com` family
- 🔧 **User-global resources**: custom categories/accounts/tags + custom icons sync per `user_id` and are shared across ledgers
- 📦 `sync_engine` split into parts: realtime / apply / serialization / attachments / resolvers / status
- 🤖 MCP tool kit + TestFlight channel
- 📱 Store compliance: iOS app name localized, OpenAI mentions removed, Google Play permissions stripped (READ_MEDIA_*)

## 3.0.0 highlights

- 🆕 [**BeeCount Cloud**](./cloud-sync/beecount-cloud) — self-hosted sync server
- 🌐 Web UI bundled in the Docker image, PWA installable
- 🔄 Realtime multi-device sync: phone + Web + tablet within seconds
- 👥 Multi-user isolation: one server hosts many accounts with separate data

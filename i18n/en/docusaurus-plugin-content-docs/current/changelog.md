---
sidebar_position: 102
description: "BeeCount version history and feature release notes. 3.0 introduces self-hosted BeeCount Cloud sync and Web access."
keywords: [BeeCount changelog, BeeCount releases, BeeCount versions]
---

# Changelog

View BeeCount's version update history.

👉 [GitHub Releases](https://github.com/TNT-Likely/BeeCount/releases)

All version details, release notes, and download links are available on the GitHub Releases page.

## 3.5.0 highlights

- 💱 **Multi-currency**: set a base currency, maintain exchange rates per currency, and have the asset page convert accounts into the base currency for one unified summary (single-currency setups are unchanged). See [Multi-currency](./account/multi-currency.md). Self-hosted users need to upgrade **BeeCount Cloud to 1.5.0** (base-currency sync / manual rates / rate proxy are provided by the server).
- 📈 **Net worth over time**: a net worth trend chart on the asset page — switch between Trend and Composition with one tap; the full-screen page supports 3 / 6 / 12 month and all-time ranges × net worth / total assets / total liabilities. Net worth, composition, and trend are all converted to the base currency, and shared ledgers you joined as a member are always excluded. See [Net worth over time](./account/net-worth-trend.md).
- 🎨 **4 new header skins**; Android 13+ **dynamic themed icon** (follows the system color).
- 🔘 A visible action entry in the bottom-right of each ledger card (equivalent to the long-press menu — budget management and friends are no longer hard to find).
- 📖 "Help" now opens the documentation center in an embedded WebView.

## 3.4.0 highlights

- 📅 **Month Start Day**: each ledger can define when "this month" begins (1-28) — great for payday budgeters and credit-card statement cycles. Home, statistics, budgets, annual reports, widgets, AI — the entire pipeline follows your accounting period, synced across devices. See the [docs](./account/month-start-day.md). Self-hosted users need to upgrade **BeeCount Cloud to 1.4.0** (web is on the same cycle; the upgrade also auto-fixes a historical under-count in web account statistics).
- 🍎 **iOS 27 compatibility**: the Shortcuts auto-recording flow no longer gets interrupted by missing notification permission — bookkeeping works even without granting notifications.

## 3.3.0 highlights

- 🎨 **Skins**: decorative header artwork on the home screen follows your theme color — built-in gradient / scene / geometric styles, works in both light and dark mode, syncs across devices, with config import/export.
- ➕ **Keypad arithmetic**: the amount keypad now supports + − × ÷ — long-press or double-tap to switch; handy for splitting bills or merging receipts right on the keypad.
- 👤 **Custom nickname**: edit your display name from the avatar entry on the "Me" page, paired with a time-of-day greeting.

## 3.2.4 / 3.2.5 highlights

- 🤖 AI recording compatibility: string amounts, Chinese-formatted dates, and inference-model parameter quirks all handled; auto-tagging now respects the "auto-tag" toggle.
- 🗂 Categories support the same name for expense and income; the transaction list always shows the category name.
- 💳 Account & asset management overhaul: edit page redesigned, credit-card display aligned (web updated to match; asset page isolates by currency).
- 🔁 Recurring transactions no longer allow selecting a past start date, preventing retroactive dirty data.

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

---
sidebar_position: 102
description: "BeeCount version history and feature release notes. 3.0 introduces self-hosted BeeCount Cloud sync and Web access."
keywords: [BeeCount changelog, BeeCount releases, BeeCount versions]
---

# Changelog

View BeeCount's version update history.

👉 [GitHub Releases](https://github.com/TNT-Likely/BeeCount/releases)

All version details, release notes, and download links are available on the GitHub Releases page.

## 3.5.5 highlights

- 🎙 **"Hold to talk" for voice bookkeeping**: a new WeChat-style trigger mode — hold to record, release to recognize, so longer entries are never cut off; switch it in Settings → Smart Billing. See [Voice Recording](./ai/voice.md).
- ⏱ **Adjustable pause detection**: in auto-detect mode the pause threshold is relaxed from a fixed 0.8s to a default of 1.5s and is now adjustable (0.5–4s), so a natural mid-sentence pause no longer ends recognition early; both the trigger mode and pause duration sync across devices.

## 3.5.2 highlights

- 🏷 **Switchable note display**: the transaction list adds a "Note display" option — "Category first" (category name + note in small text, the default) or "Note first" (show the note when present); prefer the classic style? Switch back in Settings → Appearance. The same on web requires **BeeCount Cloud 1.5.2**.
- 💱 **Many more currencies**: supported currencies expanded from 45 to **151**, covering the full set of international currencies (added Kenyan Shilling (KES), Central/West African CFA Franc (XAF/XOF), and more across Africa, the Middle East, and Latin America). See [Multi-currency](./account/multi-currency.md). The same expansion on web requires **BeeCount Cloud 1.5.2**.
- ☁️ **Cloud sync page guide**: the sync page adds a collapsible explainer — how incremental vs full sync works, why it sometimes stalls (full upload/download has no resume), and how to check the Log Center when something goes wrong — to cut down on "why won't it sync?" confusion.

## 3.5.1 highlights

- 🚩 **Transaction flags**: each transaction has two independent toggles — Exclude from Income/Expense and Exclude from Budget. Keep reimbursements from inflating your stats and one-off costs from throwing off your budget; flags **do not affect account balance or net worth** — the record stays, it just doesn't count toward stats/budget. See [Transaction flags](./record/flags.md). Self-hosted users need to upgrade **BeeCount Cloud to 1.5.1** (server-side filtering of income/expense and budget by flag; local stats are unaffected).
- 🤖 **More accurate and stable AI recognition**: non-receipt images are no longer misrecognized as transactions; relaxed vision/voice timeouts make large images and files less likely to time out.
- 🔁 Fixed an issue where "daily" recurring transactions could not be generated.
- 🖼 Clearer prompt when an image is recognized as not being a receipt.
- 📲 Fixed an issue where, on some devices, opening the entry screen from a browser or shortcut occasionally did nothing.

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

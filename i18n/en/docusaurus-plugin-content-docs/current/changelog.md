---
sidebar_position: 102
description: "BeeCount version history and feature release notes. 3.0 introduces self-hosted BeeCount Cloud sync and Web access."
keywords: [BeeCount changelog, BeeCount releases, BeeCount versions]
---

# Changelog

View BeeCount's version update history.

👉 [GitHub Releases](https://github.com/TNT-Likely/BeeCount/releases)

All version details, release notes, and download links are available on the GitHub Releases page.

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

---
sidebar_position: 103
sidebar_label: Cloud Changelog
description: Core BeeCount Cloud releases, Web and sync improvements, and upgrade notes.
keywords: [BeeCount Cloud changelog, self-hosted cloud releases]
---

# Cloud Changelog

Core releases and recent maintenance updates for self-hosted BeeCount Cloud. The App uses a separate version series; see the [App Changelog](./changelog.md).

This page covers core releases from 1.0.0 through 1.6.9. Dates are GitHub Release publication dates in UTC. See [Cloud GitHub Releases](https://github.com/TNT-Likely/BeeCount-Cloud/releases) for all maintenance releases, Docker images, and commits, or the source [CHANGELOG](https://github.com/TNT-Likely/BeeCount-Cloud/blob/main/CHANGELOG.md) for unreleased changes.

:::tip Upgrades and compatibility

For features that require both products, upgrade Cloud before the App. Back up your data and review the [deployment and upgrade guide](./cloud-sync/beecount-cloud.md). The MCP URL change in 1.5.3 also requires client configuration updates.

:::

## 1.6.9 · 2026-10-04

- **MCP consistency fixes**: improved transaction associations and batch input consistency.
- **Build maintenance**: frontend builds use a native platform to avoid QEMU build issues.

[GitHub Release 1.6.9](https://github.com/TNT-Likely/BeeCount-Cloud/releases/tag/1.6.9)

## 1.6.8 · 2026-10-04

- **Business and AI provider help**: the About page links to business inquiries, and AI settings link to provider setup guidance. Self-hosted instances can disable these entries.
- **MCP time fix**: corrected transaction timezone offsets.

[GitHub Release 1.6.8](https://github.com/TNT-Likely/BeeCount-Cloud/releases/tag/1.6.8)

## 1.6.7 · 2026-09-25

- **Account balance adjustment**: directly adjust a balance or record the difference as a regular transaction. Net-worth history supports the new adjustment rules.

[GitHub Release 1.6.7](https://github.com/TNT-Likely/BeeCount-Cloud/releases/tag/1.6.7)

## 1.6.6 · 2026-09-06

- **Duplicate submission prevention**: transaction submission blocks repeated clicks while a request is in progress.

[GitHub Release 1.6.6](https://github.com/TNT-Likely/BeeCount-Cloud/releases/tag/1.6.6)

## 1.6.5 · 2026-09-04

- **Hybrid document retrieval**: AI documentation search combines vector and keyword retrieval.

[GitHub Release 1.6.5](https://github.com/TNT-Likely/BeeCount-Cloud/releases/tag/1.6.5)

## 1.6.4 · 2026-09-03

- **Dynamic documentation index updates**: update the documentation index and inspect its version without rebuilding the Cloud image.

[GitHub Release 1.6.4](https://github.com/TNT-Likely/BeeCount-Cloud/releases/tag/1.6.4)

## 1.6.3 · 2026-08-13

- **Multi-currency AI recording**: AI recognition can record transactions in their matching currencies.
- **Anniversary themes**: Web settings support anniversary themes and synchronize the theme color for themes with a fixed palette.

[GitHub Release 1.6.3](https://github.com/TNT-Likely/BeeCount-Cloud/releases/tag/1.6.3)

## 1.6.2 · 2026-08-02

- **Compatibility maintenance**: corrected the rclone provider used for Tencent COS and constrained MCP dependencies to preserve compatibility.

[GitHub Release 1.6.2](https://github.com/TNT-Likely/BeeCount-Cloud/releases/tag/1.6.2)

## 1.6.1 · 2026-07-20

- **Hidden accounts**: account visibility synchronizes through the server and is supported on the Web. Historical transactions, balances, and net worth are retained.

[GitHub Release 1.6.1](https://github.com/TNT-Likely/BeeCount-Cloud/releases/tag/1.6.1)

## 1.6.0 · 2026-07-12

- **Transaction-level multi-currency**: transactions retain their original currency amounts while ledger statistics convert them into the base currency. Amount edits update the conversion.

[GitHub Release 1.6.0](https://github.com/TNT-Likely/BeeCount-Cloud/releases/tag/1.6.0)

## 1.5.3 · 2026-07-04

- **MCP transport upgrade**: switched to Streamable HTTP at the single `/api/v1/mcp` endpoint. Clients must update their URLs; existing PATs remain valid.

:::caution Update MCP client URLs

The old `/api/v1/mcp/sse` and `/api/v1/mcp/messages/` endpoints are no longer available. Configure `/api/v1/mcp` instead; see [MCP setup](./mcp/intro.md).

:::

[GitHub Release 1.5.3](https://github.com/TNT-Likely/BeeCount-Cloud/releases/tag/1.5.3)

## 1.5.2 · 2026-06-23

- **151 currencies**: expanded the currency list to ISO 4217 coverage with localized names.
- **Note display preferences**: Web transactions support category-first or note-first display.

[GitHub Release 1.5.2](https://github.com/TNT-Likely/BeeCount-Cloud/releases/tag/1.5.2)

## 1.5.1 · 2026-06-19

- **Transaction flags**: exclude a transaction from income/expense totals or budgets with consistent server and Web handling. Flags do not change account balances.

[GitHub Release 1.5.1](https://github.com/TNT-Likely/BeeCount-Cloud/releases/tag/1.5.1)

## 1.5.0 · 2026-06-12

- **Base currency and exchange rates**: synchronize the base currency, maintain manual rates, and support an exchange-rate proxy and converted Web views.
- **Net-worth trends**: added net-worth history and asset trend/composition views with totals converted into the base currency.

[GitHub Release 1.5.0](https://github.com/TNT-Likely/BeeCount-Cloud/releases/tag/1.5.0)

## 1.4.0 · 2026-06-10

- **Custom month start day**: ledger reporting periods synchronize across statistics, budgets, and the Web.
- **Account statistics fix**: completed transaction-to-account associations and backfilled existing data to correct missing account totals.

[GitHub Release 1.4.0](https://github.com/TNT-Likely/BeeCount-Cloud/releases/tag/1.4.0)

## 1.3.0 · 2026-05-20

- **Shared ledgers**: owners can invite editors to collaborate.
- **Data cleanup fixes**: addressed avatar misclassification, database locking, and stuck deletion.

[GitHub Release 1.3.0](https://github.com/TNT-Likely/BeeCount-Cloud/releases/tag/1.3.0)

## 1.2.0 · 2026-05-13

- **MCP and PATs**: AI clients can query, create, and edit ledger data, with MCP call history available in Web settings.
- **Attachment viewing**: Web transaction details support attachment thumbnails and full-image previews.

[GitHub Release 1.2.0](https://github.com/TNT-Likely/BeeCount-Cloud/releases/tag/1.2.0)

## 1.1.0 · 2026-05-07

- **Web workspace improvements**: added calendar and annual-report views, batch deletion/export, and CSV/TSV/Excel imports with field mapping and previews.
- **AI recording and documentation answers**: added image/text recording, AI provider settings, and documentation retrieval.
- **Security and backup**: introduced 2FA/TOTP and rclone-based cloud backup and restore.

[GitHub Release 1.1.0](https://github.com/TNT-Likely/BeeCount-Cloud/releases/tag/1.1.0)

## 1.0.0 · 2026-04-19

- **Stable self-hosted Cloud release**: a Docker image bundles the sync service and Web console, with bidirectional App/Web synchronization, isolated user data, and shared preferences.
- **Initial database schema**: consolidated the initial migrations before the stable release.

[GitHub Release 1.0.0](https://github.com/TNT-Likely/BeeCount-Cloud/releases/tag/1.0.0)

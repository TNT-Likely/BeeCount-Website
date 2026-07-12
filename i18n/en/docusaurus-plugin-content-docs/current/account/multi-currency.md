---
sidebar_position: 5
description: "BeeCount multi-currency: set a base currency, maintain exchange rates per currency, and let the asset page convert every account into your base currency for one unified net worth — for travelers, overseas assets, and multi-currency wallets."
keywords: [multi-currency, base currency, exchange rate, foreign currency assets, BeeCount multi-currency]
---

# Multi-Currency (Base-Currency Conversion)

> ✨ **New in v3.5.0**. Self-hosted users require BeeCount Cloud ≥ 1.5.0.

You hold CNY, USD, and JPY accounts at the same time, but the asset page only groups them by currency — you can't add them up. Multi-currency lets you **set one base currency**, **maintain an exchange rate** for every other currency, and have the asset page convert all accounts into that base currency for a single, unified net worth figure.

:::info Only one currency? Nothing to do
If all your accounts use the same currency, behavior is identical to previous versions — no conversion is shown, no base currency is needed. This feature is invisible to you.
:::

:::info Full international currency coverage (since v3.5.2)
The selectable currencies now cover the full ISO 4217 set — **151** in total (added Kenyan Shilling (KES), Central/West African CFA Franc (XAF/XOF), and more across Africa, the Middle East, and Latin America). Major currencies show localized names; the rest use standard English names. Custom currencies are not supported.
:::

## In-Ledger Multi-Currency Transactions (v3.6.0)

Since v3.6.0, multi-currency extends beyond the asset-page conversion below to **every transaction inside a ledger**:

- Each ledger has a **base currency** (formerly the "ledger currency", set on the ledger edit page) — the ledger's monthly totals, category summaries, and budget usage all use it as the reference
- When recording, you can **choose the transaction's currency**: it follows the account's currency when an account is selected, or you can pick it manually when no account is chosen; for a foreign currency, the amount converted to the ledger base currency previews live under the amount
- The ledger's stats **automatically convert foreign transactions to the base currency at the exchange rate** before summing, so different currencies in one ledger finally add up
- Every transaction always **keeps the original amount you actually paid**; the converted snapshot is taken at record time and then **fixed** — changing a rate later never alters the recorded conversion of past transactions

:::info "Ledger base currency" vs "user base currency" — two levels
The "user base currency" in the lower half of this page converts different-currency **accounts** across ledgers into one net worth figure on the asset page; the "ledger base currency" here converts different-currency **transactions** within a single ledger for its stats. They are separate, but **share the same rates you maintain**. Single-currency ledgers are unaffected.
:::

## Set a Base Currency

1. Go to **Me** → **Multi-currency / Exchange rates** (or the settings entry next to the converted summary on the asset page)
2. Choose a **base currency** — the asset page's unified summary and the net worth trend both use it as the reference
3. The base currency setting syncs to all devices

The base currency is a **user-level** setting (it applies to all your ledgers), not a per-ledger setting.

## Manage Exchange Rates

Maintain **other currency → base currency** rates on the same page:

1. Tap the currency you want to add or edit
2. Enter the rate against the base currency (e.g. if the base is CNY, enter "1 USD = 7.x CNY" for USD)
3. Saving takes effect immediately and the asset page re-converts

- Rates are **manually maintained** fixed values — after changing the base currency you need to re-check each currency's rate
- The web (self-hosted) can edit rates too; changes sync to your phone within seconds
- Self-hosted BeeCount Cloud provides an **exchange-rate proxy**, so reference rates can be fetched server-side (see the server docs). Manual rates edited in the App / Web always take priority.

## Converted Summary on the Asset Page

Once a base currency and rates are set, the top of the asset page shows a **unified summary converted to the base currency**:

- Total assets / total liabilities / net worth are all converted into the base currency and summed
- The existing **per-currency grouped breakdown** stays unchanged — the converted summary is an overview layer on top of it
- The [net worth trend](./net-worth-trend.md) chart is also drawn in the base currency

## Notes

- **Set a base currency first**: without one, the asset page keeps grouping by currency and performs no conversion
- **Currencies missing a rate**: if a currency has no rate to the base currency, its accounts **cannot be converted** and are **excluded** from the base-currency summary (they still appear in the grouped breakdown). Add a rate for every currency you actually use.
- **Manual, not real-time**: rates are fixed values you enter; they do not auto-update with the market. Recalibrate manually for large amounts or volatile rates.
- **Conversion only affects display**: the original currency and amount of every transaction and account are stored as-is. Conversion happens only in the asset page's summary layer — changing the base currency or a rate never alters any account balance.

## Version Requirements

| Feature | App | BeeCount Cloud (self-hosted) |
|---|---|---|
| Asset-page conversion (user base currency) | ≥ 3.5.0 | ≥ 1.5.0 |
| In-ledger multi-currency transactions (ledger base currency) | ≥ 3.6.0 | ≥ 1.6.0 |

- **Asset conversion (v3.5.0)**: the base currency and rates sync at the **user-global** level (user-global projection), with no database migration; older servers don't recognize the base-currency setting ("the conversion setting doesn't sync") — upgrading Cloud to 1.5.0 brings it into alignment.
- **Ledger multi-currency (v3.6.0)**: the transactions table gains currency / conversion columns and **includes a database schema migration** (runs automatically on image startup, with historical backfill); older servers don't recognize these columns, so foreign transactions recorded by the new App lose their conversion on Web / across devices and ledger stats sum raw original amounts — upgrade Cloud to 1.6.0 to align. **Upgrade the server first, then the App.**

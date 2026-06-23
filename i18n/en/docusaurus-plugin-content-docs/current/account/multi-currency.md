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

| Client | Requirement |
|---|---|
| App | ≥ 3.5.0 |
| BeeCount Cloud (self-hosted) | ≥ 1.5.0 (base currency / manual rates / rate proxy are provided by the server; upgrade the server first, then the App) |

The base currency and rates sync at the **user-global** level (user-global projection); this release has no database schema migration. Older servers don't recognize the base-currency setting, which looks like "the conversion setting doesn't sync" — upgrading Cloud to 1.5.0 brings it into alignment.

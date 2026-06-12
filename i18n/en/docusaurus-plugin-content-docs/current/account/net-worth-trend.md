---
sidebar_position: 6
description: "BeeCount net worth over time: view your net worth trend curve and asset composition on the asset page, with 3 / 6 / 12 month and all-time ranges, switching between net worth / total assets / total liabilities."
keywords: [net worth over time, net worth trend, asset trend chart, net worth, BeeCount assets]
---

# Net Worth Over Time

> ✨ **New in v3.5.0**. Self-hosted users require BeeCount Cloud ≥ 1.5.0.

A single net-worth number tells you where you are, but not whether you saved or spent over the last six months. The net worth trend plots **how your net worth changes over time** as a curve, so you can see your financial direction at a glance.

## Where to Find It

Open the asset page; the chart area at the top switches between **Trend** and **Composition** with one tap:

- **Trend**: a curve of net worth over time
- **Composition**: the current share of each account type (the existing composition chart)

Tap the chart to open the **full-screen trend page** for a clearer view.

## Full-Screen Trend Page

The full-screen page offers two toggles you can combine freely:

- **Time range**: last 3 months / 6 months / 12 months / all
- **Metric**: net worth / total assets / total liabilities

You can isolate how liabilities are being paid down, or watch total assets climb.

## Conversion Scope

- Net worth, composition, and the trend curve are all **converted to your [base currency](./multi-currency.md)** — multi-currency accounts are converted via your maintained rates before being summed
- With a single currency, that currency is used directly — no setup needed
- Accounts in a currency missing a rate are excluded from conversion (same as in [multi-currency](./multi-currency.md))

## Shared Ledger Handling

- **Shared ledgers you joined as a member are always excluded**: the net worth trend only counts assets in your own ledgers, not assets in ledgers you joined as an Editor — avoiding double counting and mixed scopes
- Ledgers you own are counted normally

## Notes

- The trend is drawn from asset snapshots by accounting period / calendar day; historical points are computed by accumulating transactions over time
- Transactions made today are **counted in today's** net worth point (they are not cut off by the time boundary)
- After changing the base currency or any currency's rate, the entire trend curve is re-converted at the new rate

## Version Requirements

| Client | Requirement |
|---|---|
| App | ≥ 3.5.0 |
| BeeCount Cloud (self-hosted) | ≥ 1.5.0 (provides the net-worth-history read endpoint; upgrade the server first, then the App) |

The server's net-worth-history is a **read-only endpoint**, and this release has no database schema migration. Older servers lack the endpoint, so the App falls back to local computation or hides the remote trend — upgrading Cloud to 1.5.0 resolves it.

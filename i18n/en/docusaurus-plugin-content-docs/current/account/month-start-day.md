---
sidebar_position: 3
description: "BeeCount \"Month Start Day\": define when \"this month\" begins (1-28) per ledger — align to payday or statement day, with statistics, budgets, widgets and more all following your accounting cycle. Syncs across devices."
keywords: [month start day, payday budgeting, custom billing cycle, accounting period, BeeCount]
---

# Month Start Day

> ✨ **New in v3.4.0**. Self-hosted users require BeeCount Cloud ≥ 1.4.0.

Your salary arrives on the 10th, your credit card bills on the 15th — yet every finance app's "this month" stubbornly starts on the 1st. **Month Start Day** lets each ledger define its own accounting period start.

## Where to Set It

**App:**

1. Go to **Ledger Management** (tap the ledger name at the top of the **Home** tab)
2. **Long-press** the target ledger → **Edit Ledger**
3. Tap **Month start day**, choose a day from 1 to 28, and save

**Web** (self-hosted BeeCount Cloud): ledger card → **Edit** → **Month start day** dropdown → Save.

Changes sync to all devices automatically.

## What It Affects

Once set, the following all use your accounting cycle (e.g. the 10th to the 9th of the next month):

- Home "this month" income / expense / balance and transaction anchoring
- Statistics page — monthly view and yearly view
- Budget cycle (see [Budget Management](./budget.md))
- Annual reports and share posters
- Home screen widgets and the AI assistant's "this month" scope
- Web overview, budget progress, per-month CSV export, and category trends

## Period Naming Rules

- **Period named by its start month**: with start day 10, "June" means June 10 – July 9. The web overview shows the actual date range next to the "this month" label.
- **Year = 12 accounting periods**: from the start of the January period to the start of the next year's January period, ensuring 12 monthly totals add up to the annual total.
- **Calendar page stays calendar-month**: the calendar grid is always Gregorian — it does not shift with the start day (by design).
- **Start day 1 = natural month**: identical behavior to previous versions.

## Multiple Ledgers & Shared Ledgers

- **Per-ledger setting**: set a personal ledger to your payday and a credit-card ledger to its statement day — they are completely independent.
- **Shared ledgers**: all members share the same start day; only the **Owner** can change it.

## Version Requirements & Compatibility

| Client | Requirement |
|---|---|
| App | ≥ 3.4.0 |
| BeeCount Cloud (self-hosted) | ≥ 1.4.0 — older servers ignore the setting, which looks like "the setting doesn't sync". Upgrade the server first. |

Older App versions that receive the setting simply ignore it and continue using the natural month. The underlying transaction data is identical; only the aggregation boundaries differ — upgrading the app brings them into alignment.

## FAQ

**Why does the calendar page still start on the 1st?**

The calendar grid is inherently Gregorian; rearranging it by start day would make it harder to read. The calendar page intentionally keeps the natural month — use the home page or statistics page for period-accurate figures.

**Does changing the start day affect historical data?**

No. Only the aggregation boundaries change; all transaction records remain untouched. You can switch back to 1 (natural month) at any time.

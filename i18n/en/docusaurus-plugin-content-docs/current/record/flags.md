---
sidebar_position: 7
description: "BeeCount transaction flags: two independent toggles per transaction — exclude from income/expense and exclude from budget. Keep your stats clean for reimbursements and one-off costs, without affecting account balance or net worth."
keywords: [transaction flags, exclude from stats, exclude from budget, reimbursement, BeeCount flags]
---

# Transaction Flags

> ✨ **New in v3.5.1**. In cloud mode, server-side filtering of income/expense and budget by flag is provided by BeeCount Cloud ≥ 1.5.1. (Local mode and single-device stats are always correct and do not depend on the server.)

Some entries you have to record (the account balance has to be right), but they shouldn't count toward "how much did I spend this month" or "how much budget is left" — for example, a payment you fronted for a friend, or a sudden one-off cost. Transaction flags let you tag a single transaction to **pull it out of your stats or budget while still keeping the record**.

Each transaction has two **fully independent** toggles that can be combined freely:

## Exclude from Income/Expense

When enabled, this transaction is **left out of income/expense statistics** — the income/expense charts, monthly/yearly summaries, and the per-account income/expense numbers all exclude it.

But it **still counts toward account balance, net worth, and asset trends**, and it **still appears in the transaction list** (with a small badge).

**Typical case: fronting money for a friend.** Flag both "the expense you fronted" and "the income when they pay you back" as Exclude from Income/Expense, so your stats aren't inflated by the in-and-out — while the account balance naturally nets out anyway.

## Exclude from Budget

When enabled, this transaction **does not consume budget** — the budget's used/remaining amounts don't count it.

**Typical case: an unexpected one-off cost.** A sudden extra spend that you don't want to throw off your existing budget plan — just flag it as Exclude from Budget, and budget progress keeps reflecting your everyday spending.

## The Two Are Independent

The two toggles don't affect each other and can be combined in any way:

| Combination | Effect |
|------|------|
| Only Exclude from Income/Expense | Out of stats, but still counts toward budget |
| Only Exclude from Budget | Out of budget, but still counts in stats |
| Both on | Out of both stats and budget |
| Both off | A normal transaction |

## Key: Balance and Net Worth Are Unaffected

This is the most important thing to understand about flags: **no matter how you flag a transaction, account balance, net worth, and asset trends are unaffected.** Flags only change whether it counts toward income/expense stats or budget — the money never disappears. That's why the account balance is always correct in the reimbursement case.

## Where to Set It

On the entry panel, there is a **small flag icon right after the attachment icon**. Tap it to open a dialog where you toggle these two switches.

The toggles are shown based on transaction type:

- **Exclude from Income/Expense**: visible for both income and expense
- **Exclude from Budget**: visible for expense only
- **Transfer**: the flag entry is not shown

## Badge in the Transaction List

Flagged transactions show a **small badge** in the transaction list, so you can tell at a glance which entries are excluded from stats or budget.

## For Self-Hosted Users

- **Local mode / single-device stats**: always filtered correctly by flag, independent of the server.
- **Cloud mode**: the server's income/expense and budget summaries filter by flag, which requires BeeCount Cloud ≥ 1.5.1. Upgrade order is **server first, then App** — see [BeeCount Cloud upgrade notes](../cloud-sync/beecount-cloud.md).

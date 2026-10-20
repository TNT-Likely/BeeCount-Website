---
sidebar_position: 1
---

# Account Management

BeeCount supports multiple accounts, each with independent balance tracking.

## Account Types

- **Cash** - Physical cash on hand
- **Savings** - Bank savings accounts
- **Credit Card** - Credit card accounts with credit limit management and payment reminders
- **Alipay** - Alipay account
- **WeChat** - WeChat Pay wallet
- **Other** - Other account types

## Create an Account

1. Tap "Assets" in the bottom navigation
2. Tap "+" to add an account
3. Select account type
4. Enter name and initial balance
5. Optionally add bank name, last four digits, and notes

## Account Balance

The system automatically updates balances based on transactions:

- **Expense** → Balance decreases
- **Income** → Balance increases
- **Transfer** → Source decreases, destination increases

### Reconcile an Account Balance

When you edit and save a daily account's current balance, you can choose to update the balance directly or create a regular income/expense transaction for the difference under the **Reconciliation** category. Cloud net-worth history requires **BeeCount Cloud 1.6.7**; upgrade Cloud before the app.

## Asset Management

The asset management page shows a net worth overview of all accounts:

- **Multi-currency support** - Net worth grouped by currency
- **Asset composition chart** - Visual breakdown of account types
- **Total assets / liabilities** - Clear financial overview at a glance

> ✨ **Since v3.5.0**: once a [base currency](./multi-currency.md) is set, the asset page can convert multi-currency accounts into a **single base-currency summary**; the chart at the top switches between [net worth over time](./net-worth-trend.md) and asset composition with one tap.

## Credit Card Features

Credit card accounts support additional features:

- **Credit limit** - Set credit limit, view used and available balance
- **Billing / payment due day** - Set monthly billing and payment due dates
- **Payment countdown** - Shows days until payment due, with color-coded urgency alerts
- **Quick repayment** - One-tap to record a repayment (transfer to credit card)

### Current Debt and Overpayments

Starting with **App 3.9.0**, choose Current Debt or Overpayment when editing a credit card, and enter a positive amount:

- **Current debt**: the amount still owed to the bank. Enter 0 when nothing is owed.
- **Overpayment**: money left on the card after paying more than the debt. For example, select Overpayment and enter 200 for an extra payment of 200.
- **Credit limit**: the bank's spending limit, which is not included in your total assets.

Record purchases as credit-card expenses and repayments as transfers from the paying account to the card. The purchase already counts as an expense, so repayment does not count it again. Repayments reduce debt; any excess becomes an overpayment.

For self-hosted sync, upgrade to **Cloud 1.8.0** before **App 3.9.0** for matching Web balance, currency and repayment displays.

## Account Details

Tap an account to view:

- Balance, income, and expense statistics
- Category expense/income pie chart
- Transaction history (paginated)

Starting with **App 3.9.0**, filter account entries by all transactions, expenses and transfers out, or income and transfers in. The all-transactions view shows purchases and repayments together for reconciliation. Filters do not change the account balance. **Cloud 1.8.0** updates the corresponding Web display: individual accounts keep their own currency, while totals are converted to the base currency.

## Account Sorting

Accounts are grouped by type (cash, savings, credit card, etc.). Within each group, you can long-press and drag to reorder accounts to your preferred order.

## Default Account

Set default accounts for income and expenses. They'll be auto-selected when recording for improved efficiency.

## Hide Accounts

Accounts you no longer use (a replaced bank card, a closed wallet, a car you sold…) can be **hidden** instead of deleted:

- **Once hidden**, an account no longer appears in the account pickers when recording, transferring, or setting up recurring transactions, and the account management page moves it into a "Hidden" section at the bottom;
- but its **history and balance stay fully intact and still count toward net worth / asset composition / the net-worth trend** — hiding only removes it from the pickers, it doesn't change where your money is;
- you can **restore** it to active status anytime.

Tap "Hide account" on the account edit page (next to Delete); to bring it back, open the "Hidden" section at the bottom of the account management page and tap "Restore".

> **Why hide instead of delete?** Deleting wipes the account and leaves its past transactions without an owner; hiding keeps all the data and is reversible. Use delete only when you want an account gone from your assets entirely.
>
> In cloud mode the hidden state syncs across devices; **web visibility, and keeping the hidden state through a full sync after reinstalling the app**, require the server upgraded to **BeeCount Cloud 1.6.1** or later (local and two-device incremental sync are unaffected).

## Web Account Management

Sign in to [BeeCount Cloud](../cloud-sync/beecount-cloud.md) on the web → top nav **Assets**:

- **Create / edit / delete** — same as mobile, propagates to mobile via cloud within seconds
- **Click an account card** — opens a dialog with all transactions tied to that account, great for quickly skimming history
- **Auto-create on import** — when [importing ledger data](../record/import-export.md), unknown account names are bulk-created, mirroring mobile import
- **Asset composition donut on home** — desktop visualization is clearer

Deep credit-card configuration (limit / statement day / due day) and default-account picks remain on mobile; the web shows them read-only.

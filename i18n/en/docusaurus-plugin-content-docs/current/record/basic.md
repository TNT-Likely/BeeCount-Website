---
sidebar_position: 1
description: "BeeCount basic recording guide: log expenses, income and transfers with a minimal interface designed for daily use."
keywords: [BeeCount tutorial, expense recording, income tracking, transfer logging, daily budgeting]
---

# Basic Recording

BeeCount supports three transaction types: Expense, Income, and Transfer.

## Quick Recording

Tap the **"+" button** at the bottom center to open the recording page.

![Recording Page](/img/preview/v4/en/light/05-transaction.png)

### Steps

1. **Select Type** - Expense / Income / Transfer
2. **Enter Amount** - Use the number pad
3. **Select Category** - Tap an icon; expand a parent category and select a leaf when subcategories exist
4. **Select Account** - Choose the associated account
5. **Save** - Tap Save below the number pad

> **App 4.0** keeps the number pad at the bottom and uses the remaining space for categories. Subcategories use four columns, with longer names taking two cells. Arithmetic keys let you calculate a split or combined amount directly.

### Record Another Entry

For a new expense or income, tap **Save & add another** to save and continue with the next entry. Tap **Save** to return to the transaction list.

### Optional Information

- **Note** - Type and edit the description directly in the form
- **Tags** - Add one or more tags
- **Date & Time** - Change the recording time (for backdating)
- **Image** - Add a receipt or proof

## Copy Transactions

Since **App 3.8.6**, you can copy a transaction from the home page list:

1. Long-press an expense, income or transfer and choose **Copy**.
2. Amount, category, accounts, notes, tags, currency and statistics/budget flags are prefilled. The date and time default to now and can be changed.
3. Adjust the fields and tap **Done** to save an independent new transaction.

The original transaction stays unchanged. Cancelling creates no record. Images from the original entry are not copied; add receipts for the new transaction separately.

## Transaction Receipt Images

Starting with **App 3.9.0**, turn an expense, income or transfer into a receipt image:

1. Long-press a transaction on the home page and choose Generate Receipt.
2. Choose whether to include notes, tags, accounts and the ledger. Accounts and the ledger are hidden by default.
3. Save the image to your photo library or use the system share menu.

Generating an image does not create or change a transaction. Keep original supporting images as [transaction attachments](./attachment.md).

## Edit & Delete

- **Tap** a transaction to edit it
- **Swipe left** on a transaction to delete it

## Transfer Records

Transfers move funds between different accounts:

- Select "Transfer" type
- Choose source and destination accounts
- Enter transfer amount

App 4.0 places account selection and amount entry on the same page. New transfers require two accounts with the same currency. For foreign-currency accounts, review the amount converted to the current ledger's base currency and supply a missing exchange rate before saving.

The system automatically updates both account balances.

## Web Recording

After logging in to [BeeCount Cloud](../cloud-sync/beecount-cloud.md) on the web, desktop entry is faster:

- **+ New transaction button** — top-right of the transactions page opens a dialog
- **⌘K / Ctrl+K command palette** — works on any page; type amount or note, pick "New transaction"
- **Bulk operations** — list view supports multi-select delete / export CSV (see [Transactions](../features/record.md))
- **Desktop keyboard flow** — number pad, Tab to switch fields, Enter to save

Transactions created on web sync to mobile within seconds via cloud, and vice versa.

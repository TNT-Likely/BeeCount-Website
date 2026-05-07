---
sidebar_position: 1
---

# Recording Transactions

BeeCount supports three transaction types: Expense, Income, and Transfer.

## Expense Records

Record daily spending, which deducts from the selected account balance.

## Income Records

Record salary, bonuses, and other income, which adds to the selected account balance.

## Transfer Records

Move funds between different accounts, such as withdrawing cash from a bank card.

- Source account balance decreases
- Destination account balance increases

## Transaction Details

Each transaction can include:

- **Amount** - Required, the transaction amount
- **Category** - Required, the expense/income category
- **Account** - Required, the associated account
- **Date & Time** - Defaults to current time, can be modified
- **Note** - Optional, transaction description
- **Tags** - Optional, multiple tags
- **Image** - Optional, receipt or proof

## Web Transaction Management

Sign in to [BeeCount Cloud](../cloud-sync/beecount-cloud.md) on the web → top nav **Transactions**:

### List and filter

- **Top search bar** — full-text search + filter dialog (type / account / category / tag / date range / amount range)
- **Desktop table view** — denser than mobile, attachments and tags display as inline chips
- **Pagination** — defaults to 50/page, configurable

### Bulk operations (desktop-only)

Click the **Bulk select** icon on the top-right to enter selection mode:

- **Row checkbox** — toggle one or all of the current page
- **⇧ + Click** for range select (Gmail-style); **⌘ + Click** for incremental select
- **Bulk delete** — confirmation dialog with count and total amount, atomic rollback
- **Bulk export CSV** — download selected rows, max 200 per call
- **Esc** exits selection mode

### Global shortcuts

- **⌘K / Ctrl+K** opens the command palette anywhere — search / jump / new / export / import / AI bill
- **⌘V to paste image or text** in the palette switches the default action to "AI bill"; see [AI image](../ai/image.md#web-image-recording) / [AI text](../ai/chat.md#web-text-recording)

### Export CSV

The top-right **"Export CSV"** button on the transactions list — exports all rows matching the current filter; format is identical to mobile / mobile-import (11 columns, localized headers, UTF-8 BOM, streaming download stays memory-stable for huge files).

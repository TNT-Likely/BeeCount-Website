---
sidebar_position: 2
---

# Recurring Entries

Automatically record fixed income and expenses - ideal for salary, rent, subscriptions, and other periodic transactions.

## Create a Recurring Entry

1. Go to "Me" → "Automation" → "Recurring Bills"
2. Tap "+" to create
3. Fill in transaction details
4. Set frequency and execution time

## Frequency Types

| Type | Description | Example |
|------|-------------|---------|
| Daily | Executes every day | Daily commute |
| Weekly | Fixed day each week | Weekend entertainment |
| Monthly | Fixed date each month | Salary, rent |
| Yearly | Fixed date each year | Annual membership |

## Currency (v3.7.2)

You can **pick a currency** when creating a recurring bill, instead of being limited to the ledger's base currency:

- With an account selected, its currency wins; with no account, the currency you picked on the template is used
- Changing the currency re-filters the account candidates, so any already-selected account is cleared and must be picked again
- Every generated entry **converts at the rate in effect that day** — "$10 a month" is never frozen into one fixed local amount
- Foreign-currency templates show their ISO code in front of the amount in the list

Existing recurring bills have no currency set, which means the ledger's base currency — their behavior is unchanged. See [Multi-currency](../account/multi-currency.md).

## Common Use Cases

- **Salary** - Monthly income on a fixed date
- **Rent/Mortgage** - Fixed monthly expense
- **Subscriptions** - Video/music streaming services
- **Phone Bill** - Monthly recurring charges
- **Insurance** - Annual premiums

## Managing Recurring Entries

- **Pause** - Temporarily stop execution
- **Resume** - Re-enable
- **Delete** - Remove completely
- **Set Duration** - Specify start and end dates

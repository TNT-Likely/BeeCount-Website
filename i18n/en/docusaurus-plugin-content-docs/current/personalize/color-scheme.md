---
sidebar_position: 3
---

# Income/Expense Color Scheme

Customize income and expense display colors to adapt to different regional reading habits.

## Why Switch Color Schemes?

Different regions have different color associations:

- **Red for Income · Green for Expense** - Traditional Chinese preference, red represents celebration and gain
- **Red for Expense · Green for Income** - International standard, red represents warning and outflow

## Change Color Scheme

1. Go to "Mine" → "Appearance Settings" → "Personalization"
2. Tap "Income/Expense Color Scheme"
3. Select your preferred scheme

## Color Scheme Options

### Red for Income · Green for Expense (Default)

- ✅ Income displays in red
- ✅ Expense displays in green
- Suitable for users familiar with Chinese traditions

### Red for Expense · Green for Income

- ✅ Expense displays in red
- ✅ Income displays in green
- Suitable for users familiar with international standards

## Application Scope

Color scheme applies to:

- Home page income/expense statistics
- Transaction list amounts
- Account balance display
- Statistics charts
- Calendar view
- Category details
- Tag details

## Instant Effect

Takes effect immediately after selection, no app restart needed. All page income/expense colors update automatically.

## Works with Theme Color

Income/expense color scheme is independent from theme color:

- Theme color affects navigation bar, buttons and other UI elements
- Income/expense colors specifically affect amount displays
- Both can be freely combined to create a personalized interface

## Web Profile (color / avatar / display name)

Sign in to [BeeCount Cloud](../cloud-sync/beecount-cloud.md) on the web → avatar menu → **Profile**:

- **Avatar** — click your avatar → pick an image (≤4 MB); syncs to mobile via cloud
- **Display name** — click the name to inline-edit; Enter to save, Esc to cancel
- **Income/expense color** — click the chip in "Synced preferences" to toggle; real-time bidirectional sync with mobile
- **Dark-mode header pattern** — Select with 4 options (None / Icons / Particles / Honeycomb)
- **Balance display** — Select (Full amount / Compact)
- **Show transaction time** — iOS-style Switch

Any-side change pushes via the `profile_change` WS event to the other side in real time.

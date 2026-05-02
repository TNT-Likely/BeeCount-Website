---
sidebar_position: 1
description: "Configure BeeCount app lock with PIN and biometric authentication (Face ID, fingerprint) to keep your financial data private."
keywords: [expense tracker app lock, PIN code budgeting, biometric finance app, BeeCount privacy]
---

# App Lock

BeeCount supports app lock to protect your financial privacy with PIN and biometric authentication.

## Features

- **PIN Lock** - Set a 4-digit PIN code required each time you open the app
- **Biometric Authentication** - Support for fingerprint and Face ID for quick unlock
- **Multitask Blur** - Automatically blurs screen content when switching to the app switcher, preventing others from seeing your data

## Enable App Lock

1. Go to "Me" → "Data Management"
2. Enable "App Lock"
3. Set a 4-digit PIN code
4. Optionally enable biometric authentication (fingerprint/Face ID)

## Lock Timing

- **App Launch** - Authentication required each time the app opens
- **Return from Background** - Authentication required when returning from other apps
- **Timeout Settings** - Configurable timeout (immediately, 1 minute, 5 minutes, 15 minutes)

## Privacy Blur Screen

When app lock is enabled, switching to the multitask view (swiping up to see recent apps) will:

- Automatically blur all app content
- Prevent others from seeing your financial data in the app switcher
- Blur disappears automatically when you return to the app

:::tip
The privacy blur screen only works when app lock is enabled. If you want multitask privacy protection, you need to enable app lock first.
:::

## Forgot PIN

If you forget your PIN code, you can reset it by:

1. Uninstalling and reinstalling the app
2. Setting up app lock again

:::warning Note
Make sure your data is backed up via cloud sync before resetting, or local data may be lost.
:::

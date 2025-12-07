---
sidebar_position: 3
---

# iOS Auto Recording

Use iOS Shortcuts to automatically record transactions after payments.

## How It Works

1. Set up a Shortcut to listen for payment notifications
2. Triggers automatically after successful payment
3. Recognizes amount and merchant information
4. Calls BeeCount to complete the record

## Configuration Steps

### 1. Download the Shortcut

1. Open the "Shortcuts" app
2. Import the BeeCount shortcut
3. Allow running untrusted shortcuts

### 2. Set Up Automation

1. Open "Shortcuts" → "Automation"
2. Tap "+" in the top right
3. Select "Create Personal Automation"
4. Choose trigger condition:
   - Receive Message - Listen for bank SMS
   - Receive Notification - Listen for payment app notifications

### 3. Configure Trigger Conditions

Using WeChat Pay as an example:

1. Select "App" → "WeChat"
2. Select "Receive Notification"
3. Optionally set keyword filters

### 4. Add Action

1. Add "Run Shortcut" action
2. Select "BeeCount" shortcut
3. Turn off "Ask Before Running"

## Supported Triggers

- Bank SMS - Listen for spending SMS, extract amounts
- WeChat Notifications - Listen for WeChat Pay success notifications
- Alipay Notifications - Listen for Alipay payment notifications
- NFC Tags - Auto-record after card tap

## Shortcut Parameters

The shortcut supports these input parameters:

- amount - Amount
- category - Category name
- note - Note
- account - Account name

## Manual Trigger

You can also trigger the shortcut manually:

1. Say "BeeCount" to Siri
2. Tap from Shortcuts Widget
3. Share text via the share menu

## FAQ

**Automation not triggering?**

Check:
1. Is "Ask Before Running" turned off? (needs to be off)
2. Are notification permissions working?
3. Does the shortcut have syntax errors?

**Amount recognition incorrect?**

Automation relies on regex to extract amounts. If the format is unusual, recognition may fail. You can adjust the regex rules in the shortcut.

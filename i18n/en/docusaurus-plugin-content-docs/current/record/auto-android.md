---
sidebar_position: 4
---

# Android Auto Recording

Android supports multiple auto-recording methods: screenshot recognition, share recording, and notification listening.

## Method 1: Screenshot Recording

Take a screenshot after payment, and BeeCount automatically recognizes it.

### How to Use

1. Take a screenshot after completing payment
2. BeeCount detects the new screenshot
3. Automatically recognizes amount and merchant info
4. Confirmation dialog appears
5. Confirm to complete the record

### Enable Screenshot Listening

1. Open BeeCount
2. Go to "Me" → "Auto Recording"
3. Enable "Screenshot Auto Recognition"
4. Grant storage permission

### Supported Screenshot Types

- WeChat Pay success page
- Alipay payment success page
- Bank app transaction details
- Other payment receipt screenshots

## Method 2: Share Recording

Share payment information to BeeCount.

### How to Use

1. Find the transaction record in the payment app
2. Tap the "Share" button
3. Select "BeeCount"
4. Information is auto-recognized and filled in
5. Confirm to complete the record

### Supported Share Content

- Text (spending descriptions containing amounts)
- Images (payment screenshots)
- Links (transaction detail pages)

## Method 3: Notification Listening

Listen for payment notifications and auto-record.

### Configuration Steps

1. Go to "Me" → "Auto Recording"
2. Enable "Notification Listening"
3. Grant notification access permission
4. Select apps to listen to (WeChat, Alipay, etc.)

### How It Works

1. Listens for notifications from specified apps
2. Identifies payment success notifications
3. Extracts amount and merchant info
4. Automatically creates a record

### Notes

- Requires "Notification Access" permission
- Some systems may restrict background running
- Recommend adding to battery optimization whitelist

## Recognition Capabilities

BeeCount uses AI to recognize the following:

- Amount: 95%+ accuracy
- Merchant Name: 90%+ accuracy
- Payment Method: 85%+ accuracy
- Expense Category: 80%+ accuracy

## Configuration Tips

### Best Practices

1. Enable screenshot recognition - Most stable and reliable
2. Grant necessary permissions - Storage, notifications
3. Add to whitelist - Prevent system from killing the app
4. Regular checks - Ensure auto-recording is working properly

### Power Saving Settings

If concerned about battery drain:
- Enable only screenshot recognition (passive trigger)
- Disable notification listening (active polling)

## FAQ

**Screenshot recognition not responding?**

1. Check if storage permission is granted
2. Check if screenshot listening is enabled
3. Try restarting the app

**Recognition results inaccurate?**

AI recognition may have errors. You can manually edit and save. Recognition accuracy improves with use.

**Background app being killed?**

1. Add BeeCount to battery optimization whitelist
2. Allow background running
3. Lock the app in recent tasks

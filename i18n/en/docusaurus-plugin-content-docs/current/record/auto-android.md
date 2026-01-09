---
sidebar_position: 4
---

# Android Auto Recording

Android supports multiple auto-recording methods: screenshot recognition and share recording.

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
2. Go to "Me" > "Auto Recording"
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

## Recognition Capabilities

BeeCount uses AI to recognize:

- Amount
- Merchant name
- Expense category
- Notes

## Configuration Tips

### Best Practices

1. Enable screenshot recognition - Most stable and reliable
2. Grant necessary permissions - Storage permission
3. Add to whitelist - Prevent system from killing the app

### Power Saving

Screenshot recognition is passively triggered, only works when taking screenshots, no extra battery drain.

## FAQ

**Screenshot recognition not responding?**

1. Check if storage permission is granted
2. Check if screenshot listening is enabled
3. Try restarting the app

**Recognition results inaccurate?**

AI recognition may have errors. You can manually edit and save.

**Background app being killed?**

1. Add BeeCount to battery optimization whitelist
2. Allow background running
3. Lock the app in recent tasks

## Why Not Use Accessibility Service?

Some accounting apps use Accessibility Service for automatic recording, but BeeCount chose the screenshot recognition approach for the following reasons:

### 1. Compliance Issues

Accessibility Service is designed for users with visual impairments, intended for screen reading and accessibility scenarios. Using it for automatic accounting is feature abuse and may violate app store policies.

### 2. Privacy and Security

Accessibility Service requires continuous screen monitoring and can read all app interface information, including:
- Chat messages
- Personal information
- Password inputs
- Other sensitive data

This poses serious privacy and security risks.

### 3. High Development and Maintenance Costs

- **Large adaptation workload** - Need to adapt to each app's interface structure individually
- **Low ROI** - Apps like Alipay and WeChat frequently update their interfaces, requiring continuous maintenance
- **Poor compatibility** - Some apps use image-rendered interfaces that Accessibility Service cannot read
- **System differences** - Inconsistent compatibility across different Android versions and manufacturer ROMs

### BeeCount's Approach Advantages

In comparison, the screenshot recognition approach offers:

- ✅ **Privacy-friendly** - Only processes when user actively takes screenshots, no screen monitoring
- ✅ **Compliant and secure** - Doesn't abuse system permissions
- ✅ **Universal** - Supports payment screenshots from any app, no individual adaptation needed
- ✅ **Easy maintenance** - AI-based recognition adapts better to interface changes
- ✅ **User control** - Users know exactly when recognition is triggered

While it requires users to manually take screenshots, this small action provides better privacy protection and a more stable experience.

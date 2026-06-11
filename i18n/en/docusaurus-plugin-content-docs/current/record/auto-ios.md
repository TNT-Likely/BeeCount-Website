---
sidebar_position: 3
description: "iOS auto-recording guide: combine Shortcuts and screenshot OCR to record transactions automatically after payments — no manual entry."
keywords: [iOS auto recording, iPhone expense tracker, Shortcuts budgeting, screenshot OCR finance]
---

# iOS Auto Recording

Use iOS Shortcuts + screenshot recognition to quickly record after payments.

## Video Tutorial

<video width="100%" controls>
  <source src="/img/ios-auto-record-tutorial.mp4" type="video/mp4" />
  Your browser does not support video playback
</video>

## How It Works

1. Create a Shortcut: Screenshot → BeeCount recognition
2. Bind to "Back Tap" gesture
3. Double-tap the back of your phone after payment
4. **The app runs silently in the background**: screenshot → AI recognition → result delivered via a system notification — **the app is no longer pulled to the foreground** (since 3.2.3). You get two notifications: an "in progress" and a "final result" with the specific failure reason on errors.

The whole flow doesn't interrupt the payment page / current app — you can keep scrolling WeChat / Alipay. Tap the notification to jump back into BeeCount and review the just-recorded transaction.

## Configuration Steps

### Option 1: In-App Guide (Recommended)

1. Open BeeCount, go to "Me" → "Smart Billing" → "Shortcuts"
2. Follow the guided steps on the page
3. Tap "Add Shortcut" to auto-create
4. Follow the prompts to bind to Back Tap

### Option 2: Manual Setup

#### 1. Create Shortcut

1. Open the "Shortcuts" app, tap "+" in the top right to create a new shortcut
2. Add "Take Screenshot" action
3. Search and add "BeeCount - Screenshot Auto Recording" action
4. Set the BeeCount screenshot parameter to the previous step's "Screenshot"
5. Save the shortcut

#### 2. Bind to Back Tap (Recommended)

1. Go to "Settings" > "Accessibility" > "Touch" > "Back Tap"
2. Select "Double Tap" or "Triple Tap"
3. Select the shortcut you just created
4. Done! Double-tap the back of your phone after payment to quickly record

> ✅ Recommended: After binding the shortcut to "Back Tap", double-tap the back of your phone after payment to auto-screenshot and recognize for recording, no manual screenshot needed.

## How to Use

1. After completing payment, stay on the payment success page
2. Double-tap the back of your phone (or manually run the shortcut)
3. The system takes the screenshot + runs AI recognition in the background, then surfaces a notification with the result
4. (Optional) tap the notification to jump back to BeeCount and review / adjust

> ✨ **Improved in v3.2.3**: the whole flow runs silently in the background — the app is no longer pulled to the foreground. Notifications are split into "in progress" / "final result", and failures show the specific reason (network / API quota / AI not configured, etc.) instead of always saying "AI not configured".

> ✨ **Since v2.3.3**: screenshots are automatically saved as transaction attachments, and a "Shortcut Screenshot" tag is added for easy filtering later.

## Other Trigger Methods

Besides Back Tap, you can also trigger via:

- Say the shortcut name to Siri
- Tap from Shortcuts Widget
- Add to home screen as an icon

## FAQ

**Back Tap not responding?**

1. Confirm your iPhone model supports it (iPhone 8 and later)
2. Check if the shortcut is correctly bound
3. Try adjusting tap force and position

**Recognition not accurate?**

1. Ensure screenshot includes the complete payment amount
2. Stay on payment success page long enough
3. Can manually adjust in BeeCount

**Screenshot fires on iOS 27 but nothing gets recorded?**

iOS 27 tightened notification permissions: calls from unauthorized apps now fail outright (previously they failed silently).

- **App ≥ 3.4.0**: handled — bookkeeping completes even without notification permission; you just won't see progress notifications. Enable notifications in Settings for the full experience.
- **App ≤ 3.2.5**: the whole flow gets interrupted in this scenario — upgrade the App or grant notification permission.

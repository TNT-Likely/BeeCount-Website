---
sidebar_position: 3
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
4. Auto-screenshot and recognize amount, complete recording

## Configuration Steps

### Option 1: In-App Guide (Recommended)

1. Open BeeCount, go to "Discover" → "Shortcuts"
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
3. Auto-screenshots and recognizes amount, merchant info
4. Confirm to complete recording

> ✨ **New in v2.3.3**: Screenshots are automatically saved as transaction attachments, and a "Shortcut Screenshot" tag is added for easy filtering later.

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

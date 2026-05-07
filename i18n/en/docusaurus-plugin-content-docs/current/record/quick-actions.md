---
sidebar_position: 6
---

# Quick Actions

Long-press the BeeCount app icon to quickly launch common features without opening the app first.

## Supported Platforms

- iOS (iPhone 6s and later, requires iOS 13+)
- Android (Android 7.1 and later)

## Quick Actions

After long-pressing the app icon, the following quick menu appears:

| Action | Description |
|--------|-------------|
| Image Recording | Select image from gallery, AI auto-recognizes bills |
| Camera Recording | Open camera to take photo, AI auto-recognizes bills |
| Voice Recording | Voice input, AI auto-parses for recording |
| AI Assistant | Open AI chat, smart financial assistant |

## How to Use

### iOS

1. Find the BeeCount icon on the home screen
2. Long-press the icon for about 1 second
3. When the quick menu pops up, tap the desired action

### Android

1. Find the BeeCount icon on the desktop or in the app drawer
2. Long-press the icon
3. When the quick menu pops up, tap the desired action

> Some Android launchers may not support this feature. Please use the system default launcher or mainstream third-party launchers.

## Use Cases

- **Received a bill SMS**: Long-press icon → Image Recording → Screenshot recognition
- **Offline purchase**: Long-press icon → Camera Recording → Point at receipt
- **Quick record**: Long-press icon → Voice Recording → Say "Lunch 35 yuan"
- **Financial questions**: Long-press icon → AI Assistant → Chat consultation

## Web Quick Entries

After signing in to [BeeCount Cloud](../cloud-sync/beecount-cloud.md) on the web, **⌘K / Ctrl+K** is the desktop equivalent of long-press shortcuts.

### AI Screenshot Recording (paste image)

On any page, press ⌘K → **paste an image directly with ⌘V / Ctrl+V** (Alipay / WeChat payment screenshots, credit-card bill screenshots, bank statement screenshots…) → the default action becomes "AI bill (image)" → Enter → review & edit N transaction drafts → save in bulk.

The server uses a vision LLM (Zhipu GLM-4V Flash etc.) to parse, and the original image is attached to all N transactions.

### AI Text Recording (paste text)

⌘K → paste any text (WeChat bill text, an Excel table block, natural language like "Taxi yesterday 30 + lunch 25") → default action switches to "AI bill (text)" → Enter → review the drafts.

See [AI bill recognition](../ai/image.md) / [AI text recording](../ai/chat.md).

### Other palette shortcuts

- Just type → search transactions (default action)
- Type `?xxx` → ask the AI docs site
- Pick "New transaction" / "Annual report" / "Export this month CSV" / "Export this year CSV" / "Import ledger data"
- Jump to any ledger / page

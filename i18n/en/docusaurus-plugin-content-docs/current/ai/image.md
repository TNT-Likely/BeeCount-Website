---
sidebar_position: 3
---

# Image Recognition

Take or select a photo, and AI automatically recognizes bill information.

![Image Recognition](/img/preview/en/13-ocr-recognition.png)

## How to Use

1. Hold the **Record** button in the bottom bar
2. Slide to **Camera** or **Gallery**
3. Take or select a receipt photo
4. AI recognizes the image and creates the transactions
5. Open the saved transaction to check the amount, category, account and attachment; edit it if needed

## Supported Scenarios

- **Shopping Receipts** - Supermarket, mall receipts
- **Food Delivery Orders** - Uber Eats, DoorDash screenshots
- **Transfer Records** - Payment app transfer screenshots
- **Invoices** - Electronic or paper invoices

## Recognized Content

AI will attempt to identify:

- Amount
- Merchant name
- Transaction time
- Purchase items

## Multiple Transactions per Image

A receipt or statement can contain several transactions. The current mobile flow creates the recognized transactions and displays the save result:

- Check each saved transaction's amount, category, account, tags and note; edit or delete it if needed
- With Auto-add Attachment enabled, the image is attached to each recognized transaction so you can revisit the original receipt
- Enable Keep Original Attachments when you need the original image quality

## Tips

- Use clear, legible images
- Include complete amount information
- Avoid glare or shadows

## Manual Adjustment

AI recognition may not be 100% accurate. Check the saved transactions and edit them if needed.

## Auto Tag

When using image recording, the system automatically adds an "Image Recording" tag to the transaction for easy filtering and statistics.

## Auto-Save Attachment

Enable Auto-add Attachment in Me → Smart Billing to save the selected or captured image as a transaction attachment without adding it manually.

Since **3.8.4**, enable Keep Original Attachments on the same page to preserve attachment dimensions and quality. AI recognition uses a separate compressed copy to avoid uploading oversized images. The switch is off by default, takes effect without restarting, and only affects new attachments. See [Keep Original Attachments](../record/attachment.md#keep-original-attachments).

## Web Image Recording

After signing in to [BeeCount Cloud](../cloud-sync/beecount-cloud.md) on the web, the desktop browser supports **direct image paste**:

1. On any page, press **⌘K / Ctrl+K** to open the command palette
2. Press **⌘V / Ctrl+V** to paste an image (a screenshot in the clipboard, or drag-drop)
3. The default action switches to "AI bill (image)" → Enter
4. A dialog shows N transaction drafts; edit category / account / tags / note per row
5. Click "Save selected" to commit them in one batch

The server uses a vision LLM (Zhipu GLM-4V Flash etc., bind it in [AI Config](./overview.md#web-ai-configuration)) to parse, and **all N transactions share the original image as an attachment**. On failure, the LLM raw output is shown for debugging.

Same as mobile, recognized transactions are auto-tagged with "AI" + "Image".

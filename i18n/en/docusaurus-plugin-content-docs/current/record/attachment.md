---
sidebar_position: 5
---

# Transaction Attachments

Add image attachments to transactions for receipts, invoices, and more.

## Adding Attachments

### When Recording

1. On the recording page, tap the "Attachment" icon at the bottom
2. Choose "Take Photo" or "Choose from Gallery"
3. The image will be automatically added as an attachment
4. After completing the record, attachments are saved with the transaction

### When Editing

1. Open an existing transaction's detail page
2. Tap "Edit"
3. Add images in the attachment area
4. Save changes

## Viewing Attachments

- Transactions with attachments display an attachment icon in the list
- Tap a transaction to view details and see all attachments
- Tap an attachment image to view it full-screen

## Deleting Attachments

1. Enter the transaction edit page
2. Long-press the attachment image you want to delete
3. Confirm deletion

## Auto-Save Attachments

Enable Auto-add Attachment in Me → Smart Billing to automatically save images with these recording methods:

- **Image Recording** - The selected image is auto-saved
- **Camera Recording** - The captured photo is auto-saved

## Keep Original Attachments

Since **3.8.4**, enable Keep Original Attachments in Me → Smart Billing, below Auto-add Attachment. The switch is off by default to keep the existing compression behavior. Changes take effect immediately without restarting the app.

- When enabled, manually added attachments, image recording and camera recording preserve the incoming image's original dimensions and quality. iOS Shortcuts screenshot recording follows the same setting.
- AI recognition uses a separate compressed copy with a longest edge of at most 1920 pixels; the saved original attachment is unaffected.
- Automatic saving still requires Auto-add Attachment to be enabled. Manually added attachments can also keep their originals.
- Original images use more storage and sync bandwidth.

:::tip Existing attachments
The switch only affects new attachments. Previously compressed images cannot recover their original quality automatically; add them again from the original files.
:::

## Attachment Export

Attachments can be exported as a separate archive:

1. Go to Me → Data Management → Export Attachments
2. Preview attachments and custom icons
3. Confirm to export the archive

Since **3.8.4**, thumbnails and enlarged details in import/export previews show the actual file size and width × height, making it easier to check whether an image keeps its original dimensions.

## Notes

- Attachments are stored locally and will take up device storage
- During cloud sync, attachments are also synced (depending on cloud storage plan)
- Consider cleaning up unnecessary attachments periodically

## Web Attachments

After signing in to [BeeCount Cloud](../cloud-sync/beecount-cloud.md) on the web:

- **AI screenshot recording auto-attaches** — when you paste an image via ⌘K and AI recognizes N transactions, **all N transactions share the same original image** as the attachment; see [Image recognition](../ai/image.md#web-image-recording).
- **📎 chip on transaction rows** — rows with attachments show an icon; clicking opens an attachment carousel (prev / next).
- **Detail dialog viewer** — click a transaction row to open the detail dialog where attachments can be enlarged or downloaded.
- **Storage** — web attachments live on the BeeCount Cloud server's `attachment_storage_dir`, deduplicated by sha256 with mobile so the same file is never uploaded twice.

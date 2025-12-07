---
sidebar_position: 100
---

# FAQ

## Data Related

### Q: How do I backup my data?

There are several ways:

1. **Cloud Sync** (Recommended) - Enable iCloud/Supabase/WebDAV/S3 sync
2. **Export CSV** - Export transaction data locally
3. **Export Config** - Export categories, accounts, and other settings

### Q: How do I migrate data to a new phone?

- **iOS → iOS**: Use iCloud sync, sign in with the same Apple ID on the new device
- **Android → Android**: Use Supabase/WebDAV/S3 sync
- **Cross-platform**: Use Supabase/WebDAV/S3 sync, or export CSV and import

### Q: Where is my data stored?

Data is stored locally on your device by default. When cloud sync is enabled, it syncs to your chosen cloud service (iCloud/Supabase/WebDAV/S3). BeeCount does not collect any data.

## Feature Related

### Q: Does it support multiple currencies?

Currently primarily supports CNY (Chinese Yuan). Multi-currency support is planned.

### Q: Can I record investment returns?

You can create an "Investment" category and "Investment Account" to record, but automatic ROI calculation is not yet supported.

### Q: Can multiple people share a ledger?

Real-time multi-user collaboration is not currently supported, but you can share cloud sync configuration for simple data sharing.

## Sync Related

### Q: What if sync isn't working?

1. Check network connection
2. Verify cloud service configuration is correct
3. Try manually triggering sync
4. Check sync logs for issues

### Q: Can I use multiple cloud sync services at once?

Currently only one cloud sync method can be selected at a time.

## Other Questions

### Q: Can't download from China App Store?

China App Store listing requires registration (ICP filing), which is in progress. You can use TestFlight to install in the meantime.

### Q: Is there an Android version?

Yes, you can download the APK from [GitHub Release](https://github.com/TNT-Likely/BeeCount/releases).

### Q: Is it free?

Yes, completely free. No ads, no subscriptions, no hidden fees.

---

Have other questions? Feel free to [submit an Issue](https://github.com/TNT-Likely/BeeCount/issues).

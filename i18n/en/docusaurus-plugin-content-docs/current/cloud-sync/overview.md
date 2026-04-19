---
sidebar_position: 1
---

# Cloud Sync Overview

BeeCount supports multiple cloud sync options for flexible and controllable data storage.

## Why Cloud Sync?

- **Data Backup** — Prevent data loss
- **Device Migration** — Quickly restore on a new device
- **Multi-device collaboration** — Phone / tablet / Web in real time (BeeCount Cloud)
- **Device Switching** — Move between devices

## Supported Sync Methods

| Method | Best for | Difficulty | Realtime |
|--------|---------|------------|----------|
| [**BeeCount Cloud**](./beecount-cloud) 🆕 | Multi-device realtime + Web | ⭐⭐ Easy | ✅ Yes |
| [iCloud](./icloud) | iOS users | ⭐ Easiest | ⚠️ iOS only |
| [Supabase](./supabase) | Free cloud database | ⭐⭐ Easy | ❌ Manual upload/download |
| [WebDAV](./webdav) | NAS / self-hosted | ⭐⭐ Easy | ❌ Manual upload/download |
| [S3](./s3) | Technical users | ⭐⭐⭐ Medium | ❌ Manual upload/download |

## Data Security

- All data is stored in **your own** cloud storage
- BeeCount doesn't collect or store any user data
- You can export and migrate data at any time

## Recommendations

- **Multi-device / family use** → **BeeCount Cloud** self-hosted, phone + Web in seconds
- **iOS-only single user** → **iCloud**, zero config
- **Don't want to run a server** → **Supabase**, generous free tier
- **Have NAS / Jianguoyun** → **WebDAV**
- **Prefer object storage** → **S3** (Cloudflare R2 / AWS S3 / MinIO)

## Two sync models

The cloud options fall into two camps — pick based on what you actually need:

### Realtime sync (BeeCount Cloud)

Edit a row on A → WebSocket push → B sees it within seconds. **No manual action** — feels like chat messages arriving.

### Snapshot sync (iCloud / Supabase / WebDAV / S3)

Upload your local data as a **full snapshot** overwriting the cloud copy; new device downloads the **full snapshot** overwriting local. Good for "single user, mostly one device, occasional device swap".

:::tip Multi-device with snapshot sync

Snapshot sync **does not** support simultaneous editing on two devices — the later upload overwrites the earlier one. Steps:

1. **On the original device**: make sure data is uploaded to cloud
2. **On the new device**: clear local ledgers → download from cloud
3. **Avoid** editing on two devices at once, to prevent conflicts

If you need realtime multi-device sync, switch to **BeeCount Cloud**.

:::

## Diff preview (snapshot sync)

iCloud / Supabase / WebDAV / S3 support a **diff preview** before upload/download:

- Shows added, modified, and deleted transactions row by row
- Selectively sync specific changes
- A guide popup appears on first use

## Multi-device toggle (snapshot sync)

If you only use one device, turn off the "Multi-device sync" toggle:

- **Me** → **Cloud Services** → disable "Multi-device sync"
- Once off, entering the sync page no longer hits the cloud automatically — less lag, less data
- Trigger manually when you need it

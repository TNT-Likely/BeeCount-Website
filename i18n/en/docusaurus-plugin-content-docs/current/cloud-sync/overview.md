---
sidebar_position: 1
---

# Cloud Sync Overview

BeeCount supports multiple cloud sync options for flexible and controllable data storage.

## Why Cloud Sync?

- **Data Backup** - Prevent data loss
- **Device Migration** - Quickly restore data on new devices
- **Device Switching** - Switch between different devices (requires correct procedure)

## Supported Sync Methods

| Method | Best For | Difficulty |
|--------|----------|------------|
| [iCloud](./icloud) | iOS users | ⭐ Easiest |
| [Supabase](./supabase) | Free cloud database | ⭐⭐ Easy |
| [WebDAV](./webdav) | NAS/Self-hosted users | ⭐⭐ Easy |
| [S3](./s3) | Technical users | ⭐⭐⭐ Medium |

## Data Security

- All data is stored in **your own** cloud storage
- BeeCount doesn't collect or store any user data
- You can export and migrate data at any time

## Recommendations

- **iOS Users**: iCloud is recommended - zero configuration
- **Android Users**: Supabase or WebDAV recommended
- **Technical Users**: Self-host S3 or WebDAV

## Multi-Device Usage Guide

:::warning Important Notice

Multi-device collaborative editing is currently not supported. To switch between multiple devices, follow these steps:

:::

### Correct Device Switching Steps

If you want to switch from Device A to Device B:

1. **On Device A**
   - Ensure data has synced to cloud
   - Check last sync time in cloud sync settings

2. **On Device B**
   - Delete all local ledgers (or clear app data)
   - Configure the same cloud sync service
   - Download data from cloud

3. **Important Notes**
   - ⚠️ Confirm Device A data is uploaded before switching
   - ⚠️ Device B must clear local data before downloading
   - ⚠️ Do not edit data on two devices simultaneously

### Why Not Support Multi-Device Collaboration?

The current cloud sync solution is based on file synchronization and does not support real-time conflict resolution. Simultaneous editing on multiple devices may cause data conflicts or loss.

### Multi-Device Sync Toggle

If you only use one device, you can disable the "Multi-device Sync" toggle:

- Go to "Me" → "Cloud Services" → Turn off "Multi-device Sync"
- When disabled, entering the cloud sync page won't automatically check the cloud, reducing lag and data usage
- You can still trigger sync manually when needed

### Diff Preview

Cloud sync supports diff preview, allowing you to review specific changes between local and cloud data before syncing:

- Shows added, modified, and deleted transactions one by one
- Selectively sync specific changes
- A quick-start guide popup appears on first use

### Future Plans

We are considering upgrading the cloud sync architecture to support true multi-device real-time collaboration. Until then, please strictly follow the steps above when switching devices.

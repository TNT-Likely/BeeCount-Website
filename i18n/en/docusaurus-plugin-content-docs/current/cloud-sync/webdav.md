---
sidebar_position: 4
---

# WebDAV Sync

Sync data using the WebDAV protocol - supports various services and self-hosted solutions.

## Supported Services

- **Nutstore** - Recommended for China users
- **Synology NAS** - Self-hosted
- **NextCloud** - Open source self-hosted
- **Other WebDAV services**

## Nutstore Configuration

### 1. Register Nutstore

Visit [Nutstore](https://www.jianguoyun.com/) to create an account.

### 2. Get Application Password

1. Log into Nutstore web version
2. Go to "Account Info" → "Security Options"
3. Add an application password
4. Note the generated password

### 3. Configure BeeCount

1. Go to "Me" → "Cloud Service"
2. Select "WebDAV"
3. Enter configuration:
   - Server: `https://dav.jianguoyun.com/dav/`
   - Username: Nutstore account (email)
   - Password: Application password (not login password)
4. Save and test

## Synology NAS Configuration

### 1. Enable WebDAV

1. Open Synology DSM
2. Go to "Package Center" and install WebDAV Server
3. Enable WebDAV service

### 2. Configure BeeCount

- Server: `http://your-nas-address:5005/`
- Username: NAS username
- Password: NAS password

## Sync Directory

Data is saved in the `/BeeCount/` folder in your WebDAV root directory.

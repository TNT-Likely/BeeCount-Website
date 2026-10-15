---
sidebar_position: 5
---

# WebDAV Sync

Store your accounting data in your own cloud drive or NAS using WebDAV. BeeCount supports Nutstore, Synology, Nextcloud, and other WebDAV services.

:::tip Getting a 404? Check the URL and path first
Enter the complete **WebDAV endpoint** as the server URL. The remote path is a folder beneath that endpoint. A cloud drive homepage, share link, or NAS administration URL cannot serve as the WebDAV endpoint.

Start with the [provider examples](#provider-examples), then follow the [404 troubleshooting steps](#troubleshooting-404).
:::

## Server URL and remote path {#address-and-path}

Go to **Me → Cloud Service**, select **Custom WebDAV**, and fill in these four fields:

On a phone, swipe tables horizontally to see all columns.

| Field | What to enter | Example (Nutstore) |
| --- | --- | --- |
| WebDAV Server URL | The complete endpoint, including `https://`, the port if needed, and the endpoint path | `https://dav.jianguoyun.com/dav/` |
| Username | An account with WebDAV access | Your Nutstore registration email |
| Password | The password or app password required by the provider | An app password generated in Nutstore |
| Remote Path | A storage folder relative to the endpoint, starting with `/` | `/BeeCount` |

**The server URL and remote path combine to form the storage directory.** For example:

```text
Server URL:        https://dav.jianguoyun.com/dav/
Remote path:       /BeeCount
Storage directory: https://dav.jianguoyun.com/dav/BeeCount/
```

- `/` uses the directory addressed by the server URL itself. `/BeeCount` uses a `BeeCount` folder beneath it.
- If the server URL already contains `/dav/`, do not enter `/dav/BeeCount` as the remote path. That would produce `/dav/dav/BeeCount/`.
- If the server URL already ends in `/BeeCount/`, use `/` as the remote path to avoid adding a second `BeeCount` folder.
- Enter only a folder path as the remote path, not a complete URL, a local path such as `C:\Backup`, or a NAS filesystem path such as `/volume1/Backup`. Match the server's directory name capitalization.

:::note If you have already synced data
The current app defaults to `/`. `/BeeCount` is a suggested separate directory for new configurations; BeeCount does not append it automatically. Keep the working URL and path on existing devices. Changing the directory does not move existing data and may make your cloud ledgers appear missing.
:::

## Supported services and examples {#provider-examples}

Each row is a matching **server URL + remote path** pair. Except for Nutstore's fixed endpoint, replace the example domains, ports, usernames, and directory names with your own values. For self-hosted services, use the actual WebDAV endpoint supplied by your administrator.

| Provider | Example WebDAV server URL | Example remote path |
| --- | --- | --- |
| Nutstore | `https://dav.jianguoyun.com/dav/` | `/BeeCount` |
| Synology NAS | `https://nas.example.com:5006/Backup/` | `/BeeCount` |
| Nextcloud | `https://cloud.example.com/remote.php/dav/files/alice/` | `/BeeCount` |
| ownCloud Server (classic) | `https://cloud.example.com/remote.php/webdav/` | `/BeeCount` |
| QNAP NAS | `https://nas.example.com:PORT/Backup/` | `/BeeCount` |
| OpenList / AList | `https://files.example.com/dav/` | `/Storage/BeeCount` |

### Nutstore configuration

1. Register and sign in to the [Nutstore website](https://www.jianguoyun.com/).
2. Open **Account Info → Security Options → Third-party Applications** and generate an app password, for example named "BeeCount".
3. Enter the URL and path from the table in BeeCount. Use your registration email as the username and the generated **app password** as the password.

Keep `/dav/` at the end of the server URL. Do not use the Nutstore homepage URL or your account login password. See the [official Nutstore authorization guide](https://help.jianguoyun.com/?p=2064) (Chinese).

### Synology NAS configuration

1. Install and open **WebDAV Server** from DSM's **Package Center**. Enable HTTPS and check the configured port (default: `5006`).
2. Create or select an existing shared folder, such as `Backup`. Grant your NAS account read/write access to it and permission to use the WebDAV service.
3. Use the settings in the table, including the shared folder name in the server URL. Enter your NAS account credentials. The example storage directory is `https://nas.example.com:5006/Backup/BeeCount/`.

Do not use DSM's administration ports `5000` / `5001` or a QuickConnect web link. If you enabled HTTP only on your local network, its default WebDAV port is `5005`, and the URL should start with `http://`. Use the protocol and port actually configured. Your phone must be able to reach the WebDAV endpoint when connecting remotely.

See the [official Synology WebDAV Server guide](https://kb.synology.com/en-us/DSM/help/WebDAVServer/webdav_server?version=7).

### Nextcloud configuration

In Nextcloud's web interface, open **Files → Files settings**, copy the **WebDAV URL**, and paste the complete URL into BeeCount's server URL field. Replace `alice` in the table with the actual user ID, which may differ from the display name.

If Nextcloud is installed in a subdirectory, keep that prefix. For a website at `https://example.com/nextcloud/`, the endpoint is typically `https://example.com/nextcloud/remote.php/dav/files/alice/`.

Use the account's login name. Generate an app password under **Personal settings → Security**; use an app password when two-factor authentication is enabled. Prefer the copied URL and generated credentials to avoid omitting the user directory or entering only the domain. See the [official Nextcloud WebDAV guide](https://docs.nextcloud.com/server/stable/user_manual/en/files/access_webdav.html).

### ownCloud configuration

The example applies to classic **ownCloud Server**. Use credentials for an ownCloud account with read/write access. If your instance requires an app password, generate one as directed by your administrator.

If ownCloud is installed under `/owncloud/`, include that prefix, for example `https://example.com/owncloud/remote.php/webdav/`. For Infinite Scale or hosted editions, obtain the actual WebDAV endpoint from your administrator instead of assuming the classic path applies. See the [official ownCloud Server WebDAV guide](https://doc.owncloud.com/server/10.15/classic_ui/files/access_webdav.html).

### QNAP NAS configuration

Enable WebDAV on the NAS and grant your account read/write access to the target shared folder. Replace `PORT` in the table with your configured HTTPS WebDAV port and `Backup` with an existing shared folder name. Use the authorized NAS account credentials.

Check the protocol and port in your WebDAV settings. Do not assume Synology's `5006` applies or copy the QTS administration URL. See the [official QNAP connection guide](https://www.qnap.com/en-uk/how-to/faq/article/connecting-to-webdav-shared-folders-on-a-qnap-nas-in-windows-10).

### OpenList / AList configuration

- The server URL is usually the web service URL followed by `/dav/`. Use the **OpenList / AList account's own credentials**.
- Replace `Storage` in the table with a mounted drive directory visible to that user. If the user's root directory already points to the target drive, use `/BeeCount` without repeating the mount name.
- Enable WebDAV read, WebDAV management, and the required file permissions, such as creating folders, uploading, and deleting. The underlying drive must also support those write operations.
- Configure the drive mount first. Open the target directory in the web interface and confirm you can create folders and upload files.

See the [official OpenList WebDAV guide](https://doc.oplist.org/guide/advanced/webdav) and [official AList WebDAV guide](https://alistgo.com/guide/webdav).

## Verify your configuration {#verify-configuration}

1. Save the configuration, activate WebDAV on the Cloud Service page, and select **Test Connection**.
2. Manually upload a ledger using its sync feature, then confirm that data appears in the target directory on your drive or NAS.
3. On other devices, use the same account and settings that point to the same storage directory.

:::info Connection test passes, but uploads fail?
**Test Connection** only checks the server endpoint's response. It does not verify whether the remote directory exists or is writable. If sync still fails, check the target directory, write permissions, and reverse proxy configuration.
:::

## 404 and other common issues {#troubleshooting}

### 404 / Path not found {#troubleshooting-404}

A 404 usually means the server received the request but could not find the endpoint or directory. Check these items in order:

1. **Confirm the WebDAV endpoint.** Compare against the provider examples. Check for Nutstore's `/dav/`, Nextcloud's `/remote.php/dav/files/USER_ID/`, and other required components. A login URL or file share link cannot replace the endpoint.
2. **Combine the server URL and remote path.** Look for duplicated segments such as `/dav/dav/` or `/BeeCount/BeeCount/`, or a missing installation prefix, shared folder, or drive mount name. Check capitalization.
3. **Confirm the parent directory exists.** NAS shared folders and OpenList / AList drive mounts must be configured on the server first. BeeCount attempts to create the remote directory, but cannot create a NAS share or mount a drive. For nested paths, create the full directory in the web interface first.
4. **Identify when the error occurs.** If **Test Connection** returns 404, check the server URL and port first. If the test passes but uploads or downloads return 404, check the remote path, file existence, and account permissions.
5. **Check the reverse proxy for self-hosted services.** Forward the complete WebDAV path to the correct service without rewriting it to a login page or website. Try another WebDAV client with the same account and directory, including reading and writing files, to help isolate the issue.

Opening a URL in a browser alone cannot verify WebDAV support: ordinary web requests differ from the directory listing and upload requests used during sync.

### Other errors

| Error or symptom | Check first |
| --- | --- |
| `401` / Authentication failed | Username and password; Nutstore app password; app password requirements when two-factor authentication is enabled |
| `403` / Access denied | WebDAV access and directory read/write permissions; management and upload permissions in OpenList / AList |
| `405` / Method not allowed | Wrong web endpoint or port; whether the server or proxy permits WebDAV requests such as `OPTIONS`, `PROPFIND`, `MKCOL`, `PUT`, `GET`, and `DELETE` |
| `409` / Directory conflict | Missing parent directories; create the full directory in the web interface and retry |
| Timeout / Cannot connect | Whether your phone can reach the NAS network; domain, port, firewall, and port forwarding settings |
| Certificate / SSL error | Certificate validity and whether it matches the domain used to connect |
| Connected, but old ledgers are missing | Same account and storage directory as the original device; changed remote path or an extra folder level |

## Sync directory

Sync data is stored beneath the directory formed by **server URL + remote path**. BeeCount manages its own data subdirectories and files inside it. The directory is not always `/BeeCount/`, and does not refer to the NAS filesystem root.

The Nutstore example uses `dav/BeeCount/`; the Synology example uses the `BeeCount` subdirectory of the `Backup` shared folder. Keep existing devices configured consistently, and avoid manually renaming or moving files managed by BeeCount.

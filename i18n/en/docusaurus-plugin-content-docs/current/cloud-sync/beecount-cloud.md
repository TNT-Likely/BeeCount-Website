---
sidebar_position: 2
description: "BeeCount Cloud is the official self-hosted sync server. One-line Docker deployment, real-time multi-device sync across phone, web and tablet."
keywords: [BeeCount Cloud, self-hosted finance, Docker expense tracker, multi-device sync, self-hosted budget]
---

# BeeCount Cloud (Self-hosted)

> New in 3.0 · Recommended sync option for real-time multi-device collaboration

BeeCount Cloud is the **official self-hosted sync server** — deploy it in one Docker command and get:

- 🔄 **Real-time multi-device sync**: edit on phone A, pushed to phone B and Web within seconds
- 🌐 **Web UI bundled**: one Docker image = server + Web + PWA, ready in the browser
- 👥 **Multi-user isolation**: multiple users can register; their data is fully separated
- 🐳 **One-command deploy**: docker-compose file under 10 lines

## Who is it for?

| User type | Why it fits |
|---|---|
| 🏠 Households | Each member has their own account with isolated data (shared ledgers coming later) |
| 📱 One person, many devices | Phone / iPad / Web — seconds to sync, no more manual "upload / download" |
| 🖥️ NAS / VPS owners | Docker one-shot, data stays on your own machine |
| 👨‍💻 Technical users | Open source, auditable, fork-friendly |

## Deploy

Save the following as `docker-compose.yml`:

```yaml
services:
  beecount-cloud:
    image: sunxiao0721/beecount-cloud:latest
    restart: unless-stopped
    ports:
      - "8869:8080"
    volumes:
      - ./data:/data
```

Start:

```bash
mkdir -p beecount && cd beecount
# Save the yaml above as docker-compose.yml
docker compose up -d
```

On first boot, Docker will:

1. Create `./data/beecount.db` and run migrations
2. Generate `./data/.jwt_secret` (32-byte secret, 0600)
3. Auto-create an **admin account** with a random 16-char password

## Get the admin account

### Option 1: from logs (recommended)

```bash
docker compose logs beecount-cloud | grep -A 10 "admin"
```

You'll see:

```
========================================================================
 BeeCount Cloud — First boot. Admin account auto-created:

   email:    owner@example.com
   password: FIDodUnwprkw1zUi

   Credentials saved to /data/.initial_admin_password (0600, in volume)
========================================================================
```

### Option 2: read the file

```bash
cat ./data/.initial_admin_password
```

## Sign in

### Web UI

Browser to `http://<your-server>:8869`, sign in as admin.

After first login, **change the password immediately** (top-right avatar → account settings).

### Connect from the mobile app

1. Open BeeCount → **Me** → **Cloud sync**
2. Pick **BeeCount Cloud**
3. Enter server URL (e.g. `http://192.168.1.100:8869`) + admin email + password
4. First sign-in uploads your entire local ledger to the server

## Add family / teammates

**BeeCount Cloud does not allow self-registration** (to prevent abuse on public servers). Accounts must be created by an admin.

1. Admin signs in to the Web UI → **Users**
2. Click **Add user**, enter their email + a temporary password
3. Hand them the credentials; they sign in from the app or Web

Each user's data is isolated today. **Shared ledgers (multiple users editing the same ledger)** is on the roadmap.

## Advanced config

### Specify the bootstrap admin

The default is a randomly generated password. If you'd rather pick your own:

```yaml
services:
  beecount-cloud:
    image: sunxiao0721/beecount-cloud:latest
    restart: unless-stopped
    ports:
      - "8869:8080"
    environment:
      BOOTSTRAP_ADMIN_EMAIL: me@example.com
      BOOTSTRAP_ADMIN_PASSWORD: <your-strong-password>
    volumes:
      - ./data:/data
```

These two env vars **only take effect when the users table is empty** — changing them later won't affect existing accounts.

### Specify JWT secret

The server auto-generates `/data/.jwt_secret`. If you'd rather manage it yourself:

```yaml
environment:
  JWT_SECRET: <32+ byte random string>
```

When this env is set, the server won't generate or read from the file.

### Public deployment

Put nginx / Caddy in front for HTTPS + domain:

```
Users ─HTTPS─► Caddy/Nginx ─http://localhost:8869─► BeeCount Cloud
```

Both the app and Web accept `https://` URLs.

### Backup

All persistent data lives under `./data/`:

- `beecount.db` — SQLite database (ledgers, transactions, users)
- `attachments/` — file attachments (avatars, transaction images, custom category icons)
- `backups/` — backup archives
- `.jwt_secret` — JWT signing key (if lost, all tokens invalidate; users must sign in again)

Backing up the entire `data/` dir covers everything. Migrating to a new server is `rsync` + restart.

## PWA support

The Web UI is a **Progressive Web App**:

- An "**Install**" icon appears in the browser address bar — click to pin to desktop / Dock / Start menu
- Installed as a standalone app: no browser chrome, near-native feel
- Reads cached data offline, auto-resyncs when back online

## Upgrade

```bash
cd beecount
docker compose pull
docker compose up -d
```

Database migration runs automatically. `data/` is untouched.

## FAQ

### Q: App can't connect to the server

Check:

- Firewall allows port `8869` (or whatever you mapped)
- Phone and server are on the same network (or use public IP / domain)
- Server URL prefix matches — `http://` vs `https://`

### Q: The admin banner isn't in `docker compose logs`

It's only logged on **first boot**. The password file is at `./data/.initial_admin_password`.
If that file is also gone, you can set `BOOTSTRAP_ADMIN_EMAIL` + `BOOTSTRAP_ADMIN_PASSWORD` env to create a new admin (only works if the users table is empty). To reset an existing user's password, sign in as any admin and edit them in Web → Users.

### Q: Move the server to a new machine

- Old machine: `docker compose down`
- `rsync` the `data/` directory to the new machine
- New machine: same `docker-compose.yml`, `docker compose up -d`
- Update the server URL in the mobile app and sign in again

### Q: Can I change the theme color on Web?

Yes. Top-right avatar → Account settings → Theme color. Each user has their own preference, no interference.

## Related repos

- [BeeCount-Cloud](https://github.com/TNT-Likely/BeeCount-Cloud) — server + Web UI source
- [BeeCount](https://github.com/TNT-Likely/BeeCount) — mobile app source

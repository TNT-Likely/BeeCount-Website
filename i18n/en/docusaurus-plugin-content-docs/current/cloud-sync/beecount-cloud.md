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
| 🏠 Households | Each member has their own account **plus shared ledgers** — invite family to write into the same book, Owner / Editor roles included |
| 📱 One person, many devices | Phone / iPad / Web — seconds to sync, no more manual "upload / download" |
| 🖥️ NAS / VPS owners | Docker one-shot, data stays on your own machine |
| 👨‍💻 Technical users | Open source, auditable, fork-friendly |

:::tip Upgrade notes (1.6.0)
- App 3.6.0's [ledger multi-currency](../account/multi-currency.md) (transactions store the original currency + a converted snapshot in the ledger's base currency) requires **Cloud ≥ 1.6.0**: the server projection gains currency / conversion columns, ledger-level stats sum on the converted amount, and editing an amount on Web recomputes the conversion. **Upgrade the server first, then the App.**
- **This release includes a database schema migration** (the transactions table gains `currency_code` / `native_amount` columns + historical backfill), run automatically on image startup — `docker compose pull && docker compose up -d` is all you need, no manual steps.
- Older servers don't recognize these columns, so foreign transactions recorded by the new App lose their conversion on Web / across devices and ledger stats sum raw original amounts; upgrading to 1.6.0 brings it into alignment.
:::

:::tip Upgrade notes (1.5.1)
- The App 3.5.1 [Transaction flags](../record/flags.md) require **Cloud ≥ 1.5.1**: in cloud mode the server's income/expense and budget summaries filter by the Exclude from Income/Expense and Exclude from Budget flags; older servers don't recognize the flags, so cloud-side stats would still count flagged transactions (local mode and single-device stats are unaffected and always correct). **Always upgrade the server first, then the App.**
:::

:::tip Upgrade notes (1.5.0)
- The App 3.5.0 [Multi-currency](../account/multi-currency.md) and [Net worth over time](../account/net-worth-trend.md) require **Cloud ≥ 1.5.0**: the server provides base-currency sync, manual exchange rates, a rate proxy, and the net-worth-history read endpoint. **Always upgrade the server first, then the App.**
- **No database schema migration in this release**: net-worth-history is a read-only endpoint and multi-currency syncs at the user-global level (user-global projection), so `docker compose pull && docker compose up -d` is all you need — your data is untouched.
- Older servers don't recognize the base currency, so the conversion setting "won't sync" and the remote net worth trend is unavailable; upgrading to 1.5.0 brings them into alignment.
:::

:::tip Upgrade notes (1.4.0)
- The App 3.4.0 [Month Start Day](../account/month-start-day.md) requires **Cloud ≥ 1.4.0**: older servers ignore the setting (it looks like it "doesn't sync"). Upgrade the server first, then the App.
- Upgrading to 1.4.0 runs database migrations automatically and **backfills** a historical issue where some web-created transactions lacked an account link, making web account statistics too low — no manual action needed.
- Since 1.3.12 the web CSV import converts times using the client's timezone (fixes the 8-hour offset).
:::

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

Each user's data is isolated by default. For multi-person scenarios use **shared ledgers**: an Owner generates an invite code in the App / Web and Editors join by entering it.

### Shared ledgers (multi-user collaboration)

- **Owner / Editor roles** — Owners rename / invite / remove members; Editors co-write transactions and can't see the Owner's other ledgers
- **Realtime sync** — WebSocket fan-out, every member sees changes within seconds
- **Who wrote it / who last edited it** — every transaction is tagged with creator + last editor (avatar + role)
- **Member balance stats** — dedicated dialog on Web (chart-rich, bar + pie) / compact list on App
- **Three-platform parity** — invite / join / leave / kick works on iOS, Android, and Web

See the [Shared ledgers](../shared-ledger) doc for full usage.

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

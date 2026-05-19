---
sidebar_position: 7
title: Shared ledgers
---

# Shared ledgers

Let a family, a team, or a project group co-write the same ledger. The Owner sends invites, Editors join, and every transaction is tagged with creator + last editor. Realtime sync across iOS, Android, and Web.

> ⚠️ **Prerequisite**: shared ledgers are only available on the BeeCount Cloud backend. iCloud / WebDAV / S3 / Supabase are single-user multi-device targets — data doesn't cross users. See [BeeCount Cloud deployment](./cloud-sync/beecount-cloud).

## Roles & permissions

Two roles in Phase 1 (Viewer-only and Owner-transfer ship in Phase 3):

| Role | What they can do |
|---|---|
| **Owner** (creator) | Rename the ledger / change currency, invite, kick, delete the ledger; also writes transactions like an Editor |
| **Editor** (invited member) | Co-write transactions (create / edit / delete — both their own and others'); cannot rename, invite, or modify the Owner's user-global categories / accounts / tags |

> Design intent: Editors get a **read-only mirror** of the Owner's categories / accounts / tags (the SharedLedger\* tables on the App). When an Editor records a transaction inside the shared ledger, they pick from the Owner's resources — they cannot create new ones. This keeps the Owner from being flooded with unfamiliar categories from anyone they invite.

## Sending an invite (Owner)

### App

1. **Ledgers** tab → long-press the shared ledger → choose **Members**
2. On the member page → tap **Invite new member**
3. Pick TTL (1 h / 24 h / 3 d / 7 d) → tap **Generate code**
4. Copy the 6-character code or trigger system share (full text + URL)

### Web

1. Click the **Members / Invites** icon on the ledger card (top-right)
2. In the dialog, pick TTL → click **Generate code**
3. Copy the code or click share (system share sheet / fallback copy)

> Each ledger holds at most 10 active codes; default TTL is 24 h. The Owner can revoke at any time from the invite list.

## Joining an invite (Editor)

### App

1. **Me** → **Join shared ledger**
2. Enter the 6-character code → **Preview** (verify which ledger / who invited) → **Join**
3. After joining: the app pulls the Owner's resource snapshot (categories / accounts / tags) + historical transactions; the picker now uses the Owner's resources. Your own ledgers are untouched.

### Web

1. Ledgers page top → **Join shared ledger** button
2. Enter the code → preview → confirm

## Day-to-day collaboration

### Realtime sync

Any member's change — new tx, edit, delete, rename — fans out to all other members over WebSocket. Typical end-to-end latency: ~2 s.

### Who wrote / who last edited

Every tx is tagged with `created_by` + `last_edited_by`:

- **Same author and editor, but not you**: one avatar; long-press tooltip "X created and edited"
- **Different author and editor**: two avatars; long-press tooltips "X created" / "Y last edited"
- **You created and edited**: nothing shown (no point showing your own avatar on your own tx)

Where to see it:
- App: open the tx editor — avatars sit to the left of the amount
- Web: the tx detail dialog has dedicated "Created by" / "Last edited by" rows

### Member balance stats

Per-member income / expense / count by scope (this month / this year / all time).

- **App**: long-press the ledger card → **Member stats** → compact list (avatar + amounts + share % + count)
- **Web**: stats icon on the ledger card → dialog (KPI cards + horizontal bar chart for income vs expense + pie chart for expense share + detail list)

### Offline scenarios

- **Kicked while offline**: when the Editor reconnects, the WS event was lost while offline — but on reconnect the app reconciles `LedgerMember` membership and self-purges the local ledger if it's gone
- **Owner edits resources while Editor is offline**: on reconnect the App re-pulls `/shared-resources`, the SharedLedger\* mirror tables catch up automatically; Web has both WS push and on-demand fetch

## Leaving / removing

- **Editor leaves**: Member page → **Leave** → local data is purged, server removes the `LedgerMember` row
- **Owner removes an Editor**: Member page → trash icon next to the Editor → confirm; all of the removed user's devices receive the WS event and self-purge

> The Owner cannot leave their own shared ledger (otherwise nobody owns the book). Transfer ownership ships in Phase 3. Workarounds today: the Owner stays, or deletes the entire ledger.

## Known limits (MVP)

- **At most 5 members per ledger** (Phase 1 cap; will be raised later)
- **Editors cannot create new categories / accounts / tags**: only the Owner's global resources (mirror) are usable inside the shared ledger
- **No ownership transfer**: Phase 3 only
- **No Viewer (read-only) role**: Phase 3 only
- **No "soft conflict" notice**: simultaneous edits resolve via last-write-wins; a "X just edited this" toast ships in Phase 3
- **No per-member filtering of the tx list / insights**: currently shows all members combined

## Privacy boundary

- Editors only see the shared ledger they joined; they cannot see any of the Owner's other ledgers
- Editors only pick from the Owner's global resources; the Editor's own global resources are never leaked to the Owner or other members
- Invite codes default to 24 h TTL + Owner can revoke at any time; 6 characters from a 30-symbol set ≈ 7 × 10⁸ entropy

## Related docs

- [BeeCount Cloud deployment](./cloud-sync/beecount-cloud) — the sync backend shared ledgers depend on
- [FAQ](./faq) — "Can multiple people share a ledger?"

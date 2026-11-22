---
title: Privacy Policy
description: BeeCount Privacy Policy
---

# BeeCount Privacy Policy

**Last updated** 2026-11-22

## Summary

- Your bookkeeping records stay on your device by default. Cloud sync and AI use the services you configure.
- The official iOS App Store edition offers optional skin usage statistics, off by default.

## 1. Information We Collect

You can keep records locally without signing up. You can build the app from its public source and use it without the skin statistics service.

Starting with version 4.0.1, the official App Store edition offers optional skin usage statistics on iOS 16 and later. If you turn on “Share skin usage statistics,” the app sends a randomly generated installation ID, a random event ID and an event type. Events cover opening the skin picker, previewing a skin, starting or cancelling a purchase, and a verified App Store purchase that unlocked the skins. The server records when it receives each event.

## 2. How We Store Your Data

- **Local storage**: all your records are stored in a local database on your device.
- **Cloud sync (optional).** Synced data is stored on a BeeCount Cloud, Supabase or WebDAV server you configure.
- **Skin statistics (optional).** The statistics database deletes event records older than 90 days through a daily cleanup. Service provider recovery copies expire under the provider’s retention window. [Cloudflare D1 recovery and backups](https://developers.cloudflare.com/d1/reference/time-travel/).

## 3. Data Sharing

- If you enable **cloud sync**, data goes to the server you configure.
- If you enable **AI features**, the data needed for your request goes to the AI provider you configure (see Section 5).
- Skin statistics group events from the same installation to measure skin usage and purchase conversion. The records are kept separate from your ledgers, Apple Account, advertising identifier and purchase receipts. We use these records only for this analysis. Cloudflare hosts and processes the statistics and protects them under its Data Processing Addendum. [Cloudflare Data Processing Addendum](https://www.cloudflare.com/cloudflare-customer-dpa/).
- The Apple App Store handles in-app payments, restores and redemptions. [Apple Privacy Policy](https://www.apple.com/legal/privacy/).

## 4. Permissions

- **Camera**: to capture payment receipts for AI recognition (only when you use it).
- **Microphone**: for voice bookkeeping (only when you use it).
- **Photos / Storage**: to import or share bill files you select.
- **Network.** For the cloud service and AI provider you configure, App Store purchases, and skin statistics if you opt in.
- **Notifications / Reminders**: update prompts and bookkeeping reminders (optional).

## 5. AI Features & Third-Party Services (optional, off by default)

When you enable AI features and configure a provider, BeeCount sends — for the request you initiate — receipt/screenshot images, voice recordings, text you type, and the category names, account names and transaction records needed to complete recognition or analysis, to the provider you configured:

- **Zhipu GLM** (default, `open.bigmodel.cn`, operated by Zhipu) — subject to Zhipu's privacy policy.
- **Any other third-party AI service you configure** — subject to that provider's privacy policy.

AI is **OFF by default and requires your own API key**. Before any data is sent, the app shows an in-app notice naming the provider and the data involved and asks for your consent. BeeCount itself neither receives nor stores this data.

Cloud sync likewise:

- **Supabase**: subject to the [Supabase Privacy Policy](https://supabase.com/privacy).
- **WebDAV**: subject to your own server's privacy policy.

## 6. Your Rights

You can export bookkeeping records to CSV, clear local data or uninstall the app.

You can turn off “Share skin usage statistics” in Mine → Personalization → Skin at any time. The app stops collecting new events and clears pending statistics on your device. You can still preview, buy, restore and use skins. The server deletes previously received events on the schedule above. You can email us to request access to or deletion of skin statistics data about your installation.

## 7. Contact

- For privacy questions and data requests, contact us by email. [sunxiaoyes@outlook.com](mailto:sunxiaoyes@outlook.com).
- For public feedback, use GitHub Issues. [BeeCount Issues](https://github.com/TNT-Likely/BeeCount/issues).

---
title: Privacy Policy
description: BeeCount Privacy Policy
---

# BeeCount Privacy Policy

**Last updated**: 2026-06-25

## Summary

- BeeCount itself does **NOT** collect your data and does **NOT** operate any servers
- We do **NOT** use any analytics or tracking
- By default your data stays on your device; nothing is sent off-device
- Only when you actively enable and configure AI features is the relevant data sent to the third-party AI provider you choose

## 1. Information We Collect

BeeCount is privacy-first by design: no registration, no server-side collection, no analytics or crash reporting, no advertising SDKs, no third-party tracking.

## 2. How We Store Your Data

- **Local storage**: all your records are stored in a local database on your device.
- **Cloud sync (optional)**: if enabled, data is stored only on the server YOU configure (your own Supabase / WebDAV), which we cannot access.

## 3. Data Sharing

BeeCount itself does not collect or sell your data, and we do not operate servers that receive it.

- By default, no data leaves your device.
- If you enable **cloud sync**, data goes only to the server YOU configure.
- If you enable **AI features**, the data needed for your request is sent to the third-party AI provider YOU configure (see Section 5).

## 4. Permissions

- **Camera**: to capture payment receipts for AI recognition (only when you use it).
- **Microphone**: for voice bookkeeping (only when you use it).
- **Photos / Storage**: to import or share bill files you select.
- **Network**: to communicate with the cloud service / AI provider you configure.
- **Notifications / Reminders**: update prompts and bookkeeping reminders (optional).

## 5. AI Features & Third-Party Services (optional, off by default)

When you enable AI features and configure a provider, BeeCount sends — for the request you initiate — receipt/screenshot images, voice recordings, text you type, and the category names, account names and transaction records needed to complete recognition or analysis, to the provider you configured:

- **Zhipu GLM** (default, `open.bigmodel.cn`, operated by Zhipu) — subject to Zhipu's privacy policy.
- **Any OpenAI-compatible service you configure** (e.g. OpenAI, SiliconFlow, DeepSeek) — subject to that provider's privacy policy.

AI is **OFF by default and requires your own API key**. Before any data is sent, the app shows an in-app notice naming the provider and the data involved and asks for your consent. BeeCount itself neither receives nor stores this data.

Cloud sync likewise:

- **Supabase**: subject to the [Supabase Privacy Policy](https://supabase.com/privacy).
- **WebDAV**: subject to your own server's privacy policy.

## 6. Your Rights

You are fully in control of your data: export to CSV, clear data, or uninstall the app to delete all local data at any time.

## 7. Contact

- GitHub Issues: [github.com/TNT-Likely/BeeCount/issues](https://github.com/TNT-Likely/BeeCount/issues)

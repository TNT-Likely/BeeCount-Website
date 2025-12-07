---
sidebar_position: 3
---

# Supabase Sync

Sync data using a free PostgreSQL cloud database.

## What is Supabase?

[Supabase](https://supabase.com/) is an open-source Firebase alternative that provides a free PostgreSQL database.

## Advantages

- ✅ Generous free tier (500MB database)
- ✅ Cross-platform (iOS/Android)
- ✅ Real-time sync
- ✅ Full data control

## Configuration Steps

### 1. Register Supabase

Visit [supabase.com](https://supabase.com/) to create an account.

### 2. Create Project

1. Click "New Project"
2. Enter project name
3. Set database password
4. Select region (Asia recommended for Asian users)
5. Create project

### 3. Get Configuration Info

Find these in project settings:

- **Project URL** - Project address
- **anon public key** - Public API key

### 4. Configure BeeCount

1. Go to "Me" → "Cloud Service"
2. Select "Supabase"
3. Enter Project URL and anon key
4. Save and test connection

## Database Tables

Required tables are automatically created on first connection - no manual setup needed.

## Notes

- Free tier has some limitations, but sufficient for personal use
- Inactive projects may be paused after extended periods

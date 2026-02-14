---
sidebar_position: 3
---

# Supabase Sync

Sync data using a free PostgreSQL cloud database.

## What is Supabase?

[Supabase](https://supabase.com/) is an open-source Firebase alternative that provides a free PostgreSQL database and object storage.

## Advantages

- ✅ Generous free tier (500MB database + 1GB storage)
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

### 3. Create Storage Bucket

1. Click "Storage" in the left menu
2. Click "New bucket"
3. Enter bucket name: `beecount-backups`
4. **Do not check** Public bucket (keep it Private)
5. Create bucket

### 4. Configure RLS Policies

To allow the app to read and write data properly, you need to configure RLS (Row Level Security) policies to ensure users can only access their own data:

1. Go to "Storage" → Select `beecount-backups` bucket
2. Click the "Policies" tab
3. Create the following 4 policies:

| Policy Name | Operation |
|-------------|-----------|
| Allow user SELECT | SELECT |
| Allow user INSERT | INSERT |
| Allow user UPDATE | UPDATE |
| Allow user DELETE | DELETE |

Each policy should be configured the same way:

- **Target roles**: Select `authenticated`
- **Policy definition**: Enter the following expression

```sql
((bucket_id = 'beecount-backups'::text) AND ((storage.foldername(name))[1] = 'users'::text) AND ((storage.foldername(name))[2] = (auth.uid())::text))
```

> This policy ensures users can only access files in the `beecount-backups/users/<their-user-id>/` path.

### 5. Get Configuration Info

In "Project Settings" → "API", find:

- **Project URL** - Project address
- **anon public key** - Public API key

### 6. Configure BeeCount

1. Go to "Me" → "Cloud Service"
2. Select "Supabase"
3. Enter Project URL
4. Enter anon key
5. Enter Storage Name: `beecount-backups`
6. Save and test connection

### 7. Configure Synchronization

1. In your Supabase project, go to "Authentication" in the left sidebar.
2. Open the Users page.
3. Click "Add user" → "Create new user".
4. Enter an email address and password, then create the user.
5. In BeeCount, go to "Mine" → "Sync".
6. Click "Login/Register" and enter the email address and password created above.

## Notes

- Free tier has some limitations, but sufficient for personal use
- Inactive projects may be paused (log in within 7 days to restore)
- Recommend regular data export backups

# Convex Migration Guide

This document describes the migration from Supabase to Convex for authentication and user data storage.

> **First time setting up Convex?** See [web/CONVEX_SETUP.md](web/CONVEX_SETUP.md) for step-by-step instructions.

## What Changed

### Backend (Convex)
- **Authentication**: Email/password + Google OAuth now handled by Convex Auth
- **Data Tables**: 
  - `journal_notes` - User journal entries
  - `learn_progress` - Learning path progress tracking
- **Schema**: Defined in `web/convex/schema.ts`
- **Queries/Mutations**: In `web/convex/journalNotes.ts` and `web/convex/learnProgress.ts`

### Frontend
- **Auth Provider**: Replaced Supabase client with Convex React hooks
- **Middleware**: Updated to use Convex Auth middleware
- **Components**: All auth-dependent components updated to use new API

### FastAPI Backend
- **JWT Verification**: Updated to verify Convex tokens via JWKS endpoint
- **Auth Module**: `app/auth.py` now uses Convex JWT verification

## Setup Instructions

For detailed setup instructions, see [web/CONVEX_SETUP.md](web/CONVEX_SETUP.md).

### Quick Start

1. **Deploy Convex Functions**

```bash
cd web
npx convex dev
```

Follow the prompts to log in and create/select a project.

2. **Configure Environment**

Add your Convex deployment URL to `.env.local`:

```bash
NEXT_PUBLIC_CONVEX_URL=https://your-deployment.convex.cloud
```

3. **Test Locally**

```bash
cd web
npm run dev
```

Visit http://localhost:3000 and test email/password auth.

### Optional: Google OAuth

See [web/CONVEX_SETUP.md](web/CONVEX_SETUP.md#6-optional-add-google-oauth) for Google OAuth setup.

## Data Migration

### From Existing Supabase Project

If you have existing data in Supabase that needs to be migrated:

1. **Export from Supabase**:
   ```sql
   -- Export journal notes
   COPY (SELECT * FROM journal_notes) TO '/path/to/journal_notes.csv' CSV HEADER;
   
   -- Export learn progress
   COPY (SELECT * FROM learn_progress) TO '/path/to/learn_progress.csv' CSV HEADER;
   ```

2. **Import to Convex**:
   Create a migration script in `web/convex/migrations/` to import the CSV data:
   
   ```typescript
   // web/convex/migrations/importSupabaseData.ts
   import { internalMutation } from "../_generated/server";
   import { v } from "convex/values";
   
   export const importJournalNotes = internalMutation({
     args: { notes: v.array(v.any()) },
     handler: async (ctx, args) => {
       for (const note of args.notes) {
         await ctx.db.insert("journal_notes", {
           userId: note.user_id,
           passageId: note.passage_id,
           passageTitle: note.passage_title,
           body: note.body,
           tags: note.tags || [],
           prompt: note.prompt,
           kind: note.kind,
           question: note.question,
           chatMode: note.chat_mode,
           verseId: note.verse_id,
           createdAt: note.created_at,
           updatedAt: note.updated_at,
         });
       }
     },
   });
   ```

3. Run the migration via Convex dashboard or CLI

## Removed Files

The following Supabase-specific files were removed:

- `web/src/lib/supabaseClient.ts` - Supabase browser client
- `web/src/lib/authApi.ts` - API auth helpers
- `web/src/app/auth/callback/route.ts` - OAuth callback handler
- `web/src/app/auth/continue/page.tsx` - OAuth fallback page
- `supabase/migrations/` - SQL migrations (reference only)

## Environment Variables Removed

- `SUPABASE_URL`
- `SUPABASE_JWT_SECRET`
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`

## Environment Variables Added

- `NEXT_PUBLIC_CONVEX_URL` - Your Convex deployment URL
- `GOOGLE_CLIENT_ID` - Google OAuth client ID
- `GOOGLE_CLIENT_SECRET` - Google OAuth client secret

## Troubleshooting

### Build Errors

If you get TypeScript errors about missing Convex generated files:

```bash
cd web
npx convex dev --once
```

This generates the `_generated` types.

### Auth Not Working

1. Check that `NEXT_PUBLIC_CONVEX_URL` is set
2. Verify Google OAuth credentials are correct
3. Check that authorized redirect URIs match your domain
4. Look for auth errors in browser console

### Data Not Syncing

1. Verify user is signed in
2. Check browser console for Convex errors
3. Verify Convex functions are deployed: `npx convex dev`
4. Check Convex dashboard logs

## API Changes

### Old (Supabase)
```typescript
import { getSupabase } from "@/lib/supabaseClient";

const supabase = getSupabase();
await supabase.from("journal_notes").insert(data);
```

### New (Convex)
```typescript
import { useMutation } from "convex/react";
import { api } from "../convex/_generated/api";

const upsert = useMutation(api.journalNotes.upsert);
await upsert(data);
```

## Support

For issues specific to this migration, contact the Pratibha team.

For Convex-specific help:
- Docs: https://docs.convex.dev
- Discord: https://convex.dev/community

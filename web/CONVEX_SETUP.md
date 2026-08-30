# Convex Setup Instructions

This guide walks through setting up Convex for local development.

## Prerequisites

- Node.js 18+ installed
- A Convex account (free at https://convex.dev)

## Step-by-Step Setup

### 1. Install Dependencies

```bash
cd web
npm install
```

### 2. Initialize Convex

Run the Convex dev server for the first time:

```bash
npx convex dev
```

This will:
1. Prompt you to log in to Convex (opens browser)
2. Ask you to create or select a project
3. Generate `convex/_generated/` types
4. Deploy your schema and functions
5. Give you a deployment URL

**Expected prompts:**
- "Log in to Convex" → Opens browser for authentication
- "Create a new project or select an existing one" → Choose option
- "Project name?" → Enter a name (e.g., "pratibha-dev")

After setup completes, you'll see:
```
✔ Deployed schema and functions
  Deployment URL: https://your-name-123.convex.cloud
```

### 3. Configure Environment Variables

Copy the deployment URL and add it to your environment:

**Option A: Create `.env.local`** (recommended for development)

```bash
# web/.env.local
NEXT_PUBLIC_CONVEX_URL=https://your-name-123.convex.cloud
```

**Option B: Use the root `.env`**

```bash
# .env (in repository root)
NEXT_PUBLIC_CONVEX_URL=https://your-name-123.convex.cloud
```

### 4. Generate Types

If types aren't generated, run:

```bash
npx convex dev --once
```

This generates TypeScript types in `convex/_generated/` without starting the dev server.

### 5. Test Auth (Email/Password)

With `npx convex dev` running in one terminal, start Next.js in another:

```bash
cd web
npm run dev
```

Then:
1. Visit http://localhost:3000
2. Click "Sign in"
3. Create an account with email/password
4. Verify you're signed in

### 6. (Optional) Add Google OAuth

To enable Google sign-in:

1. **Get Google OAuth credentials:**
   - Go to https://console.cloud.google.com
   - Create a project
   - Enable OAuth 2.0
   - Create credentials (OAuth 2.0 Client ID)
   - Set authorized redirect URIs to the **Convex Auth callback**, not localhost:
     - `https://energized-armadillo-158.convex.site/api/auth/callback/google`
     - (Dev and prod Convex deployments each need their own `*.convex.site` callback.)
   - Authorized JavaScript origins can include `http://localhost:3000` and the production site.

2. **Add to environment:**

```bash
# web/.env.local (or root .env)
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
```

3. **Restart Convex dev:**

```bash
# Stop npx convex dev (Ctrl+C)
npx convex dev
```

Google OAuth will now be available on the sign-in page.

## Troubleshooting

### `Cannot find module './_generated/server'`

**Solution:** Run `npx convex dev` or `npx convex dev --once` to generate types.

### `NEXT_PUBLIC_CONVEX_URL is not defined`

**Solution:** Add the deployment URL to `.env.local` or `.env`:

```bash
NEXT_PUBLIC_CONVEX_URL=https://your-name-123.convex.cloud
```

### `Convex login failed`

**Solution:** 
1. Check your internet connection
2. Try `npx convex logout` then `npx convex dev` again
3. Clear browser cache and retry

### TypeScript errors after running `npx convex dev`

**Solution:** Restart your editor/IDE to pick up the newly generated types.

## Production Deployment

### 1. Create Production Deployment

```bash
npx convex deploy --prod
```

This creates a separate production deployment with its own URL.

### 2. Set Production Environment Variables

In your Cloudflare dashboard:

```bash
NEXT_PUBLIC_CONVEX_URL=https://your-prod-123.convex.cloud
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
```

### 3. Deploy Frontend

```bash
cd web
npm run deploy
```

## Common Commands

```bash
# Start dev server (watch mode)
npx convex dev

# Deploy to production
npx convex deploy --prod

# Generate types only (no server)
npx convex dev --once

# View logs
npx convex logs

# List deployments
npx convex deployments

# Log out
npx convex logout
```

## File Structure

```
web/
├── convex/
│   ├── _generated/         # Auto-generated types (git-ignored)
│   ├── auth.ts             # Auth configuration
│   ├── auth.config.ts      # JWT provider config
│   ├── http.ts             # HTTP routes for auth
│   ├── schema.ts           # Database schema
│   ├── journalNotes.ts     # Journal queries/mutations
│   ├── learnProgress.ts    # Learning progress queries/mutations
│   └── convex.json         # Convex configuration
└── src/
    └── lib/
        └── convexClient.tsx  # React provider
```

## Resources

- Convex Docs: https://docs.convex.dev
- Convex Auth Docs: https://labs.convex.dev/auth
- Dashboard: https://dashboard.convex.dev
- Community: https://convex.dev/community

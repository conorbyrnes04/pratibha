# Convex Setup - Quick Reference

## First-Time Setup Commands

Run these commands in order for a fresh Convex setup:

```bash
# 1. Navigate to web directory
cd web

# 2. Install dependencies (if not already done)
npm install

# 3. Start Convex dev server (will prompt for login)
npx convex dev
```

**Follow the prompts:**
- Log in to Convex (opens browser)
- Create or select a project
- Choose a project name

**Expected output:**
```
✔ Deployed schema and functions
  Deployment URL: https://your-name-123.convex.cloud
```

```bash
# 4. Copy the deployment URL and add to .env.local
echo "NEXT_PUBLIC_CONVEX_URL=https://your-name-123.convex.cloud" > .env.local

# 5. In a new terminal, start Next.js dev server
npm run dev
```

## Test Email/Password Auth

1. Visit http://localhost:3000
2. Click "Sign in"
3. Switch to "Create account"
4. Enter email and password (minimum 6 characters)
5. Click "Create account"
6. You should be signed in automatically

## Verify Setup

After signing in, check:
- [ ] You see your email in the account menu (top right)
- [ ] You can navigate to `/journal` and see the journal page
- [ ] Browser console shows no Convex errors
- [ ] `npx convex dev` terminal shows no errors

## Troubleshooting

### "Cannot find module './_generated/server'"

Run: `npx convex dev --once` to generate types.

### "NEXT_PUBLIC_CONVEX_URL is not defined"

Add the deployment URL to `web/.env.local`:
```bash
NEXT_PUBLIC_CONVEX_URL=https://your-deployment.convex.cloud
```

### Types not working in IDE

Restart your IDE/editor after running `npx convex dev`.

## Optional: Add Google OAuth

Only needed if you want Google sign-in:

1. Get credentials from https://console.cloud.google.com
2. Add to `web/.env.local`:
```bash
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-secret
```
3. Restart `npx convex dev`

See [CONVEX_SETUP.md](./CONVEX_SETUP.md) for detailed instructions.

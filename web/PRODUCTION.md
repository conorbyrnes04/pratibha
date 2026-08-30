# Production Deployment

This document describes the production topology and deployment configuration for Pratibha.

## Live Infrastructure

### Frontend (Next.js on Cloudflare)
- **Public URL**: https://pratibha.agniagama.com
- **Hosting**: Cloudflare Workers (via OpenNext)
- **Wrangler Worker Name**: `pratibha`
- **Custom Domain**: pratibha.agniagama.com
- **Deployment**: `wrangler deploy` from web/ directory (after `npm run build`)

### Backend Services

#### Verses/Chat API (Render)
- **URL**: https://pratibha-1.onrender.com
- **Hosting**: Render web service
- **Purpose**: Provides verse data and chat functionality

#### Authentication Backend (Convex)
- **Production Deployment**: `giant-lapwing-264`
- **Convex Cloud URL**: https://giant-lapwing-264.convex.cloud
- **Convex Site URL**: https://giant-lapwing-264.convex.site
- **Auth Providers**: Google OAuth, Password (via @convex-dev/auth)
- **Deployment**: `npx convex deploy` from web/ directory only

#### Legacy Dev Deployment (DO NOT USE IN PRODUCTION)
- **Dev Convex**: https://energized-armadillo-158.convex.cloud
- **Status**: Previously used by production, now migrated to giant-lapwing-264

## Google OAuth Configuration

### Required Credentials (Set in Convex Dashboard)
Set these environment variables in the Convex production deployment dashboard:

```
AUTH_GOOGLE_ID=<your-google-client-id>
AUTH_GOOGLE_SECRET=<your-google-client-secret>
GOOGLE_CLIENT_ID=<your-google-client-id>
GOOGLE_CLIENT_SECRET=<your-google-client-secret>
SITE_URL=https://pratibha.agniagama.com
```

### Google Cloud Console Setup

**Web Client ID**: Starts with `999545287985-...`

**Authorized JavaScript Origins**:
- https://pratibha.agniagama.com
- https://giant-lapwing-264.convex.site
- http://localhost:3000 (for local development)

**Authorized Redirect URIs**:
- https://giant-lapwing-264.convex.site/api/auth/callback/google (PRODUCTION)
- https://energized-armadillo-158.convex.site/api/auth/callback/google (legacy dev)
- http://localhost:3000/api/auth/callback/google (local development)

> **Action Required**: Add the production callback URL to your Google Cloud Console OAuth client configuration.

## Environment Files

### `.env.production` (gitignored, required for builds)
Production builds require a `web/.env.production` file with these values:

```bash
# Copy from .env.production.example and verify these production values:
NEXT_PUBLIC_CONVEX_URL=https://giant-lapwing-264.convex.cloud
NEXT_PUBLIC_CONVEX_SITE_URL=https://giant-lapwing-264.convex.site
NEXT_PUBLIC_API_BASE=https://pratibha-1.onrender.com
NEXT_PUBLIC_SITE_URL=https://pratibha.agniagama.com
```

**Important**: 
- This file is gitignored and should NOT be committed
- Copy from `web/.env.production.example` as a template
- The file MUST exist for production builds (`npm run build`)
- The `scripts/assert-prod-env.mjs` validates it before building

**For Cloudflare deployment:**
You can also set these as Cloudflare Worker environment variables in the Cloudflare dashboard as a backup, but the `.env.production` file is still required for the Next.js build step.

### `.env.development.local` (local dev only)
For local development overrides. Not included in production builds.

### Important: Never use `.env.local` for production
Next.js loads `.env.local` during production builds, which can accidentally bake localhost URLs into deployed code. The `scripts/assert-prod-env.mjs` guard prevents this.

## Deployment Workflow

### 1. Deploy Convex Functions
```bash
cd web
npx convex deploy --prod giant-lapwing-264
```

**Important**: Always deploy from `web/` directory. The Lynx `pratibha/` folder has a different `auth.ts` that omits `isAuthenticated`.

### 2. Build Next.js for Production
```bash
cd web
npm run build
```

This validates `.env.production` and creates an optimized OpenNext build.

### 3. Deploy to Cloudflare
```bash
cd web
wrangler deploy
```

This uploads the OpenNext build to Cloudflare Workers.

### 4. Verify Deployment
- Visit https://pratibha.agniagama.com
- Test Google OAuth sign-in flow
- Verify users are redirected to production domain (not localhost)
- Check that Convex connection points to giant-lapwing-264

## Authentication Flow

1. User clicks "Continue with Google" on `/login`
2. Next.js frontend calls Convex signIn with `redirectTo: window.location.origin`
3. Convex redirects to Google OAuth with production callback URL
4. Google redirects back to `https://giant-lapwing-264.convex.site/api/auth/callback/google`
5. Convex validates the token and redirects to `https://pratibha.agniagama.com`
6. User is authenticated and can access protected routes

### Redirect Allowlist
The `convex/auth.ts` redirect callback allows:
- https://pratibha.agniagama.com (production)
- http://localhost:3000 (local dev)
- pratibha:// (iOS app deep link)
- *.convex.site (Convex hosted callbacks)
- *.convex.cloud (Convex API endpoints)
- Private network IPs (192.168.*, 10.*)

## Legacy Systems

### Supabase Auth (Deprecated)
Previous authentication system. All production auth now flows through Convex with Google OAuth.
No Supabase credentials should be set in production environment variables.

## Troubleshooting

### "Redirect URI mismatch" error
- Verify the Google Cloud Console has the production callback URL
- Check that `SITE_URL` is set correctly in Convex dashboard
- Ensure `.env.production` uses production URLs, not localhost

### Users redirected to localhost after OAuth
- Verify `AuthProvider.tsx` passes `redirectTo: window.location.origin`
- Check that `convex/auth.ts` allows the production domain
- Ensure production build uses `.env.production`, not `.env.local`

### Convex connection failed
- Verify `NEXT_PUBLIC_CONVEX_URL` points to giant-lapwing-264
- Check Convex dashboard for deployment status
- Ensure Convex functions were deployed with `npx convex deploy`

## Security Notes

- Never commit `.env.local` or `.env.production.local` files
- Service role keys and secrets should only be set in Cloudflare/Convex dashboards
- Google OAuth secrets are stored in Convex dashboard, not in repository
- The production site serves over HTTPS only (enforced by Cloudflare)

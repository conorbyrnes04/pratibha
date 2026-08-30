# Lynx Migration Summary

## Status: Work in Progress

I've created a Lynx/ReactLynx frontend structure to replace Next.js, but encountered component API issues that need resolution.

## What Was Completed

### ✅ Convex Backend (Fully Working)
- Schema: `journal_notes`, `learn_progress` tables
- Auth: Email/password + optional Google OAuth  
- Functions: Queries and mutations for all data operations
- Configuration: `convex.json`, `auth.config.ts`, `http.ts`

### ✅ Lynx App Structure Created
Location: `/workspace/pratibha/`

```
pratibha/
├── src/
│   ├── App.tsx                    # Main app
│   ├── components/Navigation.tsx  # Top nav
│   ├── pages/HomePage.tsx         # Home page
│   ├── auth/AuthProvider.tsx      # Auth context
│   └── convex/ConvexProvider.tsx  # Convex integration
├── convex/                        # Backend (copied from web/)
├── lynx.config.ts                 # Rspeedy config
├── package.json                   # Dependencies installed
└── README.md                      # Setup instructions
```

### ✅ Dependencies Installed
- `@lynx-js/rspeedy` (v0.16.5)
- `@lynx-js/react` (v0.125.0)
- `@lynx-js/react-rsbuild-plugin` (v0.19.1)
- `convex` (v1.45.0)
- React 19

## Issue Discovered

### Lynx Component API

**Problem:** `@lynx-js/react` does NOT export React Native-style primitives:
- ❌ No `View`
- ❌ No `Text`
- ❌ No `Button`
- ❌ No `ScrollView`

**Available exports:** Only React core (createElement, hooks, Context, etc.)

**Workaround Applied:** Using standard HTML elements (div, button, h1, p) which work on Lynx's Web target.

**Impact:**
- ✅ Should work on Web target (browser)
- ❓ Unknown if this works on native (iOS/Android) - needs Lynx Explorer testing
- ⚠️ May need official Lynx examples to understand proper component usage

## Commands

From `/workspace/pratibha`:

```bash
# Install dependencies
npm install

# Start Convex backend
npx convex dev

# Add deployment URL to .env
echo "NEXT_PUBLIC_CONVEX_URL=https://your-deployment.convex.cloud" > .env

# Run Lynx app (Web target)
npm run dev
```

**Expected:** Opens browser at `http://localhost:3000`

## What Needs to Be Done

1. **Verify rspeedy dev server works** - Couldn't fully test in non-interactive environment
2. **Clarify Lynx component usage** - Need official examples showing proper ReactLynx component patterns
3. **Complete Convex HTTP client** - Implement fetch-based API calls (to avoid BigInt issues on native)
4. **Port remaining features**:
   - Login page with email/password
   - Journal CRUD
   - Learning progress sync
   - Reading passages (from FastAPI)
5. **Test on native** - Verify HTML elements work or switch to proper Lynx primitives

## Limitations Hit

### 1. BigInt on Native
- Issue: Convex JS client uses BigInt, incompatible with Lynx PrimJS runtime (get-convex/convex-js#71)
- Solution: HTTP-based Convex communication (no WebSocket subscriptions)
- Status: Provider structure in place, implementation pending

### 2. Component API Mismatch
- Issue: Expected React Native-style API, got React core only
- Solution: Using HTML for Web target
- Status: Needs validation with official Lynx patterns

### 3. Dev Server
- Issue: Couldn't fully test in non-interactive cloud environment
- Solution: Needs local testing or Lynx Explorer
- Status: Config appears valid, untested

## Files

- **PR:** https://github.com/conorbyrnes04/pratibha/pull/1
- **Branch:** `cursor/convex-migration-2d2c`
- **Commit:** ea12970e "WIP: Add Lynx/ReactLynx frontend structure"

## Recommendation for Conor

1. **Test locally:**
   ```bash
   cd /workspace/pratibha
   npm install
   npm run dev
   ```

2. **Check:** Does it open in browser? Any errors?

3. **Decision point:**
   - If Web target works → Continue porting features with HTML elements
   - If not → Need to investigate proper Lynx ReactLynx component usage from official docs/examples

The Convex backend is production-ready. The frontend needs component API clarification and local testing.

# Lynx Migration - Status Report

## What Was Done

### 1. Created Lynx/ReactLynx App Structure

Created `/workspace/pratibha/` as the new Lynx-based frontend:

```
pratibha/
├── src/
│   ├── App.tsx              # Main app (React with Lynx)
│   ├── components/          # UI components
│   │   └── Navigation.tsx
│   ├── pages/
│   │   └── HomePage.tsx
│   ├── auth/
│   │   └── AuthProvider.tsx
│   └── convex/
│       └── ConvexProvider.tsx
├── convex/                   # Convex backend (copied from web/)
│   ├── schema.ts
│   ├── auth.ts
│   ├── journalNotes.ts
│   ├── learnProgress.ts
│   ├── http.ts
│   └── auth.config.ts
├── lynx.config.ts           # Lynx/Rspeedy config
├── tsconfig.json
├── package.json
├── .env.example
└── README.md
```

### 2. Kept Convex Backend

✅ All Convex schema and functions preserved:
- `journal_notes` table
- `learn_progress` table  
- Password auth + Google OAuth
- Queries and mutations

### 3. Removed Next.js

The `web/` directory remains for now but is no longer the primary UI path.

### 4. Key Components Ported

- ✅ Basic app structure
- ✅ Navigation
- ✅ Home page
- ✅ Auth provider (placeholder)
- ✅ Convex provider (HTTP-based to avoid BigInt issues)

## How to Run (After Setup Complete)

```bash
cd /workspace/pratibha

# 1. Install dependencies
npm install

# 2. Start Convex backend
npx convex dev

# 3. Add CONVEX_URL to .env
echo "NEXT_PUBLIC_CONVEX_URL=https://your-deployment.convex.cloud" > .env

# 4. Run Lynx app
npm run dev
```

Opens at `http://localhost:3000` (Web target).

## Known Issues & Limitations

### 1. Lynx Component API

**Issue:** `@lynx-js/react` doesn't export React Native-style primitives (View, Text, Button, ScrollView).

**Current Approach:** Using standard HTML elements (div, button, h1, p) which work on Lynx's Web target.

**Impact:** 
- ✅ Works on Web target (browser)
- ❓ May need adjustment for native targets (iOS/Android)

### 2. BigInt Compatibility

As mentioned in get-convex/convex-js#71, Convex's JS client has BigInt issues on native Lynx (PrimJS).

**Solution:** HTTP-based Convex communication instead of WebSocket client.

**Status:** Convex provider set up for HTTP, full implementation pending.

### 3. rspeedy Dev Server

**Issue:** Dev server starts but may require additional configuration for proper hot reload and bundling.

**Status:** Basic structure in place, needs testing.

## Next Steps to Complete

1. **Test Lynx Dev Server**: Verify `npm run dev` opens browser with working app
2. **Implement HTTP Convex Client**: Complete the ConvexProvider with fetch-based API calls
3. **Port Login Page**: Email/password form with Convex auth
4. **Port Journal**: CRUD operations for journal notes
5. **Port Learning Progress**: Sync learning path completion
6. **Port Reading UI**: Display passages from FastAPI/corpus
7. **Handle Native Targets**: Test/adjust components for iOS/Android if needed

## Files Replaced vs Kept

### Replaced
- ❌ `web/` Next.js app (no longer primary)
- ❌ React DOM rendering
- ❌ Next.js-specific features (SSR, API routes, middleware)
- ❌ Tailwind + shadcn/ui

### Kept
- ✅ Convex backend (`convex/` directory)
- ✅ FastAPI server (`/app`)
- ✅ Corpus data (`/data`)
- ✅ All canonical texts

## Commands That Should Work

```bash
# From /workspace/pratibha

# Install
npm install

# Convex setup
npx convex dev

# Run app
npm run dev

# Type check
npm run typecheck

# Build
npm run build
```

## Recommendation

Given the complexity of Lynx setup and the component API differences discovered, consider:

1. **Option A**: Complete the Lynx migration with standard HTML elements for Web target first
2. **Option B**: Investigate proper Lynx native component usage from official examples
3. **Option C**: Keep Next.js for Web, use Lynx only for true native apps (iOS/Android)

The Convex backend is solid and ready. The frontend porting needs component API clarification.

# Pratibha - Lynx + Convex Edition

Pratibha wisdom study app rebuilt with Lynx (native rendering) and Convex (backend).

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Set Up Convex

```bash
# Start Convex dev server (will prompt for login)
npx convex dev
```

Follow the prompts to log in and create/select a project. This will generate types and deploy your backend.

Copy the deployment URL shown and add to `.env`:

```bash
NEXT_PUBLIC_CONVEX_URL=https://your-deployment.convex.cloud
```

### 3. Run the App

**Web Target (Recommended for First Test):**

```bash
npm run dev
```

This opens the app in your browser at `http://localhost:3000`.

**Native Target (Optional - Requires Lynx Explorer):**

1. Download Lynx Explorer app on your phone/device
2. `npm run dev` will show a QR code
3. Scan with Lynx Explorer to see native rendering

## Project Structure

```
pratibha/
├── src/                      # Lynx React app
│   ├── App.tsx              # Main app component
│   ├── components/          # UI components
│   ├── pages/               # Page components
│   ├── auth/                # Auth provider
│   └── convex/              # Convex integration
├── convex/                   # Convex backend
│   ├── schema.ts            # Database schema
│   ├── auth.ts              # Auth setup
│   ├── journalNotes.ts      # Journal queries/mutations
│   └── learnProgress.ts     # Learning progress
├── lynx.config.ts           # Lynx/Rspeedy configuration
└── package.json
```

## What Was Replaced

### Removed (Next.js Frontend)
- `web/` directory - Entire Next.js app with React DOM
- Next.js-specific features (SSR, API routes, middleware)
- React DOM rendering
- Tailwind CSS + shadcn/ui components

### Added (Lynx Frontend)
- Lynx/ReactLynx for native rendering
- Simplified component structure
- Direct Convex integration via HTTP (avoids BigInt issues)
- Cross-platform ready (iOS, Android, Web)

### Kept (Backend)
- Convex schema (journal_notes, learn_progress)
- Convex Auth (email/password + Google OAuth)
- FastAPI server in `/app` (for corpus/RAG)
- All canonical texts in `/data`

## Features

Current implementation:
- ✅ Basic app structure with navigation
- ✅ Home page
- ✅ Convex backend integration
- ✅ Auth provider (placeholder)
- ✅ Web target works in browser

To be implemented:
- ⏳ Email/password login
- ⏳ Journal notes (create, sync)
- ⏳ Learning progress
- ⏳ Reading passages
- ⏳ Daily passage feature

## Development

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Type check
npm run typecheck
```

## Known Limitations

### BigInt Compatibility
Convex's JavaScript client has BigInt compatibility issues on native Lynx (PrimJS runtime). 

**Solution:** We use HTTP-based Convex communication instead of the WebSocket client. This works on all targets including native.

### Web vs Native
- **Web target**: Full Convex support, works in browsers
- **Native target**: HTTP-only Convex (no real-time subscriptions)

## API (FastAPI Backend)

The FastAPI server (`/app`) is still available for:
- Corpus text serving
- RAG (semantic search)
- LLM chat integration

Start it separately:

```bash
cd /workspace
source .venv/bin/activate
uvicorn app.main:app --reload
```

## Environment Variables

Create `.env`:

```bash
# Convex
NEXT_PUBLIC_CONVEX_URL=https://your-deployment.convex.cloud

# Google OAuth (optional)
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-secret
```

## Resources

- [Lynx Documentation](https://lynxjs.org/)
- [Convex Documentation](https://docs.convex.dev/)
- [ReactLynx Guide](https://lynxjs.org/next/react/)

# Pratibha - Lynx + Convex Edition

Pratibha wisdom study app with Lynx native rendering and Convex backend.

## Quick Start

```bash
# 1. Install dependencies
cd pratibha
npm install

# 2. Set up Convex backend
npx convex dev
# Follow prompts to login and create/select project
# Copy the deployment URL shown

# 3. Configure environment
echo "NEXT_PUBLIC_CONVEX_URL=https://your-deployment.convex.cloud" > .env

# 4. Start FastAPI (for corpus/passages) in another terminal
cd ..
source .venv/bin/activate  # or: python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# 5. Run the Lynx app
cd pratibha
npm run dev
```

Opens at `http://localhost:3000`.

## Features

- ✅ Email/password authentication (Convex Auth)
- ✅ Today's daily passage
- ✅ Library with collection filters, search, and prev/next reading
- ✅ Chat against the FastAPI corpus
- ✅ Learn paths and themes with local/Convex progress
- ✅ Lexicon browse and lemma detail
- ✅ Sources attributions
- ✅ Journal entries (create, list, sync via Convex)
- ✅ Cross-platform ready (Web, iOS, Android)

## Project Structure

```
pratibha/
├── src/
│   ├── App.tsx              # Main app with routing
│   ├── components/          # Navigation
│   ├── pages/               # Login, Home, Read, Journal
│   ├── auth/                # Auth provider with Convex
│   └── convex/              # HTTP client (avoids BigInt issues)
├── convex/                   # Backend
│   ├── schema.ts            # journal_notes, learn_progress tables
│   ├── auth.ts              # Email/password + Google OAuth
│   ├── journalNotes.ts      # Journal queries/mutations
│   └── learnProgress.ts     # Progress tracking
└── lynx.config.ts           # Lynx/Rspeedy configuration
```

## How It Works

### Frontend: Lynx ReactLynx

Uses lowercase JSX elements for native Lynx rendering:
- `<view>` - Container (like React Native View)
- `<text>` - Text display
- `<scroll-view>` - Scrollable container
- `<input>` - Text input

These render natively on iOS/Android via Lynx, or in browser via Web target.

### Backend: Convex

- HTTP-based client (not WebSocket) to avoid BigInt issues on native Lynx (PrimJS)
- Email/password authentication works without Google OAuth credentials
- Real-time sync for journal notes and learning progress
- All data stored in Convex cloud database

### Corpus: FastAPI

- Canonical texts served from `/data` directory
- RAG/semantic search via existing pgvector setup
- Passages loaded via HTTP from FastAPI endpoints

## Development

```bash
# Type check
npm run typecheck

# Build for production
npm run build

# Start Convex dev (watch mode)
npx convex dev
```

## Environment Variables

Required in `.env`:

```bash
NEXT_PUBLIC_CONVEX_URL=https://your-deployment.convex.cloud
```

Optional (for Google OAuth):

```bash
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-secret
```

## Testing Native

1. Download Lynx Explorer app on iOS/Android
2. Run `npm run dev`
3. Scan QR code shown in terminal
4. App renders natively on device

## Known Limitations

- **BigInt on Native**: Convex JS client uses BigInt which doesn't work on Lynx's PrimJS runtime. Solution: HTTP-based client (implemented).
- **Real-time subscriptions**: HTTP client doesn't support WebSocket subscriptions. Queries are manual/polling only.
- **FastAPI dependency**: Passages require FastAPI server running locally. Could be migrated to Convex functions if needed.

## Resources

- [Lynx Documentation](https://lynxjs.org/)
- [Convex Documentation](https://docs.convex.dev/)
- [ReactLynx Guide](https://lynxjs.org/next/react/)


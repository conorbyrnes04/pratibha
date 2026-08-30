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
- ✅ Library browser with passages from canonical corpus
- ✅ Journal entries (create, list, sync via Convex)
- ✅ Learning progress tracking
- ✅ Cross-platform ready (Web, iOS, Android)
- ✅ **Social Layer:**
  - Like verses (one per user per verse)
  - Comment on verses with threaded replies (3 levels deep)
  - Share verses to X, Instagram, TikTok with generated cards
  - Content moderation with blocklist and OpenAI API integration
  - Report system for inappropriate comments

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

### Google OAuth Setup (Optional)

To enable "Continue with Google" sign-in:

1. **Create OAuth Client in Google Cloud Console:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Select or create a project
   - Navigate to APIs & Services → Credentials
   - Create OAuth 2.0 Client ID (Web Application type)

2. **Configure Authorized Redirect URI:**
   ```
   https://<your-deployment>.convex.site/api/auth/callback/google
   ```
   Note: Use `.convex.site` (NOT `.convex.cloud`)
   - Find your HTTP Actions URL in Convex dashboard → Settings → URL & Deploy Key
   - Your actions URL will be like `https://fast-horse-123.convex.site`
   - Callback URL is then `https://fast-horse-123.convex.site/api/auth/callback/google`

3. **Add Authorized JavaScript Origins:**
   ```
   http://localhost:3000
   http://localhost:3004
   ```

4. **Set Environment Variables in Convex Dashboard:**
   ```bash
   npx convex env set AUTH_GOOGLE_ID <your-client-id>
   npx convex env set AUTH_GOOGLE_SECRET <your-client-secret>
   ```
   
   Or in Convex dashboard: Settings → Environment Variables

Without these credentials, the app will still work with email/password authentication. The Google sign-in button will show an error if credentials are not configured.

## Testing Native

1. Download Lynx Explorer app on iOS/Android
2. Run `npm run dev`
3. Scan QR code shown in terminal
4. App renders natively on device

## Known Limitations

- **BigInt on Native**: Convex JS client uses BigInt which doesn't work on Lynx's PrimJS runtime. Solution: HTTP-based client (implemented).
- **Real-time subscriptions**: HTTP client doesn't support WebSocket subscriptions. Queries are manual/polling only.
- **FastAPI dependency**: Passages require FastAPI server running locally. Could be migrated to Convex functions if needed.

## Social Layer

See [`SOCIAL.md`](./SOCIAL.md) for full details on the social features.

### Try Social Features

After starting the app and signing in:

1. **Like a verse:** Click the heart icon on any verse (Home or Read page)
2. **Comment:** Post a comment on a verse, reply to comments (up to 3 levels)
3. **Share:** Click "Share" to share to X, Instagram, or TikTok
   - X: Opens share intent with verse text
   - Instagram/TikTok: Downloads verse card image + copies caption
4. **Report:** Click "Report" on inappropriate comments

### Moderation

Comments are automatically filtered before posting:
- Blocklist for profanity and inappropriate content
- OpenAI Moderation API (if `OPENAI_API_KEY` set in `.env`)
- Rate limiting: 10 comments per hour per user
- Length limits: 10-2000 characters
- Auto-hide after 3 reports

First-time commenters see a gentle reminder about right speech.

## Resources

- [Lynx Documentation](https://lynxjs.org/)
- [Convex Documentation](https://docs.convex.dev/)
- [ReactLynx Guide](https://lynxjs.org/next/react/)


# Pratibha Mobile

Expo (SDK 54) app for reading passages, learning paths, journal notes, and chat. Shares TypeScript types with the web app via `@shared` → `web/src/lib`.

## Prerequisites

- Node.js 18+
- [Expo Go](https://expo.dev/go) on your phone (iOS or Android)
- Pratibha **API running and reachable from your phone** (see root [README](../README.md))

Simulator/emulator: default `http://127.0.0.1:8000` is fine. **Physical device:** the API must listen on all interfaces and you must point the app at your computer's LAN IP.

## Install and run

```bash
cd mobile
npm install
npx expo start
```

Open the project in Expo Go (scan QR on iOS, or press `a` / `i` for emulators).

### iPhone on the same Wi‑Fi

1. **Start the API on `0.0.0.0`** (from repo root):

   ```bash
   source .env
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir app
   ```

   Find your LAN IP, e.g. `ipconfig getifaddr en0` (macOS) or your system network settings.

2. **Start Expo on port 8082** (Docker Adminer uses **8081** on the host):

   ```bash
   cd mobile
   EXPO_PUBLIC_API_BASE=http://YOUR_LAN_IP:8000 npx expo start --port 8082
   ```

3. Scan the QR code in Expo Go.

`EXPO_PUBLIC_API_BASE` is baked in at start time. You can also change the API URL later under **Settings** in the app (stored in AsyncStorage).

## Project notes

| Path | Role |
|------|------|
| `app/` | Expo Router screens (tabs: home, read, chat, journal) |
| `lib/api.ts` | Fetch wrapper; reads `EXPO_PUBLIC_API_BASE` or Settings override |
| `lib/storage.ts` | Journal, chat saves, API override key |
| `app.config.ts` | `extra.apiBase` from `EXPO_PUBLIC_API_BASE` |
| `@shared/*` | Aliased to `../web/src/lib` (types, shared helpers) |

iOS allows HTTP to local/dev servers via `NSAllowsArbitraryLoads` in `app.config.ts` — for development only.

## Scripts

```bash
npm start          # expo start
npm run ios        # expo start --ios
npm run android    # expo start --android
```

## Troubleshooting

**"Failed to load verses"** — Wrong API URL. Confirm `curl http://YOUR_LAN_IP:8000/health` from another device on the same network.

**Metro port in use** — Use `--port 8082` if 8081 is taken (e.g. by `docker compose` Adminer).

**Types or imports fail** — Run `npm install` in both `web/` and `mobile/`; mobile imports types from `web/src/lib`.

# AGENTS.md

You are working in Pratibha's experimental Lynx client (`pratibha/`). Next.js in `web/` is the primary UI. Do not treat this app as a replacement for `web/`.

## Read in Advance

Read the docs below in advance to help you understand the library or frameworks this project depends on.

- Lynx: [llms.txt](https://lynxjs.org/llms.txt).
  While dealing with a Lynx task, an agent **MUST** read this doc because it is an entry point of all available docs about Lynx.
- ReactLynx: [https://lynxjs.org/react/introduction.md](https://lynxjs.org/react/introduction.md)
- Elements: [https://lynxjs.org/guide/ui/elements-components.md](https://lynxjs.org/guide/ui/elements-components.md)
- TypeScript: [https://lynxjs.org/rspeedy/typescript](https://lynxjs.org/rspeedy/typescript)

For any Lynx question, prefer Lynx Docs MCP resources over guessing from training data:

1. Read MCP resource `lynx-docs://llms.txt` if the `lynx-docs` server is available.
2. Then fetch the specific guide the task needs.
3. If MCP is unavailable, fetch the `.md` URL on lynxjs.org (replace `.html` with `.md`).

## Commands

Run from this directory (`pratibha/`):

- `npm run dev` — Rspeedy on port 3001 (falls forward if busy). Serves `index.lynx.bundle` for Lynx Explorer.
- `npm run build` — Production Lynx bundle. This is the real compile check.
- `npm run typecheck` — `tsc --noEmit`. `@lynx-js/types` JSX `children` errors on `<view>`/`<text>` are a known scaffold issue; do not "fix" them by switching to HTML `div`/`button`.

Corpus/chat/lexicon/sources need FastAPI on `http://127.0.0.1:8000`. Auth/journal/learn sync need `NEXT_PUBLIC_CONVEX_URL` (loaded from `pratibha/.env` or repo-root `.env`).

## UI rules

- Use Lynx elements only: `<view>`, `<text>`, `<scroll-view>`, `<input>`, `<textarea>`, `<image>`.
- Text must live inside `<text>`. Never put raw strings in `<view>`.
- Events are `bindtap` / `bindinput`, not `onClick` / `onChange`. Read input from `e.detail?.value ?? e.target?.value`.
- No `window` / `document` / `localStorage` on native. Use `src/lib/storage.ts` for KV.
- No Convex WebSocket client (PrimJS BigInt). Use `src/convex/httpClient.ts`.
- Keep the manuscript palette from `src/lib/theme.ts` (amber/gold on `#0a0a0f`). Do not import Tailwind or shadcn from `web/`.

## Layout

```
src/App.tsx                 # in-memory page switch
src/components/Navigation.tsx
src/pages/                  # Home, Read, Chat, Learn, Lexicon, Journal, Sources, Login
src/lib/corpus.ts           # FastAPI client
src/lib/learn.ts            # path/theme catalog + progress
src/lib/learnCatalog.json   # slim extract of web learn tracks/threads
src/lib/storage.ts          # web localStorage / native memory
src/auth/AuthProvider.tsx   # Convex password auth over HTTP
src/convex/httpClient.ts
convex/                     # copy of web Convex functions
```

## Do not

- Replace Lynx JSX with HTML or React Native primitives.
- Point production `NEXT_PUBLIC_API_BASE` at localhost.
- Duplicate the Monad/shadcn kit from `web/`.
- Commit `.env` or Convex tokens.

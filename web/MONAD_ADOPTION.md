# Pratibha × Monad adoption

**Decision:** Graft Monad’s kit + discipline into `web/`. Do **not** greenfield-rescaffold. Keep corpus, routes, auth, Cloudflare deploy, manuscript brand, and sacred-script reading primitives.

Monad’s own skill says not to use it for adding to an existing project — we treat the zip as a **recipe and component reference**, not a `/monad` run against this repo.

---

## Non-goals

- No new Next.js app that replaces `web/`
- No stock IBM Plex as the product face
- No stock neutral OKLCH as the product look (map *our* tokens into Monad slots)
- No dissolving `LayerBlock`, yantra, brand marks, or learn visuals into generic Cards
- No Expo/mobile shadcn port (mobile keeps `@shared` types only)

---

## Phases

### Phase 0 — Guardrails
- [x] Add `web/CLAUDE.md` (or Cursor rule) adapted from Monad: build from kit, style from tokens, escalate new primitives
- [x] List Pratibha-only primitives that require asking before replace (below)

### Phase 1 — Install kit beside current CSS
- [x] Add shadcn `base-nova`, `cn()`, `src/components/ui/*`, `motion`, `sonner`, form stack
- [x] Tailwind v3 → v4 (or staged path); merge `@theme` onto existing variables — **do not** wipe `globals.css`
- [x] Map tokens (table below)
- [x] Verify: `typecheck` + `next build` green (Cloudflare `npm run deploy` when shipping UI)
- [x] No product page visual rewrite yet

### Phase 2 — Chrome → kit
Migrate low-risk surfaces first:
1. Login / account
2. Sitewide `Button` / `Input` (replace `.btn-*` / `.input-field`)
3. `SiteNav` + `AuthMenu`
4. Journal list chrome
5. Chat composer chrome (keep streaming / RAG logic)

### Phase 3 — Reading & study
- Passage: Collapsible/Accordion for layers; keep Original / IAST / script fonts
- Glossary + Lexicon study: kit controls + existing flip/SRS
- Library: Combobox/Command for filters; keep collection art

### Phase 4 — Learn / brand (last)
- Paths, threads, yantra — mostly stay custom
- Optional light theme; optional `/dev/system` showcase (skinned, not stock Plex)

### Phase 5 — Cleanup
- Remove dead CSS once unused
- Document kit vs Pratibha primitives for iOS handoff

---

## Token map

| Monad slot | Pratibha value |
|---|---|
| `--background` | `#090912` |
| `--foreground` | `#f6efe4` |
| `--card` / surfaces | `#171421` / `#211a2a` |
| `--primary` | `#d8a84a` → bright `#f0c979` |
| `--muted-foreground` | `#a89882` |
| `--border` / `--ring` | gold line family |
| `--font-sans` (UI) | Alegreya Sans |
| Reading / headings | Cormorant Garamond |
| Extra (keep) | `--font-devanagari`, Tibetan, Arabic (Noto) |

Default theme: **dark**. Light mode later if wanted.

---

## Component map

### Use Monad / shadcn

| Today | Target |
|---|---|
| `.btn-primary` / `.btn-secondary` | `Button` |
| `.input-field` | `Input` / `Textarea` / `Field` |
| `FilterSelect` | `Select` / `Combobox` |
| `AuthMenu` | `DropdownMenu` |
| Login forms | `Field` + RHF + zod |
| Chat chrome | `Message` / `Bubble` / `InputGroup` |
| Empty states | `Empty` |
| Confirms | `Dialog` / `AlertDialog` |
| Mobile nav | `Sheet` / `Drawer` |
| Status feedback | `sonner` |

### Pratibha-only (escalate before replacing)

- `BrandMark`, `Glyph`, `InkGlyph`, `YantraBreath`
- `ArtImage` / collection art
- `LayerBlock` + source-script treatment
- Learn: `PathTree`, `ThreadsConstellation`, `JourneyMandala`, `StepIntegrationGate`
- `ThemeConstellation`, `CommentaryTeaser`
- Lexicon study flip / SRS core
- `InlineMarkdown` / markdown pipeline

Suggested home over time: `src/components/pratibha/` for these; `src/components/ui/` for the kit.

---

## Target layout

```
web/src/
  components/ui/           # Monad / shadcn
  components/pratibha/     # brand + reading + learn (migrate gradually)
  lib/utils.ts             # cn()
  lib/motion.ts            # motion tokens (optional early)
  app/globals.css          # v4 @theme + Pratibha tokens
  app/**                   # keep all product routes
```

Optional later: `app/dev/system/*` for an internal foundations browser.

---

## Risks

1. Tailwind v4 + OpenNext/Cloudflare — verify deploy every phase
2. Base UI `render` prop (not Radix `asChild`)
3. Generic Card/dashboard look creeping into manuscript pages
4. Font regression losing Noto script stacks

---

## Reference

- Skill zip: local `Monad-System-Skill-main` (SKILL.md, `demo/`, `assets/showcase/`)
- Live Monad demo: https://monad-demo-two.vercel.app
- Do **not** run scaffold Steps 1–4 against this repo; copy patterns and components selectively

# Working in Pratibha web

This app is adopting the Monad / shadcn kit **as a graft**, not a greenfield scaffold.
See `MONAD_ADOPTION.md` for phases. Product content, Cloudflare deploy, auth, and the
manuscript reading experience outrank stock demo aesthetics.

## Build from the kit

When UI chrome is needed (buttons, inputs, menus, dialogs, sheets, toasts), prefer
components in `src/components/ui/` once installed. Compose or extend `cva` variants —
do not hand-roll a second button system.

- **Base UI, not Radix.** Triggers use the `render` prop, never `asChild`.
- **Product pages stay manuscript-first.** Do not turn reading surfaces into dashboards
  of nested Cards. Cards are for interactive containers only (see project frontend rules).

## Style from tokens

- Prefer semantic tokens (`bg-background`, `text-primary`, `border-border`, or
  `var(--accent)`) over raw hex in **new** UI.
- Existing manuscript CSS (`.page-shell`, `.manuscript-card`, `.source-script`, etc.)
  remains valid until Phase 5 cleanup — do not delete it mid-migration.
- **Do not** switch the product face to IBM Plex or stock neutral OKLCH. Pratibha tokens
  (amber/gold on deep manuscript dark + sacred-script Noto stacks) stay authoritative.
- Default theme is **dark**. Light mode is optional and later.

## Pratibha-only primitives — escalate before replacing

Stop and ask before replacing these with stock kit components:

- `BrandMark`, `Glyph`, `InkGlyph`, `YantraBreath`
- `ArtImage` / collection art backdrops
- `LayerBlock` and source-script / Original layer treatment
- Learn: `PathTree`, `ThreadsConstellation`, `JourneyMandala`, `StepIntegrationGate`
- `ThemeConstellation`, `CommentaryTeaser`
- Lexicon study flip card / SRS core (`glossary/study`)
- `InlineMarkdown` / markdown rendering pipeline

These may live under `src/components/pratibha/` over time; until then, treat existing
paths as sacred.

## Stack facts

- Deploy: OpenNext → Cloudflare (`npm run deploy` in `web/`). Git push alone does not
  ship the frontend.
- API: `NEXT_PUBLIC_API_BASE` from `.env.production` (never localhost in prod builds).
- Forms (when added): react-hook-form + zod via `standardSchemaResolver` (not `zodResolver`).
- Toasts: `sonner` + mounted `<Toaster />`.
- Motion: `motion/react` + `src/lib/motion.ts` for shared timings when animating new UI.
- Mobile (Expo) shares `web/src/lib` types only — do not expect `components/ui` on RN.

## When something is missing from the kit

1. Check `src/components/ui/`.
2. Check shadcn (`npx shadcn@latest add <name>`).
3. If still missing — or if a **token** would change — tell the user before inventing a
   new primitive or retinting the whole system.

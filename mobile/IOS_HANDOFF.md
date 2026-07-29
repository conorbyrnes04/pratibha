# Pratibha → iOS handoff (new features)

**Branch / deploy line:** `cursor/study-notes-layer-labels-chuang-cleanup`  
**Reference commit (lexicon study):** `8e009cef`  
**API base:** same production API the web uses  
**Mobile today:** Expo app in `mobile/` — Read / Paths / Chat / Journal. **No Glossary or Lexicon Study UI yet.**

Use this doc when catching the iOS / Expo build up to the latest corpus + lexicon work.

---

## 1. Breaking: Bhagavad Gītā rebuilt (critical)

| | Old | New |
|---|---|---|
| Units | ~12 mega-passages (`bg_md_*`) | **309** verse-scale units |
| IDs | `bhagavad_gita.bg_md_001` … | **`bhagavad_gita.bg_01_01`**, `bg_01_02_04`, `bg_02_47`, … |
| Chunking | Half-chapters | **1–3 ślokas** per unit |

**iOS must:**

- Drop any hardcoded `bg_md_*` bookmarks, deep links, path steps, or caches
- Treat BG like a long sequential text (prev/next matters more)
- Expect ~701 verses covered across 309 units

Resonance / path `passage_id`s that pointed at old hubs were remapped on the backend; anything **client-side** still using old IDs will 404.

---

## 2. New: Shared lexicon API

| Endpoint | Purpose |
|---|---|
| `GET /lexicon?q=&tradition=&limit=` | Browse lemmas (≤500) |
| `GET /lexicon/{id}` | Full lemma: scripts, senses, traps, etymology, related |
| `GET /lexicon/{id}/passages` | Slim occurrence list → open reader |
| `GET /lexicon/study` | **Flashcard decks + cards** (language-separated) |

**Scale:** ~77 lemmas, ~75 study-ready; study payload ≈ **5 decks / 270 cards**.

**Lemma shape (essentials):**

- `scripts`: `devanagari` / `iast` / `greek` / `chinese` / `pinyin` / `arabic` / `latin`
- `senses[]`: `id`, `label`, `short`, `etymology`, `traps[]`, `exemplars[]`
- `maturity`: prefer `strong_draft`+

**Study decks:** `sanskrit` · `greek` · `chinese` · `arabic` · `german`  
**Card modes:** `recognition` · `trap` · `production` (keyed by `sense_id`)

Web stores SRS in `localStorage` (`pratibha.lexicon.srs.v1`). iOS should use **AsyncStorage** (or equivalent) with the same grade model: again / hard / good / easy.

Web routes to mirror: `/glossary`, `/glossary/[id]`, `/glossary/study`.

Shared TypeScript types live under `web/src/lib/` (aliased as `@shared` in mobile):

- `lexiconTypes.ts`
- `lexiconStudyTypes.ts`
- `lexiconStudy.ts` (SRS helpers — reusable or port)

---

## 3. Key Terms are structured + linkable

On many units (BG fully), `pratibha_layers` → `key_terms.items[]` now includes:

```json
{
  "term": "adhikāra (अधिकार)",
  "definition": "…",
  "lemma_id": "adhikara",
  "sense_id": "adhikara.gita"
}
```

Mobile `LayerContent` still renders term + definition only. **Next iOS win:** tap `lemma_id` → glossary detail (same as web `LayerBlock`).

---

## 4. Native-script Originals restored (corpus-wide)

Original layer / `sanskrit` fields now carry real script for major works, including:

- Sanskrit Devanagari (BG, Aṣṭāvakra, Dhammapada, Śāntideva, …)
- Greek (Heraclitus, Dionysius, Phaedo)
- Arabic (Ibn ʿArabī / Balyānī)
- Chinese (Zhuangzi / related)
- Tibetan Uchen (Milarepa, Tilopa)
- MHG / ME where applicable (Eckhart, Cloud)

**iOS:** keep script-aware fonts (Devanagari, Tibetan, Arabic, CJK). Prefer showing **Original** body as-is; IAST stays on the IAST layer when present. BG also exposes `sanskrit_devanagari` / `sanskrit_iast` on the verse object.

---

## 5. Lexicon expansion (Gītā-driven)

New / deepened lemmas useful for search and glossary UI:

`bhakti`, `prakrti`, `purusa`, `guna`, `buddhi`, `ahankara`, `sraddha`, `yajna`, `samkhya`, `sanga`, `adhikara`, plus richer `dharma` / `karma` / `yoga`.

---

## 6. Already on API (context if catching up)

Not unique to this wave, but relevant:

- Auth (Supabase) + journal sync
- Chat cost / rate caps
- Library filters, prev/next in reader
- Learning paths / threads
- Sources / provenance surfaces

---

## Suggested iOS build order

1. **Hard:** migrate off `bg_md_*`; retest BG library + any saved IDs
2. **Fonts:** confirm Original renders for Devanagari / Greek / Tibetan / Arabic / CJK
3. **Key Terms → Glossary:** honor `lemma_id` taps
4. **New screens:** Glossary list + lemma detail (`/lexicon`, `/lexicon/{id}`)
5. **Lexicon Study:** deck picker + flip + local SRS from `/lexicon/study`

---

## Quick QA checklist

- [ ] `GET /verse/bhagavad_gita.bg_02_47` loads; old `bg_md_*` fails cleanly
- [ ] BG Original shows Devanagari, not an English placeholder
- [ ] Key term with `lemma_id` is tappable once glossary ships
- [ ] `GET /lexicon/study` returns 5 decks; Sanskrit session grades persist across relaunch
- [ ] Paths / bookmarks that cited remapped BG IDs still resolve

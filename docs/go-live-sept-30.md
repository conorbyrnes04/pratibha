# Go live — 30 September 2026 (credits refill)

Ship the three new collections so production Listen, Library, and chat all work. Units, covers, and library wiring are already in the repo. What is left is **paid speech**, **commit/deploy**, and **prod verification**.

Works:

| Slug | Shelf | Units | Heroes (`tts_key`) |
|------|--------|------:|--------------------|
| `myths_of_ife` | Yoruba | 28 | 001, 003, 004, 006, 007, 011, 014, 019, 024, 028 |
| `animismo_fetichista` | Candomblé | 28 | 001, 003, 006, 008, 009, 010, 013, 018, 021, 028 |
| `os_africanos_no_brasil` | Candomblé | 28 | 001, 003, 004, 006, 011, 012, 017, 020, 024, 028 |

Voice room for all three: **Yoruba (Olu)**. Needs `ELEVENLABS_API_KEY`. Covers already exist at `web/public/generated/redbook/<slug>.jpg` — do not regenerate unless a cover is missing on prod.

Do **not** `--slice heroes` (bakes every collection). Do **not** compile a LearningTrack unless Conor says go.

When this list is done, delete `.cursor/rules/sept-30-go-live.mdc` and this file (or mark the file done at the top).

---

## 1. Pin hero ids, then bake Listen

`select_listen_heroes.py` has rewritten `data/listen_heroes.json` ids away from `tts_key`. `bake_listen.py --slice work` prefers `tts_key`, so baking is safe if YAML keys are intact. Still rewrite the three `ids` arrays in `listen_heroes.json` to the table above before baking, so the archive index matches the mandala.

```bash
.venv/bin/python scripts/bake_listen.py --slice work --work myths_of_ife
.venv/bin/python scripts/bake_listen.py --slice work --work animismo_fetichista
.venv/bin/python scripts/bake_listen.py --slice work --work os_africanos_no_brasil
```

Each work: 10 verses × English layers (translation / commentary / practice). Skip already-cached speech. Bake publishes the live Listen index — Play can appear on prod without waiting for a frontend deploy, but the YAML must already be on the API host.

Confirm:

```bash
.venv/bin/python -c "
import json
from pathlib import Path
a=json.loads(Path('data/listen_archive.json').read_text())
verses=a.get('verses') or a
for p in ('myths_of_ife','animismo_fetichista','os_africanos'):
    hits=[k for k in verses if p in k]
    print(p, len(hits))
"
```

Expect 10 verse keys per work (more if layer keys are nested). If a bake 402s / quota-errors, stop and retry that work only.

## 2. Commit and ship

Work is currently uncommitted on `feature/monad-phase2-chre` (mixed with other WIP). Split if needed so the three collections can merge without dragging unrelated monad work.

Must land on the branch production deploys:

- `data/canonical/myths_of_ife/`
- `data/canonical/animismo_fetichista/`
- `data/canonical/os_africanos_no_brasil/`
- `web/public/generated/redbook/{myths_of_ife,animismo_fetichista,os_africanos_no_brasil}.jpg`
- library wiring: `app/collection_aliases.py`, `app/sources_registry.py`, `app/tts.py`, `app/data_loader.py`, `web/src/lib/{libraryTomes,collectionLabels,collectionImages,heroQuotes,sumiGlyphs,catalogCache}.ts`, `pratibha/src/lib/heroQuotes.ts`, `scripts/generate_numinos_art.py`
- `data/listen_heroes.json` (pinned ids) + Listen archive updates from the bake

Push → wait for Vercel (`web/`) and Render (`app/`) green.

## 3. Production RAG

New units are invisible to Study chat until prod pgvector is refreshed (`DEPLOY.md`):

```bash
PG_SSL=true \
DATABASE_URL="postgresql://USER:PASSWORD@EXTERNAL_HOST/DBNAME" \
python scripts/ingest_pgvector.py --dir data/canonical
```

Same embedding key/model as the running API.

## 4. Verify on pratibha.agniagama.com

Hard-refresh (catalog cache is `v19`). Sign-in if Manuscript is gated.

- [ ] Sources: *Myths of Ìfẹ̀*, *O Animismo Fetichista*, *Os Africanos no Brasil*
- [ ] Library Yoruba shelf: Myths of Ìfẹ̀ (28) with Johnson — not its own stray shelf
- [ ] Library Candomblé shelf: both Rodrigues tomes (28 + 28), correct dates
- [ ] Each cover is the Red Book jpg, not a fallback
- [ ] Mandala lines rotate (hero quotes)
- [ ] Open one hero per work → Original + Translation + Commentary + Practice
- [ ] Listen Play on those three heroes (Olu). If missing, API did not pick up the bake/index
- [ ] Chat: ask something that should retrieve Nagô / Ìfẹ̀ / Malê and confirm a new unit is cited
- [ ] Alias boot: no `validate_registered_collections` warnings for the three slugs

## 5. After live (optional, wait for Conor)

Path-designer: living-speech Ìfẹ̀ path (model `the-horse-of-conversation` / `the-sky-is-not-addressed`), 6–11 gates. Rodrigues books are observer documents — supporting only, not their own path. Do not compile TypeScript unless asked.

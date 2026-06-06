# Pratibha Canonical Data

This document describes the **honest state** of the canonical corpus under `data/canonical/`. Run `python scripts/validate_canonical.py` for live counts and provenance warnings.

## Corpus snapshot

| Metric | Count |
|--------|------:|
| Total units | 887 |
| `root_text` | 538 |
| `commentary_text` | 349 |

### By `editorial_maturity`

| Maturity | Count | Meaning |
|----------|------:|---------|
| `strong_draft` | 723 | Default for most collections; human-authored or imported manuscript layers, not necessarily publishable |
| `structural_draft` | 145 | PD-normalized or template-assembled scaffolding; not finished translation/commentary |
| `publishable` | 19 | Human-revised units meeting house editorial standards |

### By collection (`work_id`)

| work_id | Units |
|---------|------:|
| patañjali_yoga_sūtras | 195 |
| heraclitus_fragments | 128 |
| vijnana_bhairava | 112 |
| tao_te_ching | 81 |
| yoga_spandakarika | 52 |
| the_book_of_chuang_tzu | 48 |
| siva_sutra | 47 |
| know_yourself_ibn_arabi_balyani | 36 |
| plotinus_enneads | 32 |
| astavakra_gita | 31 |
| isavasya_upanishad | 24 |
| svetasvatara_upanishad | 22 |
| pratyabhijnahrdayam | 21 |
| tantrasara | 19 |
| mandukya_upanishad_and_gaudapada_karika | 16 |
| bhagavad_gita | 12 |
| phaedo_plato | 7 |
| epictetus_works | 3 |
| rumi_mathnawi | 1 |

## Translation and layer honesty

**Do not assume uniform finished-translation quality across the corpus.**

### Translation layers

Units expose Pratibha content through `pratibha_layers` (preferred) and legacy top-level fields (`translation_literal`, `commentary`, etc.). When a `translation` layer exists, it should carry `layer_provenance` describing how the text was produced:

| Provenance pattern | Typical source | Quality |
|--------------------|----------------|---------|
| *(missing)* | Legacy units, most Indic/Greek manuscript imports | Unknown — treat as draft |
| `normalized from Patrick (1889), PD; regex word-modernization, not fresh translation` | Heraclitus pilot | PD derivative, **not** original translation |
| `normalized from Giles (1889), PD; regex word-modernization, not fresh translation` | Zhuangzi pilot | PD derivative, **not** original translation |
| `template-assembled` | Heraclitus/Zhuangzi commentary, key terms, practice | Structural scaffold, not hand-finished prose |
| Hand-authored / manuscript import | Shiva Sutra, VBT, Yoga Sūtras, etc. | Varies; check `editorial_maturity` |

### Commentary and auxiliary layers

Commentary, key terms, resonances, and practice layers follow the same mixed model:

- **Human-revised collections** (e.g. Tantrasara, Yoginīhṛdaya manuscript imports marked `publishable`) use author-written layers.
- **Philological pilot batches** (Heraclitus, Zhuangzi) use template-assembled commentary and practice, flagged `structural_draft`.
- **Legacy YAML imports** may embed layers only in top-level fields without `pratibha_layers` at all.

### `editorial_maturity` is the gate

| Value | Use in RAG / UI |
|-------|-----------------|
| `publishable` | Safe to treat as finished editorial product |
| `strong_draft` | Usable for exploration; may need rewrite before publication |
| `structural_draft` | Scaffolding only — PD-normalized translation and/or template commentary |
| `needs_rewrite` | Flagged for revision |

The app loader and ingest scripts respect `editorial_maturity` filters. Default ingestion should not treat `structural_draft` units as publishable translations.

## Public-domain normalization (copyright guardrail)

Scripts under `scripts/philological_lib.py` and `scripts/philological_enrich.py` perform **regex word-modernization** on verified public-domain translations only (Patrick 1889, Giles 1889). Applying the same technique to in-copyright translations is a copyright violation and must not be done.

PD source files are fetched or copied via `scripts/fetch_pd_sources.py`; each `COPIES` entry documents its PD basis (year, Gutenberg ID, or archive URL).

## Validation

```bash
python scripts/validate_canonical.py
```

The validator checks schema, category contracts, layer order, and **provenance honesty**:

- **WARN** when a `translation` layer lacks `layer_provenance` / `provenance` / `method`
- **ERROR** when `editorial_maturity: publishable` but translation provenance indicates automated normalization or template assembly

## Directory layout

```
data/
├── canonical/           # One .yml per unit; index.jsonl at root
│   ├── heraclitus_fragments/
│   ├── patañjali_yoga_sūtras/
│   └── …
├── raw_texts/           # Source manuscripts, PDFs, PD anchor texts
│   └── pd/              # Verified public-domain copies (see fetch_pd_sources.py)
└── yaml/                # Pipeline / legacy YAML (feeds canonicalize_texts.py)
```

See also `references/editorial-standards.md` for the house content bar on finished units.

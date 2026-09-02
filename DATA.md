# Data Pipeline

This document explains how texts move from source material to the queryable corpus.

---

## The Three Directories

```
data/
├── raw_texts/      ← Stage 1: Source manuscripts (Pratibhā MD format + plain text)
├── yaml/           ← Stage 2: Per-script YAML output (intermediate, not ingested)
├── canonical/      ← Stage 3: Validated, enriched units (source of truth)
└── reports/        ← Quality reports from enrichment runs
```

**`canonical/` is the source of truth.** This is what the app loads, what gets ingested into pgvector, and what `validate_canonical.py` checks. The other directories are pipeline stages.

### raw_texts/

Source manuscripts in Pratibhā MD format — the seven-layer scholarly annotation (Original, IAST, Translation, Commentary, Key Terms, Cross-Tradition Resonances, Practice). These are the human-authored master documents. Some are plain-text extractions from EPUBs or PDFs that haven't yet been run through the full Pratibhā format.

### yaml/

Intermediate YAML files produced by the conversion scripts (`*_md_to_yaml.py`, `*_epub_to_yaml.py`, etc.). Each script reads a source and outputs structured YAML. These files may have inconsistent schemas depending on the source — they are **not** the final format.

### canonical/

The validated output. Each collection lives in its own directory:

```
data/canonical/
├── siva_sutra/                          (47 units)
├── vijnana_bhairava/                    (112 units)
├── yoga_spandakarika/                   (52 units)
├── pratyabhijnahrdayam/                 (21 units)
├── astavakra_gita/                      (31 units)
├── bhagavad_gita/                       (12 units)
├── isavasya_upanishad/                  (24 units)
├── svetasvatara_upanishad/              (22 units)
├── mandukya_upanishad_and_gaudapada_karika/  (16 units)
├── heraclitus_fragments/                (128 units)
├── epictetus_works/                     (3 units)
├── phaedo_plato/                        (7 units)
├── tao_te_ching/                        (4 units)
├── the_book_of_chuang_tzu/             (48 units)
├── know_yourself_ibn_arabi_balyani/     (36 units)
└── senegalese_animism/                  (10 units)
```

Each `.yml` file is one unit — a single verse, sūtra, fragment, passage, or chapter.

---

## Canonical YAML Schema

Every canonical unit is a flat YAML file with these fields:

```yaml
# Identity
source_file: data/yaml/siva_sutra/SS_I.1.yaml    # where this was converted from
source_id: SS_I.1
category: root_text                                # root_text | commentary_text
work_id: siva_sutra                                # collection identifier
work_title: Siva Sutra
unit_id: siva_sutra.ss_i_1                         # globally unique
unit_label: "Consciousness is the Self."
title: "Consciousness is the Self."
unit_type: sutra                                   # sutra | verse | fragment | passage

# Text layers
sanskrit_devanagari: "चैतन्यमात्मा"
sanskrit_iast: "caitanyam ātmā"
translation_literal: "Consciousness is the Self."
commentary: "The sūtra does not instruct; it states ontological necessity..."
insight: "..."                                     # one-line distillation
practice: "..."                                    # contemplative instruction

# Classification
upaya: ""                                          # śāmbhava | śākta | āṇava (when applicable)
themes: [awareness, consciousness, self, caitanya]
tags: [root_text, siva_sutra, awareness, ...]

# Quality
quality_score: 0                                   # 0–100, from enrichment pipeline

# Provenance (optional)
provenance:
  collection: "Vijnana Bhairava"
  section: "meditation_technique"
  original_id: "yukti_001"
```

### Two categories

- **`root_text`** — primary source material (sūtras, verses, fragments). Required: `translation_literal`.
- **`commentary_text`** — traditional commentary or Pratibhā-authored commentary. Required: `thesis`, `source_excerpt`, `themes`.

---

## The Pipeline

### Adding a new text

```
Source (PDF/EPUB/MD/TXT)
        │
        ▼
  scripts/*_to_yaml.py          ← Extract + structure into YAML
        │
        ▼
  data/yaml/<collection>/       ← Intermediate YAML
        │
        ▼
  scripts/canonicalize_texts.py ← Normalize schema, assign IDs
        │
        ▼
  data/canonical/<collection>/  ← Validated canonical units
        │
        ▼
  scripts/validate_canonical.py ← Check schema compliance
        │
        ▼
  scripts/ingest_pgvector.py    ← Embed + store in PostgreSQL
```

### Enrichment (optional)

`scripts/enrich_yaml_shiva_style.py` uses an LLM to improve commentary, generate themes/tags, and score quality. Enrichment reports are saved to `data/reports/`.

### Validation

```bash
python scripts/validate_canonical.py
```

Checks every `.yml` in `data/canonical/` for:

- Required fields present and non-empty (`category`, `work_id`, `work_title`, `unit_id`, `unit_type`)
- Category-specific requirements (root_text needs `translation_literal`; commentary_text needs `thesis`, `source_excerpt`, `themes`)
- Devanāgarī/IAST consistency (warns if Devanāgarī present but IAST missing)
- Title/body bleed detection (warns if first sentence duplicates the title)

---

## Conversion Scripts

| Script | Source → Output | Collection |
|---|---|---|
| `siva_markdown_to_yaml.py` | MD → YAML | Śiva Sūtra |
| `build_vbt_pratibha_md.py` | MD → YAML | Vijñāna Bhairava |
| `yoga_spandakarika_epub_to_yaml.py` | EPUB → YAML | Spanda-kārikā |
| `pratyabhijnahrdayam_md_to_yaml.py` | MD → YAML | Pratyabhijñāhṛdayam |
| `astavakra_gita_md_to_yaml.py` | MD → YAML | Aṣṭāvakra Gītā |
| `bhagavad_gita_pratibha_md_to_yaml.py` | MD → YAML | Bhagavad Gītā |
| `isavasya_md_to_yaml.py` | MD → YAML | Īśāvāsya Upaniṣad |
| `svetasvatara_md_to_yaml.py` | MD → YAML | Śvetāśvatara Upaniṣad |
| `mandukya_md_to_yaml.py` | MD → YAML | Māṇḍūkya + Gauḍapāda |
| `fragments_epub_to_yaml.py` | EPUB → YAML | Heraclitus |
| `epictetus_works_epub_to_yaml.py` | EPUB → YAML | Epictetus |
| `phaedo_epub_to_yaml.py` | EPUB → YAML | Phaedo |
| `tao_te_ching_epub_to_yaml.py` | EPUB → YAML | Dào Dé Jīng |
| `chuang_tzu_epub_to_yaml.py` | EPUB → YAML | Chuang Tzu |
| `ibn_arabi_know_yourself_epub_to_yaml.py` | EPUB → YAML | Ibn ʿArabī |
| `senegalese_animism_pratibha_md_to_yaml.py` | MD → YAML | Senegalese Animism |
| `canonicalize_texts.py` | YAML → Canonical | All collections |
| `enrich_yaml_shiva_style.py` | Canonical → Enriched | LLM enrichment |
| `validate_canonical.py` | Canonical → Report | Schema validation |
| `ingest_pgvector.py` | Canonical → pgvector | Embedding + DB |

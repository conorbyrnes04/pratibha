# Provenance checklist for new collections (asteya)

Pratibha is a non-commercial offering to students, so it must be built without
stealing (*asteya*). Every unit must stand on a **public-domain source** or
**original authorship**, and say so explicitly. This checklist is what each new
collection needs before it is "in the library."

Run the audit any time to see what is unstamped:

```bash
.venv/bin/python - <<'PY'
import glob, yaml
def clean(p):
    p=str(p).lower()
    return any(k in p for k in ("public-domain","public domain","adapted from","original","author","rendered from"))
bad=[f for f in glob.glob("data/canonical/*/*.yml")
     if not clean((yaml.safe_load(open(f,encoding="utf-8")) or {}).get("translation_provenance",""))]
print(len(bad), "units missing a translation_provenance string")
for f in bad[:40]: print("  ", f)
PY
```

## Every new unit needs three things

1. **`translation_provenance`** — a string on the unit stating where the English stands (templates below). The structured `provenance:` dict (collection/section/source_reference) is good but is **not** this field; the audit and Sources page read `translation_provenance`.
2. **`sanskrit_iast`** — a real romanization of the source script, **not** `"See Original."` / `"N/A"`. Run `scripts/transliterate.py --collection <slug> --write` (Chinese/Greek/Japanese/Sanskrit/Persian supported).
3. **A `SOURCES` entry** in `app/sources_registry.py` (template below), or the collection won't appear on the Sources page.

## `translation_provenance` string templates

Pick the tier that matches how the English was actually made:

| Tier | When | String |
|---|---|---|
| **pd_render** | English generated afresh from a PD source-language text | `Rendered from the public-domain source (<LANGUAGE>). Study rendering; not a critical edition.` |
| **pd_adapted** | English follows an out-of-copyright translation | `English follows <TRANSLATOR>, <WORK> (<YEAR>, public domain).` |
| **original** | Original translation + commentary authored in Pratibha | `Original translation and commentary by <author>, from the <source>.` |

**Do not** stamp `pd_render` if the English actually tracks a modern copyrighted
translation — re-render it from the source first (see echo-gate below).

## Recommended public-domain anchor per pending collection

All confirmed public domain (author d. > 95 yrs, or pre-1929 publication):

| Collection | Source language | Recommended PD anchor | Suggested tier |
|---|---|---|---|
| **dhammapada** | Pali | F. Max Müller, *The Dhammapada* (SBE vol. 10, 1881) | pd_adapted (Müller) or pd_render (Pali) |
| **marcus_aurelius_meditations** | Koine Greek | George Long, *The Meditations* (1862) | pd_adapted (Long 1862) |
| **katha_upanishad** | Sanskrit | F. Max Müller, SBE vol. 15 (1884) | pd_render (Sanskrit), Müller as reference |
| **brihadaranyaka_upanishad** | Sanskrit | F. Max Müller, SBE vol. 15 (1884) | pd_render (Sanskrit) |
| **mundaka_upanishad** | Sanskrit | F. Max Müller, SBE vol. 15 (1884) | pd_render (Sanskrit) |
| **the_cloud_of_unknowing** | Middle English (anon., 14th c.) | Evelyn Underhill's edition (1912) | pd_render (Middle English) or pd_adapted (Underhill 1912) |
| **parmenides_fragments** | Ancient Greek | John Burnet, *Early Greek Philosophy* (1892); Arthur Fairbanks (1898) | pd_render (Greek) or pd_adapted (Burnet/Fairbanks) |
| **pseudo_dionysius** | Ancient Greek | John Parker, *The Works of Dionysius the Areopagite* (1897–99) | pd_render (Greek) or pd_adapted (Parker 1897) |

> **pseudo_dionysius** currently has no source script and blank translations —
> it needs the Greek (or Parker's PD English) sourced before it can be stamped
> or shipped. Until then it will only load locally (it is untracked in git).

## Echo-gate: compare, never copy

When rendering from a source language, the English must be genuinely independent
of any copyrighted translation. `scripts/render_from_sanskrit.py` runs an
n-gram overlap check against a reference; keep the render only if it **PASSES**
(jaccard low / no long shared runs). A short attributed quotation is fine as an
*appendix credited to a PD translator* — never a copyrighted one. (We removed
125 such copyrighted appendices from Patañjali/Yoginīhṛdaya; do not reintroduce
that pattern.)

## Sources-registry entry template

Add to `SOURCES` in `app/sources_registry.py` (id **must** equal the canonical
folder slug so passage counts resolve):

```python
{
    "id": "marcus_aurelius_meditations",
    "collection": "Marcus Aurelius — Meditations",
    "tradition": "Greek / Roman Stoic",
    "original_work": "Marcus Aurelius, *Ta eis heauton* (Meditations)",
    "anchor_translation": "English follows George Long (1862, public domain)",
    "editorial_note": "…; commentary and study layers are editorial.",
    "license": "public_domain",              # or "original_editorial"
    "provenance_tier": "pd_adapted",         # pd_render | pd_adapted | original
    "status": "in_corpus",
    # "links": [{"label": "...", "url": "https://..."}],
},
```

## One regression to fix

**heraclitus_fragments** lost its `translation_provenance` during the recent
maturation pass — all 128 units now read blank. Restore:

```
English follows George T. W. Patrick, *The Fragments of Heraclitus* (1889, public domain).
```

(12 curated units + the rest from the same Patrick text.)

## Definition of done

A collection is asteya-clean when the audit above reports **0** unstamped units
for it, its `sanskrit_iast` carries real romanization, and it has a
`SOURCES` entry. Then it belongs in the library.

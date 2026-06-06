# Public-domain anchor texts

This folder holds **PD translations and Sanskrit sources** for philological reference. They are **not** wired into the live study corpus by default — use them when building Pratibha units or comparing anchors.

## Layout

```
pd/
  manifest.yml          # catalog: paths, translators, Gutenberg IDs, URLs
  greek/                # Heraclitus (Patrick), Phaedo (Jowett), Plotinus, Epictetus
  chinese/              # Zhuangzi (Giles), Tao Te Ching (Legge)
  indian/               # Bhagavad Gita (Arnold), Yoga Sutras (Dvivedi PDF, GRETIL IAST)
  references/           # (optional) saved notes for SBE / Archive-only texts
```

## Refresh Gutenberg files

```bash
python scripts/fetch_pd_sources.py
```

## Legacy paths

Older scripts used flat files in `data/raw_texts/` (`patrick_heraclitus_1889.txt`, `ChaungTzuRaw`, etc.). Those files are kept; `pd/` is the canonical archive. Parsers in `scripts/pd_anchor_sources.py` prefer `pd/` paths.

## Sell-ready strategy (future)

Keep **Pratibha Translation** as the product voice. Use files here only as attributed reference — not pasted wholesale into study units.

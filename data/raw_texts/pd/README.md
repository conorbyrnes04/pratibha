# Public-domain anchor texts

PD translations and original-language sources for philological reference. **Not** loaded into the live study corpus by default — use them when authoring Pratibha units or comparing anchors.

For how the live corpus works, see the root [README](../../../README.md) (`data/canonical/`). For editorial rules, see [references/editorial-standards.md](../../../references/editorial-standards.md).

## Layout

```
pd/
  manifest.yml          # Catalog: paths, translators, Gutenberg IDs, URLs, status
  greek/                # Heraclitus, Phaedo, Plotinus, Epictetus, …
  chinese/              # Zhuangzi, Tao Te Ching
  indian/               # Gita, Yoga Sutras, Upaniṣads (Müller SBE), …
  japanese/             # Dōgen, Hakuin
  tibetan/              # Milarepa (Evans-Wentz 1928)
  persian/              # Rūmī Mathnawī
  …                     # See manifest.yml for full list
  references/           # Optional notes for Archive-only texts
```

## manifest.yml

- Entries **without** `status` are downloaded and present on disk.
- Entries with `status: to_be_sourced` are planned but not yet fetched.

Do not duplicate the manifest here — open [manifest.yml](manifest.yml) for paths, priorities, and sourcing notes.

## Refresh Gutenberg / catalog files

```bash
python scripts/fetch_pd_sources.py
```

## Legacy paths

Older flat files under `data/raw_texts/` (e.g. `patrick_heraclitus_1889.txt`) are kept for compatibility. **`pd/` is the canonical archive.** Parsers in `scripts/pd_anchor_sources.py` prefer `pd/` paths.

## Usage in the product

Pratibha study units use **Pratibha editorial layers** as the product voice. Files here are attributed reference material — not pasted wholesale into published units.

# Staging corpus drafts

Working area for Terra / enrichment batches before promotion into `data/canonical/`.

## Keep
- Folders still under review for promotion (Upaniṣads, MMK, Tantrasāra pilots, etc.)
- `epictetus_real/` — archive of the Carter PD Enchiridion batch (already promoted)

## Removed / do not promote
- `epictetus_ns/` — model-supplied Greek drafts **superseded** by Carter PD units in canonical

## Promoted
- `enrich/yoruba_proverbs/` — layer-split into `data/canonical/yoruba_proverbs/` (commentary, key terms, resonances, practice). Re-ingest only from canonical.

## Rule
Do not ingest staging into pgvector. Only `data/canonical/` is live corpus.

# Pratibha Corpus Audit — Original-Language Text

_Read-only audit of original-language coverage across 1015 canonical units in 28 works (source: `data/canonical/index.jsonl`)._

**Headline:** 614/1015 units (60%) carry complete, language-appropriate original text (Devanagari+IAST for Sanskrit; native script for Greek/Chinese/Persian/Arabic/Tibetan/Japanese/German).

## Per-work coverage

| Work | Lang | Units | Complete | % | Top problem (count) |
|------|------|------:|---------:|--:|---------------------|
| `vijnana_bhairava` | sanskrit | 112 | 0 | 0% | No original text at all (no script, no IAST) (112) |
| `yoga_spandakarika` | sanskrit | 52 | 0 | 0% | No original text at all (no script, no IAST) (52) |
| `know_yourself_ibn_arabi_balyani` | arabic | 36 | 0 | 0% | No original text at all (no script, no IAST) (36) |
| `tantrasara` | sanskrit | 19 | 0 | 0% | No original text at all (no script, no IAST) (19) |
| `bhagavad_gita` | sanskrit | 12 | 0 | 0% | Placeholder / source-language-basis note (no native script) (12) |
| `phaedo_plato` | greek | 12 | 0 | 0% | Placeholder / source-language-basis note (no native script) (12) |
| `shantideva_bodhicaryavatara` | sanskrit | 8 | 0 | 0% | Placeholder / source-language-basis note (no native script) (8) |
| `tilopa_mahamudra` | tibetan | 3 | 0 | 0% | Placeholder / source-language-basis note (no native script) (3) |
| `milarepa_songs` | tibetan | 14 | 1 | 7% | Non-Sanskrit work missing its native source script (7) |
| `heraclitus_fragments` | greek | 128 | 11 | 9% | Non-Sanskrit work missing its native source script (117) |
| `astavakra_gita` | sanskrit | 31 | 22 | 71% | No original text at all (no script, no IAST) (9) |
| `mandukya_upanishad_and_gaudapada_karika` | sanskrit | 16 | 12 | 75% | No original text at all (no script, no IAST) (4) |
| `pratyabhijnahrdayam` | sanskrit | 21 | 20 | 95% | No original text at all (no script, no IAST) (1) |
| `the_book_of_chuang_tzu` | chinese | 66 | 63 | 95% | Placeholder / source-language-basis note (no native script) (3) |
| `patañjali_yoga_sūtras` | sanskrit | 195 | 195 | 100% | — |
| `tao_te_ching` | chinese | 81 | 81 | 100% | — |
| `siva_sutra` | sanskrit | 47 | 47 | 100% | — |
| `plotinus_enneads` | greek | 32 | 32 | 100% | — |
| `isavasya_upanishad` | sanskrit | 24 | 24 | 100% | — |
| `svetasvatara_upanishad` | sanskrit | 22 | 22 | 100% | — |
| `rumi_mathnawi` | persian | 22 | 22 | 100% | — |
| `chāndogya_upaniṣad` | sanskrit | 12 | 12 | 100% | — |
| `meister_eckhart` | german | 12 | 12 | 100% | — |
| `dogen_shobogenzo` | japanese | 12 | 12 | 100% | — |
| `yoginihrdaya` | sanskrit | 11 | 11 | 100% | — |
| `nagarjuna_mulamadhyamakakarika` | sanskrit | 9 | 9 | 100% | — |
| `epictetus_works` | greek | 3 | 3 | 100% | — |
| `heart_sutra` | sanskrit | 3 | 3 | 100% | — |

## Worst offenders (by missing units)

| Work | Lang | Units | Missing/incomplete | Dominant issue |
|------|------|------:|-------------------:|----------------|
| `heraclitus_fragments` | greek | 128 | 117 | Non-Sanskrit work missing its native source script (117) |
| `vijnana_bhairava` | sanskrit | 112 | 112 | No original text at all (no script, no IAST) (112) |
| `yoga_spandakarika` | sanskrit | 52 | 52 | No original text at all (no script, no IAST) (52) |
| `know_yourself_ibn_arabi_balyani` | arabic | 36 | 36 | No original text at all (no script, no IAST) (36) |
| `tantrasara` | sanskrit | 19 | 19 | No original text at all (no script, no IAST) (19) |
| `milarepa_songs` | tibetan | 14 | 13 | Non-Sanskrit work missing its native source script (7) |
| `bhagavad_gita` | sanskrit | 12 | 12 | Placeholder / source-language-basis note (no native script) (12) |
| `phaedo_plato` | greek | 12 | 12 | Placeholder / source-language-basis note (no native script) (12) |
| `astavakra_gita` | sanskrit | 31 | 9 | No original text at all (no script, no IAST) (9) |
| `shantideva_bodhicaryavatara` | sanskrit | 8 | 8 | Placeholder / source-language-basis note (no native script) (8) |
| `mandukya_upanishad_and_gaudapada_karika` | sanskrit | 16 | 4 | No original text at all (no script, no IAST) (4) |
| `the_book_of_chuang_tzu` | chinese | 66 | 3 | Placeholder / source-language-basis note (no native script) (3) |

## Problem classes & representative unit_ids

- **No original text at all (no script, no IAST)** — 233 units. e.g. `astavakra_gita.asg_3_3`, `astavakra_gita.asg_6_1`, `astavakra_gita.asg_sum_01_13_01_20`, `astavakra_gita.asg_sum_02_02_02_07`, `astavakra_gita.asg_sum_02_08_02_16`, `astavakra_gita.asg_sum_08_01_08_04`
- **Non-Sanskrit work missing its native source script** — 124 units. e.g. `heraclitus_fragments.hfr_p003`, `heraclitus_fragments.hfr_p004`, `heraclitus_fragments.hfr_p005`, `heraclitus_fragments.hfr_p006`, `heraclitus_fragments.hfr_p007`, `heraclitus_fragments.hfr_p008`
- **Placeholder / source-language-basis note (no native script)** — 44 units. e.g. `bhagavad_gita.bg_md_001`, `bhagavad_gita.bg_md_002`, `bhagavad_gita.bg_md_003`, `bhagavad_gita.bg_md_004`, `bhagavad_gita.bg_md_005`, `bhagavad_gita.bg_md_006`

## Corpus hygiene — empty / duplicate work directories

These directories under `data/canonical/` contain zero unit files. Several are transliteration/name duplicates of populated works (e.g. `śiva_sūtra` vs `siva_sutra`, `vijñāna_bhairava` vs `vijnana_bhairava`, `chandogya_upanishad` vs `chāndogya_upaniṣad`).


## Prioritized recommendations

1. **Restore original text to the fully-empty Sanskrit works first — this is the largest, highest-value gap.** `vijnana_bhairava` (112 units), `yoga_spandakarika` (52), and `tantrasara` (19) have **no** Devanagari, IAST, or original layer on *any* unit — 183 Sanskrit units missing entirely. These are canonical Śaiva texts with readily available critical editions; ingest Devanagari + IAST in bulk.
2. **Fix malformed Sanskrit `sanskrit_devanagari` fields that actually hold romanized IAST.** `nagarjuna_mulamadhyamakakarika` (9/9) and `heart_sutra` (2/3) store IAST in the Devanagari field, so they read as 'has original' but carry no Devanagari. Move the IAST to the IAST layer and supply real Devanagari.
3. **Replace 'source-language basis' placeholders with real script.** `bhagavad_gita` (12), `shantideva_bodhicaryavatara` (8), `phaedo_plato` (12) and `tilopa_mahamudra` (3) ship notes like '*Source-language basis:* ...' instead of Devanagari/Greek/Tibetan. The Gītā and Phaedo are high-traffic anchor texts and should be prioritized.
4. **Backfill Greek source script for Heraclitus.** `heraclitus_fragments` is the second-largest work (128 units) but only 11 carry Greek script; 117 have no original layer. Even Diels–Kranz fragment text for the attested fragments would close most of this gap. `know_yourself_ibn_arabi_balyani` (36 units) similarly has no Arabic original on any unit.
5. **Resolve corpus-hygiene duplicate directories** (transliteration variants and empty stubs) so language-coverage tooling keys on one canonical work_id per text, and add a `provenance.source_language` field (currently null everywhere) so future audits need not infer language from work_id.

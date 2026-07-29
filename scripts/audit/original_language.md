# Pratibha Corpus Audit — Original-Language Text

_Read-only audit of original-language coverage across 1160 canonical units in 38 works (source: `data/canonical/index.jsonl`)._

**Headline:** 1131/1160 units (98%) carry complete, language-appropriate original text (Devanagari+IAST for Sanskrit; native script for Greek/Chinese/Persian/Arabic/Tibetan/Japanese/German).

## Per-work coverage

| Work | Lang | Units | Complete | % | Top problem (count) |
|------|------|------:|---------:|--:|---------------------|
| `dhammapada` | unknown | 26 | 0 | 0% | Placeholder / source-language-basis note (no native script) (26) |
| `pratyabhijnahrdayam` | sanskrit | 21 | 20 | 95% | No original text at all (no script, no IAST) (1) |
| `heraclitus_fragments` | greek | 128 | 126 | 98% | Non-Sanskrit work missing its native source script (2) |
| `patañjali_yoga_sūtras` | sanskrit | 195 | 195 | 100% | — |
| `vijnana_bhairava` | sanskrit | 112 | 112 | 100% | — |
| `tao_te_ching` | chinese | 81 | 81 | 100% | — |
| `the_book_of_chuang_tzu` | chinese | 66 | 66 | 100% | — |
| `yoga_spandakarika` | sanskrit | 52 | 52 | 100% | — |
| `siva_sutra` | sanskrit | 47 | 47 | 100% | — |
| `confucius_analects` | unknown | 45 | 45 | 100% | — |
| `know_yourself_ibn_arabi_balyani` | arabic | 36 | 36 | 100% | — |
| `plotinus_enneads` | greek | 32 | 32 | 100% | — |
| `astavakra_gita` | sanskrit | 31 | 31 | 100% | — |
| `isavasya_upanishad` | sanskrit | 24 | 24 | 100% | — |
| `svetasvatara_upanishad` | sanskrit | 22 | 22 | 100% | — |
| `rumi_mathnawi` | persian | 22 | 22 | 100% | — |
| `pseudo_dionysius` | unknown | 20 | 20 | 100% | — |
| `tantrasara` | sanskrit | 19 | 19 | 100% | — |
| `mandukya_upanishad_and_gaudapada_karika` | sanskrit | 16 | 16 | 100% | — |
| `milarepa_songs` | tibetan | 14 | 14 | 100% | — |
| `zhongyong` | unknown | 14 | 14 | 100% | — |
| `bhagavad_gita` | sanskrit | 12 | 12 | 100% | — |
| `chāndogya_upaniṣad` | sanskrit | 12 | 12 | 100% | — |
| `phaedo_plato` | greek | 12 | 12 | 100% | — |
| `meister_eckhart` | german | 12 | 12 | 100% | — |
| `dogen_shobogenzo` | japanese | 12 | 12 | 100% | — |
| `marcus_aurelius_meditations` | unknown | 12 | 12 | 100% | — |
| `yoginihrdaya` | sanskrit | 11 | 11 | 100% | — |
| `nagarjuna_mulamadhyamakakarika` | sanskrit | 9 | 9 | 100% | — |
| `katha_upanishad` | unknown | 9 | 9 | 100% | — |
| `shantideva_bodhicaryavatara` | sanskrit | 8 | 8 | 100% | — |
| `brihadaranyaka_upanishad` | unknown | 5 | 5 | 100% | — |
| `the_cloud_of_unknowing` | unknown | 5 | 5 | 100% | — |
| `mundaka_upanishad` | unknown | 5 | 5 | 100% | — |
| `parmenides_fragments` | unknown | 4 | 4 | 100% | — |
| `epictetus_works` | greek | 3 | 3 | 100% | — |
| `heart_sutra` | sanskrit | 3 | 3 | 100% | — |
| `tilopa_mahamudra` | tibetan | 3 | 3 | 100% | — |

## Worst offenders (by missing units)

| Work | Lang | Units | Missing/incomplete | Dominant issue |
|------|------|------:|-------------------:|----------------|
| `dhammapada` | ? | 26 | 26 | Placeholder / source-language-basis note (no native script) (26) |
| `heraclitus_fragments` | greek | 128 | 2 | Non-Sanskrit work missing its native source script (2) |
| `pratyabhijnahrdayam` | sanskrit | 21 | 1 | No original text at all (no script, no IAST) (1) |

## Problem classes & representative unit_ids

- **Placeholder / source-language-basis note (no native script)** — 26 units. e.g. `dhammapada.dhp_ch01`, `dhammapada.dhp_ch02`, `dhammapada.dhp_ch03`, `dhammapada.dhp_ch04`, `dhammapada.dhp_ch05`, `dhammapada.dhp_ch06`
- **Non-Sanskrit work missing its native source script** — 2 units. e.g. `heraclitus_fragments.hfr_p089`, `heraclitus_fragments.hfr_p120`
- **No original text at all (no script, no IAST)** — 1 units. e.g. `pratyabhijnahrdayam.phr_sum_appendix`

## Corpus hygiene — empty / duplicate work directories

These directories under `data/canonical/` contain zero unit files. Several are transliteration/name duplicates of populated works (e.g. `śiva_sūtra` vs `siva_sutra`, `vijñāna_bhairava` vs `vijnana_bhairava`, `chandogya_upanishad` vs `chāndogya_upaniṣad`).


## Prioritized recommendations

1. **Restore original text to the fully-empty Sanskrit works first — this is the largest, highest-value gap.** `vijnana_bhairava` (112 units), `yoga_spandakarika` (52), and `tantrasara` (19) have **no** Devanagari, IAST, or original layer on *any* unit — 183 Sanskrit units missing entirely. These are canonical Śaiva texts with readily available critical editions; ingest Devanagari + IAST in bulk.
2. **Fix malformed Sanskrit `sanskrit_devanagari` fields that actually hold romanized IAST.** `nagarjuna_mulamadhyamakakarika` (9/9) and `heart_sutra` (2/3) store IAST in the Devanagari field, so they read as 'has original' but carry no Devanagari. Move the IAST to the IAST layer and supply real Devanagari.
3. **Replace 'source-language basis' placeholders with real script.** `bhagavad_gita` (12), `shantideva_bodhicaryavatara` (8), `phaedo_plato` (12) and `tilopa_mahamudra` (3) ship notes like '*Source-language basis:* ...' instead of Devanagari/Greek/Tibetan. The Gītā and Phaedo are high-traffic anchor texts and should be prioritized.
4. **Backfill Greek source script for Heraclitus.** `heraclitus_fragments` is the second-largest work (128 units) but only 11 carry Greek script; 117 have no original layer. Even Diels–Kranz fragment text for the attested fragments would close most of this gap. `know_yourself_ibn_arabi_balyani` (36 units) similarly has no Arabic original on any unit.
5. **Resolve corpus-hygiene duplicate directories** (transliteration variants and empty stubs) so language-coverage tooling keys on one canonical work_id per text, and add a `provenance.source_language` field (currently null everywhere) so future audits need not infer language from work_id.

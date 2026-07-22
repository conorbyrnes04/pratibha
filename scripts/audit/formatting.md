# Pratibha Corpus Audit — Formatting & Structural Consistency

_Read-only audit over `data/canonical/index.jsonl` (1015 units, 28 works). Spec: `.cursor/skills/pratibha-md/SKILL.md`._

## 1. Layer Completeness (per work)

Expected layers per unit, in order: Original → IAST → Translation → Commentary → Key Terms → Resonances → Practice.

Counts below = units in that work **missing** each layer (empty layers count as missing).

| work | units | miss orig | miss iast | miss transl | miss comm | miss keyterms | miss reson | miss practice |
|---|---|---|---|---|---|---|---|---|
| patañjali_yoga_sūtras | 195 | 0 | 0 | 0 | 0 | 195 | 195 | 0 |
| heraclitus_fragments | 128 | 117 | 116 | 0 | 0 | 128 | 45 | 0 |
| vijnana_bhairava | 112 | 112 | 112 | 0 | 0 | 112 | 27 | 0 |
| tao_te_ching | 81 | 0 | 81 | 0 | 0 | 81 | 81 | 0 |
| the_book_of_chuang_tzu | 66 | 0 | 66 | 0 | 0 | 66 | 36 | 0 |
| yoga_spandakarika | 52 | 52 | 52 | 0 | 0 | 52 | 4 | 0 |
| siva_sutra | 47 | 0 | 0 | 0 | 0 | 47 | 5 | 0 |
| know_yourself_ibn_arabi_balyani | 36 | 36 | 36 | 0 | 0 | 36 | 9 | 0 |
| plotinus_enneads | 32 | 0 | 0 | 0 | 0 | 32 | 32 | 0 |
| astavakra_gita | 31 | 9 | 9 | 0 | 0 | 31 | 21 | 0 |
| isavasya_upanishad | 24 | 0 | 0 | 0 | 0 | 24 | 7 | 0 |
| rumi_mathnawi | 22 | 0 | 0 | 0 | 0 | 22 | 22 | 0 |
| svetasvatara_upanishad | 22 | 0 | 0 | 0 | 0 | 22 | 22 | 0 |
| pratyabhijnahrdayam | 21 | 1 | 1 | 0 | 0 | 21 | 20 | 0 |
| tantrasara | 19 | 19 | 19 | 19 | 0 | 19 | 17 | 0 |
| mandukya_upanishad_and_gaudapada_karika | 16 | 4 | 4 | 0 | 0 | 16 | 11 | 0 |
| milarepa_songs | 14 | 0 | 0 | 0 | 0 | 14 | 13 | 0 |
| bhagavad_gita | 12 | 0 | 12 | 0 | 0 | 12 | 12 | 0 |
| chāndogya_upaniṣad | 12 | 0 | 0 | 0 | 0 | 12 | 12 | 0 |
| dogen_shobogenzo | 12 | 0 | 0 | 0 | 0 | 12 | 12 | 0 |
| meister_eckhart | 12 | 0 | 0 | 0 | 0 | 12 | 12 | 0 |
| phaedo_plato | 12 | 0 | 12 | 0 | 0 | 12 | 12 | 0 |
| yoginihrdaya | 11 | 0 | 0 | 0 | 0 | 11 | 11 | 0 |
| nagarjuna_mulamadhyamakakarika | 9 | 0 | 0 | 0 | 0 | 9 | 9 | 0 |
| shantideva_bodhicaryavatara | 8 | 0 | 0 | 0 | 0 | 8 | 8 | 0 |
| epictetus_works | 3 | 0 | 3 | 0 | 0 | 3 | 3 | 0 |
| heart_sutra | 3 | 0 | 0 | 0 | 0 | 3 | 3 | 0 |
| tilopa_mahamudra | 3 | 0 | 0 | 0 | 0 | 3 | 3 | 0 |

**Corpus totals (units missing layer):**

- `original`: 350 / 1015 (34.5%)
- `iast`: 523 / 1015 (51.5%)
- `translation`: 19 / 1015 (1.9%)
- `commentary`: 0 / 1015 (0.0%)
- `keyterms`: 1015 / 1015 (100.0%)
- `resonances`: 664 / 1015 (65.4%)
- `practice`: 0 / 1015 (0.0%)


## 2. Buried / Malformed Resonances

- **300** units have cross-tradition resonances pasted into the commentary text with **no** structured `resonances` layer.
  - Examples: astavakra_gita.asg_11_6, astavakra_gita.asg_11_7, astavakra_gita.asg_15_11, astavakra_gita.asg_16_1, astavakra_gita.asg_1_1, astavakra_gita.asg_1_10, astavakra_gita.asg_1_11, astavakra_gita.asg_1_12, astavakra_gita.asg_1_2, astavakra_gita.asg_1_3, astavakra_gita.asg_1_4, astavakra_gita.asg_1_5, astavakra_gita.asg_1_6, astavakra_gita.asg_1_7, astavakra_gita.asg_1_8, astavakra_gita.asg_1_9, astavakra_gita.asg_2_1, astavakra_gita.asg_2_7, astavakra_gita.asg_7_3, astavakra_gita.asg_8_4 …
- **17** units have resonance text in commentary *and* a structured layer (redundant / needs cleanup).
  - Examples: isavasya_upanishad.isa_007, isavasya_upanishad.isa_008, isavasya_upanishad.isa_010, isavasya_upanishad.isa_011, isavasya_upanishad.isa_012, isavasya_upanishad.isa_013, isavasya_upanishad.isa_014, isavasya_upanishad.isa_015, isavasya_upanishad.isa_016, isavasya_upanishad.isa_017, isavasya_upanishad.isa_018, isavasya_upanishad.isa_019, isavasya_upanishad.isa_020, isavasya_upanishad.isa_021, isavasya_upanishad.isa_022 …

## 3. Filler / Templated Content

### Known boilerplate strings

- **practice** filler — **183** units: "Read this passage slowly three times. Pause for one minute and write one sentenc…"
  - e.g. astavakra_gita.asg_11_5, astavakra_gita.asg_15_11, astavakra_gita.asg_15_7, astavakra_gita.asg_3_3, astavakra_gita.asg_6_1, astavakra_gita.asg_sum_01_13_01_20, astavakra_gita.asg_sum_18_96_18_97, astavakra_gita.asg_sum_key_verses_from_chapters_3_7, know_yourself_ibn_arabi_balyani.kys_p001, know_yourself_ibn_arabi_balyani.kys_p002, know_yourself_ibn_arabi_balyani.kys_p003, know_yourself_ibn_arabi_balyani.kys_p004 …
- **commentary** filler — **68** units: "Read this line as a contemplative pointer: pause interpretation for a moment and…"
  - e.g. know_yourself_ibn_arabi_balyani.kys_p001, know_yourself_ibn_arabi_balyani.kys_p002, know_yourself_ibn_arabi_balyani.kys_p008, know_yourself_ibn_arabi_balyani.kys_p009, know_yourself_ibn_arabi_balyani.kys_p018, know_yourself_ibn_arabi_balyani.kys_p023, know_yourself_ibn_arabi_balyani.kys_p024, know_yourself_ibn_arabi_balyani.kys_p025, know_yourself_ibn_arabi_balyani.kys_p026, know_yourself_ibn_arabi_balyani.kys_p027, know_yourself_ibn_arabi_balyani.kys_p028, know_yourself_ibn_arabi_balyani.kys_p035 …

### Top duplicated `commentary` bodies

| count | unit_id (example) | text (truncated) |
|---|---|---|
| 80 | know_yourself_ibn_arabi_balyani.kys_p003 | The emphasis turns inward: clarity grows when attention returns to the knower rather than  |
| 68 | know_yourself_ibn_arabi_balyani.kys_p001 | Read this line as a contemplative pointer: pause interpretation for a moment and let the i |
| 8 | know_yourself_ibn_arabi_balyani.kys_p010 | This line points to a deeper order that is received through attentive listening rather tha |
| 5 | vijnana_bhairava.yukti_001 | The teaching frames change as lawful and intelligible, inviting steadiness within transfor |
| 2 | astavakra_gita.asg_11_7 | Extended Translation: Where is existence, where is non-existence, where is oneness, where  |

### Top duplicated `practice` bodies

| count | unit_id (example) | text (truncated) |
|---|---|---|
| 183 | astavakra_gita.asg_11_5 | Read this passage slowly three times. Pause for one minute and write one sentence about ho |
| 93 | heraclitus_fragments.hfr_p004 | Memorize the fragment in one breath. Recite it once on waking and once before sleep, watch |
| 33 | yoga_spandakarika.sp_02 | Choose one ordinary action today and perform it fully without seeking an outcome. Afterwar |
| 24 | know_yourself_ibn_arabi_balyani.kys_p010 | For 2 minutes, observe inner speech as sound only. Return to the silent awareness that hea |
| 20 | astavakra_gita.asg_sum_02_02_02_07 | Read the excerpt slowly, pause at one striking line, and reflect on its relevance to prese |
| 14 | siva_sutra.ss_ii_13 | Sit for 3 minutes with natural breathing. At each inhale and exhale, notice awareness befo |
| 12 | dogen_shobogenzo.dog_001 | Read the passage once slowly aloud. Sit three minutes without using it to improve a self-s |
| 10 | heraclitus_fragments.hfr_p003 | Before arguing a point today, pause and write one sentence you hold as obvious — then ask  |

### Top duplicated `insight` bodies

| count | unit_id (example) | text (truncated) |
|---|---|---|
| 59 | vijnana_bhairava.yukti_003 | The emphasis turns inward: clarity grows when attention returns to the knower rather than  |
| 41 | vijnana_bhairava.yukti_002 | Read this line as a contemplative pointer: pause interpretation for a moment and let the i |
| 5 | vijnana_bhairava.yukti_001 | The teaching frames change as lawful and intelligible, inviting steadiness within transfor |
| 5 | vijnana_bhairava.yukti_004 | This line points to a deeper order that is received through attentive listening rather tha |
| 2 | astavakra_gita.asg_11_5 | *Cintā* — worry, anxious thought, rumination — is named as the sole generator of suffering |
| 2 | astavakra_gita.asg_11_7 | Extended Translation: Where is existence, where is non-existence, where is oneness, where  |

## 4. Field Consistency

- **commentary == insight** (verbatim): 112 units. e.g. siva_sutra.ss_iii_12, vijnana_bhairava.yukti_001, vijnana_bhairava.yukti_002, vijnana_bhairava.yukti_003, vijnana_bhairava.yukti_004, vijnana_bhairava.yukti_005, vijnana_bhairava.yukti_006, vijnana_bhairava.yukti_007, vijnana_bhairava.yukti_008, vijnana_bhairava.yukti_009
- **translation_literal == translation layer body** (only content): 996 units. e.g. astavakra_gita.asg_11_5, astavakra_gita.asg_11_6, astavakra_gita.asg_11_7, astavakra_gita.asg_15_11, astavakra_gita.asg_15_7, astavakra_gita.asg_16_1, astavakra_gita.asg_1_1, astavakra_gita.asg_1_10, astavakra_gita.asg_1_11, astavakra_gita.asg_1_12
  - _Note: near-universal (98%) — the `Pratibha Translation` layer merely mirrors `translation_literal`, i.e. no distinct interpretive translation exists separate from the literal one._
- **Layer order deviations** (core layers out of spec order): 351 units.
  - 254×  `translation → commentary → practice → resonances`  (e.g. astavakra_gita.asg_6_1)
  - 65×  `original → iast → translation → commentary → practice → resonances`  (e.g. astavakra_gita.asg_11_5)
  - 30×  `original → translation → commentary → practice → resonances`  (e.g. the_book_of_chuang_tzu.ctz_001)
  - 2×  `commentary → practice → resonances`  (e.g. tantrasara.ts_006)
- **Appendix field/layer mismatch**: 0 units.

## 5. Corpus Hygiene — Duplicate / Orphan Works

- Directories under `data/canonical/`: 42; work_ids in index: 28.

### Near-duplicate / variant-spelling directory clusters

Each cluster groups transliteration variants (diacritics, sh/s, doubled letters, long-name variants). `(N yml)` = files present; canonical = the populated one.

- `vijnana_bhairava` (112 yml) ← canonical; `vijnana_bhairava_yuktis` (0 yml); `vijñāna_bhairava` (0 yml)
- `yoga_spandakarika` (52 yml) ← canonical; `yoga_spandakarika_the_sacred_texts_at_the_origins_of` (0 yml)
- `siva_sutra` (47 yml) ← canonical; `shiva_sutra` (0 yml); `śiva_sūtra` (0 yml)
- `tantrasara` (19 yml) ← canonical; `tantrasara_sample` (0 yml)
- `chāndogya_upaniṣad` (12 yml) ← canonical; `chandogya_upanishad` (0 yml)

### Orphan / empty directories

- Empty dirs (0 yml files) — **14**: `chandogya_upanishad`, `know_yourself_an_explanation_of_the_oneness_of_being`, `self_realization_manual`, `shiva_sutra`, `tantra_illuminated_the_philosophy_history_and_practice`, `tantrasara_sample`, `the_manual_for_self_realization_112_meditations_of_the`, `the_ubiquitous_siva_somananda_s_sivadrsti_and_his_tantric`, `utpaladeva_philosopher_of_recognition`, `vbt_translation_wallis_2`, `vijnana_bhairava_yuktis`, `vijñāna_bhairava`, `yoga_spandakarika_the_sacred_texts_at_the_origins_of`, `śiva_sūtra`
- Dirs not present as work_id in index — **14**: `chandogya_upanishad`, `know_yourself_an_explanation_of_the_oneness_of_being`, `self_realization_manual`, `shiva_sutra`, `tantra_illuminated_the_philosophy_history_and_practice`, `tantrasara_sample`, `the_manual_for_self_realization_112_meditations_of_the`, `the_ubiquitous_siva_somananda_s_sivadrsti_and_his_tantric`, `utpaladeva_philosopher_of_recognition`, `vbt_translation_wallis_2`, `vijnana_bhairava_yuktis`, `vijñāna_bhairava`, `yoga_spandakarika_the_sacred_texts_at_the_origins_of`, `śiva_sūtra`
- work_ids in index with no matching dir: none

**Suggested consolidation (empty orphan → canonical home, name-matched):**

- `chandogya_upanishad` (0 yml) → merge/delete in favor of `chāndogya_upaniṣad` (12 yml)
- `shiva_sutra` (0 yml) → merge/delete in favor of `siva_sutra` (47 yml)
- `tantrasara_sample` (0 yml) → merge/delete in favor of `tantrasara` (19 yml)
- `vijnana_bhairava_yuktis` (0 yml) → merge/delete in favor of `vijnana_bhairava` (112 yml)
- `vijñāna_bhairava` (0 yml) → merge/delete in favor of `vijnana_bhairava` (112 yml)
- `yoga_spandakarika_the_sacred_texts_at_the_origins_of` (0 yml) → merge/delete in favor of `yoga_spandakarika` (52 yml)
- `śiva_sūtra` (0 yml) → merge/delete in favor of `siva_sutra` (47 yml)

**Empty orphans with no name match — likely content-level duplicates / legacy dirs (editorial judgement needed):**

- `know_yourself_an_explanation_of_the_oneness_of_being` (0 yml) → likely related to know_yourself_ibn_arabi_balyani (same Balyāni treatise)
- `self_realization_manual` (0 yml) → likely related to vijnana_bhairava / the_manual_for_self_realization_112... (same 112 meditations)
- `tantra_illuminated_the_philosophy_history_and_practice` (0 yml) → likely related to tantrasara (Tantra Illuminated — secondary/overview work)
- `the_manual_for_self_realization_112_meditations_of_the` (0 yml) → likely related to vijnana_bhairava / self_realization_manual (112 dhāraṇās = VBT)
- `the_ubiquitous_siva_somananda_s_sivadrsti_and_his_tantric` (0 yml) → likely related to siva_sutra / pratyabhijnahrdayam (Somānanda Śivadṛṣṭi — Pratyabhijñā lineage)
- `utpaladeva_philosopher_of_recognition` (0 yml) → likely related to pratyabhijnahrdayam (Utpaladeva / Pratyabhijñā recognition school)
- `vbt_translation_wallis_2` (0 yml) → likely related to vijnana_bhairava (VBT = Vijñāna Bhairava Tantra, Wallis translation)

## Prioritized Fixes

1. **Key Terms layer is absent corpus-wide** (1015/1015 units). Either the extractor never emits `kind=='keyterms'` or the field is unpopulated — fix the pipeline so Key Terms are generated and structured.
2. **Backfill structured resonances** for the 664 units missing a `resonances` layer, starting with the 300 where resonances are already written but trapped inside commentary prose — migrate those out first.
3. **Replace templated filler** — the single most common boilerplate string covers 183 units; regenerate real, passage-specific practice/commentary for these.
4. **De-duplicate commentary/insight** — 112 units copy commentary verbatim into `insight`; derive a distinct one-line insight or drop the field.
5. **Consolidate 7 empty variant/orphan directories** (diacritic & sh/s spellings, long-name duplicates) into their canonical work_id to stop split provenance and confusion.
6. **Normalize layer order** in 351 units to the spec sequence (practice currently precedes resonances in many units).

# Pratibha Corpus Audit — Titles & Thematic Shallowness

Read-only audit of `data/canonical/index.jsonl` — **1015 units across 28 works**.
Spec reference: `.cursor/skills/pratibha-md/SKILL.md` (Title = thematic claim; Commentary >= 150 words, claim-led).

## Executive Summary

- **Bare-reference titles** (verse/section pointers, not thematic claims): **210 / 1015 (20.7%)**
- **Verbatim-passage titles** (title is the passage sentence, not a distilled claim): **190 (18.7%)**
- **Sub-150-word commentaries** (below spec minimum): **422 (41.6%)**
- **Commentary == insight** (no development beyond the one-line insight): **112**
- **Boilerplate/templated commentaries**: **161**
- **Units with <=1 theme**: **176 (17.3%)** (0 themes: 51)
- **Theme vocabulary**: 252 distinct themes, 149 used only once

## 1. Titles — Bare-Reference & Verbatim (per work)

| Work | Units | Bare titles | Bare % | Verbatim titles | Verbatim % |
|------|------:|------------:|-------:|----------------:|-----------:|
| know_yourself_ibn_arabi_balyani | 36 | 36 | 100% | 0 | 0% |
| vijnana_bhairava | 112 | 111 | 99% | 0 | 0% |
| siva_sutra | 47 | 0 | 0% | 46 | 98% |
| pratyabhijnahrdayam | 21 | 20 | 95% | 0 | 0% |
| heraclitus_fragments | 128 | 0 | 0% | 105 | 82% |
| isavasya_upanishad | 24 | 18 | 75% | 0 | 0% |
| yoga_spandakarika | 52 | 0 | 0% | 39 | 75% |
| astavakra_gita | 31 | 23 | 74% | 0 | 0% |
| mandukya_upanishad_and_gaudapada_karika | 16 | 2 | 12% | 0 | 0% |
| bhagavad_gita | 12 | 0 | 0% | 0 | 0% |
| chāndogya_upaniṣad | 12 | 0 | 0% | 0 | 0% |
| epictetus_works | 3 | 0 | 0% | 0 | 0% |
| heart_sutra | 3 | 0 | 0% | 0 | 0% |
| milarepa_songs | 14 | 0 | 0% | 0 | 0% |
| nagarjuna_mulamadhyamakakarika | 9 | 0 | 0% | 0 | 0% |
| patañjali_yoga_sūtras | 195 | 0 | 0% | 0 | 0% |
| phaedo_plato | 12 | 0 | 0% | 0 | 0% |
| plotinus_enneads | 32 | 0 | 0% | 0 | 0% |
| shantideva_bodhicaryavatara | 8 | 0 | 0% | 0 | 0% |
| svetasvatara_upanishad | 22 | 0 | 0% | 0 | 0% |
| tantrasara | 19 | 0 | 0% | 0 | 0% |
| tao_te_ching | 81 | 0 | 0% | 0 | 0% |
| the_book_of_chuang_tzu | 66 | 0 | 0% | 0 | 0% |
| tilopa_mahamudra | 3 | 0 | 0% | 0 | 0% |
| yoginihrdaya | 11 | 0 | 0% | 0 | 0% |
| meister_eckhart | 12 | 0 | 0% | 0 | 0% |
| dogen_shobogenzo | 12 | 0 | 0% | 0 | 0% |
| rumi_mathnawi | 22 | 0 | 0% | 0 | 0% |

### Worst works for bare titles — examples

- **know_yourself_ibn_arabi_balyani** — 36/36 (100%): `know_yourself_ibn_arabi_balyani.kys_p001`, `know_yourself_ibn_arabi_balyani.kys_p002`, `know_yourself_ibn_arabi_balyani.kys_p003`, `know_yourself_ibn_arabi_balyani.kys_p004`
- **vijnana_bhairava** — 111/112 (99%): `vijnana_bhairava.yukti_001`, `vijnana_bhairava.yukti_002`, `vijnana_bhairava.yukti_003`, `vijnana_bhairava.yukti_004`
- **pratyabhijnahrdayam** — 20/21 (95%): `pratyabhijnahrdayam.phr_001`, `pratyabhijnahrdayam.phr_002`, `pratyabhijnahrdayam.phr_003`, `pratyabhijnahrdayam.phr_004`
- **isavasya_upanishad** — 18/24 (75%): `isavasya_upanishad.isa_007`, `isavasya_upanishad.isa_008`, `isavasya_upanishad.isa_009`, `isavasya_upanishad.isa_010`
- **astavakra_gita** — 23/31 (74%): `astavakra_gita.asg_11_5`, `astavakra_gita.asg_11_7`, `astavakra_gita.asg_15_11`, `astavakra_gita.asg_15_7`
- **mandukya_upanishad_and_gaudapada_karika** — 2/16 (12%): `mandukya_upanishad_and_gaudapada_karika.muk_002`, `mandukya_upanishad_and_gaudapada_karika.muk_003`

### Verbatim-passage titles — examples

- **heraclitus_fragments** — 105/128: `heraclitus_fragments.hfr_p003`, `heraclitus_fragments.hfr_p004`, `heraclitus_fragments.hfr_p005`, `heraclitus_fragments.hfr_p006`
- **siva_sutra** — 46/47: `siva_sutra.ss_i_1`, `siva_sutra.ss_i_10`, `siva_sutra.ss_i_11`, `siva_sutra.ss_i_12`
- **yoga_spandakarika** — 39/52: `yoga_spandakarika.sp_01`, `yoga_spandakarika.sp_02`, `yoga_spandakarika.sp_03`, `yoga_spandakarika.sp_04`

Cited example — `heraclitus_fragments.hfr_p125` title: "For the things which are considered mysteries among men, they celebrate sacrilegiously." (the whole passage sentence).

## 2. Thematic Shallowness — Commentary Depth (per work)

| Work | Units | Sub-150w | Sub-150w % | Median cmt words | cmt==insight | boilerplate | Units <=1 theme |
|------|------:|---------:|-----------:|-----------------:|-------------:|------------:|----------------:|
| isavasya_upanishad | 24 | 24 | 100% | 25 | 0 | 0 | 4 |
| know_yourself_ibn_arabi_balyani | 36 | 36 | 100% | 17 | 0 | 35 | 21 |
| vijnana_bhairava | 112 | 111 | 99% | 17 | 111 | 110 | 42 |
| rumi_mathnawi | 22 | 20 | 91% | 122 | 0 | 0 | 0 |
| heraclitus_fragments | 128 | 116 | 91% | 61 | 0 | 0 | 79 |
| siva_sutra | 47 | 42 | 89% | 50 | 1 | 0 | 0 |
| dogen_shobogenzo | 12 | 10 | 83% | 119 | 0 | 0 | 0 |
| yoga_spandakarika | 52 | 31 | 60% | 134 | 0 | 14 | 11 |
| mandukya_upanishad_and_gaudapada_karika | 16 | 5 | 31% | 245 | 0 | 2 | 3 |
| the_book_of_chuang_tzu | 66 | 18 | 27% | 239 | 0 | 0 | 4 |
| astavakra_gita | 31 | 6 | 19% | 218 | 0 | 0 | 5 |
| meister_eckhart | 12 | 1 | 8% | 235 | 0 | 0 | 0 |
| pratyabhijnahrdayam | 21 | 1 | 5% | 180 | 0 | 0 | 0 |
| tao_te_ching | 81 | 1 | 1% | 305 | 0 | 0 | 1 |
| bhagavad_gita | 12 | 0 | 0% | 345 | 0 | 0 | 0 |
| chāndogya_upaniṣad | 12 | 0 | 0% | 372 | 0 | 0 | 0 |
| epictetus_works | 3 | 0 | 0% | 1015 | 0 | 0 | 0 |
| heart_sutra | 3 | 0 | 0% | 507 | 0 | 0 | 0 |
| milarepa_songs | 14 | 0 | 0% | 296 | 0 | 0 | 1 |
| nagarjuna_mulamadhyamakakarika | 9 | 0 | 0% | 458 | 0 | 0 | 0 |
| patañjali_yoga_sūtras | 195 | 0 | 0% | 445 | 0 | 0 | 1 |
| phaedo_plato | 12 | 0 | 0% | 352 | 0 | 0 | 1 |
| plotinus_enneads | 32 | 0 | 0% | 379 | 0 | 0 | 2 |
| shantideva_bodhicaryavatara | 8 | 0 | 0% | 475 | 0 | 0 | 0 |
| svetasvatara_upanishad | 22 | 0 | 0% | 235 | 0 | 0 | 0 |
| tantrasara | 19 | 0 | 0% | 362 | 0 | 0 | 1 |
| tilopa_mahamudra | 3 | 0 | 0% | 495 | 0 | 0 | 0 |
| yoginihrdaya | 11 | 0 | 0% | 557 | 0 | 0 | 0 |

### Thinnest-commentary works — example unit_ids

- **isavasya_upanishad** — 24/24 (100%): `isavasya_upanishad.isa_001`, `isavasya_upanishad.isa_002`, `isavasya_upanishad.isa_003`, `isavasya_upanishad.isa_004`
- **know_yourself_ibn_arabi_balyani** — 36/36 (100%): `know_yourself_ibn_arabi_balyani.kys_p001`, `know_yourself_ibn_arabi_balyani.kys_p002`, `know_yourself_ibn_arabi_balyani.kys_p003`, `know_yourself_ibn_arabi_balyani.kys_p004`
- **vijnana_bhairava** — 111/112 (99%): `vijnana_bhairava.yukti_001`, `vijnana_bhairava.yukti_002`, `vijnana_bhairava.yukti_003`, `vijnana_bhairava.yukti_004`
- **rumi_mathnawi** — 20/22 (91%): `rumi_mathnawi.rum_001`, `rumi_mathnawi.rum_002`, `rumi_mathnawi.rum_003`, `rumi_mathnawi.rum_004`
- **heraclitus_fragments** — 116/128 (91%): `heraclitus_fragments.hfr_p003`, `heraclitus_fragments.hfr_p004`, `heraclitus_fragments.hfr_p005`, `heraclitus_fragments.hfr_p006`
- **siva_sutra** — 42/47 (89%): `siva_sutra.ss_i_10`, `siva_sutra.ss_i_11`, `siva_sutra.ss_i_12`, `siva_sutra.ss_i_13`
- **dogen_shobogenzo** — 10/12 (83%): `dogen_shobogenzo.dog_002`, `dogen_shobogenzo.dog_004`, `dogen_shobogenzo.dog_005`, `dogen_shobogenzo.dog_006`
- **yoga_spandakarika** — 31/52 (60%): `yoga_spandakarika.sp_05`, `yoga_spandakarika.sp_07`, `yoga_spandakarika.sp_08`, `yoga_spandakarika.sp_09`

## 3. Theme-Count Distribution

| # themes | # units | % of corpus |
|---------:|--------:|------------:|
| 0 | 51 | 5.0% |
| 1 | 125 | 12.3% |
| 2 | 120 | 11.8% |
| 3 | 104 | 10.2% |
| 4 | 98 | 9.7% |
| 5 | 114 | 11.2% |
| 6 | 90 | 8.9% |
| 7 | 84 | 8.3% |
| 8 | 229 | 22.6% |

Units with <=1 theme by work (thin tagging):

- **heraclitus_fragments** — 79/128 (62%): `heraclitus_fragments.hfr_p003`, `heraclitus_fragments.hfr_p004`, `heraclitus_fragments.hfr_p006`
- **know_yourself_ibn_arabi_balyani** — 21/36 (58%): `know_yourself_ibn_arabi_balyani.kys_p001`, `know_yourself_ibn_arabi_balyani.kys_p002`, `know_yourself_ibn_arabi_balyani.kys_p006`
- **vijnana_bhairava** — 42/112 (38%): `vijnana_bhairava.yukti_002`, `vijnana_bhairava.yukti_007`, `vijnana_bhairava.yukti_010`
- **yoga_spandakarika** — 11/52 (21%): `yoga_spandakarika.sp_09`, `yoga_spandakarika.sp_11`, `yoga_spandakarika.sp_13`
- **mandukya_upanishad_and_gaudapada_karika** — 3/16 (19%): `mandukya_upanishad_and_gaudapada_karika.muk_001`, `mandukya_upanishad_and_gaudapada_karika.muk_002`, `mandukya_upanishad_and_gaudapada_karika.muk_016`
- **isavasya_upanishad** — 4/24 (17%): `isavasya_upanishad.isa_001`, `isavasya_upanishad.isa_013`, `isavasya_upanishad.isa_018`
- **astavakra_gita** — 5/31 (16%): `astavakra_gita.asg_15_7`, `astavakra_gita.asg_3_3`, `astavakra_gita.asg_6_1`
- **phaedo_plato** — 1/12 (8%): `phaedo_plato.phaedo_md_011`
- **milarepa_songs** — 1/14 (7%): `milarepa_songs.mil_demon_008`
- **plotinus_enneads** — 2/32 (6%): `plotinus_enneads.enn_v_1_03`, `plotinus_enneads.enn_vi_9_02`
- **the_book_of_chuang_tzu** — 4/66 (6%): `the_book_of_chuang_tzu.ctz_009`, `the_book_of_chuang_tzu.ctz_029`, `the_book_of_chuang_tzu.zhuangzi_md_009`
- **tantrasara** — 1/19 (5%): `tantrasara.ts_019`
- **tao_te_ching** — 1/81 (1%): `tao_te_ching.ttc_md_015`
- **patañjali_yoga_sūtras** — 1/195 (1%): `patañjali_yoga_sūtras.ys_3_43`

## 4. Boilerplate / Templated Commentary

Repeated commentary bodies (identical text reused across units) — 5 distinct bodies reused, covering 163 units:

| Count | Commentary body (truncated) |
|------:|------------------------------|
| 80 | The emphasis turns inward: clarity grows when attention returns to the knower rather than the passing content.… |
| 68 | Read this line as a contemplative pointer: pause interpretation for a moment and let the insight disclose itself directly.… |
| 8 | This line points to a deeper order that is received through attentive listening rather than conceptual noise.… |
| 5 | The teaching frames change as lawful and intelligible, inviting steadiness within transformation.… |
| 2 | Extended Translation: Where is existence, where is non-existence, where is oneness, where is duality? What more is there to say? Nothing ari… |

Representative unit_ids for the top boilerplate strings:

- "The emphasis turns inward: clarity grows when attention returns to the knower ra…" — 80 units, e.g. `know_yourself_ibn_arabi_balyani.kys_p003`, `know_yourself_ibn_arabi_balyani.kys_p004`, `know_yourself_ibn_arabi_balyani.kys_p005`, `know_yourself_ibn_arabi_balyani.kys_p006`
- "Read this line as a contemplative pointer: pause interpretation for a moment and…" — 68 units, e.g. `know_yourself_ibn_arabi_balyani.kys_p001`, `know_yourself_ibn_arabi_balyani.kys_p002`, `know_yourself_ibn_arabi_balyani.kys_p008`, `know_yourself_ibn_arabi_balyani.kys_p009`
- "This line points to a deeper order that is received through attentive listening …" — 8 units, e.g. `know_yourself_ibn_arabi_balyani.kys_p010`, `know_yourself_ibn_arabi_balyani.kys_p011`, `know_yourself_ibn_arabi_balyani.kys_p012`, `vijnana_bhairava.yukti_004`
- "The teaching frames change as lawful and intelligible, inviting steadiness withi…" — 5 units, e.g. `vijnana_bhairava.yukti_001`, `vijnana_bhairava.yukti_025`, `vijnana_bhairava.yukti_026`, `vijnana_bhairava.yukti_040`

## 5. Theme Vocabulary Health

- Distinct themes: **252**
- Singleton themes (used exactly once): **149**

Most-used themes:

| Theme | Uses |
|-------|-----:|
| mind | 350 |
| self | 325 |
| awareness | 278 |
| practice | 271 |
| consciousness | 238 |
| breath | 221 |
| attention | 204 |
| action | 195 |
| knowledge | 156 |
| recognition | 102 |
| heart | 86 |
| harmony | 85 |
| way | 84 |
| freedom | 84 |
| soul | 76 |
| meditation | 75 |
| stillness | 72 |
| desire | 67 |
| death | 65 |
| ignorance | 65 |

Sample singleton themes (possible inconsistent/one-off tagging): `abhasana`, `abhimana`, `abhoga`, `ahamkara`, `aikatmya`, `aksagocarah`, `amarsa`, `anna`, `anurupa`, `anusandhana`, `apasu-sakti`, `artha`, `asana`, `asanga`, `asrama`, `atmasat`, `avadhana`, `avarana`, `avaroha`, `avarudha`, `avastha`, `avidya`, `avisista-vidya`, `awe`, `bala`, `bhairava`, `bhati`, `bheda`, `bhokta`, `bhumika`, `bhuta`, `bodha`, `cetana`, `cetya`, `channa`, `christology`, `cidananda`, `citi`, `citivahni`, `citta-vikasa`

## Prioritized Recommendations

1. **Author thematic titles first for the pointer-titled works**: know_yourself_ibn_arabi_balyani (36/36); vijnana_bhairava (111/112); pratyabhijnahrdayam (20/21); isavasya_upanishad (18/24); astavakra_gita (23/31). These have titles that are pure verse/section references (e.g. `Yukti #1`, `Sutra 1`, `Verse 11.5`, `Pearl #1`) and violate the spec's Title rule outright.
2. **Distill verbatim-sentence titles into claims** for: heraclitus_fragments (105); siva_sutra (46); yoga_spandakarika (39). Titles currently copy the passage sentence (e.g. `heraclitus_fragments`, `siva_sutra`, `yoga_spandakarika`) instead of naming the move.
3. **Deepen thinnest commentary first**: isavasya_upanishad (100%); know_yourself_ibn_arabi_balyani (100%); vijnana_bhairava (99%); rumi_mathnawi (91%); heraclitus_fragments (91%). These have the highest share of sub-150-word commentaries.
4. **Replace 161 boilerplate commentaries** (templated strings like "Read this line as a contemplative pointer…" and "The emphasis turns inward…") with claim-led argument; 112 units also have commentary identical to the one-line insight.
5. **Enrich thin theme tagging**: 176 units carry <=1 theme; consolidate the 149 singleton themes and reconcile inconsistent labels to a controlled vocabulary.

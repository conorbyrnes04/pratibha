# Pratibha Corpus Audit — Titles & Thematic Shallowness

Read-only audit of `data/canonical/index.jsonl` — **1015 units across 28 works**.
Spec reference: `.cursor/skills/pratibha-md/SKILL.md` (Title = thematic claim; Commentary >= 150 words, claim-led).

## Executive Summary

- **Bare-reference titles** (verse/section pointers, not thematic claims): **0 / 1015 (0.0%)**
- **Verbatim-passage titles** (title is the passage sentence, not a distilled claim): **0 (0.0%)**
- **Sub-150-word commentaries** (below spec minimum): **454 (44.7%)**
- **Commentary == insight** (no development beyond the one-line insight): **112**
- **Boilerplate/templated commentaries**: **161**
- **Units with <=1 theme**: **37 (3.6%)** (0 themes: 7)
- **Theme vocabulary**: 252 distinct themes, 149 used only once

## 1. Titles — Bare-Reference & Verbatim (per work)

| Work | Units | Bare titles | Bare % | Verbatim titles | Verbatim % |
|------|------:|------------:|-------:|----------------:|-----------:|
| astavakra_gita | 31 | 0 | 0% | 0 | 0% |
| bhagavad_gita | 12 | 0 | 0% | 0 | 0% |
| chāndogya_upaniṣad | 12 | 0 | 0% | 0 | 0% |
| epictetus_works | 3 | 0 | 0% | 0 | 0% |
| heraclitus_fragments | 128 | 0 | 0% | 0 | 0% |
| heart_sutra | 3 | 0 | 0% | 0 | 0% |
| isavasya_upanishad | 24 | 0 | 0% | 0 | 0% |
| know_yourself_ibn_arabi_balyani | 36 | 0 | 0% | 0 | 0% |
| mandukya_upanishad_and_gaudapada_karika | 16 | 0 | 0% | 0 | 0% |
| milarepa_songs | 14 | 0 | 0% | 0 | 0% |
| nagarjuna_mulamadhyamakakarika | 9 | 0 | 0% | 0 | 0% |
| patañjali_yoga_sūtras | 195 | 0 | 0% | 0 | 0% |
| phaedo_plato | 12 | 0 | 0% | 0 | 0% |
| plotinus_enneads | 32 | 0 | 0% | 0 | 0% |
| pratyabhijnahrdayam | 21 | 0 | 0% | 0 | 0% |
| shantideva_bodhicaryavatara | 8 | 0 | 0% | 0 | 0% |
| siva_sutra | 47 | 0 | 0% | 0 | 0% |
| svetasvatara_upanishad | 22 | 0 | 0% | 0 | 0% |
| tantrasara | 19 | 0 | 0% | 0 | 0% |
| tao_te_ching | 81 | 0 | 0% | 0 | 0% |
| the_book_of_chuang_tzu | 66 | 0 | 0% | 0 | 0% |
| tilopa_mahamudra | 3 | 0 | 0% | 0 | 0% |
| vijnana_bhairava | 112 | 0 | 0% | 0 | 0% |
| yoga_spandakarika | 52 | 0 | 0% | 0 | 0% |
| yoginihrdaya | 11 | 0 | 0% | 0 | 0% |
| meister_eckhart | 12 | 0 | 0% | 0 | 0% |
| dogen_shobogenzo | 12 | 0 | 0% | 0 | 0% |
| rumi_mathnawi | 22 | 0 | 0% | 0 | 0% |

### Worst works for bare titles — examples


### Verbatim-passage titles — examples


Cited example — `heraclitus_fragments.hfr_p125` title: "Sacred Rites Profaned By Ignorant Celebration" (the whole passage sentence).

## 2. Thematic Shallowness — Commentary Depth (per work)

| Work | Units | Sub-150w | Sub-150w % | Median cmt words | cmt==insight | boilerplate | Units <=1 theme |
|------|------:|---------:|-----------:|-----------------:|-------------:|------------:|----------------:|
| isavasya_upanishad | 24 | 24 | 100% | 18 | 0 | 0 | 0 |
| know_yourself_ibn_arabi_balyani | 36 | 36 | 100% | 17 | 0 | 35 | 1 |
| vijnana_bhairava | 112 | 111 | 99% | 17 | 111 | 110 | 1 |
| rumi_mathnawi | 22 | 20 | 91% | 122 | 0 | 0 | 0 |
| heraclitus_fragments | 128 | 116 | 91% | 61 | 0 | 0 | 30 |
| siva_sutra | 47 | 42 | 89% | 50 | 1 | 0 | 0 |
| dogen_shobogenzo | 12 | 10 | 83% | 119 | 0 | 0 | 0 |
| pratyabhijnahrdayam | 21 | 15 | 71% | 117 | 0 | 0 | 0 |
| yoga_spandakarika | 52 | 31 | 60% | 134 | 0 | 14 | 2 |
| astavakra_gita | 31 | 17 | 55% | 146 | 0 | 0 | 0 |
| mandukya_upanishad_and_gaudapada_karika | 16 | 5 | 31% | 232 | 0 | 2 | 1 |
| the_book_of_chuang_tzu | 66 | 18 | 27% | 197 | 0 | 0 | 0 |
| svetasvatara_upanishad | 22 | 2 | 9% | 185 | 0 | 0 | 0 |
| meister_eckhart | 12 | 1 | 8% | 235 | 0 | 0 | 0 |
| tao_te_ching | 81 | 6 | 7% | 197 | 0 | 0 | 0 |
| bhagavad_gita | 12 | 0 | 0% | 262 | 0 | 0 | 0 |
| chāndogya_upaniṣad | 12 | 0 | 0% | 260 | 0 | 0 | 0 |
| epictetus_works | 3 | 0 | 0% | 603 | 0 | 0 | 0 |
| heart_sutra | 3 | 0 | 0% | 344 | 0 | 0 | 0 |
| milarepa_songs | 14 | 0 | 0% | 241 | 0 | 0 | 0 |
| nagarjuna_mulamadhyamakakarika | 9 | 0 | 0% | 321 | 0 | 0 | 0 |
| patañjali_yoga_sūtras | 195 | 0 | 0% | 445 | 0 | 0 | 1 |
| phaedo_plato | 12 | 0 | 0% | 266 | 0 | 0 | 0 |
| plotinus_enneads | 32 | 0 | 0% | 272 | 0 | 0 | 0 |
| shantideva_bodhicaryavatara | 8 | 0 | 0% | 340 | 0 | 0 | 0 |
| tantrasara | 19 | 0 | 0% | 362 | 0 | 0 | 1 |
| tilopa_mahamudra | 3 | 0 | 0% | 354 | 0 | 0 | 0 |
| yoginihrdaya | 11 | 0 | 0% | 557 | 0 | 0 | 0 |

### Thinnest-commentary works — example unit_ids

- **isavasya_upanishad** — 24/24 (100%): `isavasya_upanishad.isa_001`, `isavasya_upanishad.isa_002`, `isavasya_upanishad.isa_003`, `isavasya_upanishad.isa_004`
- **know_yourself_ibn_arabi_balyani** — 36/36 (100%): `know_yourself_ibn_arabi_balyani.kys_p001`, `know_yourself_ibn_arabi_balyani.kys_p002`, `know_yourself_ibn_arabi_balyani.kys_p003`, `know_yourself_ibn_arabi_balyani.kys_p004`
- **vijnana_bhairava** — 111/112 (99%): `vijnana_bhairava.yukti_001`, `vijnana_bhairava.yukti_002`, `vijnana_bhairava.yukti_003`, `vijnana_bhairava.yukti_004`
- **rumi_mathnawi** — 20/22 (91%): `rumi_mathnawi.rum_001`, `rumi_mathnawi.rum_002`, `rumi_mathnawi.rum_003`, `rumi_mathnawi.rum_004`
- **heraclitus_fragments** — 116/128 (91%): `heraclitus_fragments.hfr_p003`, `heraclitus_fragments.hfr_p004`, `heraclitus_fragments.hfr_p005`, `heraclitus_fragments.hfr_p006`
- **siva_sutra** — 42/47 (89%): `siva_sutra.ss_i_10`, `siva_sutra.ss_i_11`, `siva_sutra.ss_i_12`, `siva_sutra.ss_i_13`
- **dogen_shobogenzo** — 10/12 (83%): `dogen_shobogenzo.dog_002`, `dogen_shobogenzo.dog_004`, `dogen_shobogenzo.dog_005`, `dogen_shobogenzo.dog_006`
- **pratyabhijnahrdayam** — 15/21 (71%): `pratyabhijnahrdayam.phr_001`, `pratyabhijnahrdayam.phr_002`, `pratyabhijnahrdayam.phr_003`, `pratyabhijnahrdayam.phr_004`

## 3. Theme-Count Distribution

| # themes | # units | % of corpus |
|---------:|--------:|------------:|
| 0 | 7 | 0.7% |
| 1 | 30 | 3.0% |
| 2 | 120 | 11.8% |
| 3 | 107 | 10.5% |
| 4 | 98 | 9.7% |
| 5 | 122 | 12.0% |
| 6 | 113 | 11.1% |
| 7 | 118 | 11.6% |
| 8 | 283 | 27.9% |
| 9 | 17 | 1.7% |

Units with <=1 theme by work (thin tagging):

- **heraclitus_fragments** — 30/128 (23%): `heraclitus_fragments.hfr_p007`, `heraclitus_fragments.hfr_p016`, `heraclitus_fragments.hfr_p018`
- **mandukya_upanishad_and_gaudapada_karika** — 1/16 (6%): `mandukya_upanishad_and_gaudapada_karika.muk_001`
- **tantrasara** — 1/19 (5%): `tantrasara.ts_019`
- **yoga_spandakarika** — 2/52 (4%): `yoga_spandakarika.sp_11`, `yoga_spandakarika.sp_47`
- **know_yourself_ibn_arabi_balyani** — 1/36 (3%): `know_yourself_ibn_arabi_balyani.kys_p001`
- **vijnana_bhairava** — 1/112 (1%): `vijnana_bhairava.yukti_096`
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
| awareness | 400 |
| mind | 369 |
| self | 362 |
| consciousness | 302 |
| practice | 277 |
| knowledge | 222 |
| breath | 222 |
| attention | 213 |
| action | 204 |
| recognition | 149 |
| stillness | 123 |
| meditation | 121 |
| harmony | 104 |
| truth | 102 |
| freedom | 98 |
| transformation | 90 |
| heart | 88 |
| emptiness | 85 |
| way | 84 |
| ignorance | 83 |

Sample singleton themes (possible inconsistent/one-off tagging): `abhasana`, `abhimana`, `abhoga`, `ahamkara`, `aikatmya`, `aksagocarah`, `amarsa`, `anna`, `anurupa`, `anusandhana`, `apasu-sakti`, `artha`, `asana`, `asanga`, `asrama`, `atmasat`, `avadhana`, `avarana`, `avaroha`, `avarudha`, `avastha`, `avidya`, `avisista-vidya`, `awe`, `bala`, `bhairava`, `bhati`, `bheda`, `bhokta`, `bhumika`, `bhuta`, `bodha`, `cetana`, `cetya`, `channa`, `christology`, `cidananda`, `citi`, `citivahni`, `citta-vikasa`

## Prioritized Recommendations

1. **Deepen thinnest commentary first**: isavasya_upanishad (100%); know_yourself_ibn_arabi_balyani (100%); vijnana_bhairava (99%); rumi_mathnawi (91%); heraclitus_fragments (91%). These have the highest share of sub-150-word commentaries.
2. **Replace 161 boilerplate commentaries** (templated strings like "Read this line as a contemplative pointer…" and "The emphasis turns inward…") with claim-led argument; 112 units also have commentary identical to the one-line insight.
3. **Enrich thin theme tagging**: 37 units carry <=1 theme; consolidate the 149 singleton themes and reconcile inconsistent labels to a controlled vocabulary.

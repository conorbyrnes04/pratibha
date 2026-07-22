# Pratibha Corpus Audit — Cross-Tradition Resonances Quality
_Source: `data/canonical/index.jsonl` — 1015 canonical units. Read-only audit; no data modified._

## 1. Coverage distribution
- **Units with a structured `resonances` layer:** 716 / 1015 (70.5%)
- **Total resonance items across corpus:** 1858

| Resonance count | Units | Share |
|---|---|---|
| 0 | 299 | 29.5% |
| 1 | 7 | 0.7% |
| 2-4 | 709 | 69.9% |
| >4 | 0 | 0.0% |

**306 / 1015 units (30.1%) fall below the 2-entry minimum** (0 or 1 resonance). Only 709 (69.9%) sit in the 2-4 target band.

### Per-work coverage
| Work | Units | 0 | 1 | 2-4 | >4 | % below min |
|---|---|---|---|---|---|---|
| Astavakra Gita | 31 | 0 | 0 | 31 | 0 | 0.0% |
| Bhagavad Gita | 12 | 0 | 0 | 12 | 0 | 0.0% |
| Chāndogya Upaniṣad | 12 | 0 | 0 | 12 | 0 | 0.0% |
| Epictetus Works | 3 | 0 | 0 | 3 | 0 | 0.0% |
| Heart Sutra | 3 | 0 | 0 | 3 | 0 | 0.0% |
| Heraclitus Fragments | 128 | 8 | 0 | 120 | 0 | 6.2% |
| Isavasya Upanishad | 24 | 1 | 6 | 17 | 0 | 29.2% |
| Know Yourself (Ibn Arabi / Balyani) | 36 | 1 | 0 | 35 | 0 | 2.8% |
| Mandukya Upanishad and Gaudapada Karika | 16 | 2 | 0 | 14 | 0 | 12.5% |
| Mathnawī | 22 | 22 | 0 | 0 | 0 | 100.0% |
| Meister Eckhart | 12 | 12 | 0 | 0 | 0 | 100.0% |
| Milarepa Songs | 14 | 6 | 0 | 8 | 0 | 42.9% |
| Nagarjuna Mulamadhyamakakarika | 9 | 0 | 0 | 9 | 0 | 0.0% |
| Patañjali Yoga Sūtras | 195 | 195 | 0 | 0 | 0 | 100.0% |
| Phaedo (Plato) | 12 | 5 | 0 | 7 | 0 | 41.7% |
| Plotinus Enneads | 32 | 0 | 0 | 32 | 0 | 0.0% |
| Pratyabhijnahrdayam | 21 | 0 | 0 | 21 | 0 | 0.0% |
| Shantideva Bodhicaryavatara | 8 | 0 | 0 | 8 | 0 | 0.0% |
| Shōbōgenzō | 12 | 12 | 0 | 0 | 0 | 100.0% |
| Siva Sutra | 47 | 3 | 0 | 44 | 0 | 6.4% |
| Svetasvatara Upanishad | 22 | 0 | 0 | 22 | 0 | 0.0% |
| tantrasara | 19 | 17 | 0 | 2 | 0 | 89.5% |
| Tao Te Ching | 81 | 1 | 1 | 79 | 0 | 2.5% |
| The Book of Chuang Tzu | 66 | 1 | 0 | 65 | 0 | 1.5% |
| Tilopa Mahamudra | 3 | 0 | 0 | 3 | 0 | 0.0% |
| Vijnana Bhairava | 112 | 1 | 0 | 111 | 0 | 0.9% |
| Yoga Spandakarika | 52 | 1 | 0 | 51 | 0 | 1.9% |
| Yoginihrdaya | 11 | 11 | 0 | 0 | 0 | 100.0% |

## 2. "Cites titles, not verses" — title-only resonances
- **Resonance items pointing to NO specific passage** (no well-formed `passage_id` AND citation lacks any verse/section/number marker): **224 / 1858** (12.1%).
- `passage_id` present on 1081/1858 items (58.2%); well-formed (`work.unit`) on 1081/1858 (58.2%).

Examples (unit_id — citation — passage_id):
- `astavakra_gita.asg_1_11` — "A Course in Miracles" — passage_id: `(none)`
- `astavakra_gita.asg_1_11` — "William James, *The Varieties of Religious Experience" — passage_id: `(none)`
- `astavakra_gita.asg_1_6` — "Epictetus on *prohairesis" — passage_id: `(none)`
- `astavakra_gita.asg_1_7` — "Zen kōan tradition" — passage_id: `(none)`
- `astavakra_gita.asg_1_8` — "Epictetus" — passage_id: `(none)`
- `astavakra_gita.asg_2_1` — "Zen *kenshō* accounts" — passage_id: `(none)`
- `astavakra_gita.asg_2_7` — "Mūlamadhyamakakārikā" — passage_id: `(none)`
- `astavakra_gita.asg_2_7` — "Meister Eckhart" — passage_id: `(none)`
- `astavakra_gita.asg_7_3` — "Zhuāngzǐ, Cook Ding" — passage_id: `(none)`
- `astavakra_gita.asg_8_4` — "Epictetus on *prohairesis" — passage_id: `(none)`
- `bhagavad_gita.bg_md_002` — "Plato, Republic IV (justice as right order)" — passage_id: `(none)`
- `bhagavad_gita.bg_md_011` — "Buddhist Abhidharma (conditional factors)" — passage_id: `(none)`

## 3. Divergence clause quality
- **Missing (empty) divergence:** 271 items.
- **Trivial divergence** (< 25 chars): 0 items.

Examples missing divergence (unit_id — citation):
- `astavakra_gita.asg_11_6` — "Pratyabhijñāhṛdayam 12"
- `astavakra_gita.asg_11_6` — "Tantrasāra, opening verse"
- `astavakra_gita.asg_11_7` — "Pratyabhijñāhṛdayam 20"
- `astavakra_gita.asg_11_7` — "Dào Dé Jīng ch. 1"
- `astavakra_gita.asg_11_7` — "Wittgenstein, *Tractatus* 7"
- `astavakra_gita.asg_15_11` — "Pratyabhijñāhṛdayam 15"
- `astavakra_gita.asg_15_11` — "Plotinus *Enneads* VI.5"
- `astavakra_gita.asg_15_11` — "Dào Dé Jīng ch. 16"
- `astavakra_gita.asg_16_1` — "Pratyabhijñāhṛdayam 20"
- `astavakra_gita.asg_16_1` — "Dào Dé Jīng ch. 1"

## 4. Depth — theme-only (non-structural) resonances
- **Items flagged as asserting shared THEME rather than structural homology:** **504 / 1858** (27.1%).
  (Heuristic: generic phrasing like "both discuss / both emphasize" without structural-claim vocabulary, or very short bodies lacking a structural claim.)

Examples (unit_id — resonance excerpt):
- `astavakra_gita.asg_11_6` — "bondage is seeing the seer as other; here the threefold formula reverses that error at the level of body-ownership."
- `astavakra_gita.asg_11_7` — "*iti śivam* — the seal-phrase; both texts end in the dissolution of the teaching into the recognition it was pointing toward"
- `astavakra_gita.asg_11_7` — "the Tao that can be named is not the eternal Tao — the text begins where the Dào ends, in the dissolution of all conceptual frames"
- `astavakra_gita.asg_11_7` — ""What we cannot speak about we must pass over in silence" — a convergent endpoint from a radically different intellectual tradition"
- `astavakra_gita.asg_15_11` — "*viśvam ātmasāt karoti* — making the universe one's own; the same ocean-recognition in active voice"
- `astavakra_gita.asg_16_1` — "*iti śivam* — the seal-phrase; both texts end in the dissolution of the teaching into the recognition it was pointing toward"
- `astavakra_gita.asg_16_1` — "the Tao that can be named is not the eternal Tao — the text begins where the Dào ends, in the dissolution of all conceptual frames"
- `astavakra_gita.asg_16_1` — ""What we cannot speak about we must pass over in silence" — a convergent endpoint from a radically different intellectual tradition"

## 5. Integrity — dangling passage_id references
- **`passage_id` values that do NOT resolve to any unit_id in the corpus:** **0** (of 1081 passage_ids present).

## 6. Duplication — templated resonance text
- **Distinct resonance bodies reused across >1 unit:** 49 template strings.
- Together these span **98 unit-occurrences**.

Most-reused resonance texts (reuse count — excerpt — example units):
- **×2** — "*iti śivam* — the seal-phrase; both texts end in the dissolution of the teaching into the recognition it was pointing to…" — e.g. `astavakra_gita.asg_11_7`, `astavakra_gita.asg_16_1`
- **×2** — "the tao that can be named is not the eternal tao — the text begins where the dào ends, in the dissolution of all concept…" — e.g. `astavakra_gita.asg_11_7`, `astavakra_gita.asg_16_1`
- **×2** — ""what we cannot speak about we must pass over in silence" — a convergent endpoint from a radically different intellectua…" — e.g. `astavakra_gita.asg_11_7`, `astavakra_gita.asg_16_1`
- **×2** — "both chapters emphasize the tao as the origin of all phenomena…" — e.g. `tao_te_ching.ttc_md_022`, `tao_te_ching.ttc_md_066`
- **×2** — ""what is night for all beings is wakefulness for the disciplined one." both texts introduce scale-differentiated cogniti…" — e.g. `the_book_of_chuang_tzu.ctz_001`, `the_book_of_chuang_tzu.zhuangzi_md_001`
- **×2** — "both passages use vastness as a practical epistemology: enlarge the containing field and previously rigid limits dissolv…" — e.g. `the_book_of_chuang_tzu.ctz_001`, `the_book_of_chuang_tzu.zhuangzi_md_001`
- **×2** — "cusanus argues finite intellect cannot measure the infinite by finite ratios; zhuangzi's cicada/peng contrast makes the …" — e.g. `the_book_of_chuang_tzu.ctz_001`, `the_book_of_chuang_tzu.zhuangzi_md_001`
- **×2** — "waking and dream are both appearances within consciousness, differentiated functionally but not absolutely. structurally…" — e.g. `the_book_of_chuang_tzu.ctz_002`, `the_book_of_chuang_tzu.zhuangzi_md_002`
- **×2** — "both traditions use dream imagery to expose grasping at fixed identity and fixed world-claims.…" — e.g. `the_book_of_chuang_tzu.ctz_002`, `the_book_of_chuang_tzu.zhuangzi_md_002`
- **×2** — "eckhart's detachment from created forms parallels zhuangzi's release of rigid identification with any single form.…" — e.g. `the_book_of_chuang_tzu.ctz_002`, `the_book_of_chuang_tzu.zhuangzi_md_002`

## 7. Prioritized recommendations
1. **Close the coverage gap first.** 306/1015 units (30.1%) are below the 2-entry minimum — 299 have zero. Generating resonances for zero-coverage units is the single highest-leverage fix, since it unlocks the whole layer rather than polishing existing entries.
2. **Enforce specific-passage citation.** 224 items (12.1%) cite only a work/author with no verse/section anchor. Require a well-formed `passage_id` (currently only 58.2% of items) or a citation containing an explicit locus before a resonance is accepted.
3. **Raise depth from theme to structure.** 504 items read as shared-theme assertions rather than structural homology. Flag generic phrasing in review and require a named structural move (reduction, inversion, mechanism, etc.).
4. **Backfill divergence clauses.** 271 missing + 0 trivial. The divergence clause is mandatory per spec; treat its absence as a hard validation failure.
5. **De-template duplicated resonances.** 49 resonance bodies are copied verbatim across multiple units; rewrite them to the specific passage at hand.

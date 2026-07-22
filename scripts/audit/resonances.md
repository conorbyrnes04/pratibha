# Pratibha Corpus Audit — Cross-Tradition Resonances Quality
_Source: `data/canonical/index.jsonl` — 1015 canonical units. Read-only audit; no data modified._

## 1. Coverage distribution
- **Units with a structured `resonances` layer:** 351 / 1015 (34.6%)
- **Total resonance items across corpus:** 864

| Resonance count | Units | Share |
|---|---|---|
| 0 | 664 | 65.4% |
| 1 | 0 | 0.0% |
| 2-4 | 351 | 34.6% |
| >4 | 0 | 0.0% |

**664 / 1015 units (65.4%) fall below the 2-entry minimum** (0 or 1 resonance). Only 351 (34.6%) sit in the 2-4 target band.

### Per-work coverage
| Work | Units | 0 | 1 | 2-4 | >4 | % below min |
|---|---|---|---|---|---|---|
| Astavakra Gita | 31 | 21 | 0 | 10 | 0 | 67.7% |
| Bhagavad Gita | 12 | 12 | 0 | 0 | 0 | 100.0% |
| Chāndogya Upaniṣad | 12 | 12 | 0 | 0 | 0 | 100.0% |
| Epictetus Works | 3 | 3 | 0 | 0 | 0 | 100.0% |
| Heart Sutra | 3 | 3 | 0 | 0 | 0 | 100.0% |
| Heraclitus Fragments | 128 | 45 | 0 | 83 | 0 | 35.2% |
| Isavasya Upanishad | 24 | 7 | 0 | 17 | 0 | 29.2% |
| Know Yourself (Ibn Arabi / Balyani) | 36 | 9 | 0 | 27 | 0 | 25.0% |
| Mandukya Upanishad and Gaudapada Karika | 16 | 11 | 0 | 5 | 0 | 68.8% |
| Mathnawī | 22 | 22 | 0 | 0 | 0 | 100.0% |
| Meister Eckhart | 12 | 12 | 0 | 0 | 0 | 100.0% |
| Milarepa Songs | 14 | 13 | 0 | 1 | 0 | 92.9% |
| Nagarjuna Mulamadhyamakakarika | 9 | 9 | 0 | 0 | 0 | 100.0% |
| Patañjali Yoga Sūtras | 195 | 195 | 0 | 0 | 0 | 100.0% |
| Phaedo (Plato) | 12 | 12 | 0 | 0 | 0 | 100.0% |
| Plotinus Enneads | 32 | 32 | 0 | 0 | 0 | 100.0% |
| Pratyabhijnahrdayam | 21 | 20 | 0 | 1 | 0 | 95.2% |
| Shantideva Bodhicaryavatara | 8 | 8 | 0 | 0 | 0 | 100.0% |
| Shōbōgenzō | 12 | 12 | 0 | 0 | 0 | 100.0% |
| Siva Sutra | 47 | 5 | 0 | 42 | 0 | 10.6% |
| Svetasvatara Upanishad | 22 | 22 | 0 | 0 | 0 | 100.0% |
| tantrasara | 19 | 17 | 0 | 2 | 0 | 89.5% |
| Tao Te Ching | 81 | 81 | 0 | 0 | 0 | 100.0% |
| The Book of Chuang Tzu | 66 | 36 | 0 | 30 | 0 | 54.5% |
| Tilopa Mahamudra | 3 | 3 | 0 | 0 | 0 | 100.0% |
| Vijnana Bhairava | 112 | 27 | 0 | 85 | 0 | 24.1% |
| Yoga Spandakarika | 52 | 4 | 0 | 48 | 0 | 7.7% |
| Yoginihrdaya | 11 | 11 | 0 | 0 | 0 | 100.0% |

## 2. "Cites titles, not verses" — title-only resonances
- **Resonance items pointing to NO specific passage** (no well-formed `passage_id` AND citation lacks any verse/section/number marker): **27 / 864** (3.1%).
- `passage_id` present on 819/864 items (94.8%); well-formed (`work.unit`) on 819/864 (94.8%).

Examples (unit_id — citation — passage_id):
- `the_book_of_chuang_tzu.ctz_001` — "Vijnana Bhairava Tantra, dharana on sky-like expansion of awareness" — passage_id: `(none)`
- `the_book_of_chuang_tzu.ctz_002` — "Dhammapada / early Buddhist dream analogies for conditioned experience" — passage_id: `(none)`
- `the_book_of_chuang_tzu.ctz_002` — "Meister Eckhart, Sermon on detachment (Abgeschiedenheit)" — passage_id: `(none)`
- `the_book_of_chuang_tzu.ctz_003` — "Epictetus, Enchiridion (discipline of assent and action)" — passage_id: `(none)`
- `the_book_of_chuang_tzu.ctz_003` — "Zen tradition, Dogen's tenzo instructions" — passage_id: `(none)`
- `the_book_of_chuang_tzu.ctz_004` — "Vijnana Bhairava Tantra, dharana on the gap between breaths" — passage_id: `(none)`
- `the_book_of_chuang_tzu.ctz_005` — "Mahayana, Vimalakirti Nirdesa (non-dual skillful means)" — passage_id: `(none)`
- `the_book_of_chuang_tzu.ctz_006` — "Merleau-Ponty, *Phenomenology of Perception* (intercorporeity)" — passage_id: `(none)`
- `the_book_of_chuang_tzu.ctz_006` — "Abhinavagupta, *Tantraloka* (empathetic resonance in rasa theory lineage)" — passage_id: `(none)`
- `the_book_of_chuang_tzu.ctz_006` — "Dogen, *Genjokoan* ("to study the self is to forget the self")" — passage_id: `(none)`
- `the_book_of_chuang_tzu.ctz_007` — "Dogen, *Tenzo Kyokun* (Instructions for the Cook)" — passage_id: `(none)`
- `the_book_of_chuang_tzu.ctz_007` — "Richard Sennett, *The Craftsman* (modern craft ethics)" — passage_id: `(none)`

## 3. Divergence clause quality
- **Missing (empty) divergence:** 0 items.
- **Trivial divergence** (< 25 chars): 0 items.

## 4. Depth — theme-only (non-structural) resonances
- **Items flagged as asserting shared THEME rather than structural homology:** **28 / 864** (3.2%).
  (Heuristic: generic phrasing like "both discuss / both emphasize" without structural-claim vocabulary, or very short bodies lacking a structural claim.)

Examples (unit_id — resonance excerpt):
- `the_book_of_chuang_tzu.ctz_001` — "Both passages use vastness as a practical epistemology: enlarge the containing field and previously rigid limits dissolve."
- `the_book_of_chuang_tzu.ctz_002` — "both traditions use dream imagery to expose grasping at fixed identity and fixed world-claims."
- `the_book_of_chuang_tzu.ctz_003` — "Both traditions stress precision at the point of contact: do not hack at externals; work where agency truly operates."
- `the_book_of_chuang_tzu.ctz_004` — "both traditions train a pause between impression and reaction so freedom is exercised before compulsion."
- `the_book_of_chuang_tzu.ctz_005` — "both show that forms dismissed by conventional judgment can become vehicles of liberation when seen from a wider frame."
- `the_book_of_chuang_tzu.ctz_006` — "both argue that perception includes a pre-reflective participatory grasp of others through shared embodiment and world."
- `the_book_of_chuang_tzu.ctz_006` — "both suggest that loosening fixed self-reference allows things to disclose themselves more directly."
- `the_book_of_chuang_tzu.ctz_007` — "action is performed with inward evenness and without clinging to result; excellence appears as "skill in action.""

## 5. Integrity — dangling passage_id references
- **`passage_id` values that do NOT resolve to any unit_id in the corpus:** **0** (of 819 passage_ids present).

## 6. Duplication — templated resonance text
- **Distinct resonance bodies reused across >1 unit:** 0 template strings.

## 7. Prioritized recommendations
1. **Close the coverage gap first.** 664/1015 units (65.4%) are below the 2-entry minimum — 664 have zero. Generating resonances for zero-coverage units is the single highest-leverage fix, since it unlocks the whole layer rather than polishing existing entries.
2. **Enforce specific-passage citation.** 27 items (3.1%) cite only a work/author with no verse/section anchor. Require a well-formed `passage_id` (currently only 94.8% of items) or a citation containing an explicit locus before a resonance is accepted.
3. **Raise depth from theme to structure.** 28 items read as shared-theme assertions rather than structural homology. Flag generic phrasing in review and require a named structural move (reduction, inversion, mechanism, etc.).

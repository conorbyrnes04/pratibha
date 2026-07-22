# Pratibha Canon Gap Analysis

*Read-only scholarly audit of corpus coverage and recommended additions.*
*Data source: `data/canonical/index.jsonl` (1,015 units, 28 works, 252 distinct themes) + `app/sources_registry.py`. Balance figures are computed; gap recommendations are expert judgment.*

---

## 1. Tradition-Balance Table

Every work grouped into a tradition family (unit counts from `coverage.py`):

| Tradition family | Works | Units | % of corpus |
|---|---|---:|---:|
| **Indic — Kashmir Śaiva / Trika / Tantra** | Vijñāna Bhairava (112), Spandakārikā (52), Śiva Sūtra (47), Pratyabhijñāhṛdayam (21), Tantrasāra (19), Yoginīhṛdaya (11) | **262** | **25.8%** |
| **Indic — Yoga / Sāṃkhya** | Patañjali Yoga Sūtras (195) | **195** | **19.2%** |
| **Indic — Vedānta / Upaniṣad / Advaita** | Aṣṭāvakra Gītā (31), Īśāvāsya (24), Śvetāśvatara (22), Māṇḍūkya+Gauḍapāda (16), Bhagavad Gītā (12), Chāndogya (12) | **117** | **11.5%** |
| **Greek** | Heraclitus (128), Plotinus (32), Plato *Phaedo* (12), Epictetus (3) | **175** | **17.2%** |
| **Chinese — Daoist** | Tao Te Ching (81), Zhuangzi (66) | **147** | **14.5%** |
| **Sufi / Islamic** | Know Yourself / Balyānī–Ibn ʿArabī (36), Rūmī Mathnawī (22) | **58** | **5.7%** |
| **Buddhist (all lineages)** | Milarepa (14), Dōgen (12), Nāgārjuna (9), Śāntideva (8), Heart Sūtra (3), Tilopa (3) | **49** | **4.8%** |
| **Christian mysticism** | Meister Eckhart (12) | **12** | **1.2%** |
| **TOTAL** | 28 works | **1,015** | 100% |

**Consolidated view:** Indic (non-Buddhist) traditions total **574 units = 56.6%** of the entire corpus. The remaining ~43% is split among Greek, Daoist, Sufi, Buddhist, and Christian.

### Theme distribution (corpus-wide)
The dominant themes are meditative-psychological and confirm the Śaiva/Yoga/Advaita center of gravity:

- **Top themes:** mind (350), self (325), awareness (278), practice (271), consciousness (238), breath (221), attention (204), action (195), knowledge (156), recognition (102).
- **Mid-tier:** heart (86), harmony (85), way/dao (84), freedom (84), soul (76), meditation (75), stillness (72), desire (67), death (65), ignorance (65), truth (64).
- **Thin / structurally revealing:** Of 252 themes, ~145 occur only **once** — and nearly all singletons are transliterated Sanskrit technical terms (abhāsana, ahaṃkāra, spanda, mātṛkā, turya, etc.). This means the theme vocabulary itself is **Sanskrit-indexed**: the corpus "thinks" in Śaiva/Yogic categories even when tagging other traditions. English/cross-tradition ethical themes are comparatively starved — **friendship (1), awe (1), humility (3), conflict (1), spirit (1), illumination (1)** — and virtue (55) is carried almost entirely by the Greek and Daoist blocks.

---

## 2. Diagnosis of Imbalance

1. **Indic hegemony.** 56.6% of the corpus is Indic non-Buddhist; a single Śaiva cluster (262) is larger than *all* of Greek (175), *all* of Daoist (147), and roughly 5× the entire Buddhist presence (49).
2. **Patañjali dominance.** 195 units of Yoga Sūtras alone — 19% of the corpus — vs. **3** Epictetus, **3** Heart Sūtra, **3** Tilopa. The single largest work is ~65× the smallest represented works.
3. **Buddhism is thin *and* lopsided.** Only 49 units / 4.8% for the world's largest contemplative tradition. Within that: no Pali/early-Buddhist material at all; Madhyamaka (Nāgārjuna 9 + Śāntideva 8 + Heart 3 = 20) is verse-fragmentary; Zen is one author (Dōgen 12); Vajrayāna is two Kagyü song-collections (Milarepa 14 + Tilopa 3). No Theravāda, no Chan/koan literature, no Pure Land, no Dzogchen, no Yogācāra, no Pali suttas.
4. **Single-witness traditions.** Christianity = **one** author (Eckhart, 12). Stoicism = **one** author, near-token (Epictetus, 3). The Akbarian/Sufi stream rests on essentially one short Ibn-ʿArabī-tradition treatise (Balyānī, 36) plus Rūmī excerpts (22).
5. **Greek is Heraclitus-heavy and draft-inflated.** Heraclitus's 128 is the second-largest work in the corpus, but per the registry only **12 are curated Pratibha-layer** units; the other 116 are `structural_draft`. So Greek "depth" is partly an artifact of import scaffolding, not editorial coverage.
6. **Vedānta is broad but shallow per text.** Six Upaniṣadic/Vedānta works, but the Bhagavad Gītā (arguably the single most influential Indian text globally) sits at only **12** units, and the *principal* Upaniṣads are mostly absent (see §3b).
7. **Whole civilizational streams are absent:** Jewish mysticism (Kabbalah) — zero; Confucian/Neo-Confucian — zero; Indigenous/African/oral wisdom — zero; modern nondual (Ramana, Nisargadatta) — zero.

---

## 3. Identified Gaps

### 3a. Missing traditions / lineages (entirely or nearly absent)

**Buddhist (the biggest structural hole relative to importance):**
- **Pali Canon / early suttas** — *Dhammapada* and select *Majjhima/Saṃyutta* suttas (Fire Sermon, Satipaṭṭhāna, Anattalakkhaṇa). Zero Theravāda presently.
- **Chan / Zen koan literature** — *Gateless Gate* (Mumonkan), *Blue Cliff Record*, or the *Ten Ox-Herding Pictures*. Zen is currently only Dōgen's discursive prose.
- **Dzogchen / Tibetan beyond Kagyü songs** — e.g. Longchenpa, or Garab Dorje's *Three Statements*; also **Shantideva is present but no Atiśa/Lojong** mind-training.
- **Pure Land / devotional Buddhism** and **Yogācāra "mind-only"** — no representation of the devotional or consciousness-only streams.

**Abrahamic mystical:**
- **Jewish mysticism / Kabbalah** — *Zohar* selections, *Sefer Yetzirah*, or Abraham Abulafia. Completely absent.
- **Christian, beyond Eckhart** — Desert Fathers (*Sayings*), **Pseudo-Dionysius** (*Mystical Theology* — the fountainhead of apophatic theology), *The Cloud of Unknowing*, **John of the Cross** (*Dark Night*), **Teresa of Ávila** (*Interior Castle*), Julian of Norwich.
- **Sufi, beyond Balyānī + Rūmī** — **ʿAṭṭār** (*Conference of the Birds*), **Al-Ghazālī** (*Alchemy of Happiness* / *Niche of Lights*), **Ibn ʿArabī's own *Fuṣūṣ al-Ḥikam*** (the Balyānī text is only Akbarian-adjacent), Ḥāfiẓ.

**Greek / Hellenic breadth:**
- **Stoicism** — **Marcus Aurelius** (*Meditations*) and **Seneca** (*Letters*); Epictetus alone (3 units) is a token.
- **Presocratics beyond Heraclitus** — **Parmenides** (Way of Truth) and **Empedocles** (Purifications).
- **Neoplatonism beyond Plotinus** — **Proclus** (*Elements of Theology*).

**Chinese, beyond Daoism:**
- **Confucian / Neo-Confucian** — *Analects*, *Mencius*, *Zhongyong* (Doctrine of the Mean), Wang Yangming. Currently zero non-Daoist Chinese thought.
- **Chan is Chinese-Buddhist and also missing** (see above).

**Other:**
- **Modern nondual** — **Ramana Maharshi** (*Who Am I?* / *Upadeśa Sāram*) and **Nisargadatta** (*I Am That*) — direct heirs to the Advaita/Śaiva material already central here.
- **Indigenous / African / oral traditions** — no representation of non-textual wisdom lineages.

### 3b. Missing key texts / passages *within* represented traditions

- **Bhagavad Gītā** — only 12 units for the tradition's keystone; needs the core arcs: Ch. 2 (Sāṃkhya-yoga), Ch. 3 (karma-yoga), Ch. 6 (dhyāna), Ch. 11 (Viśvarūpa theophany), Ch. 12 (bhakti), Ch. 18 (mokṣa).
- **Principal Upaniṣads absent** — **Kaṭha** (Naciketas & Death — a top-priority gap), **Kena**, **Bṛhadāraṇyaka** ("neti neti," Yājñavalkya), **Muṇḍaka** (two birds; higher/lower knowledge), **Praśna**, **Taittirīya** (five kośas / ānanda-mīmāṃsā). Present set is only Īśā, Śvetāśvatara, Māṇḍūkya, Chāndogya.
- **Zhuangzi Inner Chapters** — corpus has 66 chapter-level units, but should ensure the canonical **Inner Chapters 1–7** (esp. Ch. 2 *Qiwulun* "On the Equality of Things," butterfly dream, Cook Ding, Ch. 6 great-clod-of-earth) are curated rather than bulk-imported.
- **Plotinus** — 32 units cover I.6, V.1, VI.9; the central tractates **IV.8 (Descent of the Soul)** and **V.3 (Knowing Hypostases / self-knowledge)** deserve inclusion.
- **Plato beyond *Phaedo*** — the **Cave / Divided Line (Republic VI–VII)**, the **chariot & the ladder of love (*Phaedrus* / *Symposium*)**, and the *Timaeus* cosmology. These are the myth-bearing passages most cited across mystical traditions.
- **Heraclitus** — deepen the 116 `structural_draft` fragments into curated Pratibha layers before adding new Greek breadth (quality-over-quantity within the block).
- **Nāgārjuna / Śāntideva** — expand beyond the current chapter fragments (MMK 18/24/25; BCA VIII/IX) toward MMK Ch. 1 (dependent origination) and BCA Ch. 6 (patience).

---

## 4. Prioritized Canon Roadmap (top additions)

Ranked by *balance impact × cross-tradition resonance potential*. Each line: what, why, and what it resonates with.

1. **Dhammapada (Pali)** — Fills the total Theravāda void with the single most-loved early-Buddhist text; verse form fits the unit model. *Resonates with:* Aṣṭāvakra (mind as source of suffering — see the existing ASG 11.5 resonance), Yoga Sūtras (citta), Heraclitus (character = fate).
2. **Kaṭha Upaniṣad** — The Naciketas–Death dialogue; keystone principal Upaniṣad currently missing. *Resonates with:* Plato *Phaedo* (death as teacher), Māṇḍūkya (the Self), Gītā (the chariot of the senses — literally shared imagery).
3. **Bhagavad Gītā — expansion (Chs. 2, 6, 11, 12, 18)** — Deepens the most globally influential Indian text from a token 12 units. *Resonates with:* Patañjali (yoga of action/meditation), Rūmī & Eckhart (surrender/bhakti and *Gelassenheit*).
4. **Marcus Aurelius, *Meditations*** — Makes Stoicism a real presence rather than a 3-unit token; PD (Long/Farquharson). *Resonates with:* Epictetus, Heraclitus (cosmic Logos/flux), Tao Te Ching (accord with nature/the Way).
5. **Pseudo-Dionysius, *Mystical Theology*** — The apophatic fountainhead of Christian (and Islamic/Jewish) negative theology; anchors a second Christian witness. *Resonates with:* Māṇḍūkya/neti-neti, Plotinus VI.9 (the One beyond being), Nāgārjuna (emptiness/negation), Balyānī.
6. **Zohar / Kabbalah selections (+ *Sefer Yetzirah*)** — Adds the wholly-absent Jewish mystical stream; Ein Sof and sefirot are a natural fourth pole to the nondual material. *Resonates with:* Ibn ʿArabī (waḥdat al-wujūd), Plotinus (emanation), Śaiva tattva-emanation.
7. **ʿAṭṭār, *Conference of the Birds*** — Broadens Sufism beyond Rūmī/Balyānī with the classic annihilation-in-God (fanāʾ) allegory; PD (FitzGerald/Nott). *Resonates with:* Rūmī, Balyānī (oneness of being), Zhuangzi (bird/journey allegory).
8. **Chan koan collection — *Gateless Gate* (Mumonkan)** — Introduces the Chan/koan genre absent from the corpus; short, unit-sized cases. *Resonates with:* Dōgen (same lineage), Vijñāna Bhairava (sudden recognition/dhāraṇā), Aṣṭāvakra (direct pointing).
9. **Ramana Maharshi, *Who Am I? / Upadeśa Sāram*** — Living-tradition bridge; self-inquiry directly extends the corpus's dominant "self/awareness" themes into the modern era. *Resonates with:* Aṣṭāvakra, Māṇḍūkya, Śiva Sūtra (recognition).
10. **Bṛhadāraṇyaka Upaniṣad (Yājñavalkya; "neti neti")** — The great dialogical Upaniṣad and origin of apophatic Vedānta. *Resonates with:* Pseudo-Dionysius, Nāgārjuna, Māṇḍūkya.
11. **Plato — Republic Cave/Divided Line + *Symposium* ladder of love** — Adds Plato's most resonant myths; multiplies the payoff of the existing *Phaedo*/Plotinus pairing. *Resonates with:* Plotinus (ascent to the Good/Beauty), Īśā (the golden disc veiling truth).
12. **Confucius, *Analects* (+ *Zhongyong*)** — Opens the entire Confucian pole of Chinese thought, complementing Daoism already present. *Resonates with:* Tao Te Ching (the Way, governance), Epictetus/Marcus (virtue-ethics of role and duty).
13. **Analayo-style Satipaṭṭhāna / Fire Sermon (Pali suttas)** — Grounds Buddhist *practice* (mindfulness, impermanence) in its earliest source, complementing the Madhyamaka verse fragments. *Resonates with:* Patañjali (attention/practice), Vijñāna Bhairava (awareness techniques).
14. **John of the Cross, *Dark Night* / Teresa, *Interior Castle*** — Deepens Christian mysticism into its experiential-stages literature. *Resonates with:* Rūmī (longing/union), Eckhart (detachment), Milarepa (ascetic ordeal as path).
15. **Parmenides, *Way of Truth*** — Completes the Presocratic pairing (Being vs. Heraclitean flux) and adds a monist counterweight. *Resonates with:* Heraclitus (direct dialectical foil), Māṇḍūkya (the changeless), Plotinus.
16. **Al-Ghazālī, *Niche of Lights* / *Alchemy of Happiness*** — Adds the systematic-philosophical wing of Sufism (light metaphysics, self-knowledge). *Resonates with:* Plotinus/light, Ibn ʿArabī, Īśā (light imagery).
17. **Nisargadatta, *I Am That* (selections)** — Second modern nondual witness; conversational form. *Resonates with:* Ramana, Aṣṭāvakra, Pratyabhijñāhṛdayam ("I-consciousness").
18. **Plotinus — add IV.8 & V.3** — Rounds out the Enneads with soul-descent and self-knowledge, the two tractates most cited by later mystics. *Resonates with:* Kaṭha (soul/Self), Pseudo-Dionysius, Śaiva pratyabhijñā (self-recognition).

**Sequencing note:** Items 1–8 do the most to correct *structural* imbalance (they add absent traditions or turn tokens into real presences); items 9–18 deepen resonance and fill within-tradition holes. In parallel, the 116 `structural_draft` Heraclitus fragments should be curated up before expanding Greek breadth further — quality parity matters as much as new coverage.

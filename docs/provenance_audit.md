# Provenance Audit — English-Text Sourcing (24 Live Collections)

**Date:** 2026-07-23
**Scope:** Classify the provenance of the English text in every live Pratibha collection so the team can reconcile copyright/asteya concerns before wider commercial use. This is a read-only audit — no corpus YAML, code, or registry files were modified.

**Primary evidence:** `app/sources_registry.py` (the `SOURCES` list and its `license` / `sell_ready_tier` / `pd_alternative` fields), cross-checked against the raw manuscript headers in `data/raw_texts/` and the PD catalog at `data/raw_texts/pd/manifest.yml`.

## Tiers

- **A · Clean** — the English is the project's own fresh rendering, or a genuine public-domain translation. Action: keep, just make attribution visible.
- **B · PD-swappable** — currently leans on a copyrighted translation, but a PD English alternative exists. Action: swap the anchor to the PD source.
- **C · Copyright-derived** — derived from an in-copyright translation and no PD English exists. Action: re-render fresh from the PD Sanskrit/source, or reduce to short attributed quote + own commentary.

**Result: 16 × A, 4 × B, 4 × C.**

---

## Full table

| Collection | Tier | English source | Rights holder | PD alternative | PD source text available | Recommended action | Confidence |
|---|---|---|---|---|---|---|---|
| Aṣṭāvakra Gītā | A | Pratibha own rendering from Sanskrit | project (own work) | — | Yes — received Sanskrit | keep+attribute | High |
| Bhagavad Gītā | A | Sir Edwin Arnold (1885, PD, Gutenberg #2388) | public domain | — | Yes | keep+attribute | High |
| Chāndogya Upaniṣad | A | F. Max Müller, SBE vol. 1 (1879, PD) | public domain | — | Yes | keep+attribute | High |
| Epictetus (Enchiridion) | A | Elizabeth Carter (1758/59, PD) | public domain | — | Yes | keep+attribute | High |
| Heart Sūtra | A | F. Max Müller, SBE vol. 49 (1894, PD) | public domain | — | Yes (GRETIL) | keep+attribute | High |
| Heraclitus (Fragments) | A | George T.W. Patrick (1889, PD) | public domain | — | Yes | keep+attribute | High |
| Īśāvāsya Upaniṣad | **B** | Pratibha editorial + Shlokam.org (non-PD web source) | mixed / Shlokam.org (uncertain rights) | Max Müller, SBE vol. 1 (1879) | Yes | swap-to-PD | Medium |
| Know Yourself (Ibn ʿArabī/Balyānī) | **C** | Cecilia Twinch, *Know Yourself* (Beshara, 2021) | Twinch / Beshara (copyrighted) | None | Yes — Arabic original (not yet sourced) | re-render-from-source | High |
| Māṇḍūkya Upaniṣad & Kārikā | A | Pratibha own rendering from Sanskrit | project (own work) | Müller SBE 34 (optional ref only) | Yes | keep+attribute | High |
| Songs of Milarepa | A | Evans-Wentz/Dawa-Samdup (1928, now PD) | public domain | — | Yes | keep+attribute | High |
| Mūlamadhyamakakārikā (Nāgārjuna) | A | Pratibha original rendering from Sanskrit (no PD English exists) | project (own work) | — | Yes (GRETIL) | keep+attribute | High |
| Yoga Sūtras (Patañjali) | **B** | Split: Dvivedi (PD) for Pada 1–Sādhana≤2.30; Satchidananda-informed (copyrighted, 1978) for 2.31+ | mixed — Dvivedi PD / Satchidananda copyrighted | Dvivedi (1890) or Vivekananda, *Raja Yoga* (1896) | Yes | swap-to-PD | High |
| Phaedo | A | Benjamin Jowett (Gutenberg #1658, PD) | public domain | — | Yes | keep+attribute | High |
| Enneads (Plotinus) | A | MacKenna & Page (PD core; Page's 1962 revision layer less clear-cut) | public domain (mostly) | — | Yes | keep+attribute | Medium-High |
| Pratyabhijñāhṛdayam | A | Pratibha own rendering from Sanskrit | project (own work) | — | Yes (KSTS) | keep+attribute | Medium-High |
| Bodhicaryāvatāra (Śāntideva) | A | L.D. Barnett, *The Path of Light* (1909, PD) | public domain | — | Yes | keep+attribute | High |
| Śiva Sūtra | A | Conor Byrnes — own translation & commentary | project (own work — Conor Byrnes) | — | Yes | keep+attribute | High |
| Śvetāśvatara Upaniṣad | **B** | Pratibha English on a disclosed "Radhakrishnan" base (1953, copyrighted) with departures | Radhakrishnan / publisher (copyrighted) | Max Müller, SBE vol. 15 (1884) | Yes | swap-to-PD | High |
| Tantrasāra | A | Conor Byrnes — own translation & commentary, informed by Christopher Wallis | project (own work), with acknowledged copyrighted influence | — | Yes (KSTS/Trivandrum) | keep+attribute | Medium |
| Tao Te Ching | **B** | Pratibha editorial + Legge (PD) reference; Lau/Mitchell (copyrighted) noted in commentary | mixed | James Legge, SBE vol. 39 / Gutenberg #216 | Yes | swap-to-PD | Medium |
| Vijñāna Bhairava | **C** | Christopher D. Wallis translation (project PDF, copyrighted) | Christopher D. Wallis (copyrighted) | None | Yes (KSTS 1918) | re-render-from-source | High |
| Spandakārikā | **C** | Daniel Odier, *Yoga Spandakarika* (Inner Traditions, 2005, copyrighted) | Odier / Inner Traditions (copyrighted) | None | Yes (KSTS) | re-render-from-source | High |
| Yoginīhṛdaya | **C** | Hybrid: "Body" layer = Padoux & Jeanty, *The Heart of the Yoginī* (OUP, 2013, copyrighted); separate "Pratibha Translation" layer is already a fresh own rendering | Padoux/Jeanty/OUP (copyrighted) for Body layer | None | Yes, in principle (edition uncertain) | quote+attribute+commentary | Medium |
| Zhuangzi | A | Herbert A. Giles (1889, Gutenberg #59709, PD) | public domain | — | Yes | keep+attribute | High |

---

## Bucket C — re-render priority queue

These four carry the highest legal exposure: the current English is a copyrighted translation used directly as the anchor, and no PD English exists to swap to. All four have PD Sanskrit available, so the fix already has a proven playbook in this repo (Nāgārjuna MMK and Śiva Sūtra both show it works).

1. **Vijñāna Bhairava** — anchor is literally Christopher Wallis's translation pulled from `data/raw_texts/VBT+translation+WALLIS-2.pdf`, spanning all 112 yuktis. Highest exposure of the four by volume. Re-render from the PD KSTS 1918 Sanskrit.
2. **Spandakārikā** — anchor is Daniel Odier's *Yoga Spandakarika* (Inner Traditions, 2005) from the project EPUB. Re-render from PD KSTS Sanskrit.
3. **Yoginīhṛdaya** — partially mitigated already: a fresh "Pratibha Translation" layer exists alongside the Padoux/Jeanty "Body" layer. Action is lighter than a from-scratch re-render — reduce the Padoux Body-layer text to short attributed quotes and promote the existing Pratibha Translation as the primary shown rendering.
4. **Know Yourself (Ibn ʿArabī/Balyānī)** — anchor is Cecilia Twinch's 2021 Beshara translation. Unlike the Kashmir Śaiva texts, the source language here is Arabic, not Sanskrit; a PD Arabic original (al-Balyānī's short medieval treatise) exists but is not yet sourced into `data/raw_texts`. Until it is, keep only short attributed Twinch quotes with Pratibha's own commentary.

## Bucket B — quick wins (PD swap available)

Lower urgency than bucket C because a clean PD English text is already on hand or nearly so — these are swap/edit jobs, not re-renders:

1. **Śvetāśvatara Upaniṣad** — manuscript header explicitly names Radhakrishnan (1953, copyrighted) as the "base translation context." Swap the base to Müller's SBE vol. 15 (1884, PD), keeping Pratibha's own departures/commentary layer.
2. **Yoga Sūtras (Patañjali)** — half already uses the PD Dvivedi anchor (Pada 1 through Sādhana ≤2.30). Just extend that same PD anchor (Dvivedi 1890 or Vivekananda's *Raja Yoga* 1896) across Sūtra 2.31 through the end of Pada 4, replacing the Satchidananda-informed English.
3. **Tao Te Ching** — Legge's PD 1891 translation is already cited as a comparative reference and is on file at `data/raw_texts/pd/chinese/tao_te_ching_legge_gutenberg_216.txt`. Make it the primary anchor across all 81 chapters (especially the 69 Wave-B LLM-generated ones) and restrict Lau/Mitchell citations to brief, clearly-marked comparative quotes in commentary only.
4. **Īśāvāsya Upaniṣad** — replace the Shlokam.org-sourced Sanskrit/transliteration with Müller's SBE vol. 1 (1879, PD), which also comes with a PD English translation as a bonus safety net.

---

## Ambiguous / low(er)-confidence items — flag for human confirmation

None of the 24 came out fully "low confidence," but four sit at **medium** and deserve a second look before being signed off as clean:

- **Tantrasāra** (tier A, medium confidence) — registry credits this as Conor Byrnes's own translation, matching the Śiva Sūtra pattern, but unlike Śiva Sūtra it explicitly discloses being "informed by Christopher Wallis" (whose *Tantra Illuminated* and *Tantrasāra* translation sit in `data/raw_texts` as in-copyright reference material). Recommend a quick phrase-level independence check against Wallis's wording before treating this as fully cleared.
- **Pratyabhijñāhṛdayam** (tier A, medium-high confidence) — manuscript inspection shows an independent Sanskrit-to-English rendering with no named copyrighted anchor, and no Jaideva Singh file exists anywhere in `data/raw_texts`. But the registry's own note ("no PD English — Jaideva Singh is copyrighted") exists specifically to flag the risk of unconscious echo of Jaideva Singh's well-known 1980 translation. Worth a one-time spot-check.
- **Tao Te Ching** (tier B, medium confidence) — the degree to which Lau/Mitchell (both copyrighted, both explicitly "noted in commentary" per the registry) influenced the 69 Wave-B LLM-generated chapters versus the smaller curated Wave A set can't be verified from the registry text alone; a chapter-by-chapter spot check is warranted, especially since a 2018 Penguin Tao Te Ching ebook sits in `data/raw_texts` (unclear if/how it was used).
- **Yoginīhṛdaya** (tier C, medium confidence) — the fix already exists in the corpus (a fresh "Pratibha Translation" layer distinct from the Padoux "Body" layer); the open question is purely editorial/product — which layer the app actually surfaces by default to readers — not a translation-quality question.
- **Enneads (Plotinus)** (tier A, medium-high confidence) — MacKenna's original 1917–1930 volumes are solidly PD, but the specific MIT Classics / Delphi text in use is the "Page"-revised 1962 edition, whose own copyright status as a distinct revision is not fully verified here.

---

## Notes on method

- The registry's own `sell_ready_tier` (green/yellow/orange/red) was treated as strong prior evidence but not taken at face value where it conflicted with what raw manuscript inspection showed — e.g., Aṣṭāvakra Gītā, Māṇḍūkya + Kārikā, and Pratyabhijñāhṛdayam are marked "green"/"mixed" in the registry with no explicit "own rendering" disclosure sentence (unlike Nāgārjuna MMK and Śiva Sūtra); direct inspection of `data/raw_texts/#<title>` manuscripts confirmed each is in fact an independent Sanskrit-to-English rendering with no named copyrighted anchor, supporting tier A.
- Conversely, Śvetāśvatara Upaniṣad is marked "yellow" in the registry, and manuscript inspection *confirmed* the risk directly — its header literally states "Base translation context: S. Radhakrishnan" — raising confidence in the bucket-B call to high.
- "PD source text available" was assessed generously: nearly every collection here draws on an ancient Sanskrit/Greek/Chinese/Arabic/Tibetan source that is PD in principle, even where a *convenient, already-transcribed* PD edition is not yet sitting in `data/raw_texts`. Where that gap exists (Know Yourself's Arabic original; Yoginīhṛdaya's pre-modern Sanskrit edition), it is called out explicitly since sourcing it is itself a prerequisite task before re-rendering can start.
- Four collections in the registry (Dōgen Shōbōgenzō, Meister Eckhart, Rūmī Mathnawī, Tilopa Mahāmudra) were excluded from this audit — they are not among the 24 live collections named in the brief, and `git status` shows their canonical YAML files as deleted in the working tree.

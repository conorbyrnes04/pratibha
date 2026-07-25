"""Attribution registry for texts in the Pratibha corpus.

Used by GET /sources and the web Sources page. Update when adding collections.

Pratibha is a non-commercial offering to students. The ethic here is *asteya*
(non-stealing): every English rendering in the corpus stands on either a
public-domain source or original authorship, and it says so plainly.

provenance_tier:
  pd_render   — Pratibha's own English rendered from a public-domain SOURCE-LANGUAGE
                text (Sanskrit, Classical Chinese, Tibetan, Persian, Greek, MHG,
                classical Japanese). No copyrighted translation is reproduced.
  pd_adapted  — English follows / lightly modernizes a named PUBLIC-DOMAIN
                translation, credited to its translator.
  original    — Original translation and commentary conceived and authored in
                Pratibha.

license:
  public_domain     — source or anchor translation is out of copyright
  original_editorial — original Pratibha authorship
"""

from __future__ import annotations

from typing import Any

SOURCES: list[dict[str, Any]] = [
    {
        "id": "astavakra_gita",
        "collection": "Astavakra Gita",
        "tradition": "Advaita Vedānta (Sanskrit)",
        "original_work": "Aṣṭāvakra Gītā (dialogue of Aṣṭāvakra and King Janaka)",
        "anchor_translation": "Pratibha rendering from the public-domain Sanskrit (received Devanāgarī / IAST)",
        "sanskrit_source": "Received Sanskrit (Devanāgarī / IAST), public domain",
        "editorial_note": "English rendered afresh from the Sanskrit; commentary, key terms, resonances, and practice are original Pratibha editorial.",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
    },
    {
        "id": "bhagavad_gita",
        "collection": "Bhagavad Gita",
        "tradition": "Sanskrit / Itihāsa",
        "original_work": "Bhagavad Gītā (Mahābhārata, Bhīṣma Parvan)",
        "anchor_translation": "English follows Sir Edwin Arnold, *The Song Celestial* (1885; Project Gutenberg #2388, public domain)",
        "sanskrit_source": "Received Devanāgarī where present; not line-aligned to Arnold throughout",
        "editorial_note": "Arnold's public-domain verse is the English basis; Pratibha layers depart where noted.",
        "license": "public_domain",
        "provenance_tier": "pd_adapted",
        "status": "in_corpus",
        "links": [{"label": "Project Gutenberg #2388 (Arnold)", "url": "https://www.gutenberg.org/ebooks/2388"}],
    },
    {
        "id": "chandogya_upanishad",
        "collection": "Chāndogya Upaniṣad",
        "tradition": "Sāmaveda Upaniṣad / Vedānta",
        "original_work": "Chāndogya Upaniṣad",
        "anchor_translation": "Pratibha rendering from the public-domain Sanskrit; F. Max Müller, SBE vol. 1 (1879) as comparative reference",
        "sanskrit_source": "Received Chāndogya text (Devanāgarī / IAST), public domain",
        "editorial_note": "Om/udgītha, Sāṇḍilya-vidyā, Uddālaka–Śvetaketu (*tat tvam asi*), Prajāpati–Indra. English rendered from the Sanskrit; commentary is editorial.",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
        "links": [{"label": "Internet Archive — Müller Upaniṣads vol. 1", "url": "https://archive.org/details/upanishads00mlgoog"}],
    },
    {
        "id": "confucius_analects",
        "collection": "Confucius — Analects",
        "tradition": "Chinese / Ruist (Confucian)",
        "original_work": "Confucius (Kǒngzǐ), *Lúnyǔ* 論語 (Analects)",
        "anchor_translation": "Pratibha rendering from the public-domain Classical Chinese; James Legge, *The Chinese Classics* vol. 1 (1893) as comparative reference",
        "sanskrit_source": "Traditional Chinese characters in the Original layer, public domain",
        "editorial_note": "English rendered from the Classical Chinese; commentary and practice layers are original Pratibha editorial.",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
        "links": [{"label": "Internet Archive — Legge, Chinese Classics vol. 1", "url": "https://archive.org/details/chineseclassics01legggoog"}],
    },
    {
        "id": "dogen_shobogenzo",
        "collection": "Dōgen — Shōbōgenzō",
        "tradition": "Japanese Zen / Sōtō",
        "original_work": "Dōgen, *Shōbōgenzō* (Treasury of the True Dharma Eye)",
        "anchor_translation": "Pratibha rendering from the public-domain classical Japanese (Kokubasha 1896 edition)",
        "sanskrit_source": "Classical Japanese / kanbun, Kokubasha 1896, public domain",
        "editorial_note": "Pilot: Genjōkōan and Uji. English rendered from the classical Japanese; commentary is editorial.",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
    },
    {
        "id": "epictetus_works",
        "collection": "Epictetus Works",
        "tradition": "Greek Stoic",
        "original_work": "Epictetus, *Enchiridion* (recorded by Arrian)",
        "anchor_translation": "English follows Elizabeth Carter, *All the Works of Epictetus* (1758; public domain)",
        "editorial_note": "Carter's public-domain translation is the English basis; commentary and study layers are editorial.",
        "license": "public_domain",
        "provenance_tier": "pd_adapted",
        "status": "in_corpus",
    },
    {
        "id": "heart_sutra",
        "collection": "Heart Sūtra",
        "tradition": "Mahāyāna / Prajñāpāramitā (Sanskrit)",
        "original_work": "Prajñāpāramitāhṛdaya (Heart Sūtra), shorter recension",
        "anchor_translation": "Pratibha rendering from the public-domain Sanskrit (GRETIL); F. Max Müller, SBE vol. 49 (1894) as reference",
        "sanskrit_source": "Sanskrit (IAST) source-verified from the GRETIL shorter recension, public domain",
        "editorial_note": "3 units: form=emptiness, no-attainment, the Gate-gate mantra. English rendered from the Sanskrit; study layers editorial.",
        "coverage": "3 pilot units",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
        "links": [{"label": "Internet Archive — SBE vol. 49 (Müller 1894)", "url": "https://archive.org/details/buddhistmahayana49cowe"}],
    },
    {
        "id": "heraclitus_fragments",
        "collection": "Heraclitus Fragments",
        "tradition": "Greek Pre-Socratic",
        "original_work": "Heraclitus of Ephesus (Diels–Kranz numbering)",
        "anchor_translation": "English follows George T. W. Patrick, *The Fragments of Heraclitus* (1889, Bywater Greek text; public domain)",
        "editorial_note": "12 curated Pratibha-layer fragments (Logos, fire, river, war, harmony, soul, Delphi); remaining units are structural drafts from the Patrick text pending curation.",
        "coverage": "12 curated + 116 structural draft",
        "license": "public_domain",
        "provenance_tier": "pd_adapted",
        "status": "in_corpus",
        "links": [{"label": "Internet Archive — Patrick 1889", "url": "https://archive.org/details/fragmentsofworko00hera"}],
    },
    {
        "id": "isavasya_upanishad",
        "collection": "Isavasya Upanishad",
        "tradition": "Śukla Yajurveda Upaniṣad",
        "original_work": "Īśāvāsya / Īśopaniṣad (Isha Upanishad)",
        "anchor_translation": "Pratibha rendering from the public-domain Sanskrit; F. Max Müller, SBE vol. 1 (1879) as reference",
        "sanskrit_source": "Received Sanskrit mantras (Devanāgarī / IAST), public domain",
        "editorial_note": "English rendered from the Sanskrit; commentary and resonances are editorial.",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
        "links": [{"label": "Sacred-texts — SBE vol. 1 (Īśā)", "url": "https://sacred-texts.com/hin/sbe01/index.htm"}],
    },
    {
        "id": "know_yourself_ibn_arabi_balyani",
        "collection": "Know Yourself (Ibn Arabi / Balyani)",
        "tradition": "Sufi / Arabic",
        "original_work": "Awḥad al-Dīn Balyānī, *Risālat al-aḥadiyya* (Epistle on Oneness) — long transmitted under Ibn ʿArabī's name",
        "anchor_translation": "Based on the public-domain English translation by T. H. Weir, *Journal of the Royal Asiatic Society* (1901)",
        "editorial_note": "Authorship is now attributed to Balyānī rather than Ibn ʿArabī. English follows Weir's public-domain 1901 translation; Pratibha study layers are editorial. (Earlier drafts leaned on a copyrighted modern translation — replaced during the asteya reconciliation.)",
        "license": "public_domain",
        "provenance_tier": "pd_adapted",
        "status": "in_corpus",
    },
    {
        "id": "mandukya_upanishad_and_gaudapada_karika",
        "collection": "Mandukya Upanishad and Gaudapada Karika",
        "tradition": "Upaniṣadic / Advaita",
        "original_work": "Māṇḍūkya Upaniṣad + Gauḍapāda Kārikā",
        "anchor_translation": "Pratibha rendering from the public-domain Sanskrit; F. Max Müller, SBE vol. 34 (1894) as reference",
        "sanskrit_source": "Received Upaniṣad and Kārikā text (Devanāgarī / IAST), public domain",
        "editorial_note": "Includes the ajātivāda (non-origination) framing. English rendered from the Sanskrit; commentary is editorial.",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
    },
    {
        "id": "meister_eckhart",
        "collection": "Meister Eckhart",
        "tradition": "Christian mysticism / Middle High German",
        "original_work": "Meister Eckhart, *Von Abegescheidenheit* (On Detachment)",
        "anchor_translation": "Pratibha rendering from the public-domain Middle High German (Franz Pfeiffer, *Deutsche Mystiker* vol. 2, 1857)",
        "sanskrit_source": "Middle High German, Pfeiffer 1857, public domain",
        "editorial_note": "Pilot: 12 units. English rendered from the MHG; commentary and resonances are editorial.",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
        "links": [{"label": "Internet Archive — Pfeiffer 1857", "url": "https://archive.org/details/deutschemystike01mystgoog"}],
    },
    {
        "id": "milarepa_songs",
        "collection": "Milarepa — Songs",
        "tradition": "Tibetan Buddhist / Kagyü",
        "original_work": "Jetsün Milarepa, songs from the *Jetsun-Kahbum* (Life and Songs)",
        "anchor_translation": "Pratibha rendering with Tibetan (Uchen) originals; Kazi Dawa-Samdup / W. Y. Evans-Wentz, *Tibet's Great Yogi Milarepa* (1928, public domain) as English basis",
        "sanskrit_source": "Tibetan (Uchen script), public domain",
        "editorial_note": "21 songs/hymns. Tibetan originals set in Uchen; English follows the public-domain Evans-Wentz / Dawa-Samdup edition; commentary is editorial.",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
        "links": [{"label": "Internet Archive — Evans-Wentz 1928", "url": "https://archive.org/details/dli.ministry.06735"}],
    },
    {
        "id": "nagarjuna_mulamadhyamakakarika",
        "collection": "Nāgārjuna — Mūlamadhyamakakārikā",
        "tradition": "Madhyamaka (Sanskrit)",
        "original_work": "Nāgārjuna, *Mūlamadhyamakakārikā* (Fundamental Verses on the Middle Way)",
        "anchor_translation": "Pratibha original rendering from the public-domain Sanskrit (GRETIL critical text)",
        "sanskrit_source": "Sanskrit (IAST) source-verified from GRETIL (chs. 18, 24, 25), public domain",
        "editorial_note": "9 verses: no-self (ch. 18), emptiness and the two truths (ch. 24), nirvāṇa (ch. 25). Original English rendering from the Sanskrit; flag for scholarly review.",
        "coverage": "9 pilot units",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
        "links": [{"label": "GRETIL — Mūlamadhyamakakārikā", "url": "https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_nAgArjuna-mUlamadhyamakakArikA.htm"}],
    },
    {
        "id": "patanjali_yoga_sutras",
        "collection": "Patañjali Yoga Sūtras",
        "tradition": "Yoga / Sāṃkhya",
        "original_work": "Patañjali, *Yoga Sūtras* (195 sūtras)",
        "anchor_translation": "Pratibha rendering from the public-domain Sanskrit; M. N. Dvivedi (1890) as comparative reference",
        "sanskrit_source": "Received Sanskrit (IAST), public domain",
        "editorial_note": "Full 195 sūtras rendered from the Sanskrit; commentary is editorial. (Earlier drafts leaned on a copyrighted modern translation — replaced during the asteya reconciliation.)",
        "coverage": "195 sūtras",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
        "links": [{"label": "Internet Archive — Dvivedi 1890", "url": "https://archive.org/details/yogaSutraOfPatanjali"}],
    },
    {
        "id": "phaedo_plato",
        "collection": "Phaedo (Plato)",
        "tradition": "Greek / Platonic",
        "original_work": "Plato, *Phaedo*",
        "anchor_translation": "English follows Benjamin Jowett (Project Gutenberg #1658, public domain)",
        "editorial_note": "12 units across the dialogue's major arcs. Jowett's public-domain English is the basis; Pratibha layers editorial.",
        "license": "public_domain",
        "provenance_tier": "pd_adapted",
        "status": "in_corpus",
        "links": [{"label": "Project Gutenberg #1658 (Jowett)", "url": "https://www.gutenberg.org/ebooks/1658"}],
    },
    {
        "id": "plotinus_enneads",
        "collection": "Plotinus Enneads",
        "tradition": "Greek Neoplatonic",
        "original_work": "Plotinus, *Enneads*",
        "anchor_translation": "English follows Stephen MacKenna & B. S. Page (public domain)",
        "editorial_note": "Pilot: I.6 (Beauty), V.1 (Three Hypostases), VI.9 (On the Good) — 32 units. MacKenna & Page's public-domain English is the basis; commentary editorial.",
        "license": "public_domain",
        "provenance_tier": "pd_adapted",
        "status": "in_corpus",
        "links": [{"label": "MIT Classics — Enneads", "url": "https://classics.mit.edu/Plotinus/enneads.html"}],
    },
    {
        "id": "pratyabhijnahrdayam",
        "collection": "Pratyabhijnahrdayam",
        "tradition": "Kashmir Śaiva",
        "original_work": "Kṣemarāja, *Pratyabhijñāhṛdayam* (The Heart of Recognition, 11th c.)",
        "anchor_translation": "Pratibha rendering from the public-domain Sanskrit (KSTS edition, 1918)",
        "sanskrit_source": "Sanskrit sūtras (IAST / Devanāgarī), KSTS 1918, public domain",
        "editorial_note": "English rendered from the Sanskrit; commentary and cross-tradition resonances are editorial.",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
    },
    {
        "id": "rumi_mathnawi",
        "collection": "Rūmī — Mathnawī-yi Maʿnawī",
        "tradition": "Sufi / Persian",
        "original_work": "Jalāl al-Dīn Rūmī, *Mathnawī-yi Maʿnawī*",
        "anchor_translation": "Pratibha rendering from the public-domain Persian (Ganjoor / masnavi.net)",
        "sanskrit_source": "Persian source text, public domain",
        "editorial_note": "Pilot: 22 units — Ney-nāmeh, Moses & shepherd, elephant in the dark, the painters, the merchant's parrot, die-before-you-die. English rendered from the Persian (strong draft, pending Persian review); commentary editorial.",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
    },
    {
        "id": "shantideva_bodhicaryavatara",
        "collection": "Śāntideva — Bodhicaryāvatāra",
        "tradition": "Mahāyāna / Madhyamaka (Sanskrit)",
        "original_work": "Śāntideva, *Bodhicaryāvatāra* (Entering the Bodhisattva's Way)",
        "anchor_translation": "Pratibha rendering from the public-domain Sanskrit (GRETIL); L. D. Barnett, *The Path of Light* (1909) as reference",
        "sanskrit_source": "Sanskrit (IAST) from GRETIL (chs. VIII–IX), public domain",
        "editorial_note": "Pilot: 8 units from ch. VIII (meditation, self–other exchange) and ch. IX (wisdom, two truths). English rendered from the Sanskrit; commentary editorial.",
        "coverage": "8 pilot units",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
        "links": [{"label": "Internet Archive — Barnett, The Path of Light (1909)", "url": "https://archive.org/details/pathoflightrende00shanuoft"}],
    },
    {
        "id": "siva_sutra",
        "collection": "Siva Sutra",
        "tradition": "Kashmir Śaiva",
        "original_work": "Śiva Sūtras (attributed to Vasugupta)",
        "anchor_translation": "Original translation and commentary by Conor Byrnes, from the Sanskrit",
        "editorial_note": "Śāmbhavopāya chapter; conceived and authored in Pratibha.",
        "license": "original_editorial",
        "provenance_tier": "original",
        "status": "in_corpus",
        "conceived_by_conor": True,
    },
    {
        "id": "svetasvatara_upanishad",
        "collection": "Svetasvatara Upanishad",
        "tradition": "Upaniṣadic / theistic Vedānta",
        "original_work": "Śvetāśvatara Upaniṣad",
        "anchor_translation": "Pratibha rendering from the public-domain Sanskrit; F. Max Müller, SBE vol. 15 (1884) as reference",
        "sanskrit_source": "Received Upaniṣad text (Devanāgarī / IAST), public domain",
        "editorial_note": "English rendered from the Sanskrit; commentary is editorial.",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
        "links": [{"label": "Sacred-texts — SBE vol. 15", "url": "https://sacred-texts.com/hin/sbe15/index.htm"}],
    },
    {
        "id": "tantrasara",
        "collection": "Tantrasāra",
        "tradition": "Kashmir Śaiva / Tantra",
        "original_work": "Abhinavagupta, *Tantrasāra*",
        "anchor_translation": "Original translation and commentary by Conor Byrnes, from the public-domain Sanskrit (KSTS)",
        "sanskrit_source": "Sanskrit (IAST), KSTS edition, public domain",
        "editorial_note": "Āhnikas 1–5. Rendered from the Sanskrit and authored in Pratibha (study informed by Christopher Wallis).",
        "coverage": "19 units (Āhnikas 1–5)",
        "license": "original_editorial",
        "provenance_tier": "original",
        "status": "in_corpus",
        "conceived_by_conor": True,
    },
    {
        "id": "tao_te_ching",
        "collection": "Tao Te Ching",
        "tradition": "Chinese Daoist",
        "original_work": "Lǎozǐ, *Dào Dé Jīng* 道德經 (81 chapters)",
        "anchor_translation": "Pratibha rendering from the public-domain Classical Chinese; James Legge, SBE vol. 39 (1891; Project Gutenberg #216) as reference",
        "sanskrit_source": "Traditional Chinese characters in the Original layer, public domain",
        "editorial_note": "Full 81 chapters rendered from the Classical Chinese; commentary and practice layers editorial.",
        "coverage": "81 of 81 chapters",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
        "links": [{"label": "Project Gutenberg #216 (Legge)", "url": "https://www.gutenberg.org/ebooks/216"}],
    },
    {
        "id": "the_book_of_chuang_tzu",
        "collection": "The Book of Chuang Tzu",
        "tradition": "Chinese Daoist",
        "original_work": "Zhuangzi (*Nánhuá Jīng* 莊子)",
        "anchor_translation": "Pratibha rendering from the public-domain Classical Chinese; Herbert A. Giles (1889; Project Gutenberg #59709) as reference",
        "sanskrit_source": "Traditional Chinese characters in the Original layer, public domain",
        "editorial_note": "English rendered from the Classical Chinese; Giles's public-domain translation informs curated units; commentary editorial.",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
        "links": [{"label": "Project Gutenberg #59709 (Giles)", "url": "https://www.gutenberg.org/ebooks/59709"}],
    },
    {
        "id": "tilopa_mahamudra",
        "collection": "Tilopa — Mahāmudrā Upadeśa",
        "tradition": "Tibetan Buddhist / Kagyü (Mahāmudrā)",
        "original_work": "Tilopa, *Mahāmudropadeśa* (Ganges Mahāmudrā), teaching to Nāropa",
        "anchor_translation": "Pratibha rendering with Tibetan (Uchen) originals from the public-domain Ganges Mahāmudrā text",
        "sanskrit_source": "Tibetan (Uchen script), public domain",
        "editorial_note": "3 units on non-meditation, mind-like-space, and the guru's grace. Tibetan originals set in Uchen; English rendered from them. (Earlier draft lacked a verified public-domain source — recovered during the asteya reconciliation.)",
        "coverage": "3 pilot units",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
    },
    {
        "id": "vijnana_bhairava",
        "collection": "Vijnana Bhairava",
        "tradition": "Kashmir Śaiva / Trika",
        "original_work": "Vijñānabhairavatantra (112 dhāraṇās)",
        "anchor_translation": "Pratibha rendering from the public-domain KSTS Sanskrit (1918)",
        "sanskrit_source": "Sanskrit (IAST / Devanāgarī), KSTS edition 1918, public domain",
        "editorial_note": "112 yuktis rendered from the KSTS Sanskrit; commentary and practice layers editorial. (Earlier drafts leaned on a copyrighted modern translation — replaced during the asteya reconciliation.)",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
        "links": [{"label": "Internet Archive — KSTS Vijñānabhairava", "url": "https://archive.org/details/dli.ernet.242056"}],
    },
    {
        "id": "yoga_spandakarika",
        "collection": "Yoga Spandakarika",
        "tradition": "Kashmir Śaiva",
        "original_work": "Spandakārikā (Kallaṭa / Vasugupta tradition)",
        "anchor_translation": "Pratibha rendering from the public-domain KSTS Sanskrit",
        "sanskrit_source": "Sanskrit (IAST), KSTS edition, public domain",
        "editorial_note": "Stanza-level units rendered from the Sanskrit; commentary editorial. (Earlier drafts leaned on a copyrighted modern translation — replaced during the asteya reconciliation.)",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
    },
    {
        "id": "yoginihrdaya",
        "collection": "Yoginīhṛdaya",
        "tradition": "Śrī Vidyā / Tantra",
        "original_work": "Yoginīhṛdaya (Heart of the Yoginī)",
        "anchor_translation": "Pratibha rendering from the public-domain KSTS Sanskrit",
        "sanskrit_source": "Sanskrit (IAST); Devanāgarī editorially reconstructed",
        "editorial_note": "English rendered from the Sanskrit; commentary editorial. (Earlier drafts leaned on a copyrighted modern translation — replaced during the asteya reconciliation.)",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
    },
    {
        "id": "zhongyong",
        "collection": "Zhongyong",
        "tradition": "Chinese / Ruist (Confucian)",
        "original_work": "Zǐsī (attrib.), *Zhōngyōng* 中庸 (Doctrine of the Mean)",
        "anchor_translation": "Pratibha rendering from the public-domain Classical Chinese; James Legge, *The Chinese Classics* vol. 1 (1893) as comparative reference",
        "sanskrit_source": "Traditional Chinese characters in the Original layer, public domain",
        "editorial_note": "English rendered from the Classical Chinese; commentary and practice layers editorial.",
        "license": "public_domain",
        "provenance_tier": "pd_render",
        "status": "in_corpus",
    },
]

LICENSE_LABELS = {
    "public_domain": "Public-domain source",
    "original_editorial": "Original Pratibha work",
}

PROVENANCE_TIER_LABELS = {
    "pd_render": "Rendered from a public-domain source text",
    "pd_adapted": "Adapted from a public-domain translation",
    "original": "Original translation & commentary",
}


def corpus_counts(verses: list[dict]) -> dict[str, int]:
    from .collection_aliases import canonical_slug

    counts: dict[str, int] = {}
    for v in verses:
        coll = str(v.get("collection") or "").strip()
        if not coll:
            continue
        slug = canonical_slug(coll)
        counts[slug] = counts.get(slug, 0) + 1
    return counts


def build_sources_payload(verses: list[dict]) -> dict[str, Any]:
    counts = corpus_counts(verses)
    items = []
    for entry in SOURCES:
        row = dict(entry)
        slug = entry["id"]
        row["passages_in_corpus"] = counts.get(slug, 0)
        row["license_label"] = LICENSE_LABELS.get(entry["license"], entry["license"])
        tier = entry.get("provenance_tier") or "pd_render"
        row["provenance_tier"] = tier
        row["provenance_tier_label"] = PROVENANCE_TIER_LABELS.get(tier, tier)
        row["conceived_by_conor"] = bool(entry.get("conceived_by_conor"))
        items.append(row)
    in_corpus = sum(1 for i in items if i["passages_in_corpus"] > 0)
    tier_counts: dict[str, int] = {}
    for i in items:
        if i["passages_in_corpus"] > 0:
            t = i["provenance_tier"]
            tier_counts[t] = tier_counts.get(t, 0) + 1
    return {
        "items": items,
        "summary": {
            "collections_documented": len(items),
            "collections_in_corpus": in_corpus,
            "total_passages": sum(counts.values()),
            "provenance_tiers": tier_counts,
        },
    }

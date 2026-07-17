"""Attribution registry for texts in the Pratibha corpus.

Used by GET /sources and the web Sources page. Update when adding collections.
"""

from __future__ import annotations

from typing import Any

# sell_ready_tier:
#   green  — PD anchor or original Pratibha work; low commercial risk
#   yellow — copyrighted anchor; PD alternative identified (swap recommended)
#   orange — no PD English; use Pratibha English from PD Sanskrit
#   red    — copyrighted anchor; no PD English alternative

SOURCES: list[dict[str, Any]] = [
    {
        "id": "astavakra_gita",
        "collection": "Astavakra Gita",
        "tradition": "Advaita Vedānta (Sanskrit)",
        "original_work": "Aṣṭāvakra Gītā (dialogue of Aṣṭāvakra and Janaka)",
        "anchor_translation": "Pratibha editorial English (manuscript in data/raw_texts); Sanskrit via received text",
        "sanskrit_source": "Received Devanagari / IAST in Pratibha manuscript",
        "editorial_note": "Commentary, key terms, resonances, and practice layers are original Pratibha editorial.",
        "license": "mixed",
        "sell_ready_tier": "green",
        "pd_alternative": None,
        "status": "in_corpus",
    },
    {
        "id": "bhagavad_gita",
        "collection": "Bhagavad Gita",
        "tradition": "Sanskrit / Itihāsa",
        "original_work": "Bhagavad Gītā (Mahābhārata, Bhīṣma Parvan)",
        "anchor_translation": "Sir Edwin Arnold, *The Bhagavad Gita* (Project Gutenberg #2388, public domain)",
        "sanskrit_source": "Devanagari in Pratibha units where present; not yet line-aligned to Arnold throughout",
        "editorial_note": "Pratibha translation and commentary layers depart from Arnold where noted in manuscript.",
        "license": "public_domain",
        "sell_ready_tier": "green",
        "pd_alternative": None,
        "status": "in_corpus",
        "links": [{"label": "Project Gutenberg #2388", "url": "https://www.gutenberg.org/ebooks/2388"}],
    },
    {
        "id": "epictetus_works",
        "collection": "Epictetus Works",
        "tradition": "Greek Stoic",
        "original_work": "Epictetus, *Enchiridion* (via Arrian)",
        "anchor_translation": "Elizabeth Carter, *All the Works of Epictetus* (Project Gutenberg / public domain)",
        "editorial_note": "Pratibha commentary and study layers are original editorial.",
        "license": "public_domain",
        "sell_ready_tier": "green",
        "pd_alternative": None,
        "status": "in_corpus",
    },
    {
        "id": "heraclitus_fragments",
        "collection": "Heraclitus Fragments",
        "tradition": "Greek Pre-Socratic",
        "original_work": "Heraclitus of Ephesus (Diels–Kranz numbering in corpus)",
        "anchor_translation": "George T.W. Patrick, *The Fragments of Heraclitus* (1889, Bywater Greek text; Internet Archive, public domain)",
        "editorial_note": (
            "Pilot: 12 curated Pratibha-layer fragments (Logos, fire, river, war, harmony, soul, Delphi); "
            "remaining units are structural_draft from EPUB import + template enrichment."
        ),
        "coverage": "12 pilot + 116 structural_draft",
        "license": "public_domain",
        "sell_ready_tier": "green",
        "pd_alternative": None,
        "status": "in_corpus",
        "links": [
            {
                "label": "Internet Archive — Patrick 1889",
                "url": "https://archive.org/details/fragmentsofworko00hera",
            },
            {
                "label": "Pilot manifest",
                "url": "data/raw_texts/heraclitus_pilot/manifest.json",
            },
        ],
    },
    {
        "id": "isavasya_upanishad",
        "collection": "Isavasya Upanishad",
        "tradition": "Śukla Yajurveda Upaniṣad",
        "original_work": "Īśāvāsya / Īśopaniṣad (Isha Upanishad)",
        "anchor_translation": (
            "Pratibha editorial English; Sanskrit mantras (Devanagari) and transliteration "
            "from Shlokam.org — Isha Upanishad"
        ),
        "sanskrit_source": "Shlokam.org — Devanagari, IAST, and reference gloss per mantra",
        "editorial_note": "Curated Pratibha manuscript; commentary and resonances are editorial.",
        "license": "mixed",
        "sell_ready_tier": "yellow",
        "pd_alternative": "Max Müller, *Sacred Books of the East* vol. 1 (Vājasaneyi / Īśā Upaniṣad, 1879, public domain)",
        "status": "in_corpus",
        "links": [
            {
                "label": "Shlokam.org — Isha Upanishad",
                "url": "https://shlokam.org/text/isha-upanishad.htm",
            },
            {
                "label": "Sacred-texts — SBE vol. 1 (Īśā)",
                "url": "https://sacred-texts.com/hin/sbe01/index.htm",
            },
        ],
    },
    {
        "id": "know_yourself_ibn_arabi_balyani",
        "collection": "Know Yourself (Ibn Arabi / Balyani)",
        "tradition": "Sufi / Arabic",
        "original_work": "ʿAbd al-Raḥmān al-Balyānī; Ibn ʿArabī tradition",
        "anchor_translation": "Cecilia Twinch, *Know Yourself: An Explanation of the Oneness of Being* (Beshara, 2021)",
        "editorial_note": "Pearl-style units; Pratibha study layers are editorial.",
        "license": "attributed_excerpt",
        "sell_ready_tier": "red",
        "pd_alternative": None,
        "status": "in_corpus",
    },
    {
        "id": "mandukya_upanishad_and_gaudapada_karika",
        "collection": "Mandukya Upanishad and Gaudapada Karika",
        "tradition": "Upaniṣadic / Advaita",
        "original_work": "Māṇḍūkya Upaniṣad + Gauḍapāda Kārikā",
        "anchor_translation": "Pratibha editorial English (manuscript in data/raw_texts)",
        "sanskrit_source": "Received Upaniṣad and Kārikā text (Devanagari / IAST)",
        "editorial_note": "Includes ajātivāda framing; commentary is Pratibha editorial.",
        "license": "mixed",
        "sell_ready_tier": "green",
        "pd_alternative": "Max Müller, SBE vol. 34 (*Māṇḍūkya*, 1894) — optional PD English reference",
        "status": "in_corpus",
    },
    {
        "id": "phaedo_plato",
        "collection": "Phaedo (Plato)",
        "tradition": "Greek / Platonic",
        "original_work": "Plato, *Phaedo*",
        "anchor_translation": "Benjamin Jowett (Project Gutenberg #1658, public domain)",
        "editorial_note": "Pratibha layers are editorial study annotations.",
        "license": "public_domain",
        "sell_ready_tier": "green",
        "pd_alternative": None,
        "status": "in_corpus",
        "links": [{"label": "Project Gutenberg #1658", "url": "https://www.gutenberg.org/ebooks/1658"}],
    },
    {
        "id": "dogen_shobogenzo",
        "collection": "Dōgen — Shōbōgenzō",
        "tradition": "Japanese Zen / Sōtō",
        "original_work": "Dōgen, *Shōbōgenzō* (Treasury of the True Dharma Eye)",
        "anchor_translation": "Pratibha editorial English from classical Japanese (Kokubasha 1896 PD text in data/raw_texts)",
        "editorial_note": "Pilot fascicles: Genjōkōan, Bendōwa, Uji, and related chapters; Pratibha commentary and practice layers are editorial.",
        "license": "mixed",
        "sell_ready_tier": "green",
        "pd_alternative": None,
        "status": "in_corpus",
    },
    {
        "id": "meister_eckhart",
        "collection": "Meister Eckhart",
        "tradition": "Christian mysticism / Middle High German",
        "original_work": "Meister Eckhart, *Von Abegescheidenheit* and *Von Armûot des Geistes*",
        "anchor_translation": "Franz Pfeiffer, *Deutsche Mystiker des vierzehnten Jahrhunderts*, vol. 2 (1857, public domain)",
        "editorial_note": "MHG source in Original layer; Pratibha English translation, commentary, and resonances are editorial.",
        "license": "public_domain",
        "sell_ready_tier": "green",
        "pd_alternative": None,
        "status": "in_corpus",
        "links": [
            {
                "label": "Internet Archive — Pfeiffer 1857",
                "url": "https://archive.org/details/deutschemystike01mystgoog",
            }
        ],
    },
    {
        "id": "plotinus_enneads",
        "collection": "Plotinus Enneads",
        "tradition": "Greek Neoplatonic",
        "original_work": "Plotinus, *Enneads*",
        "anchor_translation": "Stephen MacKenna & B. S. Page (Internet Classics Archive / MIT, public domain)",
        "sanskrit_source": None,
        "editorial_note": "Pilot corpus: I.6 (Beauty), V.1 (Three Hypostases), VI.9 (On the Good) — 32 Pratibha-layer units from MacKenna & Page (MIT + Delphi epub for VI.9).",
        "license": "public_domain",
        "sell_ready_tier": "green",
        "pd_alternative": None,
        "status": "in_corpus",
        "links": [
            {"label": "MIT Classics Enneads", "url": "https://classics.mit.edu/Plotinus/enneads.html"},
            {"label": "Pilot manifest", "url": "data/raw_texts/plotinus_pilot/manifest.json"},
        ],
    },
    {
        "id": "rumi_mathnawi",
        "collection": "Rūmī — Mathnawī-yi Maʿnawī",
        "tradition": "Sufi / Persian",
        "original_work": "Jalāl al-Dīn Rūmī, *Mathnawī-yi Maʿnawī*",
        "anchor_translation": "Pratibha editorial English; Persian from Ganjoor.net (PD source)",
        "editorial_note": "Pilot units; translation layer flagged UNVERIFIED pending Persian review. Structural draft until verified.",
        "license": "mixed",
        "sell_ready_tier": "yellow",
        "pd_alternative": None,
        "status": "in_corpus",
    },
    {
        "id": "milarepa_songs",
        "collection": "Milarepa — Songs",
        "tradition": "Tibetan Buddhist / Kagyü",
        "original_work": "Jetsün Milarepa, *Jetsun-Kahbum* (Life Story and Songs)",
        "anchor_translation": "Kazi Dawa-Samdup (trans.), W.Y. Evans-Wentz (ed.), *Tibet's Great Yogi Milarepa* (1928, public domain)",
        "editorial_note": "Pilot: 8 songs from Chapter X (Meditation in Solitude). Evans-Wentz biblical style; Pratibha translation and commentary are editorial. Snow Song and Six-Bardo songs appear only as references in Ch. XI of this edition.",
        "license": "public_domain",
        "sell_ready_tier": "green",
        "pd_alternative": None,
        "status": "in_corpus",
        "links": [
            {
                "label": "Internet Archive — Evans-Wentz 1928",
                "url": "https://archive.org/details/dli.ministry.06735",
            }
        ],
    },
    {
        "id": "heart_sutra",
        "collection": "Heart Sūtra",
        "tradition": "Mahāyāna / Prajñāpāramitā (Sanskrit)",
        "original_work": "Prajñāpāramitāhṛdaya (Heart Sūtra), shorter recension",
        "anchor_translation": "F. Max Müller, *Buddhist Mahâyâna Texts* (Sacred Books of the East vol. 49, 1894, public domain)",
        "sanskrit_source": "Sanskrit (IAST) source-verified from GRETIL shorter recension; Devanagari not fully source-verified in this pilot",
        "editorial_note": "Pilot: 3 units on emptiness (form=emptiness), no-attainment, and the Gate-gate mantra. Pratibha translation and study layers are editorial; PD Müller anchor retained per unit.",
        "coverage": "3 pilot units",
        "license": "public_domain",
        "sell_ready_tier": "green",
        "pd_alternative": None,
        "status": "in_corpus",
        "links": [
            {"label": "GRETIL — Prajñāpāramitāhṛdaya", "url": "https://gretil.sub.uni-goettingen.de/gretil.html"},
            {"label": "Internet Archive — SBE vol. 49 (Müller 1894)", "url": "https://archive.org/details/buddhistmahayana49cowe"},
            {"label": "Pilot manifest", "url": "data/raw_texts/heart_sutra_pilot/manifest.json"},
        ],
    },
    {
        "id": "nagarjuna_mulamadhyamakakarika",
        "collection": "Nāgārjuna — Mūlamadhyamakakārikā",
        "tradition": "Madhyamaka (Sanskrit)",
        "original_work": "Nāgārjuna, *Mūlamadhyamakakārikā* (Fundamental Verses on the Middle Way, c. 150–250 CE)",
        "anchor_translation": "Pratibha original English rendering from the Sanskrit (no public-domain English of these chapters exists)",
        "sanskrit_source": "Sanskrit (IAST) source-verified from GRETIL critical text (chapters 18, 24, 25)",
        "editorial_note": "Pilot: 9 verses on no-self (ch. 18), emptiness and the two truths (ch. 24), and nirvāṇa (ch. 25). Translation is an original Pratibha rendering; flag for scholarly review against a published translation.",
        "coverage": "9 pilot units",
        "license": "mixed",
        "sell_ready_tier": "orange",
        "pd_alternative": "PD Sanskrit (GRETIL / Bibliotheca Buddhica de la Vallée Poussin 1903–13); no PD English — Pratibha English is the sell-ready layer",
        "status": "in_corpus",
        "links": [
            {"label": "GRETIL — Mūlamadhyamakakārikā", "url": "https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_nAgArjuna-mUlamadhyamakakArikA.htm"},
            {"label": "Pilot manifest", "url": "data/raw_texts/nagarjuna_mmk_pilot/manifest.json"},
        ],
    },
    {
        "id": "shantideva_bodhicaryavatara",
        "collection": "Śāntideva — Bodhicaryāvatāra",
        "tradition": "Mahāyāna / Madhyamaka (Sanskrit)",
        "original_work": "Śāntideva, *Bodhicaryāvatāra* (Entering the Bodhisattva's Way, c. 700 CE)",
        "anchor_translation": "L. D. Barnett, *The Path of Light* (John Murray, 1909, public domain)",
        "sanskrit_source": "Source-language basis noted per unit (Sanskrit, chs. VIII–IX); per-verse Devanagari not source-verified in this pilot",
        "editorial_note": "Pilot: 8 units from ch. VIII (meditation, self–other exchange) and ch. IX (wisdom, two truths, dream/emptiness). Barnett PD anchor retained; Pratibha translation lightly modernizes it.",
        "coverage": "8 pilot units",
        "license": "public_domain",
        "sell_ready_tier": "green",
        "pd_alternative": None,
        "status": "in_corpus",
        "links": [
            {"label": "Internet Archive — Barnett, The Path of Light (1909)", "url": "https://archive.org/details/pathoflightrende00shanuoft"},
            {"label": "Pilot manifest", "url": "data/raw_texts/bodhicaryavatara_pilot/manifest.json"},
        ],
    },
    {
        "id": "tilopa_mahamudra",
        "collection": "Tilopa — Mahāmudrā Upadeśa",
        "tradition": "Tibetan Buddhist / Kagyü (Mahāmudrā)",
        "original_work": "Tilopa, *Mahāmudropadeśa* (Ganges Mahāmudrā), teaching to Nāropa",
        "anchor_translation": "Pratibha original editorial rendering (no clean public-domain English/critical edition source-verified for this pilot)",
        "sanskrit_source": "Tibetan/Sanskrit basis noted per unit; per-line script NOT source-verified — FLAG FOR SCHOLARLY REVIEW",
        "editorial_note": "Pilot: 3 units on non-meditation, mind-like-space, and the guru's grace / self-recognition. Original editorial rendering; needs verification against a critical edition before publication.",
        "coverage": "3 pilot units",
        "license": "mixed",
        "sell_ready_tier": "orange",
        "pd_alternative": "Tibetan source (e.g. Derge Tengyur) is out of copyright; Pratibha English is the sell-ready layer pending scholarly review",
        "status": "in_corpus",
        "links": [
            {"label": "Pilot manifest", "url": "data/raw_texts/tilopa_mahamudra_pilot/manifest.json"},
        ],
    },
    {
        "id": "chandogya_upanishad",
        "collection": "Chāndogya Upaniṣad",
        "tradition": "Śukla Yajurveda Upaniṣad / Vedānta",
        "original_work": "Chāndogya Upaniṣad (Khāndogya-upanishad)",
        "anchor_translation": "F. Max Müller, *The Upanishads*, Part 1 (Sacred Books of the East vol. 1, 1879, public domain)",
        "sanskrit_source": "Received Chāndogya text (Devanagari / IAST in Pratibha units)",
        "editorial_note": "Pilot: Om/udgitha, Sāṇḍilya-vidyā, Uddālaka–Śvetaketu (*tat tvam asi* arc), Prajāpati–Indra. Pratibha translation and commentary are editorial.",
        "license": "public_domain",
        "sell_ready_tier": "green",
        "pd_alternative": None,
        "status": "in_corpus",
        "links": [
            {
                "label": "Internet Archive — Müller Upanishads vol. 1",
                "url": "https://archive.org/details/upanishads00mlgoog",
            },
            {
                "label": "Pilot manifest",
                "url": "data/raw_texts/chandogya_pilot/manifest.json",
            },
        ],
    },
    {
        "id": "pratyabhijnahrdayam",
        "collection": "Pratyabhijnahrdayam",
        "tradition": "Kashmir Śaiva",
        "original_work": "Kṣemarāja, *Pratyabhijñāhṛdayam* (11th c.)",
        "anchor_translation": "Pratibha editorial English; Sanskrit sūtras in IAST / Devanagari",
        "sanskrit_source": "Received text in Pratibha manuscript",
        "editorial_note": "Commentary and cross-tradition resonances are editorial.",
        "license": "mixed",
        "sell_ready_tier": "orange",
        "pd_alternative": "KSTS Sanskrit edition (1918, public domain); no PD English — Jaideva Singh (1980) is copyrighted",
        "status": "in_corpus",
    },
    {
        "id": "siva_sutra",
        "collection": "Siva Sutra",
        "tradition": "Kashmir Śaiva",
        "original_work": "Śiva Sūtras (attributed to Vasugupta)",
        "anchor_translation": "Conor Byrnes — translation & commentary",
        "editorial_note": "Śāmbhavopāya chapter; conceived and authored in Pratibha.",
        "license": "mixed",
        "sell_ready_tier": "green",
        "pd_alternative": None,
        "status": "in_corpus",
        "conceived_by_conor": True,
    },
    {
        "id": "svetasvatara_upanishad",
        "collection": "Svetasvatara Upanishad",
        "tradition": "Upaniṣadic / theistic Vedānta",
        "original_work": "Śvetāśvatara Upaniṣad",
        "anchor_translation": "Pratibha editorial; philological context per S. Radhakrishnan in manuscript header",
        "sanskrit_source": "Received Upaniṣad text",
        "editorial_note": "Curated anchor units; Pratibha departures noted in manuscript.",
        "license": "mixed",
        "sell_ready_tier": "yellow",
        "pd_alternative": "Max Müller, *Sacred Books of the East* vol. 15 (Śvetāśvatara, 1884, public domain)",
        "status": "in_corpus",
        "links": [{"label": "Sacred-texts — SBE vol. 15", "url": "https://sacred-texts.com/hin/sbe15/index.htm"}],
    },
    {
        "id": "tantrasara",
        "collection": "Tantrasāra",
        "tradition": "Kashmir Śaiva / Tantra",
        "original_work": "Abhinavagupta, *Tantrasāra*",
        "anchor_translation": "Conor Byrnes — translation & commentary (informed by Christopher Wallis)",
        "editorial_note": "From the Śastra vault; conceived and authored in Pratibha.",
        "license": "mixed",
        "sell_ready_tier": "green",
        "pd_alternative": None,
        "status": "in_corpus",
        "coverage": "19 units (Āhnikas 1–5)",
        "conceived_by_conor": True,
    },
    {
        "id": "tao_te_ching",
        "collection": "Tao Te Ching",
        "tradition": "Chinese Daoist",
        "original_work": "Lǎozǐ, *Dào Dé Jīng* 道德經 (81 chapters)",
        "anchor_translation": "Pratibha editorial English; James Legge (1891) as comparative reference (Lau, Mitchell noted in commentary)",
        "sanskrit_source": "Traditional Chinese characters in Original layer",
        "editorial_note": "Full 81 chapters in corpus. Wave A curated pilot chapters plus Wave B LLM-generated units; commentary and practice layers are Pratibha editorial.",
        "coverage": "81 of 81 chapters",
        "coverage_detail": "All chapters from the Pratibha manuscript (tao_te_ching_md_001–081). Wave A curated; Wave B generated with resume-safe batch pipeline.",
        "license": "mixed",
        "sell_ready_tier": "yellow",
        "pd_alternative": "James Legge, *Sacred Books of the East* vol. 39 (1891) — Project Gutenberg #216",
        "status": "in_corpus",
        "links": [{"label": "Project Gutenberg #216 (Legge)", "url": "https://www.gutenberg.org/ebooks/216"}],
    },
    {
        "id": "the_book_of_chuang_tzu",
        "collection": "The Book of Chuang Tzu",
        "tradition": "Chinese Daoist",
        "original_work": "Zhuangzi (*Nanhua Jing* 莊子)",
        "anchor_translation": "Herbert A. Giles, *Chuang Tzu: Mystic, Moralist, and Social Reformer* (1889; Project Gutenberg #59709, public domain)",
        "editorial_note": "Chapter-level units (ctz_*); Pratibha commentary editorial. Curated Pratibha units (zhuangzi_md_*) use Giles-based editorial English.",
        "license": "public_domain",
        "sell_ready_tier": "green",
        "pd_alternative": None,
        "status": "in_corpus",
        "links": [{"label": "Project Gutenberg #59709 (Giles)", "url": "https://www.gutenberg.org/ebooks/59709"}],
    },
    {
        "id": "vijnana_bhairava",
        "collection": "Vijnana Bhairava",
        "tradition": "Kashmir Śaiva / Trika",
        "original_work": "Vijñānabhairavatantra",
        "anchor_translation": "Christopher D. Wallis, *Vijñānabhairava* translation (project PDF: VBT+translation+WALLIS-2.pdf)",
        "sanskrit_source": "IAST / Devanagari in units (source-verified where extracted from PDF)",
        "editorial_note": "112 Yuktis; Pratibha commentary and practice layers are editorial.",
        "license": "attributed_excerpt",
        "sell_ready_tier": "orange",
        "pd_alternative": "KSTS Sanskrit edition (1918, public domain); Paul Reps (1957) and Jaideva Singh (1979) are copyrighted",
        "status": "in_corpus",
        "links": [{"label": "Internet Archive — KSTS Vijñānabhairava", "url": "https://archive.org/details/dli.ernet.242056"}],
    },
    {
        "id": "yoga_spandakarika",
        "collection": "Yoga Spandakarika",
        "tradition": "Kashmir Śaiva",
        "original_work": "Spandakārikā (Kallaṭa / Vasugupta tradition)",
        "anchor_translation": "Daniel Odier, *Yoga Spandakarika* (Inner Traditions, 2005) — project EPUB",
        "editorial_note": "Stanza-level units; Pratibha enrichment is editorial.",
        "license": "attributed_excerpt",
        "sell_ready_tier": "orange",
        "pd_alternative": "KSTS Sanskrit (public domain); no PD English — Jaideva Singh (1980) is copyrighted",
        "status": "in_corpus",
    },
    {
        "id": "yoginihrdaya",
        "collection": "Yoginīhṛdaya",
        "tradition": "Śrī Vidyā / Tantra",
        "original_work": "Yoginīhṛdaya",
        "anchor_translation": "André Padoux & Roger-Orphé Jeanty, *The Heart of the Yoginī* (OUP, 2013)",
        "sanskrit_source": "IAST from Padoux/Dvivedī edition; Devanagari editorially reconstructed",
        "editorial_note": "Body uses Padoux anchor translation; Pratibha Translation is a fresh rendering.",
        "license": "attributed_excerpt",
        "sell_ready_tier": "orange",
        "pd_alternative": "No PD English translation; Pratibha Translation layer is the sell-ready English",
        "status": "in_corpus",
    },
    {
        "id": "patanjali_yoga_sutras",
        "collection": "Patañjali Yoga Sūtras",
        "tradition": "Yoga / Sāṃkhya",
        "original_work": "Patañjali, *Yoga Sūtras*",
        "anchor_translation": "Swami Satchidananda, *The Yoga Sutras of Patanjali* (Integral Yoga, 1978)",
        "editorial_note": "Full 195 sūtras. Pada 1 and Sādhana ≤2.30 use Dvivedi (1890) anchor; 2.31+ Satchidananda-informed Pratibha English.",
        "license": "attributed_excerpt",
        "sell_ready_tier": "yellow",
        "pd_alternative": "Manilal Nabhubhai Dvivedi (1890, public domain) or Swami Vivekananda, *Raja Yoga* (1896)",
        "status": "in_corpus",
        "links": [
            {"label": "Internet Archive — Dvivedi 1890", "url": "https://archive.org/details/yogaSutraOfPatanjali"},
            {"label": "Internet Archive — Vivekananda Raja Yoga", "url": "https://archive.org/details/in.ernet.dli.2015.20715"},
        ],
    },
]

LICENSE_LABELS = {
    "public_domain": "Public domain anchor text",
    "attributed_excerpt": "Copyrighted translation — attributed excerpts for study",
    "mixed": "Mixed: received Sanskrit + editorial / attributed English",
    "original_editorial": "Original Pratibha editorial",
}

SELL_READY_TIER_LABELS = {
    "green": "Sell-ready — PD anchor or original Pratibha work",
    "yellow": "Swap recommended — PD alternative available",
    "orange": "Use Pratibha English — PD Sanskrit only",
    "red": "License required — no PD English",
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
        tier = entry.get("sell_ready_tier") or "yellow"
        row["sell_ready_tier"] = tier
        row["sell_ready_tier_label"] = SELL_READY_TIER_LABELS.get(tier, tier)
        row["pd_alternative"] = entry.get("pd_alternative")
        row["conceived_by_conor"] = bool(entry.get("conceived_by_conor"))
        items.append(row)
    in_corpus = sum(1 for i in items if i["passages_in_corpus"] > 0)
    tier_counts: dict[str, int] = {}
    for i in items:
        if i["passages_in_corpus"] > 0:
            t = i["sell_ready_tier"]
            tier_counts[t] = tier_counts.get(t, 0) + 1
    return {
        "items": items,
        "summary": {
            "collections_documented": len(items),
            "collections_in_corpus": in_corpus,
            "total_passages": sum(counts.values()),
            "sell_ready_tiers": tier_counts,
        },
    }

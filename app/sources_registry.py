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
        "editorial_note": "Short English renderings anchor each unit; Pratibha commentary and practice are editorial.",
        "license": "public_domain",
        "sell_ready_tier": "green",
        "pd_alternative": None,
        "status": "in_corpus",
        "links": [
            {
                "label": "Internet Archive — Patrick 1889",
                "url": "https://archive.org/details/fragmentsofworko00hera",
            }
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
        "id": "plotinus_enneads",
        "collection": "Plotinus Enneads",
        "tradition": "Greek Neoplatonic",
        "original_work": "Plotinus, *Enneads*",
        "anchor_translation": "Stephen MacKenna & B. S. Page (Internet Classics Archive / MIT, public domain)",
        "sanskrit_source": None,
        "editorial_note": "Section-level units; translation body from MIT text; maturity varies by tractate.",
        "license": "public_domain",
        "sell_ready_tier": "green",
        "pd_alternative": None,
        "status": "in_corpus",
        "links": [{"label": "MIT Classics Enneads", "url": "https://classics.mit.edu/Plotinus/enneads.html"}],
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

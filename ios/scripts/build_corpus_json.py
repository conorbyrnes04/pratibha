#!/usr/bin/env python3
"""Convert the canonical corpus (data/canonical/index.jsonl) into a single
app-ready corpus.json bundled into the Pratibhā iOS app.

Run from the repo root:
    uv run python ios/scripts/build_corpus_json.py

Output: ios/Pratibha/Resources/corpus.json
"""
from __future__ import annotations

import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INDEX = os.path.join(REPO_ROOT, "data", "canonical", "index.jsonl")
OUT = os.path.join(REPO_ROOT, "ios", "Pratibha", "Resources", "corpus.json")

# Curated display metadata per collection (proper diacritics + tradition +
# a one-line orientation + a stable reading order). Keyed by work_id.
COLLECTIONS: dict[str, dict] = {
    "siva_sutra": {
        "title": "Śiva Sūtra",
        "tradition": "Nondual Śaiva Tantra",
        "blurb": "Vasugupta's aphorisms — three doors into one recognition.",
        "order": 1,
    },
    "vijnana_bhairava": {
        "title": "Vijñāna Bhairava Tantra",
        "tradition": "Nondual Śaiva Tantra",
        "blurb": "112 dhāraṇās — techniques for entering the space between.",
        "order": 2,
    },
    "yoga_spandakarika": {
        "title": "Spanda-kārikā",
        "tradition": "Spanda school",
        "blurb": "The subtle tremor at the root of all experience.",
        "order": 3,
    },
    "pratyabhijnahrdayam": {
        "title": "Pratyabhijñāhṛdayam",
        "tradition": "Pratyabhijñā",
        "blurb": "Kṣemarāja's Heart of Recognition — a circle you complete.",
        "order": 4,
    },
    "astavakra_gita": {
        "title": "Aṣṭāvakra Gītā",
        "tradition": "Advaita Vedānta",
        "blurb": "Radical non-dual dialogue on the witness and freedom.",
        "order": 5,
    },
    "isavasya_upanishad": {
        "title": "Īśāvāsya Upaniṣad",
        "tradition": "Upaniṣadic",
        "blurb": "The whole enveloped by the Lord; renounce and enjoy.",
        "order": 6,
    },
    "svetasvatara_upanishad": {
        "title": "Śvetāśvatara Upaniṣad",
        "tradition": "Upaniṣadic",
        "blurb": "Two birds on one tree — witness and enjoyer.",
        "order": 7,
    },
    "mandukya_upanishad_and_gaudapada_karika": {
        "title": "Māṇḍūkya Upaniṣad & Gauḍapāda Kārikā",
        "tradition": "Advaita / Ajātivāda",
        "blurb": "The four states of consciousness and the unborn.",
        "order": 8,
    },
    "heraclitus_fragments": {
        "title": "Heraclitus — Fragments",
        "tradition": "Pre-Socratic Greek",
        "blurb": "Fire, flux, and the logos that governs all.",
        "order": 9,
    },
    "epictetus_works": {
        "title": "Epictetus — Enchiridion",
        "tradition": "Stoic",
        "blurb": "What is up to us, and what is not.",
        "order": 10,
    },
    "phaedo_plato": {
        "title": "Phaedo",
        "tradition": "Platonic",
        "blurb": "Socrates on death, the soul, and the philosophic life.",
        "order": 11,
    },
    "tao_te_ching": {
        "title": "Dào Dé Jīng",
        "tradition": "Daoist",
        "blurb": "The way that can be named is not the eternal way.",
        "order": 12,
    },
    "the_book_of_chuang_tzu": {
        "title": "Zhuāngzǐ",
        "tradition": "Daoist",
        "blurb": "Wandering free and easy through the transformation of things.",
        "order": 13,
    },
    "know_yourself_ibn_arabi_balyani": {
        "title": "Know Yourself",
        "tradition": "Sufi (Ibn ʿArabī / al-Balayānī)",
        "blurb": "He who knows himself knows his Lord.",
        "order": 14,
    },
    "senegalese_animism": {
        "title": "Senegalese Animism",
        "tradition": "Serer / Senegambian",
        "blurb": "Roog, the unaddressed sky, and the spirits you pour to at the baobab.",
        "order": 15,
    },
    "pulaar_tradition": {
        "title": "Pulaar Tradition",
        "tradition": "Fulɓe / Pulaar (pre-Islamic remnants)",
        "blurb": "The remaining cult is the herd — cattle-pen, green-leaf greeting, ancestor interdit.",
        "order": 16,
    },
    "pulaar_texts": {
        "title": "Pulaar Texts",
        "tradition": "Futa Toro Pulaar",
        "blurb": "won ko wonnō do — tale formula, a father's counsel, and mallol from Gaden 1913.",
        "order": 17,
    },
}


def clean(value) -> str:
    if value is None:
        return ""
    return str(value).strip()


def main() -> int:
    if not os.path.isfile(INDEX):
        print(f"ERROR: {INDEX} not found", file=sys.stderr)
        return 1

    passages: list[dict] = []
    counts: dict[str, int] = {}
    unknown: set[str] = set()

    with open(INDEX, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            work_id = clean(d.get("work_id"))
            if work_id not in COLLECTIONS:
                unknown.add(work_id)
                continue

            devanagari = clean(d.get("sanskrit_devanagari"))
            iast = clean(d.get("sanskrit_iast"))
            translation = clean(d.get("translation_literal"))
            source_excerpt = clean(d.get("source_excerpt"))
            # For commentary_text (Greek/Sufi/Daoist) the primary text lives in
            # source_excerpt; fall back so every passage has a "primary" line.
            primary = translation or source_excerpt

            passage = {
                "id": clean(d.get("unit_id")),
                "workId": work_id,
                "title": clean(d.get("title")) or clean(d.get("unit_label")),
                "unitLabel": clean(d.get("unit_label")),
                "unitType": clean(d.get("unit_type")) or "passage",
                "category": clean(d.get("category")) or "root_text",
                "devanagari": devanagari,
                "iast": iast,
                "primary": primary,
                "translation": translation,
                "sourceExcerpt": source_excerpt,
                "commentary": clean(d.get("commentary")),
                "thesis": clean(d.get("thesis")),
                "insight": clean(d.get("insight")),
                "practice": clean(d.get("practice")),
                "section": clean((d.get("provenance") or {}).get("section")),
                "themes": [t for t in (d.get("themes") or []) if clean(t)][:8],
                "qualityScore": int(d.get("quality_score") or 0),
            }
            if not passage["id"] or not passage["title"]:
                continue
            passages.append(passage)
            counts[work_id] = counts.get(work_id, 0) + 1

    collections = []
    for work_id, meta in COLLECTIONS.items():
        collections.append({
            "id": work_id,
            "title": meta["title"],
            "tradition": meta["tradition"],
            "blurb": meta["blurb"],
            "order": meta["order"],
            "count": counts.get(work_id, 0),
        })
    collections.sort(key=lambda c: c["order"])

    out = {
        "version": 1,
        "passageCount": len(passages),
        "collectionCount": len([c for c in collections if c["count"] > 0]),
        "collections": collections,
        "passages": passages,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, separators=(",", ":"))

    size_kb = os.path.getsize(OUT) / 1024
    print(f"Wrote {len(passages)} passages across "
          f"{out['collectionCount']} collections -> {OUT} ({size_kb:.0f} KB)")
    if unknown:
        print(f"WARNING: skipped unknown work_ids: {sorted(unknown)}", file=sys.stderr)
    for c in collections:
        print(f"  {c['count']:>4}  {c['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

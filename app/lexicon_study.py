"""Build language-separated flashcard decks from lexicon lemmas."""

from __future__ import annotations

from typing import Any

from .lexicon_api import get_lexicon

MATURITY_RANK = {
    "structural_draft": 0,
    "strong_draft": 1,
    "canonical": 2,
}

DECK_META: dict[str, dict[str, str]] = {
    "sanskrit": {
        "id": "sanskrit",
        "label": "Sanskrit",
        "native_label": "संस्कृतम्",
        "blurb": "Devanagari forms and Indic senses — dharma, karma, yoga, and the rest of the manuscript’s shared spine.",
        "script_hint": "devanagari",
    },
    "greek": {
        "id": "greek",
        "label": "Greek",
        "native_label": "Ἑλληνική",
        "blurb": "λόγος, νοῦς, φύσις — terms that order Greek and Christian mystical speech.",
        "script_hint": "greek",
    },
    "chinese": {
        "id": "chinese",
        "label": "Chinese",
        "native_label": "中文",
        "blurb": "道, 德, 無為 — Daoist and classical Chinese vocabulary as living path-words.",
        "script_hint": "chinese",
    },
    "arabic": {
        "id": "arabic",
        "label": "Arabic",
        "native_label": "العربية",
        "blurb": "Tawḥīd, fanāʾ — sparse, precise terms from the Sufi and philosophical stream.",
        "script_hint": "arabic",
    },
    "german": {
        "id": "german",
        "label": "German",
        "native_label": "Deutsch",
        "blurb": "Eckhart’s Gelassenheit and kindred releasement vocabulary.",
        "script_hint": "latin",
    },
}


def _maturity_ok(maturity: str, minimum: str) -> bool:
    return MATURITY_RANK.get(maturity, 0) >= MATURITY_RANK.get(minimum, 1)


def assign_deck(scripts: dict[str, Any]) -> str | None:
    """Prefer native script family; IAST-only Indic joins Sanskrit."""
    if not isinstance(scripts, dict):
        return None
    if scripts.get("devanagari"):
        return "sanskrit"
    if scripts.get("greek"):
        return "greek"
    if scripts.get("chinese"):
        return "chinese"
    if scripts.get("arabic"):
        return "arabic"
    if scripts.get("iast"):
        return "sanskrit"
    if scripts.get("latin"):
        return "german"
    return None


def _front_forms(scripts: dict[str, Any], deck_id: str) -> dict[str, str]:
    scripts = scripts if isinstance(scripts, dict) else {}
    iast = str(scripts.get("iast") or "").strip()
    latin = str(scripts.get("latin") or "").strip()
    pinyin = str(scripts.get("pinyin") or "").strip()

    if deck_id == "sanskrit":
        native = str(scripts.get("devanagari") or "").strip() or iast
        roman = iast or latin
        script_class = "devanagari" if scripts.get("devanagari") else "latin"
    elif deck_id == "greek":
        native = str(scripts.get("greek") or "").strip() or latin
        roman = latin or iast
        script_class = "greek"
    elif deck_id == "chinese":
        native = str(scripts.get("chinese") or "").strip()
        roman = pinyin or latin
        script_class = "chinese"
    elif deck_id == "arabic":
        native = str(scripts.get("arabic") or "").strip() or latin
        roman = latin or iast
        script_class = "arabic"
    else:
        native = latin or iast
        roman = latin or iast
        script_class = "latin"

    return {
        "native": native,
        "roman": roman if roman != native else "",
        "script_class": script_class,
    }


def _recognition_card(
    lemma: dict[str, Any],
    sense: dict[str, Any],
    deck_id: str,
) -> dict[str, Any]:
    forms = _front_forms(lemma.get("scripts") or {}, deck_id)
    sense_id = str(sense.get("id") or "")
    return {
        "id": f"{sense_id}:recognition",
        "sense_id": sense_id,
        "lemma_id": str(lemma.get("id") or ""),
        "deck_id": deck_id,
        "mode": "recognition",
        "maturity": str(lemma.get("maturity") or ""),
        "traditions": list(sense.get("traditions") or lemma.get("traditions") or []),
        "front": {
            **forms,
            "prompt": "What does this term mean in this sense?",
        },
        "back": {
            "label": str(sense.get("label") or ""),
            "short": str(sense.get("short") or ""),
            "etymology": str(sense.get("etymology") or ""),
            "traps": [str(t) for t in (sense.get("traps") or []) if str(t).strip()],
            "exemplars": [str(x) for x in (sense.get("exemplars") or []) if str(x).strip()][:3],
        },
    }


def _trap_card(
    lemma: dict[str, Any],
    sense: dict[str, Any],
    deck_id: str,
    trap: str,
    trap_index: int,
) -> dict[str, Any]:
    forms = _front_forms(lemma.get("scripts") or {}, deck_id)
    sense_id = str(sense.get("id") or "")
    display = forms["roman"] or forms["native"] or str(lemma.get("id") or "")
    return {
        "id": f"{sense_id}:trap:{trap_index}",
        "sense_id": sense_id,
        "lemma_id": str(lemma.get("id") or ""),
        "deck_id": deck_id,
        "mode": "trap",
        "maturity": str(lemma.get("maturity") or ""),
        "traditions": list(sense.get("traditions") or lemma.get("traditions") or []),
        "front": {
            **forms,
            "prompt": f"Why is this a trap for {display}?",
            "trap": trap,
        },
        "back": {
            "label": str(sense.get("label") or ""),
            "short": str(sense.get("short") or ""),
            "etymology": str(sense.get("etymology") or ""),
            "traps": [str(t) for t in (sense.get("traps") or []) if str(t).strip()],
            "exemplars": [str(x) for x in (sense.get("exemplars") or []) if str(x).strip()][:3],
            "correction": "That gloss collapses the sense. Hold the short definition instead.",
        },
    }


def _production_card(
    lemma: dict[str, Any],
    sense: dict[str, Any],
    deck_id: str,
) -> dict[str, Any]:
    forms = _front_forms(lemma.get("scripts") or {}, deck_id)
    sense_id = str(sense.get("id") or "")
    return {
        "id": f"{sense_id}:production",
        "sense_id": sense_id,
        "lemma_id": str(lemma.get("id") or ""),
        "deck_id": deck_id,
        "mode": "production",
        "maturity": str(lemma.get("maturity") or ""),
        "traditions": list(sense.get("traditions") or lemma.get("traditions") or []),
        "front": {
            "native": "",
            "roman": "",
            "script_class": forms["script_class"],
            "prompt": "Which sacred term is this?",
            "cue": str(sense.get("short") or ""),
            "sense_label": str(sense.get("label") or ""),
        },
        "back": {
            "label": str(sense.get("label") or ""),
            "short": str(sense.get("short") or ""),
            "etymology": str(sense.get("etymology") or ""),
            "traps": [str(t) for t in (sense.get("traps") or []) if str(t).strip()],
            "exemplars": [str(x) for x in (sense.get("exemplars") or []) if str(x).strip()][:3],
            "native": forms["native"],
            "roman": forms["roman"],
            "script_class": forms["script_class"],
        },
    }


def build_study_payload(minimum_maturity: str = "strong_draft") -> dict[str, Any]:
    """Return decks + cards for the lexicon study surface."""
    payload = get_lexicon()
    lemmas: dict[str, dict[str, Any]] = payload.get("lemmas") or {}

    cards: list[dict[str, Any]] = []
    deck_lemmas: dict[str, set[str]] = {k: set() for k in DECK_META}
    deck_card_counts: dict[str, int] = {k: 0 for k in DECK_META}

    for lid in sorted(lemmas):
        lemma = lemmas[lid]
        if not isinstance(lemma, dict):
            continue
        maturity = str(lemma.get("maturity") or "structural_draft")
        if not _maturity_ok(maturity, minimum_maturity):
            continue
        scripts = lemma.get("scripts") or {}
        deck_id = assign_deck(scripts if isinstance(scripts, dict) else {})
        if not deck_id:
            continue

        senses = [s for s in (lemma.get("senses") or []) if isinstance(s, dict) and s.get("short")]
        if not senses:
            continue

        deck_lemmas[deck_id].add(str(lemma.get("id") or lid))
        for sense in senses:
            recognition = _recognition_card(lemma, sense, deck_id)
            cards.append(recognition)
            deck_card_counts[deck_id] += 1

            traps = [str(t).strip() for t in (sense.get("traps") or []) if str(t).strip()]
            # One trap card per sense (first trap) keeps decks lean and high-signal.
            if traps:
                cards.append(_trap_card(lemma, sense, deck_id, traps[0], 0))
                deck_card_counts[deck_id] += 1

            # Production only when native script differs from a usable roman cue.
            forms = _front_forms(scripts if isinstance(scripts, dict) else {}, deck_id)
            if forms["native"] and (forms["roman"] or forms["native"]):
                cards.append(_production_card(lemma, sense, deck_id))
                deck_card_counts[deck_id] += 1

    decks = []
    for deck_id, meta in DECK_META.items():
        count = deck_card_counts[deck_id]
        if count == 0:
            continue
        sample = next(
            (
                c["front"].get("native")
                for c in cards
                if c["deck_id"] == deck_id and c["mode"] == "recognition" and c["front"].get("native")
            ),
            meta["native_label"],
        )
        decks.append(
            {
                **meta,
                "lemma_count": len(deck_lemmas[deck_id]),
                "card_count": count,
                "sample": sample,
            }
        )

    return {
        "minimum_maturity": minimum_maturity,
        "decks": decks,
        "cards": cards,
        "totals": {
            "decks": len(decks),
            "cards": len(cards),
            "lemmas": sum(len(v) for v in deck_lemmas.values()),
        },
    }

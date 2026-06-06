"""Philological helpers for PD anchor → Pratibha layer enrichment."""

from __future__ import annotations

import re
from typing import Any

# Layer provenance labels (regex-normalized PD derivatives vs template assembly).
PROVENANCE_PATRICK_NORMALIZED = (
    "normalized from Patrick (1889), PD; regex word-modernization, not fresh translation"
)
PROVENANCE_GILES_NORMALIZED = (
    "normalized from Giles (1889), PD; regex word-modernization, not fresh translation"
)
PROVENANCE_TEMPLATE = "template-assembled"
PROVENANCE_HAND_CONSTANT = "hand-authored constant"

# Famous fragments: pre-written cross-tradition resonances (passage-level specificity).
HERACLITUS_RESONANCES: dict[int, list[dict[str, str]]] = {
    1: [
        {
            "citation": "Gospel of John 1:1",
            "resonance": "Both texts treat Logos as an ordering principle that precedes and governs what becomes manifest.",
            "divergence": "John personalizes Logos christologically; Heraclitus keeps it cosmological and immanent in process.",
        },
        {
            "citation": "Plotinus, Enneads V.1.3",
            "resonance": "Intellect and intelligible order are 'heard' before they are argued — contemplative attunement precedes proof.",
            "divergence": "Plotinus ascends to a transcendent One; Heraclitus stays with the tension of becoming.",
        },
    ],
    45: [
        {
            "citation": "Vijnana Bhairava Tantra (harmony-in-opposites dharanas)",
            "resonance": "Both treat apparent opposition as the field in which unity becomes experiential rather than conceptual.",
            "divergence": "The VBT gives contemplative methods; Heraclitus states a cosmological principle without technique.",
        },
        {
            "citation": "Nicholas of Cusa, De docta ignorantia I.9",
            "resonance": "Coincidentia oppositorum names what Heraclitus shows through bow and lyre: unity includes tension.",
            "divergence": "Cusa's move is theological; Heraclitus remains pre-theological and physical-metaphorical.",
        },
    ],
    56: [
        {
            "citation": "Heraclitus B45 (bow and lyre)",
            "resonance": "Same image-cluster: harmony is not absence of conflict but measured counter-tension.",
            "divergence": "B56 generalizes to world-harmony; B45 focuses on the mind's failure to grasp the pattern.",
        },
    ],
}

CHAPTER_INTROS: dict[int, str] = {
    1: (
        "Chapter 1 (*Xiaoyaoyou*) is Zhuangzi's scale argument: capacity depends on the depth of water, wind, and "
        "attention — not on moral rank. The Peng story is not natural history but a test of whether your measure of "
        "the 'realistic' is itself provincial. Giles renders Kun/Peng as Leviathan/Rukh; Pratibha restores received "
        "Chinese names to avoid imported mythic baggage."
    ),
    2: (
        "Chapter 2 (*Qiwulun*) turns to language, perspective, and the famous butterfly dream. Zhuangzi asks whether "
        "distinctions (self/other, waking/dream, right/wrong) are discovered or projected. The chapter is a sustained "
        "attack on fixed epistemic frames — not skepticism for its own sake, but liberation from scale-locked judgment."
    ),
    3: (
        "Chapter 3 (*Yangsheng*) moves from knowing to nourishing life: skill that bypasses anxious calculation "
        "(the cook Ding, the ferryman). Technical mastery appears when the self does not obstruct the work — a "
        "Daoist correction to deliberate over-control."
    ),
}


def clean_ocr(text: str) -> str:
    text = re.sub(r"(\w)-\s+(\w)", r"\1\2", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = text.replace("''", '"').replace('""', '"')
    return text.strip()


def normalize_patrick_heraclitus(anchor: str) -> str:
    """Lightly normalizes the public-domain Patrick (1889) translation — word modernization and OCR cleanup.

    Derivative of PD source, not original translation.
    """
    s = clean_ocr(anchor)
    s = re.sub(r"\buniversal Reason\b", "the Logos", s, flags=re.I)
    s = re.sub(r"\bthis Reason\b", "this Logos", s, flags=re.I)
    s = re.sub(r"\bthe Reason\b", "the Logos", s, flags=re.I)
    s = re.sub(r"\bnotwithstanding\b", "even though", s, flags=re.I)
    s = re.sub(r"\bmen\b", "people", s, flags=re.I)
    s = re.sub(r"\bMen\b", "People", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def normalize_giles_excerpt(anchor: str) -> str:
    """Lightly normalizes the public-domain Giles (1889) translation — word modernization and OCR cleanup.

    Derivative of PD source, not original translation.
    """
    s = clean_ocr(anchor)
    subs = [
        (r"\bLeviathan\b", "Kun"),
        (r"\bleviathan\b", "Kun"),
        (r"\bRukh\b", "Peng"),
        (r"\brukh\b", "Peng"),
        (r"\bCelestial Lake\b", "the Heavenly Pool"),
        (r"\bsouthern ocean\b", "southern darkness"),
        (r"\bRecord of Marvels\b", "old records"),
        (r"\btyphoon\b", "whirlwind"),
    ]
    for pat, rep in subs:
        s = re.sub(pat, rep, s)
    return s.strip()


def heraclitus_key_terms(anchor: str) -> list[dict[str, str]]:
    s = anchor.lower()
    terms: list[dict[str, str]] = []
    if any(k in s for k in ("logos", "reason", "word", "hearing", "heard")):
        terms.append(
            {
                "term": "Logos (λόγος)",
                "definition": (
                    "Greek: speech, account, ratio, intelligible order. In Heraclitus, the Logos is the "
                    "pattern according to which all things occur — not a private doctrine but the world's "
                    "articulation. Patrick's 'Reason' is a Victorian gloss; we use Logos to preserve the "
                    "Greek range (cosmic order + intelligible speech)."
                ),
            }
        )
    if "fire" in s or "lightning" in s or "ever-living" in s:
        terms.append(
            {
                "term": "pyr / cosmic fire",
                "definition": (
                    "Heraclitus's world-ruling fire is not mythic flame alone but measured transformation — "
                    "exchange (πυρὸς τροπαὶ) governed by proportion. Fire names process, not a static element."
                ),
            }
        )
    if any(k in s for k in ("soul", "psyche", "character", "ethos")):
        terms.append(
            {
                "term": "psychē (ψυχή)",
                "definition": (
                    "Soul/breath/life — for Heraclitus often linked to depth of character (ethos) and fate. "
                    "The fragment turns ethics into cosmology: how you live is how you align (or fail) with measure."
                ),
            }
        )
    if any(k in s for k in ("harmony", "opposition", "bow", "lyre", "strife", "war")):
        terms.append(
            {
                "term": "harmoniē (ἁρμονίη)",
                "definition": (
                    "Harmony here is tension held in proportion — the bent bow, tuned lyre. Unity is dynamic, "
                    "not the removal of difference. This is Heraclitus's answer to those who expect peace as sameness."
                ),
            }
        )
    return terms[:4]


def heraclitus_commentary(anchor: str, frag_num: int) -> str:
    s = clean_ocr(anchor).lower()
    parts: list[str] = []

    if any(k in s for k in ("logos", " universal reason", "this reason", "the reason", "word which", "heard it", "have heard")):
        parts.append(
            "Heraclitus insists that wisdom is auditory before it is argumentative: the Logos is already "
            "at work in how things happen, yet people live as if they had no prior encounter with it. "
            "The complaint is not elitism but phenomenology — most consciousness is forgetful, whether "
            "in sleep or in 'waking' busyness."
        )
    if any(k in s for k in ("fire", "lightning", "measure", "transform", "exchange")):
        parts.append(
            "Fire-language names lawful change: the cosmos is not static substance but measured transformation. "
            "What looks like destruction is often conversion governed by proportion — a physics of becoming "
            "that refuses both chaos and immobility."
        )
    if any(k in s for k in ("war", "strife", "conflict", "opposition", "contending", "harmony", "bow", "lyre")):
        parts.append(
            "Opposition is not a failure of order but its instrument. Heraclitus uses craft images (bow, lyre) "
            "to show that tension generates stable function. Peace as mere absence of conflict would collapse the "
            "very structures that make harmony audible."
        )
    if any(k in s for k in ("soul", "character", "ethos", "death", "fate")):
        parts.append(
            "The turn is ethical-cosmological: character is not private style but alignment with the measure "
            "that governs all things. Mortality intensifies the question — finite life must choose whether to "
            "hear the pattern or merely repeat opinion."
        )
    if any(k in s for k in ("one", "all things", "wise")):
        parts.append(
            "The 'one' is not mystical fusion but the single intelligible order within apparent plurality. "
            "To confess that all things are one is to refuse piecemeal metaphysics — yet Heraclitus never "
            "denies the visibility of difference; he reframes it."
        )

    if not parts:
        parts.append(
            "This aphorism compresses a cosmological claim into a single image or paradox. Read it slowly: "
            "Heraclitus is not offering a syllogism but training perception. The fragment asks you to notice "
            "what experience already shows once opinion falls quiet."
        )

    note = (
        f" Anchor: George T.W. Patrick (1889), fragment {frag_num} (Bywater Greek). "
        f"Corpus index HFR_P{frag_num:03d} follows the Diels–Kranz-style numbering used in the Pratibha pilot batch."
    )
    return " ".join(parts) + note


def heraclitus_practice(anchor: str) -> str:
    s = anchor.lower()
    if "hear" in s or "logos" in s or "reason" in s:
        return (
            "Before arguing a point today, pause and write one sentence you hold as obvious — then ask "
            "what experience it actually rests on. Can you hear the claim, not only think it?"
        )
    if "fire" in s or "change" in s:
        return (
            "Choose one situation that feels chaotic. Name one measure or proportion hidden in it "
            "(timing, limit, exchange). Sit with that pattern for two minutes."
        )
    if "harmony" in s or "opposition" in s or "bow" in s:
        return (
            "Identify a tension in your life that you treat as pure conflict. Reframe it as a bow: "
            "what two pulls create the function? Write both pulls without trying to remove either."
        )
    return (
        "Memorize the fragment in one breath. Recite it once on waking and once before sleep, "
        "watching what image or resistance arises — that resistance is part of the teaching."
    )


def strip_commentary_layers(commentary: str) -> str:
    """Return philosophical commentary only — drop embedded Key Terms / Resonances blocks."""
    m = re.search(r"(?i)\n\nKey Terms:", commentary)
    return commentary[: m.start()].strip() if m else commentary.strip()


def chapter_commentary(chapter_n: int, title: str, anchor_excerpt: str) -> str:
    intro = CHAPTER_INTROS.get(chapter_n, "")
    if not intro:
        intro = (
            f"Chapter {chapter_n} ({title}) in Giles's 1889 rendering. Pratibha treats the chapter as a "
            "philosophical movement: read the anchor appendix for the full Victorian translation, "
            "then the Pratibha translation for a modern, source-honest excerpt."
        )
    return intro + (
        " Full chapter text remains in the public-domain appendix for philological comparison; "
        "the display layers do not reproduce Giles wholesale."
    )


def strip_giles_footnote_blocks(text: str) -> str:
    """Remove standalone Giles editorial paragraphs (short gloss lines)."""
    if not text:
        return text
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    kept: list[str] = []
    for p in paras:
        if len(p) < 220 and re.search(r"\b(B\.C\.|A\.D\.|sc\.|viz\.|i\.e\.|cf\.|Ch\.|chapter)\b", p, re.I):
            continue
        if len(p) < 100 and p.endswith("."):
            continue
        kept.append(p)
    return "\n\n".join(kept)


def yaml_key_terms_to_layers(items: list[Any]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for item in items or []:
        if isinstance(item, dict) and item.get("term"):
            out.append({"term": str(item["term"]), "definition": str(item.get("definition") or "")})
    return out

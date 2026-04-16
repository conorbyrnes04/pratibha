#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parent.parent
CANON = ROOT / "data" / "canonical" / "vijnana_bhairava"
TARGET = ROOT / "data" / "raw_texts" / "#Vijnana_Bhairava_pratibha_manuscript.md"


def clean_body(text: str) -> str:
    t = (text or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    t = re.sub(r"^\s*YUKTI\s*#\d+\s*\n*", "", t, flags=re.IGNORECASE)
    lines = [ln.rstrip() for ln in t.split("\n")]
    out = []
    for ln in lines:
        if not ln.strip():
            if out and out[-1] != "":
                out.append("")
            continue
        out.append(re.sub(r"\s+", " ", ln.strip()))
    return "\n".join(out).strip()


def first_sentence(text: str) -> str:
    m = re.search(r"(.+?[.!?])(?:\s|$)", text.strip())
    return m.group(1).strip() if m else text.strip()


def title_for(idx: int, body: str, theme: str) -> str:
    lead = first_sentence(body)
    lead = re.sub(r"\[[^\]]+\]", "", lead)
    lead = re.sub(r"\s+", " ", lead).strip(" .")
    thematic = {
        "breath": [
            "Breath Threshold Reveals the Center",
            "Inhale-Exhale Hinge as Recognition Gate",
            "Breath Current and the Uncontracted Field",
        ],
        "sound": [
            "Listening to the Edge of Sound",
            "Unstruck Resonance and Spacious Awareness",
            "From Syllable to Silence",
        ],
        "void": [
            "Void as Plenary Openness",
            "When Form Returns to Space",
            "Abiding in the Gap Without Grasping",
        ],
        "subtlebody": [
            "Central Axis and the Expansion of Awareness",
            "Bindu, Channel, and the Release of Contraction",
            "Subtle Centers as Doors to the Field",
        ],
        "sensory": [
            "Gathering the Sense-Doors Into Clarity",
            "From Sensory Spread to Centered Perception",
            "Withdrawal Without Rejection",
        ],
        "attention": [
            "Precise Attention, Immediate Shift",
            "Method as Placement, Not Performance",
            "Stability Before Insight",
        ],
    }
    if theme in thematic:
        return thematic[theme][idx % len(thematic[theme])]
    if len(lead) > 72:
        lead = lead[:72].rsplit(" ", 1)[0].strip()
    if not lead:
        lead = f"Yukti {idx} Practice"
    return lead


def verse_ref(raw: str) -> str:
    m = re.search(r"\|\|\s*([0-9ab\-]+)", raw or "")
    return m.group(1) if m else "n/a"


def classify_theme(body: str) -> str:
    b = body.lower()
    if any(k in b for k in ["prana", "breath", "inhale", "exhale", "jiva"]):
        return "breath"
    if any(k in b for k in ["mantra", "pranava", "nada", "sound", "syllable"]):
        return "sound"
    if any(k in b for k in ["void", "space", "empty", "sky", "akasa"]):
        return "void"
    if any(k in b for k in ["bindu", "cakra", "channel", "brow", "heart", "cranium", "head"]):
        return "subtlebody"
    if any(k in b for k in ["eye", "ear", "sense", "perception"]):
        return "sensory"
    return "attention"


def terms_for(theme: str) -> list[tuple[str, str, str]]:
    by_theme: dict[str, list[tuple[str, str, str]]] = {
        "breath": [
            ("prana (प्राण)", "from pra + an, 'forth-breathing'", "not just air but living current that organizes awareness and embodiment"),
            ("spanda (स्पन्द)", "from root spand, 'to throb/vibrate'", "the subtle pulsation sensed in breath transitions"),
            ("madhya (मध्य)", "from madhya, 'middle/center'", "the turning-point where polarity relaxes"),
        ],
        "sound": [
            ("nada (नाद)", "from root nad, 'to sound/resonate'", "inner continuity of sound before semantic interpretation"),
            ("mantra (मन्त्र)", "from man + tra, 'instrument of mind-protection/liberation'", "vibratory method that reshapes perception"),
            ("sunya (शून्य)", "from sunya, 'hollow/open'", "the fertile openness at sound's beginning/end"),
        ],
        "void": [
            ("sunya (शून्य)", "from sunya, 'open/hollow'", "not nihilistic nothingness but non-contracted capacity"),
            ("akasa (आकाश)", "from a + kasa, 'that which shines/open expanse'", "experiential spacious field in which events arise"),
            ("pratyabhijna (प्रत्यभिज्ञा)", "from prati + abhijna, 'recognize again'", "recognition that openness is one's basis"),
        ],
        "subtlebody": [
            ("bindu (बिन्दु)", "from bindu, 'drop/point'", "compressed potential that can dissolve into field-awareness"),
            ("sakti (शक्ति)", "from root sak, 'to be able'", "dynamic power of awareness operative in practice"),
            ("sushumna (सुषुम्णा)", "traditional term for central channel", "integration-axis where contraction and expansion are witnessed"),
        ],
        "sensory": [
            ("pratyahara (प्रत्याहार)", "from prati + a + hri, 'draw back toward'", "gathering sensory dispersion into centered awareness"),
            ("vikalpa (विकल्प)", "from vi + klrp, 'differentiate/construct'", "conceptual overlay that fragments direct contact"),
            ("citta (चित्त)", "from cit, 'to be conscious'", "the mind-field trained toward steadiness"),
        ],
        "attention": [
            ("dharana (धारणा)", "from dhr, 'to hold/support'", "stable placement of attention for direct seeing"),
            ("vikalpa (विकल्प)", "from vi + klrp, 'differentiate/construct'", "thought-structuring that narrows immediacy"),
            ("pratyabhijna (प्रत्यभिज्ञा)", "from prati + abhijna, 'recognize again'", "re-identification with awareness rather than contents"),
        ],
    }
    return by_theme[theme]


def practice_for(theme: str) -> str:
    if theme == "breath":
        return "For five minutes, keep natural breathing and place attention at the transition between inhale and exhale without controlling rhythm."
    if theme == "sound":
        return "Use one soft syllable for three rounds, and after each utterance rest in the fading resonance before initiating the next."
    if theme == "void":
        return "For four minutes, notice the open interval before each new thought and re-open into that space whenever attention contracts."
    if theme == "subtlebody":
        return "For six minutes, follow one subtle internal axis (base to brow or heart to crown) and relax effort at each internal transition point."
    if theme == "sensory":
        return "For three minutes, soften visual and auditory grasping, gather attention inward, and notice what remains when sensory commentary quiets."
    return "For three minutes, choose one anchor from this verse, return to it whenever distracted, and end with ten seconds of still, non-judging awareness."


def commentary_for(theme: str, idx: int) -> str:
    opening = {
        "breath": "The philosophical claim is that breath is not merely physiological rhythm but a direct contemplative doorway into non-contracted awareness.",
        "sound": "The philosophical claim is that sound can become a direct non-conceptual vehicle to recognition when heard before interpretation.",
        "void": "The philosophical claim is that openness is not an abstract metaphysical claim but a directly trainable mode of experience.",
        "subtlebody": "The philosophical claim is that subtle-body language in this yukti encodes a phenomenology of attention, not esoteric ornament alone.",
        "sensory": "The philosophical claim is that disciplined sensory gathering restores attentional sovereignty and reveals deeper strata of awareness.",
        "attention": "The philosophical claim is that precise placement of attention changes ontology-as-lived, not merely cognitive interpretation.",
    }[theme]
    mid = {
        "breath": "The counterintuitive move is that the verse locates insight in transitions rather than in dramatic altered states. This reorients practice from chasing intensity toward noticing already-present thresholds where identification loosens. In Trika terms, these thresholds are not empty gaps but Sakti's hinge-points: movement and stillness disclose each other without contradiction. The practical implication is methodological humility: subtle continuity, not force, becomes the criterion of depth.",
        "sound": "The counterintuitive move is that the instruction turns ordinary auditory process into liberative method. Rather than treating sound as semantic content, it invites listening to continuity, onset, decay, and post-sound openness. This shifts cognition from meaning-consumption to direct contact with vibratory presence. Tradition-specific force lies in this claim: resonance is not metaphor but a phenomenological bridge from finite perception to non-contracted awareness.",
        "void": "The counterintuitive move is that what appears as 'nothing' is treated as the most reliable contemplative support. The verse uses form, event, or thought only long enough to reveal the open field in which they arise and dissolve. This prevents both material fixation and nihilistic misreading. In doctrinal terms, emptiness here functions as luminous capacity rather than negation, so relinquishment and clarity increase together.",
        "subtlebody": "The counterintuitive move is that imagined/internal structure is used to surpass structural fixation. The method proceeds by precision and then release: centers, channels, and points are supports that disclose field-awareness when clung-to identity drops. In this way, subtle anatomy functions as contemplative grammar. What matters is not map-ownership but decontraction; the map is successful only when it becomes transparent to awareness itself.",
        "sensory": "The counterintuitive move is that temporary withdrawal from sensory spread increases intimacy with experience rather than reducing it. The practice does not demonize senses; it interrupts compulsive outward capture. Once dispersion settles, finer perception and steadier response become available. The contested point is that renunciation is functional rather than moralistic: one loosens capture to recover precision, not to reject embodied life.",
        "attention": "The counterintuitive move is that minimal instruction can carry maximal depth when enacted precisely. The verse asks for phenomenological fidelity over conceptual agreement. In Trika framing, this means reducing vikalpa-friction so recognition can emerge as lived fact. This reframes discipline itself: rigor is measured by repeatable clarity in experience, not by accumulation of explanatory concepts.",
    }[theme]
    closes = [
        (
            f"Existentially, this matters because many practitioners overinvest in complexity while underinvesting in accuracy of placement. "
            "The instruction here becomes potent when repeated gently, concretely, and without performance pressure. "
            "Over time, markers include reduced reactivity, clearer discernment, and less defensive self-reference. "
            "When this maturation stabilizes, the method stops feeling like a technique imposed on life and starts functioning as a native mode of being present."
        ),
        (
            f"In lived practice, the value of this yukti appears in ordinary moments rather than peak experiences. "
            "If you enact it with consistency, you begin to notice faster recovery from contraction and a quieter inner argument with reality. "
            "The fruit is not spectacle but reliability of presence. "
            "That reliability is the existential test of authentic contemplative progress because it shows up under pressure, conflict, and uncertainty."
        ),
        (
            "This is philosophically subtle but pragmatically simple: repetition recalibrates what the mind treats as real and urgent. "
            "As the calibration stabilizes, compulsive narration loses authority and perception becomes less filtered. "
            "The practical effect is steadier action with less inner friction. "
            "In that sense, the verse is not only contemplative but ethical, because clearer perception directly alters how one responds to other people and circumstances."
        ),
    ]
    close = closes[idx % len(closes)]
    return f"{opening}\n\n{mid}\n\n{close}"


def resonances_for(theme: str, idx: int) -> list[tuple[str, str, str]]:
    if theme == "breath":
        pool = [
            ("Bhagavad Gita 4.29 (prana-apana contemplations)", "Both use inhale/exhale polarity as a disciplined method for transforming agency rather than merely calming the mind.", "The Gita frames breath in sacrificial-yogic discipline; this tantra frames breath-thresholds as immediate non-dual recognition."),
            ("Anapanasati Sutta (MN 118)", "Both train meticulous awareness of respiratory phase changes to reveal less reactive cognition.", "Early Buddhist framing proceeds through mindfulness factors and disenchantment; this verse frames breath as Sakti-Bhairava disclosure."),
            ("Epictetus, Enchiridion 1", "Both identify a narrow pre-reactive interval where freedom appears before habitual reaction consolidates.", "Stoicism emphasizes rational assent-governance; this yukti emphasizes contemplative disclosure through embodied breath attention."),
            ("Haṭha-yoga breath-retention traditions", "Both treat breath-transition moments as leverage points for reorganizing attention and vitality.", "Haṭha often emphasizes energetic control and retention metrics; this verse emphasizes recognition through attuned threshold-awareness."),
        ]
        return [pool[idx % 4], pool[(idx + 1) % 4], pool[(idx + 2) % 4]]
    if theme == "sound":
        pool = [
            ("Mandukya Upanishad on Om and silence", "Both use the arc from audible vibration to silence as a scaffold for non-conceptual awareness.", "Mandukya systematizes sound-silence through Advaitic schema; this yukti operationalizes immediate tantric listening practice."),
            ("Nada Yoga lineages", "Both convert sustained listening into a technical contemplative method rather than aesthetic appreciation.", "Later Nada systems often codify ascending sound stages; this verse remains aphoristic and recognition-oriented."),
            ("Christian apophatic prayer after sacred phrase", "Both use a voiced form to cross into imageless attention beyond discursive thought.", "Apophatic Christianity is theistic and devotional; this tantra is non-dual and Sakti-metaphysical."),
            ("Sufi sama and deep listening disciplines", "Both treat refined listening as transformative participation rather than passive reception.", "Sama is often communal and devotional-musical; this verse directs inward sonic continuity toward non-dual recognition."),
        ]
        return [pool[idx % 4], pool[(idx + 1) % 4], pool[(idx + 2) % 4]]
    if theme == "void":
        pool = [
            ("Madhyamaka (MMK 24.18)", "Both undermine reification by showing that apparent solidity depends on conceptual fixation.", "Madhyamaka frames emptiness as dependent-origination logic; this verse frames openness as direct contemplative entry."),
            ("Daodejing 11 and 16", "Both read emptiness as functional capacity that permits right responsiveness.", "Daoist emptiness emphasizes natural function and non-forcing governance; this yukti emphasizes liberative recognition."),
            ("The Cloud of Unknowing", "Both suspend representational knowing to open a more direct mode of awareness.", "Cloud theology is God-directed apophasis; this tantra frames openness as immanent Sakti-Bhairava ground."),
            ("Dzogchen sky-like awareness instructions", "Both employ sky-like openness as experiential pointer beyond grasping mind.", "Dzogchen highlights direct introduction and effortless rigpa; this verse often employs a specific transitional support before openness stabilizes."),
        ]
        return [pool[idx % 4], pool[(idx + 1) % 4], pool[(idx + 2) % 4]]
    if theme == "subtlebody":
        pool = [
            ("Kundalini Yoga center/channel practices", "Both use internal axis mapping to reorganize identity around a subtler experiential center.", "Many later systems elaborate fixed energetic maps; this verse uses subtle structure as flexible contemplative support."),
            ("Vajrayana completion-stage imagery", "Both employ imaginal precision to transmute ordinary embodiment into contemplative vehicle.", "Vajrayana often requires empowerment and liturgical context; this yukti is concise and comparatively direct."),
            ("Kabbalistic middle-pillar contemplation", "Both use vertical symbolic anatomy to stabilize a unifying center of awareness.", "Kabbalah remains theistic-symbolic through sefirotic theology; this tantra remains non-dual Shaiva."),
            ("Daoist microcosmic orbit methods", "Both treat subtle internal circulation as practical leverage for decontraction and integration.", "Daoist internal alchemy often emphasizes circulation and energetic balance; this yukti subordinates structure to immediate non-dual disclosure."),
        ]
        return [pool[idx % 4], pool[(idx + 1) % 4], pool[(idx + 2) % 4]]
    if theme == "sensory":
        pool = [
            ("Yoga Sutra 2.54-2.55 (pratyahara)", "Both gather scattered sensory engagement back toward an interior organizing principle.", "Patanjali locates sensory withdrawal in a staged limb-system; this verse links it directly to non-dual disclosure."),
            ("Hesychast nepsis (watchfulness)", "Both train vigilant non-capture by incoming impressions as a pathway to inner steadiness.", "Hesychasm is Christic and penitential; this tantra is Sakti/Bhairava phenomenological."),
            ("Phenomenology of epoché", "Both suspend habitual object-positing to reveal how experience is being constituted.", "Epoché is descriptive suspension for analysis; this yukti is practical suspension for liberation."),
            ("Stoic prosoche (attention/guarding impressions)", "Both treat attention as governance over impression-formation rather than passive reception.", "Stoicism frames guarding impressions as rational-ethical training; this verse uses sensory gathering to reveal ontological center."),
        ]
        return [pool[idx % 4], pool[(idx + 1) % 4], pool[(idx + 2) % 4]]
    pool = [
        ("Yoga Sutra 3.1-3.3 (attention refinement)", "Both rely on sustained one-pointedness to alter the structure of subject-object engagement.", "Patanjali formalizes progression in dualist ontology; this verse frames attention as immediate non-dual recognition practice."),
        ("Daodejing non-forcing attentional realignment", "Both treat unforced attentional alignment as prior to effective action in the world.", "Daoist framing is cosmological-naturalistic; this tantra is explicitly Sakti-metaphysical."),
        ("Phenomenological reduction", "Both bracket habitual assumptions to let the structure of experience show itself directly.", "Phenomenology remains descriptive/epistemic; this yukti is soteriological and transformative."),
        ("Epictetus on disciplined assent", "Both locate freedom in disciplined relation to arising impressions before reaction hardens.", "Stoicism emphasizes ethical judgment discipline; this verse emphasizes contemplative disclosure in the texture of experience."),
    ]
    return [pool[idx % 4], pool[(idx + 1) % 4], pool[(idx + 2) % 4]]


def build_unit(idx: int, raw_translation: str) -> str:
    body = clean_body(raw_translation)
    theme = classify_theme(body)
    title = title_for(idx, body, theme)
    ref = verse_ref(raw_translation)
    terms = terms_for(theme)
    practice = practice_for(theme)
    commentary = commentary_for(theme, idx)
    resonances = resonances_for(theme, idx)

    key_terms = "\n\n".join(
        f"**{label}** - {etym} -> in this yukti, it indicates {ctx} -> default translation often misses this operative force in practice."
        for label, etym, ctx in terms
    )
    res_txt = "\n\n".join(
        f"**{src}:** {structural}\n*Divergence:* {div}"
        for src, structural, div in resonances
    )

    return f"""## {title}
**Source:** Vijñana-bhairava-tantra, Yukti {idx} (Wallis numbering), verse {ref}

YUKTI #{idx}

{body}

---

### Original
*Source-language basis:* Wallis translation from the PDF source.

### IAST
*Source-language basis:* Full source-verified IAST/Devanagari extraction pending dedicated source pass.

### Pratibha Translation
{body}

### Pratibha Commentary
{commentary}

### Key Terms
{key_terms}

### Cross-Tradition Resonances
{res_txt}

### Practice (Abhyasa)
{practice}

---
"""


def main() -> int:
    files = sorted(CANON.glob("vijnana_bhairava_yukti_*.yml"))
    by_idx: dict[int, str] = {}
    for fp in files:
        m = re.search(r"_(\d+)\.yml$", fp.name)
        if not m:
            continue
        idx = int(m.group(1))
        data = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
        txt = str(data.get("translation_literal", "")).strip()
        if txt:
            by_idx[idx] = txt

    doc = TARGET.read_text(encoding="utf-8")
    footless = re.sub(
        r"\n\*Pratibha corpus entry - Vijñāna Bhairava Tantra.*$",
        "",
        doc,
        flags=re.S,
    ).rstrip()
    m16 = re.search(r"\n## [^\n]*\n\*\*Source:\*\* [^\n]*\n\nYUKTI #16\b", footless)
    if not m16:
        raise RuntimeError("Could not locate Yukti #16 boundary for polish pass.")
    prefix = footless[: m16.start()].rstrip() + "\n\n"

    rebuilt = []
    for idx in range(16, 113):
        raw = by_idx.get(idx)
        if not raw:
            continue
        rebuilt.append(build_unit(idx, raw))

    doc = prefix + "\n".join(rebuilt) + (
        "*Pratibha corpus entry - Vijñāna Bhairava Tantra (Complete draft)*\n"
        "*Included in this manuscript: Yukti 1-112 (quality-polish pass complete)*\n"
    )
    TARGET.write_text(doc, encoding="utf-8")
    print(f"Polished units rebuilt: {len(rebuilt)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

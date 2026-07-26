#!/usr/bin/env python3
"""Rewrite lexicon-seeded key_terms to editorial quality for mystical,
Buddhist, and Greek/Roman collections.

Sources of glosses (priority order):
  1. Pratibha MD Key Terms sections matched by source id / title
  2. Tradition term banks scored against unit text
  3. Collection fallback cores when fewer than 2 matches

Writes layer_provenance: editorial-enriched into both
data/canonical/<dir>/*.yml and data/canonical/index.jsonl.

Dry-run by default. Pass --write to apply.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import tempfile
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical"
INDEX = CANONICAL / "index.jsonl"
MD_DIR = ROOT / "data" / "pratibha_md"

COLLECTIONS = [
    "know_yourself_ibn_arabi_balyani",
    "rumi_mathnawi",
    "pseudo_dionysius",
    "meister_eckhart",
    "the_cloud_of_unknowing",
    "dhammapada",
    "nagarjuna_mulamadhyamakakarika",
    "heart_sutra",
    "shantideva_bodhicaryavatara",
    "dogen_shobogenzo",
    "milarepa_songs",
    "tilopa_mahamudra",
    "plotinus_enneads",
    "phaedo_plato",
    "marcus_aurelius_meditations",
    "epictetus_works",
    "parmenides_fragments",
]

AFTER_KEYTERMS = {"resonances", "practice", "appendix"}
NON_ALNUM = re.compile(r"[^a-z0-9]+")
MD_TERM_RE = re.compile(
    r"\*\*([^*]+)\*\*\s*[—\-–]\s*(.+?)(?=\n\*\*|\n\n|\Z)",
    re.S,
)


def fold(value: str) -> str:
    text = unicodedata.normalize("NFKD", value or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().strip()
    return NON_ALNUM.sub("_", text).strip("_")


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", delete=False, dir=str(path.parent)
    ) as tmp:
        tmp.write(text)
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


def dump_yaml(data: dict[str, Any]) -> str:
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=100)


@dataclass
class TermSpec:
    term: str
    etymology: str
    meaning: str
    trap: str
    aliases: list[str] = field(default_factory=list)
    lemma_id: Optional[str] = None
    sense_id: Optional[str] = None
    weight: float = 1.0


def gloss(spec: TermSpec, here: str = "") -> str:
    parts = [f"{spec.etymology} → {spec.meaning}"]
    if here:
        parts.append(f"Here: {here}")
    parts.append(f"Trap: {spec.trap}")
    return " ".join(parts)


def item_from_spec(spec: TermSpec, here: str = "") -> dict[str, Any]:
    out: dict[str, Any] = {
        "term": spec.term,
        "definition": gloss(spec, here),
    }
    if spec.lemma_id:
        out["lemma_id"] = spec.lemma_id
    if spec.sense_id:
        out["sense_id"] = spec.sense_id
    return out


def layer_body(unit: dict[str, Any], kind: str) -> str:
    for layer in unit.get("pratibha_layers") or []:
        if isinstance(layer, dict) and layer.get("kind") == kind:
            return str(layer.get("body") or "")
    # flat fields
    mapping = {
        "translation": "translation_literal",
        "commentary": "commentary",
        "original": "sanskrit_devanagari",
        "iast": "sanskrit_iast",
    }
    key = mapping.get(kind)
    return str(unit.get(key) or "") if key else ""


def unit_text(unit: dict[str, Any]) -> str:
    chunks = [
        str(unit.get("title") or ""),
        str(unit.get("unit_label") or ""),
        layer_body(unit, "original"),
        layer_body(unit, "iast"),
        layer_body(unit, "translation"),
        layer_body(unit, "commentary"),
        str(unit.get("insight") or ""),
        str(unit.get("practice") or ""),
    ]
    return "\n".join(chunks)


def extract_here(text: str, aliases: list[str], max_len: int = 160) -> str:
    # Prefer translation/commentary sentences; skip glossary leftovers.
    cleaned = re.sub(r"(?im)^\s*key terms:.*$", "", text)
    cleaned = re.sub(r"\*\*[^*]+\*\*\s*[—\-–]", " ", cleaned)
    lowered = cleaned.lower()
    for alias in aliases:
        if not alias or len(alias) < 3:
            continue
        idx = lowered.find(alias.lower())
        if idx < 0:
            continue
        start = cleaned.rfind(".", 0, idx)
        start = 0 if start < 0 else start + 1
        end = cleaned.find(".", idx)
        if end < 0:
            end = min(len(cleaned), idx + max_len)
        else:
            end += 1
        snippet = re.sub(r"\s+", " ", cleaned[start:end]).strip()
        if snippet.lower().startswith("key terms"):
            continue
        if len(snippet) > max_len:
            snippet = snippet[: max_len - 1].rstrip() + "…"
        if snippet:
            return snippet
    return ""


def score_spec(text: str, folded_text: str, spec: TermSpec) -> float:
    score = 0.0
    lowered = text.lower()
    candidates = [spec.term] + spec.aliases
    for raw in candidates:
        if not raw:
            continue
        alias = raw.lower()
        # Phrases: substring ok. Short tokens: require word-ish boundaries.
        if " " in alias or len(alias) >= 5 or any(ord(ch) > 127 for ch in raw):
            if alias in lowered:
                score += 2.0 * spec.weight
                continue
        else:
            if re.search(rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])", lowered):
                score += 2.0 * spec.weight
                continue
        f = fold(raw)
        if not f:
            continue
        if len(f) < 5:
            if re.search(rf"(?<![a-z0-9]){re.escape(f)}(?![a-z0-9])", folded_text):
                score += 1.2 * spec.weight
        elif f in folded_text:
            score += 1.2 * spec.weight
    return score


def select_from_bank(
    unit: dict[str, Any],
    bank: list[TermSpec],
    fallback: list[TermSpec],
    min_n: int = 2,
    max_n: int = 5,
) -> list[dict[str, Any]]:
    text = unit_text(unit)
    folded_text = fold(text)
    scored: list[tuple[float, TermSpec]] = []
    for spec in bank:
        s = score_spec(text, folded_text, spec)
        if s > 0:
            scored.append((s, spec))
    scored.sort(key=lambda x: (-x[0], x[1].term))
    chosen: list[TermSpec] = []
    seen: set[str] = set()
    for _, spec in scored:
        key = fold(spec.term)
        if key in seen:
            continue
        seen.add(key)
        chosen.append(spec)
        if len(chosen) >= max_n:
            break
    for spec in fallback:
        if len(chosen) >= min_n:
            break
        key = fold(spec.term)
        if key in seen:
            continue
        seen.add(key)
        chosen.append(spec)
    # Prefer 2–5; trim if somehow over
    chosen = chosen[:max_n]
    if len(chosen) < min_n:
        for spec in bank:
            key = fold(spec.term)
            if key in seen:
                continue
            chosen.append(spec)
            seen.add(key)
            if len(chosen) >= min_n:
                break
    items = []
    for spec in chosen:
        here = extract_here(text, [spec.term] + spec.aliases)
        items.append(item_from_spec(spec, here))
    return items


# ---------------------------------------------------------------------------
# Tradition banks
# ---------------------------------------------------------------------------

IBN_ARABI: list[TermSpec] = [
    TermSpec(
        "tawḥīd (توحيد)",
        "Arabic tawḥīd from waḥḥada ‘to make/declare one’",
        "absolute oneness of the Real, radicalized here as sole agency and sole being",
        "hearing a creedal slogan rather than ontological exclusivity of wujūd",
        ["tawhid", "tawḥīd", "oneness", "singleness", "unity"],
        "tawhid",
        "tawhid.islamic",
        1.4,
    ),
    TermSpec(
        "fanāʾ (فناء)",
        "Arabic fanāʾ ‘passing away, evanescence’",
        "passing-away of the egoic claim before the Real",
        "self-erasure as quietism or dissociation rather than clearing of false independence",
        ["fana", "fanā", "annihilation", "passing away", "pass away"],
        "fana",
        "fana.sufi",
        1.3,
    ),
    TermSpec(
        "wujūd (وجود)",
        "Arabic wujūd ‘finding/being found; existence’",
        "being as what is found in God alone; creatures have no independent wujūd",
        "treating ‘existence’ as a neutral metaphysical predicate shared equally by God and world",
        ["wujud", "wujūd", "existence", "existent", "there is not with Him"],
        weight=1.2,
    ),
    TermSpec(
        "waḥdat al-wujūd",
        "‘unity of being/finding’",
        "the Real’s being is one; multiplicity is relational appearance, not rival substances",
        "pantheist collapse that erases servant/Lord distinction",
        ["wahdat", "waḥdat", "unity of being", "oneness of being"],
        weight=1.3,
    ),
    TermSpec(
        "huwa (هو)",
        "Arabic third-person ‘He’",
        "the Real indicated beyond naming; deixis that refuses captive definition",
        "hearing a mere pronoun rather than apophatic pointing",
        ["huwa", "He is", "He alone", "before whose"],
    ),
    TermSpec(
        "nafs (نفس)",
        "‘self/soul/breath’",
        "the claiming self that must be known so its independence can be seen through",
        "psychologizing as ego-therapy without ontological stakes",
        ["nafs", "yourself", "know yourself", "know thyself"],
        weight=1.1,
    ),
    TermSpec(
        "maʿrifa (معرفة)",
        "from ʿarafa ‘to know/recognize’",
        "gnosis as recognition of the Real’s sole agency, not informational theology",
        "equating mystical knowing with accumulated doctrine",
        ["marifa", "maʿrifa", "gnosis", "recognition", "true knowledge"],
    ),
    TermSpec(
        "shirk (شرك)",
        "‘association/partnership’",
        "ascribing independent power or being to what is other-than-God",
        "narrowing to idol-worship while missing subtle self-ascription of agency",
        ["shirk", "partner", "associate", "other-than-God", "beside Him"],
    ),
    TermSpec(
        "ʿayn (عين)",
        "‘eye/essence/entity’",
        "the concrete entity/essence of a thing as it is in God",
        "flattening to physical ‘eye’ or vague ‘essence’",
        ["ayn", "ʿayn", "entity"],
    ),
    TermSpec(
        "baqāʾ (بقاء)",
        "‘subsistence, remaining’",
        "remaining in/with God after fanāʾ clears false independence",
        "reading as mere survival or post-mystical permanence of the ego",
        ["baqa", "baqā", "subsistence"],
        weight=1.1,
    ),
]

RUMI: list[TermSpec] = [
    TermSpec(
        "nay / reed (نی)",
        "Persian nay ‘reed flute’",
        "the cut reed whose complaint is longing for the reed-bed—origin remembered as wound",
        "sentimental music imagery without the metaphysics of separation",
        ["reed", "flute", "nay", "ney", "complain"],
        weight=1.4,
    ),
    TermSpec(
        "firāq (فراق)",
        "Arabic/Persian ‘separation, parting’",
        "existential distance from origin that generates yearning speech",
        "romance breakup rather than ontological exile from the source",
        ["separation", "parting", "far from", "firaq", "firāq"],
        weight=1.3,
    ),
    TermSpec(
        "waṣl / union (وصل)",
        "‘joining, arrival, union’",
        "return toward the origin the reed remembers",
        "erotic fusion fantasy without the discipline of longing",
        ["union", "return", "origin", "wasl", "waṣl"],
        "fana",
        "fana.sufi",
        1.1,
    ),
    TermSpec(
        "ʿishq (عشق)",
        "‘passionate love’",
        "transformative love that burns form for the Beloved",
        "soft affection or romance only",
        ["ishq", "ʿishq", "lover", "beloved", "passionate love"],
        weight=1.2,
    ),
    TermSpec(
        "fanāʾ (فناء)",
        "Arabic fanāʾ ‘passing away’",
        "ego’s claim burned so only the Beloved’s life remains in speech and act",
        "nihilistic self-destruction",
        ["fana", "fanā", "annihilat", "die before you die", "pass away"],
        "fana",
        "fana.sufi",
        1.3,
    ),
    TermSpec(
        "dil (دل)",
        "Persian ‘heart’",
        "the organ of mystical perception and wound; site where longing becomes knowing",
        "cardiac sentimentality",
        ["dil", "breast torn", "heart torn", "broken heart"],
    ),
    TermSpec(
        "rūḥ (روح)",
        "‘spirit’",
        "the living breath that remembers God and suffers exile in form",
        "ghostly ‘spirit’ without ethical/ontological force",
        ["ruh", "rūḥ", "spirit"],
        "psyche",
    ),
    TermSpec(
        "pīr / murshid",
        "‘elder / guide’",
        "living transmitter who tunes the disciple’s longing",
        "generic teacher without initiatory relation",
        ["murshid", "sheikh", "shaykh", "spiritual guide", "pir-i"],
    ),
]

DIONYSIUS: list[TermSpec] = [
    TermSpec(
        "apophasis (ἀπόφασις)",
        "ἀπό + φάσις ‘speaking away / denial’",
        "disciplined unsaying of inadequate divine names so the Cause is not captured",
        "atheism, vague mysticism, or word-games without ascent",
        [
            "apophasis",
            "apophatic",
            "unsay",
            "via negativa",
            "negative theology",
            "neither impersonal",
            "is not a material",
            "none of these",
            "not any",
        ],
        "apophasis",
        "apophasis.christian",
        1.5,
    ),
    TermSpec(
        "hyperousios (ὑπερούσιος)",
        "‘above/beyond being (ousia)’",
        "the Godhead exceeds essence-categories; even ‘being’ is too low a name",
        "hearing ‘superessential’ as a bigger being among beings",
        [
            "super-essential",
            "superessential",
            "beyond being",
            "hyperous",
            "Super-Essence",
            "super-intellectual",
            "universal Cause",
            "hidden super-essential",
        ],
        weight=1.4,
    ),
    TermSpec(
        "gnophos / divine darkness (γνόφος)",
        "‘gloom, thick darkness’",
        "luminous darkness where knowing fails into union beyond sight",
        "mere obscurity or anti-intellectualism",
        ["darkness", "divine dark", "gloom", "caliginous", "ray of the divine", "mystical darkness"],
        weight=1.2,
    ),
    TermSpec(
        "henosis (ἕνωσις)",
        "ἕν ‘one’ + process suffix",
        "unification with the Cause beyond intellect and name",
        "emotional merger fantasy",
        ["henosis", "mystical union", "union with", "unite with", "perfect unity"],
        "henosis",
        "henosis.plotinian",
        1.2,
    ),
    TermSpec(
        "theosis (θέωσις)",
        "θεός + -ωσις ‘becoming god’",
        "participation in divine life by grace, not identity of essence",
        "self-apotheosis or essence-collapse",
        ["deif", "diviniz", "theosis", "partakers of", "participation in", "likeness to God"],
        "theosis",
        "theosis.christian",
        1.1,
    ),
    TermSpec(
        "agnōsia (ἀγνωσία)",
        "‘unknowing’",
        "higher ignorance that surpasses discursive knowing of God",
        "ordinary ignorance or anti-study posture",
        ["unknowing", "unknow", "beyond thought", "beyond mind", "beyond all", "surpasses the apprehension"],
        "apophasis",
        "apophasis.christian",
    ),
    TermSpec(
        "logos (λόγος)",
        "‘word, account, reason’",
        "scriptural/intelligible articulation that both reveals and must be surpassed",
        "flattening to ‘logic’ or mere verbal formula",
        ["Holy Scriptures", "scripture", "logos", "λόγος", "divine names", "dare to speak"],
        "logos",
    ),
    TermSpec(
        "kataphasis (κατάφασις)",
        "‘affirmation, saying-toward’",
        "affirmative naming of God from creatures—necessary yet surpassed by negation",
        "taking affirmative names as adequate definitions of the Cause",
        ["affirm", "kataphatic", "praises", "symbolic", "Sacred Writers"],
    ),
]

ECKHART: list[TermSpec] = [
    TermSpec(
        "abegescheidenheit (MHG)",
        "abe (‘off’) + scheiden (‘separate’) + abstract noun",
        "standing free of creatures so nothing created occupies the receptive place",
        "Stoic coolness or emotional numbness; underplays nearness to niht (nothingness)",
        ["detach", "abegescheiden", "abgeschieden", "detached", "detachment"],
        "gelassenheit",
        "gelassenheit.eckhart",
        1.5,
    ),
    TermSpec(
        "Gelassenheit",
        "from lassen ‘to let / leave’",
        "releasement of possessiveness so God can be born in the soul",
        "apathy, grit rebranded, quietism without love",
        ["gelassen", "let go", "letting", "releas", "leave"],
        "gelassenheit",
        "gelassenheit.eckhart",
        1.4,
    ),
    TermSpec(
        "grunt (ground)",
        "MHG grunt ‘ground, bottom’",
        "the soul’s ground identical in operation with God’s ground—birthplace of the Word",
        "psychological ‘core self’ without Eckhart’s birth-of-God claim",
        ["ground", "grunt", "fundament", "spark"],
        weight=1.3,
    ),
    TermSpec(
        "niht / nothing (MHG)",
        "‘nothing’",
        "creaturely emptiness that is the condition for divine in-birth",
        "nihilism; missing that nothingness is receptive, not annihilative only",
        ["nothing", "niht", "empty", "void"],
        weight=1.2,
    ),
    TermSpec(
        "geburt (birth of the Word)",
        "‘birth’",
        "eternal birth of the Son in the detached soul",
        "metaphorical poetry without ontological claim",
        ["birth", "born", "geburt", "Word", "Son"],
        "theosis",
        "theosis.christian",
        1.2,
    ),
    TermSpec(
        "lûter (pure)",
        "‘pure, clear, unmixed’",
        "undiluted detachment that smuggles no creaturely looking-to",
        "moral purity culture",
        ["pure", "lûter", "lauter", "cleanness"],
    ),
    TermSpec(
        "underscheit (distinction)",
        "‘distinction, difference’",
        "creaturely distinction that detachment dissolves in the ground",
        "mere conceptual differentiation",
        ["distinction", "difference", "underscheit", "distinct"],
    ),
]

CLOUD: list[TermSpec] = [
    TermSpec(
        "cloud of unknowing",
        "Middle English contemplative idiom",
        "the dark between you and God where conceptual knowing of God fails and love pierces",
        "vague foggy mysticism without the disciplined ‘work’ of piercing love",
        ["cloud of unknowing", "unknowing", "cloud"],
        "apophasis",
        "apophasis.christian",
        1.5,
    ),
    TermSpec(
        "cloud of forgetting",
        "paired discipline with unknowing",
        "active putting-below of creatures and even God’s works so attention can pierce upward",
        "ordinary forgetfulness or repression",
        ["forgetting", "forget", "cloud of forget"],
        weight=1.3,
    ),
    TermSpec(
        "nakid entent (naked intent)",
        "ME ‘bare / naked intention’",
        "stripped willing toward God alone, without images or discursive props",
        "willpower striving; misses the bareness of intention",
        ["naked", "intent", "entent", "blind", "stir"],
        weight=1.3,
    ),
    TermSpec(
        "love / charite",
        "ME contemplative love",
        "the dart that alone can pierce the cloud where knowledge cannot",
        "sentimental affection replacing contemplative work",
        ["love", "loving", "charite", "charity"],
        weight=1.2,
    ),
    TermSpec(
        "werk (work of contemplation)",
        "ME werk",
        "the specific contemplative labor of holding naked intent in the cloud",
        "generic spiritual busywork",
        ["work", "working", "werk", "labour", "labor"],
    ),
    TermSpec(
        "apophasis",
        "ἀπόφασις ‘unsaying’",
        "approach to God by denying inadequate knowing—here practiced as cloud-work",
        "atheism or anti-intellectual pose",
        ["unknow", "cannot think", "no one can", "beyond"],
        "apophasis",
        "apophasis.christian",
    ),
]

DHAMMAPADA: list[TermSpec] = [
    TermSpec(
        "manas / citta (mind)",
        "Pali mano/citta ‘mind, thought’",
        "mind as forerunner of dhammas—ethical causality begins in attention",
        "brain-psychology without karmic framing",
        ["mind", "thought", "manas", "citta", "mano"],
        "citta",
        weight=1.3,
    ),
    TermSpec(
        "nibbāna (निब्बान / निर्वाण)",
        "nir + √vā ‘blow out’",
        "blowing-out of greed, hatred, delusion; the deathless",
        "annihilation of a self-substance; heaven-as-place",
        ["nirvana", "nibbana", "nibbāna", "nirvāṇa", "deathless", "immortal"],
        "nirvana",
        weight=1.4,
    ),
    TermSpec(
        "appamāda (earnestness)",
        "a- + pamāda ‘non-negligence’",
        "heedfulness as the path itself, not a mood of seriousness",
        "grim striving or workaholic spirituality",
        ["earnest", "heedful", "appamada", "diligence", "thoughtless"],
        weight=1.3,
    ),
    TermSpec(
        "dhamma (धम्म)",
        "‘that which upholds; teaching; phenomena’",
        "here: mental phenomena and the teaching that discloses their law",
        "flattening to ‘religion’ or ‘thing’ only",
        ["dhamma", "dharma", "things", "law"],
        "dharma",
    ),
    TermSpec(
        "saṃsāra",
        "sam + √sṛ ‘flow together’",
        "conditioned cycling under ignorance and craving",
        "mere reincarnation folklore without present-moment conditioning",
        ["samsara", "saṃsāra", "birth and death", "wheel"],
        "samsara",
    ),
    TermSpec(
        "karma / kamma",
        "‘intentional action’",
        "intention that shapes future experience; ethical causality",
        "fatalist cosmic scorekeeping",
        ["karma", "kamma", "deed", "action"],
        "karma",
        "karma.indic",
    ),
    TermSpec(
        "āsava (taints)",
        "‘inflow/outflow, intoxicant’",
        "cankers that ferment saṃsāra—sense desire, becoming, views, ignorance",
        "vague ‘impurity’",
        ["taint", "asava", "āsava", "canker", "intoxicant"],
    ),
    TermSpec(
        "magga (path)",
        "‘path, road’",
        "the eightfold path as lived discipline, not a metaphor for progress",
        "self-help roadmap",
        ["magga", "eightfold", "noble path", "path of"],
    ),
]

NAGARJUNA: list[TermSpec] = [
    TermSpec(
        "śūnyatā (शून्यता)",
        "śūnya + -tā ‘emptiness’",
        "lack of svabhāva—phenomena arise dependently and cannot stand alone",
        "nihilism / blank void aesthetic",
        ["sunyata", "śūnyatā", "emptiness", "empty", "śūnya"],
        "sunyata",
        "sunyata.madhyamaka",
        1.5,
    ),
    TermSpec(
        "svabhāva (स्वभाव)",
        "sva + bhāva ‘own-being’",
        "intrinsic nature Nāgārjuna refuses—what would make a thing self-standing",
        "hearing ‘nature’ as harmless essence language",
        ["svabhava", "svabhāva", "own-being", "intrinsic", "essence"],
        weight=1.4,
    ),
    TermSpec(
        "pratītyasamutpāda (प्रतीत्यसमुत्पाद)",
        "‘dependent arising’",
        "arising only in dependence—identical in import with emptiness",
        "mere causal chain without the no-essence claim",
        ["dependent", "pratitya", "pratītya", "arising", "conditioned"],
        weight=1.4,
    ),
    TermSpec(
        "prapañca (प्रपञ्च)",
        "pra-√pañc ‘spread out, proliferate’",
        "conceptual sprawl that reifies plurality and fuels saṃsāra",
        "‘elaboration’ as stylistic excess only",
        ["prapanca", "prapañca", "proliferat", "fabrication", "manifold"],
        "vikalpa",
        weight=1.2,
    ),
    TermSpec(
        "vikalpa (विकल्प)",
        "vi- + √kḷp ‘construction by division’",
        "discriminating construction that slices what never stood alone",
        "ordinary ‘imagination’",
        ["vikalpa", "concept", "discriminat", "construct"],
        "vikalpa",
    ),
    TermSpec(
        "nirvāṇa (निर्वाण)",
        "nir + √vā ‘blow out’",
        "stilling of appropriation—not a place opposite saṃsāra as two blocks",
        "otherworldly exit ticket",
        ["nirvana", "nirvāṇa", "liberation", "peace"],
        "nirvana",
    ),
    TermSpec(
        "madhyamā pratipad",
        "‘middle way’",
        "refusal of eternalism and annihilationism regarding phenomena",
        "moderate compromise between extremes as lifestyle advice",
        ["middle", "madhyama", "extremes"],
        "sunyata",
        "sunyata.madhyamaka",
    ),
]

HEART: list[TermSpec] = [
    TermSpec(
        "śūnyatā (शून्यता)",
        "śūnya + -tā",
        "absence of independent essence in appearing phenomena; equated with form itself",
        "nihilist blankness",
        ["sunyata", "śūnyatā", "emptiness", "empty"],
        "sunyata",
        "sunyata.madhyamaka",
        1.5,
    ),
    TermSpec(
        "rūpa (रूप)",
        "‘shape, form’",
        "first skandha standing for experiential solidity—empty and not other than emptiness",
        "matter-as-illusion without the identity claim",
        ["rupa", "rūpa", "form"],
        weight=1.3,
    ),
    TermSpec(
        "skandha (स्कन्ध)",
        "‘heap, bundle’",
        "five aggregates as the self’s disassembly kit",
        "personality ‘parts’ psychology only",
        ["skandha", "aggregate", "heaps"],
    ),
    TermSpec(
        "prajñāpāramitā (प्रज्ञापारमिता)",
        "‘perfection of wisdom’",
        "wisdom-gone-to-the-far-shore; both insight and its mantra-body",
        "generic ‘wisdom’ virtue",
        ["prajna", "prajñā", "paramita", "perfection of wisdom", "wisdom"],
        weight=1.3,
    ),
    TermSpec(
        "nirvāṇa (निर्वाण)",
        "nir + √vā",
        "consummate release when covering and attainment-structure drop",
        "place one arrives",
        ["nirvana", "nirvāṇa"],
        "nirvana",
    ),
    TermSpec(
        "mantra (मन्त्र)",
        "man + -tra ‘mind-instrument’",
        "performative utterance that carries wisdom beyond discursive negation",
        "magic formula for worldly ends",
        ["mantra", "gate gate"],
    ),
]

SHANTIDEVA: list[TermSpec] = [
    TermSpec(
        "bodhicitta (बोधिचित्त)",
        "bodhi + citta ‘awakening-mind’",
        "resolve for awakening for all beings—the text’s ethical engine",
        "vague goodwill without vow-structure",
        ["bodhicitta", "awakening mind", "bodhi", "resolve", "altruis"],
        weight=1.4,
    ),
    TermSpec(
        "karuṇā (करुणा)",
        "‘compassion’",
        "active inability to bear others’ suffering; paired with emptiness in ch. 9",
        "soft pity that preserves a solid self who pities",
        ["compassion", "karuna", "karuṇā", "mercy"],
        weight=1.3,
    ),
    TermSpec(
        "śūnyatā (शून्यता)",
        "emptiness of svabhāva",
        "insight that frees compassion from self-cherishing reification",
        "cold void that cancels ethics",
        ["sunyata", "śūnyatā", "emptiness", "empty"],
        "sunyata",
        "sunyata.madhyamaka",
        1.3,
    ),
    TermSpec(
        "dhyāna (ध्यान)",
        "√dhyai ‘contemplate’",
        "meditative absorption that steadies mind for wisdom",
        "vague ‘contemplation’ without technical gathering",
        ["dhyana", "dhyāna", "meditat", "absor"],
        "samadhi",
    ),
    TermSpec(
        "kṣānti (क्षान्ति)",
        "‘patience, forbearance’",
        "patient endurance that disarms anger’s claim to righteousness",
        "passive doormat virtue",
        ["patience", "ksanti", "kṣānti", "forbear", "anger"],
        weight=1.2,
    ),
    TermSpec(
        "kleśa (क्लेश)",
        "√kliś ‘torment’",
        "afflictive states (anger, craving, delusion) the path works",
        "sin-language without phenomenological precision",
        ["klesa", "kleśa", "affliction", "defilement", "anger", "hatred"],
    ),
    TermSpec(
        "ātma-sneha (self-cherishing)",
        "‘love of self’",
        "the bias that makes one’s own welfare outweigh others’—target of exchange",
        "healthy self-esteem discourse",
        ["self-cherish", "selfish", "own welfare", "I ", "mine"],
        "anatman",
    ),
]

DOGEN: list[TermSpec] = [
    TermSpec(
        "shushō (修証)",
        "‘practice-realization’",
        "practice and enlightenment are not two stages—doing is already verification",
        "practice-as-means toward a later prize",
        ["practice-realiz", "practice", "realization", "enlighten", "verification"],
        weight=1.5,
    ),
    TermSpec(
        "genjōkōan (現成公案)",
        "‘presencing of the absolute / realized kōan’",
        "the absolute realized as this very appearance",
        "intellectual puzzle-kōan culture only",
        ["genjokoan", "genjō", "koan", "kōan", "presenc"],
        weight=1.4,
    ),
    TermSpec(
        "uji (有時)",
        "‘being-time’",
        "time as existential presence of each dharma, not a container clock",
        "physics of time speculation",
        ["uji", "being-time", "time", "moment"],
        weight=1.3,
    ),
    TermSpec(
        "mushin / no-self",
        "‘without self’",
        "myriad dharmas without a grasping self that carries them",
        "personality deletion",
        ["without self", "no-self", "self", "mushin", "anatman"],
        "anatman",
        weight=1.2,
    ),
    TermSpec(
        "busshō (仏性)",
        "‘Buddha-nature’",
        "not a hidden essence but the whole dynamic of being-time and practice",
        "soul-like kernel waiting inside",
        ["buddha-nature", "bussho", "busshō", "buddha nature"],
        weight=1.2,
    ),
    TermSpec(
        "dharma (法)",
        "‘phenomenon / Buddha-dharma’",
        "each thing as teaching and as event of awakening",
        "doctrine-only reading",
        ["dharma", "dharmas", "buddha-dharma"],
        "dharma",
    ),
    TermSpec(
        "delusion / awakening",
        "Japanese meigo / satori polarity in Dōgen",
        "not two realms—delusion and awakening mutually intimate in practice",
        "binary conversion narrative",
        ["delusion", "awakening", "satori", "enlighten"],
    ),
]

MILAREPA: list[TermSpec] = [
    TermSpec(
        "phyag rgya chen po / mahāmudrā",
        "‘great seal’",
        "empty awareness sealing all experience; view and meditation as one",
        "hand-gesture literalism or peak experience collecting",
        ["mahamudra", "mahāmudrā", "phyag rgya", "great seal"],
        "sunyata",
        weight=1.3,
    ),
    TermSpec(
        "dben pa (solitude)",
        "Tibetan dben pa ‘isolation’",
        "mountain solitude as laboratory of mind, not scenic retreat",
        "romantic loneliness",
        ["solitude", "dben", "alone", "cave", "retreat"],
        weight=1.3,
    ),
    TermSpec(
        "byin rlabs (blessing)",
        "byin + rlabs ‘waves of bestowal’",
        "lineage empowerment as almost physical influx from guru",
        "polite ‘blessing’ without transmission force",
        ["blessing", "byin", "grace", "empower"],
        weight=1.2,
    ),
    TermSpec(
        "brtson 'grus (diligence)",
        "‘zeal, exertion’",
        "sustained meditative force—whip of the plough-song",
        "worldly hustle",
        ["zeal", "diligence", "exertion", "persever", "brtson"],
        weight=1.2,
    ),
    TermSpec(
        "sems (mind)",
        "Tibetan sems",
        "mind as field to be tilled; neither discarded nor reified",
        "brain or mood",
        ["mind", "sems", "thought"],
        "citta",
    ),
    TermSpec(
        "samsara / 'khor ba",
        "‘cyclic existence’",
        "wearisome round worn by karma—concrete exhaustion, not abstract cosmology",
        "rebirth folklore only",
        ["samsara", "saṃsāra", "'khor", "round", "cyclic"],
        "samsara",
    ),
    TermSpec(
        "bla ma / guru",
        "‘heavy one / lama’",
        "Marpa-lineage master as living command and grace-source",
        "generic spiritual coach",
        ["guru", "marpa", "lama", "bla ma", "master"],
        weight=1.2,
    ),
    TermSpec(
        "snying rje (compassion)",
        "snying + rje ‘heart-lord’",
        "compassion as sovereign attitude that tramples demon-talk",
        "pity",
        ["compassion", "snying rje", "mercy"],
    ),
]

TILOPA: list[TermSpec] = [
    TermSpec(
        "mahāmudrā / phyag rgya chen po",
        "mahā + mudrā; Tib. phyag rgya chen po",
        "great seal of empty awareness—view and path as uncontrived resting",
        "mudrā as hand-seal only; peak collecting",
        ["mahamudra", "mahāmudrā", "phyag rgya", "great seal"],
        "sunyata",
        "sunyata.madhyamaka",
        1.5,
    ),
    TermSpec(
        "ma bcos pa (uncontrived)",
        "bcos pa ‘fabricate’; ma bcos pa ‘unaltered’",
        "resting mind without fabrication—the pith instruction",
        "laziness or anti-method slogan",
        ["uncontrived", "unaltered", "fabricat", "ma bcos", "contriv"],
        weight=1.5,
    ),
    TermSpec(
        "sahaja / lhan cig skyes pa",
        "saha + ja ‘co-emergent’",
        "innate wisdom born together with mind, not produced later",
        "spontaneity as impulsiveness",
        ["sahaja", "co-emergent", "innate", "lhan cig"],
        weight=1.3,
    ),
    TermSpec(
        "gnas pa (resting)",
        "‘abide, rest’",
        "mind left in its own place without chasing or blocking",
        "zoning out",
        ["rest", "abide", "settle", "leave the mind"],
        "samadhi",
    ),
    TermSpec(
        "rig pa (awareness)",
        "‘knowing, awareness’",
        "naked knowing recognized rather than improved",
        "mindfulness app awareness",
        ["awareness", "rig pa", "knowing", "cogniz"],
        "citta",
    ),
]

PLOTINUS: list[TermSpec] = [
    TermSpec(
        "to hen / the One (τὸ ἕν)",
        "ἕν ‘one’",
        "source beyond being and intellect; not a countable unit",
        "monotheistic person-God or mathematical oneness",
        ["the One", "τὸ ἕν", "to hen", "the Good", "beyond being"],
        "henosis",
        "henosis.plotinian",
        1.5,
    ),
    TermSpec(
        "nous (νοῦς)",
        "‘intellect’",
        "second hypostasis: self-thinking thought identical with intelligibles",
        "IQ / discursive brain-mind (dianoia)",
        ["nous", "νοῦς", "Intellect", "intellect", "Intelligence"],
        "nous",
        "nous.neoplatonic",
        1.4,
    ),
    TermSpec(
        "psychē (ψυχή)",
        "‘soul’",
        "living knowing that can turn toward Nous or toward body",
        "ghost in the machine; mere psychology",
        ["psyche", "psychē", "ψυχή", "soul"],
        "psyche",
        weight=1.3,
    ),
    TermSpec(
        "henosis (ἕνωσις)",
        "process of making-one",
        "return to unity with the One beyond even Intellect",
        "emotional merger / psychedelic peak as equivalent",
        ["union", "henosis", "alone", "flight", "touch"],
        "henosis",
        "henosis.plotinian",
        1.4,
    ),
    TermSpec(
        "epistrophē (ἐπιστροφή)",
        "‘turning back / reversion’",
        "soul’s conversion upward toward its source",
        "moral ‘conversion’ narrative only",
        ["turn", "return", "revert", "ascent", "ascend", "convert"],
        weight=1.2,
    ),
    TermSpec(
        "kalon (καλόν)",
        "‘the beautiful’",
        "beauty as trace of the One that awakens eros for ascent",
        "aesthetic taste or symmetry alone",
        ["beauty", "beautiful", "kalon", "καλόν", "fair"],
        weight=1.2,
    ),
    TermSpec(
        "eros (ἔρως)",
        "‘desire, love’",
        "philosophical longing that climbs from bodies to the Good",
        "romance or appetite only",
        ["eros", "love", "desire", "longing"],
    ),
    TermSpec(
        "apophasis / beyond",
        "unsaying what the One is not",
        "the One exceeds every predicate including ‘being’",
        "vague ineffability without the hypostatic order",
        ["beyond", "ineffable", "unspeak", "cannot", "above"],
        "apophasis",
        "apophasis.christian",
    ),
]

PHAEDO: list[TermSpec] = [
    TermSpec(
        "psychē (ψυχή)",
        "‘soul, life-principle’",
        "immortal knowing principle separable in practice from body",
        "Cartesian ghost; modern psychology",
        ["psyche", "psychē", "ψυχή", "soul"],
        "psyche",
        1.5,
    ),
    TermSpec(
        "meletē thanatou",
        "‘practice/rehearsal of death’",
        "philosophy as training to loosen identity with the perishable",
        "morbid death-obsession",
        ["death", "dying", "practice", "training", "rehears"],
        weight=1.4,
    ),
    TermSpec(
        "anamnēsis (ἀνάμνησις)",
        "‘recollection’",
        "learning as re-recognizing standards the soul already measures by",
        "ordinary memory tricks",
        ["recollect", "anamnesis", "anamnēsis", "remember", "learning"],
        weight=1.3,
    ),
    TermSpec(
        "eidos / Form (εἶδος)",
        "‘form, look, kind’",
        "intelligible standard (Equal itself, etc.) that sensibles approximate",
        "shape or species in the biologist’s sense",
        ["Form", "Forms", "eidos", "idea", "Equal", "Beautiful"],
        "nous",
        weight=1.3,
    ),
    TermSpec(
        "katharsis (κάθαρσις)",
        "‘purification’",
        "soul’s cleansing from bodily distraction toward truth",
        "ritual hygiene only",
        ["purif", "katharsis", "cleanse", "separate"],
    ),
    TermSpec(
        "phronēsis (φρόνησις)",
        "‘practical/intellectual wisdom’",
        "wisdom that sees Forms and orders life toward them",
        "mere cleverness",
        ["wisdom", "phronesis", "phronēsis", "knowing"],
        "nous",
    ),
]

MARCUS: list[TermSpec] = [
    TermSpec(
        "hēgemonikon (ἡγεμονικόν)",
        "‘ruling faculty’",
        "the governing center that assents, chooses, and can remain inviolate",
        "willpower pep-talk; misses Stoic physics of mind",
        ["ruling", "hegemonikon", "hēgemonikon", "governing", "reason within"],
        weight=1.4,
    ),
    TermSpec(
        "prohairesis (προαίρεσις)",
        "‘moral choice / volition’",
        "the sphere of what is up to us—judgment and impulse under assent",
        "free will as metaphysical libertarianism",
        ["choice", "prohairesis", "assent", "judgment", "up to"],
        weight=1.3,
    ),
    TermSpec(
        "logos (λόγος)",
        "‘reason / cosmic account’",
        "shared rational order in cosmos and in the human ruling faculty",
        "mere talk or logic puzzles",
        ["logos", "reason", "rational", "λόγος", "Nature"],
        "logos",
        weight=1.3,
    ),
    TermSpec(
        "phantasia (φαντασία)",
        "‘impression, appearance’",
        "presentations the hegemonikon must test before assent",
        "fantasy / imagination hobby",
        ["impression", "phantasia", "appearance", "seem"],
    ),
    TermSpec(
        "heimarmenē / fate",
        "‘allotted portion’",
        "ordered unfolding to be met with assent, not resentment",
        "fatalist passivity",
        ["fate", "allotted", "destiny", "providence", "Nature"],
        "physis",
    ),
    TermSpec(
        "oikeiōsis (οἰκείωσις)",
        "‘appropriation, affinity’",
        "natural affinity extending from self to cosmopolis",
        "tribal belonging",
        ["kin", "affinity", "common", "human", "citizen", "cosmopolis"],
    ),
    TermSpec(
        "thanatos / death",
        "‘death’",
        "limit that clarifies present action; not an evil in itself",
        "morbid fixation",
        ["death", "die", "depart", "mortal"],
        weight=1.2,
    ),
]

EPICTETUS: list[TermSpec] = [
    TermSpec(
        "eph' hēmin (ἐφ' ἡμῖν)",
        "‘upon us / up to us’",
        "the Stoic cut: freedom locates in what is genuinely ours—judgment, impulse, desire, aversion",
        "control-freak optimization of externals",
        ["eph'", "up to us", "in our power", "our power", "not in our power"],
        weight=1.5,
    ),
    TermSpec(
        "prohairesis (προαίρεσις)",
        "‘moral choice’",
        "the choosing self that uses impressions; sole site of good and bad",
        "free will metaphysics without Stoic psychology of assent",
        ["prohairesis", "προαίρεσις", "choice", "volition", "will"],
        weight=1.5,
    ),
    TermSpec(
        "phantasia (φαντασία)",
        "‘impression’",
        "appearance presented to the mind—primary object prohairesis works on",
        "daydream fantasy",
        ["phantasia", "φαντασία", "impression", "appearance"],
        weight=1.3,
    ),
    TermSpec(
        "dogma (δόγμα)",
        "‘judgment, belief’",
        "the evaluative take that disturbs—not the bare event",
        "dogma as rigid ideology only",
        ["dogma", "δόγμα", "judgment", "judgments", "opinion"],
        weight=1.3,
    ),
    TermSpec(
        "hormē (ὁρμή)",
        "‘impulse’",
        "impulse to act within the sphere of what is up to us",
        "raw urge without assent structure",
        ["horme", "hormē", "impulse"],
    ),
    TermSpec(
        "ataraxia (ἀταραξία)",
        "‘untroubledness’",
        "undisturbedness that follows correct use of impressions",
        "numb calm as goal",
        ["disturb", "ataraxia", "peace", "tranqu"],
    ),
]

PARMENIDES: list[TermSpec] = [
    TermSpec(
        "to eon / Being (τὸ ἐόν)",
        "neuter participle of εἰμί ‘what is’",
        "what-is as ungenerated, whole, immovable—object of genuine thought",
        "a big entity among entities; modern ‘existence’ predicate",
        ["being", "what-is", "it is", "eon", "ἐόν", "is and"],
        weight=1.5,
    ),
    TermSpec(
        "alētheia (ἀλήθεια)",
        "a- + lēthē ‘unconcealment / truth’",
        "the trustworthy path: that it is and cannot not be",
        "correspondence trivia",
        ["truth", "aletheia", "alētheia", "true", "Persuasion"],
        weight=1.3,
    ),
    TermSpec(
        "doxa (δόξα)",
        "‘seeming, opinion’",
        "mortal opinions about coming-to-be—the deceptive dual path",
        "mere ‘opinion’ as soft belief without cosmological stakes",
        ["opinion", "doxa", "δόξα", "seeming", "mortals"],
        weight=1.3,
    ),
    TermSpec(
        "hodos (ὁδός)",
        "‘road, way’",
        "ways of inquiry: the path of is vs the path of is-not",
        "lifestyle path metaphor",
        ["road", "way", "path", "hodos", "inquiry"],
        weight=1.4,
    ),
    TermSpec(
        "noein (νοεῖν)",
        "‘to think / to know’",
        "thinking and being co-disclosed—what can be thought is what is",
        "private mental events",
        ["think", "thinking", "thought", "noein", "νοεῖν", "know"],
        "nous",
        weight=1.3,
    ),
    TermSpec(
        "genesis / perishing",
        "coming-to-be and passing-away",
        "what the goddess bans from genuine Being",
        "biology of birth/death only",
        ["birth", "perish", "become", "genesis", "destruction", "generated"],
    ),
]

BANKS: dict[str, tuple[list[TermSpec], list[TermSpec]]] = {
    "know_yourself_ibn_arabi_balyani": (IBN_ARABI, IBN_ARABI[:3]),
    "rumi_mathnawi": (RUMI, RUMI[:3]),
    "pseudo_dionysius": (DIONYSIUS, DIONYSIUS[:3]),
    "meister_eckhart": (ECKHART, ECKHART[:3]),
    "the_cloud_of_unknowing": (CLOUD, CLOUD[:3]),
    "dhammapada": (DHAMMAPADA, DHAMMAPADA[:3]),
    "nagarjuna_mulamadhyamakakarika": (NAGARJUNA, NAGARJUNA[:3]),
    "heart_sutra": (HEART, HEART[:3]),
    "shantideva_bodhicaryavatara": (SHANTIDEVA, SHANTIDEVA[:3]),
    "dogen_shobogenzo": (DOGEN, DOGEN[:3]),
    "milarepa_songs": (MILAREPA, MILAREPA[:3]),
    "tilopa_mahamudra": (TILOPA, TILOPA[:3]),
    "plotinus_enneads": (PLOTINUS, PLOTINUS[:3]),
    "phaedo_plato": (PHAEDO, PHAEDO[:3]),
    "marcus_aurelius_meditations": (MARCUS, MARCUS[:3]),
    "epictetus_works": (EPICTETUS, EPICTETUS[:3]),
    "parmenides_fragments": (PARMENIDES, PARMENIDES[:3]),
}

# MD files with usable Key Terms (work_id -> paths)
MD_SOURCES: dict[str, list[str]] = {
    "heart_sutra": ["heart_sutra_pilot.md"],
    "nagarjuna_mulamadhyamakakarika": ["nagarjuna_mmk_pilot.md"],
    "shantideva_bodhicaryavatara": ["shantideva_bodhicaryavatara_pilot.md"],
    "tilopa_mahamudra": ["tilopa_mahamudra_pilot.md"],
    "meister_eckhart": ["meister_eckhart_abegescheidenheit.md"],
    "milarepa_songs": ["milarepa_songs_pilot.md", "milarepa_songs_wave_b.md"],
}

# Lemma hints for MD-parsed terms
LEMMA_HINTS: list[tuple[re.Pattern[str], str, Optional[str]]] = [
    (re.compile(r"śūnyatā|shunyata|sunyata", re.I), "sunyata", "sunyata.madhyamaka"),
    (re.compile(r"śūnya\b|shunya", re.I), "sunya", None),
    (re.compile(r"nirvāṇa|nirvana|nibbāna", re.I), "nirvana", None),
    (re.compile(r"fanā|fana\b", re.I), "fana", "fana.sufi"),
    (re.compile(r"tawḥīd|tawhid", re.I), "tawhid", "tawhid.islamic"),
    (re.compile(r"apophas|unknowing|negative theology", re.I), "apophasis", "apophasis.christian"),
    (re.compile(r"gelassen|abegescheiden|detach", re.I), "gelassenheit", "gelassenheit.eckhart"),
    (re.compile(r"henosis|ἕνωσις|the One", re.I), "henosis", "henosis.plotinian"),
    (re.compile(r"theosis|deif", re.I), "theosis", "theosis.christian"),
    (re.compile(r"nous|νοῦς|intellect", re.I), "nous", "nous.neoplatonic"),
    (re.compile(r"psychē|psyche|ψυχ", re.I), "psyche", None),
    (re.compile(r"logos|λόγος", re.I), "logos", None),
    (re.compile(r"vikalpa", re.I), "vikalpa", None),
    (re.compile(r"samādhi|samadhi", re.I), "samadhi", None),
    (re.compile(r"dharma|dhamma", re.I), "dharma", None),
    (re.compile(r"karma|kamma", re.I), "karma", "karma.indic"),
    (re.compile(r"saṃsāra|samsara", re.I), "samsara", None),
    (re.compile(r"anātman|anatman|no[- ]?self|mushin", re.I), "anatman", None),
    (re.compile(r"citta|sems\b", re.I), "citta", None),
]


def lemma_for_term(term: str) -> tuple[Optional[str], Optional[str]]:
    # Match headword only — never the gloss body (avoids false sunyata hits, etc.).
    head = term.split("—")[0].split("-")[0]
    for pat, lid, sid in LEMMA_HINTS:
        if pat.search(head):
            return lid, sid
    return None, None


def parse_md_units(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    chunks = re.split(r"\n(?=## )", text)
    out = []
    for chunk in chunks:
        if "### Key Terms" not in chunk:
            continue
        title_m = re.match(r"##\s+(.+)", chunk)
        src_m = re.search(r"\*\*Source:\*\*\s*(.+)", chunk)
        kt_m = re.search(r"### Key Terms\n(.*?)(?=\n### |\Z)", chunk, re.S)
        if not kt_m:
            continue
        terms = []
        for term, definition in MD_TERM_RE.findall(kt_m.group(1)):
            term = term.strip()
            definition = re.sub(r"\s+", " ", definition).strip()
            if not term or not definition:
                continue
            lid, sid = lemma_for_term(term)
            item: dict[str, Any] = {"term": term, "definition": definition}
            if lid:
                item["lemma_id"] = lid
            if sid:
                item["sense_id"] = sid
            terms.append(item)
        if not terms:
            continue
        # source ids like HS_001, MMK_24_18, ECK_001
        src = src_m.group(1).strip() if src_m else ""
        ids = re.findall(
            r"\b([A-Z]{2,5}_[A-Z0-9]+(?:_[A-Z0-9]+)*)\b",
            src,
        )
        out.append(
            {
                "title": title_m.group(1).strip() if title_m else "",
                "source": src,
                "ids": [i.lower() for i in ids],
                "items": terms[:5],
            }
        )
    return out


def build_md_index() -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = {}
    for work, files in MD_SOURCES.items():
        rows: list[dict[str, Any]] = []
        for fname in files:
            path = MD_DIR / fname
            if path.exists():
                rows.extend(parse_md_units(path))
        index[work] = rows
    return index


def match_md(unit: dict[str, Any], md_rows: list[dict[str, Any]]) -> Optional[list[dict[str, Any]]]:
    uid = str(unit.get("unit_id") or "")
    local = uid.split(".", 1)[-1].lower()
    title = fold(str(unit.get("title") or ""))
    source_id = str(unit.get("source_id") or unit.get("provenance", {}).get("original_id") or "").lower()
    # try id match
    for row in md_rows:
        for rid in row["ids"]:
            rid_norm = rid.lower().replace("-", "_")
            if rid_norm in local or rid_norm in source_id or local in rid_norm:
                return row["items"]
            # hs_001 vs HS_001
            if rid_norm.replace("_", "") in local.replace("_", ""):
                return row["items"]
    # title match
    best = None
    best_score = 0
    for row in md_rows:
        rt = fold(row["title"])
        if not rt or not title:
            continue
        if rt == title:
            return row["items"]
        # token overlap
        a, b = set(rt.split("_")), set(title.split("_"))
        if not a or not b:
            continue
        score = len(a & b) / max(len(a), len(b))
        if score > best_score:
            best_score = score
            best = row
    if best and best_score >= 0.5:
        return best["items"]
    return None


def set_key_terms_layer(unit: dict[str, Any], layer: dict[str, Any]) -> None:
    layers = unit.get("pratibha_layers")
    if not isinstance(layers, list):
        unit["pratibha_layers"] = [copy.deepcopy(layer)]
        return
    for i, row in enumerate(layers):
        if isinstance(row, dict) and row.get("kind") == "key_terms":
            layers[i] = copy.deepcopy(layer)
            return
    insertion = next(
        (
            i
            for i, row in enumerate(layers)
            if isinstance(row, dict) and row.get("kind") in AFTER_KEYTERMS
        ),
        len(layers),
    )
    layers.insert(insertion, copy.deepcopy(layer))


def enrich_unit(
    unit: dict[str, Any],
    md_index: dict[str, list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], str]:
    work = str(unit.get("work_id") or "")
    md_items = match_md(unit, md_index.get(work) or [])
    if md_items and 2 <= len(md_items) <= 5:
        return md_items, "md"
    if md_items and len(md_items) == 1:
        # pad from bank
        bank, fallback = BANKS[work]
        padded = select_from_bank(unit, bank, fallback)
        # keep md first, fill unique
        seen = {fold(i["term"]) for i in md_items}
        for it in padded:
            if fold(it["term"]) not in seen:
                md_items.append(it)
            if len(md_items) >= 3:
                break
        return md_items[:5], "md+bank"
    bank, fallback = BANKS[work]
    return select_from_bank(unit, bank, fallback), "bank"


def load_yaml_units(collections: set[str]) -> dict[str, tuple[Path, dict[str, Any]]]:
    out: dict[str, tuple[Path, dict[str, Any]]] = {}
    for work in collections:
        d = CANONICAL / work
        if not d.is_dir():
            continue
        for path in sorted(d.glob("*.yml")):
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                continue
            uid = str(data.get("unit_id") or "")
            if uid:
                out[uid] = (path, data)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--collection", action="append", default=[])
    args = parser.parse_args()

    collections = set(args.collection) if args.collection else set(COLLECTIONS)
    md_index = build_md_index()
    yaml_units = load_yaml_units(collections)

    # Load index
    raw_lines = INDEX.read_text(encoding="utf-8").splitlines()
    index_units = [json.loads(line) for line in raw_lines if line.strip()]
    index_by_uid = {
        str(u.get("unit_id")): i
        for i, u in enumerate(index_units)
        if u.get("work_id") in collections
    }

    stats_source = {"md": 0, "md+bank": 0, "bank": 0}
    by_work_n: dict[str, int] = {w: 0 for w in collections}
    by_work_terms: dict[str, list[int]] = {w: [] for w in collections}
    lemma_hits = 0
    lemma_total = 0
    attestation_gaps: dict[str, int] = {}
    changed_uids: list[str] = []

    # Enrich all YAML units in scope (includes yaml-only extras)
    for uid, (path, data) in sorted(yaml_units.items()):
        work = str(data.get("work_id") or "")
        if work not in collections:
            continue
        items, source = enrich_unit(data, md_index)
        if not items:
            continue
        layer = {
            "kind": "key_terms",
            "label": "Key Terms",
            "items": items,
            "layer_provenance": "editorial-enriched",
        }
        set_key_terms_layer(data, layer)
        stats_source[source] = stats_source.get(source, 0) + 1
        by_work_n[work] = by_work_n.get(work, 0) + 1
        by_work_terms.setdefault(work, []).append(len(items))
        for it in items:
            lemma_total += 1
            if it.get("lemma_id"):
                lemma_hits += 1
            else:
                attestation_gaps[it["term"]] = attestation_gaps.get(it["term"], 0) + 1
        changed_uids.append(uid)
        yaml_units[uid] = (path, data)

        # Sync into index if present
        if uid in index_by_uid:
            idx = index_by_uid[uid]
            index_unit = copy.deepcopy(index_units[idx])
            set_key_terms_layer(index_unit, layer)
            index_units[idx] = index_unit

    print("=== Enrichment plan ===")
    print(f"units={len(changed_uids)} sources={stats_source}")
    print(f"lemma_link_rate={lemma_hits}/{lemma_total}")
    for work in COLLECTIONS:
        if work not in collections:
            continue
        ns = by_work_terms.get(work) or []
        avg = (sum(ns) / len(ns)) if ns else 0.0
        print(
            f"  {work}: units={by_work_n.get(work, 0)} "
            f"avg_terms={avg:.1f} "
            f"min={min(ns) if ns else 0} max={max(ns) if ns else 0}"
        )
    print("\nHardest attestation gaps (no lemma_id), top 25:")
    for term, n in sorted(attestation_gaps.items(), key=lambda x: (-x[1], x[0]))[:25]:
        print(f"  {n:3d}  {term}")

    # Sample one unit per tradition cluster
    samples = [
        "know_yourself_ibn_arabi_balyani.kys_p001",
        "heart_sutra.hs_001",
        "epictetus_works.epi_enc_001",
        "pseudo_dionysius.pd_mt_06",
        "dogen_shobogenzo.dog_001",
    ]
    print("\n=== Samples ===")
    for uid in samples:
        if uid not in yaml_units:
            continue
        _, data = yaml_units[uid]
        kt = next(
            (
                L
                for L in data.get("pratibha_layers") or []
                if isinstance(L, dict) and L.get("kind") == "key_terms"
            ),
            None,
        )
        print(uid)
        for it in (kt or {}).get("items") or []:
            print(f"  - {it.get('term')}: {str(it.get('definition'))[:140]}")
            if it.get("lemma_id"):
                print(f"    lemma_id={it['lemma_id']}")

    if not args.write:
        print("\ndry-run only; re-run with --write to apply")
        return

    # Write YAML
    for uid in changed_uids:
        path, data = yaml_units[uid]
        atomic_write(path, dump_yaml(data))

    # Write index
    atomic_write(
        INDEX,
        "".join(json.dumps(u, ensure_ascii=False) + "\n" for u in index_units),
    )
    print(f"\nwrote {len(changed_uids)} YAML files and updated index.jsonl")


if __name__ == "__main__":
    main()

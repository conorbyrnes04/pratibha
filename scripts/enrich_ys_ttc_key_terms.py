#!/usr/bin/env python3
"""Editorial-enrich key_terms for Yoga Sūtras + Tao Te Ching.

Rewrites lexicon-seeded stubs into compact three-part glosses
(etymology -> meaning HERE -> translation trap), links lemmas when known,
sets layer_provenance: editorial-enriched, and syncs YAML + index.jsonl.

Dry-run by default. Pass --write to apply.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import tempfile
import unicodedata
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical"
INDEX = CANONICAL / "index.jsonl"

YS_DIR = CANONICAL / "patañjali_yoga_sūtras"
TTC_DIR = CANONICAL / "tao_te_ching"

WORKS = {
    "patañjali_yoga_sūtras": YS_DIR,
    "tao_te_ching": TTC_DIR,
}

KT_SECTION_RE = re.compile(
    r"Key Terms[:\s]*\n(.+?)(?:\n\s*Cross-Tradition|\n\s*Practice \(Abhyasa\)|\Z)",
    re.S | re.I,
)
KT_ITEM_RE = re.compile(r"\*\*([^*]+)\*\*\s*[—\-–]\s*(.+?)(?=\n\s*\*\*|\Z)", re.S)
NON_ALNUM = re.compile(r"[^a-z0-9\u4e00-\u9fff]+")


def fold(value: str) -> str:
    text = unicodedata.normalize("NFKD", value or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().strip()
    text = NON_ALNUM.sub("", text)
    return text


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", delete=False, dir=str(path.parent)
    ) as tmp:
        tmp.write(text)
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


def dump_yaml(data: dict[str, Any]) -> str:
    return yaml.safe_dump(
        data,
        allow_unicode=True,
        sort_keys=False,
        width=100,
        default_flow_style=False,
    )


# ---------------------------------------------------------------------------
# Term banks: etymology, trap, display form, lemma links, match keys
# ---------------------------------------------------------------------------

TermSpec = dict[str, Any]

YS_TERMS: list[TermSpec] = [
    {
        "keys": ["yoga", "योग"],
        "term": "yoga (योग)",
        "etym": "√yuj ‘yoke, harness, join’",
        "trap": "not a posture class or romantic ‘union’ fantasy — technical stilling/harnessing of mind",
        "lemma_id": "yoga",
        "sense_id": "yoga.classical",
    },
    {
        "keys": ["anusasana", "anuśāsana", "anuśāsanam", "अनुशासन"],
        "term": "anuśāsana (अनुशासन)",
        "etym": "anu-√śās ‘instruct along / discipline’",
        "trap": "not a casual ‘intro’; systematic disciplinary teaching that opens the path",
    },
    {
        "keys": ["atha"],
        "term": "atha (अथ)",
        "etym": "atha ‘now’ — auspicious commencement particle",
        "trap": "not filler ‘now then’; marks readiness and the opening of authorized instruction",
    },
    {
        "keys": ["citta", "cittam", "cittasya", "चित्त"],
        "term": "citta (चित्त)",
        "etym": "√cit ‘perceive/notice’ → mind-continuum as cognizing instrument",
        "trap": "not ‘brain software’ or an enemy to smash; the reflecting medium whose turnings veil puruṣa",
        "lemma_id": "citta",
    },
    {
        "keys": ["vrtti", "vritti", "vrttih", "वृत्ति"],
        "term": "vṛtti (वृत्ति)",
        "etym": "√vṛt ‘turn, revolve’ → a turning/modification",
        "trap": "not ‘bad thoughts’ only — any cognitive wave (valid cognition, error, fantasy, sleep, memory)",
    },
    {
        "keys": ["nirodha", "nirodhah", "निरोध"],
        "term": "nirodha (निरोध)",
        "etym": "ni + √rudh ‘obstruct, restrain’ → cessation/stilling",
        "trap": "not annihilation of mind; settling of flux so awareness is no longer hijacked",
    },
    {
        "keys": ["samadhi", "समाधि"],
        "term": "samādhi (समाधि)",
        "etym": "sam-ā-√dhā ‘settle completely together’",
        "trap": "not trance-entertainment or unconsciousness; graded absorption where subject–object friction quiets",
        "lemma_id": "samadhi",
        "sense_id": "samadhi.yoga",
    },
    {
        "keys": ["purusa", "purusha", "पुरुष"],
        "term": "puruṣa (पुरुष)",
        "etym": "‘person/witness’ in Sāṃkhya — pure awareness as seer",
        "trap": "not ‘person’ as social self; the unchanging witness distinct from prakṛti’s display",
    },
    {
        "keys": ["prakrti", "prakriti", "प्रकृति"],
        "term": "prakṛti (प्रकृति)",
        "etym": "pra-√kṛ ‘bring forth’ → productive nature/matter",
        "trap": "not pastoral ‘Nature’; the tri-guṇa matrix generating all experience including mind",
    },
    {
        "keys": ["guna", "gunah", "गुण"],
        "term": "guṇa (गुण)",
        "etym": "‘strand/quality’ — sattva, rajas, tamas as constitutive modes",
        "trap": "not optional personality traits; the dynamic constitution of all prakṛtic phenomena",
    },
    {
        "keys": ["klesa", "klesah", "क्लेश"],
        "term": "kleśa (क्लेश)",
        "etym": "√kliś ‘afflict, torment’ → afflictive root-patterns",
        "trap": "not mere ‘stress’; five deep causes (avidyā etc.) that generate suffering and rebirth",
    },
    {
        "keys": ["avidya", "अविद्या"],
        "term": "avidyā (अविद्या)",
        "etym": "a- + vidyā ‘non-knowing’ — mis-seeing the permanent/impure/self etc.",
        "trap": "not simple ignorance of facts; structural misidentification that parents the other kleśas",
        "lemma_id": "vidya",
    },
    {
        "keys": ["asmita", "अस्मिता"],
        "term": "asmitā (अस्मिता)",
        "etym": "asmi + -tā ‘I-am-ness’",
        "trap": "not healthy self-esteem; the confusion of seer with seeing-instrument (citta)",
    },
    {
        "keys": ["raga", "राग"],
        "term": "rāga (राग)",
        "etym": "√rañj ‘color, dye’ → affective coloring as attachment",
        "trap": "not only romantic desire; sticky attraction to pleasure that fuels bondage",
    },
    {
        "keys": ["dvesa", "द्वेष"],
        "term": "dveṣa (द्वेष)",
        "etym": "√dviṣ ‘hate’ → aversion",
        "trap": "not moral disapproval alone; reactive push-away that mirrors rāga as binding force",
    },
    {
        "keys": ["abhinivesa", "अभिनिवेश"],
        "term": "abhiniveśa (अभिनिवेश)",
        "etym": "abhi-ni-√viś ‘enter intensely into’ → clutch at continuity/life",
        "trap": "not only fear of death; instinctive clinging to existence even in the wise",
    },
    {
        "keys": ["abhyasa", "अभ्यास"],
        "term": "abhyāsa (अभ्यास)",
        "etym": "abhi-√ās ‘sit toward’ → sustained practice",
        "trap": "not sporadic effort; long, uninterrupted, earnest cultivation of stability",
    },
    {
        "keys": ["vairagya", "वैराग्य"],
        "term": "vairāgya (वैराग्य)",
        "etym": "vi-rāga ‘dispassion / fading of coloring’",
        "trap": "not cold indifference; mastery of thirst so objects lose compulsive pull",
    },
    {
        "keys": ["isvara", "ईश्वर"],
        "term": "īśvara (ईश्वर)",
        "etym": "√īś ‘rule, be capable’ → the special puruṣa untouched by kleśa/karma",
        "trap": "not necessarily a creator-god dogma; Patañjali’s omniscient special puruṣa as object of praṇidhāna",
    },
    {
        "keys": ["pranidhana", "प्रणिधान"],
        "term": "praṇidhāna (प्रणिधान)",
        "etym": "pra-ni-√dhā ‘place thoroughly toward’ → dedicated surrender/orientation",
        "trap": "not fatalistic resignation; active offering of practice-mind toward īśvara",
    },
    {
        "keys": ["om", "pranava", "प्रणव"],
        "term": "praṇava / oṃ (प्रणव)",
        "etym": "praṇava as the voiced designator of īśvara",
        "trap": "not a lucky charm syllable; sonic support for japa and meaning-absorption (tad-artha-bhāvana)",
    },
    {
        "keys": ["japa", "जप"],
        "term": "japa (जप)",
        "etym": "√jap ‘mutter, recite’ → repeated vocal/mental sounding",
        "trap": "not empty repetition; practice that ripens into inwardness and removal of obstacles",
    },
    {
        "keys": ["pramana", "प्रमाण"],
        "term": "pramāṇa (प्रमाण)",
        "etym": "pra-√mā ‘measure accurately’ → valid means of knowing",
        "trap": "not ‘proof’ in courtroom sense alone; perception, inference, testimony as vṛtti-types",
    },
    {
        "keys": ["viparyaya", "विपर्यय"],
        "term": "viparyaya (विपर्यय)",
        "etym": "vi-pari-√i ‘go the wrong way’ → misconception",
        "trap": "not mere mistake of detail; false cognition mistaking the form of something for what it is not",
    },
    {
        "keys": ["vikalpa", "विकल्प"],
        "term": "vikalpa (विकल्प)",
        "etym": "vi-√kḷp ‘fashion alternately’ → verbal/constructive ideation",
        "trap": "not all thinking; cognition following words without a corresponding object present",
        "lemma_id": "vikalpa",
        "sense_id": "vikalpa.shaiva",
    },
    {
        "keys": ["nidra", "निद्रा"],
        "term": "nidrā (निद्रा)",
        "etym": "ni-√drā ‘sleep’ → sleep as a distinct vṛtti",
        "trap": "not mere rest; a cognition of absence that still counts as mental modification to be stilled",
    },
    {
        "keys": ["smrti", "smriti", "स्मृति"],
        "term": "smṛti (स्मृति)",
        "etym": "√smṛ ‘remember’ → memory as re-presentation",
        "trap": "not archival storage only; a vṛtti that re-lives past experience without adding new object",
    },
    {
        "keys": ["samskara", "संस्कार", "saṃskāra", "samskāra"],
        "term": "saṃskāra (संस्कार)",
        "etym": "sam-√kṛ ‘put together / impress’ → formative latent imprint",
        "trap": "not only life-cycle rites; residual grooves that propel future citta movement",
        "lemma_id": "samskara",
        "sense_id": "samskara.habit",
    },
    {
        "keys": ["vasana", "वासना"],
        "term": "vāsanā (वासना)",
        "etym": "√vas ‘dwell’ → lingering scent/habit-tendency",
        "trap": "not vague ‘vibes’; subliminal residue that can fruit when conditions align",
    },
    {
        "keys": ["karma", "कर्म"],
        "term": "karma (कर्म)",
        "etym": "√kṛ ‘do’ → action and its formative result-structure",
        "trap": "not cosmic scorekeeping cartoon; action-deposit that conditions birth, span, and experience",
        "lemma_id": "karma",
        "sense_id": "karma.indic",
    },
    {
        "keys": ["karmasaya", "कर्माशय"],
        "term": "karmāśaya (कर्माशय)",
        "etym": "karma + āśaya ‘repository’ → deposit of action-potency",
        "trap": "not a literal warehouse; the latent store from which fruitions arise across lives",
    },
    {
        "keys": ["yama", "यम"],
        "term": "yama (यम)",
        "etym": "√yam ‘restrain’ → outer ethical restraints",
        "trap": "not optional etiquette; first limb establishing non-harm etc. as practice ground",
    },
    {
        "keys": ["niyama", "नियम"],
        "term": "niyama (नियम)",
        "etym": "ni-√yam ‘bind down / observe’ → observances",
        "trap": "not self-help habits only; purity, contentment, tapas, study, īśvara-praṇidhāna as limbs",
    },
    {
        "keys": ["ahimsa", "अहिंसा"],
        "term": "ahiṃsā (अहिंसा)",
        "etym": "a- + hiṃsā ‘non-injury’",
        "trap": "not passivity; active non-harm that ripens into ambient safety (pratishṭhā)",
    },
    {
        "keys": ["satya", "सत्य"],
        "term": "satya (सत्य)",
        "etym": "sat ‘what is’ → truthfulness aligned with being",
        "trap": "not bluntness; speech and knowing that do not distort what is",
    },
    {
        "keys": ["asteya", "अस्तेय"],
        "term": "asteya (अस्तेय)",
        "etym": "a- + steya ‘non-stealing’",
        "trap": "not only property law; non-appropriation that includes subtle taking of credit/energy",
    },
    {
        "keys": ["brahmacarya", "ब्रह्मचर्य"],
        "term": "brahmacarya (ब्रह्मचर्य)",
        "etym": "brahman + carya ‘moving in the sacred/continuum’",
        "trap": "not only celibacy slogan; energy-conservation and fidelity of orientation",
    },
    {
        "keys": ["aparigraha", "अपरिग्रह"],
        "term": "aparigraha (अपरिग्रह)",
        "etym": "a- + pari-graha ‘non-grasping/hoarding’",
        "trap": "not aesthetic minimalism; release of acquisitive clutch that clarifies why one is born as one is",
    },
    {
        "keys": ["sauca", "शौच"],
        "term": "śauca (शौच)",
        "etym": "√śuc ‘be clean/bright’ → purity",
        "trap": "not hygiene alone; outer/inner cleansing that breeds distaste for bodily identification and clarity of sattva",
    },
    {
        "keys": ["samtosa", "सन्तोष", "santosa"],
        "term": "saṃtoṣa (संतोष)",
        "etym": "sam-√tuṣ ‘be content’",
        "trap": "not complacency; contentment that yields unsurpassed happiness as practice-fruit",
    },
    {
        "keys": ["tapas", "तपस्", "तपः"],
        "term": "tapas (तपस्)",
        "etym": "√tap ‘heat, burn’ → austerity as transformative heat",
        "trap": "not self-harm; disciplined heat that burns impurity and ripens body/sense capacity",
    },
    {
        "keys": ["svadhyaya", "स्वाध्याय"],
        "term": "svādhyāya (स्वाध्याय)",
        "etym": "sva + adhyāya ‘self-study / study of what is one’s own’",
        "trap": "not generic reading; scriptural/self-inquiry that can culminate in contact with desired deity/form",
    },
    {
        "keys": ["asana", "आसन"],
        "term": "āsana (आसन)",
        "etym": "√ās ‘sit’ → stable seated posture",
        "trap": "not gymnastic catalogue; steady, easeful seat that removes disturbance for further limbs",
    },
    {
        "keys": ["pranayama", "प्राणायाम"],
        "term": "prāṇāyāma (प्राणायाम)",
        "etym": "prāṇa + āyāma ‘extension/regulation of breath-life’",
        "trap": "not breath tricks for calm apps; interruption of inhalation/exhalation that thins the covering of light",
    },
    {
        "keys": ["prana", "प्राण"],
        "term": "prāṇa (प्राण)",
        "etym": "pra-√an ‘breathe forth’ → vital breath/force",
        "trap": "not oxygen alone; the life-current whose regulation alters citta’s coverings",
    },
    {
        "keys": ["pratyahara", "प्रत्याहार"],
        "term": "pratyāhāra (प्रत्याहार)",
        "etym": "prati-ā-√hṛ ‘draw back toward’ → sense-withdrawal",
        "trap": "not sensory deprivation; senses following citta’s inward turn as bees follow the queen",
    },
    {
        "keys": ["dharana", "धारणा"],
        "term": "dhāraṇā (धारणा)",
        "etym": "√dhṛ ‘hold’ → binding mind to a place",
        "trap": "not casual focus; deliberate localization of citta that begins saṃyama",
    },
    {
        "keys": ["dhyana", "ध्यान"],
        "term": "dhyāna (ध्यान)",
        "etym": "√dhyā ‘contemplate’ → unbroken flow toward the object",
        "trap": "not ‘thinking about’; continuous single-current cognizing that deepens dhāraṇā",
    },
    {
        "keys": ["samyama", "संयम"],
        "term": "saṃyama (संयम)",
        "etym": "sam-√yam ‘hold together’ → the triad dhāraṇā-dhyāna-samādhi as one",
        "trap": "not generic self-control; technical confluence that yields prajñā and siddhis",
    },
    {
        "keys": ["prajna", "प्रज्ञा"],
        "term": "prajñā (प्रज्ञा)",
        "etym": "pra-√jñā ‘know forth’ → discerning insight",
        "trap": "not IQ; lucid knowing that arises in samādhi and can be truth-bearing (ṛtambharā)",
        "lemma_id": "jnana",
    },
    {
        "keys": ["rtambhara", "ऋतंभरा"],
        "term": "ṛtambharā (ऋतंभरा)",
        "etym": "ṛta + bhara ‘bearing the real/order’",
        "trap": "not mystical vibe; prajñā that carries truth rather than inference or testimony alone",
    },
    {
        "keys": ["viveka", "विवेक"],
        "term": "viveka (विवेक)",
        "etym": "vi-√vic ‘discriminate apart’ → discernment",
        "trap": "not intellectual nitpicking; seeing the difference between puruṣa and sattva/prakṛti",
        "lemma_id": "aviveka",
    },
    {
        "keys": ["vivekakhyati", "विवेकख्याति"],
        "term": "viveka-khyāti (विवेकख्याति)",
        "etym": "discernment + khyāti ‘clear appearing’",
        "trap": "not a belief that one is the Self; uninterrupted discriminative revelation ending kaivalya’s approach",
    },
    {
        "keys": ["kaivalya", "कैवल्य"],
        "term": "kaivalya (कैवल्य)",
        "etym": "kevala ‘alone/absolute’ → aloneness/independence of puruṣa",
        "trap": "not lonely isolation; establishment in own-form when guṇas reverse and citi-śakti stands as itself",
        "lemma_id": "moksa",
    },
    {
        "keys": ["drastr", "drashta", "द्रष्टृ"],
        "term": "draṣṭṛ (द्रष्टृ)",
        "etym": "√dṛś ‘see’ → the Seer",
        "trap": "not the eyeball-subject; puruṣa as pure seeing, ordinarily seeming colored by what is seen",
    },
    {
        "keys": ["drsya", "दृश्य"],
        "term": "dṛśya (दृश्य)",
        "etym": "‘the seeable’ — prakṛti as object for the Seer",
        "trap": "not only outer world; includes mind and body as experienced object-field",
    },
    {
        "keys": ["svarupa", "स्वरूप"],
        "term": "svarūpa (स्वरूप)",
        "etym": "sva + rūpa ‘own form’",
        "trap": "not personality essence; the Seer’s standing in itself when vṛtti quiet",
    },
    {
        "keys": ["parinama", "परिणाम"],
        "term": "pariṇāma (परिणाम)",
        "etym": "pari-√nam ‘bend around / transform’ → transformation",
        "trap": "not random change; structured transformation of dharma/lakṣaṇa/avasthā that saṃyama can know",
    },
    {
        "keys": ["dharma", "धर्म"],
        "term": "dharma (धर्म)",
        "etym": "√dhṛ ‘uphold’ → property/quality upheld by a substrate",
        "trap": "not only ‘duty/religion’; here often a property-phase of an underlying dharmin",
        "lemma_id": "dharma",
    },
    {
        "keys": ["siddhi", "सिद्धि"],
        "term": "siddhi (सिद्धि)",
        "etym": "√sidh ‘accomplish’ → accomplishment/power",
        "trap": "not the goal; attainments that can distract from kaivalya if clung to",
        "lemma_id": "siddhi",
        "sense_id": "siddhi.indic",
    },
    {
        "keys": ["sabija", "सबीज"],
        "term": "sabīja (सबीज)",
        "etym": "sa + bīja ‘with seed’",
        "trap": "not botanical metaphor only; samādhi still carrying latent object/seed vs seedless",
    },
    {
        "keys": ["nirbija", "निर्बीज"],
        "term": "nirbīja (निर्बीज)",
        "etym": "nir + bīja ‘seedless’",
        "trap": "not blank nihilism; absorption without residual object-seed, toward ultimate restraint",
    },
    {
        "keys": ["samprajnata", "सम्प्रज्ञात"],
        "term": "samprajñāta (सम्प्रज्ञात)",
        "etym": "sam-pra-√jñā ‘known together with’ → cognitive samādhi with support",
        "trap": "not ‘lower failure’; valid staged absorption still involving vitarka/vicāra/ānanda/asmitā supports",
    },
    {
        "keys": ["asamprajnata", "असम्प्रज्ञात"],
        "term": "asamprajñāta (असम्प्रज्ञात)",
        "etym": "a- + samprajñāta → non-cognitive / beyond supported knowing",
        "trap": "not coma; cessation of supported cognitions through latent impressions of cessation",
    },
    {
        "keys": ["vitarka", "वितर्क"],
        "term": "vitarka (वितर्क)",
        "etym": "vi-√tark ‘reason about’ → gross discursive engagement with object",
        "trap": "not idle argument; a level of samprajñāta still working with gross object-aspect",
    },
    {
        "keys": ["vicara", "विचार"],
        "term": "vicāra (विचार)",
        "etym": "vi-√car ‘move through’ → subtle reflective engagement",
        "trap": "not ordinary rumination; subtler samprajñāta level beyond gross vitarka",
    },
    {
        "keys": ["ananda", "आनन्द"],
        "term": "ānanda (आनन्द)",
        "etym": "ā-√nand ‘rejoice’ → bliss-tone of certain samādhi",
        "trap": "not hedonism; a support-level of absorption, still not final kaivalya",
        "lemma_id": "cidananda",
    },
    {
        "keys": ["pratiprasava", "प्रतिप्रसव"],
        "term": "pratiprasava (प्रतिप्रसव)",
        "etym": "prati + prasava ‘reverse generation / involution’",
        "trap": "not cosmic destruction fantasy; guṇas returning to quiescence when purpose for puruṣa is done",
    },
    {
        "keys": ["citi", "citisakti", "चिति"],
        "term": "citi-śakti (चितिशक्ति)",
        "etym": "citi ‘awareness’ + śakti ‘power’ — consciousness-power as such",
        "trap": "not a goddess add-on; puruṣa’s own knowing-power standing in svarūpa at kaivalya",
        "lemma_id": "cit",
    },
    {
        "keys": ["duhkha", "duhkham", "दुःख"],
        "term": "duḥkha (दुःख)",
        "etym": "dus + kha ‘bad axle-hole’ → suffering/friction",
        "trap": "not only acute pain; the structural unsatisfactoriness yogins see even in pleasure’s change",
    },
    {
        "keys": ["heya", "हेय"],
        "term": "heya (हेय)",
        "etym": "√hā ‘abandon’ → that which is to be discarded (future suffering)",
        "trap": "not past pain fixation; the avoidable future duḥkha that viveka aims to cut",
    },
    {
        "keys": ["hanopadeya", "hāna", "हान"],
        "term": "hāna (हान)",
        "etym": "√hā ‘abandon’ → cessation/abandonment as goal",
        "trap": "not repression; the ending of future suffering’s cause through viveka",
    },
    {
        "keys": ["hetu", "हेतु"],
        "term": "hetu (हेतु)",
        "etym": "‘cause/reason’",
        "trap": "not vague ‘reason why’; the causal factor (often saṃyoga of seer/seen) producing heya",
    },
    {
        "keys": ["samyoga", "संयोग"],
        "term": "saṃyoga (संयोग)",
        "etym": "sam-√yuj ‘join together’ → conjunction of seer and seen",
        "trap": "not romantic union; the mis-conjunction that is the hetu of suffering",
    },
    {
        "keys": ["nirodhaparinama", "निरोधपरिणाम"],
        "term": "nirodha-pariṇāma (निरोधपरिणाम)",
        "etym": "transformation toward restraint — moments of stillness overpowering outgoing moments",
        "trap": "not sudden magic silence; measurable shift in citta’s patterning toward restraint",
    },
    {
        "keys": ["ekagrata", "एकाग्रता"],
        "term": "ekāgratā (एकाग्रता)",
        "etym": "eka + agra ‘one-pointedness’",
        "trap": "not tunnel vision; citta’s transformation into stable single-point flow",
    },
    {
        "keys": ["sattva", "सत्त्व"],
        "term": "sattva (सत्त्व)",
        "etym": "sat + tva ‘being-ness / luminosity-clarity strand’",
        "trap": "not moral ‘goodness’ alone; the guṇa of clarity that can still bind if identified with",
    },
    {
        "keys": ["rajas", "रजस्"],
        "term": "rajas (रजस्)",
        "etym": "√rañj / ‘dust, passion’ → activating strand",
        "trap": "not only anger; kinetic agitation that paints experience with restlessness",
    },
    {
        "keys": ["tamas", "तमस्"],
        "term": "tamas (तमस्)",
        "etym": "‘darkness/inertia’ strand",
        "trap": "not evil; obscuring heaviness that veils discrimination",
    },
    {
        "keys": ["bija", "बीज"],
        "term": "bīja (बीज)",
        "etym": "‘seed’ — latent causal potency",
        "trap": "not metaphor for ‘potential’ vaguely; technical seed of kleśa/karma/object in absorption theory",
    },
    {
        "keys": ["pratipaksa", "प्रतिपक्ष"],
        "term": "pratipakṣa-bhāvana (प्रतिपक्षभावन)",
        "etym": "pratipakṣa ‘opposite side’ + bhāvana ‘cultivation’",
        "trap": "not positive thinking; deliberate counter-cultivation against afflictive thoughts",
    },
    {
        "keys": ["pratyaya", "प्रत्यय"],
        "term": "pratyaya (प्रत्यय)",
        "etym": "prati-√i ‘go toward’ → cognitive content/presentation",
        "trap": "not grammatical ‘suffix’; the mind’s object-presenting content in a given moment",
    },
    {
        "keys": ["alambana", "आलम्बन"],
        "term": "ālambana (आलम्बन)",
        "etym": "ā-√lamb ‘lean on’ → support/object of meditation",
        "trap": "not crutch in a weak sense; the chosen support that citta rests upon in practice",
    },
    {
        "keys": ["angani", "anga", "अङ्ग"],
        "term": "aṅga (अङ्ग)",
        "etym": "‘limb/accessory’ of the eightfold path",
        "trap": "not body-part list for its own sake; interdependent accessories culminating in samādhi",
    },
]

TTC_TERMS: list[TermSpec] = [
    {
        "keys": ["dao", "tao", "道", "dào"],
        "term": "dào (道)",
        "etym": "道 ‘path/way; to speak/lead’",
        "trap": "not a deity named Tao or a lifestyle brand — source-and-course that resists full naming",
        "lemma_id": "dao",
        "sense_id": "dao.daoist",
    },
    {
        "keys": ["de", "te", "德", "dé"],
        "term": "dé (德)",
        "etym": "德 ‘virtue/potency/accrued power’",
        "trap": "not Victorian moralism — a thing’s unforced efficacy when it accords with dào",
        "lemma_id": "de",
        "sense_id": "de.daoist",
    },
    {
        "keys": ["wuwei", "无为", "無為", "wúwéi", "wú wéi"],
        "term": "wúwéi (無為)",
        "etym": "無 ‘without’ + 為 ‘doing/making/deeming’",
        "trap": "not laziness or zero activity — skilled non-imposition that leaves nothing undone",
        "lemma_id": "wuwei",
        "sense_id": "wuwei.daoist",
    },
    {
        "keys": ["ziran", "自然", "zìrán", "zì rán"],
        "term": "zìrán (自然)",
        "etym": "自 ‘self’ + 然 ‘so/thus’ → self-so",
        "trap": "not wilderness romanticism or do-whatever impulse — being so of itself without forced sanding",
        "lemma_id": "ziran",
        "sense_id": "ziran.daoist",
    },
    {
        "keys": ["xuan", "玄", "xuán"],
        "term": "xuán (玄)",
        "etym": "玄 ‘deep dark / reddish-black of depth’",
        "trap": "not romantic ‘mystery’; structural depth that cannot be exhausted by one approach",
    },
    {
        "keys": ["chang", "常", "cháng"],
        "term": "cháng (常)",
        "etym": "常 ‘constant/enduring’",
        "trap": "not theological eternity with start/stop brackets — what persists through change without being used up",
    },
    {
        "keys": ["名"],
        "term": "míng (名)",
        "etym": "名 ‘name/fame/designation’",
        "trap": "not mere label; the carving power that mothers the ten thousand things into distinctness",
        "char_keys": ["名"],
    },
    {
        "keys": ["明"],
        "term": "míng (明)",
        "etym": "明 ‘bright/clear/illumine’",
        "trap": "not IQ brightness; lucid seeing that often comes from yielding rather than glare",
        "char_keys": ["明"],
    },
    {
        "keys": ["wu", "無", "wú"],
        "term": "wú (無)",
        "etym": "無 ‘without / not-have’",
        "trap": "not nihilistic void; generative absence (of forcing, name, desire) that opens function",
    },
    {
        "keys": ["you", "有", "yǒu"],
        "term": "yǒu (有)",
        "etym": "有 ‘there-is / having’",
        "trap": "not mere possession; the named/manifest pole that co-arises with wú",
    },
    {
        "keys": ["miao", "妙", "miào"],
        "term": "miào (妙)",
        "etym": "妙 ‘subtle/fine/wonderful’",
        "trap": "not vague mysticism; interior fine-grain of the real as seen from non-desire",
    },
    {
        "keys": ["jiao", "徼", "jiǎo"],
        "term": "jiǎo (徼)",
        "etym": "徼 ‘boundary/edge/threshold’",
        "trap": "not ‘outcome’ alone; the outer fringe desire can map while missing interiority",
    },
    {
        "keys": ["wanwu", "萬物", "万物", "wànwù", "wàn wù"],
        "term": "wànwù (萬物)",
        "etym": "萬 ‘myriad’ + 物 ‘things’",
        "trap": "not a zoo inventory; the whole differentiated field born once naming divides",
    },
    {
        "keys": ["tian", "天", "tiān"],
        "term": "tiān (天)",
        "etym": "天 ‘heaven/sky’ — cosmic order above human forcing",
        "trap": "not a personal sky-god by default; impersonal heaven-pattern the sage aligns with",
    },
    {
        "keys": ["tianxia", "天下", "tiānxià"],
        "term": "tiānxià (天下)",
        "etym": "天+下 ‘all under heaven’ — the political-cosmic whole",
        "trap": "not only ‘the world’ as map; the realm that cannot be seized by contrivance",
    },
    {
        "keys": ["shengren", "聖人", "圣人", "shèngrén"],
        "term": "shèngrén (聖人)",
        "etym": "聖 ‘sage-adept’ + 人 ‘person’",
        "trap": "not canonized saint; the one who acts by emptying self-assertion so the world orders itself",
    },
    {
        "keys": ["pu", "朴", "樸", "pǔ", "pú"],
        "term": "pǔ (朴)",
        "etym": "朴/樸 ‘uncarved wood / raw simplicity’",
        "trap": "not rustic branding; pre-carved wholeness before names and uses split it",
    },
    {
        "keys": ["rou", "柔", "róu"],
        "term": "róu (柔)",
        "etym": "柔 ‘soft/supple’",
        "trap": "not weakness as failure; yielding strength that outlasts the hard",
    },
    {
        "keys": ["ruo", "弱", "ruò"],
        "term": "ruò (弱)",
        "etym": "弱 ‘weak/pliant’",
        "trap": "not pathetic frailty; strategic pliancy aligned with water’s way",
    },
    {
        "keys": ["shui", "水", "shuǐ"],
        "term": "shuǐ (水)",
        "etym": "水 ‘water’ — paradigmatic soft that benefits all",
        "trap": "not decorative nature image; ethical-cosmic model for dwelling low without contention",
    },
    {
        "keys": ["buzheng", "不爭", "不争", "bùzhēng", "bù zhēng"],
        "term": "bùzhēng (不爭)",
        "etym": "不 ‘not’ + 爭 ‘contend/strive’",
        "trap": "not conflict-avoidant niceness; non-contention as the mode that none can contend with",
    },
    {
        "keys": ["fan", "反", "fǎn"],
        "term": "fǎn (反)",
        "etym": "反 ‘return/reverse’",
        "trap": "not mere opposition; the dào’s movement of reversal/return as structural law",
    },
    {
        "keys": ["qiang", "強", "强", "qiáng"],
        "term": "qiáng (強)",
        "etym": "強 ‘strong/forceful’",
        "trap": "not virtue of dominance; often the stiff strength that dies first, opposite of living soft",
    },
    {
        "keys": ["jing", "靜", "静", "jìng"],
        "term": "jìng (靜)",
        "etym": "靜 ‘still/quiet’",
        "trap": "not inert silence; stillness that masters restlessness and returns things to root",
    },
    {
        "keys": ["gen", "根", "gēn"],
        "term": "gēn (根)",
        "etym": "根 ‘root’",
        "trap": "not botanical aside; return-to-root as the quiet from which enduring life issues",
    },
    {
        "keys": ["yi", "一", "yī"],
        "term": "yī (一)",
        "etym": "一 ‘one’ — unifying hold",
        "trap": "not numerical trivia; embracing the One (bào yī) as integration against dispersal",
    },
    {
        "keys": ["baoyi", "抱一", "bào yī"],
        "term": "bào yī (抱一)",
        "etym": "抱 ‘embrace’ + 一 ‘one’",
        "trap": "not cuddly unity rhetoric; concentrating the vital into undivided alignment",
    },
    {
        "keys": ["qi", "氣", "气", "qì"],
        "term": "qì (氣)",
        "etym": "氣 ‘breath/vapor/vital process’",
        "trap": "not New Age electricity; psycho-physical process-field refined or turbid in practice",
        "lemma_id": "qi",
        "sense_id": "qi.chinese",
    },
    {
        "keys": ["xin", "心", "xīn"],
        "term": "xīn (心)",
        "etym": "心 ‘heart-mind’ (thought-feeling undivided)",
        "trap": "not brain-only mind or soft sentiment; the seat emptied or filled in Daoist/Confucian work",
        "lemma_id": "xin",
        "sense_id": "xin.chinese",
    },
    {
        "keys": ["xu", "虛", "虚", "xū"],
        "term": "xū (虛)",
        "etym": "虛 ‘empty/open/unoccupied’",
        "trap": "not nihilism; fertile vacancy in which dào collects and responds",
    },
    {
        "keys": ["yong", "用", "yòng"],
        "term": "yòng (用)",
        "etym": "用 ‘use/function’",
        "trap": "not utilitarianism; function that often arises from emptiness (wú) as the wheel hub",
    },
    {
        "keys": ["xuande", "玄德", "xuán dé"],
        "term": "xuán dé (玄德)",
        "etym": "玄+德 ‘dark/deep potency’",
        "trap": "not secret magic power; virtue so unadvertised it seems obscure yet generative",
        "lemma_id": "de",
        "sense_id": "de.daoist",
    },
    {
        "keys": ["zihua", "自化", "zì huà"],
        "term": "zìhuà (自化)",
        "etym": "自+化 ‘self-transform / transform of themselves’",
        "trap": "not laissez-faire neglect; the world’s self-ordering when the sage ceases interference",
    },
    {
        "keys": ["wushi", "無事", "无事", "wú shì"],
        "term": "wúshì (無事)",
        "etym": "無+事 ‘without (meddling) affairs’",
        "trap": "not unemployment; governing by not stirring needless business",
    },
    {
        "keys": ["wuyu", "無欲", "无欲", "wú yù"],
        "term": "wúyù (無欲)",
        "etym": "無+欲 ‘without desire/craving stance’",
        "trap": "not numbness; sustained non-grasping attention that perceives miào",
    },
    {
        "keys": ["fa", "法", "fǎ"],
        "term": "fǎ (法)",
        "etym": "法 ‘model/law/pattern’",
        "trap": "not only legal statute; patterning (humans model earth, earth heaven, heaven dào, dào zìrán)",
        "lemma_id": "li",
    },
    {
        "keys": ["zhengyanruofan", "正言若反"],
        "term": "zhèng yán ruò fǎn (正言若反)",
        "etym": "正言 ‘straight words’ + 若反 ‘seem reverse’",
        "trap": "not riddling for style; true speech that sounds paradoxical because the dào reverses expectations",
    },
    {
        "keys": ["daxiang", "大象", "dà xiàng"],
        "term": "dà xiàng (大象)",
        "etym": "大+象 ‘great image/form’",
        "trap": "not a big statue; the formless great image of dào that seems incomplete yet inexhaustible",
    },
    {
        "keys": ["weiming", "微明", "wēi míng"],
        "term": "wēi míng (微明)",
        "etym": "微 ‘subtle’ + 明 ‘clarity’",
        "trap": "not dim lightbulb; subtle clarity that sees soft/weak strategies before force does",
    },
    {
        "keys": ["gongsuishentui", "功遂身退"],
        "term": "gōng suì shēn tuì (功遂身退)",
        "etym": "功遂 ‘work accomplished’ + 身退 ‘person withdraws’",
        "trap": "not quitting early; heaven’s way — finish the work and do not cling to the role",
    },
    {
        "keys": ["天下神器", "shénqì", "神器"],
        "term": "tiānxià shénqì (天下神器)",
        "etym": "天下 ‘all-under-heaven’ + 神器 ‘spirit-like vessel/instrument’",
        "trap": "not a sacred object to seize; the world’s holy implement that breaks when forced",
    },
    {
        "keys": ["qubiqici", "去彼取此"],
        "term": "qù bǐ qǔ cǐ (去彼取此)",
        "etym": "去彼 ‘leave that’ + 取此 ‘take this’",
        "trap": "not consumer choice; reject sensory overstimulation for the belly/root sufficiency",
    },
    {
        "keys": ["wubuwei", "無不為", "无不為", "wú bù wéi"],
        "term": "wú bù wéi (無不為)",
        "etym": "無不為 ‘nothing not done’ — corollary of wúwéi",
        "trap": "not omnipotent micromanagement; when non-forcing holds, everything gets done",
        "lemma_id": "wuwei",
        "sense_id": "wuwei.daoist",
    },
    {
        "keys": ["shen", "身", "shēn"],
        "term": "shēn (身)",
        "etym": "身 ‘body/person/self-as-lived’",
        "trap": "not corpse anatomy only; the vulnerable personhood one can lose by clinging to empire/self",
    },
    {
        "keys": ["yu", "愚", "yú"],
        "term": "yú (愚)",
        "etym": "愚 ‘foolish/simple-seeming’",
        "trap": "not stupidity as defect; cultivated uncarved seeming that refuses clever fragmentation",
    },
    {
        "keys": ["ci", "雌", "cí"],
        "term": "cí (雌)",
        "etym": "雌 ‘female/feminine’ as receptive polarity",
        "trap": "not gender stereotype; strategic receptivity (know the male, keep the female) as valley-power",
    },
    {
        "keys": ["xiong", "雄", "xióng"],
        "term": "xióng (雄)",
        "etym": "雄 ‘male/masculine’ as active polarity",
        "trap": "not endorsement of dominance; the known pole one does not cling to while holding the receptive",
    },
    {
        "keys": ["wuji", "无极", "無極", "wújí"],
        "term": "wújí (無極)",
        "etym": "無+極 ‘without limit/pole’",
        "trap": "not infinity poster art; return to the unlimited before polar carving",
    },
    {
        "keys": ["dadao", "大道", "dàdào"],
        "term": "dà dào (大道)",
        "etym": "大+道 ‘great way’",
        "trap": "not highway metaphor only; the broad way people abandon for side-paths of cleverness",
        "lemma_id": "dao",
        "sense_id": "dao.daoist",
    },
]


def build_index(specs: list[TermSpec]) -> dict[str, TermSpec]:
    out: dict[str, TermSpec] = {}
    for spec in specs:
        for key in spec.get("keys") or []:
            out[fold(key)] = spec
        for key in spec.get("char_keys") or []:
            out[fold(key)] = spec
        # also index by display term fold
        out[fold(spec["term"])] = spec
    return out


YS_INDEX = build_index(YS_TERMS)
TTC_INDEX = build_index(TTC_TERMS)

# Terms that are lexicon noise for TTC when they appear only via resonances
TTC_BLOCK = {
    "brahman",
    "karma",
    "sunyata",
    "sunya",
    "atman",
    "nirvana",
    "yoga",
    "samadhi",
    "citta",
    "moksa",
    "pinyin汉字",
    "pinyin",
}


def layer_body(unit: dict[str, Any], kind: str) -> str:
    for layer in unit.get("pratibha_layers") or []:
        if isinstance(layer, dict) and layer.get("kind") == kind:
            return str(layer.get("body") or "")
    return ""


def buried_key_terms(unit: dict[str, Any]) -> list[tuple[str, str]]:
    texts = [
        layer_body(unit, "commentary"),
        str(unit.get("commentary") or ""),
    ]
    found: list[tuple[str, str]] = []
    seen: set[str] = set()
    for text in texts:
        m = KT_SECTION_RE.search(text)
        if not m:
            continue
        for raw_term, raw_def in KT_ITEM_RE.findall(m.group(1)):
            term = " ".join(raw_term.split())
            definition = " ".join(raw_def.split())
            key = fold(term)
            if not key or key in seen:
                continue
            if key in {"pinyin汉字", "pinyin"} or "pinyin" in term.lower() and "汉字" in term:
                continue
            seen.add(key)
            found.append((term, definition))
    return found


def normalize_term_display(raw: str, tradition: str) -> str:
    t = " ".join(raw.split())
    # Chinese: prefer "pinyin (chars)"
    m = re.search(r"([\u4e00-\u9fff]{1,6})", t)
    chars = m.group(1) if m else ""
    # extract pinyin-ish token
    py = re.search(
        r"([A-Za-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜüĀÁǍÀĒÉĚÈĪÍǏÌŌÓǑÒŪÚǓÙÜ]+(?:\s+[A-Za-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]+)?)",
        t,
    )
    pinyin = py.group(1).strip() if py else ""
    if tradition == "chinese" and chars:
        if pinyin:
            return f"{pinyin} ({chars})"
        # chars-first forms like 道 (dào)
        return f"{chars}"
    # Sanskrit: keep if already has Devanagari
    return t


def lookup_spec(term: str, index: dict[str, TermSpec], tradition: str) -> TermSpec | None:
    f = fold(term)
    if f in index:
        return index[f]
    # Exact character-compound hits (Chinese)
    chars = re.findall(r"[\u4e00-\u9fff]+", term)
    for ch in chars:
        if fold(ch) in index:
            return index[fold(ch)]
    # Exact latin token hits only (avoid anuśāsana → āsana)
    for tok in re.findall(r"[A-Za-zāīūṛṝḷṅñṭḍṇśṣḥṃĀĪŪṚ]+", term):
        ft = fold(tok)
        if tradition == "chinese" and ft in TTC_BLOCK:
            continue
        if ft in index:
            return index[ft]
    return None


def clean_here_fragment(text: str, title: str) -> str:
    t = " ".join((text or "").split())
    t = re.sub(r"^(etymology|root|from|literally|originally)\s*[:：\-]?\s*", "", t, flags=re.I)
    # drop leading "term (script) —" echoes
    t = re.sub(r"^[A-Za-zāīūṛṅñṭḍṇśṣḥṃ\u4e00-\u9fff\s]+\([^)]+\)\s*[—\-–:]?\s*", "", t)
    t = re.sub(r"\bdefault translation\b.*$", "", t, flags=re.I)
    t = re.sub(r"\btranslation stakes\b.*$", "", t, flags=re.I)
    t = re.sub(r"\bLegge\b.*$", "", t, flags=re.I)
    t = t.strip(" ;,.-")
    if len(t) > 220:
        t = t[:217].rstrip() + "…"
    if not t:
        t = f"load-bearing in “{title}”"
    return t


def _meaning_from_buried(buried: str) -> str:
    """Pull the tradition/here clause out of a buried glossary line."""
    if not buried:
        return ""
    chunks = re.split(r"[;—–]\s*", buried)
    meaningful: list[str] = []
    for chunk in chunks:
        c = chunk.strip().strip('"“”')
        if not c:
            continue
        low = c.lower()
        if low.startswith(
            (
                "etymology",
                "root",
                "from ",
                "literally",
                "originally",
                "by extension",
                "default translation",
                "translation stakes",
                "translation:",
                "often translated",
                "common translation",
                "pratibhā",
                "pratibha",
                "legge",
            )
        ):
            continue
        if "pratibhā" in low or "pratibha" in low or "legge" in low:
            continue
        if any(
            noise in low
            for noise in (
                "brahman",
                "advait",
                "madhyamaka",
                "śūnyatā",
                "sunyata",
                "compare sanskrit",
                "closest indic",
            )
        ):
            continue
        if low in {'"the way"', "the way", '"tao"', "tao"}:
            continue
        c = re.sub(
            r"^(?:tradition|sāṃkhya(?: tradition)?|sankhya|yoga|taoist sense|contextual meaning|in Lǎozǐ|in Laozi)\s*[:：]\s*",
            "",
            c,
            flags=re.I,
        )
        c = re.sub(r"^translation\s*[:：]\s*", "", c, flags=re.I)
        if len(c) < 8:
            continue
        meaningful.append(c)
    if not meaningful:
        return clean_here_fragment(buried, "")
    # Prefer the most informative chunk (length + contextual cues)
    def score(c: str) -> tuple[int, int]:
        low = c.lower()
        bonus = 0
        for cue in ("here", "this", "sūtra", "sutra", "chapter", "passage", "argument", "claim"):
            if cue in low:
                bonus += 20
        return (bonus, len(c))

    best = max(meaningful, key=score)
    return clean_here_fragment(best, "")


def compact_here(unit: dict[str, Any], term: str, buried_def: str, spec: TermSpec | None) -> str:
    title = str(unit.get("title") or unit.get("unit_label") or unit.get("unit_id") or "this unit")
    buried_here = _meaning_from_buried(" ".join((buried_def or "").split()))

    if buried_here and len(buried_here) >= 24:
        here = buried_here
    else:
        translation = " ".join(
            (
                layer_body(unit, "translation")
                or str(unit.get("translation") or unit.get("translation_literal") or "")
            ).split()
        )
        hook = ""
        if translation:
            hook = re.split(r"(?<=[.!?。])\s+", translation)[0]
            hook = re.sub(r"^\d+\s*[.)]?\s*", "", hook).strip()
            if len(hook) < 12:
                hook = ""
            if len(hook) > 120:
                hook = hook[:117] + "…"
        here = buried_here or hook or "does philosophical work in this passage"
        if hook and buried_here and fold(hook[:40]) not in fold(buried_here):
            here = f"{buried_here}; stakes the argument of: {hook}"

    if title.lower() not in here.lower():
        here = f"in “{title}”: {here}"
    if len(here) > 260:
        here = here[:257].rstrip() + "…"
    return here


def make_definition(unit: dict[str, Any], term: str, buried_def: str, spec: TermSpec | None) -> str:
    if spec:
        etym = spec["etym"]
        trap = spec["trap"]
    else:
        # Derive weak etym/trap from buried text
        buried = " ".join((buried_def or "").split())
        etym_m = re.search(
            r"(?:etymology|root|from|literally|originally)\s*[:：]?\s*([^;—–]+)",
            buried,
            re.I,
        )
        etym = etym_m.group(1).strip() if etym_m else f"source-term {term.split('(')[0].strip()}"
        trap_m = re.search(
            r"(?:default translation|translation stakes|often translated|common translations?)\s*[:：]?\s*(.+)$",
            buried,
            re.I,
        )
        trap = (
            trap_m.group(1).strip(" ;.")
            if trap_m
            else "default English flattens the technical work this term does here"
        )
        if len(trap) > 160:
            trap = trap[:157] + "…"
    here = compact_here(unit, term, buried_def, spec)
    return f"{etym} -> {here} -> {trap}"


CORE_YS = {
    "yoga",
    "citta",
    "vrtti",
    "nirodha",
    "samadhi",
    "purusa",
    "prakrti",
    "klesa",
    "kaivalya",
    "samyama",
    "abhyasa",
    "vairagya",
}
CORE_TTC = {"dao", "de", "wuwei", "ziran", "xuan", "pu", "rou", "wu", "you", "ming", "chang"}


def _spec_core_rank(spec: TermSpec, tradition: str) -> int:
    keys = {fold(k) for k in (spec.get("keys") or [])}
    # Also treat display-term folds
    keys.add(fold(spec.get("term") or ""))
    chars = "".join(re.findall(r"[\u4e00-\u9fff]+", spec.get("term") or ""))
    if chars:
        keys.add(fold(chars))
    core = CORE_TTC if tradition == "chinese" else CORE_YS
    # Chinese cores keyed by char folds too
    if tradition == "chinese":
        char_core = {"道", "德", "無為", "自然", "玄", "朴", "樸", "柔", "無", "有", "名", "常"}
        if any(c in (spec.get("term") or "") for c in char_core):
            return 0
    return 0 if keys & core else 1


def match_terms_in_text(text: str, index: dict[str, TermSpec], tradition: str) -> list[TermSpec]:
    found: list[TermSpec] = []
    seen: set[int] = set()
    specs = []
    seen_spec = set()
    for spec in index.values():
        if id(spec) in seen_spec:
            continue
        seen_spec.add(id(spec))
        specs.append(spec)
    specs.sort(
        key=lambda s: (
            _spec_core_rank(s, tradition),
            -max((len(fold(k)) for k in (s.get("keys") or ["a"])), default=0),
        )
    )

    folded_text = fold(text)
    matched_keys: list[str] = []

    for spec in specs:
        sid = id(spec)
        if sid in seen:
            continue
        hit = False
        hit_key = ""
        display_chars = re.findall(r"[\u4e00-\u9fff]+", spec["term"])
        if tradition == "chinese" and display_chars:
            for ch in sorted(display_chars, key=len, reverse=True):
                if ch in text:
                    hit = True
                    hit_key = ch
                    break
        else:
            for key in sorted(spec.get("keys") or [], key=lambda k: len(fold(k)), reverse=True):
                fk = fold(key)
                if len(fk) < 3:
                    continue
                if fk in folded_text:
                    if any(fk != mk and fk in mk for mk in matched_keys):
                        continue
                    hit = True
                    hit_key = fk
                    break
        if hit:
            if hit_key and any(hit_key != mk and hit_key in mk for mk in matched_keys):
                continue
            seen.add(sid)
            found.append(spec)
            if hit_key:
                matched_keys.append(hit_key)
    return found


def select_items(unit: dict[str, Any], work_id: str) -> list[dict[str, Any]]:
    tradition = "sanskrit" if work_id == "patañjali_yoga_sūtras" else "chinese"
    index = YS_INDEX if tradition == "sanskrit" else TTC_INDEX

    buried = buried_key_terms(unit)
    items: list[dict[str, Any]] = []
    used_specs: set[int] = set()
    used_terms: set[str] = set()

    def add(term_display: str, buried_def: str, spec: TermSpec | None) -> None:
        nonlocal items
        if len(items) >= 5:
            return
        if tradition == "chinese":
            f = fold(term_display)
            if any(b in f for b in TTC_BLOCK):
                return
            # require Chinese characters when possible
            if not re.search(r"[\u4e00-\u9fff]", term_display) and not (
                spec and re.search(r"[\u4e00-\u9fff]", spec["term"])
            ):
                # allow only if spec provides chars
                if not spec:
                    return
        if spec:
            if id(spec) in used_specs:
                return
            used_specs.add(id(spec))
            term_display = spec["term"]
        else:
            term_display = normalize_term_display(term_display, tradition)
            if fold(term_display) in used_terms:
                return
        if fold(term_display) in used_terms:
            return
        used_terms.add(fold(term_display))
        row: dict[str, Any] = {
            "term": term_display,
            "definition": make_definition(unit, term_display, buried_def, spec),
        }
        if spec and spec.get("lemma_id"):
            row["lemma_id"] = spec["lemma_id"]
        if spec and spec.get("sense_id"):
            row["sense_id"] = spec["sense_id"]
        items.append(row)

    primary = "\n".join(
        [
            str(unit.get("sanskrit_iast") or ""),
            str(unit.get("sanskrit_devanagari") or ""),
            layer_body(unit, "original"),
            layer_body(unit, "iast"),
            layer_body(unit, "translation"),
            str(unit.get("translation") or ""),
            str(unit.get("title") or ""),
        ]
    )
    primary_specs = match_terms_in_text(primary, index, tradition)

    # 1) Primary-text load-bearing terms first (with buried defs when available)
    buried_by_spec: dict[int, str] = {}
    buried_unmatched: list[tuple[str, str]] = []
    for raw_term, raw_def in buried:
        spec = lookup_spec(raw_term, index, tradition)
        if spec:
            buried_by_spec[id(spec)] = raw_def
        else:
            buried_unmatched.append((raw_term, raw_def))

    for spec in primary_specs:
        add(spec["term"], buried_by_spec.get(id(spec), ""), spec)
        if len(items) >= 5:
            break

    # 2) Remaining buried Key Terms (unit-authored, even if not in primary line)
    if len(items) < 5:
        for raw_term, raw_def in buried:
            spec = lookup_spec(raw_term, index, tradition)
            if tradition == "chinese" and not spec:
                if not re.search(r"[\u4e00-\u9fff]", raw_term):
                    continue
            add(raw_term, raw_def, spec)
            if len(items) >= 5:
                break

    # 3) Still short: scan commentary for bank terms (YS/TTC only)
    if len(items) < 2:
        commentary = layer_body(unit, "commentary") + "\n" + str(unit.get("commentary") or "")
        for spec in match_terms_in_text(commentary, index, tradition):
            add(spec["term"], "", spec)
            if len(items) >= 4:
                break

    # Clamp to 2–5; if only 1, try harder with core defaults
    if len(items) < 2:
        defaults = (
            ["yoga", "citta", "vrtti", "samadhi"]
            if tradition == "sanskrit"
            else ["dao", "de", "wuwei", "ziran"]
        )
        for key in defaults:
            spec = index.get(fold(key))
            if spec:
                add(spec["term"], "", spec)
            if len(items) >= 2:
                break

    return items[:5]


def set_key_terms_layer(unit: dict[str, Any], layer: dict[str, Any]) -> None:
    layers = unit.get("pratibha_layers")
    if not isinstance(layers, list):
        unit["pratibha_layers"] = [copy.deepcopy(layer)]
        return
    for i, row in enumerate(layers):
        if isinstance(row, dict) and row.get("kind") == "key_terms":
            # Preserve non-key_terms fields? No — replace whole KT layer only
            layers[i] = copy.deepcopy(layer)
            return
    # insert before resonances/practice/appendix
    after = {"resonances", "practice", "appendix"}
    insertion = next(
        (
            i
            for i, row in enumerate(layers)
            if isinstance(row, dict) and row.get("kind") in after
        ),
        len(layers),
    )
    layers.insert(insertion, copy.deepcopy(layer))


def load_yaml_units(work_id: str) -> list[tuple[Path, dict[str, Any]]]:
    directory = WORKS[work_id]
    out: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(directory.glob("*.yml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            out.append((path, data))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--work", action="append", default=[], help="work_id filter; repeatable")
    parser.add_argument("--max-units", type=int, default=0)
    args = parser.parse_args()

    work_filter = set(args.work) if args.work else set(WORKS)
    yaml_changes: dict[str, dict[str, Any]] = {}  # unit_id -> layer
    stats = {w: {"units": 0, "items": 0, "enriched": 0} for w in WORKS}

    for work_id in WORKS:
        if work_id not in work_filter:
            continue
        for path, doc in load_yaml_units(work_id):
            items = select_items(doc, work_id)
            if len(items) < 2:
                print(f"WARN <2 terms: {path.name} ({len(items)})")
            layer = {
                "kind": "key_terms",
                "label": "Key Terms",
                "items": items,
                "layer_provenance": "editorial-enriched",
            }
            uid = str(doc.get("unit_id") or "")
            stats[work_id]["units"] += 1
            stats[work_id]["items"] += len(items)
            stats[work_id]["enriched"] += 1
            yaml_changes[uid] = layer

            if args.write:
                set_key_terms_layer(doc, layer)
                atomic_write(path, dump_yaml(doc))

            if args.max_units and sum(s["units"] for s in stats.values()) >= args.max_units:
                break
        if args.max_units and sum(s["units"] for s in stats.values()) >= args.max_units:
            break

    # Sync index.jsonl
    index_updated = 0
    if args.write:
        lines = INDEX.read_text(encoding="utf-8").splitlines()
        new_lines: list[str] = []
        for line in lines:
            if not line.strip():
                new_lines.append(line)
                continue
            unit = json.loads(line)
            uid = str(unit.get("unit_id") or "")
            if uid in yaml_changes:
                set_key_terms_layer(unit, yaml_changes[uid])
                index_updated += 1
            new_lines.append(json.dumps(unit, ensure_ascii=False))
        atomic_write(INDEX, "\n".join(new_lines) + "\n")

    print("Enrichment summary:")
    for work_id, s in stats.items():
        if s["units"]:
            avg = s["items"] / s["units"]
            print(
                f"  {work_id}: units={s['units']} enriched={s['enriched']} "
                f"items={s['items']} avg_items={avg:.2f}"
            )
    if args.write:
        print(f"wrote YAML companions and updated {index_updated} index.jsonl rows")
    else:
        print("dry-run only; re-run with --write to apply")
        # show 2 examples
        for work_id in work_filter:
            for path, doc in load_yaml_units(work_id)[:1]:
                items = select_items(doc, work_id)
                print(f"\nEXAMPLE {doc.get('unit_id')}:")
                for it in items:
                    print(f"  - {it['term']}: {it['definition'][:200]}")


if __name__ == "__main__":
    main()

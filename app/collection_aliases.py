import re
from typing import Iterable


def slugify(value: str) -> str:
    return re.sub(r"[\s\W]+", "_", (value or "").strip().lower()).strip("_")


# Canonical registry for all corpus collections and historical aliases.
COLLECTION_ALIASES: dict[str, set[str]] = {
    "siva_sutra": {"siva_sutra", "shiva_sutra", "siva_sutras", "śiva_sūtra"},
    "vijnana_bhairava": {
        "vijnana_bhairava",
        "vijnana_bhairava_yuktis",
        "vijnana_bhairava_final",
        "vbt_translation_wallis_2",
        "vijñāna_bhairava",
    },
    "tao_te_ching": {"tao_te_ching", "dao_de_jing"},
    "bhagavad_gita": {"bhagavad_gita", "bhagavad_gītā"},
    "the_book_of_chuang_tzu": {"the_book_of_chuang_tzu", "chuang_tzu", "zhuangzi"},
    "yoga_spandakarika": {
        "yoga_spandakarika",
        "yoga_spandakarika_the_sacred_texts_at_the_origins_of",
    },
    "heraclitus_fragments": {"heraclitus_fragments", "fragments"},
    "know_yourself_ibn_arabi_balyani": {
        "know_yourself_ibn_arabi_balyani",
        "know_yourself_ibn_arabi",
        "know_yourself_an_explanation_of_the_oneness_of_being",
    },
    "epictetus_works": {"epictetus_works"},
    "phaedo_plato": {"phaedo_plato", "phaedo"},
    "plotinus_enneads": {
        "plotinus_enneads",
        "plotinus",
        "enneads",
        "the_enneads_of_plotinus",
        "the_six_enneads",
    },
    "rumi_mathnawi": {
        "rumi_mathnawi",
        "rūmī_mathnawī_yi_maʿnawī",
        "mathnawi",
        "mathnawī",
        "rumi",
    },
    "dogen_shobogenzo": {
        "dogen_shobogenzo",
        "dōgen_shōbōgenzō",
        "shobogenzo",
        "shōbōgenzō",
        "dogen",
        "genjokoan",
        "genjōkōan",
        "fukanzazengi",
        "bendowa",
        "bendōwa",
    },
    "meister_eckhart": {
        "meister_eckhart",
        "meister_eckhart_von_abegescheidenheit",
        "meister_eckhart_von_armûot_des_geistes",
        "von_abegescheidenheit",
        "von_armûot_des_geistes",
        "eckhart",
    },
    "pseudo_dionysius": {
        "pseudo_dionysius",
        "pseudo_dionysius_mystical_theology",
        "dionysius",
        "dionysius_the_areopagite",
        "pseudo_dionysius_the_areopagite",
        "mystical_theology",
        "divine_names",
        "areopagite",
    },
    "dhammapada": {
        "dhammapada",
        "dhammapāda",
        "dhp",
    },
    "katha_upanishad": {
        "katha_upanishad",
        "kaṭha_upaniṣad",
        "katha",
        "kaṭha",
        "kathopanishad",
    },
    "brihadaranyaka_upanishad": {
        "brihadaranyaka_upanishad",
        "bṛhadāraṇyaka_upaniṣad",
        "brihadaranyaka",
        "bṛhadāraṇyaka",
        "brihad",
    },
    "mundaka_upanishad": {
        "mundaka_upanishad",
        "muṇḍaka_upaniṣad",
        "mundaka",
        "muṇḍaka",
    },
    "marcus_aurelius_meditations": {
        "marcus_aurelius_meditations",
        "marcus_aurelius",
        "meditations",
        "marcus",
    },
    "the_cloud_of_unknowing": {
        "the_cloud_of_unknowing",
        "cloud_of_unknowing",
    },
    "parmenides_fragments": {
        "parmenides_fragments",
        "parmenides",
        "on_nature",
    },
    "milarepa_songs": {
        "milarepa_songs",
        "milarepa",
        "jetsun_kahbum",
        "jetsün_kahbum",
        "tibet_great_yogi_milarepa",
    },
    "chandogya_upanishad": {
        "chandogya_upanishad",
        "chandogya",
        "chāndogya_upaniṣad",
        "khândogya_upanishad",
        "khandogya",
    },
    "pratyabhijnahrdayam": {
        "pratyabhijnahrdayam",
        "pratyabhijna_hrdayam",
        "pratyabhijñāhṛdayam",
    },
    "astavakra_gita": {
        "astavakra_gita",
        "aṣṭāvakra_gītā",
        "ashtavakra_gita",
    },
    "mandukya_upanishad_karika": {
        "mandukya_upanishad_karika",
        "mandukya_upanishad_and_gaudapada_karika",
        "māṇḍūkya_upaniṣad",
        "gaudapada_karika",
    },
    "svetasvatara_upanishad": {
        "svetasvatara_upanishad",
        "svetasvatara_upanisad",
        "śvetāśvatara_upaniṣad",
        "svetasvatara",
    },
    "isavasya_upanishad": {
        "isavasya_upanishad",
        "isha_upanishad",
        "isa_upanishad",
        "isavasya_upanisad",
        "īśāvāsya_upaniṣad",
    },
    "yoginihrdaya": {
        "yoginihrdaya",
        "yoginihrdayam",
        "yogini_hrdaya",
        "yoginī_hṛdaya",
        "yoginīhṛdaya",
        "the_heart_of_the_yogini",
    },
    "tantrasara": {
        "tantrasara",
        "tantrasāra",
        "tantra_sara",
        "abhinavagupta_tantrasara",
    },
    "patanjali_yoga_sutras": {
        "patanjali_yoga_sutras",
        "patañjali_yoga_sūtras",
        "patanjali",
        "yoga_sutras",
        "yoga_sūtras",
        "raja_yoga",
    },
    "heart_sutra": {
        "heart_sutra",
        "heart_sūtra",
        "prajnaparamitahrdaya",
        "prajñāpāramitāhṛdaya",
        "prajnaparamita_hrdaya",
        "hridaya_sutra",
    },
    "nagarjuna_mulamadhyamakakarika": {
        "nagarjuna_mulamadhyamakakarika",
        "nāgārjuna_mūlamadhyamakakārikā",
        "mulamadhyamakakarika",
        "mūlamadhyamakakārikā",
        "mmk",
        "nagarjuna",
        "nāgārjuna",
    },
    "shantideva_bodhicaryavatara": {
        "shantideva_bodhicaryavatara",
        "śāntideva_bodhicaryāvatāra",
        "bodhicaryavatara",
        "bodhicaryāvatāra",
        "bodhicharyavatara",
        "bca",
        "shantideva",
        "śāntideva",
    },
    "tilopa_mahamudra": {
        "tilopa_mahamudra",
        "tilopa_mahāmudrā",
        "tilopa",
        "mahamudra_upadesa",
        "mahāmudrā_upadeśa",
        "ganges_mahamudra",
        "ganges_mahāmudrā",
    },
}


_ALIAS_TO_CANONICAL: dict[str, str] = {}
for _canonical, _alias_set in COLLECTION_ALIASES.items():
    for _name in {_canonical, *_alias_set}:
        _ALIAS_TO_CANONICAL[slugify(_name)] = _canonical


def canonical_slug(value: str, source_file: str = "") -> str:
    """Map any collection label/alias to its canonical registry slug.

    Falls back to the directory name in the source path, then to a plain slug,
    so ingestion and enrichment store one consistent collection identifier.
    """
    s = slugify(value)
    if s in _ALIAS_TO_CANONICAL:
        return _ALIAS_TO_CANONICAL[s]
    m = re.search(r"data/(?:yaml|canonical)/([^/]+)/", (source_file or "").lower())
    if m:
        s2 = slugify(m.group(1))
        return _ALIAS_TO_CANONICAL.get(s2, s2)
    return s


def aliases_for_selection(selection: str) -> set[str]:
    s = slugify(selection)
    if not s:
        return set()
    for canonical, aliases in COLLECTION_ALIASES.items():
        normalized = {slugify(canonical), *(slugify(a) for a in aliases)}
        if s in normalized:
            return normalized
    # Keep graceful fallback for free-form user selections.
    return {s}


def meta_collection_slug(metadata: dict) -> str:
    """Canonical collection slug for diversity caps / compare filters.

    Display labels like ``Chāndogya Upaniṣad`` and folder slugs like
    ``chandogya_upanishad`` must collapse to one key, or per-collection
    caps count them as different traditions.
    """
    coll = str((metadata or {}).get("collection", "") or "")
    source_file = str((metadata or {}).get("source_file", "") or "")
    if coll or source_file:
        return canonical_slug(coll, source_file)
    return ""


def belongs_to_selection(metadata: dict, selection: str) -> bool:
    aliases = aliases_for_selection(selection)
    coll = meta_collection_slug(metadata)
    if coll in aliases:
        return True
    source_file = str((metadata or {}).get("source_file", "")).lower()
    return any(f"/{a}/" in source_file for a in aliases)


def validate_registered_collections(collection_names: Iterable[str]) -> list[str]:
    known = {slugify(c) for c in COLLECTION_ALIASES.keys()}
    for aliases in COLLECTION_ALIASES.values():
        known.update(slugify(a) for a in aliases)
    missing: list[str] = []
    for name in collection_names:
        s = slugify(name)
        if s and s not in known:
            missing.append(name)
    return sorted(set(missing))

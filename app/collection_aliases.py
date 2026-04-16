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
}


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
    coll = slugify(str((metadata or {}).get("collection", "")))
    if coll:
        return coll
    source_file = str((metadata or {}).get("source_file", "")).lower()
    m = re.search(r"data/(?:yaml|canonical)/([^/]+)/", source_file)
    if m:
        return slugify(m.group(1))
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

"""ElevenLabs listen path — English layers only, voice room per tradition.

Speech is archived in object storage so a later subscription cancel keeps
what we already generated. Dakota uses a real Dakota/Lakota/Nakota speaker
only when one is pinned or present in the workspace — never a costume
"Native American" accent. Christian stays unmarked English.
Original / IAST are never spoken.
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import time
from dataclasses import dataclass
from typing import Any, Literal
from pathlib import Path

import httpx

from . import listen_store
from .config import settings

logger = logging.getLogger("pratibha.tts")

_DEFAULT_VOICE = "nPczCjzI2devNBz1zQrb"  # Brian — unmarked American only
# Pins live here (not only .env) so a reload picks them up. Env still wins.
_ROOM_DEFAULT_VOICES: dict[str, str] = {
    "indic": "aoVMYhTrJqXZPDJhHqkj",  # Anagh — Indian English
    "yoruba": "ytMkkl3KqcF3nhlFgtys",
    "sinosphere": "mBoVD3461U2BagYEwjeo",
    "sufi": "PleK417YVMP2SUWm8Btb",
    "hellenic": "1gkXJMvrzBWAwt0XqBaa",
}
_MODEL = "eleven_multilingual_v2"
_MAX_CHARS = 4200
_ELEVEN_TTS = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
_ELEVEN_VOICES = "https://api.elevenlabs.io/v1/voices"
_ELEVEN_SHARED = "https://api.elevenlabs.io/v1/shared-voices"
_ELEVEN_SFX = "https://api.elevenlabs.io/v1/sound-generation"

_MD_RE = re.compile(r"[*_`#>\[\]()]+")
_WS_RE = re.compile(r"\s+")
# Chapter-file headers sometimes leaked into the last unit's practice layer.
_EDITORIAL_TAIL_RE = re.compile(
    r"(?is)(?:\n\s*)+(?:\*{0,2}\s*)?(?:corpus entry|sanskrit basis|english layers)\b.*$"
)
_BRIEF_META_TAIL_RE = re.compile(
    r"(?is)(?:\n\s*)+(?:one unit per brief chunk\b|(?:\*{0,2}\s*)?(?:units:\s*\d|chapter:\s*\d|sanskrit:\s*devanagari)).*$"
)
_COSTUME_NATIVE_RE = re.compile(
    r"native american|indigenous accent|tribal|indian accent|first nations",
    re.I,
)
_DAKOTA_SELF_RE = re.compile(r"\b(dakota|lakota|nakota|oceti\s*sakowin)\b", re.I)

ListenSection = Literal["translation", "commentary", "practice", "all"]
SPEAKABLE_SECTIONS: tuple[ListenSection, ...] = ("translation", "commentary", "practice")
VoiceRoom = str

_ROOM_ACCENTS: dict[str, tuple[str, ...]] = {
    "indic": ("indian", "indian english", "south asian", "hindi"),
    "sinosphere": ("chinese", "mandarin", "cantonese", "singaporean", "taiwanese"),
    "yoruba": ("nigerian", "african", "west african", "yoruba"),
    "hebrew": ("israeli", "hebrew", "jewish"),
    "hellenic": ("greek",),
    "sufi": ("persian", "iranian", "arabic", "egyptian", "levantine"),
    "dakota": ("dakota", "lakota", "nakota"),
    "unmarked": (),
}

# Collection / work_id → room. Order matters; first match wins.
_ROOM_PATTERNS: list[tuple[re.Pattern[str], VoiceRoom]] = [
    (re.compile(r"yoruba|johnson", re.I), "yoruba"),
    (re.compile(r"eastman|zitkala|soul of the indian|old indian legends|dakota", re.I), "dakota"),
    (re.compile(r"ecclesiastes|qoheleth|psalm|tehillim|zohar|yetzirah|kabbalah", re.I), "hebrew"),
    (re.compile(r"rumi|rūmī|ibn.?arabi|balyani|mathnaw|attar|mantiq|conference.?of.?the.?birds|hujwir|kashf", re.I), "sufi"),
    (
        re.compile(
            r"tao|dao.?de|zhuang|chuang|analect|confucius|lunyu|zhongyong|"
            r"dogen|dōgen|shobogenzo|heart.?s[uū]tra|prajnaparamita|"
            r"diamond.?s[uū]tra|vajracchedik",
            re.I,
        ),
        "sinosphere",
    ),
    (
        re.compile(
            r"heraclitus|epictetus|enchiridion|phaedo|plato|plotinus|ennead|"
            r"marcus|meditations|parmenides",
            re.I,
        ),
        "hellenic",
    ),
    (
        re.compile(
            r"eckhart|dionysius|areopagite|cloud.?of.?unknowing|"
            r"gospel.?of.?thomas|gospel.?of.?mary|logia of jesus|"
            r"new.?testament.?logia|course in miracles|acim",
            re.I,
        ),
        "unmarked",
    ),
    (
        re.compile(
            r"dhammapada|nagarjuna|madhyamaka|shantideva|bodhicary|"
            r"milarepa|tilopa|patanjali|yoga.?s[uū]tra|hatha.?yoga|siva.?samhita|"
            r"vijnana.?bhairava|spanda|siva.?s[uū]tra|pratyabhij|tantras|"
            r"yogin[iī]|upanishad|gita|astavakra|mandukya|gaudapada|"
            r"katha|chandogya|mundaka|brihad|isavasya|svetasvatara|"
            r"lalla|lal.?ded|lalleshwari|vakyani|vākyāni",
            re.I,
        ),
        "indic",
    ),
]

# Room tone, not costume. Dakota is land and air — never flute or drum.
_CUE_PROMPTS: dict[str, dict[str, str]] = {
    "indic": {
        "open": "A single soft bronze singing bowl struck once in a quiet stone shrine. Long clean decay. No hiss, no static, no noise floor, no melody, no voice, no chant.",
        "close": "The last faint overtone of a bronze bowl fading into a still stone room. Clean silence. No hiss, no voice.",
    },
    "sinosphere": {
        "open": "A single soft wooden fish tap in an empty monastery hall. One hit, then silence. Clean recording. No hiss, no flute, no voice.",
        "close": "Quiet wooden hall after one tap, air settling. Clean silence. No hiss, no instrument continues.",
    },
    "yoruba": {
        "open": "One warm low calabash tone in still night air. A single note, then silence. Clean recording. No hiss, not a drum solo, not festive.",
        "close": "Warm night air after one low tone has died. Clean silence. No hiss, no percussion, no voice.",
    },
    "hebrew": {
        "open": "A single quiet bronze overtone in a dry stone room. Desert stillness. Clean recording. No hiss, no shofar, no chant, no voice.",
        "close": "Dry stone room after one metallic tone fades. Clean silence. No hiss.",
    },
    "hellenic": {
        "open": "One quiet plucked gut string in a marble room. A single note, then stone silence. Clean recording. No hiss, no melody.",
        "close": "Marble room after one string has gone still. Clean silence. No hiss.",
    },
    "sufi": {
        "open": "One soft reed breath, a single note fading on a carpeted floor. Clean recording. No hiss, no ornament, no voice.",
        "close": "A reed tone disappearing into a quiet carpeted room. Clean silence. No hiss.",
    },
    "dakota": {
        "open": "Wind moving through dry prairie grass under an open sky. A few seconds. Soft and clean. No hiss crackle, no flute, no drum, no voice, no melody, no stereotyped Native American music. Only land and air.",
        "close": "Prairie wind falling still. Only air. Clean fade. No instrument, no voice.",
    },
    "unmarked": {
        "open": "A single page turning in a quiet wooden library. Paper and wood. Clean recording. No hiss, no organ, no church bell, no voice.",
        "close": "A book closing softly on a wooden table. Then clean silence. No hiss.",
    },
}

_account_voices: list[dict[str, Any]] | None = None
_account_voices_at = 0.0


@dataclass(frozen=True)
class ListenScript:
    room: VoiceRoom
    voice_id: str
    text: str
    title: str
    section: ListenSection


def configured() -> bool:
    return bool((settings.ELEVENLABS_API_KEY or os.getenv("ELEVENLABS_API_KEY") or "").strip())


def _api_key() -> str:
    return (settings.ELEVENLABS_API_KEY or os.getenv("ELEVENLABS_API_KEY") or "").strip()


def _strip_editorial(text: str) -> str:
    """Drop ingest metadata that must never be spoken."""
    cleaned = _EDITORIAL_TAIL_RE.sub("", text)
    cleaned = _BRIEF_META_TAIL_RE.sub("", cleaned)
    return cleaned.strip()


def _strip_md(text: str) -> str:
    cleaned = _MD_RE.sub("", text.replace("**", "").replace("__", ""))
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    return _WS_RE.sub(" ", cleaned).strip()


def _layer(verse: dict[str, Any], kind: str) -> str:
    layers = verse.get("pratibha_layers")
    if isinstance(layers, list):
        for layer in layers:
            if not isinstance(layer, dict):
                continue
            if str(layer.get("kind") or "").lower() != kind:
                continue
            body = str(layer.get("body") or "")
            if kind == "practice":
                body = _strip_editorial(body)
            body = _strip_md(body)
            if body:
                return body
    fallback = {
        "translation": verse.get("translation"),
        "commentary": verse.get("commentary"),
        "practice": verse.get("practice") or verse.get("abhyasa"),
    }.get(kind)
    raw = str(fallback or "")
    if kind == "practice":
        raw = _strip_editorial(raw)
    return _strip_md(raw)


def _haystack(verse: dict[str, Any]) -> str:
    return " ".join(
        str(verse.get(key) or "")
        for key in ("collection", "work_id", "_id", "sutra_id")
    )


def voice_room_for(verse: dict[str, Any]) -> VoiceRoom:
    hay = _haystack(verse)
    for pattern, room in _ROOM_PATTERNS:
        if pattern.search(hay):
            return room
    return "unmarked"


# Really-large collections offer Listen only for curated key verses (scripts/
# earmark_tts_key.py sets `tts_key: true`). Bhagavad Gītā is intentionally NOT here —
# every one of its verses is listenable.
_TTS_GATED_COLLECTIONS = frozenset(
    {"siva_samhita", "marcus_aurelius_meditations", "hatha_yoga_pradipika"}
)


def _tts_gated(verse: dict[str, Any]) -> bool:
    """True if this verse is in a gated large collection but is not a key verse."""
    slug = str(verse.get("work_id") or "").strip().lower()
    if not slug:
        uid = str(verse.get("unit_id") or "")
        slug = uid.split(".", 1)[0].strip().lower()
    return slug in _TTS_GATED_COLLECTIONS and not verse.get("tts_key")


def available_sections(verse: dict[str, Any]) -> list[ListenSection]:
    if _tts_gated(verse):
        return []
    return [kind for kind in SPEAKABLE_SECTIONS if _layer(verse, kind)]


async def archived_cue(room: VoiceRoom, edge: str) -> bytes | None:
    """Return a baked room cue, or None — never generate on demand."""
    if edge not in {"open", "close"}:
        return None
    safe_room = room if room in _CUE_PROMPTS else "unmarked"
    return await listen_store.get_object(_cue_key(safe_room, edge))


async def archived_audio(
    verse: dict[str, Any],
    section: ListenSection,
    voice_id: str | None = None,
) -> tuple[bytes, ListenScript] | None:
    """Return ElevenLabs audio already in the archive. Never call the API."""
    if section not in {"translation", "commentary", "practice", "all"}:
        return None
    room = voice_room_for(verse)
    title = str(verse.get("title") or "")
    vid = str(verse.get("_id") or "")
    text = build_script(verse, section)
    cached = await listen_store.get_object(verse_speech_key(vid, section)) if vid else None
    if not cached and text:
        if not voice_id:
            pinned = _env_voice(room) or _ROOM_DEFAULT_VOICES.get(room) or _unmarked_voice()
            voice_id = pinned
        cached = await listen_store.get_object(_speech_key(voice_id, text))
    if not cached:
        return None
    return cached, ListenScript(room, voice_id or "", text, title, section)


def archived_sections(verse: dict[str, Any]) -> list[ListenSection]:
    """Sections that already have ElevenLabs speech in the archive."""
    vid = str(verse.get("_id") or "")
    return list(listen_archive().get(vid) or ())


def _env_voice(room: VoiceRoom) -> str:
    return (
        (os.getenv(f"ELEVENLABS_VOICE_{room.upper()}") or "").strip()
        or _ROOM_DEFAULT_VOICES.get(room, "")
    )


def _voice_blob(voice: dict[str, Any]) -> str:
    labels = voice.get("labels") if isinstance(voice.get("labels"), dict) else {}
    parts = [
        str(voice.get("name") or ""),
        str(voice.get("description") or ""),
        str(labels.get("accent") or ""),
        str(labels.get("description") or ""),
        str(voice.get("accent") or ""),
    ]
    return " ".join(parts)


def _is_respectful_dakota_voice(voice: dict[str, Any]) -> bool:
    """A first name 'Dakota' is not a Dakota/Lakota/Nakota speaker."""
    labels = voice.get("labels") if isinstance(voice.get("labels"), dict) else {}
    identity = " ".join(
        [
            str(voice.get("description") or ""),
            str(voice.get("accent") or ""),
            str(labels.get("accent") or ""),
            str(labels.get("description") or ""),
        ]
    )
    if not _DAKOTA_SELF_RE.search(identity):
        return False
    if _COSTUME_NATIVE_RE.search(identity) and not _DAKOTA_SELF_RE.search(identity):
        return False
    return True


def _match_account_voice(room: VoiceRoom) -> str:
    if room == "dakota":
        for voice in _account_voices or []:
            if not _is_respectful_dakota_voice(voice):
                continue
            vid = str(voice.get("voice_id") or "").strip()
            if vid:
                return vid
        return ""
    accents = _ROOM_ACCENTS.get(room) or ()
    if not accents:
        return ""
    preferred: list[str] = []
    fallback: list[str] = []
    for voice in _account_voices or []:
        labels = voice.get("labels") if isinstance(voice.get("labels"), dict) else {}
        accent = str(labels.get("accent") or "").strip().lower()
        name = str(voice.get("name") or "").lower()
        use = str(labels.get("use case") or labels.get("use_case") or "").lower()
        if not any(token in accent or token in name for token in accents):
            continue
        vid = str(voice.get("voice_id") or "").strip()
        if not vid:
            continue
        if use in {"narration", "audiobook", "narrative", "meditation", ""}:
            preferred.append(vid)
        else:
            fallback.append(vid)
    return (preferred or fallback or [""])[0]


async def _refresh_account_voices(client: httpx.AsyncClient) -> None:
    global _account_voices, _account_voices_at
    now = time.monotonic()
    if _account_voices is not None and now - _account_voices_at < 3600:
        return
    try:
        res = await client.get(
            _ELEVEN_VOICES,
            headers={"xi-api-key": _api_key()},
            timeout=20.0,
        )
        if res.status_code >= 400:
            logger.info("ElevenLabs voices list failed: %s", res.status_code)
            _account_voices = _account_voices or []
            return
        data = res.json()
        voices = data.get("voices") if isinstance(data, dict) else None
        _account_voices = voices if isinstance(voices, list) else []
        _account_voices_at = now
    except Exception:
        logger.debug("ElevenLabs voices list error", exc_info=True)
        _account_voices = _account_voices or []


def _unmarked_voice() -> str:
    return (
        (os.getenv("ELEVENLABS_VOICE_UNMARKED") or "").strip()
        or (os.getenv("ELEVENLABS_VOICE_ID") or "").strip()
        or _DEFAULT_VOICE
    )


async def search_dakota_library(client: httpx.AsyncClient) -> list[dict[str, str]]:
    """Shared-library search. Only keep voices that name Dakota/Lakota/Nakota."""
    found: list[dict[str, str]] = []
    seen: set[str] = set()
    for query in ("dakota", "lakota", "nakota", "oceti sakowin"):
        try:
            res = await client.get(
                _ELEVEN_SHARED,
                headers={"xi-api-key": _api_key()},
                params={"page_size": 20, "search": query, "language": "en"},
                timeout=20.0,
            )
        except Exception:
            continue
        if res.status_code >= 400:
            continue
        data = res.json() if res.headers.get("content-type", "").startswith("application/json") else {}
        for voice in (data.get("voices") if isinstance(data, dict) else None) or []:
            if not isinstance(voice, dict) or not _is_respectful_dakota_voice(voice):
                continue
            vid = str(voice.get("voice_id") or "").strip()
            if not vid or vid in seen:
                continue
            seen.add(vid)
            found.append(
                {
                    "voice_id": vid,
                    "name": str(voice.get("name") or ""),
                    "accent": str(voice.get("accent") or ""),
                    "description": str(voice.get("description") or "")[:240],
                }
            )
    return found


async def resolve_voice(room: VoiceRoom, client: httpx.AsyncClient) -> str:
    pinned = _env_voice(room)
    if pinned:
        return pinned
    if room not in {"unmarked", "dakota"}:
        await _refresh_account_voices(client)
        matched = _match_account_voice(room)
        if matched:
            return matched
    if room == "dakota":
        await _refresh_account_voices(client)
        matched = _match_account_voice(room)
        if matched:
            return matched
        # Do not invent an accent. Fall through to unmarked English.
    return _unmarked_voice()


def _clip(text: str) -> str:
    if len(text) <= _MAX_CHARS:
        return text
    return text[:_MAX_CHARS].rsplit(" ", 1)[0].rstrip() + "."


def _speech_key(voice_id: str, text: str) -> str:
    digest = hashlib.sha256(f"{_MODEL}\0{voice_id}\0{text}".encode("utf-8")).hexdigest()
    return f"speech/{voice_id}/{digest}.mp3"


def verse_speech_key(verse_id: str, section: str) -> str:
    safe = str(verse_id or "").strip().replace("/", "__")
    return f"verse/{safe}/{section}.mp3"


def _cue_key(room: VoiceRoom, edge: str) -> str:
    return f"cues/v2/{room}/{edge}.mp3"


ARCHIVE_INDEX_KEY = "index/archive.json"
_ARCHIVE_TTL = 20.0
_archive_memo: dict[str, tuple[str, ...]] | None = None
_archive_at = 0.0


def _archive_path() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "listen_archive.json"


def normalize_listen_archive(raw: Any) -> dict[str, tuple[str, ...]]:
    out: dict[str, tuple[str, ...]] = {}
    if not isinstance(raw, dict):
        return out
    for vid, sections in raw.items():
        if isinstance(sections, tuple):
            kinds = [s for s in sections if s in SPEAKABLE_SECTIONS]
        elif isinstance(sections, list):
            kinds = [s for s in sections if s in SPEAKABLE_SECTIONS]
        else:
            continue
        if kinds:
            out[str(vid)] = tuple(dict.fromkeys(kinds))
    return out


def _merge_archives(*parts: dict[str, tuple[str, ...]]) -> dict[str, tuple[str, ...]]:
    acc: dict[str, list[str]] = {}
    for part in parts:
        for vid, sections in part.items():
            bucket = acc.setdefault(str(vid), [])
            for kind in sections:
                if kind in SPEAKABLE_SECTIONS and kind not in bucket:
                    bucket.append(kind)
    return {vid: tuple(kinds) for vid, kinds in acc.items() if kinds}


def bundled_listen_archive() -> dict[str, tuple[str, ...]]:
    path = _archive_path()
    if not path.is_file():
        return {}
    try:
        return normalize_listen_archive(json.loads(path.read_text()))
    except Exception:
        logger.exception("Could not read bundled Listen archive")
        return {}


def write_bundled_listen_archive(archive: dict[str, tuple[str, ...]]) -> None:
    path = _archive_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {k: list(v) for k, v in sorted(archive.items())}
        path.write_text(json.dumps(payload, indent=2) + "\n")
    except OSError:
        logger.debug("Could not write bundled Listen archive", exc_info=True)


def listen_archive() -> dict[str, tuple[str, ...]]:
    """Last known archive (bundled snapshot until a live refresh)."""
    return _archive_memo if _archive_memo is not None else bundled_listen_archive()


async def listen_archive_live(*, force: bool = False) -> dict[str, tuple[str, ...]]:
    """Bundled snapshot merged with the live storage index written by bake."""
    global _archive_memo, _archive_at
    now = time.monotonic()
    if not force and _archive_memo is not None and now - _archive_at < _ARCHIVE_TTL:
        return _archive_memo
    live: dict[str, tuple[str, ...]] = {}
    blob = await listen_store.get_object(ARCHIVE_INDEX_KEY, bypass_local=True)
    if blob:
        try:
            live = normalize_listen_archive(json.loads(blob.decode("utf-8")))
        except Exception:
            logger.exception("Could not parse live Listen archive")
    merged = _merge_archives(bundled_listen_archive(), live)
    _archive_memo = merged
    _archive_at = now
    return merged


async def publish_listen_sections(updates: dict[str, list[str]]) -> dict[str, tuple[str, ...]]:
    """Merge newly baked layers into the live index so Listen appears without a deploy."""
    global _archive_memo, _archive_at
    extra = normalize_listen_archive(updates)
    if not extra:
        return await listen_archive_live()
    current = dict(await listen_archive_live(force=True))
    merged = _merge_archives(current, extra)
    body = (json.dumps({k: list(v) for k, v in sorted(merged.items())}, indent=2) + "\n").encode("utf-8")
    ok = await listen_store.put_object(ARCHIVE_INDEX_KEY, body, content_type="application/json")
    if not ok and listen_store.configured():
        logger.warning("Live Listen archive did not upload; Listen may wait for the next deploy")
    write_bundled_listen_archive(merged)
    _archive_memo = merged
    _archive_at = time.monotonic()
    return merged


def stamp_listen_sections(verse: dict[str, Any]) -> dict[str, Any]:
    vid = str(verse.get("_id") or "")
    sections = list(listen_archive().get(vid) or ())
    if sections:
        verse["listen_sections"] = sections
    else:
        verse.pop("listen_sections", None)
    return verse


def build_script(verse: dict[str, Any], section: ListenSection = "all") -> str:
    title = _strip_md(str(verse.get("title") or verse.get("sutra_id") or ""))
    translation = _layer(verse, "translation")
    commentary = _layer(verse, "commentary")
    practice = _layer(verse, "practice")
    if section == "translation":
        parts = [p for p in (f"{title}." if title else "", translation) if p]
        return _clip("\n\n".join(parts).strip())
    if section == "commentary":
        return _clip(commentary)
    if section == "practice":
        return _clip(practice)
    parts: list[str] = []
    if title:
        parts.append(title + ".")
    if translation:
        parts.append(translation)
    if commentary:
        parts.extend(["Commentary.", commentary])
    if practice:
        parts.extend(["The practice.", practice])
    return _clip("\n\n".join(parts).strip())


async def _speak(client: httpx.AsyncClient, voice_id: str, text: str) -> bytes:
    key = _api_key()
    res = await client.post(
        _ELEVEN_TTS.format(voice_id=voice_id),
        params={"output_format": "mp3_44100_192"},
        headers={"xi-api-key": key, "Accept": "audio/mpeg"},
        json={
            "text": text,
            "model_id": (os.getenv("ELEVENLABS_MODEL") or _MODEL).strip() or _MODEL,
            "voice_settings": {
                "stability": 0.78,
                "similarity_boost": 0.68,
                "style": 0.0,
                "speed": 0.9,
                "use_speaker_boost": False,
            },
        },
        timeout=90.0,
    )
    if res.status_code >= 400:
        logger.info("ElevenLabs TTS failed: %s %s", res.status_code, res.text[:240])
        raise RuntimeError(f"ElevenLabs returned {res.status_code}")
    if not res.content:
        raise RuntimeError("ElevenLabs returned empty audio")
    return res.content


async def synthesize_cue(room: VoiceRoom, edge: str) -> bytes:
    if edge not in {"open", "close"}:
        raise ValueError("Cue edge must be open or close")
    safe_room = room if room in _CUE_PROMPTS else "unmarked"
    key = _cue_key(safe_room, edge)
    cached = await listen_store.get_object(key)
    if cached:
        return cached
    prompt = _CUE_PROMPTS[safe_room][edge]
    api_key = _api_key()
    if not api_key:
        raise RuntimeError("ElevenLabs is not configured")
    async with httpx.AsyncClient() as client:
        res = await client.post(
            _ELEVEN_SFX,
            headers={"xi-api-key": api_key, "Accept": "audio/mpeg"},
            json={
                "text": prompt,
                "duration_seconds": 2.4,
                "prompt_influence": 0.35,
            },
            timeout=60.0,
        )
        if res.status_code >= 400 or not res.content:
            logger.info("ElevenLabs SFX failed: %s %s", res.status_code, res.text[:200])
            raise RuntimeError(f"ElevenLabs cue returned {res.status_code}")
        audio = res.content
    await listen_store.put_object(key, audio)
    return audio


async def synthesize(
    verse: dict[str, Any],
    section: ListenSection = "all",
    *,
    publish: bool = True,
) -> tuple[bytes, ListenScript]:
    key = _api_key()
    if not key:
        raise RuntimeError("ElevenLabs is not configured")
    if section not in {"translation", "commentary", "practice", "all"}:
        raise ValueError("Unknown listen section")
    room = voice_room_for(verse)
    text = build_script(verse, section)
    if not text:
        raise ValueError("Nothing to speak on this passage")
    async with httpx.AsyncClient() as client:
        voice_id = await resolve_voice(room, client)
        store_key = _speech_key(voice_id, text)
        cached = await listen_store.get_object(store_key)
        title = str(verse.get("title") or "")
        verse_id = str(verse.get("_id") or "")
        if cached:
            if verse_id:
                await listen_store.put_object(verse_speech_key(verse_id, section), cached)
            audio = cached
        else:
            audio = await _speak(client, voice_id, text)
            await listen_store.put_object(store_key, audio)
            if verse_id:
                await listen_store.put_object(verse_speech_key(verse_id, section), audio)
        if publish and verse_id and section in SPEAKABLE_SECTIONS:
            await publish_listen_sections({verse_id: [section]})
        return audio, ListenScript(room, voice_id, text, title, section)

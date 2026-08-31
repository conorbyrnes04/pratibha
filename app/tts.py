"""ElevenLabs listen path — English layers only, voice room per tradition.

Accent comes from a real library/account voice when one is configured or
already in the ElevenLabs workspace. Dakota and Christian stay unmarked
English. Original / IAST are never spoken.
"""
from __future__ import annotations

import hashlib
import logging
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx

from .config import settings

logger = logging.getLogger("pratibha.tts")

_DEFAULT_VOICE = "nPczCjzI2devNBz1zQrb"  # Brian — calm American narration
_MODEL = "eleven_multilingual_v2"
_MAX_CHARS = 4200
_CACHE_DIR = Path(__file__).resolve().parents[1] / ".cache" / "tts"
_ELEVEN_TTS = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
_ELEVEN_VOICES = "https://api.elevenlabs.io/v1/voices"

_MD_RE = re.compile(r"[*_`#>\[\]()]+")
_WS_RE = re.compile(r"\s+")

VoiceRoom = str  # indic | sinosphere | yoruba | hebrew | hellenic | sufi | unmarked

_ROOM_ACCENTS: dict[str, tuple[str, ...]] = {
    "indic": ("indian", "indian english", "south asian", "hindi"),
    "sinosphere": ("chinese", "mandarin", "cantonese", "singaporean", "taiwanese"),
    "yoruba": ("nigerian", "african", "west african", "yoruba"),
    "hebrew": ("israeli", "hebrew", "jewish"),
    "hellenic": ("greek",),
    "sufi": ("persian", "iranian", "arabic", "egyptian", "levantine"),
    "unmarked": (),
}

# Collection / work_id → room. Order matters; first match wins.
_ROOM_PATTERNS: list[tuple[re.Pattern[str], VoiceRoom]] = [
    (re.compile(r"yoruba|johnson", re.I), "yoruba"),
    (re.compile(r"eastman|zitkala|soul of the indian|old indian legends|dakota", re.I), "unmarked"),
    (re.compile(r"ecclesiastes|qoheleth|zohar|yetzirah|kabbalah", re.I), "hebrew"),
    (re.compile(r"rumi|rūmī|ibn.?arabi|balyani|mathnaw", re.I), "sufi"),
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
            r"gospel.?of.?thomas|course in miracles|acim",
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
            r"katha|chandogya|mundaka|brihad|isavasya|svetasvatara",
            re.I,
        ),
        "indic",
    ),
]

_account_voices: list[dict[str, Any]] | None = None
_account_voices_at = 0.0


@dataclass(frozen=True)
class ListenScript:
    room: VoiceRoom
    voice_id: str
    text: str
    title: str


def configured() -> bool:
    return bool((settings.ELEVENLABS_API_KEY or os.getenv("ELEVENLABS_API_KEY") or "").strip())


def _api_key() -> str:
    return (settings.ELEVENLABS_API_KEY or os.getenv("ELEVENLABS_API_KEY") or "").strip()


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
            body = _strip_md(str(layer.get("body") or ""))
            if body:
                return body
    fallback = {
        "translation": verse.get("translation"),
        "commentary": verse.get("commentary"),
        "practice": verse.get("practice") or verse.get("abhyasa"),
    }.get(kind)
    return _strip_md(str(fallback or ""))


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


def _env_voice(room: VoiceRoom) -> str:
    key = f"ELEVENLABS_VOICE_{room.upper()}"
    return (os.getenv(key) or "").strip()


def _match_account_voice(room: VoiceRoom) -> str:
    accents = _ROOM_ACCENTS.get(room) or ()
    if not accents:
        return ""
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
        if use and use not in {"narration", "audiobook", "narrative", "meditation", ""}:
            # Still usable; prefer narration when several match.
            continue
        return vid
    for voice in _account_voices or []:
        labels = voice.get("labels") if isinstance(voice.get("labels"), dict) else {}
        accent = str(labels.get("accent") or "").strip().lower()
        name = str(voice.get("name") or "").lower()
        if any(token in accent or token in name for token in accents):
            vid = str(voice.get("voice_id") or "").strip()
            if vid:
                return vid
    return ""


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


async def resolve_voice(room: VoiceRoom, client: httpx.AsyncClient) -> str:
    pinned = _env_voice(room)
    if pinned:
        return pinned
    if room != "unmarked":
        await _refresh_account_voices(client)
        matched = _match_account_voice(room)
        if matched:
            return matched
    return _unmarked_voice()


def build_script(verse: dict[str, Any]) -> str:
    title = _strip_md(str(verse.get("title") or verse.get("sutra_id") or ""))
    translation = _layer(verse, "translation")
    commentary = _layer(verse, "commentary")
    practice = _layer(verse, "practice")
    parts: list[str] = []
    if title:
        parts.append(title + ".")
    if translation:
        parts.append(translation)
    if commentary:
        parts.extend(["Commentary.", commentary])
    if practice:
        parts.extend(["The practice.", practice])
    text = "\n\n".join(parts).strip()
    if len(text) > _MAX_CHARS:
        text = text[:_MAX_CHARS].rsplit(" ", 1)[0].rstrip() + "."
    return text


def _cache_path(voice_id: str, text: str) -> Path:
    digest = hashlib.sha256(f"{_MODEL}\0{voice_id}\0{text}".encode("utf-8")).hexdigest()
    return _CACHE_DIR / f"{digest}.mp3"


async def synthesize(verse: dict[str, Any]) -> tuple[bytes, ListenScript]:
    key = _api_key()
    if not key:
        raise RuntimeError("ElevenLabs is not configured")
    room = voice_room_for(verse)
    text = build_script(verse)
    if not text:
        raise ValueError("Nothing to speak on this passage")
    async with httpx.AsyncClient() as client:
        voice_id = await resolve_voice(room, client)
        cached = _cache_path(voice_id, text)
        if cached.is_file():
            return cached.read_bytes(), ListenScript(room, voice_id, text, str(verse.get("title") or ""))
        url = _ELEVEN_TTS.format(voice_id=voice_id)
        res = await client.post(
            url,
            params={"output_format": "mp3_44100_128"},
            headers={"xi-api-key": key, "Accept": "audio/mpeg"},
            json={
                "text": text,
                "model_id": (os.getenv("ELEVENLABS_MODEL") or _MODEL).strip() or _MODEL,
                "voice_settings": {
                    "stability": 0.68,
                    "similarity_boost": 0.72,
                    "style": 0.0,
                    "speed": 0.92,
                    "use_speaker_boost": True,
                },
            },
            timeout=90.0,
        )
        if res.status_code >= 400:
            logger.info("ElevenLabs TTS failed: %s %s", res.status_code, res.text[:240])
            raise RuntimeError(f"ElevenLabs returned {res.status_code}")
        audio = res.content
        if not audio:
            raise RuntimeError("ElevenLabs returned empty audio")
        try:
            cached.parent.mkdir(parents=True, exist_ok=True)
            cached.write_bytes(audio)
        except OSError:
            logger.debug("TTS cache write failed", exc_info=True)
        return audio, ListenScript(room, voice_id, text, str(verse.get("title") or ""))

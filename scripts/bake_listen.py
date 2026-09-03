#!/usr/bin/env python3
"""Bake Listen audio: tradition cues, then a named slice of speech.

Default slice is the essential Path primaries (not supporting readings).
Skip anything already in the local/Supabase archive. English layers only.
After speech lands, the live Listen index is published so the verse
shows Play on production without waiting for a deploy.

Every run also bakes spoken layer titles ("Translation.", "Commentary.",
"Practice.") once per pinned voice. Use --slice announces to do only that.

Accented rooms (Indic, Yoruba/Nigerian, Sinosphere, Hellenic, Sufi, Hebrew)
must bake with a matching accent pin. Unmarked English is only for Christian
works, ACIM, and Dakota when no real Dakota/Lakota/Nakota speaker is pinned.
Named women (Lal Ded) use the female pin for that room.

Usage:
    .venv/bin/python scripts/bake_listen.py
    .venv/bin/python scripts/bake_listen.py --dry-run
    .venv/bin/python scripts/bake_listen.py --slice path
    .venv/bin/python scripts/bake_listen.py --slice announces
    .venv/bin/python scripts/bake_listen.py --tracks seer-in-its-nature
    .venv/bin/python scripts/bake_listen.py --slice work --work lalla_vakyani
    .venv/bin/python scripts/bake_listen.py --slice fill --reserve 0
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.data_loader import get_all_verses  # noqa: E402
from app.tts import (  # noqa: E402
    SECTION_ANNOUNCE,
    _CUE_PROMPTS,
    _api_key,
    _speech_key,
    available_sections,
    build_script,
    iter_pinned_voices,
    publish_listen_sections,
    resolve_verse_voice,
    synthesize,
    synthesize_announce,
    synthesize_cue,
    verse_speech_key,
    voice_gender_for,
    voice_room_for,
)

SPINE = [
    "action-without-contraction",
    "recognizing-awareness",
    "heart-of-recognition",
    "three-doors-of-shiva",
    "the-112-doorways",
    "descent-of-the-cakra",
    "letting-go-death-emptiness",
    "the-one-and-the-many",
]
LIVING = [
    "seer-in-its-nature",
    "emptiness-and-compassion",
    "the-horse-of-conversation",
    "you-are-that",
    "nameless-source",
    "become-sunlike",
    "divine-darkness",
    "what-is-up-to-you",
    "the-living-saying",
    "before-the-face",
    "the-beloved-in-plain-sight",
    "the-sacred-tremor",
    "lallas-house",
    "straight-speech",
    "know-yourself",
    "unveiling-the-veiled",
    "the-seven-valleys",
    "the-reed-complains",
    "the-body-of-hatha",
    "humaneness-at-hand",
    "cutting-the-diamond",
    "under-the-sun",
    "thirty-two-paths",
    "flux-and-what-is",
    "silent-worship",
    "stop-seeking",
    "the-sky-is-not-addressed",
    "the-remaining-cult",
    "between-the-tomb-and-the-pulpit",
]


def _parse_tracks(path: Path) -> list[tuple[str, list[str], list[str]]]:
    text = path.read_text()
    tracks: list[tuple[str, list[str], list[str]]] = []

    def collect(tid: str, chunk: str) -> None:
        primaries = re.findall(r'passageId:\s*"([^"]+)"', chunk)
        supporting: list[str] = []
        for match in re.finditer(r'supportingPassageIds:\s*\[(.*?)\]', chunk, re.S):
            supporting.extend(re.findall(r'"([^"]+)"', match.group(1)))
        if primaries or supporting:
            tracks.append((tid, primaries, supporting))

    chunks = re.split(r'\n  \{\n    id: "', text)
    if len(chunks) > 1:
        for chunk in chunks[1:]:
            collect(chunk.split('"', 1)[0], chunk)
        return tracks

    match = re.search(r'export const \w+: LearningTrack = \{\s*id: "([^"]+)"', text)
    if match:
        collect(match.group(1), text)
    return tracks


_TRACK_DIR = ROOT / "web/src/lib/learn/tracks"
TRACK_FILES = (
    ROOT / "web/src/lib/learningPaths.ts",
    ROOT / "web/src/lib/learn/livingTrails.ts",
    ROOT / "web/src/lib/learn/lineageTrails.ts",
    ROOT / "web/src/lib/learn/westernTrails.ts",
    *sorted(_TRACK_DIR.glob("*.ts")),
)


def _all_tracks() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for path in TRACK_FILES:
        for tid, ids, _supporting in _parse_tracks(path):
            out[tid] = ids
    return out


def _supporting_ids(track_ids: list[str]) -> list[str]:
    out: list[str] = []
    for path in TRACK_FILES:
        for tid, _primaries, supporting in _parse_tracks(path):
            if tid in track_ids:
                out.extend(supporting)
    return out


def _fold(s: str) -> str:
    table = str.maketrans(
        {
            "ā": "a",
            "ī": "i",
            "ū": "u",
            "ś": "s",
            "ṣ": "s",
            "ñ": "n",
            "ṭ": "t",
            "ḍ": "d",
            "ṇ": "n",
            "ō": "o",
            "é": "e",
            "ṁ": "m",
            "ṃ": "m",
        }
    )
    return s.lower().translate(table)


def _index_verses() -> tuple[dict[str, dict], dict[str, dict]]:
    verses = get_all_verses()
    by_id: dict[str, dict] = {}
    folded: dict[str, dict] = {}
    for verse in verses:
        for key in ("_id", "unit_id", "sutra_id"):
            val = str(verse.get(key) or "").strip()
            if val:
                by_id.setdefault(val, verse)
                folded.setdefault(_fold(val), verse)
    return by_id, folded


def resolve_passage(pid: str, by_id: dict, folded: dict):
    if pid in by_id:
        return by_id[pid]
    folded_id = _fold(pid)
    if folded_id in folded:
        return folded[folded_id]
    tail = pid.split(".")[-1]
    hits = [
        verse
        for verse in by_id.values()
        if str(verse.get("sutra_id") or "") == tail
        or str(verse.get("_id") or "").endswith("." + tail)
    ]
    if len(hits) == 1:
        return hits[0]
    return None


def subscription() -> dict:
    key = _api_key()
    req = urllib.request.Request(
        "https://api.elevenlabs.io/v1/user/subscription",
        headers={"xi-api-key": key},
    )
    with urllib.request.urlopen(req, timeout=20) as res:
        return json.load(res)


def remaining_chars(sub: dict | None = None) -> int:
    data = sub or subscription()
    return int(data.get("character_limit") or 0) - int(data.get("character_count") or 0)


async def bake_cues(*, dry_run: bool) -> tuple[int, int]:
    made = skipped = 0
    rooms = sorted(_CUE_PROMPTS)
    print(f"Cues: {len(rooms)} rooms × open/close = {len(rooms) * 2}")
    for room in rooms:
        for edge in ("open", "close"):
            if dry_run:
                print(f"  would cue {room}/{edge}")
                made += 1
                continue
            for attempt in range(3):
                try:
                    await synthesize_cue(room, edge)
                    print(f"  cue {room}/{edge}")
                    made += 1
                    break
                except Exception as exc:
                    if attempt == 2:
                        print(f"  FAIL cue {room}/{edge}: {exc}")
                    else:
                        await asyncio.sleep(2 ** attempt)
    return made, skipped


async def bake_announces(*, dry_run: bool) -> tuple[int, int, int, list[str]]:
    """Spoken 'Translation.' / 'Commentary.' / 'Practice.' once per pinned voice."""
    from app import listen_store
    from app.tts import announce_key

    made = skipped = chars_spent = 0
    failed: list[str] = []
    pins = iter_pinned_voices()
    jobs = [
        (room, gender, voice_id, section)
        for room, gender, voice_id in pins
        for section in SECTION_ANNOUNCE
    ]
    print(f"Announces: {len(pins)} voices × {len(SECTION_ANNOUNCE)} headings = {len(jobs)}")
    for room, gender, voice_id, section in jobs:
        n = len(SECTION_ANNOUNCE[section])
        label = f"{room}/{gender} {section} ({voice_id[:8]})"
        if dry_run:
            print(f"  would announce {label}")
            made += 1
            chars_spent += n
            continue
        cached = listen_store.read_local(announce_key(voice_id, section)) or await listen_store.get_object(
            announce_key(voice_id, section)
        )
        if cached:
            print(f"  skip announce {label}")
            skipped += 1
            continue
        for attempt in range(3):
            try:
                await synthesize_announce(voice_id, section)
                chars_spent += n
                made += 1
                print(f"  announce {label} ({n} chars)")
                break
            except Exception as exc:
                if attempt == 2:
                    failed.append(f"{voice_id}:{section}")
                    print(f"  FAIL announce {label}: {exc}")
                else:
                    await asyncio.sleep(2 ** attempt)
        await asyncio.sleep(0.1)
    return made, skipped, chars_spent, failed


async def bake_speech(
    verses: list[dict],
    *,
    dry_run: bool,
    reserve: int,
    leftover: int | None = None,
) -> tuple[int, int, int, list[str]]:
    import httpx

    from app import listen_store

    made = skipped = chars_spent = 0
    missing: list[str] = []
    pending: dict[str, list[str]] = {}
    jobs: list[tuple[dict, str, str, str, str, str]] = []
    async with httpx.AsyncClient() as client:
        voice_by_cast: dict[tuple[str, str], str] = {}
        for verse in verses:
            room = voice_room_for(verse)
            gender = voice_gender_for(verse)
            key = (room, gender)
            if key not in voice_by_cast:
                voice_by_cast[key] = await resolve_verse_voice(verse, client)
                print(
                    f"  cast {room}/{gender} → {voice_by_cast[key]}"
                    f"{'  (female author)' if gender == 'female' else ''}"
                )
            voice_id = voice_by_cast[key]
            for section in available_sections(verse):
                text = build_script(verse, section)
                if not text:
                    continue
                jobs.append((verse, section, voice_id, text, room, gender))

    print(f"Speech jobs: {len(jobs)} across {len(verses)} verses")
    left = leftover if leftover is not None else remaining_chars()
    print(f"Creator remaining before speech: {left:,}")

    for verse, section, voice_id, text, room, gender in jobs:
        vid = str(verse.get("_id") or "")
        key = _speech_key(voice_id, text)
        cached = listen_store.read_local(key) or await listen_store.get_object(key)
        if cached:
            dest = verse_speech_key(vid, section)
            await listen_store.put_object(dest, cached)
            pending.setdefault(vid, []).append(section)
            print(f"  skip {vid} {section} (cache {room}/{gender})")
            skipped += 1
            continue
        n = len(text)
        if not dry_run and left - chars_spent - n < reserve:
            print(f"  STOP at reserve ({reserve:,}). leftover would be {left - chars_spent:,}")
            break
        if dry_run:
            print(f"  would speak {vid} {section} ({n} chars, {room}/{gender})")
            made += 1
            chars_spent += n
            continue
        for attempt in range(4):
            try:
                await synthesize(verse, section, publish=False)
                chars_spent += n
                made += 1
                pending.setdefault(vid, []).append(section)
                print(f"  bake {vid} {section} ({n} chars, {room}/{gender})")
                break
            except Exception as exc:
                wait = 3 * (attempt + 1)
                if attempt == 3:
                    missing.append(f"{vid}:{section}")
                    print(f"  FAIL {vid} {section}: {exc}")
                else:
                    print(f"  retry {vid} {section} in {wait}s ({exc})")
                    await asyncio.sleep(wait)
        await asyncio.sleep(0.15)
    if pending and not dry_run:
        live = await publish_listen_sections(pending)
        print(f"Live Listen index: {len(live)} verses")
    return made, skipped, chars_spent, missing


def collect_verses(track_ids: list[str]) -> tuple[list[dict], list[str]]:
    catalog = _all_tracks()
    by_id, folded = _index_verses()
    seen: set[str] = set()
    verses: list[dict] = []
    unresolved: list[str] = []
    for tid in track_ids:
        ids = catalog.get(tid) or []
        if not ids:
            print(f"Unknown or empty track: {tid}")
            continue
        for pid in ids:
            verse = resolve_passage(pid, by_id, folded)
            if verse is None:
                unresolved.append(pid)
                continue
            vid = str(verse.get("_id") or "")
            if vid in seen:
                continue
            seen.add(vid)
            verses.append(verse)
    return verses, unresolved


def collect_supporting(track_ids: list[str]) -> tuple[list[dict], list[str]]:
    by_id, folded = _index_verses()
    seen: set[str] = set()
    verses: list[dict] = []
    unresolved: list[str] = []
    for pid in _supporting_ids(track_ids):
        verse = resolve_passage(pid, by_id, folded)
        if verse is None:
            unresolved.append(pid)
            continue
        vid = str(verse.get("_id") or "")
        if vid in seen:
            continue
        seen.add(vid)
        verses.append(verse)
    return verses, unresolved


HEROES_PATH = ROOT / "data" / "listen_heroes.json"
FILL_PATH = ROOT / "data" / "listen_fill.json"


def collect_work(work_id: str) -> tuple[list[dict], list[str]]:
    want = work_id.strip().lower()
    verses = [
        v for v in get_all_verses()
        if str(v.get("work_id") or "").strip().lower() == want
    ]
    keyed = [v for v in verses if v.get("tts_key")]
    if keyed:
        return keyed, []
    if HEROES_PATH.is_file():
        data = json.loads(HEROES_PATH.read_text())
        ids = list((data.get(want) or {}).get("ids") or [])
        if ids:
            by_id, folded = _index_verses()
            out: list[dict] = []
            unresolved: list[str] = []
            seen: set[str] = set()
            for pid in ids:
                verse = resolve_passage(pid, by_id, folded)
                if verse is None:
                    unresolved.append(pid)
                    continue
                vid = str(verse.get("_id") or "")
                if vid in seen:
                    continue
                seen.add(vid)
                out.append(verse)
            return out, unresolved
    return verses, []


def collect_fill_verses() -> tuple[list[dict], list[str]]:
    """Bake the even-split wave recorded in data/listen_fill.json."""
    if not FILL_PATH.is_file():
        print("Missing data/listen_fill.json — run scripts/listen_fill.py --plan first")
        return [], []
    data = json.loads(FILL_PATH.read_text())
    ids = list(((data.get("next_wave") or {}).get("ids")) or [])
    if not ids:
        print("listen_fill.json has no next_wave.ids — run scripts/listen_fill.py --plan")
        return [], []
    by_id, folded = _index_verses()
    seen: set[str] = set()
    verses: list[dict] = []
    unresolved: list[str] = []
    for pid in ids:
        verse = resolve_passage(pid, by_id, folded)
        if verse is None:
            unresolved.append(pid)
            continue
        vid = str(verse.get("_id") or "")
        if not vid or vid in seen:
            continue
        seen.add(vid)
        verses.append(verse)
    wave = data.get("next_wave") or {}
    print(
        f"Fill wave {wave.get('id')}: {len(verses)} verses · "
        f"~{wave.get('planned_chars', 0):,} chars"
    )
    return verses, unresolved


def collect_hero_verses() -> tuple[list[dict], list[str]]:
    if not HEROES_PATH.is_file():
        print("Missing data/listen_heroes.json — run scripts/select_listen_heroes.py first")
        return [], []
    data = json.loads(HEROES_PATH.read_text())
    by_id, folded = _index_verses()
    seen: set[str] = set()
    verses: list[dict] = []
    unresolved: list[str] = []
    for row in data.values():
        for pid in row.get("ids") or []:
            verse = resolve_passage(pid, by_id, folded)
            if verse is None:
                unresolved.append(pid)
                continue
            vid = str(verse.get("_id") or "")
            if vid in seen:
                continue
            seen.add(vid)
            verses.append(verse)
    return verses, unresolved


async def main() -> int:
    ap = argparse.ArgumentParser(description="Bake Listen cues and Path speech.")
    ap.add_argument(
        "--slice",
        choices=("cues", "path", "walkable", "tracks", "heroes", "suggested", "work", "fill", "announces"),
        default="path",
        help="path = cues + essential Path primaries. fill = next wave in data/listen_fill.json. suggested = Path supporting readings. announces = spoken layer titles.",
    )
    ap.add_argument("--tracks", nargs="*", default=[], help="Track ids when --slice tracks.")
    ap.add_argument(
        "--work",
        action="append",
        default=[],
        help="Work_id when --slice work (repeatable). Uses tts_key verses, else listen_heroes.json.",
    )
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--ids",
        nargs="*",
        default=[],
        help="Verse _ids to bake (recast spoken audio for these only).",
    )
    ap.add_argument(
        "--reserve",
        type=int,
        default=20_000,
        help="Leave at least this many TTS characters for later Path work.",
    )
    args = ap.parse_args()

    if not _api_key():
        print("ELEVENLABS_API_KEY is not set")
        return 1

    sub = subscription()
    print(
        f"Plan {sub.get('tier')} · used {sub.get('character_count'):,} / "
        f"{sub.get('character_limit'):,} · left {remaining_chars(sub):,}"
    )

    t0 = time.monotonic()
    cue_made = cue_skip = 0
    recast_only = bool(args.ids)
    if not recast_only and args.slice in {"cues", "path", "walkable", "work"}:
        cue_made, cue_skip = await bake_cues(dry_run=args.dry_run)

    track_ids: list[str] = []
    verses: list[dict] = []
    unresolved: list[str] = []
    if recast_only:
        by_id, folded = _index_verses()
        seen: set[str] = set()
        for pid in args.ids:
            verse = resolve_passage(pid, by_id, folded)
            if verse is None:
                unresolved.append(pid)
                continue
            vid = str(verse.get("_id") or "")
            if not vid or vid in seen:
                continue
            seen.add(vid)
            verses.append(verse)
        print(f"Recast ids: {len(verses)} verses")
    elif args.slice == "path":
        track_ids = list(SPINE)
    elif args.slice == "walkable":
        track_ids = list(SPINE) + list(LIVING)
    elif args.slice == "tracks":
        track_ids = list(args.tracks)
    elif args.slice == "heroes":
        verses, unresolved = collect_hero_verses()
    elif args.slice == "fill":
        verses, unresolved = collect_fill_verses()
    elif args.slice == "work":
        if not args.work:
            print("--work is required with --slice work")
            return 1
        seen: set[str] = set()
        for wid in args.work:
            chunk, missing = collect_work(wid)
            unresolved.extend(missing)
            print(f"Work {wid}: {len(chunk)} verses")
            for verse in chunk:
                vid = str(verse.get("_id") or "")
                if not vid or vid in seen:
                    continue
                seen.add(vid)
                verses.append(verse)
    elif args.slice == "suggested":
        verses, unresolved = collect_supporting(list(SPINE))

    if track_ids:
        verses, unresolved = collect_verses(track_ids)

    announce_made = announce_skip = announce_chars = 0
    announce_failed: list[str] = []
    if not recast_only and args.slice != "fill":
        announce_made, announce_skip, announce_chars, announce_failed = await bake_announces(
            dry_run=args.dry_run
        )

    speech_made = speech_skip = chars = 0
    failed: list[str] = []
    if verses:
        if unresolved:
            print(f"Unresolved passage ids ({len(unresolved)}): {unresolved}")
        speech_made, speech_skip, chars, failed = await bake_speech(
            verses, dry_run=args.dry_run, reserve=args.reserve, leftover=remaining_chars(sub)
        )

    elapsed = time.monotonic() - t0
    spent = chars + announce_chars
    if args.dry_run:
        after = remaining_chars(sub) - spent
    else:
        try:
            after = remaining_chars()
        except Exception:
            after = remaining_chars(sub) - spent
    print()
    print(
        f"Done in {elapsed:.0f}s · cues {cue_made} · announces {announce_made} · "
        f"speech baked {speech_made} · skipped {speech_skip + announce_skip} · "
        f"~{spent:,} chars · leftover ~{after:,}"
    )
    failed = failed + announce_failed
    if failed:
        print(f"Failed ({len(failed)}): {failed}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))

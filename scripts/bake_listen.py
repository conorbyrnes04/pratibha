#!/usr/bin/env python3
"""Bake Listen audio: tradition cues, then a named slice of speech.

Default slice is the essential Path primaries (not supporting readings).
Skip anything already in the local/Supabase archive. English layers only.

Usage:
    .venv/bin/python scripts/bake_listen.py
    .venv/bin/python scripts/bake_listen.py --dry-run
    .venv/bin/python scripts/bake_listen.py --slice path
    .venv/bin/python scripts/bake_listen.py --tracks seer-in-its-nature
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
    SPEAKABLE_SECTIONS,
    _CUE_PROMPTS,
    _api_key,
    _speech_key,
    available_sections,
    build_script,
    resolve_voice,
    synthesize,
    synthesize_cue,
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
]


def _parse_tracks(path: Path) -> list[tuple[str, list[str], list[str]]]:
    text = path.read_text()
    tracks: list[tuple[str, list[str], list[str]]] = []
    for chunk in re.split(r'\n  \{\n    id: "', text)[1:]:
        tid = chunk.split('"', 1)[0]
        primaries = re.findall(r'passageId:\s*"([^"]+)"', chunk)
        supporting: list[str] = []
        for match in re.finditer(r'supportingPassageIds:\s*\[(.*?)\]', chunk, re.S):
            supporting.extend(re.findall(r'"([^"]+)"', match.group(1)))
        if primaries or supporting:
            tracks.append((tid, primaries, supporting))
    return tracks


def _all_tracks() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for path in (
        ROOT / "web/src/lib/learningPaths.ts",
        ROOT / "web/src/lib/learn/livingTrails.ts",
    ):
        for tid, ids, _supporting in _parse_tracks(path):
            out[tid] = ids
    return out


def _supporting_ids(track_ids: list[str]) -> list[str]:
    out: list[str] = []
    for path in (
        ROOT / "web/src/lib/learningPaths.ts",
        ROOT / "web/src/lib/learn/livingTrails.ts",
    ):
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


async def bake_speech(
    verses: list[dict],
    *,
    dry_run: bool,
    reserve: int,
) -> tuple[int, int, int, list[str]]:
    import httpx

    from app import listen_store

    made = skipped = chars_spent = 0
    missing: list[str] = []
    jobs: list[tuple[dict, str, str, str]] = []
    async with httpx.AsyncClient() as client:
        voice_by_room: dict[str, str] = {}
        for verse in verses:
            room = voice_room_for(verse)
            if room not in voice_by_room:
                voice_by_room[room] = await resolve_voice(room, client)
            voice_id = voice_by_room[room]
            for section in available_sections(verse):
                text = build_script(verse, section)
                if not text:
                    continue
                jobs.append((verse, section, voice_id, text))

    print(f"Speech jobs: {len(jobs)} across {len(verses)} verses")
    left = remaining_chars()
    print(f"Creator remaining before speech: {left:,}")

    for verse, section, voice_id, text in jobs:
        vid = str(verse.get("_id") or "")
        key = _speech_key(voice_id, text)
        cached = listen_store.read_local(key) or await listen_store.get_object(key)
        if cached:
            print(f"  skip {vid} {section} (cache)")
            skipped += 1
            continue
        n = len(text)
        if not dry_run and left - chars_spent - n < reserve:
            print(f"  STOP at reserve ({reserve:,}). leftover would be {left - chars_spent:,}")
            break
        if dry_run:
            print(f"  would speak {vid} {section} ({n} chars, {voice_room_for(verse)})")
            made += 1
            chars_spent += n
            continue
        for attempt in range(4):
            try:
                await synthesize(verse, section)
                chars_spent += n
                made += 1
                print(f"  bake {vid} {section} ({n} chars)")
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
        choices=("cues", "path", "walkable", "tracks", "heroes", "suggested"),
        default="path",
        help="path = cues + essential Path primaries. suggested = Path supporting readings.",
    )
    ap.add_argument("--tracks", nargs="*", default=[], help="Track ids when --slice tracks.")
    ap.add_argument("--dry-run", action="store_true")
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
    if args.slice in {"cues", "path", "walkable"}:
        cue_made, cue_skip = await bake_cues(dry_run=args.dry_run)

    track_ids: list[str] = []
    verses: list[dict] = []
    unresolved: list[str] = []
    if args.slice == "path":
        track_ids = list(SPINE)
    elif args.slice == "walkable":
        track_ids = list(SPINE) + list(LIVING)
    elif args.slice == "tracks":
        track_ids = list(args.tracks)
    elif args.slice == "heroes":
        verses, unresolved = collect_hero_verses()
    elif args.slice == "suggested":
        verses, unresolved = collect_supporting(list(SPINE))

    if track_ids:
        verses, unresolved = collect_verses(track_ids)

    speech_made = speech_skip = chars = 0
    failed: list[str] = []
    if verses:
        if unresolved:
            print(f"Unresolved passage ids ({len(unresolved)}): {unresolved}")
        speech_made, speech_skip, chars, failed = await bake_speech(
            verses, dry_run=args.dry_run, reserve=args.reserve
        )

    elapsed = time.monotonic() - t0
    after = remaining_chars() if not args.dry_run else remaining_chars(sub) - chars
    print()
    print(
        f"Done in {elapsed:.0f}s · cues {cue_made} · speech baked {speech_made} · "
        f"skipped {speech_skip} · ~{chars:,} chars · leftover ~{after:,}"
    )
    if failed:
        print(f"Failed ({len(failed)}): {failed}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))

#!/usr/bin/env python3
"""Map already-baked ElevenLabs speech onto verse ids.

Writes data/listen_archive.json, copies hits to verse/{id}/{section}.mp3,
and publishes the live storage index so Listen appears without a deploy.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import listen_store  # noqa: E402
from app.data_loader import get_all_verses  # noqa: E402
from app.tts import (  # noqa: E402
    SPEAKABLE_SECTIONS,
    _DEFAULT_VOICE,
    _env_voice,
    _speech_key,
    build_script,
    publish_listen_sections,
    verse_speech_key,
    voice_gender_for,
    voice_room_for,
)

OUT = ROOT / "data" / "listen_archive.json"


def _voice_for(verse: dict) -> str:
    room = voice_room_for(verse)
    gender = voice_gender_for(verse)
    return _env_voice(room, gender) or _DEFAULT_VOICE


def index_local() -> dict[str, list[str]]:
    archive: dict[str, list[str]] = {}
    verses = get_all_verses()
    print(f"Scanning {len(verses)} verses against local Listen cache…")
    hits = 0
    for verse in verses:
        vid = str(verse.get("_id") or "").strip()
        if not vid:
            continue
        voice = _voice_for(verse)
        found: list[str] = []
        for section in SPEAKABLE_SECTIONS:
            text = build_script(verse, section)
            if not text:
                continue
            if listen_store.read_local(_speech_key(voice, text)):
                found.append(section)
        if found:
            archive[vid] = found
            hits += 1
    print(f"Baked verses: {hits}")
    return archive


async def copy_stable(archive: dict[str, list[str]], *, upload: bool) -> tuple[int, int]:
    copied = skipped = 0
    verses = {str(v.get("_id") or ""): v for v in get_all_verses()}
    jobs: list[tuple[str, bytes]] = []
    for vid, sections in archive.items():
        verse = verses.get(vid)
        if not verse:
            continue
        voice = _voice_for(verse)
        for section in sections:
            text = build_script(verse, section)
            src_key = _speech_key(voice, text)
            audio = listen_store.read_local(src_key)
            if not audio:
                continue
            dest = verse_speech_key(vid, section)
            if listen_store.read_local(dest):
                skipped += 1
            else:
                listen_store.write_local(dest, audio)
                copied += 1
            if upload:
                jobs.append((dest, audio))
    if not upload or not jobs:
        return copied, skipped
    sem = asyncio.Semaphore(8)
    done = 0

    async def put(dest: str, audio: bytes) -> None:
        nonlocal done
        async with sem:
            await listen_store.put_object(dest, audio)
            done += 1
            if done == 1 or done % 40 == 0 or done == len(jobs):
                print(f"Uploaded {done}/{len(jobs)}", flush=True)

    print(f"Uploading {len(jobs)} stable keys…", flush=True)
    await asyncio.gather(*(put(dest, audio) for dest, audio in jobs))
    return copied, skipped


async def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--upload", action="store_true", help="Also write stable keys to Supabase.")
    ap.add_argument(
        "--from-json",
        action="store_true",
        help="Reuse data/listen_archive.json instead of rescanning the local cache.",
    )
    args = ap.parse_args()
    if args.from_json and OUT.is_file():
        archive = json.loads(OUT.read_text())
        if not isinstance(archive, dict):
            raise SystemExit("listen_archive.json is not an object")
        print(f"Loaded {OUT.relative_to(ROOT)} ({len(archive)} verses)")
    else:
        archive = index_local()
        OUT.write_text(json.dumps(archive, indent=2, sort_keys=True) + "\n")
        print(f"Wrote {OUT.relative_to(ROOT)} ({len(archive)} verses)")
    copied, skipped = await copy_stable(archive, upload=args.upload)
    print(f"Stable keys copied {copied} · already present {skipped}")
    live = await publish_listen_sections(
        {str(vid): list(sections) for vid, sections in archive.items()}
    )
    print(f"Live Listen index: {len(live)} verses")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))

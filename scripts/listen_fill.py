#!/usr/bin/env python3
"""Listen fill tracker: what still needs baking, and the next even-split wave.

Refreshes data/listen_fill.json from the corpus, Path gates, heroes, and the
Listen archive. Fill order per work is path primaries → hero verses → the rest.

Usage:
    .venv/bin/python scripts/listen_fill.py
    .venv/bin/python scripts/listen_fill.py --plan 41000
    .venv/bin/python scripts/listen_fill.py --plan 41000 --dry-run
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.data_loader import get_all_verses  # noqa: E402
from app.tts import (  # noqa: E402
    _TTS_GATED_COLLECTIONS,
    available_sections,
    build_script,
    voice_room_for,
)
from scripts.bake_listen import (  # noqa: E402
    HEROES_PATH,
    LIVING,
    SPINE,
    _all_tracks,
    _index_verses,
    resolve_passage,
)

OUT = ROOT / "data" / "listen_fill.json"
ARCHIVE = ROOT / "data" / "listen_archive.json"
QUEUE_HEAD = 16

# Landmark works to even-split a budget across when they are still empty or
# missing Path gates. Edit this list in listen_fill.json; a missing file falls
# back to this default.
DEFAULT_HIGH_VALUE = [
    "patañjali_yoga_sūtras",
    "heart_sutra",
    "nagarjuna_mulamadhyamakakarika",
    "shantideva_bodhicaryavatara",
    "katha_upanishad",
    "milarepa_songs",
    "mundaka_upanishad",
    "tao_te_ching",
    "yoga_spandakarika",
    "dhammapada",
    "mandukya_upanishad_and_gaudapada_karika",
    "yoruba_proverbs",
    "plotinus_enneads",
]

POLICY = {
    "fill_order": ["path_primary", "hero", "rest"],
    "gated_works": sorted(_TTS_GATED_COLLECTIONS),
    "target": {
        "gated": "tts_key verses only",
        "small": "every speakable unit when there are 15 or fewer",
        "default": "Path primaries, then heroes, then the rest over time",
        "catalogue": "Path + heroes only when there are 80 or more units",
    },
}


def _vid(verse: dict) -> str:
    return str(verse.get("_id") or verse.get("unit_id") or "").strip()


def _wid(verse: dict) -> str:
    return str(verse.get("work_id") or verse.get("collection") or "unknown").strip()


def verse_chars(verse: dict) -> int:
    return sum(len(build_script(verse, section) or "") for section in available_sections(verse))


def load_archive() -> dict[str, list[str]]:
    if not ARCHIVE.is_file():
        return {}
    raw = json.loads(ARCHIVE.read_text())
    return raw if isinstance(raw, dict) else {}


def load_heroes() -> dict:
    if not HEROES_PATH.is_file():
        return {}
    return json.loads(HEROES_PATH.read_text())


def load_existing() -> dict:
    if not OUT.is_file():
        return {}
    try:
        data = json.loads(OUT.read_text())
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def target_for(n: int, gated: bool) -> str:
    if gated:
        return "keys"
    if n <= 15:
        return "all"
    if n >= 80:
        return "path_then_heroes"
    return "path_then_heroes_then_rest"


def status_for(baked: int, speakable: int) -> str:
    if speakable <= 0:
        return "silent"
    pct = 100.0 * baked / speakable
    if baked <= 0:
        return "empty"
    if pct < 25:
        return "thin"
    if pct < 80:
        return "filling"
    if pct < 100:
        return "nearly"
    return "complete"


def path_primaries() -> dict[str, list[str]]:
    tracks = _all_tracks()
    by_id, folded = _index_verses()
    by_work: dict[str, list[str]] = defaultdict(list)
    seen: set[str] = set()
    for tid in list(SPINE) + list(LIVING):
        for pid in tracks.get(tid) or []:
            verse = resolve_passage(pid, by_id, folded)
            if verse is None:
                continue
            vid = _vid(verse)
            if not vid or vid in seen:
                continue
            seen.add(vid)
            by_work[_wid(verse)].append(vid)
    return dict(by_work)


def build_works() -> dict[str, dict]:
    archive = load_archive()
    heroes = load_heroes()
    by_id, folded = _index_verses()
    path_ids = path_primaries()
    buckets: dict[str, list[dict]] = defaultdict(list)
    for verse in get_all_verses():
        buckets[_wid(verse)].append(verse)

    works: dict[str, dict] = {}
    for wid, rows in sorted(buckets.items()):
        gated = wid.lower() in _TTS_GATED_COLLECTIONS
        title = str(rows[0].get("work_title") or wid)
        room = voice_room_for(rows[0])
        speakable_rows = [v for v in rows if available_sections(v)]
        baked_rows = [v for v in speakable_rows if archive.get(_vid(v))]
        speakable_ids = [_vid(v) for v in speakable_rows]
        baked_set = {_vid(v) for v in baked_rows}

        def resolve_list(ids: list[str]) -> list[str]:
            out: list[str] = []
            seen: set[str] = set()
            for pid in ids:
                verse = resolve_passage(pid, by_id, folded) if pid not in by_id else by_id.get(pid)
                if verse is None:
                    continue
                vid = _vid(verse)
                if not vid or vid in seen:
                    continue
                seen.add(vid)
                out.append(vid)
            return out

        path = resolve_list(path_ids.get(wid, []))
        hero = resolve_list(list((heroes.get(wid) or {}).get("ids") or []))
        rest = [vid for vid in speakable_ids if vid not in path and vid not in hero]
        queue = [vid for vid in path + hero + rest if vid not in baked_set]
        costs = { _vid(v): verse_chars(v) for v in speakable_rows }
        remaining_chars = sum(costs.get(vid, 0) for vid in queue)
        n = len(rows)
        speak = len(speakable_rows)
        baked = len(baked_rows)
        works[wid] = {
            "title": title,
            "room": room,
            "gated": gated,
            "target": target_for(n, gated),
            "status": status_for(baked, speak),
            "units": n,
            "speakable": speak,
            "baked": baked,
            "coverage_pct": round(100.0 * baked / speak, 1) if speak else 0.0,
            "path_unbaked": sum(1 for vid in path if vid not in baked_set),
            "hero_unbaked": sum(1 for vid in hero if vid not in baked_set),
            "remaining_chars": remaining_chars,
            "queue_head": queue[:QUEUE_HEAD],
            "queue_remaining": max(0, len(queue) - QUEUE_HEAD),
        }
    return works


def pick_high_value(works: dict[str, dict], existing: dict) -> list[str]:
    listed = existing.get("high_value")
    if isinstance(listed, list) and listed:
        return [str(wid) for wid in listed if wid in works]
    return [wid for wid in DEFAULT_HIGH_VALUE if wid in works]


def plan_even(works: dict[str, dict], high_value: list[str], budget: int) -> dict:
    """Even-split budget across high-value works: share first, leftover round-robin."""
    by_id, folded = _index_verses()
    archive = load_archive()

    queues: dict[str, list[tuple[str, int]]] = {}
    for wid in high_value:
        # Rebuild the live queue so the wave is not capped at queue_head.
        verses = [v for v in get_all_verses() if _wid(v) == wid]
        heroes = load_heroes()
        path = path_primaries().get(wid, [])
        hero = list((heroes.get(wid) or {}).get("ids") or [])
        seen: set[str] = set()
        ordered: list[str] = []
        for pid in path + hero:
            verse = resolve_passage(pid, by_id, folded)
            if verse is None:
                continue
            vid = _vid(verse)
            if vid and vid not in seen:
                seen.add(vid)
                ordered.append(vid)
        for verse in verses:
            if not available_sections(verse):
                continue
            vid = _vid(verse)
            if vid and vid not in seen:
                seen.add(vid)
                ordered.append(vid)
        q: list[tuple[str, int]] = []
        for vid in ordered:
            if archive.get(vid):
                continue
            verse = resolve_passage(vid, by_id, folded)
            if verse is None:
                continue
            q.append((vid, verse_chars(verse)))
        queues[wid] = q

    n = max(1, len(high_value))
    share = budget // n
    taken: dict[str, list[dict]] = {wid: [] for wid in high_value}
    spent = {wid: 0 for wid in high_value}
    used = 0

    def take(wid: str, vid: str, cost: int) -> bool:
        nonlocal used
        if used + cost > budget:
            return False
        taken[wid].append({"id": vid, "chars": cost})
        spent[wid] += cost
        used += cost
        queues[wid] = [(i, c) for i, c in queues[wid] if i != vid]
        return True

    for wid in high_value:
        while queues[wid]:
            vid, cost = queues[wid][0]
            if spent[wid] == 0:
                if not take(wid, vid, cost):
                    break
                continue
            if spent[wid] + cost <= share:
                take(wid, vid, cost)
            else:
                break

    progressed = True
    while progressed and used < budget:
        progressed = False
        for wid in high_value:
            if not queues[wid]:
                continue
            vid, cost = queues[wid][0]
            if take(wid, vid, cost):
                progressed = True

    ids = [row["id"] for wid in high_value for row in taken[wid]]
    return {
        "id": f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}-even-{budget // 1000}k",
        "budget_chars": budget,
        "share_chars": share,
        "planned_chars": used,
        "works": [
            {
                "work_id": wid,
                "title": (works.get(wid) or {}).get("title") or wid,
                "share": share,
                "chars": spent[wid],
                "verses": taken[wid],
            }
            for wid in high_value
        ],
        "ids": ids,
    }


def snapshot(
    works: dict[str, dict],
    high_value: list[str],
    wave: dict | None,
    scheduled: list | None = None,
) -> dict:
    data = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "policy": POLICY,
        "high_value": high_value,
        "summary": {
            "works": len(works),
            "empty": sum(1 for w in works.values() if w["status"] == "empty"),
            "thin": sum(1 for w in works.values() if w["status"] == "thin"),
            "filling": sum(1 for w in works.values() if w["status"] == "filling"),
            "nearly": sum(1 for w in works.values() if w["status"] == "nearly"),
            "complete": sum(1 for w in works.values() if w["status"] == "complete"),
            "unbaked_path_gates": sum(int(w["path_unbaked"]) for w in works.values()),
            "remaining_chars": sum(int(w["remaining_chars"]) for w in works.values()),
        },
        "works": works,
        "next_wave": wave,
    }
    if scheduled:
        data["scheduled"] = scheduled
    return data


def print_table(data: dict) -> None:
    works = data.get("works") or {}
    print(
        f"{'status':<9} {'cov':>6} {'baked':>6} {'speak':>6} {'pathΔ':>6} "
        f"{'left chars':>11}  work"
    )
    print("-" * 96)
    order = {"empty": 0, "thin": 1, "filling": 2, "nearly": 3, "complete": 4, "silent": 5}
    rows = sorted(
        works.items(),
        key=lambda kv: (order.get(kv[1].get("status"), 9), -int(kv[1].get("remaining_chars") or 0)),
    )
    for wid, w in rows:
        star = "*" if wid in (data.get("high_value") or []) else " "
        print(
            f"{star}{w.get('status', ''):<8} {w.get('coverage_pct', 0):5.0f}% "
            f"{w.get('baked', 0):6d} {w.get('speakable', 0):6d} {w.get('path_unbaked', 0):6d} "
            f"{w.get('remaining_chars', 0):11,d}  {wid}"
        )
    summary = data.get("summary") or {}
    print()
    print(
        f"{summary.get('empty', 0)} empty · {summary.get('thin', 0)} thin · "
        f"{summary.get('filling', 0)} filling · {summary.get('complete', 0)} complete · "
        f"{summary.get('unbaked_path_gates', 0)} path gates still silent"
    )
    for job in data.get("scheduled") or []:
        when = job.get("when") or "?"
        title = job.get("title") or job.get("work_id") or "scheduled bake"
        ids = job.get("ids") or []
        print(f"Scheduled {when}: {title} ({len(ids)} ids)")
    wave = data.get("next_wave")
    if not wave:
        return
    print()
    print(
        f"Next wave {wave.get('id')} · {wave.get('planned_chars', 0):,} / "
        f"{wave.get('budget_chars', 0):,} chars · {len(wave.get('ids') or [])} verses"
    )
    for row in wave.get("works") or []:
        n = len(row.get("verses") or [])
        print(f"  {row.get('chars', 0):5,d} / {row.get('share', 0):,}  {n:2d}v  {row.get('work_id')}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Refresh the Listen fill tracker.")
    ap.add_argument("--plan", type=int, metavar="CHARS", help="Even-split this many characters across high_value works.")
    ap.add_argument("--dry-run", action="store_true", help="Print without writing listen_fill.json.")
    args = ap.parse_args()

    existing = load_existing()
    works = build_works()
    high_value = pick_high_value(works, existing)
    wave = existing.get("next_wave") if isinstance(existing.get("next_wave"), dict) else None
    scheduled = existing.get("scheduled") if isinstance(existing.get("scheduled"), list) else None
    if args.plan:
        wave = plan_even(works, high_value, args.plan)
    data = snapshot(works, high_value, wave, scheduled)
    print_table(data)
    if args.dry_run:
        return 0
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"\nWrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

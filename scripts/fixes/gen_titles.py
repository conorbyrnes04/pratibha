#!/usr/bin/env python3
"""Author thematic-claim titles for bare-reference and verbatim-passage titles.

Per the Pratibha spec, a Title is a thematic CLAIM (it names the move/insight of
the passage), not a verse pointer ("Yukti #2", "Sutra 1") nor the passage
sentence copied verbatim. This detects those two failure modes with the SAME
logic as scripts/audit/titles_themes.py, then authors a short claim-title via a
cheap LLM, grounded in the unit's own translation + commentary.

The navigational reference is preserved separately in `unit_label`/`section`;
only the display `title` is rewritten. Output is a JSONL patch for
apply_canonical_patch.py. Validated to never re-emit a bare/verbatim title.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
INDEX = ROOT / "data" / "canonical" / "index.jsonl"

# --- detection (copied from scripts/audit/titles_themes.py) ------------------
REF_KEYWORD = (
    r"(?:verse|verses|yukti|sutra|sūtra|sloka|śloka|karika|kārikā|fragment|"
    r"pearl|chapter|section|aphorism|enchiridion|book|canto|stanza|hymn|"
    r"mantra|khanda|khaṇḍa|adhyaya|adhyāya|pada|pāda|part|no|number)"
)
BARE_PATTERNS = [
    re.compile(r"^\s*" + REF_KEYWORD + r"[\s#.:§-]*[0-9ivxlcdm]+([.\-–][0-9ivxlcdm]+)*\s*[.:]?\s*$", re.I),
    re.compile(r"^\s*§\s*[0-9]+.*$", re.I),
    re.compile(r"^\s*#\s*[0-9]+\s*$"),
    re.compile(r"^\s*[0-9]+([.\-–][0-9]+)*\s*[.:]?\s*$"),
    re.compile(r"^\s*[ivxlcdm]+([.\-–][0-9]+)*\s*[.:]?\s*$", re.I),
    re.compile(r"^\s*" + REF_KEYWORD + r"\s*[#§]\s*[0-9]+\s*$", re.I),
]


def norm(s: Any) -> str:
    return re.sub(r"\s+", " ", str(s)).strip() if s else ""


def norm_cmp(s: Any) -> str:
    return norm(s).casefold().rstrip(".;: ")


def word_count(s: Any) -> int:
    return len(re.findall(r"\S+", re.sub(r"[*_`>#]", " ", str(s or ""))))


def translation_body(r: dict[str, Any]) -> str:
    for layer in r.get("pratibha_layers", []):
        if layer.get("kind") == "translation":
            return layer.get("body", "") or ""
    return r.get("translation_literal") or r.get("translation") or ""


def commentary_body(r: dict[str, Any]) -> str:
    for layer in r.get("pratibha_layers", []):
        if layer.get("kind") == "commentary":
            return layer.get("body", "") or ""
    return r.get("commentary") or ""


def is_bare_title(title: Any) -> bool:
    t = norm(title)
    if not t:
        return True
    return any(pat.match(t) for pat in BARE_PATTERNS)


def is_verbatim_title(r: dict[str, Any]) -> bool:
    t = norm_cmp(r.get("title"))
    if not t:
        return False
    for c in (r.get("translation_literal"), r.get("source_excerpt"), translation_body(r), r.get("insight")):
        c = norm_cmp(c)
        if not c:
            continue
        if t == c or (len(t) >= 40 and c.startswith(t)):
            return True
    if word_count(t) >= 12 and re.search(r"[.!?]$", norm(r.get("title"))):
        return True
    return False


# --- authoring ---------------------------------------------------------------
SYSTEM = (
    "You are an editor for a cross-tradition contemplative anthology. You write TITLES.\n"
    "A good title is a THEMATIC CLAIM: a short phrase (3-8 words) that names the move or\n"
    "insight the passage makes. It is NOT a verse/section reference and NOT the passage\n"
    "sentence copied out.\n"
    "Rules:\n"
    "- 3-8 words, Title Case, no ending period, no quotation marks.\n"
    "- Name the idea/turn, do not summarize the whole sentence.\n"
    "- No verse numbers, no 'Yukti/Sutra/Fragment #', no bare references.\n"
    "- Ground it in THIS passage; be specific, not generic ('On Awareness' is too weak).\n"
    '- Return ONLY JSON: {"title": "..."}'
)


def _first(text: str, limit: int) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[#*_`>]", "", text or "")).strip()[:limit]


def build_prompt(r: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"Tradition: {r.get('work_title') or r.get('collection')}",
            f"Current (bad) title: {norm(r.get('title'))}",
            f"Passage: {_first(translation_body(r), 600) or '(none)'}",
            f"Commentary: {_first(commentary_body(r), 400) or '(none)'}",
            f"Themes: {', '.join(r.get('themes') or []) or '(none)'}",
            "",
            'Write the thematic-claim title. Return JSON: {"title": "..."}',
        ]
    )


def valid_title(new_title: str, r: dict[str, Any]) -> bool:
    t = norm(new_title)
    if not t or word_count(t) < 2 or word_count(t) > 10:
        return False
    if re.search(r"[.!?]$", t):
        return False
    if is_bare_title(t):
        return False
    probe = {**r, "title": t}
    if is_verbatim_title(probe):
        return False
    return True


async def _llm_title(r: dict[str, Any]) -> str:
    from app.llm import smart_chat

    text = (
        await smart_chat(
            [{"role": "system", "content": SYSTEM}, {"role": "user", "content": build_prompt(r)}],
            temperature=0.4,
        )
    ).strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        data = json.loads(text)
        return str(data.get("title") or "").strip()
    except Exception:
        return ""


async def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--work", help="restrict to a work_id substring")
    ap.add_argument("--concurrency", type=int, default=6)
    ap.add_argument("--retries", type=int, default=1)
    ap.add_argument("--out", default=str(ROOT / "scratch" / "titles_proposals.jsonl"))
    args = ap.parse_args()

    rows = [json.loads(l) for l in INDEX.read_text(encoding="utf-8").splitlines() if l.strip()]
    targets = [
        r
        for r in rows
        if (is_bare_title(r.get("title")) or is_verbatim_title(r))
        and (not args.work or args.work in str(r.get("work_id", "")))
    ]
    if args.limit:
        targets = targets[: args.limit]
    print(f"target units (bad titles): {len(targets)}")

    sem = asyncio.Semaphore(args.concurrency)
    records: list[dict[str, Any]] = []
    skipped = 0

    async def work(r: dict[str, Any]) -> None:
        nonlocal skipped
        new = ""
        async with sem:
            for _ in range(args.retries + 1):
                cand = await _llm_title(r)
                if valid_title(cand, r):
                    new = cand
                    break
        if not new:
            skipped += 1
            print(f"  [skip] {r['unit_id']}")
            return
        records.append({"unit_id": r["unit_id"], "set_fields": {"title": new}})
        print(f"  [ok]   {r['unit_id']}: {norm(r.get('title'))[:30]!r} -> {new!r}")

    await asyncio.gather(*(work(r) for r in targets))

    out_path = Path(args.out)
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n", encoding="utf-8")
    print(f"\nwrote {len(records)} title patches ({skipped} skipped) -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))

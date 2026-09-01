#!/usr/bin/env python3
"""Pick up to ten hero verses per collection and expand the mandala quote banks.

Writes data/listen_heroes.json. Updates web (and Lynx) heroQuotes.ts.
Collections with fewer than ten units are listed, not padded.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.data_loader import get_all_verses  # noqa: E402
from app.tts import _layer, _TTS_GATED_COLLECTIONS  # noqa: E402

TARGET = 10
HEROES_PATH = ROOT / "data" / "listen_heroes.json"
QUOTE_FILES = [
    ROOT / "web" / "src" / "lib" / "heroQuotes.ts",
    ROOT / "pratibha" / "src" / "lib" / "heroQuotes.ts",
]

_BANK_RE = re.compile(
    r"\{\s*pattern:\s*(/.*?/[a-z]*),\s*quotes:\s*\[(.*?)\],\s*\}",
    re.S,
)
_QUOTE_RE = re.compile(r'"((?:\\.|[^"\\])*)"')
_SENT_RE = re.compile(r"(?<=[.!?])\s+")
_WEAK_END = re.compile(
    r"\b(the|a|an|and|or|of|to|for|by|in|on|with|from|as|that|this|"
    r"we|he|she|it|is|are|be|than|which|when|then|into|onto)\.?$",
    re.I,
)


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (text or "").lower())


def _hay(verse: dict) -> str:
    return " ".join(
        str(verse.get(k) or "")
        for k in ("work_id", "work_title", "collection", "_id")
    )


def _work_id(verse: dict) -> str:
    return str(verse.get("work_id") or verse.get("collection") or "unknown").strip()


def parse_banks(path: Path) -> list[tuple[str, list[str]]]:
    text = path.read_text()
    banks: list[tuple[str, list[str]]] = []
    for match in _BANK_RE.finditer(text):
        pattern = match.group(1)
        quotes = [q.replace(r"\"", '"').replace(r"\\", "\\") for q in _QUOTE_RE.findall(match.group(2))]
        banks.append((pattern, quotes))
    return banks


def compile_pattern(raw: str) -> re.Pattern:
    body, _, flags = raw[1:].rpartition("/")
    flag = re.I if "i" in flags else 0
    return re.compile(body, flag)


def _usable_line(line: str, avoid: set[str]) -> bool:
    clean = re.sub(r"\s+", " ", line).strip().rstrip(";:—–,")
    if not clean.endswith((".", "?", "!")):
        clean = clean + "."
    if not (36 <= len(clean) <= 148):
        return False
    if _WEAK_END.search(clean.rstrip(".?!")):
        return False
    if clean.count(" ") < 5:
        return False
    if _norm(clean) in avoid:
        return False
    return True


def hero_line(verse: dict, avoid: set[str]) -> str:
    text = re.sub(r"\s+", " ", _layer(verse, "translation") or "").strip()
    parts = [p.strip() for p in _SENT_RE.split(text) if p.strip()]
    if not parts:
        parts = [text]
    candidates: list[str] = []
    for part in parts:
        line = part.rstrip(";:—–,")
        if not line.endswith((".", "?", "!")):
            line = line + "."
        if _usable_line(line, avoid):
            candidates.append(line)
        elif len(part) > 148:
            for chunk in re.split(r"[;:—–]", part):
                clause = chunk.strip()
                if not clause.endswith((".", "?", "!")):
                    clause = clause + "."
                if _usable_line(clause, avoid):
                    candidates.append(clause)
    if not candidates:
        return ""
    return min(candidates, key=lambda s: abs(len(s) - 90))


def quality(verse: dict, gated: bool) -> tuple:
    trans = _layer(verse, "translation")
    comm = _layer(verse, "commentary")
    prac = _layer(verse, "practice")
    mat = str(verse.get("editorial_maturity") or "").lower()
    mat_n = 3 if mat in {"publishable", "published", "canonical", "polished"} else 2 if mat else 1
    layers = sum(bool(x) for x in (trans, comm, prac))
    tlen = len(trans)
    quotable = 1 if 40 <= tlen <= 700 else 0
    key = 1 if verse.get("tts_key") else 0
    return (key if gated else 0, mat_n, layers, quotable, -abs(tlen - 280))


def match_quote(quote: str, rows: list[dict]) -> dict | None:
    nq = _norm(quote)
    if len(nq) < 12:
        return None
    best = None
    best_score = 0
    for verse in rows:
        hay = _norm(_layer(verse, "translation") + " " + str(verse.get("title") or ""))
        if not hay:
            continue
        if nq in hay:
            return verse
        # shared prefix / containment of a long stem
        stem = nq[:24]
        score = 2 if stem and stem in hay else 0
        if score > best_score:
            best, best_score = verse, score
    return best if best_score else None


def pick_spread(pool: list[dict], need: int) -> list[dict]:
    if need <= 0 or not pool:
        return []
    if len(pool) <= need:
        return list(pool)
    gated = _work_id(pool[0]) in _TTS_GATED_COLLECTIONS
    ordered = sorted(pool, key=lambda v: str(v.get("_id") or ""))
    index = {id(v): i for i, v in enumerate(ordered)}
    ranked = sorted(pool, key=lambda v: quality(v, gated), reverse=True)
    min_gap = max(1, len(pool) // (need * 2))
    picks: list[dict] = []
    for verse in ranked:
        pos = index[id(verse)]
        if any(abs(pos - index[id(other)]) < min_gap for other in picks):
            continue
        picks.append(verse)
        if len(picks) >= need:
            break
    if len(picks) < need:
        for verse in ranked:
            if verse in picks:
                continue
            picks.append(verse)
            if len(picks) >= need:
                break
    return picks


def select_for(rows: list[dict], quotes: list[str]) -> list[dict]:
    gated = _work_id(rows[0]) in _TTS_GATED_COLLECTIONS if rows else False
    eligible = [v for v in rows if _layer(v, "translation")]
    if gated:
        keyed = [v for v in eligible if v.get("tts_key")]
        if keyed:
            eligible = keyed
    used: set[str] = set()
    picked: list[dict] = []
    for quote in quotes:
        hit = match_quote(quote, eligible)
        if not hit:
            continue
        vid = str(hit.get("_id") or "")
        if vid in used:
            continue
        used.add(vid)
        picked.append(hit)
    rest = [v for v in eligible if str(v.get("_id") or "") not in used]
    need = max(0, min(TARGET, len(rows)) - len(picked))
    picked.extend(pick_spread(rest, need))
    return picked[:TARGET]


def rewrite_quotes_file(path: Path, quotes_by_pattern: dict[str, list[str]]) -> None:
    if not path.is_file():
        return
    text = path.read_text()
    text = text.replace(
        "Curated hero lines — four or five of the strongest sentences per text.",
        "Curated hero lines — up to ten of the strongest sentences per text.",
    )
    text = text.replace(".slice(0, 5)", ".slice(0, 10)")

    def repl(match: re.Match) -> str:
        pattern = match.group(1)
        quotes = quotes_by_pattern.get(pattern)
        if not quotes:
            return match.group(0)
        body = ",\n".join(f"      {json.dumps(q, ensure_ascii=False)}" for q in quotes)
        return "{\n    pattern: " + pattern + ",\n    quotes: [\n" + body + ",\n    ],\n  }"

    new, n = _BANK_RE.subn(repl, text)
    if n != len(quotes_by_pattern) and n == 0:
        print(f"  warning: no banks rewritten in {path}")
    path.write_text(new)
    print(f"  updated {path.relative_to(ROOT)} ({n} banks)")


def main() -> int:
    verses = get_all_verses()
    by_work: dict[str, list[dict]] = defaultdict(list)
    for verse in verses:
        by_work[_work_id(verse)].append(verse)

    banks = parse_banks(QUOTE_FILES[0])
    compiled = [(raw, compile_pattern(raw), quotes) for raw, quotes in banks]

    assigned: dict[str, tuple[str, list[str]]] = {}
    for work_id, rows in by_work.items():
        hay = _hay(rows[0])
        for raw, pat, quotes in compiled:
            if pat.search(hay) or pat.search(work_id):
                assigned[work_id] = (raw, quotes)
                break

    payload: dict[str, dict] = {}
    quotes_by_pattern: dict[str, list[str]] = {}
    short: list[tuple[str, int]] = []

    for work_id, rows in sorted(by_work.items()):
        raw, existing = assigned.get(work_id, ("", []))
        chosen = select_for(rows, existing)
        avoid = {_norm(q) for q in existing}
        extra: list[str] = []
        matched_ids = set()
        for quote in existing:
            hit = match_quote(quote, chosen)
            if hit:
                matched_ids.add(str(hit.get("_id") or ""))
        for verse in chosen:
            if str(verse.get("_id") or "") in matched_ids:
                continue
            line = hero_line(verse, avoid)
            if not line:
                continue
            extra.append(line)
            avoid.add(_norm(line))
        quotes = (existing + extra)[:TARGET]
        if raw and raw not in quotes_by_pattern:
            quotes_by_pattern[raw] = quotes
        elif raw and len(quotes) > len(quotes_by_pattern[raw]):
            quotes_by_pattern[raw] = quotes
        payload[work_id] = {
            "count": len(rows),
            "hero_count": len(chosen),
            "ids": [str(v.get("_id") or "") for v in chosen],
            "quotes": quotes,
            "short": len(rows) < TARGET,
        }
        if len(rows) < TARGET:
            short.append((work_id, len(rows)))

    HEROES_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {HEROES_PATH.relative_to(ROOT)} · {len(payload)} collections")
    print(f"Hero verses: {sum(len(v['ids']) for v in payload.values())}")
    if short:
        print("\nCollections with fewer than ten entries:")
        for work_id, n in short:
            print(f"  {work_id}: {n}")
    for path in QUOTE_FILES:
        rewrite_quotes_file(path, quotes_by_pattern)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Restore Devanagari Pali originals for Dhammapada canonical units.

Source (PD):
  V. Fausböll, The Dhammapada, 2nd ed. 1900 (Pali in Latin script).
  Digital text: ETCBC sources/pali.txt → data/raw_texts/pd/pali/dhammapada_fausboll_1900_pali.txt

Each unit already carries chapter-opening verses in Latin/IAST romanization
aligned to Müller SBE 10 English. This script:

  1. Parses Fausböll stanzas 1–423
  2. Matches each unit's numbered verses to Fausböll by number + similarity
  3. Keeps Latin/IAST in iast / sanskrit_iast
  4. Writes Devanagari (IAST→Devanagari) into original / sanskrit_devanagari
  5. Documents provenance and syncs index.jsonl (+ collection index)

    python scripts/restore_dhammapada_pali.py            # preview
    python scripts/restore_dhammapada_pali.py --write
"""
from __future__ import annotations

import argparse
import json
import re
import tempfile
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

import yaml
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical"
WORK = "dhammapada"
UNITS = CANONICAL / WORK
MAIN_INDEX = CANONICAL / "index.jsonl"
COLL_INDEX = UNITS / "index.jsonl"
FAUSBOLL = ROOT / "data" / "raw_texts" / "pd" / "pali" / "dhammapada_fausboll_1900_pali.txt"

PROV = (
    "pali: Fausböll 1900 (ETCBC transcription of PD Latin-script Pali); "
    "Devanagari via indic_transliteration from unit IAST; "
    "English alignment Müller SBE 10 1881"
)
SOURCE_REF = (
    "Pali: V. Fausböll, The Dhammapada, 2nd ed. (London: Luzac, 1900), "
    "PD Latin-script text via ETCBC etcbc/dhammapada sources/pali.txt "
    "(data/raw_texts/pd/pali/dhammapada_fausboll_1900_pali.txt). "
    "Devanagari restored by IAST→Devanagari transliteration of unit romanization "
    "after stanza-number match to Fausböll. English: F. Max Müller, SBE vol. 10 (1881)."
)

DEVA_RE = re.compile(r"[\u0900-\u097F]")
VERSE_RE = re.compile(r"\((\d+)\)\s*(.*?)(?=\(\d+\)|\Z)", re.S)
MIN_RATIO = 0.88


def parse_fausboll(path: Path) -> dict[int, str]:
    """Parse consecutively numbered stanzas from ETCBC Fausböll pali.txt."""
    raw = path.read_text(encoding="utf-8")
    verses: dict[int, str] = {}
    cur: int | None = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal cur, buf
        if cur is not None:
            verses[cur] = " ".join(buf).strip()
        cur = None
        buf = []

    for line in raw.splitlines():
        s = line.strip()
        # 143a / 143b variants in Fausböll
        m_ab = re.match(r"^(\d+)([ab])\s+(.+)$", s)
        if m_ab:
            n = int(m_ab.group(1))
            if cur is not None and cur != n:
                flush()
            if cur is None:
                cur = n
                buf = [m_ab.group(3)]
            else:
                buf.append(m_ab.group(3))
            continue
        m = re.match(r"^(\d+)\s+(.+)$", s)
        if m and 1 <= int(m.group(1)) <= 423:
            n = int(m.group(1))
            flush()
            cur = n
            buf = [m.group(2)]
            continue
        if cur is None:
            continue
        if re.match(r"^\d+\.\s+\S", s) or re.search(r"vaggo\s+\w+", s, re.I):
            flush()
            continue
        if s:
            buf.append(s)
    flush()
    return verses


def norm_pali(s: str) -> str:
    s = (s or "").lower()
    s = s.replace("â", "ā").replace("î", "ī").replace("û", "ū")
    s = s.replace("ê", "e").replace("ô", "o")
    s = s.replace("ṁ", "ṃ")
    s = re.sub(r"[\[\]]", "", s)
    s = re.sub(r"[“”\"'\-\.,;:!\?]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def verse_ratio(unit_body: str, fausboll: str) -> float:
    a, b = norm_pali(unit_body), norm_pali(fausboll)
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def extract_verses(iast: str) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for m in VERSE_RE.finditer(iast or ""):
        out.append((int(m.group(1)), m.group(2).strip()))
    return out


def to_devanagari_preserve_nums(iast: str) -> str:
    """IAST → Devanagari; keep ASCII (N) verse markers and spacing."""
    # Capture whitespace between ) and body so "(1) Foo" stays "(1) देव"
    verse_ws = re.compile(r"\((\d+)\)(\s*)(.*?)(?=\(\d+\)|\Z)", re.S)
    parts: list[str] = []
    pos = 0
    for m in verse_ws.finditer(iast):
        if m.start() > pos:
            prefix = iast[pos : m.start()]
            if re.search(r"[A-Za-zāīūṛṅñṭḍṇśṣṃṁḥ]", prefix):
                parts.append(_iast_chunk_to_deva(prefix))
            else:
                parts.append(prefix)
        num, ws, body = m.group(1), m.group(2), m.group(3)
        trailing = ""
        body_core = body
        mt = re.search(r"(\s+)\Z", body_core)
        if mt:
            trailing = mt.group(1)
            body_core = body_core[: mt.start()]
        # Prefer a single space after the marker when IAST had one.
        if not ws and body_core:
            ws = " "
        deva_body = _iast_chunk_to_deva(body_core) if body_core else ""
        parts.append(f"({num}){ws}{deva_body}{trailing}")
        pos = m.end()
    if pos < len(iast):
        tail = iast[pos:]
        if re.search(r"[A-Za-zāīūṛṅñṭḍṇśṣṃṁḥ]", tail):
            parts.append(_iast_chunk_to_deva(tail))
        else:
            parts.append(tail)
    return "".join(parts).strip()


def _iast_chunk_to_deva(chunk: str) -> str:
    s = chunk.replace("ṁ", "ṃ")
    return transliterate(s, sanscript.IAST, sanscript.DEVANAGARI)


def has_deva(s: str) -> bool:
    return bool(DEVA_RE.search(s or ""))


def upsert_layer(unit: dict[str, Any], kind: str, body: str, label: str, provenance: str) -> None:
    layers = unit.get("pratibha_layers")
    if not isinstance(layers, list):
        layers = []
        unit["pratibha_layers"] = layers
    existing = next((L for L in layers if isinstance(L, dict) and L.get("kind") == kind), None)
    if existing is None:
        existing = {"kind": kind, "label": label}
        order = [
            "original",
            "iast",
            "translation",
            "commentary",
            "key_terms",
            "resonances",
            "practice",
            "appendix",
        ]
        idx = order.index(kind) if kind in order else len(layers)
        pos = 0
        for i, L in enumerate(layers):
            k = L.get("kind")
            if k in order and order.index(k) <= idx:
                pos = i + 1
        layers.insert(pos, existing)
    existing["label"] = label
    existing["body"] = body
    existing["layer_provenance"] = provenance


def dump_yaml(unit: dict[str, Any]) -> str:
    return yaml.safe_dump(
        unit, allow_unicode=True, sort_keys=False, default_flow_style=False, width=100
    )


def atomic_write(path: Path, content: str) -> None:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(content)
        temp = Path(handle.name)
    temp.replace(path)


def sync_indexes(updated: dict[str, dict[str, Any]]) -> None:
    # collection index: rewrite from updated units in sorted unit_id order
    if COLL_INDEX.exists() or updated:
        lines = []
        for uid in sorted(updated):
            lines.append(json.dumps(updated[uid], ensure_ascii=False) + "\n")
        atomic_write(COLL_INDEX, "".join(lines))

    main_lines = MAIN_INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
    out: list[str] = []
    seen: set[str] = set()
    for line in main_lines:
        if not line.strip():
            out.append(line)
            continue
        obj = json.loads(line)
        uid = str(obj.get("unit_id") or "")
        if obj.get("work_id") == WORK or uid.startswith(f"{WORK}."):
            if uid in updated:
                out.append(json.dumps(updated[uid], ensure_ascii=False) + "\n")
                seen.add(uid)
            else:
                out.append(line)
        else:
            out.append(line)
    missing = set(updated) - seen
    for uid in sorted(missing):
        out.append(json.dumps(updated[uid], ensure_ascii=False) + "\n")
    atomic_write(MAIN_INDEX, "".join(out))


def layer_body(unit: dict[str, Any], kind: str) -> str:
    for L in unit.get("pratibha_layers") or []:
        if isinstance(L, dict) and L.get("kind") == kind:
            return str(L.get("body") or "")
    return ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true", help="Apply updates to YAML + indexes")
    ap.add_argument("--min-ratio", type=float, default=MIN_RATIO)
    args = ap.parse_args()

    if not FAUSBOLL.exists():
        raise SystemExit(f"missing Fausböll source: {FAUSBOLL}")

    fausboll = parse_fausboll(FAUSBOLL)
    print(f"fausboll_verses={len(fausboll)} (expect ~423)")

    paths = sorted(UNITS.glob("dhammapada_dhp_ch*.yml"))
    before = after = 0
    unmatched: list[str] = []
    plans: list[dict[str, Any]] = []

    for path in paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        uid = str(data.get("unit_id") or path.stem)
        iast = str(data.get("sanskrit_iast") or layer_body(data, "iast") or "")
        orig = layer_body(data, "original") or str(data.get("sanskrit_devanagari") or "")
        if has_deva(orig):
            before += 1

        verses = extract_verses(iast)
        if not verses:
            unmatched.append(f"{uid}: no numbered verses in IAST")
            continue

        bad: list[str] = []
        scores: list[float] = []
        for n, body in verses:
            fb = fausboll.get(n)
            if not fb:
                bad.append(f"v{n} missing in Fausböll parse")
                continue
            r = verse_ratio(body, fb)
            scores.append(r)
            if r < args.min_ratio:
                bad.append(f"v{n} ratio={r:.2f} < {args.min_ratio}")

        if bad:
            unmatched.append(f"{uid}: " + "; ".join(bad))
            continue

        deva = to_devanagari_preserve_nums(iast)
        if not has_deva(deva):
            unmatched.append(f"{uid}: transliteration produced no Devanagari")
            continue

        plans.append(
            {
                "path": path,
                "uid": uid,
                "data": data,
                "iast": iast,
                "deva": deva,
                "verses": [n for n, _ in verses],
                "min_score": min(scores) if scores else 0.0,
            }
        )

    print(f"units={len(paths)} before_deva={before}")
    print(f"matched={len(plans)} unmatched={len(unmatched)}")
    for u in unmatched:
        print("  UNMATCHED", u)
    for p in plans:
        print(
            f"  {p['uid']}: vv={p['verses']} min_fausboll_ratio={p['min_score']:.2f} "
            f"deva_chars={len(DEVA_RE.findall(p['deva']))}"
        )

    if not args.write:
        print("dry-run only; pass --write to apply")
        return 0 if not unmatched else 1

    updated: dict[str, dict[str, Any]] = {}
    for plan in plans:
        data = plan["data"]
        deva = plan["deva"]
        iast = plan["iast"]
        upsert_layer(data, "original", deva, "Original", "sourced")
        upsert_layer(data, "iast", iast, "IAST", "sourced")
        data["sanskrit_devanagari"] = deva
        data["sanskrit_iast"] = iast
        prov = dict(data.get("provenance") or {})
        prov["source_reference"] = SOURCE_REF
        data["provenance"] = prov
        # optional top-level note used by some restores
        lp = data.get("layer_provenance")
        if isinstance(lp, dict):
            lp["original"] = PROV
            data["layer_provenance"] = lp

        atomic_write(plan["path"], dump_yaml(data))
        updated[plan["uid"]] = data
        if has_deva(deva):
            after += 1

    sync_indexes(updated)
    print(f"wrote {len(updated)} YAML units; synced index.jsonl + collection index")
    print(f"coverage Devanagari original: before={before} after={after} / {len(paths)}")
    return 0 if after == len(paths) and not unmatched else 1


if __name__ == "__main__":
    raise SystemExit(main())

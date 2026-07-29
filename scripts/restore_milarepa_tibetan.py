#!/usr/bin/env python3
"""Restore Tibetan Unicode originals for milarepa_songs pilot units.

Source:
  Editorial Wylie under data/raw_texts/pd/tibetan/milarepa_songs_wylie_restore.yml
  (Jetsün-Kahbum song-cycle refrains; English locator = Evans-Wentz 1928 PD).
  Converted EWTS → Unicode Tibetan with pyewts.

Matching is by source_id / unit_id (MIL_* ↔ milarepa_songs.mil_*).

Updates:
  - data/canonical/milarepa_songs/*.yml  (pratibha_layers original/iast,
    sanskrit_devanagari / sanskrit_iast, layer provenance)
  - data/canonical/index.jsonl           (milarepa_songs rows only)
  - data/canonical/milarepa_songs/index.jsonl (if present)

Does not touch other collections. Does not commit.

    python scripts/restore_milarepa_tibetan.py            # preview
    python scripts/restore_milarepa_tibetan.py --write
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "data" / "canonical" / "milarepa_songs"
MAIN_INDEX = ROOT / "data" / "canonical" / "index.jsonl"
COLL_INDEX = CANON / "index.jsonl"
WYLIE_SRC = ROOT / "data" / "raw_texts" / "pd" / "tibetan" / "milarepa_songs_wylie_restore.yml"

PROV = (
    "tibetan: Jetsün-Kahbum / rje btsun mi la ras pa'i rnam thar song-cycle "
    "editorial Wylie → Unicode (EWTS/pyewts); English locator Evans-Wentz 1928 "
    "PD (data/raw_texts/pd/tibetan/milarepa_evans_wentz_1928.txt + "
    "milarepa_songs_wylie_restore.yml). Not a critical xylograph edition."
)

TIB_RE = re.compile(r"[\u0F00-\u0FFF]")
PILOT_SLUGS = (
    "mil_sorrow_001",
    "mil_zeal_002",
    "mil_wisdom_003",
    "mil_reproof_004",
    "mil_comforts_005",
    "mil_sister_006",
    "mil_race_007",
    "mil_demon_008",
    "mil_satis_009",
    "mil_inter_010",
    "mil_maiden_011",
    "mil_world_012",
    "mil_shame_013",
    "mil_illness_014",
)


def tib_count(text: str) -> int:
    return len(TIB_RE.findall(text or ""))


def has_native_tibetan(text: str, min_chars: int = 20) -> bool:
    """True if text has enough Tibetan and is not a fake phonetic stub."""
    if tib_count(text) < min_chars:
        return False
    # Corrupted stubs map English metadata into Uchen letters; reject short
    # gibberish that still contains Latin leftovers like "Eབ༹".
    if re.search(r"[A-Za-z]", text) and tib_count(text) < 120:
        return False
    if "Source-language basis" in (text or "") or "not line-aligned" in (text or "").lower():
        return False
    return True


def normalize_wylie(raw: str) -> str:
    lines: list[str] = []
    for line in (raw or "").splitlines():
        s = line.strip()
        if not s:
            lines.append("")
            continue
        # Drop trailing shad-like / already present
        s = s.rstrip("/").strip()
        lines.append(s)
    # Collapse excess blank lines
    out: list[str] = []
    blank = False
    for line in lines:
        if not line:
            if not blank:
                out.append("")
            blank = True
        else:
            out.append(line)
            blank = False
    return "\n".join(out).strip() + "\n"


def wylie_to_tibetan(wylie: str, converter: Any) -> str:
    """Convert EWTS Wylie lines to Unicode Tibetan; append shad per verse line."""
    out_lines: list[str] = []
    for line in normalize_wylie(wylie).splitlines():
        if not line.strip():
            out_lines.append("")
            continue
        # Already Tibetan? keep
        if tib_count(line) >= max(4, len(line) // 4):
            t = line.rstrip("།/ ").strip()
            out_lines.append(t + "།" if t else "")
            continue
        try:
            tib = converter.toUnicode(line)
        except Exception as exc:  # noqa: BLE001
            raise ValueError(f"pyewts failed on {line!r}: {exc}") from exc
        tib = (tib or "").strip()
        if not tib:
            continue
        if not tib.endswith("།"):
            tib += "།"
        out_lines.append(tib)
    # tidy blank runs
    cleaned: list[str] = []
    blank = False
    for line in out_lines:
        if not line:
            if not blank:
                cleaned.append("")
            blank = True
        else:
            cleaned.append(line)
            blank = False
    return "\n".join(cleaned).strip() + "\n"


def load_wylie_map() -> dict[str, dict[str, str]]:
    raw = yaml.safe_load(WYLIE_SRC.read_text(encoding="utf-8"))
    units = raw.get("units") or {}
    out: dict[str, dict[str, str]] = {}
    for sid, meta in units.items():
        w = normalize_wylie(meta.get("wylie") or "")
        if not w.strip():
            raise ValueError(f"empty wylie for {sid}")
        out[sid] = {
            "title": str(meta.get("title") or ""),
            "ew_anchor": str(meta.get("ew_anchor") or ""),
            "wylie": w,
        }
    return out


def get_converter() -> Any:
    try:
        import pyewts  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "pyewts is required. Create a venv and: pip install pyewts\n"
            f"Import error: {exc}"
        ) from exc
    return pyewts.pyewts()


def upsert_layer(
    unit: dict[str, Any],
    kind: str,
    body: str,
    label: str,
    provenance: str,
) -> None:
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
            k = L.get("kind") if isinstance(L, dict) else None
            if k in order and order.index(k) <= idx:
                pos = i + 1
        layers.insert(pos, existing)
    existing["label"] = label
    existing["body"] = body.rstrip() + "\n" if body and not body.endswith("\n") else body
    # Keep compact single-line bodies without forced trailing newline for short notes
    if kind == "iast":
        existing["body"] = body.strip() + "\n"
    existing["layer_provenance"] = provenance


def set_top_provenance(unit: dict[str, Any], note: str) -> None:
    prov = unit.get("layer_provenance")
    if not isinstance(prov, dict):
        unit["layer_provenance"] = {"original": note}
    else:
        prov["original"] = note
    top = unit.get("provenance")
    if isinstance(top, dict):
        ref = str(top.get("source_reference") or "")
        if "Evans-Wentz" not in ref and "Jetsün" not in ref and "tibetan:" not in ref:
            tip = "Evans-Wentz 1928 PD English locator; Tibetan editorial Wylie→Unicode (see layer_provenance)."
            top["source_reference"] = f"{ref}; {tip}".strip("; ") if ref else tip


def dump_yaml(unit: dict[str, Any]) -> str:
    return yaml.safe_dump(
        unit, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120
    )


def atomic_write(path: Path, content: str) -> None:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(content)
        temp = Path(handle.name)
    temp.replace(path)


def unit_english(data: dict[str, Any]) -> str:
    layers = {L.get("kind"): L for L in (data.get("pratibha_layers") or []) if isinstance(L, dict)}
    for key in ("translation",):
        body = (layers.get(key) or {}).get("body") or ""
        if body.strip():
            return body
    return str(data.get("translation_literal") or data.get("title") or "")


def verify_match(sid: str, meta: dict[str, str], data: dict[str, Any]) -> str | None:
    """Return warning string if title/English look mismatched; None if ok."""
    want = (meta.get("title") or "").lower()
    have = (data.get("title") or data.get("unit_label") or "").lower()
    # Soft check: share a distinctive token
    tokens = {t for t in re.split(r"[^a-z]+", want) if len(t) > 4}
    if tokens and not any(t in have for t in tokens):
        # also check translation
        en = unit_english(data).lower()
        if not any(t in en for t in tokens):
            return f"title mismatch? source title={meta.get('title')!r} unit={data.get('title')!r}"
    return None


def apply_to_unit(data: dict[str, Any], tibetan: str, wylie: str) -> None:
    upsert_layer(data, "original", tibetan.rstrip() + "\n", "Original (Tibetan)", PROV)
    upsert_layer(data, "iast", wylie.rstrip() + "\n", "Wylie", PROV)
    data["sanskrit_devanagari"] = tibetan.rstrip() + "\n"
    data["sanskrit_iast"] = wylie.rstrip() + "\n"
    set_top_provenance(data, PROV)


def sync_index_row(row: dict[str, Any], tibetan: str, wylie: str) -> None:
    apply_to_unit(row, tibetan, wylie)


def count_coverage(paths: list[Path]) -> tuple[int, int]:
    good = 0
    for path in paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        layers = {L.get("kind"): L for L in (data.get("pratibha_layers") or []) if isinstance(L, dict)}
        orig = (layers.get("original") or {}).get("body") or ""
        sd = data.get("sanskrit_devanagari") or ""
        if has_native_tibetan(orig) or has_native_tibetan(sd):
            # Prefer original-layer Tibetan for "after" reporting
            if has_native_tibetan(orig) or has_native_tibetan(sd):
                good += 1
    return good, len(paths)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true", help="Apply changes (default: dry-run)")
    args = ap.parse_args()

    if not WYLIE_SRC.is_file():
        print(f"missing Wylie source: {WYLIE_SRC}", file=sys.stderr)
        return 1

    converter = get_converter()
    wylie_map = load_wylie_map()

    paths = [CANON / f"milarepa_songs_{slug}.yml" for slug in PILOT_SLUGS]
    missing_files = [p for p in paths if not p.is_file()]
    if missing_files:
        print("missing canonical YAML:", *[p.name for p in missing_files], sep="\n  ")
        return 1

    before, total = count_coverage(paths)
    # Stricter before: original layer specifically
    before_orig = 0
    for path in paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        layers = {L.get("kind"): L for L in (data.get("pratibha_layers") or []) if isinstance(L, dict)}
        if has_native_tibetan((layers.get("original") or {}).get("body") or ""):
            before_orig += 1

    plans: list[dict[str, Any]] = []
    unmatched: list[str] = []
    warnings: list[str] = []

    for path in paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        sid = str(data.get("source_id") or "").upper()
        # normalize mil_ew style
        if not sid.startswith("MIL_"):
            # derive from unit_id
            uid = str(data.get("unit_id") or "")
            m = re.search(r"\.(mil_[a-z0-9_]+)$", uid)
            if m:
                sid = m.group(1).upper()
        if sid not in wylie_map:
            unmatched.append(str(data.get("unit_id")))
            continue
        meta = wylie_map[sid]
        warn = verify_match(sid, meta, data)
        if warn:
            warnings.append(f"{sid}: {warn}")
        tib = wylie_to_tibetan(meta["wylie"], converter)
        if not has_native_tibetan(tib):
            unmatched.append(f"{data.get('unit_id')} (conversion produced insufficient Tibetan)")
            continue
        plans.append(
            {
                "path": path,
                "uid": data["unit_id"],
                "sid": sid,
                "tibetan": tib,
                "wylie": meta["wylie"],
                "title": meta.get("title"),
            }
        )

    print(f"pilot_units={total}")
    print(f"before_native_tibetan (orig layer)={before_orig}/{total}")
    print(f"before_native_tibetan (orig|sd)={before}/{total}")
    print(f"planned={len(plans)} unmatched={len(unmatched)}")
    if unmatched:
        print("unmatched:")
        for u in unmatched:
            print(" ", u)
    if warnings:
        print("warnings:")
        for w in warnings:
            print(" ", w)
    for p in plans:
        print(f"  {p['sid']}: tib_chars={tib_count(p['tibetan'])} ← {p['title']}")

    if not args.write:
        print("dry-run only; pass --write to apply")
        return 0

    # Load main index
    index_lines = MAIN_INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
    index_units = [json.loads(line) for line in index_lines if line.strip()]
    by_uid = {u["unit_id"]: i for i, u in enumerate(index_units)}

    coll_lines: list[str] | None = None
    coll_units: list[dict[str, Any]] | None = None
    coll_by_uid: dict[str, int] = {}
    if COLL_INDEX.is_file():
        coll_lines = COLL_INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
        coll_units = [json.loads(line) for line in coll_lines if line.strip()]
        coll_by_uid = {u["unit_id"]: i for i, u in enumerate(coll_units)}

    updated = 0
    for plan in plans:
        path: Path = plan["path"]
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        apply_to_unit(data, plan["tibetan"], plan["wylie"])
        atomic_write(path, dump_yaml(data))

        uid = plan["uid"]
        if uid in by_uid:
            idx = by_uid[uid]
            sync_index_row(index_units[idx], plan["tibetan"], plan["wylie"])
            index_lines[idx] = json.dumps(index_units[idx], ensure_ascii=False) + "\n"
        if coll_units is not None and coll_lines is not None and uid in coll_by_uid:
            cidx = coll_by_uid[uid]
            sync_index_row(coll_units[cidx], plan["tibetan"], plan["wylie"])
            coll_lines[cidx] = json.dumps(coll_units[cidx], ensure_ascii=False) + "\n"
        updated += 1

    atomic_write(MAIN_INDEX, "".join(index_lines))
    if coll_lines is not None:
        atomic_write(COLL_INDEX, "".join(coll_lines))

    after_orig = 0
    for path in paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        layers = {L.get("kind"): L for L in (data.get("pratibha_layers") or []) if isinstance(L, dict)}
        if has_native_tibetan((layers.get("original") or {}).get("body") or ""):
            after_orig += 1

    # Index coverage (deva field)
    idx_tib = 0
    for line in MAIN_INDEX.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("work_id") != "milarepa_songs":
            continue
        if has_native_tibetan(row.get("sanskrit_devanagari") or "") or has_native_tibetan(
            next(
                (
                    L.get("body") or ""
                    for L in (row.get("pratibha_layers") or [])
                    if isinstance(L, dict) and L.get("kind") == "original"
                ),
                "",
            )
        ):
            idx_tib += 1

    print(f"wrote {updated} YAML units; synchronized index.jsonl")
    print(f"after_native_tibetan (orig layer)={after_orig}/{total}")
    print(f"index milarepa rows with Tibetan≈{idx_tib}/14")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

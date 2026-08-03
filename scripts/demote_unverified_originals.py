#!/usr/bin/env python3
"""Restore or demote units flagged UNVERIFIED by PD phrase-match.

For a few known near-misses, restore the PD witness text as the original.
For the rest: withdraw the unverified source-language fields, keep the English
translation as an editorial rendering, and mark provenance honestly.

  python scripts/demote_unverified_originals.py          # write
  python scripts/demote_unverified_originals.py --dry-run
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "data" / "canonical"
PD = ROOT / "data" / "raw_texts" / "pd"

REMOVED = (
    "ORIGINAL_REMOVED — source-language text withdrawn after failing PD phrase-match; "
    "English translation retained as an editorial rendering (may be modernized/poetic). "
    "Not a verbatim quotation of a verified original."
)

# unit_id -> (relative PD path, how to extract)
RESTORES: dict[str, tuple[str, str]] = {
    # Ganjoor Ney-Nāme opening (first two hemistichs as one couplet pair)
    "rumi_mathnawi_yi_manawi.mth_001": (
        "persian/mathnawi_neynameh_ganjoor.txt",
        "first_lines:2",
    ),
    "rumi_mathnawi_yi_manawi.mth_005": (
        "persian/mathnawi_elephant_dark_masnavi_net.txt",
        "first_lines:4",
    ),
}


def extract_pd(rel: str, mode: str) -> str:
    text = (PD / rel).read_text(encoding="utf-8", errors="replace").strip()
    if mode.startswith("first_lines:"):
        n = int(mode.split(":")[1])
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        return "\n".join(lines[:n])
    return text


def find_unverified() -> list[Path]:
    out: list[Path] = []
    for p in CANON.rglob("*.yml"):
        try:
            d = yaml.safe_load(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        prov = d.get("provenance") or {}
        if not isinstance(prov, dict):
            continue
        rel = str(prov.get("original_reliability", ""))
        ver = str(prov.get("verification", ""))
        if "UNVERIFIED" in rel or "PD phrase-match: miss" in ver or "ORIGINAL_REMOVED" in rel:
            # skip already demoted cleanly
            if "ORIGINAL_REMOVED" in rel and not (d.get("sanskrit_devanagari") or d.get("sanskrit_iast")):
                continue
            out.append(p)
    return sorted(out)


def demote(d: dict) -> None:
    d["sanskrit_devanagari"] = ""
    d["sanskrit_iast"] = ""
    # Clear misused original fields if present
    for k in ("tibetan_uchen", "original"):
        if k in d and isinstance(d[k], str) and d[k].strip():
            # only clear if it was the unverified original store — keep real tibetan if separate
            pass
    layers = d.get("pratibha_layers")
    if isinstance(layers, list):
        for L in layers:
            if isinstance(L, dict) and L.get("kind") in ("original", "iast"):
                L["body"] = ""
                L["content"] = ""
    prov = d.get("provenance") if isinstance(d.get("provenance"), dict) else {}
    prov["original_reliability"] = REMOVED
    prov["original_source"] = (
        "Withdrawn — previous model-supplied original failed PD phrase-match against "
        "local public-domain witness."
    )
    ver = str(prov.get("verification", ""))
    if "original withdrawn" not in ver:
        prov["verification"] = f"{ver}; original withdrawn after PD miss".strip("; ")
    prov["source_confidence"] = "low"
    d["provenance"] = prov
    if d.get("editorial_maturity") in ("rich", "standard", "complete", "strong_draft"):
        d["editorial_maturity"] = "draft"


def restore(d: dict, text: str, pd_rel: str) -> None:
    d["sanskrit_devanagari"] = text
    # Keep iast empty for non-Sanskrit restores (Persian etc.)
    if re.search(r"[\u0900-\u097F]", text):
        pass  # leave existing iast if any; don't invent
    else:
        d["sanskrit_iast"] = d.get("sanskrit_iast") or ""
    prov = d.get("provenance") if isinstance(d.get("provenance"), dict) else {}
    prov["original_reliability"] = "PD_RESTORED — original replaced from local public-domain witness."
    prov["original_source"] = f"Restored from data/raw_texts/pd/{pd_rel}"
    prov["verification"] = "PD restore after phrase-match miss"
    prov["source_confidence"] = "medium"
    note = str(prov.get("verification_note", ""))
    prov["verification_note"] = (
        f"Restored from {pd_rel}. Prior model-supplied original withdrawn. {note}"
    )[:500]
    d["provenance"] = prov


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    paths = find_unverified()
    restored = demoted = 0
    for path in paths:
        d = yaml.safe_load(path.read_text(encoding="utf-8"))
        uid = d.get("unit_id") or path.stem
        if uid in RESTORES:
            rel, mode = RESTORES[uid]
            text = extract_pd(rel, mode)
            print(f"RESTORE {uid} ← {rel}")
            if not args.dry_run:
                restore(d, text, rel)
                path.write_text(
                    yaml.safe_dump(d, allow_unicode=True, sort_keys=False, width=120),
                    encoding="utf-8",
                )
            restored += 1
        else:
            print(f"DEMOTE  {uid}")
            if not args.dry_run:
                demote(d)
                path.write_text(
                    yaml.safe_dump(d, allow_unicode=True, sort_keys=False, width=120),
                    encoding="utf-8",
                )
            demoted += 1

    print(f"\nDone. restored={restored} demoted={demoted} dry_run={args.dry_run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

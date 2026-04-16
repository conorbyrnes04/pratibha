#!/usr/bin/env python3
"""
Auto-enrich YAML units toward a "Siva Sutra gold standard" baseline.

What it does:
- normalizes title/translation/commentary whitespace
- removes duplicate commentary that mirrors translation
- generates concise micro-commentary when missing
- ensures abhyasa and modes.sadhana are present and practical
- adds lightweight themes
- writes a QA summary report

Usage:
  python scripts/enrich_yaml_shiva_style.py --input-dir data/yaml/fragments
  python scripts/enrich_yaml_shiva_style.py --input-dir data/yaml/fragments --dry-run
  python scripts/enrich_yaml_shiva_style.py --all-yaml
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent.parent


def _txt(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, str):
        return v.strip()
    return str(v).strip()


def _normalize_ws(s: str) -> str:
    s = s.replace("\r", "\n")
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in s.split("\n")]
    out: list[str] = []
    blank = False
    for ln in lines:
        if not ln:
            if not blank:
                out.append("")
            blank = True
            continue
        out.append(ln)
        blank = False
    return "\n".join(out).strip()


def _first_sentence(s: str, max_len: int = 96) -> str:
    s = _normalize_ws(_txt(s))
    if not s:
        return ""
    first = re.split(r"(?<=[.!?])\s+", s)[0].strip()
    first = re.sub(r"\s+", " ", first)
    if len(first) > max_len:
        return first[: max_len - 3].rstrip() + "..."
    return first


def _norm_cmp(s: str) -> str:
    return re.sub(r"\W+", " ", _txt(s).lower()).strip()


THEME_KEYWORDS: list[tuple[str, tuple[str, ...]]] = [
    ("awareness", ("awareness", "witness", "presence", "mindful")),
    ("consciousness", ("consciousness", "self", "knowing", "recognition")),
    ("nonduality", ("nondual", "oneness", "unity", "one")),
    ("practice", ("practice", "discipline", "exercise", "abhyasa")),
    ("speech", ("word", "speech", "language", "logos", "mantra")),
    ("change", ("change", "becoming", "flow", "transformation", "fire")),
    ("ethics", ("virtue", "justice", "conduct", "character")),
    ("suffering", ("suffering", "pain", "conflict", "strife")),
]


def infer_themes(*parts: str) -> list[str]:
    blob = " ".join(_txt(p).lower() for p in parts)
    out: list[str] = []
    for theme, words in THEME_KEYWORDS:
        if any(w in blob for w in words):
            out.append(theme)
    return out[:6]


def micro_commentary(translation: str) -> str:
    t = _txt(translation).lower()
    if any(k in t for k in ("word", "logos", "language", "speech")):
        return "This line points to a deeper order that is received through attentive listening rather than conceptual noise."
    if any(k in t for k in ("fire", "change", "flow", "becoming")):
        return "The teaching frames change as lawful and intelligible, inviting steadiness within transformation."
    if any(k in t for k in ("self", "awareness", "consciousness", "mind")):
        return "The emphasis turns inward: clarity grows when attention returns to the knower rather than the passing content."
    if any(k in t for k in ("conflict", "strife", "opposite", "war")):
        return "Opposition is treated as a dynamic tension that can reveal hidden harmony when seen without reactivity."
    return "Read this line as a contemplative pointer: pause interpretation for a moment and let the insight disclose itself directly."


def suggest_abhyasa(translation: str, commentary: str) -> str:
    b = f"{_txt(translation)} {_txt(commentary)}".lower()
    if any(k in b for k in ("breath", "inhale", "exhale")):
        return "Sit for 3 minutes with natural breathing. At each inhale and exhale, notice awareness before naming experience."
    if any(k in b for k in ("word", "speech", "language", "logos", "mantra")):
        return "For 2 minutes, observe inner speech as sound only. Return to the silent awareness that hears it."
    if any(k in b for k in ("action", "character", "conduct", "virtue")):
        return "Choose one ordinary action today and perform it without haste or self-narration. End with one breath of gratitude."
    return "Read this passage slowly three times. Pause for one minute and write one sentence about how to apply it today."


def ensure_modes(value: Any) -> dict[str, str]:
    if isinstance(value, dict):
        modes = {k: _txt(v) for k, v in value.items()}
    else:
        modes = {}
    for k in ("bhasya", "doctrinal", "comparative", "sadhana"):
        modes.setdefault(k, "")
    return modes


def enrich_record(item: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    changes: list[str] = []
    y = dict(item)

    translation = _normalize_ws(_txt(y.get("translation")))
    commentary = _normalize_ws(_txt(y.get("commentary")))
    title = _txt(y.get("title"))

    if not title:
        y["title"] = _first_sentence(translation) or _txt(y.get("sutra_id")) or "Untitled"
        changes.append("title_generated")
    else:
        clean_title = _normalize_ws(title)
        if clean_title != title:
            y["title"] = clean_title
            changes.append("title_normalized")

    if _norm_cmp(commentary) and _norm_cmp(commentary) == _norm_cmp(translation):
        commentary = ""
        changes.append("commentary_duplicate_removed")

    if not commentary and translation:
        commentary = micro_commentary(translation)
        changes.append("commentary_generated")

    if translation != _txt(y.get("translation")):
        y["translation"] = translation
        changes.append("translation_normalized")
    if commentary != _txt(y.get("commentary")):
        y["commentary"] = commentary
        changes.append("commentary_normalized")

    abhyasa = _txt(y.get("abhyasa"))
    if not abhyasa:
        y["abhyasa"] = suggest_abhyasa(translation, commentary)
        changes.append("abhyasa_generated")

    modes = ensure_modes(y.get("modes"))
    if not modes.get("sadhana", "").strip():
        modes["sadhana"] = y.get("abhyasa", "")
        changes.append("modes_sadhana_filled")
    y["modes"] = modes

    if not isinstance(y.get("themes"), list) or not y.get("themes"):
        themes = infer_themes(y.get("title", ""), translation, commentary)
        if themes:
            y["themes"] = themes
            changes.append("themes_generated")

    y.setdefault("voice_of_siva", _txt(y.get("voice_of_siva")))
    y.setdefault("glossary", y.get("glossary") if isinstance(y.get("glossary"), list) else [])
    return y, changes


def _quality_score(qa: dict[str, Any]) -> int:
    total = int(qa.get("total_files", 0)) or 1
    missing_translation = int(qa.get("issues", {}).get("missing_translation", 0))
    empty_commentary = int(qa.get("issues", {}).get("empty_commentary", 0))
    missing_abhyasa = int(qa.get("issues", {}).get("missing_abhyasa", 0))
    penalty = (
        (missing_translation / total) * 45
        + (empty_commentary / total) * 35
        + (missing_abhyasa / total) * 20
    )
    return max(0, min(100, int(round(100 - penalty))))


def _contains_devanagari(s: str) -> bool:
    return bool(re.search(r"[\u0900-\u097F]", s or ""))


def _unit_quality(enriched: dict[str, Any]) -> int:
    score = 100
    if not _txt(enriched.get("translation")):
        score -= 55
    if not _txt(enriched.get("commentary")):
        score -= 20
    if not _txt(enriched.get("abhyasa")):
        score -= 15
    themes = enriched.get("themes")
    if not isinstance(themes, list) or len(themes) == 0:
        score -= 10
    return max(0, min(100, score))


def run_collection(input_dir: Path, dry_run: bool) -> tuple[int, dict[str, Any] | None]:
    files = sorted(list(input_dir.glob("*.yml")) + list(input_dir.glob("*.yaml")))
    if not files:
        print(f"No YAML files found in {input_dir}")
        return 1, None

    changed = 0
    totals: dict[str, int] = {}
    collection_name = input_dir.name
    qa: dict[str, Any] = {
        "collection": collection_name,
        "input_dir": str(input_dir),
        "total_files": len(files),
        "changed_files": 0,
        "changes_by_type": {},
        "issues": {"missing_translation": 0, "empty_commentary": 0, "missing_abhyasa": 0},
    }
    qa_failures: list[dict[str, Any]] = []

    for fp in files:
        raw = yaml.safe_load(fp.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            continue
        enriched, changes = enrich_record(raw)
        enriched["quality_score_unit"] = _unit_quality(enriched)
        if changes:
            changed += 1
            for c in changes:
                totals[c] = totals.get(c, 0) + 1
            if not dry_run:
                fp.write_text(
                    yaml.safe_dump(enriched, allow_unicode=True, sort_keys=False, default_flow_style=False),
                    encoding="utf-8",
                )

        # QA counters post-enrichment
        if not _txt(enriched.get("translation")):
            qa["issues"]["missing_translation"] += 1
        if not _txt(enriched.get("commentary")):
            qa["issues"]["empty_commentary"] += 1
        if not _txt(enriched.get("abhyasa")):
            qa["issues"]["missing_abhyasa"] += 1

        translation = _txt(enriched.get("translation"))
        themes = enriched.get("themes")
        has_themes = isinstance(themes, list) and len(themes) > 0
        has_abhyasa = bool(_txt(enriched.get("abhyasa")))
        devanagari_present = _contains_devanagari(_txt(enriched.get("sanskrit"))) or _contains_devanagari(translation)
        unit_row = {
            "file": fp.name,
            "sutra_id": _txt(enriched.get("sutra_id")),
            "body_word_count": len(re.findall(r"\b[\w'-]+\b", translation)),
            "has_translation": bool(translation),
            "has_themes": has_themes,
            "has_abhyasa": has_abhyasa,
            "translation_devanagari_present": devanagari_present,
            "quality_score": int(enriched.get("quality_score_unit", 0)),
        }
        if int(unit_row["quality_score"]) < 70:
            qa_failures.append(unit_row)

    qa["changed_files"] = changed
    qa["changes_by_type"] = totals
    qa["quality_score"] = _quality_score(qa)

    print(f"Scanned {len(files)} files in {input_dir} [{collection_name}]")
    print(f"Changed {changed} files{' (dry-run)' if dry_run else ''}")
    for k in sorted(totals.keys()):
        print(f"  - {k}: {totals[k]}")
    print("QA:")
    for k, v in qa["issues"].items():
        print(f"  - {k}: {v}")
    print(f"  - quality_score: {qa['quality_score']}/100")

    failures_csv = input_dir / "_qa_failures.csv"
    if qa_failures:
        with failures_csv.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(
                f,
                fieldnames=[
                    "file",
                    "sutra_id",
                    "body_word_count",
                    "has_translation",
                    "has_themes",
                    "has_abhyasa",
                    "translation_devanagari_present",
                    "quality_score",
                ],
            )
            w.writeheader()
            w.writerows(qa_failures)
    elif failures_csv.exists() and not dry_run:
        failures_csv.unlink()

    return 0, qa


def run(input_dir: Path, dry_run: bool, report_path: Path | None) -> int:
    code, qa = run_collection(input_dir=input_dir, dry_run=dry_run)
    if code != 0 or qa is None:
        return code
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(qa, indent=2), encoding="utf-8")
        print(f"Report written to {report_path}")
    return code


def _list_yaml_collections(yaml_root: Path) -> list[Path]:
    if not yaml_root.exists():
        return []
    out: list[Path] = []
    for p in sorted(yaml_root.iterdir()):
        if not p.is_dir():
            continue
        has_yaml = any(p.glob("*.yml")) or any(p.glob("*.yaml"))
        if has_yaml:
            out.append(p)
    return out


def run_all(yaml_root: Path, dry_run: bool, report_path: Path | None) -> int:
    collections = _list_yaml_collections(yaml_root)
    if not collections:
        print(f"No YAML collections found under {yaml_root}")
        return 1

    scorecard: list[dict[str, Any]] = []
    failures = 0
    for cdir in collections:
        print(f"\n=== Enriching {cdir.name} ===")
        code, qa = run_collection(input_dir=cdir, dry_run=dry_run)
        if code != 0 or qa is None:
            failures += 1
            continue
        scorecard.append(qa)

    # Rank by quality then collection name.
    scorecard.sort(key=lambda x: (-int(x.get("quality_score", 0)), str(x.get("collection", ""))))
    print("\n=== Enrichment Scorecard ===")
    for row in scorecard:
        issues = row["issues"]
        print(
            f"{row['collection']}: {row['quality_score']}/100 | "
            f"files={row['total_files']} changed={row['changed_files']} "
            f"missing_translation={issues['missing_translation']} "
            f"empty_commentary={issues['empty_commentary']} "
            f"missing_abhyasa={issues['missing_abhyasa']}"
        )

    aggregate = {
        "yaml_root": str(yaml_root),
        "collections": scorecard,
        "totals": {
            "collections": len(scorecard),
            "files": sum(int(x.get("total_files", 0)) for x in scorecard),
            "changed_files": sum(int(x.get("changed_files", 0)) for x in scorecard),
            "missing_translation": sum(int(x.get("issues", {}).get("missing_translation", 0)) for x in scorecard),
            "empty_commentary": sum(int(x.get("issues", {}).get("empty_commentary", 0)) for x in scorecard),
            "missing_abhyasa": sum(int(x.get("issues", {}).get("missing_abhyasa", 0)) for x in scorecard),
        },
    }
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(aggregate, indent=2), encoding="utf-8")
        print(f"\nBatch report written to {report_path}")
    return 0 if failures == 0 else 2


def main() -> int:
    ap = argparse.ArgumentParser(description="Auto-enrich YAML files toward Siva Sutra quality.")
    ap.add_argument("--input-dir", type=Path, help="Directory containing YAML files to enrich.")
    ap.add_argument(
        "--all-yaml",
        action="store_true",
        help="Enrich all YAML collections under --yaml-root and output a scorecard.",
    )
    ap.add_argument(
        "--yaml-root",
        type=Path,
        default=ROOT / "data" / "yaml",
        help="Root directory containing YAML collection folders (used with --all-yaml).",
    )
    ap.add_argument("--dry-run", action="store_true", help="Compute changes without writing files.")
    ap.add_argument(
        "--report-path",
        type=Path,
        default=ROOT / "data" / "reports" / "enrichment_report.json",
        help="JSON report output path.",
    )
    args = ap.parse_args()
    if args.all_yaml:
        return run_all(args.yaml_root, args.dry_run, args.report_path)
    if not args.input_dir:
        ap.error("Provide --input-dir or use --all-yaml")
    return run(args.input_dir, args.dry_run, args.report_path)


if __name__ == "__main__":
    raise SystemExit(main())


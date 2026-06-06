#!/usr/bin/env python3
"""
Canonicalize mixed YAML into two primary categories:

1) root_text      -> essential sutra/verse style units
2) commentary_text -> book/chapter exposition units (thesis/themes/excerpt)

Usage:
  python scripts/canonicalize_texts.py
  python scripts/canonicalize_texts.py --yaml-root data/yaml --out-root data/canonical
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent.parent
YAML_ROOT_DEFAULT = ROOT / "data" / "yaml"
OUT_ROOT_DEFAULT = ROOT / "data" / "canonical"


def txt(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, dict):
        for key in ("title", "translation", "transliteration", "devanagari", "text", "name"):
            val = v.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
        return ""
    if isinstance(v, list):
        return "\n".join(str(x) for x in v if x).strip()
    return str(v).strip()


def _strip_controls(s: str) -> str:
    # Keep newline/tab/carriage-return, remove other control chars that break YAML parsing.
    return "".join(ch for ch in s if ch in "\n\t\r" or ord(ch) >= 32)


def _sanitize(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize(v) for v in obj]
    if isinstance(obj, str):
        return _strip_controls(obj)
    return obj


def slug(s: str) -> str:
    s = re.sub(r"[^\w\s.-]", " ", s, flags=re.UNICODE)
    s = re.sub(r"[\s._-]+", "_", s).strip("_").lower()
    return s or "text"


def rel(path: Path) -> str:
    p = path.resolve()
    try:
        return str(p.relative_to(ROOT))
    except Exception:
        return str(path)


def first_sentence(s: str) -> str:
    s = txt(s)
    if not s:
        return ""
    parts = re.split(r"(?<=[.!?])\s+", s)
    return parts[0].strip() if parts else s


def first_paragraph(s: str, limit: int = 600) -> str:
    s = txt(s)
    if not s:
        return ""
    p = [x.strip() for x in s.split("\n\n") if x.strip()]
    out = p[0] if p else s
    return out[:limit].strip()


THEME_TERMS = [
    "awareness",
    "consciousness",
    "self",
    "heart",
    "breath",
    "mantra",
    "śiva",
    "shiva",
    "śakti",
    "shakti",
    "mind",
    "recognition",
    "meditation",
    "silence",
    "practice",
    "freedom",
    "ignorance",
    "knowledge",
    "vibration",
    # Taoist / Chinese philosophy terms
    "dao",
    "tao",
    "way",
    "wu wei",
    "non-action",
    "ziran",
    "naturalness",
    "sage",
    "heaven",
    "earth",
    "yin",
    "yang",
    "virtue",
    "de",
    "emptiness",
    "stillness",
    "spontaneity",
    "transformation",
    "harmony",
    "simplicity",
    "fasting of the mind",
    "sitting in forgetfulness",
    "usefulness",
    "uselessness",
    # Learning-path vocabulary (kept aligned with web/src/lib/learningPaths.ts
    # so curated path steps can match passages by theme).
    "action",
    "duty",
    "renunciation",
    "non-attachment",
    "detachment",
    "surrender",
    "death",
    "dying",
    "impermanence",
    "soul",
    "witness",
    "witnessing",
    "contraction",
    "devotion",
    "desire",
    "suffering",
    "equanimity",
    "courage",
    "fear",
    "fate",
    "truth",
    "illusion",
    "ego",
    "attention",
    "grace",
]

def _normalize_for_match(s: str) -> str:
    s = txt(s).lower()
    # Strip diacritics so dao/tao style terms match reliably.
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", s)


def _strip_cross_tradition(text: str) -> str:
    """Remove the Cross-Tradition Resonances section so other traditions'
    vocabulary (e.g. Daoist terms inside a Phaedo unit) does not leak into a
    passage's own themes."""
    s = txt(text)
    if not s:
        return ""
    match = re.search(r"(?im)^\s*#*\s*cross-tradition resonances?\s*:?\s*$", s)
    return s[: match.start()].strip() if match else s


def extract_themes(*parts: str) -> list[str]:
    blob = _normalize_for_match(" ".join(_strip_cross_tradition(p) for p in parts))
    out: list[str] = []
    for term in THEME_TERMS:
        t = _normalize_for_match(term)
        # Phrase match for multi-word terms; word-boundary for single words.
        if " " in t:
            if t in blob:
                out.append(term)
        else:
            if re.search(rf"\b{re.escape(t)}\b", blob):
                out.append(term)
    return sorted(set(out))[:8]


def _glossary_terms(y: dict[str, Any]) -> list[str]:
    out: list[str] = []
    g = y.get("glossary")
    if not isinstance(g, list):
        return out
    for row in g:
        if not isinstance(row, dict):
            continue
        term = txt(row.get("term"))
        if not term:
            continue
        t = _normalize_for_match(term)
        # Keep compact, meaningful terms.
        if 2 <= len(t) <= 40 and len(t.split()) <= 4:
            out.append(t)
    return out[:6]


def themes_for_unit(y: dict[str, Any], *parts: str) -> list[str]:
    # Themes come from a controlled vocabulary (THEME_TERMS) plus the unit's own
    # glossary. The old frequency-based fallback produced noisy tokens
    # ("things", "way", "make") and is intentionally dropped.
    out: list[str] = []
    for t in extract_themes(*parts):
        if t not in out:
            out.append(t)
    for g in _glossary_terms(y):
        if g not in out:
            out.append(g)
        if len(out) >= 8:
            break
    return out[:8]


def _normalize_appendixes(v: Any) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    if not isinstance(v, list):
        return out
    for item in v:
        if not isinstance(item, dict):
            continue
        commentator = txt(item.get("commentator") or item.get("author") or item.get("title"))
        text = txt(item.get("text") or item.get("content") or item.get("body"))
        if text:
            out.append({"commentator": commentator or "Appendix", "text": text})
    return out


def _appendixes_as_commentary(appendixes: list[dict[str, str]]) -> str:
    if not appendixes:
        return ""
    return "\n\n".join(f"{a['commentator']}:\n{a['text']}" for a in appendixes if txt(a.get("text")))


def build_pratibha_layers(
    *,
    sanskrit: str = "",
    iast: str = "",
    translation: str = "",
    commentary: str = "",
    practice: str = "",
    appendixes: list[dict[str, str]] | None = None,
) -> list[dict[str, Any]]:
    layers: list[dict[str, Any]] = []
    for kind, label, body in [
        ("original", "Original", sanskrit),
        ("iast", "IAST", iast),
        ("translation", "Pratibha Translation", translation),
        ("commentary", "Pratibha Commentary", commentary),
        ("practice", "Practice (Abhyasa)", practice),
    ]:
        clean = txt(body)
        if clean:
            layers.append({"kind": kind, "label": label, "body": clean})
    for idx, appendix in enumerate(appendixes or []):
        body = txt(appendix.get("text"))
        if body:
            layers.append({
                "kind": "appendix",
                "label": txt(appendix.get("commentator")) or f"Appendix {idx + 1}",
                "body": body,
            })
    return layers


def _coerce_wrapped_record(raw: dict[str, Any]) -> dict[str, Any]:
    """
    Some legacy YAMLs wrap the actual verse payload in a single top-level key,
    e.g. {"1.14": {"sutra": "...", "translation": "..."}}.
    """
    if not isinstance(raw, dict) or len(raw) != 1:
        return raw
    key = next(iter(raw.keys()))
    val = raw[key]
    if not isinstance(val, dict):
        return raw
    out = dict(val)
    key_s = str(key).strip()
    if key_s and not out.get("sutra"):
        out["sutra"] = key_s
    if key_s and not out.get("sutra_id") and re.match(r"^\d+\.\d+$", key_s):
        out["sutra_id"] = f"SS_{key_s}"
    return out


def infer_root_like(y: dict[str, Any], path: Path) -> bool:
    p = str(path).lower()
    coll = txt(y.get("collection")).lower()
    sid = txt(y.get("sutra_id")).lower()
    sec = txt(y.get("section")).lower()
    s = txt(y.get("sanskrit"))
    i = txt(y.get("transliteration"))
    tr = txt(y.get("translation"))

    if any(k in p for k in ["siva_sutra", "vijnana_bhairava", "yukti"]):
        return True
    if "sutra" in coll or "bhairava" in coll:
        return True
    if sid.startswith("ss_") or sid.startswith("yukti_"):
        return True
    if "sutra" in sec or "verse" in sec or "meditation_technique" in sec:
        return True
    if s and i and len(tr) < 1200:
        return True
    return False


def classify_unit_type(y: dict[str, Any], path: Path, is_root: bool) -> str:
    sec = txt(y.get("section")).lower()
    sid = txt(y.get("sutra_id")).lower()
    if is_root:
        if "yukti" in sid or "meditation_technique" in sec:
            return "verse"
        return "sutra"
    if "chapter" in sec or re.search(r"\bch_\d+", path.stem.lower()):
        return "chapter_section"
    return "teaching_passage"


def normalize_root_unit(y: dict[str, Any], path: Path) -> dict[str, Any]:
    coll = txt(y.get("collection")) or path.parent.name
    sutra_id = txt(y.get("sutra_id")) or path.stem
    display_title = txt(y.get("title")) or txt(y.get("sutra"))
    label = display_title or txt(y.get("number")) or sutra_id
    sanskrit = txt(y.get("sanskrit"))
    iast = txt(y.get("transliteration"))
    translation = txt(y.get("translation"))
    commentary = txt(y.get("scholarly_commentary")) or txt(y.get("commentary"))
    appendixes = _normalize_appendixes(y.get("appendixes"))
    if not commentary and appendixes:
        commentary = _appendixes_as_commentary(appendixes)
    if not translation:
        translation = txt((y.get("modes") or {}).get("sadhana")) or txt(y.get("voice_of_siva")) or commentary
    insight = txt(y.get("voice_of_siva")) or first_sentence(commentary or translation)
    practice = txt(y.get("abhyasa")) or txt((y.get("modes") or {}).get("sadhana"))
    upaya = txt(y.get("upaya"))

    work_id = slug(coll)
    unit_id = f"{work_id}.{slug(sutra_id)}"
    themes = themes_for_unit(y, display_title, translation, commentary, insight, practice)
    tags = sorted(set([work_id, "root_text"] + themes))

    return {
        "source_file": rel(path),
        "source_id": sutra_id,
        "category": "root_text",
        "work_id": work_id,
        "work_title": coll,
        "unit_id": unit_id,
        "unit_label": label,
        "title": display_title or label,
        "unit_type": "sutra_or_verse",
        "sanskrit_devanagari": sanskrit,
        "sanskrit_iast": iast,
        "translation_literal": translation,
        "commentary": commentary,
        "insight": insight,
        "practice": practice,
        "upaya": upaya,
        "themes": themes,
        "tags": tags,
        "quality_score": y.get("quality_score_unit") or 0,
        "editorial_maturity": y.get("editorial_maturity") or "strong_draft",
        "editorial_score": y.get("editorial_score") or 0,
        "pratibha_layers": build_pratibha_layers(
            sanskrit=sanskrit,
            iast=iast,
            translation=translation,
            commentary=commentary,
            practice=practice,
            appendixes=appendixes,
        ),
        "appendixes": appendixes,
        "provenance": {
            "collection": coll,
            "section": txt(y.get("section")),
            "original_id": sutra_id,
        },
    }


def normalize_commentary_unit(y: dict[str, Any], path: Path) -> dict[str, Any]:
    coll = txt(y.get("collection")) or path.parent.name
    source_id = txt(y.get("sutra_id")) or path.stem
    section = txt(y.get("section")) or "chapter_section"
    display_title = txt(y.get("title")) or txt(y.get("sutra")) or source_id
    translation = txt(y.get("translation"))
    commentary = txt(y.get("commentary"))
    appendixes = _normalize_appendixes(y.get("appendixes"))
    if not commentary and appendixes:
        commentary = _appendixes_as_commentary(appendixes)
    thesis = first_sentence(txt(y.get("voice_of_siva")) or txt((y.get("modes") or {}).get("doctrinal")) or commentary or translation)
    excerpt = first_paragraph(translation or commentary, limit=700)
    practice = txt(y.get("abhyasa")) or txt((y.get("modes") or {}).get("sadhana"))
    if not practice:
        practice = "Read the excerpt slowly, pause at one striking line, and reflect on its relevance to present experience."

    work_id = slug(coll)
    unit_id = f"{work_id}.{slug(source_id)}"
    themes = themes_for_unit(y, display_title, thesis, excerpt, commentary, practice)
    tags = sorted(set([work_id, "commentary_text"] + themes))

    return {
        "source_file": rel(path),
        "source_id": source_id,
        "category": "commentary_text",
        "work_id": work_id,
        "work_title": coll,
        "unit_id": unit_id,
        "unit_label": display_title,
        "title": display_title,
        "unit_type": section if section else "chapter_section",
        "thesis": thesis,
        "themes": themes,
        "source_excerpt": excerpt,
        "translation_literal": translation,
        "commentary": commentary,
        "insight": txt(y.get("voice_of_siva")),
        "practice": practice,
        "sanskrit_devanagari": txt(y.get("sanskrit")),
        "sanskrit_iast": txt(y.get("transliteration")),
        "tags": tags,
        "quality_score": y.get("quality_score_unit") or 0,
        "editorial_maturity": y.get("editorial_maturity") or "strong_draft",
        "editorial_score": y.get("editorial_score") or 0,
        "pratibha_layers": build_pratibha_layers(
            sanskrit=txt(y.get("sanskrit")),
            iast=txt(y.get("transliteration")),
            translation=translation,
            commentary=commentary,
            practice=practice,
            appendixes=appendixes,
        ),
        "appendixes": appendixes,
        "provenance": {
            "collection": coll,
            "section": section,
            "original_id": source_id,
        },
    }


def normalize(path: Path, y: dict[str, Any]) -> dict[str, Any]:
    is_root = infer_root_like(y, path)
    unit_type = classify_unit_type(y, path, is_root)
    unit = normalize_root_unit(y, path) if is_root else normalize_commentary_unit(y, path)
    unit["unit_type"] = unit_type if unit_type else unit["unit_type"]
    return unit


def all_yaml_files(root: Path) -> list[Path]:
    return sorted(list(root.glob("**/*.yml")) + list(root.glob("**/*.yaml")))


def main() -> int:
    ap = argparse.ArgumentParser(description="Canonicalize YAML into root_text/commentary_text categories.")
    ap.add_argument("--yaml-root", type=Path, default=YAML_ROOT_DEFAULT)
    ap.add_argument("--out-root", type=Path, default=OUT_ROOT_DEFAULT)
    args = ap.parse_args()

    yaml_root = args.yaml_root
    out_root = args.out_root
    out_root.mkdir(parents=True, exist_ok=True)

    # clear previous generated files
    for p in out_root.glob("**/*.yml"):
        p.unlink()

    units: list[dict[str, Any]] = []
    for fp in all_yaml_files(yaml_root):
        try:
            with open(fp, "r", encoding="utf-8") as f:
                raw = yaml.safe_load(f)
            if not isinstance(raw, dict):
                continue
            raw = _coerce_wrapped_record(raw)
            unit = normalize(fp, raw)
            units.append(unit)
        except Exception as e:
            print(f"skip {fp}: {e}")

    # dedupe by unit_id
    seen: set[str] = set()
    kept: list[dict[str, Any]] = []
    for u in units:
        uid = txt(u.get("unit_id"))
        if not uid or uid in seen:
            continue
        seen.add(uid)
        kept.append(u)

    # write grouped by work_id
    for u in kept:
        work_id = txt(u.get("work_id")) or "text"
        d = out_root / work_id
        d.mkdir(parents=True, exist_ok=True)
        fname = f"{txt(u.get('unit_id')).replace('.', '_')}.yml"
        clean = _sanitize(u)
        with open(d / fname, "w", encoding="utf-8") as f:
            yaml.safe_dump(clean, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)

    # write index + summary
    idx = out_root / "index.jsonl"
    with open(idx, "w", encoding="utf-8") as f:
        for u in kept:
            f.write(json.dumps(_sanitize(u), ensure_ascii=False) + "\n")

    root_n = sum(1 for u in kept if u.get("category") == "root_text")
    comm_n = sum(1 for u in kept if u.get("category") == "commentary_text")
    print(f"canonical units: {len(kept)}")
    print(f"root_text: {root_n}")
    print(f"commentary_text: {comm_n}")
    print(f"wrote: {out_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


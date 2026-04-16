import datetime
import glob
import hashlib
import os
import ast
from typing import Any

import pytz
import yaml

ROOT = os.path.dirname(os.path.dirname(__file__))


def _as_text(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, dict):
        for key in ("title", "translation", "transliteration", "devanagari", "text", "name"):
            val = v.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
        return ""
    if isinstance(v, list):
        return "\n".join(_as_text(x) for x in v if _as_text(x)).strip()
    if isinstance(v, str):
        s = v.strip()
        # Some legacy fields were stringified dicts; recover the useful title text.
        if s.startswith("{") and s.endswith("}"):
            try:
                parsed = ast.literal_eval(s)
                if isinstance(parsed, dict):
                    recovered = _as_text(parsed)
                    if recovered:
                        return recovered
            except Exception:
                pass
        return s
    return str(v).strip()


def _humanize_collection(v: str) -> str:
    s = v.strip()
    if not s:
        return "Unknown Collection"
    if "_" in s and s.lower() == s:
        s = s.replace("_", " ")
    s = " ".join(s.split())
    return s.title() if s == s.lower() else s


def _pretty_section(v: str) -> str:
    s = " ".join(v.split()).strip().lower()
    if not s:
        return ""
    if s == "chapter_section":
        return "Chapter"
    if s == "teaching_passage":
        return "Teaching Passage"
    if s == "sutra":
        return "Sutra"
    if s == "verse":
        return "Verse"
    return s.capitalize()


def _default_data_roots() -> list[str]:
    canonical = os.path.join(ROOT, "data", "canonical")
    legacy = os.path.join(ROOT, "data", "yaml")
    data_dir = os.environ.get("DATA_DIR", "").strip()
    if data_dir:
        return [os.path.join(ROOT, data_dir) if not os.path.isabs(data_dir) else data_dir]
    # Prefer canonical corpus if present.
    if os.path.isdir(canonical):
        return [canonical]
    return [legacy]


def _normalize(item: dict[str, Any], path: str) -> dict[str, Any]:
    out = dict(item)
    out["_id"] = _as_text(item.get("_id") or item.get("unit_id") or item.get("sutra_id") or os.path.splitext(os.path.basename(path))[0])
    out["collection"] = _humanize_collection(_as_text(item.get("work_title") or item.get("collection") or item.get("work_id") or "Unknown Collection"))
    out["section"] = _pretty_section(_as_text(item.get("section") or item.get("unit_type")))
    out["sutra_id"] = _as_text(item.get("sutra_id") or item.get("source_id") or out["_id"])
    out["translation"] = _as_text(item.get("translation") or item.get("translation_literal"))
    out["commentary"] = _as_text(item.get("commentary"))
    out["sanskrit"] = _as_text(item.get("sanskrit") or item.get("sanskrit_devanagari"))
    out["transliteration"] = _as_text(item.get("transliteration") or item.get("sanskrit_iast"))
    out["title"] = _as_text(item.get("title") or item.get("unit_label") or item.get("sutra") or out["sutra_id"])
    out["themes"] = item.get("themes") if isinstance(item.get("themes"), list) else []
    out["appendixes"] = item.get("appendixes") if isinstance(item.get("appendixes"), list) else []
    out["abhyasa"] = _as_text(item.get("abhyasa") or item.get("practice"))
    return out


def load_all() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    patterns = ["**/*.yml", "**/*.yaml"]
    for root in _default_data_roots():
        for pattern in patterns:
            for path in sorted(glob.glob(os.path.join(root, pattern), recursive=True)):
                if os.path.basename(path) == "_work.yml":
                    continue
                try:
                    with open(path, "r", encoding="utf-8", errors="replace") as f:
                        item = yaml.safe_load(f)
                    if not isinstance(item, dict):
                        continue
                    norm = _normalize(item, path)
                    _id = norm["_id"]
                    if _id in seen:
                        continue
                    seen.add(_id)
                    out.append(norm)
                except Exception:
                    continue
    return out


ALL_VERSES = load_all()


def pick_daily(user_id: str = "guest", tz: str = "Europe/Paris"):
    if not ALL_VERSES:
        return None
    now = datetime.datetime.now(pytz.timezone(tz))
    key = f"{now.year}-{now.month}-{now.day}-{user_id}"
    h = hashlib.sha1(key.encode()).hexdigest()
    idx = int(h, 16) % len(ALL_VERSES)
    return ALL_VERSES[idx]

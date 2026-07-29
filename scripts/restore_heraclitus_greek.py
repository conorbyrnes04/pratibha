#!/usr/bin/env python3
"""Restore Ancient Greek originals for Heraclitus canonical units.

Source: Bywater 1877 Greek as transmitted with Patrick 1889 numbering, from the
Classic Persuasion Unicode HTML (Wayback; public domain Bywater/Patrick text).
Clean Diels 1903 B-text is also kept under data/raw_texts/pd/greek/ for reference.

Matching:
  1. Prefer Patrick English ↔ unit Pratibha translation similarity
  2. Fall back to Patrick number from unit_id (HFR_P### / hfr_p###)
  3. Skip latin-only Bywater lemmata with no extractable Greek

Updates pratibha_layers original/iast, flat sanskrit_* slots, layer_provenance,
and synchronizes data/canonical/index.jsonl.
"""
from __future__ import annotations

import argparse
import json
import re
import tempfile
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical"
INDEX = CANONICAL / "index.jsonl"
FRAGS_JSON = ROOT / "data" / "raw_texts" / "pd" / "greek" / "heraclitus_bywater_patrick_frags.json"
WORK = "heraclitus_fragments"
PROV = "greek: bywater_1877 (Patrick numbering; Classic Persuasion Unicode)"


def load_frags() -> dict[int, dict[str, str]]:
    raw = json.loads(FRAGS_JSON.read_text(encoding="utf-8"))
    return {int(k): v for k, v in raw.items()}


def norm_en(s: str) -> str:
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def greek_char_count(s: str) -> int:
    return sum(1 for ch in s if "\u0370" <= ch <= "\u03FF" or "\u1F00" <= ch <= "\u1FFF")


def clean_greek(raw: str) -> str | None:
    """Strip testimonia wrappers; return pure-ish Heraclitean Greek or None."""
    s = re.sub(r"\s+", " ", (raw or "").strip())
    if not s:
        return None
    # Pure Latin paraphrase (Bywater sometimes)
    min_g = 4 if len(s) <= 40 else 8
    if greek_char_count(s) < min_g:
        return None
    # Author wrapper: "Plutarchus, ...: GREEK" or "Name ... φησι, GREEK"
    if re.match(r"^[A-Za-z]", s):
        # take longest greek run after a colon or quotation cue
        parts = re.split(r"[:;]\s*", s, maxsplit=1)
        candidate = parts[-1] if len(parts) > 1 else s
        # drop leading latin words still present
        m = re.search(r"[\u0370-\u03FF\u1F00-\u1FFF]", candidate)
        if not m:
            return None
        candidate = candidate[m.start() :]
        # stop at trailing latin apparatus if any
        candidate = re.split(r"\s+(?:cf\.|Conf\.|Compare|v\.|see\b)", candidate, maxsplit=1, flags=re.I)[0]
        s = candidate.strip(" .;,—-")
        if greek_char_count(s) < min_g:
            return None
    # Remove dagger/obelus noise markers but keep text
    s = s.replace("†", "").strip()
    s = re.sub(r"\s+", " ", s)
    return s if greek_char_count(s) >= min_g else None


def score_pair(unit_en: str, patrick_en: str) -> float:
    a = norm_en(unit_en)
    b = norm_en(patrick_en)
    if not a or not b:
        return 0.0
    n = min(220, max(len(a), 40), max(len(b), 40))
    return SequenceMatcher(None, a[:n], b[:n]).ratio()


_STOP = {
    "the",
    "a",
    "an",
    "of",
    "to",
    "and",
    "for",
    "in",
    "is",
    "are",
    "be",
    "this",
    "that",
    "which",
    "who",
    "with",
    "as",
    "or",
    "not",
    "on",
    "by",
    "from",
    "it",
    "its",
    "they",
    "their",
    "them",
    "he",
    "his",
    "her",
    "was",
    "were",
    "been",
    "have",
    "has",
    "had",
    "will",
    "would",
    "can",
    "may",
    "than",
    "but",
    "all",
}


def tokens(s: str) -> set[str]:
    s = re.sub(r"[^a-z0-9\s]", " ", (s or "").lower())
    return {w for w in s.split() if len(w) > 2 and w not in _STOP}


def jaccard(unit_en: str, patrick_en: str) -> float:
    a, b = tokens(unit_en), tokens(patrick_en)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def choose_patrick(
    unit_en: str,
    prefer: int,
    frags: dict[int, dict[str, str]],
    cleaned: dict[int, str],
    min_score: float,
) -> tuple[int | None, str]:
    """Prefer filename Patrick number; remap only on clear content mismatch."""
    prefer_en = (frags.get(prefer) or {}).get("english") or ""
    prefer_seq = score_pair(unit_en, prefer_en)
    prefer_jac = jaccard(unit_en, prefer_en)

    scored: list[tuple[float, float, float, int]] = []
    for n, f in frags.items():
        if n not in cleaned:
            continue
        en = f.get("english") or ""
        seq = score_pair(unit_en, en)
        jac = jaccard(unit_en, en)
        # Combined: require some lexical overlap for remaps
        comb = 0.55 * seq + 0.45 * jac
        scored.append((comb, seq, jac, n))
    scored.sort(reverse=True)
    best_comb, best_seq, best_jac, best_n = scored[0] if scored else (0.0, 0.0, 0.0, prefer)
    prefer_comb = 0.55 * prefer_seq + 0.45 * prefer_jac

    def ok_remap() -> bool:
        if best_n == prefer:
            return False
        # Strong lexical hit
        if best_jac >= 0.35 and (best_jac - prefer_jac) >= 0.15:
            return True
        # Strong sequence + some lexical support (handles paraphrase)
        if best_seq >= 0.50 and best_jac >= 0.15 and (best_seq - prefer_seq) >= 0.12:
            return True
        # Near-identical English
        if best_seq >= 0.85:
            return True
        return False

    if prefer in cleaned:
        prefer_toks = tokens(prefer_en)
        unit_toks = tokens(unit_en)
        prefer_covered = (
            bool(prefer_toks) and len(prefer_toks & unit_toks) / len(prefer_toks) >= 0.8
        )
        title = unit_en.split("\n")[-1] if "\n" in unit_en else ""
        title_jac = jaccard(title, prefer_en) if title else 0.0
        if prefer_jac >= 0.25 or prefer_seq >= min_score or title_jac >= 0.5 or prefer_covered:
            if ok_remap() and best_comb > prefer_comb + 0.08 and not prefer_covered and title_jac < 0.5:
                return best_n, f"remap:{prefer_comb:.2f}->{best_comb:.2f}"
            return prefer, f"patrick_num:{prefer_seq:.2f}/{prefer_jac:.2f}"
        if ok_remap():
            return best_n, f"remap:{prefer_comb:.2f}->{best_comb:.2f}"
        return prefer, f"patrick_num_keep:{prefer_seq:.2f}/{prefer_jac:.2f}"

    # Prefer uncleanable (Latin-only): require strong lexical match
    if best_jac >= 0.40 or best_seq >= 0.85:
        return best_n, f"en_match:{best_seq:.2f}/{best_jac:.2f}"
    return None, f"unmatched:{best_seq:.2f}/{best_jac:.2f}"


# Polytonic-aware rough transliteration to Latin (scholarly-ish, not full ISO)
_BASE = {
    "α": "a",
    "β": "b",
    "γ": "g",
    "δ": "d",
    "ε": "e",
    "ζ": "z",
    "η": "ē",
    "θ": "th",
    "ι": "i",
    "κ": "k",
    "λ": "l",
    "μ": "m",
    "ν": "n",
    "ξ": "x",
    "ο": "o",
    "π": "p",
    "ρ": "r",
    "σ": "s",
    "ς": "s",
    "τ": "t",
    "υ": "u",
    "φ": "ph",
    "χ": "ch",
    "ψ": "ps",
    "ω": "ō",
    "ϝ": "w",
}


def transliterate(greek: str) -> str:
    nfd = unicodedata.normalize("NFD", greek)
    out: list[str] = []
    i = 0
    chars = list(nfd)
    while i < len(chars):
        ch = chars[i]
        if ch in ("\u0313", "\u0314") or unicodedata.category(ch) == "Mn":
            i += 1
            continue
        low = ch.lower()
        if low in _BASE:
            # Collect following combining marks (breathings, accents)
            j = i + 1
            marks = []
            while j < len(chars) and (
                chars[j] in ("\u0313", "\u0314") or unicodedata.category(chars[j]) == "Mn"
            ):
                marks.append(chars[j])
                j += 1
            rough = "\u0314" in marks
            # gamma nasal before γ κ χ ξ
            if low == "γ":
                k = j
                while k < len(chars) and (
                    chars[k] in ("\u0313", "\u0314") or unicodedata.category(chars[k]) == "Mn"
                ):
                    k += 1
                if k < len(chars) and chars[k].lower() in ("γ", "κ", "χ", "ξ"):
                    out.append("n")
                    i = j
                    continue
            tok = _BASE[low]
            if rough:
                tok = "h" + tok
            out.append(tok.upper() if ch.isupper() else tok)
            i = j
            continue
        if ch in ("·", ";", ":", ",", ".", "—", "-", "(", ")", "[", "]", "’", "'", "᾽", "᾿", " ", "\n"):
            out.append("." if ch == "·" else ch)
        else:
            out.append(ch)
        i += 1
    return re.sub(r" +", " ", "".join(out)).strip()


def unit_english(data: dict[str, Any]) -> str:
    parts: list[str] = []
    for layer in data.get("pratibha_layers") or []:
        if isinstance(layer, dict) and layer.get("kind") == "translation" and layer.get("body"):
            parts.append(str(layer["body"]))
            break
    for key in ("translation_literal", "source_excerpt", "title", "unit_label", "thesis"):
        val = data.get(key)
        if val:
            parts.append(str(val))
    # Prefer translation body for matching, but append title (helps OCR-merged bodies)
    if not parts:
        return ""
    # Weight: primary translation first; title always included for short anchors
    primary = parts[0]
    title = str(data.get("title") or data.get("unit_label") or "")
    if title and title not in primary:
        return f"{primary}\n{title}"
    return primary


def patrick_num(unit_id: str, data: dict[str, Any]) -> int:
    m = re.search(r"[._]p(\d+)$", unit_id, re.I) or re.search(r"P(\d+)", str(data.get("source_id") or ""))
    return int(m.group(1)) if m else 0


def upsert_layer(unit: dict[str, Any], kind: str, body: str, label: str, provenance: str) -> None:
    layers = unit.get("pratibha_layers")
    if not isinstance(layers, list):
        layers = []
        unit["pratibha_layers"] = layers
    existing = next((L for L in layers if isinstance(L, dict) and L.get("kind") == kind), None)
    if existing is None:
        existing = {"kind": kind, "label": label}
        # insert in conventional order
        order = ["original", "iast", "translation", "commentary", "key_terms", "resonances", "practice", "appendix"]
        idx = order.index(kind) if kind in order else len(layers)
        # find insertion point among existing
        pos = 0
        for i, L in enumerate(layers):
            k = L.get("kind")
            if k in order and order.index(k) <= idx:
                pos = i + 1
        layers.insert(pos, existing)
    existing["label"] = label
    existing["body"] = body
    existing["layer_provenance"] = provenance


def set_top_provenance(unit: dict[str, Any], note: str) -> None:
    prov = unit.get("layer_provenance")
    if not isinstance(prov, dict):
        prov = {}
    prov["original"] = note
    prov["iast"] = "transliterated_from_greek"
    unit["layer_provenance"] = prov


def dump_yaml(unit: dict[str, Any]) -> str:
    return yaml.safe_dump(
        unit, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120
    )


def atomic_write(path: Path, content: str) -> None:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(content)
        temp = Path(handle.name)
    temp.replace(path)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--min-score", type=float, default=0.38)
    args = ap.parse_args()

    frags = load_frags()
    # Pre-clean greek
    cleaned: dict[int, str] = {}
    uncleanable: list[int] = []
    for n, f in frags.items():
        g = clean_greek(f.get("greek") or "")
        if g:
            cleaned[n] = g
        else:
            uncleanable.append(n)

    yaml_paths = sorted((CANONICAL / WORK).glob("*.yml"))
    before_greek = 0
    after_plans: list[dict[str, Any]] = []
    unmatched: list[str] = []

    for path in yaml_paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        uid = str(data["unit_id"])
        layers = {L["kind"]: L for L in (data.get("pratibha_layers") or []) if isinstance(L, dict)}
        orig = (layers.get("original") or {}).get("body") or ""
        if greek_char_count(orig) >= 8 and "not directly provided" not in orig.lower():
            # count as already having greek if mostly greek / short greek line
            before_greek += 1

        prefer = patrick_num(uid, data)
        unit_en = unit_english(data)
        chosen, method = choose_patrick(unit_en, prefer, frags, cleaned, args.min_score)

        if chosen is None:
            unmatched.append(uid)
            continue

        greek = cleaned[chosen]
        iast = transliterate(greek)
        after_plans.append(
            {
                "path": path,
                "uid": uid,
                "patrick": chosen,
                "method": method,
                "greek": greek,
                "iast": iast,
                "prefer": prefer,
            }
        )

    print(f"units={len(yaml_paths)} before_greek≈{before_greek}")
    print(f"planned_updates={len(after_plans)} unmatched={len(unmatched)}")
    print(f"uncleanable_bywater={uncleanable}")
    if unmatched:
        print("unmatched unit_ids:")
        for u in unmatched:
            print(" ", u)

    # Coverage of methods
    from collections import Counter

    print("methods", Counter(p["method"].split(":")[0] for p in after_plans))
    # Show remaps where chosen != prefer
    remaps = [p for p in after_plans if p["patrick"] != p["prefer"]]
    print(f"remapped_from_filename={len(remaps)}")
    for p in remaps[:20]:
        print(f"  {p['uid']}: P{p['prefer']} -> P{p['patrick']} ({p['method']})")

    if not args.write:
        print("dry-run only; pass --write to apply")
        return 0

    # Load index
    index_lines = INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
    index_units = [json.loads(line) for line in index_lines if line.strip()]
    by_uid = {u["unit_id"]: i for i, u in enumerate(index_units)}

    updated = 0
    for plan in after_plans:
        path: Path = plan["path"]
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        greek = plan["greek"]
        iast = plan["iast"]
        note = f"{PROV}; Patrick/Bywater fr. {plan['patrick']}"

        upsert_layer(data, "original", greek, "Original", note)
        upsert_layer(data, "iast", iast, "IAST", "transliterated_from_greek")
        data["sanskrit_devanagari"] = greek
        data["sanskrit_iast"] = iast
        set_top_provenance(data, note)

        # provenance.source_reference tweak if present
        prov = data.get("provenance")
        if isinstance(prov, dict):
            ref = str(prov.get("source_reference") or "")
            if "Bywater" not in ref and "Patrick" in ref:
                pass
            elif not ref:
                prov["source_reference"] = f"Patrick (1889) / Bywater Greek, fr. {plan['patrick']}"

        atomic_write(path, dump_yaml(data))

        uid = plan["uid"]
        if uid in by_uid:
            idx = by_uid[uid]
            row = index_units[idx]
            # sync fields present on index rows
            row["sanskrit_devanagari"] = greek
            row["sanskrit_iast"] = iast
            # sync layers
            layers = row.get("pratibha_layers")
            if isinstance(layers, list):
                # reuse upsert on row
                upsert_layer(row, "original", greek, "Original", note)
                upsert_layer(row, "iast", iast, "IAST", "transliterated_from_greek")
            set_top_provenance(row, note)
            index_lines[idx] = json.dumps(row, ensure_ascii=False) + "\n"
        updated += 1

    atomic_write(INDEX, "".join(index_lines))
    print(f"wrote {updated} YAML units and synchronized index.jsonl")

    # After count
    after = 0
    for path in yaml_paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        layers = {L["kind"]: L for L in (data.get("pratibha_layers") or []) if isinstance(L, dict)}
        orig = (layers.get("original") or {}).get("body") or ""
        if greek_char_count(orig) >= 8:
            after += 1
    print(f"after_greek={after}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

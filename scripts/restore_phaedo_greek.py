#!/usr/bin/env python3
"""Restore Ancient Greek originals for Plato Phaedo canonical units.

Source: John Burnet, Platonis Opera vol. I (OCT, 1900) Greek as distributed by
Perseus Digital Library (urn:cts:greekLit:tlg0059.tlg004.perseus-grc2;
CC BY-SA). Stephanus sections extracted from the TEI XML under
data/raw_texts/pd/greek/.

Each unit is mapped to a Burnet/Stephanus locus matching its Pratibha English
excerpt (not always the full cited dialogue span when that span is a long
myth or composite argument). English translation layers are left unchanged.
IAST holds scholarly Greek romanization (same convention as Dionysius restore).

Updates pratibha_layers original/iast, flat sanskrit_* slots, provenance,
collection index, and data/canonical/index.jsonl.
"""
from __future__ import annotations

import argparse
import json
import re
import tempfile
import unicodedata
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

import yaml

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "data" / "canonical" / "phaedo_plato"
MAIN_INDEX = ROOT / "data" / "canonical" / "index.jsonl"
COLL_INDEX = CANON / "index.jsonl"
XML_PATH = ROOT / "data" / "raw_texts" / "pd" / "greek" / "phaedo_burnet_perseus-grc2.xml"
JSON_CACHE = ROOT / "data" / "raw_texts" / "pd" / "greek" / "phaedo_burnet_stephanus.json"

WORK = "phaedo_plato"
PROV = (
    "Greek: Burnet OCT (1900) via Perseus "
    "urn:cts:greekLit:tlg0059.tlg004.perseus-grc2 (CC BY-SA)"
)

GREEK_RE = re.compile(r"[\u0370-\u03FF\u1F00-\u1FFF]")

# unit_id suffix -> (start, end[, start_anchor]) and human locus note
# start_anchor: optional substring; text begins at first occurrence (trim lead-in)
LOCI: dict[str, dict[str, Any]] = {
    # Philosophy as training for death: definition + punchline (μελετῶσι)
    "phaedo_md_001": {
        "parts": [("64a", "65d"), ("67d", "67e")],
        "part_anchors": {"64a": "κινδυνεύουσι γὰρ ὅσοι"},
        "cite": "64a–65d; 67d–e",
        "note": "melete thanatou / soul-body separation",
    },
    # Recollection / equals (core argument, not full closure)
    "phaedo_md_002": {
        "start": "72e",
        "end": "75e",
        "anchor": "καὶ κατ’ ἐκεῖνόν γε τὸν λόγον",
        "cite": "72e–75e",
        "note": "anamnesis / Equality",
    },
    # Affinity with invisible / simple
    "phaedo_md_003": {
        "start": "79a",
        "end": "80b",
        "cite": "79a–80b",
        "note": "affinity / visible vs invisible",
    },
    # Harmony theory: Simmias' proposal + soul-as-ruler refutation
    "phaedo_md_004": {
        "parts": [("85e", "86d"), ("94b", "94e")],
        "cite": "85e–86d; 94b–e",
        "note": "harmonia analogy + soul governs body",
    },
    # Second sailing / Forms as causes
    "phaedo_md_005": {
        "start": "99c",
        "end": "100c",
        "anchor": "τὸν δεύτερον πλοῦν",
        "cite": "99c–100c",
        "note": "deuteros plous / Forms as aitiai",
    },
    # Soul as life-bearer / deathless
    "phaedo_md_006": {
        "start": "105c",
        "end": "106e",
        "anchor": "ἀσφαλῆ σοι ἐρῶ",
        "cite": "105c–106e",
        "note": "soul brings life / athanatos",
    },
    # Final composure / cock to Asclepius (English focuses here, not full myth)
    "phaedo_md_007": {
        "start": "117c",
        "end": "118a",
        "cite": "117c–118a",
        "note": "hemlock scene / Asclepius offering",
    },
    # Possession of the gods / against suicide
    "phaedo_md_008": {
        "start": "61c",
        "end": "62e",
        "cite": "61c–62e",
        "note": "gods' possession / may not open the door",
    },
    # Living from the dead
    "phaedo_md_009": {
        "start": "70c",
        "end": "72a",
        "cite": "70c–72a",
        "note": "cycle of opposites / souls exist",
    },
    # Thyrsus-bearers / true virtue with wisdom
    "phaedo_md_010": {
        "start": "69a",
        "end": "69d",
        "cite": "69a–d",
        "note": "true exchange / narthēkophoroi",
    },
    # Misology
    "phaedo_md_011": {
        "start": "89d",
        "end": "90d",
        "cite": "89d–90d",
        "note": "misologia warning",
    },
    # Ants or frogs about a marsh
    "phaedo_md_012": {
        "start": "109a",
        "end": "110a",
        "cite": "109a–110a",
        "note": "true earth / ants or frogs",
    },
}


def greek_char_count(s: str) -> int:
    return len(GREEK_RE.findall(s or ""))


def clean_ws(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s*\n\s*", " ", text)
    return text.strip()


def parse_stephanus(xml_path: Path) -> tuple[list[str], dict[str, str]]:
    raw = xml_path.read_text(encoding="utf-8")
    raw2 = re.sub(r'\sxmlns(:\w+)?="[^"]*"', "", raw)
    root = ET.fromstring(raw2.encode("utf-8"))
    edition = next(d for d in root.iter("div") if d.get("type") == "edition")

    sections: dict[str, str] = {}
    order: list[str] = []
    cur: str | None = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal cur, buf
        if cur is None:
            return
        text = clean_ws("".join(buf))
        if cur in sections:
            if text:
                sections[cur] = clean_ws(sections[cur] + " " + text)
        else:
            sections[cur] = text
            order.append(cur)
        buf = []

    def walk(el: ET.Element) -> None:
        nonlocal cur
        if el.tag == "milestone" and el.get("unit") == "section":
            n = el.get("n") or ""
            if re.fullmatch(r"\d{2,3}[a-e]", n):
                flush()
                cur = n
                return
        if el.tag in ("note", "bibl", "ref", "teiHeader"):
            return
        if el.text:
            buf.append(el.text)
        for child in list(el):
            walk(child)
            if child.tail:
                buf.append(child.tail)

    walk(edition)
    flush()
    return order, sections


def slice_range(
    order: list[str], sections: dict[str, str], start: str, end: str
) -> str:
    if start not in sections or end not in sections:
        missing = [x for x in (start, end) if x not in sections]
        raise KeyError(f"missing Stephanus section(s): {missing}")
    i0, i1 = order.index(start), order.index(end)
    if i1 < i0:
        raise ValueError(f"end {end} before start {start}")
    parts = [sections[order[i]] for i in range(i0, i1 + 1) if sections[order[i]]]
    return clean_ws(" ".join(parts))


def apply_anchor(text: str, anchor: str | None) -> str:
    if not anchor:
        return text
    i = text.find(anchor)
    if i < 0:
        # try normalized apostrophe variants
        alt = anchor.replace("’", "'").replace("'", "’")
        i = text.find(alt)
    if i < 0:
        raise ValueError(f"start anchor not found: {anchor[:60]!r}")
    return clean_ws(text[i:])


def build_passage(
    order: list[str], sections: dict[str, str], spec: dict[str, Any]
) -> str:
    if "parts" in spec:
        anchors = spec.get("part_anchors") or {}
        chunks = []
        for a, b in spec["parts"]:
            chunk = slice_range(order, sections, a, b)
            chunk = apply_anchor(chunk, anchors.get(a))
            chunks.append(chunk)
        return clean_ws(" … ".join(chunks))
    text = slice_range(order, sections, spec["start"], spec["end"])
    return apply_anchor(text, spec.get("anchor"))


# --- scholarly Greek romanization (aligned with restore_dionysius_greek) ---

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
    "υ": "y",
    "φ": "ph",
    "χ": "ch",
    "ψ": "ps",
    "ω": "ō",
}


def romanize_greek(text: str) -> str:
    """Scholarly romanization; rough breathing -> initial h; accents dropped."""
    nfd = unicodedata.normalize("NFD", text)
    out: list[str] = []
    i = 0
    chars = list(nfd)
    while i < len(chars):
        ch = chars[i]
        if ch in "«»\"'′″“”᾽᾿":
            i += 1
            continue
        if ch in "··;:.,!?()[]{}—–‐-/\\…":
            out.append(";" if ch in "··" else ch)
            i += 1
            continue
        if ch.isspace():
            if out and out[-1] != " ":
                out.append(" ")
            i += 1
            continue
        if unicodedata.category(ch) == "Mn":
            i += 1
            continue

        low = ch.lower()
        # strip combining already via NFD; map base
        # handle precomposed that didn't decompose fully: fall through
        base = low
        # rough breathing combining was Mn and skipped; detect via original?
        # Use NFC char lookup for rough: check original composed form
        # Simpler path: use NFD and look at following Mn before we skipped —
        # re-scan with marks retained for breathing only.
        j = i + 1
        marks = []
        while j < len(chars) and unicodedata.category(chars[j]) == "Mn":
            marks.append(chars[j])
            j += 1
        rough = "\u0314" in marks  # combining reversed comma above

        if base in _BASE:
            # gamma nasal
            if base == "γ":
                k = j
                while k < len(chars) and unicodedata.category(chars[k]) == "Mn":
                    k += 1
                if k < len(chars) and chars[k].lower() in ("γ", "κ", "χ", "ξ"):
                    out.append("N" if ch.isupper() else "n")
                    i = j
                    continue
            tok = _BASE[base]
            if rough:
                if base == "ρ":
                    tok = "Rh" if ch.isupper() else "rh"
                else:
                    prev = out[-1] if out else " "
                    if prev == " " or not out:
                        tok = ("H" + tok) if ch.isupper() else ("h" + tok)
            out.append(tok.upper() if ch.isupper() and len(tok) == 1 else (
                tok[0].upper() + tok[1:] if ch.isupper() else tok
            ))
            i = j
            continue

        # leftover Greek letter?
        if "\u0370" <= ch <= "\u03FF" or "\u1F00" <= ch <= "\u1FFF":
            i += 1
            continue
        out.append(ch)
        i += 1

    return re.sub(r" +", " ", "".join(out)).strip()


def upsert_layer(
    unit: dict[str, Any], kind: str, body: str, label: str, provenance: str | None = None
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
            k = L.get("kind")
            if k in order and order.index(k) <= idx:
                pos = i + 1
        layers.insert(pos, existing)
    existing["label"] = label
    existing["body"] = body
    if provenance:
        existing["layer_provenance"] = provenance
    elif "layer_provenance" in existing:
        existing.pop("layer_provenance", None)


def dump_yaml(unit: dict[str, Any]) -> str:
    return yaml.safe_dump(
        unit, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120
    )


def atomic_write(path: Path, content: str) -> None:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(content)
        temp = Path(handle.name)
    temp.replace(path)


def short_id(unit_id: str) -> str:
    return unit_id.split(".", 1)[-1]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true", help="Apply updates to YAML + indexes")
    ap.add_argument("--refresh-cache", action="store_true", help="Rebuild Stephanus JSON from XML")
    args = ap.parse_args()

    if not XML_PATH.exists():
        raise SystemExit(
            f"Missing {XML_PATH}. Download Burnet Phaedo TEI from Perseus "
            "canonical-greekLit data/tlg0059/tlg004/tlg0059.tlg004.perseus-grc2.xml"
        )

    if args.refresh_cache or not JSON_CACHE.exists():
        order, sections = parse_stephanus(XML_PATH)
        JSON_CACHE.write_text(
            json.dumps({"order": order, "sections": sections}, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"wrote cache {JSON_CACHE} sections={len(sections)}")
    else:
        cache = json.loads(JSON_CACHE.read_text(encoding="utf-8"))
        order, sections = cache["order"], cache["sections"]

    yaml_paths = sorted(CANON.glob("phaedo_plato_phaedo_md_*.yml"))
    before = 0
    plans: list[dict[str, Any]] = []
    unmatched: list[str] = []

    for path in yaml_paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        uid = str(data["unit_id"])
        sid = short_id(uid)
        layers = {
            L["kind"]: L for L in (data.get("pratibha_layers") or []) if isinstance(L, dict)
        }
        orig = (layers.get("original") or {}).get("body") or ""
        if greek_char_count(orig) >= 8 and "not yet" not in orig.lower() and "not line-aligned" not in orig.lower():
            before += 1

        spec = LOCI.get(sid)
        if not spec:
            unmatched.append(uid)
            continue
        try:
            greek = build_passage(order, sections, spec)
        except (KeyError, ValueError) as exc:
            unmatched.append(f"{uid} ({exc})")
            continue
        if greek_char_count(greek) < 20:
            unmatched.append(f"{uid} (too little Greek)")
            continue
        iast = romanize_greek(greek)
        note = f"{PROV}; Stephanus {spec['cite']} ({spec['note']})"
        plans.append(
            {
                "path": path,
                "uid": uid,
                "sid": sid,
                "greek": greek,
                "iast": iast,
                "note": note,
                "cite": spec["cite"],
                "gchars": greek_char_count(greek),
                "words": len(greek.split()),
            }
        )

    print(f"units={len(yaml_paths)} before_greek={before}")
    print(f"planned_updates={len(plans)} unmatched={len(unmatched)}")
    if unmatched:
        print("unmatched:")
        for u in unmatched:
            print(" ", u)
    for p in plans:
        print(f"  {p['sid']}: {p['cite']} greek_chars={p['gchars']} words={p['words']}")

    if not args.write:
        print("dry-run only; pass --write to apply")
        return 0

    # --- write YAML ---
    updated_docs: dict[str, dict[str, Any]] = {}
    for plan in plans:
        path: Path = plan["path"]
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        greek, iast, note = plan["greek"], plan["iast"], plan["note"]
        upsert_layer(data, "original", greek, "Original", note)
        upsert_layer(data, "iast", iast, "IAST", "transliterated_from_greek")
        data["sanskrit_devanagari"] = greek
        data["sanskrit_iast"] = iast
        lp = data.get("layer_provenance")
        if not isinstance(lp, dict):
            lp = {}
        lp["original"] = note
        lp["iast"] = "transliterated_from_greek"
        data["layer_provenance"] = lp
        prov = data.get("provenance")
        if not isinstance(prov, dict):
            prov = {}
        prov["source_reference"] = note
        data["provenance"] = prov
        atomic_write(path, dump_yaml(data))
        updated_docs[plan["sid"]] = data

    # --- collection index (no pratibha_layers in current schema) ---
    coll_lines = COLL_INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
    new_coll: list[str] = []
    for line in coll_lines:
        if not line.strip():
            new_coll.append(line)
            continue
        row = json.loads(line)
        sid = short_id(str(row.get("unit_id") or ""))
        if sid in updated_docs:
            doc = updated_docs[sid]
            row["sanskrit_devanagari"] = doc["sanskrit_devanagari"]
            row["sanskrit_iast"] = doc["sanskrit_iast"]
            if isinstance(row.get("provenance"), dict) or "provenance" in doc:
                row["provenance"] = doc.get("provenance")
            new_coll.append(json.dumps(row, ensure_ascii=False) + "\n")
        else:
            new_coll.append(line)
    atomic_write(COLL_INDEX, "".join(new_coll))

    # --- main index ---
    main_lines = MAIN_INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
    new_main: list[str] = []
    seen: set[str] = set()
    for line in main_lines:
        if not line.strip():
            new_main.append(line)
            continue
        row = json.loads(line)
        uid = str(row.get("unit_id") or "")
        if uid.startswith("phaedo_plato.") or row.get("work_id") == WORK:
            sid = short_id(uid)
            if sid in updated_docs:
                doc = updated_docs[sid]
                # Prefer YAML as source of truth for synced fields
                row["sanskrit_devanagari"] = doc["sanskrit_devanagari"]
                row["sanskrit_iast"] = doc["sanskrit_iast"]
                row["pratibha_layers"] = doc["pratibha_layers"]
                if "layer_provenance" in doc:
                    row["layer_provenance"] = doc["layer_provenance"]
                if "provenance" in doc:
                    row["provenance"] = doc["provenance"]
                new_main.append(json.dumps(row, ensure_ascii=False) + "\n")
                seen.add(sid)
            else:
                new_main.append(line)
        else:
            new_main.append(line)
    atomic_write(MAIN_INDEX, "".join(new_main))

    after = 0
    for path in yaml_paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        layers = {
            L["kind"]: L for L in (data.get("pratibha_layers") or []) if isinstance(L, dict)
        }
        orig = (layers.get("original") or {}).get("body") or ""
        if greek_char_count(orig) >= 8:
            after += 1

    print(f"wrote {len(updated_docs)} YAML units; synced collection + main index.jsonl")
    print(f"after_greek={after}/{len(yaml_paths)} index_rows_touched={len(seen)}")
    missing = set(updated_docs) - seen
    if missing:
        print("WARNING: main index missing rows:", sorted(missing))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

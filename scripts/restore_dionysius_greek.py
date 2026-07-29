#!/usr/bin/env python3
"""Restore passage-level Greek originals for Pseudo-Dionysius canonical units.

Reads Migne-line Greek under data/raw_texts/pd/greek/, maps curated Rolt
excerpts to corresponding Greek, fills pratibha_layers original + iast
(romanization), updates top-level fields, and syncs collection + main
index.jsonl. Does not rewrite editorial English commentary/key_terms.
"""
from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
GREEK_DIR = ROOT / "data" / "raw_texts" / "pd" / "greek"
CANON = ROOT / "data" / "canonical" / "pseudo_dionysius"
MAIN_INDEX = ROOT / "data" / "canonical" / "index.jsonl"
COLL_INDEX = CANON / "index.jsonl"

SOURCE_NOTE = (
    "Greek: Migne PG / traditional Corpus Areopagiticum (Bibliotheca Augustana PG 3 "
    "for MT; Unicode DN aligned to same tradition). English alignment: C.E. Rolt, "
    "Dionysius the Areopagite on the Divine Names and the Mystical Theology (SPCK, 1920)."
)

GREEK_RE = re.compile(r"[\u0370-\u03FF\u1F00-\u1FFF]")


def clean_ws(text: str) -> str:
    text = text.replace("\xa0", " ")
    # Latin lookalikes adjacent to Greek (digital dumps)
    latin = {
        "A": "Α", "B": "Β", "E": "Ε", "H": "Η", "I": "Ι", "K": "Κ",
        "M": "Μ", "N": "Ν", "O": "Ο", "P": "Ρ", "T": "Τ", "X": "Χ",
        "Y": "Υ", "Z": "Ζ",
    }
    chars = list(text)
    for i, ch in enumerate(chars):
        if ch in latin:
            prev = chars[i - 1] if i else ""
            nxt = chars[i + 1] if i + 1 < len(chars) else ""
            if GREEK_RE.match(prev or "") or GREEK_RE.match(nxt or ""):
                chars[i] = latin[ch]
    text = "".join(chars)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s*\n\s*", " ", text)
    return text.strip()


def slice_between(text: str, start: str, end: str | None) -> str:
    i = text.find(start)
    if i < 0:
        raise ValueError(f"start not found: {start[:60]!r}")
    if end is None:
        return clean_ws(text[i:])
    j = text.find(end, i + len(start))
    if j < 0:
        raise ValueError(f"end not found after start: {end[:60]!r}")
    return clean_ws(text[i:j])


def load_dn_sections(path: Path) -> dict[str, str]:
    raw = path.read_text(encoding="utf-8")
    parts = re.split(r"\n\n(?=\d+\.\d+\.\s)", raw)
    secs: dict[str, str] = {}
    for part in parts:
        m = re.match(r"(\d+\.\d+)\.\s*(.*)$", part, re.S)
        if m:
            secs[m.group(1)] = clean_ws(m.group(2))
    return secs


def join_secs(secs: dict[str, str], keys: list[str]) -> str:
    missing = [k for k in keys if k not in secs]
    if missing:
        raise ValueError(f"missing DN sections: {missing}")
    return clean_ws(" ".join(secs[k] for k in keys))


# --- scholarly Greek romanization (deterministic) ---

_BASE = {
    "α": "a", "β": "b", "γ": "g", "δ": "d", "ε": "e", "ζ": "z", "η": "ē",
    "θ": "th", "ι": "i", "κ": "k", "λ": "l", "μ": "m", "ν": "n", "ξ": "x",
    "ο": "o", "π": "p", "ρ": "r", "σ": "s", "ς": "s", "τ": "t", "υ": "y",
    "φ": "ph", "χ": "ch", "ψ": "ps", "ω": "ō",
    "Α": "A", "Β": "B", "Γ": "G", "Δ": "D", "Ε": "E", "Ζ": "Z", "Η": "Ē",
    "Θ": "Th", "Ι": "I", "Κ": "K", "Λ": "L", "Μ": "M", "Ν": "N", "Ξ": "X",
    "Ο": "O", "Π": "P", "Ρ": "R", "Σ": "S", "Τ": "T", "Υ": "Y",
    "Φ": "Ph", "Χ": "Ch", "Ψ": "Ps", "Ω": "Ō",
}

# precomposed Greek with diacritics → (base letter lower/upper, rough?, accent ignored)
_PRECOMP: dict[str, tuple[str, bool]] = {}


def _build_precomp() -> None:
    # Map common precomposed forms via NFKD-ish manual table for Greek extended
    pairs = [
        ("ἀ", "α", False), ("ἁ", "α", True), ("ἂ", "α", False), ("ἃ", "α", True),
        ("ἄ", "α", False), ("ἅ", "α", True), ("ἆ", "α", False), ("ἇ", "α", True),
        ("Ἀ", "Α", False), ("Ἁ", "Α", True), ("Ἂ", "Α", False), ("Ἃ", "Α", True),
        ("Ἄ", "Α", False), ("Ἅ", "Α", True), ("Ἆ", "Α", False), ("Ἇ", "Α", True),
        ("ἐ", "ε", False), ("ἑ", "ε", True), ("ἒ", "ε", False), ("ἓ", "ε", True),
        ("ἔ", "ε", False), ("ἕ", "ε", True),
        ("Ἐ", "Ε", False), ("Ἑ", "Ε", True), ("Ἒ", "Ε", False), ("Ἓ", "Ε", True),
        ("Ἔ", "Ε", False), ("Ἕ", "Ε", True),
        ("ἠ", "η", False), ("ἡ", "η", True), ("ἢ", "η", False), ("ἣ", "η", True),
        ("ἤ", "η", False), ("ἥ", "η", True), ("ἦ", "η", False), ("ἧ", "η", True),
        ("Ἠ", "Η", False), ("Ἡ", "Η", True), ("Ἢ", "Η", False), ("Ἣ", "Η", True),
        ("Ἤ", "Η", False), ("Ἥ", "Η", True), ("Ἦ", "Η", False), ("Ἧ", "Η", True),
        ("ἰ", "ι", False), ("ἱ", "ι", True), ("ἲ", "ι", False), ("ἳ", "ι", True),
        ("ἴ", "ι", False), ("ἵ", "ι", True), ("ἶ", "ι", False), ("ἷ", "ι", True),
        ("Ἰ", "Ι", False), ("Ἱ", "Ι", True), ("Ἲ", "Ι", False), ("Ἳ", "Ι", True),
        ("Ἴ", "Ι", False), ("Ἵ", "Ι", True), ("Ἶ", "Ι", False), ("Ἷ", "Ι", True),
        ("ὀ", "ο", False), ("ὁ", "ο", True), ("ὂ", "ο", False), ("ὃ", "ο", True),
        ("ὄ", "ο", False), ("ὅ", "ο", True),
        ("Ὀ", "Ο", False), ("Ὁ", "Ο", True), ("Ὂ", "Ο", False), ("Ὃ", "Ο", True),
        ("Ὄ", "Ο", False), ("Ὅ", "Ο", True),
        ("ὐ", "υ", False), ("ὑ", "υ", True), ("ὒ", "υ", False), ("ὓ", "υ", True),
        ("ὔ", "υ", False), ("ὕ", "υ", True), ("ὖ", "υ", False), ("ὗ", "υ", True),
        ("Ὑ", "Υ", True), ("Ὓ", "Υ", True), ("Ὕ", "Υ", True), ("Ὗ", "Υ", True),
        ("ὠ", "ω", False), ("ὡ", "ω", True), ("ὢ", "ω", False), ("ὣ", "ω", True),
        ("ὤ", "ω", False), ("ὥ", "ω", True), ("ὦ", "ω", False), ("ὧ", "ω", True),
        ("Ὠ", "Ω", False), ("Ὡ", "Ω", True), ("Ὢ", "Ω", False), ("Ὣ", "Ω", True),
        ("Ὤ", "Ω", False), ("Ὥ", "Ω", True), ("Ὦ", "Ω", False), ("Ὧ", "Ω", True),
        ("ὰ", "α", False), ("ά", "α", False), ("ᾶ", "α", False), ("ᾳ", "α", False),
        ("ᾴ", "α", False), ("ᾷ", "α", False), ("ᾲ", "α", False),
        ("ὲ", "ε", False), ("έ", "ε", False),
        ("ὴ", "η", False), ("ή", "η", False), ("ῆ", "η", False), ("ῃ", "η", False),
        ("ῄ", "η", False), ("ῇ", "η", False), ("ῂ", "η", False),
        ("ὶ", "ι", False), ("ί", "ι", False), ("ῖ", "ι", False), ("ϊ", "ι", False),
        ("ΐ", "ι", False), ("ῒ", "ι", False), ("ῗ", "ι", False),
        ("ὸ", "ο", False), ("ό", "ο", False),
        ("ὺ", "υ", False), ("ύ", "υ", False), ("ῦ", "υ", False), ("ϋ", "υ", False),
        ("ΰ", "υ", False), ("ῢ", "υ", False), ("ῧ", "υ", False),
        ("ὼ", "ω", False), ("ώ", "ω", False), ("ῶ", "ω", False), ("ῳ", "ω", False),
        ("ῴ", "ω", False), ("ῷ", "ω", False), ("ῲ", "ω", False),
        ("ῤ", "ρ", False), ("ῥ", "ρ", True), ("Ῥ", "Ρ", True),
        ("Ά", "Α", False), ("Έ", "Ε", False), ("Ή", "Η", False), ("Ί", "Ι", False),
        ("Ό", "Ο", False), ("Ύ", "Υ", False), ("Ώ", "Ω", False),
        # iota-subscript forms
        ("ᾐ", "η", False), ("ᾑ", "η", True), ("ᾒ", "η", False), ("ᾓ", "η", True),
        ("ᾔ", "η", False), ("ᾕ", "η", True), ("ᾖ", "η", False), ("ᾗ", "η", True),
        ("ᾨ", "Ω", False), ("ᾩ", "Ω", True), ("ᾪ", "Ω", False), ("ᾫ", "Ω", True),
        ("Ὤ", "Ω", False), ("Ὥ", "Ω", True), ("Ὦ", "Ω", False), ("Ὧ", "Ω", True),
        ("ᾠ", "ω", False), ("ᾡ", "ω", True), ("ᾢ", "ω", False), ("ᾣ", "ω", True),
        ("ᾤ", "ω", False), ("ᾥ", "ω", True), ("ᾦ", "ω", False), ("ᾧ", "ω", True),
        ("ᾀ", "α", False), ("ᾁ", "α", True), ("ᾂ", "α", False), ("ᾃ", "α", True),
        ("ᾄ", "α", False), ("ᾅ", "α", True), ("ᾆ", "α", False), ("ᾇ", "α", True),
        ("ᾈ", "Α", False), ("ᾉ", "Α", True), ("ᾊ", "Α", False), ("ᾋ", "Α", True),
        ("ᾌ", "Α", False), ("ᾍ", "Α", True), ("ᾎ", "Α", False), ("ᾏ", "Α", True),
        ("ᾐ", "η", False), ("ᾑ", "η", True),
        ("ῌ", "Η", False), ("ῃ", "η", False),
    ]
    for ch, base, rough in pairs:
        _PRECOMP[ch] = (base, rough)


_build_precomp()


def _base_of(ch: str) -> tuple[str | None, bool]:
    """Return (base Greek letter, rough?) for a character."""
    # Latin lookalikes sometimes appear in digital dumps (Oὐκ, Aὐτῇ, …)
    latin_as_greek = {
        "A": "Α", "B": "Β", "E": "Ε", "H": "Η", "I": "Ι", "K": "Κ",
        "M": "Μ", "N": "Ν", "O": "Ο", "P": "Ρ", "T": "Τ", "X": "Χ",
        "Y": "Υ", "Z": "Ζ",
        "a": "α", "o": "ο", "i": "ι", "v": "ν",
    }
    if ch in latin_as_greek:
        ch = latin_as_greek[ch]
    if ch in _PRECOMP:
        return _PRECOMP[ch]
    if ch in _BASE:
        return ch, False
    return None, False


def romanize_greek(text: str) -> str:
    """Scholarly romanization without accents; initial h for rough breathing."""
    out: list[str] = []
    i = 0
    chars = list(text)
    while i < len(chars):
        ch = chars[i]
        if ch in "«»\"'′″“”":
            i += 1
            continue
        if ch in "··;:.,!?()[]{}—–‐-;/\\":
            out.append(ch if ch not in "··" else ";")
            i += 1
            continue
        if ch.isspace():
            if out and out[-1] != " ":
                out.append(" ")
            i += 1
            continue
        if ch in "0123456789":
            out.append(ch)
            i += 1
            continue

        base, rough = _base_of(ch)
        if base is None:
            # drop leftover combining marks / unknown Greek diacritic forms
            if "\u0300" <= ch <= "\u036f" or "\u1f00" <= ch <= "\u1fff" or "\u0370" <= ch <= "\u03ff":
                i += 1
                continue
            out.append(ch)
            i += 1
            continue

        # digraphs: αυ/ευ/ηυ/ου/υι
        digraph = None
        if i + 1 < len(chars):
            nb, _ = _base_of(chars[i + 1])
            pair = (base.lower() if base else "", (nb or "").lower())
            digraph_map = {
                ("α", "υ"): "au",
                ("ε", "υ"): "eu",
                ("η", "υ"): "ēu",
                ("ο", "υ"): "ou",
                ("υ", "ι"): "yi",
            }
            if pair in digraph_map:
                digraph = digraph_map[pair]
                if base.isupper():
                    digraph = digraph[0].upper() + digraph[1:]

        if digraph:
            roman = digraph
            consumed = 2
        else:
            roman = _BASE.get(base, base)
            consumed = 1
            # gamma nasal
            if base.lower() == "γ" and i + 1 < len(chars):
                nb, _ = _base_of(chars[i + 1])
                if (nb or "").lower() in ("γ", "κ", "ξ", "χ"):
                    roman = "n" if base.islower() else "N"

        if rough:
            prev = out[-1] if out else " "
            if base.lower() == "ρ":
                roman = "Rh" if (roman[:1].isupper()) else "rh"
            elif prev == " " or not out:
                if roman[:1].isupper():
                    roman = "H" + roman[:1].lower() + roman[1:]
                else:
                    roman = "h" + roman

        out.append(roman)
        i += consumed

    s = "".join(out)
    s = re.sub(r" +", " ", s).strip()
    return s


def build_passages() -> dict[str, str]:
    mt = (GREEK_DIR / "mystical_theology_migne_pg3.txt").read_text(encoding="utf-8")
    # Drop title line for slicing convenience
    if "Τριὰς ὑπερούσιε" in mt:
        mt = mt[mt.find("Τριὰς ὑπερούσιε") :]
    secs = load_dn_sections(GREEK_DIR / "divine_names_greek_unicode.txt")
    dn = (GREEK_DIR / "divine_names_greek_unicode.txt").read_text(encoding="utf-8")

    passages: dict[str, str] = {}

    # --- Mystical Theology ---
    passages["pd_mt_01"] = slice_between(mt, "Τριὰς ὑπερούσιε", "Ἐμοὶ μὲν οὖν")
    passages["pd_mt_02"] = slice_between(mt, "Ἐμοὶ μὲν οὖν", "Τούτων δὲ ὅρα")
    passages["pd_mt_03"] = slice_between(
        mt, "Καὶ γὰρ οὐχ ἁπλῶς ὁ θεῖος Μωϋσῆς", "Κατὰ τοῦτον ἡμεῖς"
    )
    passages["pd_mt_04"] = slice_between(mt, "Κατὰ τοῦτον ἡμεῖς", "Χρὴ δέ, ὡς οἶμαι")
    passages["pd_mt_05"] = slice_between(mt, "Χρὴ δέ, ὡς οἶμαι", "Ἐν μὲν οὖν ταῖς Θεολογικαῖς")
    passages["pd_mt_06"] = slice_between(mt, "Λέγομεν οὖν", "Αὖθις δὲ ἀνιόντες")
    passages["pd_mt_07"] = slice_between(mt, "Αὖθις δὲ ἀνιόντες", "οὔτε λόγος αὐτῆς ἐστιν")
    passages["pd_mt_08"] = slice_between(mt, "οὔτε λόγος αὐτῆς ἐστιν", None)

    # --- Divine Names ---
    passages["pd_dn_01"] = slice_between(dn, "Καθόλου τοιγαροῦν οὐ τολμητέον", "Ὥσπερ γὰρ ἄληπτα")
    passages["pd_dn_02"] = slice_between(
        dn,
        "Ὥσπερ γὰρ ἄληπτα",
        "1.2. Περὶ ταύτης οὖν",
    )
    # dn_03: Latin/Greek Omicron lookalike at start in source
    m = re.search(r"[OΟ]ὐ μὴν ἀκοινώνητόν ἐστι", dn)
    if not m:
        raise ValueError("dn_03 start not found")
    end = dn.find("1.3.", m.start())
    passages["pd_dn_03"] = clean_ws(dn[m.start() : end])

    # dn_04: DN II opening — Absolute Goodness defines/reveals whole Godhead; names of whole
    # Prefer the compressed statement matching Rolt's curated excerpt.
    p = secs["2.1"]
    # Start at the Absolute Goodness definition if present; else whole section head
    start = p.find("ἡ αὐτοαγαθότης ἀφορίζουσα")
    if start < 0:
        start = 0
    else:
        # include a short lead-in: Τὴν θεαρχικὴν ὅλην ὕπαρξιν…
        start = p.rfind("Τὴν θεαρχικὴν", 0, start + 1)
        if start < 0:
            start = 0
    chunk = p[start:]
    # End after the "whole/entire Godhead" insistence (before further Trinity distinctions)
    cut_markers = [
        "Καὶ ὅτι μὲν ἑνωμέναι πᾶσαί εἰσιν",
        "Καὶ ὅτι μὲν ἡνωμέναι",
        "Eἰ δέ τις φαίη",
        "Εἰ δέ τις φαίη",
    ]
    cut = -1
    for m in cut_markers:
        cut = chunk.find(m)
        if cut > 0:
            break
    # Also try a tighter cut after first few sentences if still huge
    passages["pd_dn_04"] = clean_ws(chunk if cut < 0 else chunk[:cut])
    if len(passages["pd_dn_04"]) > 1200:
        # Fall back: first two sentences of 2.1
        parts = re.split(r"(?<=\.)\s+", passages["pd_dn_04"])
        passages["pd_dn_04"] = clean_ws(" ".join(parts[:4]))

    # dn_05: ship / rock prayer image closing DN III.1
    passages["pd_dn_05"] = slice_between(
        dn,
        "Ἢ ὥσπερ εἰς ναῦν ἐμβεβηκότες",
        "3.2.",
    )

    # dn_06: Good / sun — 4.1 through sun analogy core
    p = secs["4.1"]
    # Include sun sentence; whole 4.1 is the right unit length
    passages["pd_dn_06"] = p

    passages["pd_dn_07"] = secs["4.34"]
    passages["pd_dn_08"] = secs["5.1"]
    passages["pd_dn_09"] = secs["6.1"]
    passages["pd_dn_10"] = secs["7.1"]
    # Power (VIII.2) + Peace (XI.1) — matches curated English composite
    passages["pd_dn_11"] = join_secs(secs, ["8.2", "11.1"])
    passages["pd_dn_12"] = join_secs(secs, ["13.1", "13.2"])

    return passages


def set_layer(layers: list, kind: str, body: str, provenance: str | None = None) -> list:
    layers = [dict(x) for x in layers]
    existing = next((L for L in layers if L.get("kind") == kind), None)
    payload: dict = {"kind": kind, "label": "Original" if kind == "original" else "IAST", "body": body}
    if provenance:
        payload["layer_provenance"] = provenance
    if existing:
        existing.clear()
        existing.update(payload)
        # keep label convention
        if kind == "original":
            existing["label"] = "Original"
        elif kind == "iast":
            existing["label"] = "IAST"
    else:
        # insert original/iast before translation
        insert_at = 0
        for i, L in enumerate(layers):
            if L.get("kind") == "translation":
                insert_at = i
                break
        else:
            insert_at = 0
        if kind == "iast":
            # after original if present
            for i, L in enumerate(layers):
                if L.get("kind") == "original":
                    insert_at = i + 1
                    break
        layers.insert(insert_at, payload)
    # enforce order: original, iast, then rest
    order = {"original": 0, "iast": 1}
    head = [L for L in layers if L.get("kind") in order]
    tail = [L for L in layers if L.get("kind") not in order]
    head.sort(key=lambda L: order.get(L.get("kind"), 99))
    return head + tail


def dump_yaml(path: Path, data: dict) -> None:
    text = yaml.safe_dump(
        data,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=100,
    )
    path.write_text(text, encoding="utf-8")


def atomic_write(path: Path, content: str) -> None:
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(content)
        tmp = Path(handle.name)
    tmp.replace(path)


def sync_indexes(units: dict[str, dict]) -> None:
    # collection index
    lines = []
    for uid in sorted(units):
        lines.append(json.dumps(units[uid], ensure_ascii=False) + "\n")
    atomic_write(COLL_INDEX, "".join(lines))

    # main index: replace PD rows in place
    main_lines = MAIN_INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
    out = []
    seen = set()
    for line in main_lines:
        if not line.strip():
            out.append(line)
            continue
        obj = json.loads(line)
        wid = obj.get("work_id")
        uid = obj.get("unit_id", "")
        if wid == "pseudo_dionysius" or str(uid).startswith("pseudo_dionysius."):
            key = uid.split(".", 1)[-1].lower()
            # unit_id like pseudo_dionysius.pd_mt_01
            short = uid.split(".")[-1].lower()
            if short in units:
                out.append(json.dumps(units[short], ensure_ascii=False) + "\n")
                seen.add(short)
            else:
                out.append(line)
        else:
            out.append(line)
    missing = set(units) - seen
    if missing:
        # append any missing at end (should not happen)
        for short in sorted(missing):
            out.append(json.dumps(units[short], ensure_ascii=False) + "\n")
    atomic_write(MAIN_INDEX, "".join(out))


def main() -> int:
    passages = build_passages()
    updated: dict[str, dict] = {}
    before = after = 0

    for path in sorted(CANON.glob("pseudo_dionysius_pd_*.yml")):
        short = path.stem.replace("pseudo_dionysius_", "")  # pd_mt_01
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        layers = list(doc.get("pratibha_layers") or [])
        old_orig = next((L.get("body", "") for L in layers if L.get("kind") == "original"), "")
        if GREEK_RE.search(old_orig or ""):
            before += 1

        greek = passages[short]
        iast = romanize_greek(greek)
        layers = set_layer(layers, "original", greek, provenance="sourced")
        layers = set_layer(layers, "iast", iast)

        doc["pratibha_layers"] = layers
        doc["sanskrit_devanagari"] = greek
        doc["sanskrit_iast"] = iast
        prov = dict(doc.get("provenance") or {})
        prov["source_reference"] = SOURCE_NOTE
        doc["provenance"] = prov

        dump_yaml(path, doc)
        updated[short] = doc
        if GREEK_RE.search(greek):
            after += 1
        print(f"{short}: greek_chars={len(GREEK_RE.findall(greek))} translit_len={len(iast)}")

    sync_indexes(updated)
    print(f"coverage original Greek Unicode: before={before} after={after} / {len(updated)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

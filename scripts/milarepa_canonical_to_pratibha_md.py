#!/usr/bin/env python3
"""Regenerate data/pratibha_md/milarepa_songs_pilot.md from canonical YAML units."""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CANON_DIR = ROOT / "data" / "canonical" / "milarepa_songs"
MANIFEST = ROOT / "data" / "raw_texts" / "milarepa_pilot" / "manifest.json"
OUT_MD = ROOT / "data" / "pratibha_md" / "milarepa_songs_pilot.md"
PILOT_DIR = ROOT / "data" / "raw_texts" / "milarepa_pilot"


def _layer_body(doc: dict, kind: str) -> str:
    for layer in doc.get("pratibha_layers") or []:
        if layer.get("kind") == kind:
            return (layer.get("body") or "").strip()
    return ""


def _layer_items_md(doc: dict, kind: str, heading: str) -> str:
    for layer in doc.get("pratibha_layers") or []:
        if layer.get("kind") != kind:
            continue
        items = layer.get("items") or []
        if not items:
            body = (layer.get("body") or "").strip()
            return f"### {heading}\n{body}" if body else ""
        lines = [f"### {heading}", ""]
        for item in items:
            if kind == "key_terms":
                lines.append(f"**{item.get('term', '')}** — {item.get('definition', '')}")
            else:
                cite = item.get("citation", "")
                res = item.get("resonance", "")
                div = item.get("divergence", "")
                block = f"**{cite}:** {res}"
                if div:
                    block += f"\n*Divergence:* {div}"
                lines.append(block)
        return "\n".join(lines)
    return ""


def _clean_anchor(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Drop Evans-Wentz footnote blocks (numbered editorial notes)
    lines: list[str] = []
    skip = False
    for line in text.split("\n"):
        if re.match(r"^\s*\d+\s+That is,", line):
            skip = True
            continue
        if skip and line.strip() == "":
            skip = False
            continue
        if skip:
            continue
        if re.match(r"^\s*CHAP\.", line, re.I):
            continue
        lines.append(line.rstrip())
    out = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", out).strip()


def _unit_section(doc: dict, manifest_entry: dict) -> str:
    sid = doc.get("source_id", "")
    title = doc.get("title", "Untitled")
    pilot_title = manifest_entry.get("title", title)
    chapter = manifest_entry.get("chapter", "X")
    source = (
        f"Milarepa, *Tibet's Great Yogi Milarepa*, Chapter {chapter}, "
        f"{pilot_title} ({sid}; Evans-Wentz 1928 / Dawa-Samdup translation)"
    )

    pilot_file = manifest_entry.get("file", "")
    body = ""
    if pilot_file:
        p = ROOT / pilot_file if not pilot_file.startswith("/") else Path(pilot_file)
        if p.exists():
            body = _clean_anchor(p.read_text(encoding="utf-8"))

    original = _layer_body(doc, "original")
    wylie = _layer_body(doc, "iast")
    translation = _layer_body(doc, "translation") or doc.get("translation_literal", "")
    commentary = _layer_body(doc, "commentary")
    practice = _layer_body(doc, "practice") or doc.get("practice", "")
    key_terms = _layer_items_md(doc, "key_terms", "Key Terms")
    resonances = _layer_items_md(doc, "resonances", "Cross-Tradition Resonances")

    orig_label = "Original (Tibetan)"
    for layer in doc.get("pratibha_layers") or []:
        if layer.get("kind") == "original":
            orig_label = layer.get("label") or orig_label
            break

    parts = [
        f"## {title}",
        f"**Source:** {source}",
        "",
        body,
        "",
        "---",
        "",
        f"### {orig_label}",
        original or "_Tibetan witness pending; Evans-Wentz English anchor in body above._",
        "",
        "### Wylie / Key Terms",
        wylie or "_See Key Terms below._",
        "",
        "### Pratibha Translation",
        translation,
        "",
        "### Pratibha Commentary",
        commentary,
        "",
    ]
    if key_terms:
        parts.extend([key_terms, ""])
    if resonances:
        parts.extend([resonances, ""])
    parts.extend(
        [
            "### Practice (Abhyasa)",
            practice,
            "",
            "---",
            "",
        ]
    )
    return "\n".join(parts)


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_id = {m["sutra_id"]: m for m in manifest}

    header = """# Pratibha — Milarepa Songs (Pilot)
**Corpus entry:** Tibetan Buddhist / Kagyü / 11th–12th century CE
**Anchor:** W.Y. Evans-Wentz (ed.), *Tibet's Great Yogi Milarepa* (1928); Kazi Dawa-Samdup translation (public domain)
**Pilot:** Chapter X songs — Meditation in Solitude

---

"""

    sections: list[str] = []
    for entry in manifest:
        sid = entry["sutra_id"]
        slug = sid.lower()
        path = CANON_DIR / f"milarepa_songs_{slug}.yml"
        if not path.exists():
            print(f"  skip missing: {path.name}")
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        sections.append(_unit_section(doc, entry))
        print(f"  md: {sid}")

    OUT_MD.write_text(header + "".join(sections).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT_MD.relative_to(ROOT)} ({len(sections)} units)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

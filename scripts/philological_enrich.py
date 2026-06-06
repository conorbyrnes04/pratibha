#!/usr/bin/env python3
"""Philologically honest PD enrichment: anchor appendix + Pratibha layers.

Separates public-domain anchor text from sell-ready Pratibha translation, adds
Key Terms, resonances (where catalogued), and educational commentary.

COPYRIGHT GUARDRAIL — read before extending:
This converter calls ``normalize_patrick_heraclitus`` and ``normalize_giles_excerpt``
from ``philological_lib``. Those normalization functions are ONLY for genuinely
public-domain source translations (Patrick 1889, Giles 1889, etc.). Applying
word-substitution to a copyrighted translation does NOT create an original work
and is a copyright violation. Do not extend these functions to in-copyright sources.

Usage:
  python scripts/philological_enrich.py --collection heraclitus_fragments
  python scripts/philological_enrich.py --collection the_book_of_chuang_tzu
  python scripts/philological_enrich.py --all --canonicalize
  python scripts/philological_enrich.py --all --canonicalize --llm  # when API keys set
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

from philological_lib import (  # noqa: E402
    CHAPTER_INTROS,
    HERACLITUS_RESONANCES,
    PROVENANCE_GILES_NORMALIZED,
    PROVENANCE_HAND_CONSTANT,
    PROVENANCE_PATRICK_NORMALIZED,
    PROVENANCE_TEMPLATE,
    chapter_commentary,
    clean_ocr,
    heraclitus_commentary,
    heraclitus_key_terms,
    heraclitus_practice,
    normalize_giles_excerpt,
    normalize_patrick_heraclitus,
    strip_commentary_layers,
    strip_giles_footnote_blocks,
    yaml_key_terms_to_layers,
)

COLLECTION_DIRS = {
    "heraclitus_fragments": ROOT / "data" / "yaml" / "fragments",
    "the_book_of_chuang_tzu": ROOT / "data" / "yaml" / "the_book_of_chuang_tzu",
    "zhuangzi_pratibha": ROOT / "data" / "yaml" / "zhuangzi_pratibha",
}

HERACLITUS_SYSTEM = """You are a Pratibha editor for Heraclitus fragments. Return ONLY JSON:
{
  "title": "thematic title (not 'Fragment 12')",
  "pratibha_translation": "fresh English, present tense where apt; use Logos for λόγος; do NOT copy Patrick verbatim",
  "commentary": ">=120 words. Open with philosophical claim. Cite Patrick as anchor, note Greek terms. Name contested move.",
  "key_terms": [{"term": "...", "definition": "etymology -> Heraclitean meaning -> translation stakes"}],
  "resonances": [{"citation": "Author, work, passage", "resonance": "structural homology", "divergence": "where it breaks"}],
  "practice": "one executable instruction from THIS fragment"
}
Rules: 1-3 key_terms; 1-2 resonances with divergence; commentary original not paraphrase."""

CHUANG_SYSTEM = """You are a Pratibha editor for Zhuangzi chapter excerpts. Return ONLY JSON:
{
  "pratibha_translation": "modern English excerpt (~400-800 words max) from the anchor; use Kun/Peng not Leviathan/Rukh",
  "commentary": ">=150 words on the chapter's philosophical movement; mention Giles 1889 as PD anchor",
  "key_terms": [{"term": "pinyin (汉字)", "definition": "graph -> Zhuangzi meaning -> translation stakes"}],
  "resonances": [{"citation": "...", "resonance": "...", "divergence": "..."}],
  "practice": "one executable instruction"
}
Use received Chinese names. Do not reproduce Giles footnotes."""


def _save_yaml(path: Path, data: dict[str, Any]) -> None:
    path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False, width=100),
        encoding="utf-8",
    )


def _template_heraclitus_commentary(commentary: str) -> bool:
    return "Anchor: George T.W. Patrick" in str(commentary or "")


def is_human_revised_heraclitus(data: dict[str, Any]) -> bool:
    """Unit has hand-authored layers beyond regex/template assembly."""
    comm = str(data.get("commentary") or "")
    if comm and not _template_heraclitus_commentary(comm):
        return True
    anchor = clean_ocr(str(data.get("anchor_translation") or data.get("translation") or ""))
    pratibha = str(data.get("pratibha_translation") or data.get("translation") or "")
    if anchor and pratibha and normalize_patrick_heraclitus(anchor) != clean_ocr(pratibha):
        return True
    return False


def is_human_revised_chuang(data: dict[str, Any], md: dict[str, Any] | None) -> bool:
    """Chapter enriched from zhuangzi_pratibha MD (hand-authored pilot units)."""
    return bool(md)


def _set_layer_provenance(data: dict[str, Any], mapping: dict[str, str]) -> None:
    existing = dict(data.get("layer_provenance") or {})
    existing.update(mapping)
    data["layer_provenance"] = existing


def _heraclitus_template_provenance(n: int) -> dict[str, str]:
    out = {
        "translation": PROVENANCE_PATRICK_NORMALIZED,
        "commentary": PROVENANCE_TEMPLATE,
        "key_terms": PROVENANCE_TEMPLATE,
        "practice": PROVENANCE_TEMPLATE,
    }
    if n in HERACLITUS_RESONANCES:
        out["resonances"] = PROVENANCE_HAND_CONSTANT
    return out


def _chuang_template_provenance() -> dict[str, str]:
    return {
        "translation": PROVENANCE_GILES_NORMALIZED,
        "commentary": PROVENANCE_TEMPLATE,
        "practice": PROVENANCE_TEMPLATE,
    }


def _frag_num(path: Path, data: dict[str, Any]) -> int:
    m = re.search(r"fragment_(\d+)", path.name)
    if m:
        return int(m.group(1))
    sid = str(data.get("sutra_id") or "")
    m2 = re.search(r"P(\d+)", sid, re.I)
    return int(m2.group(1)) if m2 else 0


def _ch_num(path: Path, data: dict[str, Any]) -> int:
    if data.get("chapter_number"):
        return int(data["chapter_number"])
    m = re.search(r"ch_(\d+)", path.name)
    return int(m.group(1)) if m else 0


def enrich_heraclitus(path: Path, data: dict[str, Any], use_llm: bool, relabel_only: bool = False) -> bool:
    anchor = clean_ocr(str(data.get("anchor_translation") or data.get("translation") or ""))
    if not anchor:
        return False
    n = _frag_num(path, data)
    changed = False
    human = is_human_revised_heraclitus(data)

    if relabel_only:
        if human:
            return False
        _set_layer_provenance(data, _heraclitus_template_provenance(n))
        if data.get("editorial_maturity") != "structural_draft":
            data["editorial_maturity"] = "structural_draft"
        return True

    data["anchor_translation"] = anchor
    data["source_reference"] = f"Patrick (1889), frag. {n}; corpus HFR_P{n:03d}"
    data["transliteration"] = data.get("transliteration") or "*(Greek original not in corpus; see Patrick/Bywater.)*"

    if use_llm:
        return False  # filled by async batch

    if human:
        return False

    pratibha = normalize_patrick_heraclitus(anchor)
    if data.get("pratibha_translation") != pratibha:
        data["pratibha_translation"] = pratibha
        changed = True
    if data.get("translation") != pratibha:
        data["translation"] = pratibha
        changed = True

    comm = heraclitus_commentary(anchor, n)
    if data.get("commentary") != comm:
        data["commentary"] = comm
        changed = True

    kt = heraclitus_key_terms(anchor)
    if kt and data.get("key_terms") != kt:
        data["key_terms"] = kt
        changed = True

    res = HERACLITUS_RESONANCES.get(n, [])
    if res and data.get("resonances") != res:
        data["resonances"] = res
        changed = True

    practice = heraclitus_practice(anchor)
    if data.get("abhyasa") != practice:
        data["abhyasa"] = practice
        changed = True

    title = data.get("title") or ""
    if len(title) > 100 or title.lower().startswith("to this universal"):
        new_title = pratibha.split(".")[0][:90].strip()
        if new_title and new_title != title:
            data["title"] = new_title
            changed = True

    _set_layer_provenance(data, _heraclitus_template_provenance(n))
    if data.get("editorial_maturity") != "structural_draft":
        data["editorial_maturity"] = "structural_draft"
        changed = True
    return changed


def restructure_chuang_chapter(data: dict[str, Any]) -> bool:
    """Move full Giles chapter out of commentary into anchor_chapter."""
    comm = str(data.get("commentary") or "")
    trans = str(data.get("translation") or "")
    changed = False
    if len(comm) > max(4000, len(trans) * 3):
        cleaned = strip_giles_footnote_blocks(comm)
        if data.get("anchor_chapter") != cleaned:
            data["anchor_chapter"] = cleaned
            changed = True
        if not data.get("anchor_translation"):
            data["anchor_translation"] = clean_ocr(trans) or clean_ocr(cleaned[:1500])
            changed = True
    elif comm and not data.get("anchor_chapter"):
        data["anchor_chapter"] = strip_giles_footnote_blocks(comm)
        changed = True
    return changed


def giles_chapter_excerpt(data: dict[str, Any]) -> str:
    """First substantial paragraph of the PD chapter for display excerpt."""
    full = strip_giles_footnote_blocks(
        str(data.get("anchor_chapter") or data.get("anchor_translation") or data.get("translation") or "")
    )
    paras = [p.strip() for p in re.split(r"\n\s*\n", full) if len(p.strip()) > 80]
    if paras:
        return paras[0][:1000]
    return clean_ocr(full[:1000])


def enrich_chuang_chapter(
    path: Path, data: dict[str, Any], md_by_chapter: dict[int, dict], use_llm: bool, relabel_only: bool = False
) -> bool:
    if not path.name.startswith("ch_"):
        return False
    n = _ch_num(path, data)
    md = md_by_chapter.get(n)
    human = is_human_revised_chuang(data, md)

    if relabel_only:
        if human:
            return False
        _set_layer_provenance(data, _chuang_template_provenance())
        if data.get("editorial_maturity") != "structural_draft":
            data["editorial_maturity"] = "structural_draft"
            return True
        return bool(data.get("layer_provenance"))

    changed = restructure_chuang_chapter(data)
    anchor = clean_ocr(str(data.get("anchor_translation") or data.get("translation") or ""))
    title = str(data.get("title") or f"Chapter {n}")

    if md:
        if md.get("sanskrit") and data.get("sanskrit") != md["sanskrit"]:
            data["sanskrit"] = md["sanskrit"]
            changed = True
        if md.get("transliteration") and not data.get("transliteration"):
            data["transliteration"] = md["transliteration"]
            changed = True
        if md.get("key_terms"):
            data["key_terms"] = md["key_terms"]
            changed = True
        if md.get("resonances"):
            data["resonances"] = md["resonances"]
            changed = True

    if use_llm:
        return changed

    excerpt = giles_chapter_excerpt(data)
    anchor = clean_ocr(str(data.get("anchor_translation") or excerpt))
    if not data.get("anchor_translation"):
        data["anchor_translation"] = anchor[:2000]
        changed = True

    if human and md:
        pratibha = md.get("pratibha_translation") or data.get("pratibha_translation")
        if pratibha and (data.get("pratibha_translation") != pratibha or data.get("translation") != pratibha):
            data["pratibha_translation"] = pratibha
            data["translation"] = pratibha
            changed = True
        if md.get("commentary"):
            comm = strip_commentary_layers(md["commentary"])
            if data.get("commentary") != comm:
                data["commentary"] = comm
                changed = True
        if md.get("abhyasa") and data.get("abhyasa") != md["abhyasa"]:
            data["abhyasa"] = md["abhyasa"]
            changed = True
        data["source_reference"] = f"Giles (1889), chapter {n}; Project Gutenberg #59709"
        return changed

    pratibha = normalize_giles_excerpt(excerpt)
    if data.get("pratibha_translation") != pratibha or data.get("translation") != pratibha:
        data["pratibha_translation"] = pratibha
        data["translation"] = pratibha
        changed = True

    comm = chapter_commentary(n, title, excerpt)
    if data.get("commentary") != comm:
        data["commentary"] = comm
        changed = True

    if not data.get("abhyasa"):
        data["abhyasa"] = (
            "Read the Pratibha excerpt, then open the Giles appendix and compare one sentence "
            "where the mythic names differ — note what philosophical work the naming does."
        )
        changed = True

    data["source_reference"] = f"Giles (1889), chapter {n}; Project Gutenberg #59709"
    _set_layer_provenance(data, _chuang_template_provenance())
    if data.get("editorial_maturity") != "structural_draft":
        data["editorial_maturity"] = "structural_draft"
        changed = True
    return changed


def load_zhuangzi_md_by_chapter() -> dict[int, dict[str, Any]]:
    """Map inner-chapter MD units to chapter numbers (pilot: md index ~= primary chapter focus)."""
    md_dir = COLLECTION_DIRS["zhuangzi_pratibha"]
    out: dict[int, dict[str, Any]] = {}
    for path in sorted(md_dir.glob("zhuangzi_md_*.yml")):
        m = re.search(r"zhuangzi_md_(\d+)", path.name)
        if not m:
            continue
        idx = int(m.group(1))
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        # Pilot MD units align with inner chapters 1-15 thematically.
        ch = idx
        out[ch] = {
            "sanskrit": data.get("sanskrit"),
            "transliteration": data.get("transliteration"),
            "pratibha_translation": data.get("pratibha_translation") or data.get("translation"),
            "commentary": data.get("commentary"),
            "abhyasa": data.get("abhyasa"),
            "key_terms": _parse_md_key_terms(data.get("commentary") or ""),
            "resonances": _parse_md_resonances(data.get("commentary") or ""),
        }
    return out


def _parse_md_key_terms(commentary: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    block = re.search(r"(?is)key terms:\s*(.+?)(?:cross-tradition|$)", commentary)
    if not block:
        return items
    for m in re.finditer(r"\*\*([^*]+)\*\*\s*-\s*(.+?)(?=\n\n\*\*|\n\nCross|$)", block.group(1), re.S):
        items.append({"term": m.group(1).strip(), "definition": re.sub(r"\s+", " ", m.group(2).strip())})
    return items[:6]


def _parse_md_resonances(commentary: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    block = re.search(r"(?is)cross-tradition resonances:\s*(.+?)(?:\n\nPractice|\Z)", commentary)
    if not block:
        return items
    for part in re.split(r"\n\n(?=\*\*)", block.group(1).strip()):
        part = part.strip()
        if not part.startswith("**"):
            continue
        inner = part.lstrip("*")
        m = re.match(r"^(.+?):\*\*\s*(.+)", inner, re.S)
        if not m:
            continue
        citation = m.group(1).strip()
        body = m.group(2).strip()
        div_m = re.search(r"(?is)\*Divergence:\*\s*(.+)", body)
        resonance = re.sub(r"(?is)\*Divergence:\*\s*.+", "", body).strip()
        divergence = div_m.group(1).strip() if div_m else ""
        if citation and resonance:
            items.append({"citation": citation, "resonance": resonance, "divergence": divergence})
    return items[:4]


async def _llm_json(system: str, user: str) -> dict[str, Any]:
    from app.llm import smart_chat  # noqa: E402

    text = await smart_chat(
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
        temperature=0.35,
    )
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


async def llm_enrich_heraclitus(paths: list[Path]) -> int:
    count = 0
    for path in paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        anchor = clean_ocr(str(data.get("anchor_translation") or ""))
        n = _frag_num(path, data)
        if not anchor:
            continue
        try:
            out = await _llm_json(
                HERACLITUS_SYSTEM,
                f"Fragment {n}\nPatrick (1889) anchor:\n{anchor}",
            )
        except Exception as e:
            print(f"  LLM skip {path.name}: {e}")
            continue
        for k in ("title", "pratibha_translation", "commentary", "key_terms", "resonances", "practice"):
            if out.get(k):
                data[k if k != "practice" else "abhyasa"] = out[k]
        data["translation"] = data.get("pratibha_translation") or data.get("translation")
        _save_yaml(path, data)
        count += 1
    return count


def main() -> int:
    ap = argparse.ArgumentParser(description="Philological PD enrichment for Pratibha corpus.")
    ap.add_argument("--collection", choices=list(COLLECTION_DIRS.keys()))
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--canonicalize", action="store_true")
    ap.add_argument("--llm", action="store_true", help="Use LLM when API keys are configured")
    ap.add_argument(
        "--relabel-only",
        action="store_true",
        help="Set layer_provenance and structural_draft on template units only; do not rewrite content",
    )
    ap.add_argument("--prefix", default="")
    args = ap.parse_args()
    if not args.all and not args.collection:
        ap.error("Specify --collection or --all")

    targets = list(COLLECTION_DIRS.keys()) if args.all else [args.collection]
    md_map = load_zhuangzi_md_by_chapter() if "the_book_of_chuang_tzu" in targets else {}

    for coll in targets:
        if coll == "zhuangzi_pratibha":
            continue
        d = COLLECTION_DIRS[coll]
        paths = sorted(d.glob("*.yml"))
        if args.prefix:
            paths = [p for p in paths if p.name.startswith(args.prefix)]

        if args.llm and coll == "heraclitus_fragments":
            n = asyncio.run(llm_enrich_heraclitus(paths))
            print(f"{coll}: LLM enriched {n} files")
            continue

        n = 0
        for path in paths:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            if coll == "heraclitus_fragments":
                ok = enrich_heraclitus(path, data, args.llm, relabel_only=args.relabel_only)
            elif coll == "the_book_of_chuang_tzu":
                ok = enrich_chuang_chapter(path, data, md_map, args.llm, relabel_only=args.relabel_only)
            else:
                ok = False
            if ok:
                _save_yaml(path, data)
                n += 1
        print(f"{coll}: enriched {n} files")

    if args.canonicalize:
        subprocess.run([sys.executable, str(ROOT / "scripts" / "canonicalize_texts.py")], check=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Restore Classical Chinese into 3 zhuangzi_md units missing CJK in original.

Source: received traditional Chinese (Wikisource 莊子 + Haodoo 好讀 via
andy0130tw.github.io/zhuangzi), public domain. Passages matched to each unit's
English excerpt by chapter/episode.

Usage:
  python scripts/restore_zhuangzi_md_cjk.py          # dry-run
  python scripts/restore_zhuangzi_md_cjk.py --write  # apply YAML + index.jsonl
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CANON = ROOT / "data/canonical/the_book_of_chuang_tzu"
INDEX = ROOT / "data/canonical/index.jsonl"

CJK = re.compile(r"[\u4e00-\u9fff]")
IAST_NOTE = (
    "*(Chinese source text; no Sanskrit original. "
    "Pinyin with tones for key terms is provided in Key Terms.)*"
)
LAYER_PROV = (
    "restored from PD Classical Chinese (Wikisource 莊子 / Haodoo 好讀 traditional); "
    "passage matched to unit English"
)

# Passage texts: traditional characters, paragraph breaks matching sibling md units.
UNITS: dict[str, dict[str, str]] = {
    "the_book_of_chuang_tzu.zhuangzi_md_010": {
        "file": "the_book_of_chuang_tzu_zhuangzi_md_010.yml",
        "chapter": "齊物論 (ch. 2)",
        "chinese": (
            "夢飲酒者，旦而哭泣；夢哭泣者，旦而田獵。方其夢也，不知其夢也。"
            "夢之中又占其夢焉，覺而後知其夢也。"
            "且有大覺而後知此其大夢也，而愚者自以為覺，竊竊然知之。"
        ),
        "source_reference": (
            "Zhuangzi 齊物論; PD Chinese via Wikisource 莊子/齊物論 "
            "and Haodoo 好讀 (andy0130tw.github.io/zhuangzi ch.2)"
        ),
    },
    "the_book_of_chuang_tzu.zhuangzi_md_013": {
        "file": "the_book_of_chuang_tzu_zhuangzi_md_013.yml",
        "chapter": "天道 (ch. 13) — 輪扁",
        "chinese": (
            "桓公讀書於堂上，輪扁斲輪於堂下，釋椎鑿而上，問桓公曰：「敢問公之所讀者何言邪？」\n\n"
            "公曰：「聖人之言也。」\n\n"
            "曰：「聖人在乎？」\n\n"
            "公曰：「已死矣。」\n\n"
            "曰：「然則君之所讀者，古人之糟魄已夫！」\n\n"
            "桓公曰：「寡人讀書，輪人安得議乎？有說則可，無說則死。」\n\n"
            "輪扁曰：「臣也以臣之事觀之。斲輪，徐則甘而不固，疾則苦而不入。"
            "不徐不疾，得之於手而應於心，口不能言，有數存焉於其間。"
            "臣不能以喻臣之子，臣之子亦不能受之於臣，是以行年七十而老斲輪。"
            "古之人與其不可傳也死矣，然則君之所讀者，古人之糟魄已夫！」"
        ),
        "source_reference": (
            "Zhuangzi 天道 (Wheelwright Bian); PD Chinese via Wikisource 莊子/天道 "
            "and Haodoo 好讀 (andy0130tw.github.io/zhuangzi ch.13)"
        ),
    },
    "the_book_of_chuang_tzu.zhuangzi_md_014": {
        "file": "the_book_of_chuang_tzu_zhuangzi_md_014.yml",
        "chapter": "達生 (ch. 19) — 呂梁",
        "chinese": (
            "孔子觀於呂梁，縣水三十仞，流沫四十里，黿鼉魚鼈之所不能游也。"
            "見一丈夫游之，以為有苦而欲死也，使弟子並流而拯之。"
            "數百步而出，被髮行歌而游於塘下。\n\n"
            "孔子從而問焉，曰：「吾以子為鬼，察子則人也。請問，蹈水有道乎？」\n\n"
            "曰：「亡，吾無道。吾始乎故，長乎性，成乎命。"
            "與齊俱入，與汩偕出，從水之道而不為私焉。此吾所以蹈之也。」\n\n"
            "孔子曰：「何謂始乎故，長乎性，成乎命？」\n\n"
            "曰：「吾生於陵而安於陵，故也；長於水而安於水，性也；"
            "不知吾所以然而然，命也。」"
        ),
        "source_reference": (
            "Zhuangzi 達生 (Lüliang swimmer); PD Chinese via Wikisource 莊子/達生 "
            "and Haodoo 好讀 (andy0130tw.github.io/zhuangzi ch.19)"
        ),
    },
}


def set_original(data: dict, chinese: str) -> None:
    data["sanskrit_devanagari"] = chinese
    data["sanskrit_iast"] = IAST_NOTE
    layers = data.get("pratibha_layers")
    if not isinstance(layers, list):
        raise ValueError("pratibha_layers missing")
    for layer in layers:
        if isinstance(layer, dict) and layer.get("kind") == "original":
            layer["body"] = chinese
            layer["layer_provenance"] = LAYER_PROV
            return
    raise ValueError("original layer missing")


def set_provenance(data: dict, source_reference: str) -> None:
    prov = data.get("provenance")
    if isinstance(prov, dict):
        prov["source_reference"] = source_reference


def coverage_work() -> tuple[int, int]:
    total = 0
    with_cjk = 0
    for path in sorted(CANON.glob("*.yml")):
        total += 1
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        layers = data.get("pratibha_layers") or []
        orig = next(
            (L for L in layers if isinstance(L, dict) and L.get("kind") == "original"),
            None,
        )
        body = (orig or {}).get("body") or data.get("sanskrit_devanagari") or ""
        if CJK.search(str(body)):
            with_cjk += 1
    return with_cjk, total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    before = coverage_work()
    print(f"coverage before: {before[0]}/{before[1]}")

    index_lines = INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
    if any(not ln.strip() for ln in index_lines):
        raise SystemExit("index.jsonl has blank lines; refusing")
    index_units = [json.loads(ln) for ln in index_lines]
    by_uid = {u["unit_id"]: i for i, u in enumerate(index_units)}

    for uid, meta in UNITS.items():
        path = CANON / meta["file"]
        chinese = meta["chinese"]
        assert CJK.search(chinese), uid
        print(f"\n{uid} [{meta['chapter']}]")
        print(f"  chars={len(chinese.replace(chr(10), ''))} CJK={len(CJK.findall(chinese))}")
        print(f"  preview={chinese[:60].replace(chr(10), ' / ')}…")

        if not args.write:
            continue

        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        set_original(data, chinese)
        set_provenance(data, meta["source_reference"])
        path.write_text(
            yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=100),
            encoding="utf-8",
        )

        if uid not in by_uid:
            raise SystemExit(f"missing from index: {uid}")
        row = index_units[by_uid[uid]]
        set_original(row, chinese)
        set_provenance(row, meta["source_reference"])
        index_lines[by_uid[uid]] = json.dumps(row, ensure_ascii=False) + "\n"
        print(f"  wrote {path.name}")

    if args.write:
        INDEX.write_text("".join(index_lines), encoding="utf-8")
        after = coverage_work()
        print(f"\ncoverage after: {after[0]}/{after[1]}")
        print("index.jsonl synced")
    else:
        print("\ndry-run only; pass --write to apply")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

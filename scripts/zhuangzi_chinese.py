#!/usr/bin/env python3
"""Fetch traditional Chinese for Zhuangzi chapters and sync into YAML/canonical.

Source: Haodoo 好讀 (via andy0130tw.github.io/zhuangzi) — received text, traditional
characters, public domain. Giles (1889) English from data/raw_texts/ChaungTzuRaw.

Usage:
  python scripts/zhuangzi_chinese.py --fetch          # cache all 33 chapters
  python scripts/zhuangzi_chinese.py --sync-yaml      # inject into ch_*.yml
  python scripts/zhuangzi_chinese.py --sync-canonical # direct canonical update
  python scripts/zhuangzi_chinese.py --all              # fetch + yaml + canonicalize
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.request
from html import unescape
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

HAODOO_URL = "https://andy0130tw.github.io/zhuangzi/articles/{n}.html"
CACHE = ROOT / "data/raw_texts/pd/chinese/zhuangzi_haodoo_chapters.json"
GILES_RAW = ROOT / "data/raw_texts/ChaungTzuRaw"
YAML_DIR = ROOT / "data/yaml/the_book_of_chuang_tzu"
CANONICAL_DIR = ROOT / "data/canonical/the_book_of_chuang_tzu"

CHAPTER_NAMES: dict[int, str] = {
    1: "逍遙遊",
    2: "齊物論",
    3: "養生主",
    4: "人間世",
    5: "德充符",
    6: "大宗師",
    7: "應帝王",
    8: "駢拇",
    9: "馬蹄",
    10: "胠篋",
    11: "在宥",
    12: "天地",
    13: "天道",
    14: "天運",
    15: "刻意",
    16: "繕性",
    17: "秋水",
    18: "至樂",
    19: "達生",
    20: "山木",
    21: "田子方",
    22: "知北遊",
    23: "庚桑楚",
    24: "徐無鬼",
    25: "則陽",
    26: "外物",
    27: "寓言",
    28: "讓王",
    29: "盜跖",
    30: "說劍",
    31: "漁父",
    32: "列御寇",
    33: "天下",
}


def roman_to_int(s: str) -> int:
    s = s.upper().strip()
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}
    total = 0
    prev = 0
    for ch in reversed(s):
        val = values[ch]
        if val < prev:
            total -= val
        else:
            total += val
        prev = val
    return total


def normalize_chinese(text: str) -> str:
    text = unescape(text)
    text = text.replace("\u3000", "")
    text = re.sub(r"[﹁﹂﹃﹄]", lambda m: {"﹁": "「", "﹂": "」", "﹃": "「", "﹄": "」"}[m.group()], text)
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"(前篇|次篇|目錄).*$", "", text)
    return text.strip()


def format_chinese(text: str, max_chars: int | None = None) -> str:
    text = normalize_chinese(text)
    if max_chars and len(text) > max_chars:
        text = text[:max_chars]
    parts = re.split(r"(?<=[。；！？])", text)
    lines = [p.strip() for p in parts if p.strip()]
    return "\n".join(lines)


def _extract_haodoo_body(html: str) -> tuple[str, str]:
    """Return (title, body) from Haodoo article HTML."""
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    title = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""
    # Body is plain text after h1 in markdown conversion; grab longest CJK block.
    text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.I | re.S)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", "\n", text)
    text = unescape(text)
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    cjk_lines = [ln for ln in lines if re.search(r"[\u4e00-\u9fff]", ln)]
    # Drop nav/title duplicates; keep substantive chapter text.
    body_lines: list[str] = []
    for ln in cjk_lines:
        if re.match(r"^(內篇|外篇|雜篇)", ln) and "第" in ln and len(ln) < 30:
            continue
        if ln in ("莊子",):
            continue
        body_lines.append(ln)
    body = normalize_chinese("".join(body_lines))
    return title, body


def fetch_haodoo_chapter(n: int, timeout: int = 60) -> dict[str, Any]:
    url = HAODOO_URL.format(n=n)
    req = urllib.request.Request(url, headers={"User-Agent": "Pratibha/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        html = resp.read().decode("utf-8", errors="replace")
    title, body = _extract_haodoo_body(html)
    if len(body) < 80:
        raise RuntimeError(f"Chapter {n}: extracted Chinese too short ({len(body)} chars)")
    return {
        "chapter": n,
        "title": title or CHAPTER_NAMES.get(n, ""),
        "chinese_name": CHAPTER_NAMES.get(n, ""),
        "url": url,
        "source": "Haodoo 好讀 (andy0130tw.github.io/zhuangzi)",
        "text": body,
    }


def load_cache() -> dict[str, Any]:
    if CACHE.exists():
        try:
            return json.loads(CACHE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"source": HAODOO_URL, "chapters": {}}


def save_cache(data: dict[str, Any]) -> None:
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_all(chapters: list[int] | None = None) -> dict[int, str]:
    chapters = chapters or list(range(1, 34))
    data = load_cache()
    stored: dict[str, Any] = data.setdefault("chapters", {})
    out: dict[int, str] = {}
    for n in chapters:
        key = str(n)
        if key in stored and len(str(stored[key].get("text", ""))) > 80:
            out[n] = str(stored[key]["text"])
            print(f"  ch.{n:02d} cached ({len(out[n])} chars)", flush=True)
            continue
        print(f"  ch.{n:02d} fetching...", flush=True)
        entry = fetch_haodoo_chapter(n)
        stored[key] = entry
        out[n] = entry["text"]
        save_cache(data)
    return out


def parse_giles(path: Path = GILES_RAW) -> dict[int, dict[str, str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    pattern = re.compile(r"^CHAPTER ([IVXLC]+)\.\s*$", re.M)
    matches = list(pattern.finditer(text))
    chapters: dict[int, dict[str, str]] = {}
    for i, m in enumerate(matches):
        num = roman_to_int(m.group(1))
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end].strip()
        lines = block.splitlines()
        title = lines[0].strip() if lines else f"Chapter {num}"
        body_lines: list[str] = []
        for ln in lines[1:]:
            if ln.startswith("Argument:"):
                continue
            if re.match(r"^It requires but scant acumen", ln):
                break
            if re.match(r"^We are left in the dark", ln):
                break
            body_lines.append(ln)
        body = "\n".join(body_lines).strip()
        chapters[num] = {"title": title, "body": body}
    return chapters


def sync_yaml(chinese: dict[int, str], excerpt_chars: int = 1200) -> int:
    updated = 0
    for n, zh in chinese.items():
        path = YAML_DIR / f"ch_{n:03d}.yml"
        if not path.exists():
            print(f"  skip missing {path.name}", flush=True)
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        formatted = format_chinese(zh, max_chars=excerpt_chars)
        if doc.get("sanskrit") == formatted:
            continue
        doc["sanskrit"] = formatted
        doc["transliteration"] = (
            "*(Chinese source text; no Sanskrit original. Pinyin with tones for key terms is provided in Key Terms.)*"
        )
        path.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False), encoding="utf-8")
        updated += 1
        print(f"  updated {path.name} ({len(formatted)} chars)", flush=True)
    return updated


def sync_canonical(chinese: dict[int, str], excerpt_chars: int = 1200) -> int:
    updated = 0
    for n, zh in chinese.items():
        matches = list(CANONICAL_DIR.glob(f"*_ctz_{n:03d}.yml"))
        if not matches:
            continue
        formatted = format_chinese(zh, max_chars=excerpt_chars)
        iast = (
            "*(Chinese source text; no Sanskrit original. Pinyin with tones for key terms is provided in Key Terms.)*"
        )
        for path in matches:
            doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            if doc.get("sanskrit_devanagari") == formatted and doc.get("sanskrit_iast") == iast:
                continue
            doc["sanskrit_devanagari"] = formatted
            doc["sanskrit_iast"] = iast
            maturity = doc.get("editorial_maturity") or doc.get("maturity")
            if maturity == "structural_draft" and len(formatted) > 200:
                doc["editorial_maturity"] = "strong_draft"
            path.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False), encoding="utf-8")
            updated += 1
            print(f"  updated {path.name}", flush=True)
    return updated


def run_canonicalize() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts/canonicalize_texts.py")], check=True, cwd=ROOT)


def main() -> int:
    parser = argparse.ArgumentParser(description="Zhuangzi traditional Chinese sourcing")
    parser.add_argument("--fetch", action="store_true", help="Fetch/cache Haodoo chapters")
    parser.add_argument("--sync-yaml", action="store_true", help="Write Chinese into ch_*.yml")
    parser.add_argument("--sync-canonical", action="store_true", help="Update canonical ctz_* files")
    parser.add_argument("--canonicalize", action="store_true", help="Run canonicalize_texts.py")
    parser.add_argument("--all", action="store_true", help="fetch + sync-yaml + canonicalize")
    parser.add_argument("--chapter", type=int, action="append", dest="chapters")
    parser.add_argument("--full-text", action="store_true", help="Do not truncate Chinese excerpts")
    args = parser.parse_args()

    if args.all:
        args.fetch = args.sync_yaml = args.canonicalize = True

    if not any([args.fetch, args.sync_yaml, args.sync_canonical, args.canonicalize]):
        parser.print_help()
        return 1

    excerpt = None if args.full_text else 1200
    chinese: dict[int, str] = {}

    if args.fetch or args.sync_yaml or args.sync_canonical:
        chinese = fetch_all(args.chapters)

    if args.sync_yaml:
        print("Syncing YAML...", flush=True)
        n = sync_yaml(chinese, excerpt_chars=excerpt or 999_999)
        print(f"YAML: {n} files updated", flush=True)

    if args.sync_canonical:
        print("Syncing canonical...", flush=True)
        n = sync_canonical(chinese, excerpt_chars=excerpt or 999_999)
        print(f"Canonical: {n} files updated", flush=True)

    if args.canonicalize:
        print("Running canonicalize_texts.py...", flush=True)
        run_canonicalize()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

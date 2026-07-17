#!/usr/bin/env python3
"""Fix Wave B Tao Te Ching translations: gloss key Chinese terms in English prose.

Replaces raw Chinese, broken bracket patterns, and editorial notes in translation
layers with readable English using the Wave A convention:
  the Way [*dào* 道], non-being [*wú* 無], etc.

Updates both data/yaml/tao_te_ching/*.yml and data/canonical/tao_te_ching/*.yml.

Usage:
  python scripts/tao_te_ching_gloss_translations.py --dry-run
  python scripts/tao_te_ching_gloss_translations.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
YAML_DIR = ROOT / "data/yaml/tao_te_ching"
CANON_DIR = ROOT / "data/canonical/tao_te_ching"
LEGGE = ROOT / "data/raw_texts/pd/chinese/tao_te_ching_legge_gutenberg_216.txt"
CTEXT_URL = "https://api.ctext.org/gettext?urn=ctp:dao-de-jing&format=json"

CJK = re.compile(r"[\u4e00-\u9fff]")

# Standard chapter -> (pinyin, hanzi, English gloss) for first-occurrence inline marking
KEY_TERMS = [
    ("dào", "道", "the Way"),
    ("dàodé jīng", "道德經", "the Classic of the Way and Virtue"),
    ("dé", "德", "virtue"),
    ("wú", "無", "non-being"),
    ("yǒu", "有", "being"),
    ("wúwéi", "無為", "non-action"),
    ("zìrán", "自然", "self-so"),
    ("tiān", "天", "Heaven"),
    ("dì", "地", "earth"),
    ("shèng rén", "聖人", "sage"),
    ("cháng", "常", "enduring"),
    ("pǔ", "朴", "uncarved block"),
    ("xióng", "雄", "masculine strength"),
    ("cí", "雌", "feminine receptivity"),
    ("wújí", "無極", "the unbounded"),
    ("dàdào", "大道", "Great Way"),
    ("rén", "仁", "benevolence"),
    ("yì", "義", "righteousness"),
    ("míng", "名", "name"),
    ("yòng", "用", "use"),
    ("lì", "利", "advantage"),
    ("miào", "妙", "subtle interiority"),
    ("jiǎo", "徼", "outer boundary"),
    ("xuán", "玄", "dark depth"),
]

# Prose translations for chapters where Legge is verse-only or missing
PROSE_OVERRIDES: dict[int, str] = {
    6: (
        "The valley spirit [*gǔ shén* 谷神] never dies — it is called the mysterious feminine [*xuán pìn* 玄牝]. "
        "The gate of the mysterious feminine is called the root of heaven and earth. "
        "Continuous, seeming to remain: use it and it is never exhausted."
    ),
    11: (
        "Thirty spokes converge on a single hub [*gǔ* 轂]; "
        "it is precisely the empty space [*wú* 無] at the hub that makes the wheel work. "
        "Clay is thrown to make a vessel; it is precisely the empty space inside that makes the vessel work. "
        "Doors and windows are cut into walls to make a room; it is precisely the empty space within that makes the room work. "
        "Therefore: what has being [*yǒu* 有] provides the useful shape; what has non-being [*wú*] provides the actual use."
    ),
    12: (
        "The five colours blind the eye; the five tones deafen the ear; the five flavours dull the palate. "
        "Racing and hunting madden the mind; rare goods lead conduct astray. "
        "Therefore the sage satisfies the belly, not the eye — he puts away the latter and takes up the former."
    ),
    20: (
        "Abandon learning and there will be no sorrow. How much difference between yes and yea? "
        "How much difference between good and evil? What others fear, I cannot but fear too — "
        "wild, boundless, never settled! The people are merry as at a feast, as if ascending a terrace in spring. "
        "I alone am inactive, showing no signs, like an infant that has not yet smiled — forlorn, as if with no home. "
        "The people have more than enough; I alone seem to have lost all. I have the mind of a fool — so confused! "
        "Ordinary people are bright; I alone am dull. Ordinary people are sharp; I alone am muddled. "
        "Vast, like the sea; drifting, with no place to rest. All have purpose; I alone am stubborn and lowly. "
        "I alone differ from others, yet I value being nourished by the Way [*dào* 道]."
    ),
    21: (
        "The greatest virtue [*dé* 德] is entirely from the Way [*dào* 道] alone. "
        "The Way is elusive and indistinct — indistinct, yet within it are images; elusive, yet within it are things. "
        "Dim and dark, yet within it is essence. This essence is very real; within it is trustworthiness. "
        "From of old until now its name never departs, by which the ten thousand things arise. "
        "How do I know the nature of the ten thousand things? By this."
    ),
    28: (
        "Know the masculine strength [*xióng* 雄] and guard the feminine receptivity [*cí* 雌]; be the world's valley stream [*xī* 谿]. "
        "As the world's valley stream, constant virtue [*cháng dé* 常德] never leaves you, and you return to the infant state. "
        "Know the white and guard the black; be the world's model [*shì* 式]. "
        "As the world's model, constant virtue never errs, and you return to the unbounded [*wújí* 無極]. "
        "Know honour and guard disgrace; be the world's valley [*gǔ* 谷]. "
        "As the world's valley, constant virtue is sufficient, and you return to the uncarved block [*pǔ* 朴]. "
        "When the uncarved block is scattered, it becomes vessels; when the sage uses it, he becomes the chief officer. "
        "Thus the great cutting does not sever."
    ),
    40: (
        "Reversal [*fǎn* 反] is the movement of the Way [*dào* 道]. Weakness [*ruò* 弱] is the use of the Way. "
        "The ten thousand things under heaven are born from being [*yǒu* 有]; being is born from non-being [*wú* 無]."
    ),
    44: (
        "Which is more intimate — name or body? Which is more abundant — body or goods? "
        "Which is more harmful — gain or loss? Extreme love must be costly; great hoarding must be heavily lost. "
        "Know contentment and you will not be disgraced; know when to stop and you will not be endangered — long-lasting indeed."
    ),
    45: (
        "The greatest completion seems incomplete, yet its use is never exhausted. "
        "The greatest fullness seems empty, yet its use is never depleted. "
        "The straightest seems crooked; the most skilled seems clumsy; the most eloquent seems to stammer. "
        "Movement overcomes cold; stillness overcomes heat. Clear and calm — this can set the world right."
    ),
    54: (
        "The sage has no fixed mind — he takes the mind of the people as his mind. "
        "To those who are good I am good; to those who are not good I am also good — thus virtue [*dé* 德] is attained. "
        "To those who are truthful I am truthful; to those who are not truthful I am also truthful — thus virtue is attained. "
        "The sage, dwelling in the world, makes the world's mind his own. "
        "The people all attend to him; he treats them all as children."
    ),
    58: (
        "When the ruler is relaxed, the people are simple; when the ruler is sharp, the people are scheming. "
        "Fortune rests upon misfortune; misfortune hides within fortune. Who knows the limit? There is no fixed standard. "
        "The correct returns to the strange; the good returns to the perverse — and people have been confused for long ages. "
        "Therefore the sage is square but not cutting, pointed but not piercing, straight but not unbridled, bright but not dazzling."
    ),
    62: (
        "The Way [*dào* 道] is the sanctuary of the ten thousand things — a treasure for the good and a refuge for the not-good. "
        "Fine words can buy honour; fine deeds can elevate a person. Even if a person is not good, why abandon them? "
        "Therefore when the ruler is installed and the three ministers appointed, though jade disks and teams of horses are offered, "
        "it is better to remain still and offer the Way. "
        "Why did the ancients prize the Way? Did they not say: seek and you find; atone and you are forgiven? "
        "Therefore it is prized under heaven."
    ),
    68: (
        "The best warrior is not warlike; the best fighter does not rage; "
        "the best victor does not contend; the best employer puts himself below others. "
        "This is called the virtue [*dé* 德] of non-contention; this is called using the strength of others; "
        "this is called matching heaven — the highest of the ancients."
    ),
}


def norm_chinese(s: str) -> str:
    s = re.sub(r"\s+", "", s)
    return re.sub(r"[，。；：、！？「」『』（）\(\)\[\]\"\'\-\.\,;:!?]+", "", s)


def fetch_ctext() -> list[str]:
    with urllib.request.urlopen(CTEXT_URL, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    chapters = data.get("fulltext") or []
    if len(chapters) != 81:
        raise RuntimeError(f"Expected 81 ctext chapters, got {len(chapters)}")
    return [str(c).strip() for c in chapters]


def parse_legge(path: Path) -> dict[int, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    markers: list[tuple[int, int]] = []
    for i, line in enumerate(lines):
        m = re.match(r"^Ch\. (\d+)\.", line)
        m2 = re.match(r"^(\d+)\. 1\. ", line)
        m3 = re.match(r"^(\d+)\.\s*$", line)
        m4 = re.match(r"^(\d+)\. [A-Z]", line)  # e.g. "24. He who stands..."
        if m:
            markers.append((int(m.group(1)), i))
        elif m2 and 1 <= int(m2.group(1)) <= 81:
            markers.append((int(m2.group(1)), i))
        elif m4 and 1 <= int(m4.group(1)) <= 81:
            markers.append((int(m4.group(1)), i))
        elif m3 and 1 <= int(m3.group(1)) <= 81:
            # e.g. "11." followed by blank line then prose
            if i + 1 < len(lines) and not re.match(r"^\d+\.", lines[i + 1]):
                markers.append((int(m3.group(1)), i))

    # dedupe by chapter, keep first
    seen: set[int] = set()
    unique: list[tuple[int, int]] = []
    for ch, idx in sorted(markers, key=lambda x: x[1]):
        if ch not in seen:
            seen.add(ch)
            unique.append((ch, idx))

    chapters: dict[int, str] = {}
    for j, (ch, start) in enumerate(unique):
        end = unique[j + 1][1] if j + 1 < len(unique) else len(lines)
        body = "\n".join(lines[start:end]).strip()
        chapters[ch] = body
    return chapters


def clean_legge(raw: str) -> str:
    s = raw
    # drop leading chapter header line
    s = re.sub(r"^Ch\. \d+\.\s*", "", s, flags=re.MULTILINE)
    s = re.sub(r"^\d+\. 1\. ", "", s, count=1)
    s = re.sub(r"^\d+\. ", "", s, count=1)
    s = re.sub(r"^\d+\.\s*\n", "", s, count=1)
    # remove subsection numbers
    s = re.sub(r"(?m)^\d+\. ", "", s)
    # remove verse indentation blocks markers
    s = re.sub(r"(?m)^\s{2,3}", "", s)
    # strip any embedded Chinese (Legge should be English-only)
    s = CJK.sub("", s)
    # normalize whitespace
    s = re.sub(r"\s*\n\s*", " ", s)
    s = re.sub(r"  +", " ", s)
    # light modernization — order matters
    replacements = [
        (r"\bthe Great Tao\b", "the Great Way"),
        (r"\bGreat Tao\b", "Great Way"),
        (r"\bthe Tao of Heaven\b", "Heaven's Way"),
        (r"\bthe Tao of old\b", "the Way of old"),
        (r"\bthe Tao\b", "the Way"),
        (r"\bTao\b", "the Way"),
        (r"\btao\b", "the Way"),
        (r"\bthe Way \(Way or Method\)", "the Great Way"),
        (r"\bthe Way of Heaven\b", "Heaven's Way"),
        (r"\bthe the Way\b", "the Way"),
        (r"\bthe Great the Great Way\b", "the Great Way"),
        (r"  +", " "),
        (" ;", ";"),
        (" ,", ","),
    ]
    for old, new in replacements:
        s = re.sub(old, new, s)
    s = re.sub(r"\bthe the Way\b", "the Way", s)
    s = re.sub(r"\(Way or Method\)", "", s)
    s = re.sub(r"  +", " ", s)
    s = s.strip()
    # split into readable paragraphs at sentence groups
    sentences = re.split(r"(?<=[.!?])\s+", s)
    sentences = [x.strip() for x in sentences if x.strip()]
    return "\n\n".join(sentences)


def add_term_glosses(text: str) -> str:
    """Add [*pinyin* 汉字] glosses on first English occurrence of key terms."""
    out = text
    used: set[str] = set()

    gloss_rules = [
        (r"\bthe Great Way\b", "the Great Way [*dàdào* 大道]", "dàdào"),
        (r"\bGreat Way\b", "Great Way [*dàdào* 大道]", "dàdào"),
        (r"\bHeaven's Way\b", "Heaven's Way [*tiān dào* 天道]", "tiān dào"),
        (r"\bnon-action\b", "non-action [*wúwéi* 無為]", "wúwéi"),
        (r"\bnon-being\b", "non-being [*wú* 無]", "wú"),
        (r"\bself-so\b", "self-so [*zìrán* 自然]", "zìrán"),
        (r"\buncarved block\b", "uncarved block [*pǔ* 朴]", "pǔ"),
        (r"\bthe Way\b", "the Way [*dào* 道]", "dào"),
        (r"\bvirtue\b", "virtue [*dé* 德]", "dé"),
        (r"\bsage\b", "sage [*shèng rén* 聖人]", "shèng rén"),
        (r"\bHeaven\b", "Heaven [*tiān* 天]", "tiān"),
        (r"\bbeing\b", "being [*yǒu* 有]", "yǒu"),
    ]

    for pattern, replacement, key in gloss_rules:
        if key in used:
            continue
        if re.search(pattern, out, flags=re.IGNORECASE):
            out = re.sub(pattern, replacement, out, count=1, flags=re.IGNORECASE)
            used.add(key)

    return out


def build_translation(std_ch: int, legge: dict[int, str]) -> str:
    if std_ch in PROSE_OVERRIDES:
        return PROSE_OVERRIDES[std_ch]
    raw = legge.get(std_ch, "")
    if not raw:
        raise ValueError(f"No Legge text for chapter {std_ch}")
    cleaned = clean_legge(raw)
    if len(cleaned) < 80:
        raise ValueError(f"Legge prose too short for chapter {std_ch}")
    return add_term_glosses(cleaned)


def needs_fix(trans: str, category: str) -> bool:
    if category == "root_text":
        return False
    if not trans.strip():
        return True
    cjk = len(CJK.findall(trans))
    if cjk > 8:
        return True
    if re.search(r"\[[^\]]*\]\([^\)]*\)", trans):
        return True
    if "are kept in brackets" in trans:
        return True
    if re.search(r"\[[\u4e00-\u9fff]+\]", trans):
        return True
    if re.search(r"Tao \(道\)|Dao \(道\)", trans):
        return True
    if re.search(r"\[[\u4e00-\u9fff]+\] \([\u4e00-\u9fff]+\)", trans):
        return True
    if re.search(r"\[[a-zàáâãäåèéêëìíîïòóôõöùúûüǎěīōūǖ]+\] \([^\)]*\)", trans, re.IGNORECASE):
        return True
    if re.search(r"\([^\)]*[\u4e00-\u9fff][^\)]*\)", trans):
        return True
    if re.search(r"\[[\u4e00-\u9fff][^\]]*,[^\]]*\]", trans):
        return True
    if re.search(r"\[[a-zàáâãäåèéêëìíîïòóôõöùúûüǎěīōūǖ]+\](?!\s*\*)", trans, re.IGNORECASE):
        return True
    if re.search(r"\bthe the Way\b", trans):
        return True
    return False


def get_original(data: dict) -> str:
    for layer in data.get("pratibha_layers") or []:
        if layer.get("kind") == "original":
            return layer.get("body") or ""
    return data.get("sanskrit_devanagari") or data.get("sanskrit") or ""


def get_translation(data: dict) -> str:
    for layer in data.get("pratibha_layers") or []:
        if layer.get("kind") == "translation":
            return layer.get("body") or ""
    return data.get("translation_literal") or data.get("translation") or ""


def set_translation(data: dict, new_trans: str) -> None:
    data["translation_literal"] = new_trans
    if "translation" in data:
        data["translation"] = new_trans
    if "source_excerpt" in data and CJK.findall(str(data.get("source_excerpt", ""))):
        # replace excerpt if it was the broken translation
        old_excerpt = data.get("source_excerpt") or ""
        if needs_fix(old_excerpt, "commentary_text") or len(CJK.findall(old_excerpt)) > 5:
            data["source_excerpt"] = new_trans[:500]
    layers = data.get("pratibha_layers") or []
    for layer in layers:
        if layer.get("kind") == "translation":
            layer["body"] = new_trans
            break
    else:
        # insert after original if present
        insert_at = 0
        for i, layer in enumerate(layers):
            if layer.get("kind") == "original":
                insert_at = i + 1
                break
        layers.insert(
            insert_at,
            {"kind": "translation", "label": "Pratibha Translation", "body": new_trans},
        )
        data["pratibha_layers"] = layers


def map_file_to_chapter(ctext: list[str]) -> dict[int, int]:
    ctext_norm = {norm_chinese(c): i + 1 for i, c in enumerate(ctext)}
    mapping: dict[int, int] = {}
    for f in sorted(CANON_DIR.glob("tao_te_ching_ttc_md_*.yml")):
        file_num = int(re.search(r"_(\d+)\.yml", f.name).group(1))
        data = yaml.safe_load(f.read_text(encoding="utf-8"))
        orig = get_original(data)
        n = norm_chinese(orig)
        std_ch = ctext_norm.get(n)
        if not std_ch:
            for cn, ch in ctext_norm.items():
                if cn[:12] == n[:12]:
                    std_ch = ch
                    break
        if std_ch:
            mapping[file_num] = std_ch
    return mapping


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ctext = fetch_ctext()
    legge = parse_legge(LEGGE)
    file_to_ch = map_file_to_chapter(ctext)

    updated: list[tuple[int, int, Path]] = []
    skipped: list[tuple[int, str]] = []

    for f in sorted(CANON_DIR.glob("tao_te_ching_ttc_md_*.yml")):
        file_num = int(re.search(r"_(\d+)\.yml", f.name).group(1))
        data = yaml.safe_load(f.read_text(encoding="utf-8"))
        trans = get_translation(data)
        category = data.get("category", "")

        if not needs_fix(trans, category):
            continue

        std_ch = file_to_ch.get(file_num)
        if not std_ch:
            skipped.append((file_num, "no chapter mapping"))
            continue

        try:
            new_trans = build_translation(std_ch, legge)
        except ValueError as e:
            skipped.append((file_num, str(e)))
            continue

        set_translation(data, new_trans)

        yaml_path = YAML_DIR / f"tao_te_ching_md_{file_num:03d}.yml"
        if yaml_path.exists():
            ydata = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
            set_translation(ydata, new_trans)
        else:
            ydata = None

        if args.dry_run:
            print(f"[dry-run] file {file_num:03d} -> std ch {std_ch}")
            print(f"  BEFORE: {trans[:100].replace(chr(10), ' ')}...")
            print(f"  AFTER:  {new_trans[:100].replace(chr(10), ' ')}...")
            continue

        f.write_text(yaml.dump(data, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")
        if ydata is not None:
            yaml_path.write_text(
                yaml.dump(ydata, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8"
            )
        updated.append((file_num, std_ch, f))

    print(f"Updated: {len(updated)} units")
    for file_num, std_ch, path in updated:
        print(f"  file {file_num:03d} (std ch {std_ch}) -> {path.name}")
    if skipped:
        print(f"Skipped: {len(skipped)}")
        for file_num, reason in skipped:
            print(f"  file {file_num:03d}: {reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

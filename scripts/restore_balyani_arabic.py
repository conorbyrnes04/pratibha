#!/usr/bin/env python3
"""Restore Arabic original + ALA-LC transliteration for Know Yourself (Balyānī).

Uses public-domain classical Arabic of Risālat al-Wujūdiyya / Risālat al-Aḥadiyya
(Balyānī; long ascribed to Ibn ʿArabī), aligned to each unit via Weir JRAS 1901
English as locator. Does not use Twinch copyrighted English.

Alignment is deterministic landmark matching over the early continuous discourse
(Weir 809–812 / Arabic opening through the fanāʾ critique), which is where the
36 contemplative pearls live.

    python scripts/restore_balyani_arabic.py            # preview
    python scripts/restore_balyani_arabic.py --write
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ARABIC = ROOT / "data/raw_texts/pd/arabic/balyani_risalat_al_wujudiyya_ahadiyya_ar.txt"
UNITS = ROOT / "data/canonical/know_yourself_ibn_arabi_balyani"
INDEX = ROOT / "data/canonical/index.jsonl"

PROVENANCE = (
    "Arabic: classical text of Risālat al-Wujūdiyya / Risālat al-Aḥadiyya "
    "(Auḥad al-Dīn al-Balyānī; traditionally ascribed to Ibn ʿArabī). "
    "Unicode transcription from https://www.ibnalarabi.com/books/wujudiya.php "
    "(text pages), saved at data/raw_texts/pd/arabic/balyani_risalat_al_wujudiyya_ahadiyya_ar.txt. "
    "Passage aligned using T. H. Weir JRAS 1901 English as locator. "
    "Underlying medieval Arabic is public domain."
)

# English keyword groups → Arabic paragraph indices in the early treatise.
# Indices refer to load_paragraphs() order (basmala/opening through fanāʾ).
# Keywords cover both Weir-modernized and Twinch-style pearl locators.
LANDMARKS: list[tuple[str, tuple[str, ...], tuple[int, ...]]] = [
    (
        "opening_basmala_praise",
        (
            "in the name of god",
            "before whose oneness",
            "before or after",
            "outward without",
            "inward without",
            "one without oneness",
            "name and named",
            "first without firstness",
            "temporal distinctions",
            "manifested existence or place",
            "closeness or distance",
            "he is now as he was",
            "he is, and there is not with him",
        ),
        (0, 1, 2, 3),
    ),
    (
        "not_in_thing_know_him",
        (
            "incarnation",
            "indwelling",
            "ḥulūl",
            "hulul",
            "not in a thing",
            "not in anything",
            "no thing is in him",
            "not by knowledge",
            "theoretical knowledge",
            "nor by intellect",
            "none sees him",
            "no one sees him",
            "by himself he",
            "through himself",
            "outward eye",
            "inward eye",
            "external eye",
            "interior sight",
            "no one knows him except himself",
            "no one reaches him",
            "knows himself through himself",
            "sees himself by means of himself",
        ),
        (4,),
    ),
    (
        "veil_prophet_sending",
        (
            "his veil",
            "own being veils",
            "concealment of his",
            "concealed by his oneness",
            "his prophet is he",
            "his sending is he",
            "sent himself",
            "no mediator",
            "prophetic message",
            "sender and the thing sent",
            "sender, that which is sent",
            "no sent prophet",
            "angel brought",
            "perfect saint",
        ),
        (5,),
    ),
    (
        "know_yourself_hadith",
        (
            "whoever knows himself",
            "whoever knows their self",
            "whoso knoweth himself",
            "knoweth his lord",
            "knows his lord",
            "knows their lord",
            "i know my lord by my lord",
            "you are not you",
            "thou art not thou",
            "thou art he",
            "you are he",
            "never were",
            "never wast",
            "if you know your existence",
            "if thou know thine existence",
            "without existing and passing away",
            "know yourself without",
        ),
        (6,),
    ),
    (
        "fana_critique",
        (
            "ceasing of existence",
            "ceasing to be",
            "cease to be",
            "passing away of existence",
            "passing away of that passing",
            "what does not exist cannot pass",
            "fana",
            "fanā",
            "those who know god",
            "claim to know god",
            "al-ʿurrāf",
            "urrāf",
            "polytheism",
            "non-existent now",
            "nonexistent now",
            "before the creation",
            "past eternity",
            "eternity-without-beginning",
            "eternity-without-end",
            "maketh himself to cease",
            "makes himself cease",
            "annihilates their self",
            "annihilation of self",
            "your being is nothing",
            "affirmation of something other",
            "without any associate",
        ),
        (7, 8),
    ),
]


# --- ALA-LC-ish Arabic romanization (scholarly simple) ---
_LETTER = {
    "ء": "ʾ",
    "آ": "ā",
    "أ": "a",
    "ؤ": "ʾ",
    "إ": "i",
    "ئ": "ʾ",
    "ا": "ā",
    "ب": "b",
    "ة": "a",
    "ت": "t",
    "ث": "th",
    "ج": "j",
    "ح": "ḥ",
    "خ": "kh",
    "د": "d",
    "ذ": "dh",
    "ر": "r",
    "ز": "z",
    "س": "s",
    "ش": "sh",
    "ص": "ṣ",
    "ض": "ḍ",
    "ط": "ṭ",
    "ظ": "ẓ",
    "ع": "ʿ",
    "غ": "gh",
    "ف": "f",
    "ق": "q",
    "ك": "k",
    "ل": "l",
    "م": "m",
    "ن": "n",
    "ه": "h",
    "و": "w",
    "ى": "á",
    "ي": "y",
    "ٱ": "a",
}
_VOWEL = {"َ": "a", "ِ": "i", "ُ": "u", "ً": "an", "ٍ": "in", "ٌ": "un", "ْ": "", "ّ": "", "ٰ": "ā", "ۡ": ""}
_DROP = set("ـ۪ۣ۟ۢۤۥۦۨ۫۬۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩")


def transliterate_ala_lc(arabic: str) -> str:
    """Simple scholarly Latinization approximating ALA-LC (consonants + written vowels)."""
    out: list[str] = []
    chars = list(arabic)
    i = 0
    while i < len(chars):
        ch = chars[i]
        if ch in _DROP:
            i += 1
            continue
        if ch in _VOWEL:
            out.append(_VOWEL[ch])
            i += 1
            continue
        if ch == "لا" or (ch == "ل" and i + 1 < len(chars) and chars[i + 1] == "ا"):
            # handled below via letter map + alif
            pass
        if ch in _LETTER:
            base = _LETTER[ch]
            # shadda: double previous consonant letter
            if i + 1 < len(chars) and chars[i + 1] == "ّ":
                # geminate: repeat consonant portion
                cons = base
                if cons.startswith(("th", "kh", "dh", "sh", "gh")):
                    out.append(cons + cons)
                else:
                    out.append(cons + cons[-1:])
                i += 2
                # optional vowel after shadda
                if i < len(chars) and chars[i] in _VOWEL:
                    out.append(_VOWEL[chars[i]])
                    i += 1
                continue
            out.append(base)
            i += 1
            continue
        if ch in " \n\t":
            if out and out[-1] != " ":
                out.append(" ")
            i += 1
            continue
        if ch in "،؛؟!:.,;?\"'«»()[]{}…—*":
            out.append(ch)
            i += 1
            continue
        if "\u0600" <= ch <= "\u06FF":
            # unmapped Arabic: skip silently
            i += 1
            continue
        out.append(ch)
        i += 1
    text = "".join(out)
    text = re.sub(r" +", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def has_arabic(text: str) -> bool:
    return any("\u0600" <= c <= "\u06FF" for c in text or "")


def clean_arabic(text: str) -> str:
    text = (text or "").strip()
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def load_paragraphs(arabic_full: str) -> list[str]:
    """Load treatise paragraphs; stop before the Q&A section (كيف السبيل)."""
    cut = arabic_full.find("## [كيف السبيل")
    early = arabic_full[:cut] if cut > 0 else arabic_full
    paras: list[str] = []
    buf: list[str] = []
    for line in early.splitlines():
        if line.startswith("## "):
            body = "\n".join(buf).strip()
            if body:
                for block in re.split(r"\n\s*\n", body):
                    block = clean_arabic(block)
                    if block and has_arabic(block):
                        paras.append(block)
            buf = []
            continue
        if line.startswith("#"):
            continue
        buf.append(line)
    body = "\n".join(buf).strip()
    if body:
        for block in re.split(r"\n\s*\n", body):
            block = clean_arabic(block)
            if block and has_arabic(block):
                paras.append(block)
    return paras


def locator_candidates(unit: dict) -> list[str]:
    """Ordered locator strings from tight pearl body to longer Weir flat fields."""
    layer_tr = ""
    for layer in unit.get("pratibha_layers") or []:
        if isinstance(layer, dict) and layer.get("kind") == "translation":
            layer_tr = str(layer.get("body") or "").strip()
            if layer_tr:
                break
    title = str(unit.get("title") or "")
    out: list[str] = []
    for body in (
        layer_tr,
        str(unit.get("source_excerpt") or "").strip(),
        str(unit.get("translation") or "").strip(),
        str(unit.get("translation_literal") or "").strip(),
    ):
        if not body:
            continue
        text = f"{title} {body}".lower()
        if text not in out:
            out.append(text)
    if not out and title:
        out.append(title.lower())
    return out


def score_landmarks(loc: str) -> tuple[str, int, tuple[int, ...]]:
    best_id = ""
    best_score = 0
    best_idxs: tuple[int, ...] = ()
    for lid, keys, idxs in LANDMARKS:
        score = sum(1 for k in keys if k in loc)
        if score > best_score:
            best_score = score
            best_id = lid
            best_idxs = idxs
    return best_id, best_score, best_idxs


def align_unit(unit: dict, paras: list[str]) -> tuple[str, str, str] | None:
    """Return (arabic, landmark_id, confidence) or None."""
    best: tuple[str, int, tuple[int, ...]] | None = None
    best_loc = ""
    for loc in locator_candidates(unit):
        lid, score, idxs = score_landmarks(loc)
        if score < 1:
            continue
        # Bridging pearls quote the hadith while arguing against fanāʾ —
        # prefer the fanāʾ critique Arabic when annihilation language dominates.
        if lid == "know_yourself_hadith":
            fana_hits = sum(
                1
                for k in (
                    "annihilat",
                    "passing away",
                    "ceasing of existence",
                    "ceasing to be",
                    "your being is nothing",
                    "affirmation of something other",
                    "polytheism",
                )
                if k in loc
            )
            if fana_hits >= 2:
                lid, score, idxs = "fana_critique", score + fana_hits, (7, 8)
        if best is None or score > best[1]:
            best = (lid, score, idxs)
            best_loc = loc
            if score >= 2 and lid != "know_yourself_hadith":
                break
            if score >= 3:
                break
    if best is None:
        return None
    best_id, best_score, best_idxs = best
    chunks = []
    for idx in best_idxs:
        if 0 <= idx < len(paras):
            chunks.append(paras[idx])
    if not chunks:
        return None
    arabic = clean_arabic("\n\n".join(chunks))
    if best_id == "opening_basmala_praise" and "in the name of god" not in best_loc:
        parts = [
            p
            for p in chunks
            if not p.startswith("بسم الله") and p != "الحمد لله ربِّ العالمين"
        ]
        if parts:
            arabic = clean_arabic("\n\n".join(parts))
    conf = "high" if best_score >= 2 else "medium"
    return arabic, best_id, conf


def locator_text(unit: dict) -> str:
    cands = locator_candidates(unit)
    return cands[0] if cands else ""


def upsert_layers(unit: dict, arabic: str, iast: str) -> None:
    layers = unit.get("pratibha_layers")
    if not isinstance(layers, list):
        layers = []
    layers = [
        L
        for L in layers
        if not (isinstance(L, dict) and L.get("kind") in ("original", "iast"))
    ]
    new_layers = [
        {
            "kind": "original",
            "label": "Original (Arabic)",
            "body": arabic,
            "layer_provenance": PROVENANCE,
        },
        {
            "kind": "iast",
            "label": "Transliteration (ALA-LC)",
            "body": iast,
            "layer_provenance": "ALA-LC / scholarly latinization of the matched Arabic passage.",
        },
    ]
    unit["pratibha_layers"] = new_layers + layers
    unit["sanskrit_devanagari"] = arabic
    unit["sanskrit_iast"] = iast
    prov = unit.get("provenance")
    if isinstance(prov, dict):
        prov = dict(prov)
        prov["arabic_source"] = (
            "balyani_risalat_al_wujudiyya_ahadiyya_ar.txt "
            "(ibnalarabi.com transcription; classical PD Arabic)"
        )
        unit["provenance"] = prov


def atomic_write(path: Path, content: str) -> None:
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(content)
        tmp = Path(handle.name)
    tmp.replace(path)


def dump_yaml(unit: dict) -> str:
    return yaml.safe_dump(
        unit, allow_unicode=True, sort_keys=False, width=100, default_flow_style=False
    )


def sync_index(updated: dict[str, dict]) -> int:
    lines = INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
    units = [json.loads(line) for line in lines if line.strip()]
    if len(lines) != len(units):
        raise SystemExit("index.jsonl has blank lines; refusing")
    n = 0
    out_lines = []
    for unit in units:
        uid = unit.get("unit_id")
        if uid in updated:
            src = updated[uid]
            unit["pratibha_layers"] = src.get("pratibha_layers")
            unit["sanskrit_devanagari"] = src.get("sanskrit_devanagari", "")
            unit["sanskrit_iast"] = src.get("sanskrit_iast", "")
            if isinstance(src.get("provenance"), dict):
                unit["provenance"] = src["provenance"]
            n += 1
        out_lines.append(json.dumps(unit, ensure_ascii=False) + "\n")
    atomic_write(INDEX, "".join(out_lines))
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    arabic_full = ARABIC.read_text(encoding="utf-8")
    paras = load_paragraphs(arabic_full)
    files = sorted(UNITS.glob("*.yml"))
    if args.limit:
        files = files[: args.limit]

    print(f"units={len(files)} early_paras={len(paras)} write={args.write}")
    for i, p in enumerate(paras):
        print(f"  P{i}: {p[:80].replace(chr(10), ' ')}")

    matched: dict[str, dict] = {}
    gaps: list[str] = []
    report: list[str] = []

    for i, path in enumerate(files, 1):
        unit = yaml.safe_load(path.read_text(encoding="utf-8"))
        name = path.name
        uid = str(unit.get("unit_id"))
        result = align_unit(unit, paras)
        if not result:
            print(f"[{i}] {name}: NO MATCH")
            gaps.append(uid)
            report.append(f"{uid}\tnone\tok=False\t")
            continue
        arabic, landmark, conf = result
        iast = transliterate_ala_lc(arabic)
        preview = arabic[:70].replace("\n", " ")
        print(f"[{i}] {name}: {landmark} conf={conf} {preview}")
        report.append(f"{uid}\t{landmark}\t{conf}\t{preview}")
        upsert_layers(unit, arabic, iast)
        matched[uid] = unit
        if args.write:
            atomic_write(path, dump_yaml(unit))

    if args.write and matched:
        n = sync_index(matched)
        print(f"synced index.jsonl rows={n}")

    print("---")
    print(f"matched={len(matched)}/{len(files)}")
    if gaps:
        print("UNMATCHED:")
        for g in gaps:
            print(" ", g)
    out = ROOT / "data/raw_texts/pd/arabic/balyani_arabic_restore_report.tsv"
    out.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"report={out}")
    print("done" + (" (WRITE)" if args.write else " (preview)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

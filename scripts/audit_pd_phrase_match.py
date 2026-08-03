#!/usr/bin/env python3
"""Phrase-match model-supplied / PD-pending corpus units against local PD anchors.

Read-only audit. Writes a TSV report under docs/private/ (or --out).

Verdicts:
  hit      — distinctive phrase found in PD (strong evidence the text is real)
  partial  — weaker / shorter overlap only
  miss     — no usable overlap (likely paraphrase, wrong cite, or fabrication)
  no_pd    — no local PD file mapped for this collection
  no_query — unit has no usable original/translation text to search
"""

from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CANON = ROOT / "data" / "canonical"
PD = ROOT / "data" / "raw_texts" / "pd"

# Collection folder name → list of PD relative paths (first existing wins for primary;
# all existing are searched).
COLL_PD: dict[str, list[str]] = {
    "shantideva_bodhicaryavatara": ["indian/bodhicaryavatara_gretil_iast_sanskrit.txt"],
    "chāndogya_upaniṣad": [
        "indian/chandogya_upanishad_gretil_iast.txt",
        "indian/chandogya_upanishad_muller_sbe01.txt",
    ],
    "phaedo_plato": [
        "greek/phaedo_jowett_gutenberg_1658.txt",
        "greek/phaedo_burnet_perseus-grc2.xml",
    ],
    "plotinus_enneads": ["greek/plotinus_mackenna_enneads.txt"],
    "pseudo_dionysius": [
        "greek/dionysius_rolt_1920.txt",
        "greek/mystical_theology_migne_pg3.txt",
        "greek/divine_names_greek_unicode.txt",
    ],
    "meister_eckhart": ["german/pfeiffer_eckhart_1857_ocr.txt"],
    "rumi_mathnawi": [
        "persian/mathnawi_neynameh_ganjoor.txt",
        "persian/mathnawi_moses_shepherd_ganjoor.txt",
        "persian/mathnawi_elephant_dark_masnavi_net.txt",
        "persian/mathnawi_chinese_greek_painters_masnavi_net.txt",
        "persian/mathnawi_merchant_parrot_masnavi_net.txt",
    ],
    "dōgen_shōbōgenzō": ["japanese/shobogenzo_1896_kokubasha.txt"],
    "dogen_shobogenzo": ["japanese/shobogenzo_1896_kokubasha.txt"],
    "milarepa_songs": ["tibetan/milarepa_evans_wentz_1928.txt"],
    "epictetus_works": [
        "greek/epictetus_enchiridion_gutenberg_45109.txt",
        "greek/epictetus_long_discourses_gutenberg_10662.txt",
    ],
    "the_book_of_chuang_tzu": ["chinese/zhuangzi_giles_gutenberg_59709.txt"],
    "know_yourself_ibn_arabi_balyani": [
        "arabic/balyani_risalat_al_wujudiyya_ahadiyya_ar.txt",
        "arabic/ibn_arabi_balyani_weir_jras_1901.txt",
    ],
    "astavakra_gita": ["indian/astavakra_gita_gretil_iast.txt"],
    "katha_upanishad": [
        "indian/katha_upanishad_gretil_iast.txt",
        "indian/upanishads_muller_sbe15_gutenberg_3283.txt",
    ],
    "brihadaranyaka_upanishad": [
        "indian/brihadaranyaka_upanishad_gretil_iast.txt",
        "indian/upanishads_muller_sbe15_gutenberg_3283.txt",
    ],
    "mundaka_upanishad": [
        # GRETIL Mundaka file not yet located; Müller SBE English only for now
        "indian/upanishads_muller_sbe15_gutenberg_3283.txt",
        "indian/chandogya_upanishad_muller_sbe01.txt",
    ],
    "isavasya_upanishad": [
        "indian/isavasya_upanishad_gretil_iast.txt",
        "indian/chandogya_upanishad_muller_sbe01.txt",
    ],
    "svetasvatara_upanishad": [
        "indian/svetasvatara_upanishad_gretil_iast.txt",
        "indian/upanishads_muller_sbe15_gutenberg_3283.txt",
    ],
    "mandukya_upanishad_and_gaudapada_karika": [
        "indian/mandukya_gaudapada_gretil_iast.txt",
        "indian/mandukya_upanishad_gretil_iast.txt",
    ],
    "nagarjuna_mulamadhyamakakarika": ["indian/nagarjuna_mmk_gretil_iast.txt"],
    "tantrasara": ["indian/tantrasara_abhinavagupta_gretil_iast.txt"],
    "marcus_aurelius_meditations": ["greek/marcus_aurelius_long_1862.txt"],
    "confucius_analects": ["chinese/analects_legge_gutenberg_4094.txt"],
    "zhongyong": ["chinese/zhongyong_legge_gutenberg_4096.txt"],
}


def fold(s: str) -> str:
    """Lowercase, strip combining marks, keep letters/digits/spaces (incl. non-Latin)."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^\w\s]", " ", s, flags=re.UNICODE)
    return re.sub(r"\s+", " ", s).strip()


def as_text(v) -> str:
    if v is None:
        return ""
    if isinstance(v, list):
        return "\n".join(as_text(x) for x in v)
    if isinstance(v, dict):
        for k in ("content", "text", "body", "value"):
            if k in v:
                return as_text(v[k])
        return ""
    return str(v).strip()


def is_risk_unit(d: dict) -> bool:
    prov = d.get("provenance") or {}
    if not isinstance(prov, dict):
        return False
    blob = " ".join(str(v) for v in prov.values())
    return (
        "model-supplied" in blob
        or "PD-verification pending" in blob
        or "2026" in str(prov.get("english_source", ""))
    )


def layer_text(d: dict, kind: str) -> str:
    for layer in d.get("pratibha_layers") or []:
        if isinstance(layer, dict) and layer.get("kind") == kind:
            return as_text(layer.get("content") or layer.get("text"))
    return ""


def usable_query(t: str) -> bool:
    """Accept short originals in non-Latin scripts; require more for English prose."""
    if not t:
        return False
    low = t.lower().strip()
    if low.startswith("n/a") or "key verse is:" in low or "received text does not" in low:
        return False
    f = fold(t)
    if len(f) < 12:
        return False
    # Non-Latin (Arabic, CJK, Greek, Devanagari, etc.): short dicta are valid
    if re.search(r"[^\x00-\x7f]", t) and len(f) >= 12:
        return True
    return len(f) >= 24


def extract_queries(d: dict) -> list[tuple[str, str]]:
    """Return (field, raw_text) candidates to match, preferred order."""
    out: list[tuple[str, str]] = []
    for field in (
        "sanskrit_iast",
        "sanskrit_devanagari",
        "translation_literal",
        "source_excerpt",
    ):
        t = as_text(d.get(field))
        if usable_query(t):
            out.append((field, t))
    for kind in ("original", "translation"):
        t = layer_text(d, kind)
        if usable_query(t):
            out.append((f"layer:{kind}", t))
    return out


def phrase_windows(norm: str, sizes: tuple[int, ...] = (12, 10, 8, 6)) -> list[str]:
    words = norm.split()
    phrases: list[str] = []
    seen: set[str] = set()
    for n in sizes:
        if len(words) < n:
            continue
        # sample start, mid, and a few strides
        idxs = {0, max(0, len(words) // 2 - n // 2), max(0, len(words) - n)}
        for i in range(0, max(1, len(words) - n + 1), max(1, n // 2)):
            idxs.add(i)
        for i in sorted(idxs):
            if i + n > len(words):
                continue
            p = " ".join(words[i : i + n])
            if p not in seen and len(p) >= 20:
                seen.add(p)
                phrases.append(p)
    # also a long contiguous char slice for non-spaced scripts
    if len(words) <= 2 and len(norm) >= 24:
        for start in (0, max(0, len(norm) // 3), max(0, len(norm) - 40)):
            chunk = norm[start : start + 40].strip()
            if len(chunk) >= 20 and chunk not in seen:
                seen.add(chunk)
                phrases.append(chunk)
    return phrases[:24]


def best_fuzzy_window(query: str, hay: str, window: int = 240) -> float:
    q = query[:180]
    if not q or not hay:
        return 0.0
    if len(hay) <= window:
        return SequenceMatcher(None, q, hay).ratio()
    step = max(40, window // 3)
    best = 0.0
    # Prefer regions that share a short token
    tokens = [t for t in q.split() if len(t) >= 5][:6]
    starts = set(range(0, len(hay) - window + 1, step))
    for tok in tokens:
        pos = hay.find(tok)
        while pos != -1 and len(starts) < 40:
            starts.add(max(0, pos - 40))
            pos = hay.find(tok, pos + len(tok))
            if pos > 0 and pos - (max(starts) if starts else 0) > 50000:
                break
    for i in list(starts)[:50]:
        chunk = hay[i : i + window]
        r = SequenceMatcher(None, q, chunk).ratio()
        if r > best:
            best = r
            if best >= 0.92:
                return best
    return best


def match_against(norm_query: str, haystacks: list[tuple[str, str]]) -> tuple[str, float, str, str]:
    """Return verdict, score, matched_phrase, pd_file."""
    phrases = phrase_windows(norm_query)
    # For very short non-spaced / few-word originals, also try the whole string
    if norm_query and norm_query not in phrases and len(norm_query) >= 12:
        phrases = [norm_query] + phrases
    if not phrases:
        return "no_query", 0.0, "", ""

    best_hit: tuple[float, str, str, str] = (0.0, "miss", "", "")
    for pd_name, hay in haystacks:
        # exact phrase hits
        for p in phrases:
            if p in hay:
                # longer phrase = stronger
                score = min(1.0, 0.55 + max(len(p.split()), len(p) // 8) * 0.05)
                if score > best_hit[0]:
                    best_hit = (score, "hit", p[:120], pd_name)
        # fuzzy fallback on full query once per file if no strong hit yet
        if best_hit[0] < 0.75:
            fuzzy = best_fuzzy_window(norm_query, hay)
            if fuzzy > best_hit[0]:
                verdict = "hit" if fuzzy >= 0.72 else ("partial" if fuzzy >= 0.48 else "miss")
                best_hit = (fuzzy, verdict, norm_query[:80], pd_name)

    score, verdict, phrase, pd_name = best_hit
    if verdict == "hit" and score < 0.55:
        verdict = "partial"
    return verdict, score, phrase, pd_name


def load_haystacks(coll: str, cache: dict[str, str]) -> list[tuple[str, str]]:
    paths = COLL_PD.get(coll, [])
    out: list[tuple[str, str]] = []
    for rel in paths:
        fp = PD / rel
        if not fp.exists():
            continue
        key = str(fp)
        if key not in cache:
            raw = fp.read_text(encoding="utf-8", errors="replace")
            cache[key] = fold(raw)
        out.append((rel, cache[key]))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        type=Path,
        default=ROOT / "docs" / "private" / "pd_phrase_match_report.tsv",
    )
    ap.add_argument("--collection", action="append", default=[], help="Limit to collection folder name(s)")
    args = ap.parse_args()

    cache: dict[str, str] = {}
    rows: list[dict] = []
    by_coll: dict[str, Counter] = defaultdict(Counter)

    collections = sorted(p for p in CANON.iterdir() if p.is_dir())
    if args.collection:
        want = set(args.collection)
        collections = [p for p in collections if p.name in want]

    for coll_dir in collections:
        coll = coll_dir.name
        haystacks = load_haystacks(coll, cache)
        for path in sorted(coll_dir.glob("*.yml")):
            try:
                d = yaml.safe_load(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if not isinstance(d, dict) or not is_risk_unit(d):
                continue

            unit_id = as_text(d.get("unit_id")) or path.stem
            luna = as_text((d.get("provenance") or {}).get("verification"))
            queries = extract_queries(d)

            if not haystacks:
                verdict, score, phrase, pd_file, field = "no_pd", 0.0, "", "", ""
            elif not queries:
                verdict, score, phrase, pd_file, field = "no_query", 0.0, "", "", ""
            else:
                # try fields in order; keep best verdict
                best = ("miss", 0.0, "", "", "")
                rank = {"hit": 3, "partial": 2, "miss": 1, "no_query": 0}
                for field, raw in queries:
                    v, s, p, f = match_against(fold(raw), haystacks)
                    if rank.get(v, 0) > rank.get(best[0], 0) or (
                        rank.get(v, 0) == rank.get(best[0], 0) and s > best[1]
                    ):
                        best = (v, s, p, f, field)
                    if best[0] == "hit" and best[1] >= 0.8:
                        break
                verdict, score, phrase, pd_file, field = best

            by_coll[coll][verdict] += 1
            by_coll[coll]["risk"] += 1
            rows.append(
                {
                    "collection": coll,
                    "unit_id": unit_id,
                    "verdict": verdict,
                    "score": f"{score:.3f}",
                    "query_field": field,
                    "matched_phrase": phrase,
                    "pd_file": pd_file,
                    "luna": luna,
                    "section": as_text(d.get("section") or d.get("source_id")),
                    "title": as_text(d.get("title")),
                }
            )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(
            fh,
            fieldnames=[
                "collection",
                "unit_id",
                "verdict",
                "score",
                "query_field",
                "matched_phrase",
                "pd_file",
                "luna",
                "section",
                "title",
            ],
            delimiter="\t",
        )
        w.writeheader()
        w.writerows(rows)

    print(f"Audited {len(rows)} risk units → {args.out.relative_to(ROOT)}")
    print()
    print(f"{'collection':40} {'risk':>5} {'hit':>5} {'part':>5} {'miss':>5} {'no_pd':>5} {'no_q':>5}")
    for coll, c in sorted(by_coll.items(), key=lambda kv: -kv[1]["risk"]):
        print(
            f"{coll:40} {c['risk']:5} {c['hit']:5} {c['partial']:5} {c['miss']:5} "
            f"{c['no_pd']:5} {c['no_query']:5}"
        )

    print()
    misses = [r for r in rows if r["verdict"] == "miss"]
    print(f"Misses ({len(misses)}) — strongest fabrication / paraphrase suspects:")
    for r in sorted(misses, key=lambda x: (x["collection"], x["unit_id"]))[:40]:
        print(f"  {r['unit_id']:50} luna={r['luna'][:40] or '-'}  via={r['query_field'] or '-'}")

    no_pd = [r for r in rows if r["verdict"] == "no_pd"]
    if no_pd:
        print()
        print(f"No local PD mapped ({len(no_pd)} units) — need source fetch before phrase-match:")
        for coll, n in sorted(
            Counter(r["collection"] for r in no_pd).items(), key=lambda kv: -kv[1]
        ):
            print(f"  {coll}: {n}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

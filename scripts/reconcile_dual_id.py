#!/usr/bin/env python3
"""Reconcile dual-ID Sanskrit collections: map each opaque legacy unit (e.g.
SVU_001) to the verse range it actually covers by content-matching its stored
IAST against the parsed GRETIL source, then rewrite provenance.section so
coverage detection works and gap-filling won't duplicate.

  python reconcile.py --collection svetasvatara [--apply]
"""
import argparse, glob, os, re, sys
import yaml

REPO = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha"
sys.path.insert(0, os.path.join(REPO, "scripts"))
from faithful_expand_upanishads import COLLS, CANON, parse_gretil  # noqa: E402


def norm(s: str) -> str:
    """Collapse to a comparable fingerprint: IAST letters only, lowercased."""
    s = re.sub(r"\|\|.*?\|\|", " ", s)          # drop verse numbers
    s = re.sub(r"[^a-zāīūṛṝḷḹṅñṭḍṇśṣṃḥ]", "", s.lower())
    return s


def reconcile(cfg, apply):
    verses = parse_gretil(cfg)                    # [(c, v, iast)]
    nverses = [(c, v, norm(t)) for c, v, t in verses]
    joined = "".join(t for _, _, t in nverses)
    # index: char offset -> (c,v) so we can locate a fingerprint in the stream
    offsets, pos = [], 0
    for c, v, t in nverses:
        offsets.append((pos, pos + len(t), c, v)); pos += len(t)

    def at(off):
        for a, b, c, v in offsets:
            if a <= off < b:
                return (c, v)
        return None

    changed = 0
    for path in sorted(glob.glob(os.path.join(CANON, cfg["canon"], "*.yml"))):
        d = yaml.safe_load(open(path)) or {}
        sid = str(d.get("source_id") or "")
        # skip units already coverable by per-verse source_id (SU_CC_VV)
        if cfg.get("cover_id") and re.search(cfg["cover_id"], sid):
            continue
        ia = norm(str(d.get("sanskrit_iast") or d.get("sanskrit_devanagari") or ""))
        if len(ia) < 20:
            continue
        # A unit is a contiguous run of verses: locate its head, then derive the
        # end from head_offset + text length (robust to sandhi variants in a
        # long tail fingerprint, which independent tail-search gets wrong).
        # try a firm head first, then shorten to tolerate variant sandhi /
        # compound word-order (e.g. anila-anala vs anala-anila in Śvet 2.11)
        start = -1
        for hl in (22, 16, 12):
            start = joined.find(ia[:hl])
            if start >= 0:
                break
        prov = d.get("provenance") if isinstance(d.get("provenance"), dict) else {}
        if start < 0:
            print(f"  ? {sid}: NO MATCH (head={ia[:22]}…)")
            continue
        end_off = min(start + len(ia) - 1, len(joined) - 1)
        s, e = at(start), at(end_off)
        c1, v1 = s
        c2, v2 = e if e else s
        ref = f"{cfg['name']} {c1}.{v1}" if (c1, v1) == (c2, v2) else f"{cfg['name']} {c1}.{v1}–{c2}.{v2}"
        old = str(prov.get("section") or "")
        print(f"  ✓ {sid}: {old or '(none)'} -> {ref}")
        if apply:
            prov["section"] = ref
            prov.setdefault("collection", cfg["name"])
            prov["reconciled"] = f"verse range content-matched to {cfg['edition']}"
            d["provenance"] = prov
            yaml.safe_dump(d, open(path, "w"), allow_unicode=True, sort_keys=False, width=100)
            changed += 1
    print(f"[{cfg['name']}] reconciled {changed} units" if apply else "[dry run]")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--collection", required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    reconcile(COLLS[a.collection], a.apply)

"""Attach aligned Sanskrit (Devanagari + IAST) to the 52 Spandakārikā units.
Source: GRETIL Vasugupta Spandakārikā (PD IAST). Alignment: content-aligned real
units + shared units inheriting their owner + colophon. Staged, canonical untouched."""
import json, os, re, sys, glob
import yaml
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iast_to_deva import iast_to_deva
from app.data_loader import normalize_unit, _as_text  # noqa

SP = os.path.dirname(os.path.abspath(__file__))
ROOT = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha"
CANON = os.path.join(ROOT, "data/canonical/yoga_spandakarika")
STAGE = os.path.join(ROOT, "data/staging/spanda_sanskrit")
seq = json.load(open(f"{SP}/spanda_clean.json"))
KAR = {i + 1: seq[i] for i in range(len(seq))}
UNIT_KAR = {int(k): v for k, v in json.load(open(f"{SP}/spanda_unit_karika.json")).items()}
DIG = str.maketrans("0123456789", "०१२३४५६७८९")


def clean(s):
    s = re.sub(r"=[0-9A-F]{2}", "'", s)
    s = re.sub(r"(?<=[a-zāīūṛṝḷṅñṭḍṇśṣṃḥ])\.(?=[a-zāīūṛṝḷṅñṭḍṇśṣṃḥ])", "", s)
    return re.sub(r"\s+", " ", s).strip(" |")


def fmt(klist):
    devs, iasts = [], []
    for k in klist:
        raw = clean(KAR[k])
        parts = [p.strip() for p in raw.split("|") if p.strip()]
        iasts.append(" |\n".join(parts) + f" || {k} ||")
        devs.append(" ।\n".join(iast_to_deva(p) for p in parts) + f" ॥ {str(k).translate(DIG)} ॥")
    return "\n\n".join(devs), "\n\n".join(iasts)


def main():
    write = "--write" in sys.argv
    if write:
        os.makedirs(STAGE, exist_ok=True)
    ok = 0
    for f in sorted(glob.glob(os.path.join(CANON, "*.yml"))):
        n = int(re.search(r"sp_(\d+)", f).group(1))
        klist = UNIT_KAR.get(n, [])
        if not klist:
            print(f"  sp_{n:02d}: NO SANSKRIT (flagged)"); continue
        dev, iast = fmt(klist)
        d = yaml.safe_load(open(f))
        d["sanskrit_devanagari"] = dev
        d["sanskrit_iast"] = iast
        d["source_verse"] = "Spandakārikā " + ",".join(str(k) for k in klist)
        prov = d.get("provenance") if isinstance(d.get("provenance"), dict) else {}
        prov["sanskrit_source"] = ("GRETIL Vasugupta Spandakārikā (PD Sanskrit), kārikā(s) "
                                   + ",".join(str(k) for k in klist) + "; Devanagari from IAST.")
        d["provenance"] = prov
        norm = normalize_unit(d, f)
        has = "original" in {L["kind"] for L in norm["pratibha_layers"]}
        ok += 1
        print(f"  sp_{n:02d} -> kārikā {klist} | original={has} | {dev.splitlines()[0][:34]}")
        if write:
            with open(os.path.join(STAGE, os.path.basename(f)), "w") as fh:
                yaml.safe_dump(d, fh, allow_unicode=True, sort_keys=False, width=120)
    print(f"\n{'wrote' if write else 'previewed'} {ok}/52")


if __name__ == "__main__":
    main()

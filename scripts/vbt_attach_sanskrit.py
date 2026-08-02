"""Attach aligned Sanskrit (Devanagari + IAST) to each of the 112 VBT yuktis.
Source: GRETIL VBT (IAST, PD text). Alignment: Wallis verse markers embedded in
the existing translations, verified monotonic + content-checked, gaps 4/12 hand-
resolved. Devanagari is deterministically transliterated from IAST (round-trip
verified). Writes to STAGING — canonical untouched until promoted."""
import json, os, re, sys, glob
import yaml
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iast_to_deva import iast_to_deva
from app.data_loader import normalize_unit, _as_text  # noqa

SP = os.path.dirname(os.path.abspath(__file__))
ROOT = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha"
CANON = os.path.join(ROOT, "data/canonical/vijnana_bhairava")
STAGE = os.path.join(ROOT, "data/staging/vbt_sanskrit")

verses = json.load(open(f"{SP}/vbt_verses.json"))
align = {int(k): v for k, v in json.load(open(f"{SP}/vbt_alignment_final.json")).items()}
DIG = str.maketrans("0123456789", "०१२३४५६७८९")


def clean_iast(s: str) -> str:
    s = s.replace("=B9", "'")           # quoted-printable avagraha artifact
    s = re.sub(r"=[0-9A-F]{2}", "", s)   # strip any other QP artifacts
    s = s.replace(".ṅd", "ṇḍ")           # GRETIL retroflex-cluster artifact (maṇḍa/piṇḍa)
    s = re.sub(r"(?<=[a-zāīūṛṝḷṅñṭḍṇśṣṃḥ])\.(?=[a-zāīūṛṝḷṅñṭḍṇśṣṃḥ])", "", s)  # any residual stray periods
    s = re.sub(r"\bbhairava uvāca\b|\bśrī devī uvāca\b|\bdevī uvāca\b", "", s)  # speaker tags
    s = re.sub(r"\s*\|\s*", " | ", s)
    s = re.sub(r"\s+", " ", s).strip(" |")
    return s.strip()


def format_verse(vnum: int) -> tuple[str, str]:
    raw = clean_iast(verses[str(vnum)])
    # split the two padas on the internal danda for a clean two-line unit
    parts = [p.strip() for p in raw.split("|") if p.strip()]
    iast = " |\n".join(parts) + f" || {vnum} ||"
    dev_parts = [iast_to_deva(p) for p in parts]
    dev = " ।\n".join(dev_parts) + f" ॥ {str(vnum).translate(DIG)} ॥"
    return dev, iast


def main():
    write = "--write" in sys.argv
    if write:
        os.makedirs(STAGE, exist_ok=True)
    ok = 0
    for f in sorted(glob.glob(os.path.join(CANON, "*.yml"))):
        m = re.search(r"yukti_(\d+)", f)
        n = int(m.group(1))
        vnum = align[n][0]
        dev, iast = format_verse(vnum)
        d = yaml.safe_load(open(f))
        d["sanskrit_devanagari"] = dev
        d["sanskrit_iast"] = iast
        d["source_verse"] = f"VBT {vnum}"
        prov = d.get("provenance") if isinstance(d.get("provenance"), dict) else {}
        prov["sanskrit_source"] = ("GRETIL digitization of the Vijñāna Bhairava (public-domain "
                                   f"Sanskrit); verse {vnum}. Devanagari transliterated from IAST.")
        d["provenance"] = prov
        norm = normalize_unit(d, f)
        kinds = [L["kind"] for L in norm.get("pratibha_layers", [])]
        has_orig = "original" in kinds and bool(_as_text(
            next((L.get("body") for L in norm["pratibha_layers"] if L["kind"] == "original"), "")))
        print(f"  y{n:3} -> VBT {vnum:3} | original={has_orig} iast={'iast' in kinds} | {dev.splitlines()[0][:40]}")
        if write:
            with open(os.path.join(STAGE, os.path.basename(f)), "w") as fh:
                yaml.safe_dump(d, fh, allow_unicode=True, sort_keys=False, width=120)
        ok += 1
    print(f"\n{'wrote' if write else 'previewed'} {ok}/112 yuktis" + (f" -> {STAGE}" if write else ""))


if __name__ == "__main__":
    main()

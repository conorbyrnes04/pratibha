import sys, glob, re, json, yaml
sys.path.insert(0, "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha")
from app.data_loader import _as_text, normalize_unit
frags = json.load(open("data/raw_texts/pd/greek/heraclitus_bywater_patrick_frags.json"))
attached = miss = already = 0
for f in sorted(glob.glob("data/canonical/heraclitus_fragments/*.yml")):
    d = yaml.safe_load(open(f))
    if _as_text(d.get("sanskrit_devanagari")):  # already has Greek
        already += 1; continue
    sid = _as_text(d.get("source_id"))  # HFR_P006
    m = re.search(r"P0*(\d+)", sid)
    if not m: miss += 1; continue
    n = m.group(1)
    if n not in frags or not frags[n].get("greek"):
        miss += 1; continue
    greek = frags[n]["greek"].strip()
    d["sanskrit_devanagari"] = greek
    # update explicit original layer if present so it serves
    for L in (d.get("pratibha_layers") or []):
        if isinstance(L, dict) and L.get("kind") == "original":
            L["body"] = greek
    prov = d.get("provenance") or {}
    prov["greek_source"] = f"Heraclitus fr. {n} (Bywater 1877 Greek, Patrick numbering; local PD corpus)."
    prov["verification"] = "PD source (Bywater 1877, local)"
    d["provenance"] = prov
    d.pop("needs_source_review", None)
    yaml.safe_dump(d, open(f, "w"), allow_unicode=True, sort_keys=False, width=120)
    attached += 1
print(f"Heraclitus: attached Greek to {attached} | already had {already} | no-match {miss}")
# tier check
import collections
t = collections.Counter(normalize_unit(yaml.safe_load(open(f)), f)["editorial_maturity"] for f in glob.glob("data/canonical/heraclitus_fragments/*.yml"))
print("heraclitus tiers now:", dict(t))

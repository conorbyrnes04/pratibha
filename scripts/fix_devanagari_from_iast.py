"""Surgically correct Devanagari verses that disagree with their (reliable) IAST.
For each flagged verse, regenerate ONLY that verse's Devanagari from its IAST and
splice it back, leaving every correct verse untouched. Verifies each correction
round-trips (new Deva -> IAST == source IAST). Dry-run unless --write."""
import json, os, re, sys, glob, collections
import yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iast_to_deva import iast_to_deva

SP = os.path.dirname(os.path.abspath(__file__))
ROOT = "/Users/conorbyrnes04/Documents/Projects/VAK/pratibha"
pure = json.load(open(f"{SP}/pure_errors.json"))
DIG = str.maketrans("0123456789", "०१२३४५६७८९")

# deva->iast for verification
INDEP = {'अ':'a','आ':'ā','इ':'i','ई':'ī','उ':'u','ऊ':'ū','ऋ':'ṛ','ॠ':'ṝ','ऌ':'ḷ','ए':'e','ऐ':'ai','ओ':'o','औ':'au'}
MATRA = {'ा':'ā','ि':'i','ी':'ī','ु':'u','ू':'ū','ृ':'ṛ','ॄ':'ṝ','े':'e','ै':'ai','ो':'o','ौ':'au'}
CONS = {'क':'k','ख':'kh','ग':'g','घ':'gh','ङ':'ṅ','च':'c','छ':'ch','ज':'j','झ':'jh','ञ':'ñ','ट':'ṭ','ठ':'ṭh','ड':'ḍ','ढ':'ḍh','ण':'ṇ','त':'t','थ':'th','द':'d','ध':'dh','न':'n','प':'p','फ':'ph','ब':'b','भ':'bh','म':'m','य':'y','र':'r','ल':'l','व':'v','श':'ś','ष':'ṣ','स':'s','ह':'h','ळ':'ḻ'}
OTHER = {'ं':'ṃ','ः':'ḥ','ँ':'m̐','ऽ':"'"}
def d2i(t):
    o = []; i = 0
    while i < len(t):
        c = t[i]
        if c in CONS:
            o.append(CONS[c]); nx = t[i+1] if i+1 < len(t) else ''
            if nx == '्': i += 2; continue
            if nx in MATRA: o.append(MATRA[nx]); i += 2; continue
            o.append('a'); i += 1; continue
        if c in INDEP: o.append(INDEP[c]); i += 1; continue
        if c in OTHER: o.append(OTHER[c]); i += 1; continue
        o.append(c); i += 1
    return ''.join(o)
def norm(s):
    return re.sub(r"[|॥।\s'\-०-९0-9.]", "", s.lower())


def iast_verses(text):
    out = {}
    parts = re.split(r"\|\|\s*([\d.]+)\s*\|\|", text)
    buf = parts[0]; i = 1
    while i < len(parts):
        out[parts[i].strip()] = buf.strip(); buf = parts[i+1] if i+1 < len(parts) else ''; i += 2
    return out


by_file = collections.defaultdict(set)
for r in pure:
    by_file[r['file']].add(r['verse'])

write = "--write" in sys.argv
fixed = failed = 0
for f, verses in sorted(by_file.items()):
    d = yaml.safe_load(open(f))
    dev = d['sanskrit_devanagari']; iv = iast_verses(d['sanskrit_iast'])
    blocks = dev.split("\n\n")
    changed = False
    for idx, blk in enumerate(blocks):
        m = re.search(r"॥\s*([\d०-९.]+)\s*॥", blk)
        if not m:
            continue
        vn = m.group(1).translate(str.maketrans('०१२३४५६७८९', '0123456789'))
        if vn not in verses or vn not in iv:
            continue
        body = re.sub(r"\|\|.*", "", iv[vn]).strip()
        new_dev = iast_to_deva(body) + f" ॥ {vn.translate(DIG)} ॥"
        # verify round-trip
        if norm(d2i(new_dev)) != norm(iv[vn]):
            print(f"  SKIP {os.path.basename(f)} v{vn}: round-trip check failed"); failed += 1; continue
        old = blk
        blocks[idx] = new_dev
        changed = True
        print(f"  {os.path.basename(f)} v{vn}:")
        print(f"    - {old.strip()}")
        print(f"    + {new_dev}")
        fixed += 1
    if changed and write:
        d['sanskrit_devanagari'] = "\n\n".join(blocks)
        with open(f, "w") as fh:
            yaml.safe_dump(d, fh, allow_unicode=True, sort_keys=False, width=120)

print(f"\n{'FIXED' if write else 'would fix'} {fixed} verses across {len(by_file)} files | round-trip failures: {failed}")

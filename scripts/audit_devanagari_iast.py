"""Per-verse Devanagari vs IAST scan. Splits each unit's sanskrit_devanagari and
sanskrit_iast into individual verses by their || N || / ॥ N ॥ markers, aligns by
verse number, and flags real word-level disagreements (ignoring pure diacritic
loss and placeholder-note fields). Writes the mismatch list to JSON."""
import glob, yaml, re, json, collections
from difflib import SequenceMatcher

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
    s = s.lower(); s = re.sub(r"[|॥।\s'\-]", "", s); return re.sub(r"[०-९0-9.]", "", s)


def strip_dia(s):
    return s.translate(str.maketrans('āīūṛṝḷṅñṭḍṇśṣṃḥ', 'aiurllnntdnssmh'))


def has_dev(s):
    return bool(re.search(r"[ऀ-ॿ]", s))


def split_verses(text, dev):
    """Return {verse_num: verse_text} split on trailing markers. Handles
    ॥ १.४ ॥ / ॥ २४ ॥ / || 1.4 || / || 24 || forms; verse number = last group."""
    out = {}
    marker = r"॥\s*([\d०-९.]+)\s*॥" if dev else r"\|\|\s*([\d.]+)\s*\|\|"
    parts = re.split(marker, text)
    buf = parts[0]; i = 1
    while i < len(parts):
        num = parts[i]
        # devanagari digits -> arabic
        num = num.translate(str.maketrans('०१२३४५६७८९', '0123456789'))
        out[num.strip('.')] = buf.strip()
        buf = parts[i+1] if i+1 < len(parts) else ''
        i += 2
    return out


rows = []
placeholder = 0
for f in sorted(glob.glob('data/canonical/*/*.yml')):
    d = yaml.safe_load(open(f))
    dev = str(d.get('sanskrit_devanagari') or ''); iast = str(d.get('sanskrit_iast') or '')
    if not has_dev(dev) or not iast.strip() or iast.strip().startswith('*'):
        continue
    # skip placeholder-note fields (English prose mixed in)
    if re.search(r'\b(received text|does not provide|the key verse|not aligned|pending)\b', dev + iast, re.I):
        placeholder += 1; continue
    dv = split_verses(dev, True); iv = split_verses(iast, False)
    common = set(dv) & set(iv)
    if not common:  # single-verse unit, no markers matched: compare whole
        common = {'_whole'}; dv = {'_whole': dev}; iv = {'_whole': iast}
    for vn in sorted(common):
        b = norm(d2i(dv[vn])); s = norm(iv[vn])
        if not b or not s:
            continue
        r = SequenceMatcher(None, b, s).ratio()
        if r >= 0.92:
            continue
        kind = 'diacritic' if SequenceMatcher(None, strip_dia(b), strip_dia(s)).ratio() >= 0.92 else 'REAL'
        rows.append({'file': f, 'coll': f.split('/')[-2], 'verse': vn, 'ratio': round(r, 2),
                     'kind': kind, 'dev': dv[vn][:60], 'iast': iv[vn][:60]})

real = [r for r in rows if r['kind'] == 'REAL']
dia = [r for r in rows if r['kind'] == 'diacritic']
print(f"per-verse scan: {len(real)} REAL word-errors, {len(dia)} diacritic-only, {placeholder} placeholder units skipped")
print("\nREAL errors by collection:")
for c, n in collections.Counter(r['coll'] for r in real).most_common():
    print(f"  {c:34} {n}")
json.dump(real, open('/private/tmp/claude-502/-Users-conorbyrnes04-Documents-Projects-VAK-pratibha/8c1784bd-13e3-4f53-83f1-d1943f549304/scratchpad/real_errors.json', 'w'), ensure_ascii=False, indent=0)
print("\nsample REAL errors:")
for r in real[:12]:
    print(f"  {r['coll'][:20]}/{r['verse']}: dev={r['dev'][:34]!r} iast={r['iast'][:34]!r}")

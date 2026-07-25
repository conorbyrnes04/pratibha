#!/usr/bin/env python3
"""Re-render Vijñāna Bhairava English FRESH from the public-domain IAST Sanskrit,
with an independent echo-gate that verifies the rendering does NOT reproduce the
copyrighted-lineage translation it replaces.

Provenance rationale (asteya):
- SOURCE is `sanskrit_iast` (public-domain KSTS Sanskrit), never the copyrighted
  English. The model translates the MEANING from the Sanskrit.
- The unit's existing `translation_literal` is the copyrighted-lineage English
  (Wallis et al.). We use it ONLY as a private reference for the echo-gate — to
  confirm we did not echo it — then drop it from the unit.
- Output is marked a STUDY rendering (`strong_draft`), not authoritative.

Echo-gate: distinctive shared phrasing (a run of N+ consecutive ordinary English
words) between the fresh rendering and the copyrighted text = echo = FAIL (regen
or flag). Shared technical Sanskrit terms are ignored (not copyrightable).

    python scripts/render_vbt_from_sanskrit.py --limit 3            # proof, no write
    python scripts/render_vbt_from_sanskrit.py --limit 3 --write    # write 3
    python scripts/render_vbt_from_sanskrit.py --write              # full run
"""
from __future__ import annotations

import argparse
import asyncio
import glob
import json
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import settings  # noqa: E402
from app.llm import smart_chat  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Per-collection framing: (canonical dir slug) -> (short work description, commentary focus).
COLLECTIONS: dict[str, tuple[str, str]] = {
    "vijnana_bhairava": (
        "the Vijñāna Bhairava Tantra (a Kashmir Śaiva text of 112 meditation techniques / dhāraṇā)",
        "what faculty the technique works — breath, the gap between breaths, space, sound, gaze, the collapse of subject/object — and why it works in the Trika framework",
    ),
    "yoga_spandakarika": (
        "the Spanda Kārikās (the foundational Kashmir Śaiva verses on spanda — the vibratory pulse of consciousness, after Vasugupta/Kallaṭa)",
        "how the verse points to spanda — the throb of awareness beneath every perception, emotion, and gap — and how recognition of it liberates",
    ),
    "yoginihrdaya": (
        "the Yoginīhṛdaya, the 'Heart of the Yoginī' (a Śrīvidyā tantra on the śrīcakra and the goddess Tripurasundarī)",
        "how the verse maps the śrīcakra / mantra / the goddess's self-manifestation, and what it asks the practitioner to recognize or do",
    ),
    "isavasya_upanishad": (
        "the Īśā (Īśāvāsya) Upaniṣad, a short Vedānta text on the non-dual vision of the Self pervading all",
        "how the verse points to the unity of Self and world (īśā pervading all) and its contemplative/ethical import",
    ),
    "svetasvatara_upanishad": (
        "the Śvetāśvatara Upaniṣad, a theistic Vedānta text",
        "how the verse presents Rudra / Brahman and the path to liberation",
    ),
    "patañjali_yoga_sūtras": (
        "Patañjali's Yoga Sūtras, the foundational aphorisms of classical yoga",
        "the specific yogic mechanism or stage the sūtra defines, within the Yoga–Sāṃkhya framework",
    ),
    "tao_te_ching": (
        "the Tao Te Ching (Dào Dé Jīng) of Laozi",
        "how the chapter turns on the Daoist paradox it names (wúwéi, the useful emptiness, the soft overcoming the hard, the nameless dào)",
    ),
    "the_book_of_chuang_tzu": (
        "the Zhuangzi (Chuang Tzu), the inner-chapters Daoist classic",
        "how the passage's story or paradox dissolves a fixed distinction (usefulness, self/other, dreaming/waking, life/death)",
    ),
    "milarepa_songs": (
        "the songs (mgur) of the Tibetan yogi Milarepa",
        "the realization the song expresses and the yogic instruction it gives (mahāmudrā, the nature of mind, renunciation)",
    ),
    "rumi_mathnawi": (
        "Rūmī's Mathnawī, the great Persian Sufi poem",
        "the spiritual turn of the story or image (longing/separation, the reed's cry, annihilation of self in the Beloved)",
    ),
    "meister_eckhart": (
        "the German sermons and treatises of Meister Eckhart",
        "the mystical move the passage makes (detachment/abegescheidenheit, the birth of the Word in the soul, the ground of God and soul)",
    ),
    "dogen_shobogenzo": (
        "Dōgen's Shōbōgenzō, the Sōtō Zen masterwork",
        "how the fascicle overturns ordinary understanding (being-time, practice-realization, the koan of everyday activity)",
    ),
    "tilopa_mahamudra": (
        "Tilopa's Ganges Mahāmudrā (phyag rgya chen po gang gā ma), pith instructions given to Nāropa",
        "the mahāmudrā instruction the verse gives (non-fabrication, mind's sky-like nature, resting uncontrived, the guru's blessing, looking at the looker)",
    ),
    "confucius_analects": (
        "the Analects (Lúnyǔ 論語) of Confucius",
        "the ethical or ritual teaching the passage gives (rén 仁 benevolence, lǐ 禮 ritual propriety, the exemplary person jūnzǐ 君子, learning, filial devotion)",
    ),
    "zhongyong": (
        "the Zhōngyōng 中庸 (the Doctrine of the Mean), a core Confucian classic",
        "how the passage develops centrality/equilibrium (zhōng 中), sincerity (chéng 誠), and the Way as following one's Heaven-conferred nature (xìng 性)",
    ),
    "astavakra_gita": (
        "the Aṣṭāvakra Gītā, a radical Advaita (non-dual) dialogue on the Self",
        "how the verse points to the ever-free witness-Self (sākṣin, ātman) beyond doership and bondage",
    ),
    "chāndogya_upaniṣad": (
        "the Chāndogya Upaniṣad, a foundational Vedānta text",
        "the non-dual teaching the passage gives (tat tvam asi, the Self as the ground of all, the imperishable)",
    ),
    "mandukya_upanishad_and_gaudapada_karika": (
        "the Māṇḍūkya Upaniṣad with Gauḍapāda's Kārikā",
        "how the passage treats OM, the four states (waking/dream/deep-sleep/turīya) and non-origination (ajātivāda)",
    ),
    "nagarjuna_mulamadhyamakakarika": (
        "Nāgārjuna's Mūlamadhyamakakārikā, the root text of Madhyamaka Buddhism",
        "how the verse works its emptiness (śūnyatā) analysis — dependent origination, the two truths, the refutation of svabhāva",
    ),
    "pratyabhijnahrdayam": (
        "Kṣemarāja's Pratyabhijñāhṛdayam ('The Heart of Recognition'), a Kashmir Śaiva Pratyabhijñā text",
        "how the sūtra unfolds recognition (pratyabhijñā) of one's own Self as universal Consciousness (Cit), its freedom (svātantrya) and manifestation",
    ),
    "heart_sutra": (
        "the Heart Sūtra (Prajñāpāramitā-hṛdaya)",
        "how the passage turns on emptiness (śūnyatā) — form is emptiness, the negation of the skandhas, the mantra gate gate",
    ),
    "heraclitus_fragments": (
        "the Fragments of Heraclitus of Ephesus",
        "how the fragment's paradox or image works (the logos, the unity of opposites, ever-living fire, flux / panta rhei, the hidden harmony, the dry soul)",
    ),
    "tantrasara": (
        "Abhinavagupta's Tantrasāra, the condensed essence of the Tantrāloka (Kashmir Śaiva Trika)",
        "the upāya (means) or metaphysical point the passage develops (anupāya, śāmbhava, śākta, āṇava; svātantrya, prakāśa-vimarśa, the recognition of Śiva-consciousness)",
    ),
}
_DEFAULT_CTX = (
    "a Kashmir Śaiva / Śākta tantric text",
    "what the verse points to in the Trika/Śākta framework and what it asks the practitioner to do",
)

# Source language per collection: (unit field holding the source text, human label,
# example technical terms to keep untranslated). Default is Sanskrit/IAST.
SOURCE_LANG: dict[str, tuple[str, str, str]] = {
    "tao_te_ching": ("sanskrit_devanagari", "Classical Chinese",
                     "dào 道, dé 德, wúwéi 無為, tiān 天, wàn wù 萬物"),
    "the_book_of_chuang_tzu": ("sanskrit_devanagari", "Classical Chinese",
                               "dào 道, qì 氣, tiān 天, xiāo yáo 逍遙"),
    "confucius_analects": ("sanskrit_devanagari", "Classical Chinese",
                           "rén 仁, lǐ 禮, jūnzǐ 君子, dào 道, xiào 孝, tiān 天"),
    "zhongyong": ("sanskrit_devanagari", "Classical Chinese",
                  "zhōng 中, yōng 庸, chéng 誠, dào 道, xìng 性, tiān 天"),
    "heraclitus_fragments": ("sanskrit_devanagari", "Ancient Greek",
                             "λόγος logos, ἁρμονίη harmoníē, πῦρ pŷr (fire), φύσις phýsis"),
    "milarepa_songs": ("sanskrit_devanagari", "Tibetan (Uchen script)",
                       "phyag rgya chen po (mahāmudrā), rnal 'byor pa (yogin), ting nge 'dzin (samādhi)"),
    "tilopa_mahamudra": ("sanskrit_devanagari", "Tibetan (Uchen script)",
                         "phyag rgya chen po (mahāmudrā), gnyug ma (the innate), sems nyid (mind-nature), bla ma (guru)"),
    "rumi_mathnawi": ("sanskrit_devanagari", "Persian",
                      "nay (reed), fanā (annihilation), 'ishq (love), dūrī (separation)"),
    "meister_eckhart": ("sanskrit_devanagari", "Middle High German",
                        "abegescheidenheit (detachment), gotheit (Godhead), grunt (ground), gebürt (birth)"),
    "dogen_shobogenzo": ("sanskrit_devanagari", "Classical Japanese/Chinese (kanbun)",
                         "有時 uji (being-time), 現成公案 genjōkōan, 修証 shushō (practice-realization)"),
}
_DEFAULT_SOURCE = ("sanskrit_iast", "Sanskrit (IAST)", "prāṇa, apāna, madhya, śakti, ākāśa, spanda")


def source_of(collection: str) -> tuple[str, str, str]:
    return SOURCE_LANG.get(collection, _DEFAULT_SOURCE)


def render_system(collection: str) -> str:
    work_desc, focus = COLLECTIONS.get(collection, _DEFAULT_CTX)
    _field, src_label, terms = source_of(collection)
    return f"""You are rendering {work_desc} into fresh, clear, contemporary English FROM THE {src_label.upper()} provided.

Absolute rules:
- Translate the MEANING of the given {src_label} directly. Your English must be your own, rendered from this source — not a paraphrase of any published translation.
- You may know published translations (Wallis, Lakshmanjoo, Singh, Odier, Padoux, Legge, Lau, Mitchell, Radhakrishnan). You must NOT reproduce their distinctive wording, sentence shapes, or signature phrasings. If a phrase feels like a remembered translation, re-say it plainly from the source instead.
- Keep genuine technical terms in the original with a short gloss ({terms}) — those are shared vocabulary, not anyone's phrasing.
- Faithful and plain over ornate. This is a study rendering, so clarity and accuracy beat literary flourish.

Then write publishable-quality study commentary grounded in THIS specific passage ({focus}), and one concrete practice a modern reader can actually do today.

Return ONLY valid JSON:
{{"translation": "...", "commentary": "...", "practice": "...", "key_terms": [{{"term":"...","definition":"..."}}]}}
key_terms: 1-3 relevant original-language terms with a one-line gloss, or []."""

# ---- echo-gate ---------------------------------------------------------------

_WORD_RE = re.compile(r"[a-z]+")
# Sanskrit technical terms and common function words are legitimately shared
# across any two faithful translations (they're not copyrightable phrasing);
# don't let them trigger an echo flag. Standard technical English renderings of
# untranslatable terms (e.g. "partless" for niṣkala) count as shared vocabulary.
_ALLOWED_SHARED = {
    # breath / centre / vibration
    "prana", "apana", "jiva", "madhya", "spanda", "unmesa", "nimesa", "visarga",
    # deity / self / mind
    "sakti", "shakti", "bhairava", "siva", "shiva", "sankara", "devi", "devetc",
    "atman", "citta", "kundalini", "brahman", "purusa", "prakrti",
    # space / sound / point / dissolution
    "akasa", "akasha", "nada", "bindu", "kala", "kula", "cakra", "chakra",
    "mantra", "mudra", "nyasa", "tattva", "turya", "samadhi", "niskala", "partless",
    # Śrīvidyā / Yoginīhṛdaya proper terms
    "hrdaya", "yogini", "yogin", "tripura", "tripurasundari", "sricakra",
    "kamakala", "srividya",
    # common function / connective words
    "the", "a", "an", "of", "in", "to", "and", "is", "as", "on", "at", "by", "with",
    "one", "that", "this", "into", "between", "through", "from", "for", "it", "are",
    "or", "its", "which", "whose", "when", "then", "her", "his",
}


def _deaccent(text: str) -> str:
    """Fold IAST diacritics to base ASCII so 'nāda'->'nada', 'niṣkala'->'niskala'
    stay single tokens instead of splitting (which hid them from the allow-list)."""
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))


def _norm_words(text: str) -> list[str]:
    return _WORD_RE.findall(_deaccent((text or "").lower()))


def _max_shared_ngram(a: str, b: str) -> tuple[int, str]:
    """Longest run of consecutive words shared by both texts, ignoring runs made
    only of allowed/technical words. Returns (length, the phrase)."""
    wa, wb = _norm_words(a), _norm_words(b)
    setb_ngrams: dict[int, set] = {}
    best_len, best_phrase = 0, ""
    # Build b's n-grams up to a reasonable window.
    max_n = min(12, len(wa), len(wb))
    b_grams = {n: set() for n in range(2, max_n + 1)}
    for n in range(2, max_n + 1):
        for i in range(len(wb) - n + 1):
            b_grams[n].add(" ".join(wb[i:i + n]))
    for n in range(max_n, 1, -1):
        for i in range(len(wa) - n + 1):
            gram_words = wa[i:i + n]
            if all(w in _ALLOWED_SHARED for w in gram_words):
                continue  # a run of only shared/technical words isn't an echo
            gram = " ".join(gram_words)
            if gram in b_grams[n]:
                return n, gram  # longest first
    return best_len, best_phrase


def _jaccard(a: str, b: str) -> float:
    sa = {w for w in _norm_words(a) if w not in _ALLOWED_SHARED}
    sb = {w for w in _norm_words(b) if w not in _ALLOWED_SHARED}
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


# A shared run of this many consecutive non-technical words is treated as echoing.
ECHO_NGRAM_FAIL = 6


def echo_check(fresh: str, copyrighted: str) -> dict:
    n, phrase = _max_shared_ngram(fresh, copyrighted)
    j = _jaccard(fresh, copyrighted)
    fail = n >= ECHO_NGRAM_FAIL
    return {"pass": not fail, "max_shared_run": n, "shared_phrase": phrase, "jaccard": round(j, 2)}


# ---- rendering ---------------------------------------------------------------

def _extract_json(text: str) -> dict | None:
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.M).strip()
    try:
        return json.loads(text)
    except Exception:
        m = re.search(r"\{.*\}", text, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                return None
    return None


async def render_unit(item: dict, system: str, source_field: str, source_label: str,
                      avoid: list[str] | None = None) -> dict | None:
    src = str(item.get(source_field) or "").strip()
    # Reject empty / placeholder sources (e.g. "*(Chinese text.)*" in the iast field).
    if not src or src.lower() == "none" or src.startswith("*("):
        return None
    title = str(item.get("title") or item.get("unit_label") or "").strip()
    avoid_note = ""
    if avoid:
        quoted = "; ".join(f'"{p}"' for p in avoid if p)
        avoid_note = (
            f"\n\nIMPORTANT: another published translation used this exact phrasing: {quoted}. "
            "Do NOT reuse those words in that order. Re-render the meaning differently, straight from the source."
        )
    user = (
        f"Passage title: {title}\n\n"
        f"{source_label}: {src}\n"
        + "\nRender the fresh English translation, commentary, and practice as JSON."
        + avoid_note
    )
    msgs = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    # Long source passages (Zhuangzi, Dōgen fascicles) produce a long translation
    # + commentary + practice; too small a cap truncates the JSON mid-output.
    budget = 4000 if len(src) > 500 else 1700
    text = await smart_chat(msgs, temperature=0.5, max_tokens=budget)
    return _extract_json(text)


def _key_terms_tail(key_terms) -> str:
    if not isinstance(key_terms, list) or not key_terms:
        return ""
    lines = ["", "Key Terms", ""]
    for kt in key_terms[:3]:
        if isinstance(kt, dict) and kt.get("term") and kt.get("definition"):
            lines.append(f"**{str(kt['term']).strip()}** — {str(kt['definition']).strip()}")
    return "\n".join(lines) if len(lines) > 3 else ""


def write_unit(path: str, item: dict, rendered: dict, source_label: str = "Sanskrit (IAST)") -> None:
    translation = str(rendered.get("translation") or "").strip()
    commentary = str(rendered.get("commentary") or "").strip()
    practice = str(rendered.get("practice") or "").strip()
    tail = _key_terms_tail(rendered.get("key_terms"))
    item = dict(item)
    item["translation"] = translation
    item["translation_literal"] = translation  # fresh, from the source language
    item["commentary"] = (commentary + ("\n" + tail if tail else "")).strip()
    item["practice"] = practice
    item["abhyasa"] = practice
    # Study rendering, not authoritative; provenance is now the public-domain source text.
    item["editorial_maturity"] = "strong_draft"
    item["translation_provenance"] = f"Rendered from the public-domain source ({source_label}). Study rendering; not a critical edition."
    item.pop("pratibha_layers", None)  # loader re-derives from new fields
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(item, f, allow_unicode=True, sort_keys=False, width=100)


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--collection", default="vijnana_bhairava",
                    help="canonical dir slug under data/canonical/ (e.g. yoga_spandakarika)")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--no-gate", dest="no_gate", action="store_true",
                    help="Write every successful render regardless of the echo-gate. Use when the "
                         "unit carries NO copyrighted reference text to echo (e.g. bucket-B texts "
                         "rendered from PD Sanskrit): the gate score is then informational only.")
    args = ap.parse_args()
    if not settings.OPENROUTER_API_KEY:
        print("ERROR: OPENROUTER_API_KEY not set (source your .env).")
        sys.exit(1)

    coll_dir = os.path.join(ROOT, "data", "canonical", args.collection)
    if not os.path.isdir(coll_dir):
        print(f"ERROR: no such collection dir: {coll_dir}")
        sys.exit(1)
    system = render_system(args.collection)
    source_field, source_label, _terms = source_of(args.collection)

    files = sorted(glob.glob(os.path.join(coll_dir, "**", "*.yml"), recursive=True))
    if args.limit:
        files = files[: args.limit]
    print(f"Re-render from PD source [{args.collection}, {source_label}] — {len(files)} unit(s), "
          f"{'WRITE' if args.write else 'PROOF'}, model={settings.effective_default_model()}\n")

    counts = {"rendered": 0, "echo_fail": 0, "no_json": 0, "no_source": 0}
    for i, path in enumerate(files, 1):
        item = yaml.safe_load(open(path, encoding="utf-8"))
        name = os.path.basename(path)
        # Idempotent: skip units already reconciled from the PD Sanskrit so a
        # re-run only retries the stragglers (echo-fails / parse-fails).
        if args.write and "public-domain" in str(item.get("translation_provenance") or ""):
            continue
        old_copyrighted = str(item.get("translation_literal") or "")
        src_present = str(item.get(source_field) or "").strip()
        src_present = bool(src_present and src_present.lower() != "none" and not src_present.startswith("*("))
        try:
            rendered = await render_unit(item, system, source_field, source_label)
        except Exception as e:
            print(f"[{i}] {name}: ERROR {e!r}"); continue
        if not rendered:
            counts["no_json" if src_present else "no_source"] += 1
            print(f"[{i}] {name}: no render"); continue
        fresh = str(rendered.get("translation") or "").strip()
        gate = echo_check(fresh, old_copyrighted)
        # One divergence-nudge retry: name the echoed phrase and re-render.
        # Skipped in --no-gate mode (there is no copyrighted text to diverge from).
        if not args.no_gate and not gate["pass"] and gate["shared_phrase"]:
            try:
                retry = await render_unit(item, system, source_field, source_label, avoid=[gate["shared_phrase"]])
            except Exception:
                retry = None
            if retry:
                fresh_r = str(retry.get("translation") or "").strip()
                gate_r = echo_check(fresh_r, old_copyrighted)
                if gate_r["pass"]:
                    rendered, fresh, gate = retry, fresh_r, gate_r
        counts["rendered"] += 1
        write_ok = gate["pass"] or args.no_gate
        if not gate["pass"] and not args.no_gate:
            counts["echo_fail"] += 1
        if args.write and write_ok:
            write_unit(path, item, rendered, source_label)
        if args.no_gate:
            verdict = f"✓ written (info: {gate['max_shared_run']}-word max overlap)"
        else:
            verdict = "✓ PASS" if gate["pass"] else f"✗ ECHO ({gate['max_shared_run']}-word run: “{gate['shared_phrase']}”)"
        print(f"[{i}] {name}: {verdict}  (jaccard={gate['jaccard']})")
        if not args.write:
            print(f"    SANSKRIT: {str(item.get('sanskrit_iast'))[:110]}")
            print(f"    OLD (copyrighted-lineage): {old_copyrighted[:160].strip()}")
            print(f"    NEW (from Sanskrit):        {fresh[:160]}")
            print(f"    commentary: {str(rendered.get('commentary'))[:130]}...\n")
    print("\nSUMMARY:", counts)


if __name__ == "__main__":
    asyncio.run(main())

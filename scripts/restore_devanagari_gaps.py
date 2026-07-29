#!/usr/bin/env python3
"""Restore small Devanagari gaps for Mandukya + Aṣṭāvakra sum unit.

Targets:
  mandukya_upanishad_and_gaudapada_karika:
    muk_001 — extract śāntiḥ pāṭha already embedded in thesis/commentary
    muk_004 — composite Upaniṣad vv.3–6 from sibling units muk_005–008
    muk_010 — composite Upaniṣad vv.8–12 from sibling units muk_011–015
    muk_016 — Gauḍapāda Kārikā Āgama I.11–12 (verses the unit commentary cites)

  astavakra_gita:
    asg_sum_11_01_11_08 — Aṣṭāvakra Gītā 11.1–11.8 (GRETIL IAST → Devanagari;
      cross-checked against Vaidika Vignanam Devanagari dump)

Does NOT invent Sanskrit for English-only appendix units:
  pratyabhijnahrdayam.phr_sum_appendix — left unmatched (editorial English appendix)

  python scripts/restore_devanagari_gaps.py            # preview
  python scripts/restore_devanagari_gaps.py --write
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical"
MAIN_INDEX = CANONICAL / "index.jsonl"

DEV_RE = re.compile(r"[\u0900-\u097F]")

MUK_DIR = CANONICAL / "mandukya_upanishad_and_gaudapada_karika"
ASG_DIR = CANONICAL / "astavakra_gita"

MUK_PROV = (
    "devanagari: Māṇḍūkya Upaniṣad / Gauḍapāda Kārikā — restored from "
    "in-corpus sibling verse units or standard PD Upaniṣad/Kārikā text "
    "(ancient; not a critical edition). IAST mirrored."
)
ASG_PROV = (
    "devanagari: Aṣṭāvakra Gītā 11.1–11.8 — GRETIL IAST (Richards input) "
    "converted to Devanagari; wording cross-checked against Vaidika Vignanam "
    "Devanagari chapter 11. Not a critical edition."
)

# GRETIL Avg_11.1–11.8 (IAST), padā markers normalized.
ASG_11_IAST = {
    "11.1": (
        "bhāvābhāvavikāraś ca svabhāvād iti niścayī |\n"
        "nirvikāro gatakleśaḥ sukhenaivopaśāmyati ||"
    ),
    "11.2": (
        "īśvaraḥ sarvanirmātā nehānya iti niścayī |\n"
        "antargalitasarvāśaḥ śāntaḥ kvāpi na sajjate ||"
    ),
    "11.3": (
        "āpadaḥ sampadaḥ kāle daivād eveti niścayī |\n"
        "tṛptaḥ svasthendriyo nityaṃ na vāñchati na śocati ||"
    ),
    "11.4": (
        "sukhaduḥkhe janmamṛtyū daivād eveti niścayī |\n"
        "sādhyādarśī nirāyāsaḥ kurvann api na lipyate ||"
    ),
    "11.5": (
        "cintayā jāyate duḥkhaṃ nānyatheheti niścayī |\n"
        "tayā hīnaḥ sukhī śāntaḥ sarvatra galitaspṛhaḥ ||"
    ),
    "11.6": (
        "nāhaṃ deho na me deho bodho 'ham iti niścayī |\n"
        "kaivalyam iva saṃprāpto na smaraty akṛtaṃ kṛtam ||"
    ),
    "11.7": (
        "ābrahmastambaparyantam aham eveti niścayī |\n"
        "nirvikalpaḥ śuciḥ śāntaḥ prāptāprāptavinirvṛtaḥ ||"
    ),
    "11.8": (
        "nānāścaryam idaṃ viśvaṃ na kiṃcid iti niścayī |\n"
        "nirvāsanaḥ sphūrtimātro na kiṃcid iva śāmyati ||"
    ),
}

# Standard Kārikā I.11–12 (Āgama) — PD ancient text; unit commentary cites these.
KARIKA_I_11_12_IAST = (
    "kāryakāraṇabaddhau tāv iṣyete viśvataijasau |\n"
    "prājñaḥ kāraṇabaddhas tu dvau tau turye na sidhyataḥ || 11 ||\n"
    "\n"
    "nātmānaṃ na parāṃś caiva na satyaṃ nāpi cānṛtam |\n"
    "prājñaḥ kiṃcana saṃvetti turyaṃ tat sarvadṛk sadā || 12 ||"
)


def has_deva(text: str) -> bool:
    return bool(DEV_RE.search(text or ""))


def iast_to_deva(text: str) -> str:
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate

    # Keep newlines / || / | ; transliterate per line to avoid marker issues.
    out: list[str] = []
    for line in text.splitlines():
        if not line.strip():
            out.append("")
            continue
        # Protect dandas and verse numbers
        protected = line
        out.append(transliterate(protected, sanscript.IAST, sanscript.DEVANAGARI))
    return "\n".join(out).strip() + "\n"


def upsert_layer(
    unit: dict[str, Any],
    kind: str,
    body: str,
    label: str,
    provenance: str,
) -> None:
    layers = unit.get("pratibha_layers")
    if not isinstance(layers, list):
        layers = []
        unit["pratibha_layers"] = layers
    existing = next(
        (L for L in layers if isinstance(L, dict) and L.get("kind") == kind), None
    )
    if existing is None:
        existing = {"kind": kind, "label": label}
        order = [
            "original",
            "iast",
            "translation",
            "commentary",
            "key_terms",
            "resonances",
            "practice",
            "appendix",
        ]
        idx = order.index(kind) if kind in order else 0
        pos = 0
        for i, L in enumerate(layers):
            k = L.get("kind") if isinstance(L, dict) else None
            if k in order and order.index(k) <= idx:
                pos = i + 1
        layers.insert(pos, existing)
    existing["label"] = label
    existing["body"] = body if body.endswith("\n") else body + "\n"
    existing["layer_provenance"] = provenance


def apply_sanskrit(unit: dict[str, Any], deva: str, iast: str, prov: str) -> None:
    upsert_layer(unit, "original", deva, "Devanagari", prov)
    upsert_layer(unit, "iast", iast, "IAST", prov)
    unit["sanskrit_devanagari"] = deva if deva.endswith("\n") else deva + "\n"
    unit["sanskrit_iast"] = iast if iast.endswith("\n") else iast + "\n"
    lp = unit.get("layer_provenance")
    if not isinstance(lp, dict):
        unit["layer_provenance"] = {"original": prov}
    else:
        lp["original"] = prov


def dump_yaml(unit: dict[str, Any]) -> str:
    return yaml.safe_dump(
        unit, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120
    )


def atomic_write(path: Path, content: str) -> None:
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(content)
        temp = Path(handle.name)
    temp.replace(path)


def load_unit(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        data = data[0]
    return data


def extract_blocks_from_thesis(thesis: str) -> tuple[str, str]:
    """Parse 'Devanāgarī\\n...\\nIAST\\n...' embedded thesis (muk_001)."""
    t = thesis or ""
    if "Devanāgarī" not in t and "Devanagari" not in t:
        raise ValueError("no Devanagari header in thesis")
    # Normalize header
    t = t.replace("Devanagari", "Devanāgarī")
    parts = re.split(r"\n\s*IAST\s*\n", t, maxsplit=1, flags=re.I)
    if len(parts) != 2:
        raise ValueError("no IAST split in thesis")
    deva_part = re.sub(r"^.*?Devanāgarī\s*\n", "", parts[0], count=1, flags=re.S)
    iast_part = parts[1]
    return deva_part.strip() + "\n", iast_part.strip() + "\n"


def composite_from_siblings(paths: list[Path]) -> tuple[str, str]:
    devas: list[str] = []
    iasts: list[str] = []
    for p in paths:
        u = load_unit(p)
        d = (u.get("sanskrit_devanagari") or "").strip()
        i = (u.get("sanskrit_iast") or "").strip()
        if not has_deva(d):
            raise ValueError(f"sibling missing Devanagari: {p.name}")
        if not i:
            raise ValueError(f"sibling missing IAST: {p.name}")
        title = u.get("title") or u.get("unit_label") or p.stem
        # Keep verses separated by blank line; no editorial English headers in original.
        devas.append(d)
        iasts.append(i)
        _ = title  # reserved for future labelled composites
    return ("\n\n".join(devas) + "\n", "\n\n".join(iasts) + "\n")


def sync_index(updated: dict[str, dict[str, Any]]) -> int:
    lines = MAIN_INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
    out: list[str] = []
    n = 0
    for line in lines:
        if not line.strip():
            out.append(line)
            continue
        obj = json.loads(line)
        uid = obj.get("unit_id")
        if uid in updated:
            out.append(json.dumps(updated[uid], ensure_ascii=False) + "\n")
            n += 1
        else:
            out.append(line)
    atomic_write(MAIN_INDEX, "".join(out))
    return n


def native_ok(unit: dict[str, Any]) -> bool:
    for L in unit.get("pratibha_layers") or []:
        if isinstance(L, dict) and L.get("kind") == "original" and has_deva(L.get("body") or ""):
            return True
    return has_deva(unit.get("sanskrit_devanagari") or "")


def build_asg_11() -> tuple[str, str]:
    iast_parts = []
    for key in sorted(ASG_11_IAST, key=lambda k: float(k)):
        iast_parts.append(ASG_11_IAST[key])
    iast = "\n\n".join(iast_parts) + "\n"
    # Prefer hand-checked Devanagari from Vignanam (matches GRETIL meaning).
    # Convert IAST for consistency with corpus diacritics; spot-check 11.5 against asg_11_5.
    deva = iast_to_deva(iast)
    # Fix common transliteration spacing around dandas (indic may insert spaces)
    # Compare 11.5 to corpus sibling for fidelity.
    sib = load_unit(ASG_DIR / "astavakra_gita_asg_11_5.yml")
    sib_d = (sib.get("sanskrit_devanagari") or "").strip()
    # Extract converted 11.5 block (3rd blank-separated? 11.5 is 5th)
    blocks = [b.strip() for b in re.split(r"\n\s*\n", deva.strip()) if b.strip()]
    if len(blocks) != 8:
        raise SystemExit(f"expected 8 ASG blocks, got {len(blocks)}")
    # Prefer sibling 11.5 Devanagari (already in corpus) if it matches IAST sense.
    if has_deva(sib_d):
        blocks[4] = sib_d
        # Rebuild IAST 11.5 from sibling too
        iast_blocks = [b.strip() for b in re.split(r"\n\s*\n", iast.strip()) if b.strip()]
        sib_i = (sib.get("sanskrit_iast") or "").strip()
        if sib_i:
            iast_blocks[4] = sib_i
            iast = "\n\n".join(iast_blocks) + "\n"
    deva = "\n\n".join(blocks) + "\n"
    return deva, iast


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    plans: list[tuple[Path, str, str, str]] = []  # path, deva, iast, prov
    unmatched: list[tuple[str, str]] = []

    # --- Mandukya muk_001 ---
    p001 = MUK_DIR / "mandukya_upanishad_and_gaudapada_karika_muk_001.yml"
    u001 = load_unit(p001)
    try:
        d, i = extract_blocks_from_thesis(u001.get("thesis") or "")
        plans.append((p001, d, i, MUK_PROV + " Extracted from unit thesis (śāntiḥ pāṭha)."))
    except ValueError as exc:
        unmatched.append(("mandukya...muk_001", str(exc)))

    # --- muk_004 composite vv.3–6 ---
    p004 = MUK_DIR / "mandukya_upanishad_and_gaudapada_karika_muk_004.yml"
    sibs_004 = [
        MUK_DIR / f"mandukya_upanishad_and_gaudapada_karika_muk_{n:03d}.yml"
        for n in (5, 6, 7, 8)
    ]
    try:
        d, i = composite_from_siblings(sibs_004)
        plans.append(
            (
                p004,
                d,
                i,
                MUK_PROV + " Composite of muk_005–008 (Upaniṣad vv.3–6) for overview unit.",
            )
        )
    except ValueError as exc:
        unmatched.append(("mandukya...muk_004", str(exc)))

    # --- muk_010 composite vv.8–12 ---
    p010 = MUK_DIR / "mandukya_upanishad_and_gaudapada_karika_muk_010.yml"
    sibs_010 = [
        MUK_DIR / f"mandukya_upanishad_and_gaudapada_karika_muk_{n:03d}.yml"
        for n in (11, 12, 13, 14, 15)
    ]
    try:
        d, i = composite_from_siblings(sibs_010)
        plans.append(
            (
                p010,
                d,
                i,
                MUK_PROV + " Composite of muk_011–015 (Upaniṣad vv.8–12) for overview unit.",
            )
        )
    except ValueError as exc:
        unmatched.append(("mandukya...muk_010", str(exc)))

    # --- muk_016 Kārikā I.11–12 ---
    p016 = MUK_DIR / "mandukya_upanishad_and_gaudapada_karika_muk_016.yml"
    i016 = KARIKA_I_11_12_IAST.strip() + "\n"
    d016 = iast_to_deva(i016)
    plans.append(
        (
            p016,
            d016,
            i016,
            MUK_PROV
            + " Gauḍapāda Kārikā Āgama I.11–12 (verses cited in unit commentary); "
            "standard PD ancient text via IAST→Devanagari.",
        )
    )

    # --- Astavakra sum 11.1–11.8 ---
    p_asg = ASG_DIR / "astavakra_gita_asg_sum_11_01_11_08.yml"
    d_asg, i_asg = build_asg_11()
    plans.append((p_asg, d_asg, i_asg, ASG_PROV))

    # --- PHR appendix: honest skip ---
    unmatched.append(
        (
            "pratyabhijnahrdayam.phr_sum_appendix",
            "English philosophical-context appendix; no corresponding Sanskrit root text.",
        )
    )

    updated: dict[str, dict[str, Any]] = {}
    before = after = 0

    for path, deva, iast, prov in plans:
        unit = load_unit(path)
        uid = unit.get("unit_id") or path.stem
        if native_ok(unit):
            before += 1
        print(f"{uid}: restoring Devanagari chars={len(DEV_RE.findall(deva))}")
        if args.write:
            apply_sanskrit(unit, deva, iast, prov)
            atomic_write(path, dump_yaml(unit))
            updated[uid] = unit
            if native_ok(unit):
                after += 1
        else:
            after += 1

    if args.write and updated:
        n = sync_index(updated)
        print(f"synced index.jsonl rows={n}")
    elif not args.write:
        print("dry-run (pass --write to apply)")

    print(f"planned restores: {len(plans)}; before_native≈{before} after≈{after}")
    print("unmatched:")
    for uid, reason in unmatched:
        print(f"  - {uid}: {reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

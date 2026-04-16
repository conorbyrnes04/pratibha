#!/usr/bin/env python3
"""
Convert files in data/raw_texts into YAML stubs under data/yaml.

Supported: .txt, .pdf, .epub
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RAW_ROOT_DEFAULT = ROOT / "data" / "raw_texts"
YAML_ROOT_DEFAULT = ROOT / "data" / "yaml"


def slug(s: str) -> str:
    s = re.sub(r"[^\w\s.-]", " ", s, flags=re.UNICODE)
    s = re.sub(r"[\s._-]+", "_", s).strip("_").lower()
    return s or "text"


def title_from_name(name: str) -> str:
    t = re.sub(r"[_-]+", " ", name).strip()
    return re.sub(r"\s+", " ", t).title() or "Unknown Collection"


def ascii_fold(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii").lower()


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def process_file(fp: Path, yaml_root: Path, clear_existing: bool) -> bool:
    stem = fp.stem
    out_dir = yaml_root / slug(stem)
    if clear_existing and out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    collection = title_from_name(stem)
    ext = fp.suffix.lower()
    py = sys.executable

    name_l = fp.name.lower()
    name_ascii = ascii_fold(fp.name)

    if "pratyabhij" in name_l or "pratyabhijn" in name_l:
        out_dir = yaml_root / "pratyabhijnahrdayam"
        if clear_existing and out_dir.exists():
            shutil.rmtree(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        cmd = [py, str(ROOT / "scripts" / "pratyabhijnahrdayam_md_to_yaml.py"), str(fp), str(out_dir)]
        print(f"[raw->yaml] {fp.name} -> {out_dir}")
        run(cmd)
        return True
    if "astavakra" in name_ascii or "ashtavakra" in name_ascii:
        out_dir = yaml_root / "astavakra_gita"
        if clear_existing and out_dir.exists():
            shutil.rmtree(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        cmd = [py, str(ROOT / "scripts" / "astavakra_gita_md_to_yaml.py"), str(fp), str(out_dir)]
        print(f"[raw->yaml] {fp.name} -> {out_dir}")
        run(cmd)
        return True
    if "epictetus" in name_ascii and "enchiridion" in name_ascii:
        out_dir = yaml_root / "epictetus_works"
        if clear_existing and out_dir.exists():
            shutil.rmtree(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        cmd = [py, str(ROOT / "scripts" / "epictetus_enchiridion_md_to_yaml.py"), str(fp), str(out_dir)]
        print(f"[raw->yaml] {fp.name} -> {out_dir}")
        run(cmd)
        return True
    if "dao de jing" in name_ascii or "tao te ching" in name_ascii:
        out_dir = yaml_root / "tao_te_ching"
        if clear_existing and out_dir.exists():
            shutil.rmtree(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        cmd = [py, str(ROOT / "scripts" / "tao_te_ching_md_to_yaml.py"), str(fp), str(out_dir)]
        print(f"[raw->yaml] {fp.name} -> {out_dir}")
        run(cmd)
        return True
    if "zhuangzi" in name_ascii and "pratibha" in name_ascii:
        out_dir = yaml_root / "the_book_of_chuang_tzu"
        if clear_existing and out_dir.exists():
            shutil.rmtree(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        cmd = [py, str(ROOT / "scripts" / "zhuangzi_pratibha_md_to_yaml.py"), str(fp), str(out_dir)]
        print(f"[raw->yaml] {fp.name} -> {out_dir}")
        run(cmd)
        return True
    if "phaedo" in name_ascii and "pratibha" in name_ascii:
        out_dir = yaml_root / "phaedo"
        if clear_existing and out_dir.exists():
            shutil.rmtree(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        cmd = [py, str(ROOT / "scripts" / "phaedo_pratibha_md_to_yaml.py"), str(fp), str(out_dir)]
        print(f"[raw->yaml] {fp.name} -> {out_dir}")
        run(cmd)
        return True
    if "bhagavad" in name_ascii and "gita" in name_ascii and "pratibha" in name_ascii:
        out_dir = yaml_root / "bhagavad_gita"
        if clear_existing and out_dir.exists():
            shutil.rmtree(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        cmd = [py, str(ROOT / "scripts" / "bhagavad_gita_pratibha_md_to_yaml.py"), str(fp), str(out_dir)]
        print(f"[raw->yaml] {fp.name} -> {out_dir}")
        run(cmd)
        return True
    if "mandukya" in name_ascii or "mandukya upanisad" in name_ascii:
        out_dir = yaml_root / "mandukya_upanishad_karika"
        if clear_existing and out_dir.exists():
            shutil.rmtree(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        cmd = [py, str(ROOT / "scripts" / "mandukya_md_to_yaml.py"), str(fp), str(out_dir)]
        print(f"[raw->yaml] {fp.name} -> {out_dir}")
        run(cmd)
        return True
    if "svetasvatara" in name_ascii or "svetasvatara upanisad" in name_ascii:
        out_dir = yaml_root / "svetasvatara_upanishad"
        if clear_existing and out_dir.exists():
            shutil.rmtree(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        cmd = [py, str(ROOT / "scripts" / "svetasvatara_md_to_yaml.py"), str(fp), str(out_dir)]
        print(f"[raw->yaml] {fp.name} -> {out_dir}")
        run(cmd)
        return True
    if "isavasya" in name_ascii or "isha upanishad" in name_ascii or "isavasya upanisad" in name_ascii:
        out_dir = yaml_root / "isavasya_upanishad"
        if clear_existing and out_dir.exists():
            shutil.rmtree(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        cmd = [py, str(ROOT / "scripts" / "isavasya_md_to_yaml.py"), str(fp), str(out_dir)]
        print(f"[raw->yaml] {fp.name} -> {out_dir}")
        run(cmd)
        return True

    if ext == ".txt":
        cmd = [py, str(ROOT / "scripts" / "text_to_yaml.py"), str(fp), str(out_dir), "--collection", collection]
    elif ext == ".pdf":
        if "vbt+translation+wallis" in name_l or "vijnana bhairava" in name_l:
            cmd = [py, str(ROOT / "scripts" / "vbt_wallis_pdf_to_yaml.py"), str(fp), str(out_dir)]
        else:
            cmd = [py, str(ROOT / "scripts" / "pdf_to_yaml.py"), str(fp), str(out_dir), "--collection", collection]
    elif ext == ".epub":
        if name_l == "fragments.epub" or name_l.startswith("fragments"):
            cmd = [py, str(ROOT / "scripts" / "fragments_epub_to_yaml.py"), str(fp), str(out_dir)]
        elif "phaedo" in name_l:
            cmd = [py, str(ROOT / "scripts" / "phaedo_epub_to_yaml.py"), str(fp), str(out_dir)]
        elif "all the works of epictetus" in name_l or "epictetus" in name_l:
            cmd = [py, str(ROOT / "scripts" / "epictetus_works_epub_to_yaml.py"), str(fp), str(out_dir)]
        elif "tao te ching" in name_l:
            cmd = [py, str(ROOT / "scripts" / "tao_te_ching_epub_to_yaml.py"), str(fp), str(out_dir)]
        elif "chuang tzu" in name_l:
            cmd = [py, str(ROOT / "scripts" / "chuang_tzu_epub_to_yaml.py"), str(fp), str(out_dir)]
        elif "yoga spandakarika" in name_l or "spandakarika" in name_l:
            cmd = [py, str(ROOT / "scripts" / "yoga_spandakarika_epub_to_yaml.py"), str(fp), str(out_dir)]
        elif "know yourself" in name_l and "ibn arabi" in name_l:
            cmd = [py, str(ROOT / "scripts" / "ibn_arabi_know_yourself_epub_to_yaml.py"), str(fp), str(out_dir)]
        else:
            cmd = [py, str(ROOT / "scripts" / "epub_to_yaml.py"), str(fp), str(out_dir), "--collection", collection]
    else:
        return False

    print(f"[raw->yaml] {fp.name} -> {out_dir}")
    run(cmd)
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Convert all raw text files to YAML stubs.")
    ap.add_argument("--raw-root", type=Path, default=RAW_ROOT_DEFAULT)
    ap.add_argument("--yaml-root", type=Path, default=YAML_ROOT_DEFAULT)
    ap.add_argument("--clear-existing", action="store_true", default=True)
    args = ap.parse_args()

    raw_root = args.raw_root
    yaml_root = args.yaml_root
    yaml_root.mkdir(parents=True, exist_ok=True)

    files = sorted([p for p in raw_root.iterdir() if p.is_file()]) if raw_root.exists() else []
    if not files:
        print(f"No files found in {raw_root}")
        return 0

    done = 0
    skipped = 0
    for fp in files:
        try:
            ok = process_file(fp, yaml_root, args.clear_existing)
            if ok:
                done += 1
            else:
                skipped += 1
                print(f"[skip] Unsupported extension: {fp.name}")
        except subprocess.CalledProcessError as e:
            print(f"[error] Failed {fp.name}: {e}")

    print(f"Completed: {done} processed, {skipped} skipped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


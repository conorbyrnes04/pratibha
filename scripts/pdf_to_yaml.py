# Best-effort PDF → YAML stubs
import argparse, os, yaml
from pdfminer.high_level import extract_text

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf_path")
    ap.add_argument("output_dir")
    ap.add_argument("--collection", default="Unknown Collection")
    ap.add_argument("--section", default="")
    args = ap.parse_args()

    text = extract_text(args.pdf_path)
    os.makedirs(args.output_dir, exist_ok=True)
    pages = [p.strip() for p in text.split("\f") if p.strip()]
    for i, page in enumerate(pages, start=1):
        yaml_obj = {
            "sutra_id": f"auto-p{i}",
            "collection": args.collection,
            "section": args.section,
            "sanskrit": "",
            "transliteration": "",
            "translation": page.splitlines()[0:4],
            "commentary": "\n".join(page.splitlines()[4:]),
            "modes": {"bhasya":"","doctrinal":"","comparative":"","sadhana":""}
        }
        out = os.path.join(args.output_dir, f"auto_p{i:03d}.yml")
        with open(out, "w", encoding="utf-8") as f:
            yaml.safe_dump(yaml_obj, f, allow_unicode=True, sort_keys=False)
    print(f"Wrote {len(pages)} YAML stubs to {args.output_dir}")

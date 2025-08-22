# Best-effort EPUB → YAML stubs
import argparse, os, re, yaml
from bs4 import BeautifulSoup
from ebooklib import epub, ITEM_DOCUMENT

def clean_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text("\n")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("epub_path")
    ap.add_argument("output_dir")
    ap.add_argument("--collection", default="Unknown Collection")
    ap.add_argument("--section", default="")
    args = ap.parse_args()

    book = epub.read_epub(args.epub_path)
    os.makedirs(args.output_dir, exist_ok=True)
    n = 1
    for item in book.get_items_of_type(ITEM_DOCUMENT):
        text = clean_text(item.get_content())
        if not text or len(text) < 40:
            continue
        yaml_obj = {
            "sutra_id": f"auto-{n}",
            "collection": args.collection,
            "section": args.section,
            "sanskrit": "",
            "transliteration": "",
            "translation": text.splitlines()[0:4],
            "commentary": "\n".join(text.splitlines()[4:]),
            "modes": {"bhasya":"","doctrinal":"","comparative":"","sadhana":""}
        }
        out = os.path.join(args.output_dir, f"auto_{n:03d}.yml")
        with open(out, "w", encoding="utf-8") as f:
            yaml.safe_dump(yaml_obj, f, allow_unicode=True, sort_keys=False)
        n += 1
    print(f"Wrote {n-1} YAML stubs to {args.output_dir}")

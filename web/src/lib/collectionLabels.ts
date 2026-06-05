const ZHUANGZI_ALIASES = new Set([
  "the book of chuang tzu",
  "the_book_of_chuang_tzu",
  "chuang tzu",
  "chuang_tzu",
  "zhuangzi",
]);

export function displayCollectionName(name?: string): string {
  const raw = (name || "").trim();
  if (!raw) return "";
  const normalized = raw.toLowerCase().replace(/\s+/g, " ");
  if (ZHUANGZI_ALIASES.has(normalized)) return "Zhuangzi";
  return raw;
}

const ZHUANGZI_ALIASES = new Set([
  "the book of chuang tzu",
  "the_book_of_chuang_tzu",
  "chuang tzu",
  "chuang_tzu",
  "zhuangzi",
]);

const SENEGALESE_ANIMISM_ALIASES = new Set([
  "senegalese animism",
  "senegalese_animism",
  "serer cosaan",
  "serer_cosaan",
  "serer religion",
  "serer_religion",
]);

export function displayCollectionName(name?: string): string {
  const raw = (name || "").trim();
  if (!raw) return "";
  const normalized = raw.toLowerCase().replace(/\s+/g, " ");
  if (ZHUANGZI_ALIASES.has(normalized)) return "Zhuangzi";
  if (SENEGALESE_ANIMISM_ALIASES.has(normalized) || normalized.replace(/_/g, " ") === "senegalese animism") {
    return "Senegalese Animism";
  }
  return raw;
}

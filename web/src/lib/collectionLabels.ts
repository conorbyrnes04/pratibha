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

const PULAAR_TRADITION_ALIASES = new Set([
  "pulaar tradition",
  "pulaar_tradition",
  "pulaar pre islam",
  "pulaar_pre_islam",
  "fulbe tradition",
  "fulbe_tradition",
  "peul tradition",
  "peul_tradition",
]);

const PULAAR_TEXTS_ALIASES = new Set([
  "pulaar texts",
  "pulaar_texts",
  "pulaar text",
  "pulaar_text",
  "gaden poular",
  "gaden_poular",
]);

export function displayCollectionName(name?: string): string {
  const raw = (name || "").trim();
  if (!raw) return "";
  const normalized = raw.toLowerCase().replace(/\s+/g, " ");
  if (ZHUANGZI_ALIASES.has(normalized)) return "Zhuangzi";
  if (SENEGALESE_ANIMISM_ALIASES.has(normalized) || normalized.replace(/_/g, " ") === "senegalese animism") {
    return "Senegalese Animism";
  }
  if (PULAAR_TRADITION_ALIASES.has(normalized) || normalized.replace(/_/g, " ") === "pulaar tradition") {
    return "Pulaar Tradition";
  }
  if (PULAAR_TEXTS_ALIASES.has(normalized) || normalized.replace(/_/g, " ") === "pulaar texts") {
    return "Pulaar Texts";
  }
  return raw;
}

/** Plain-language replacements for Tao Te Ching §N chapter markers. */

const TTC_CHAPTER_GLOSS: Record<number, string> = {
  1: "chapter 1 (the Way that cannot be fully named)",
  2: "chapter 2 (beauty and ugliness arising together)",
  8: "chapter 8 (the highest good is like water)",
  11: "chapter 11 (the empty hub at the center of the wheel)",
  16: "chapter 16 (all things arise and return to the root)",
  25: "chapter 25 (something formless before heaven and earth)",
  33: "chapter 33 (knowing others and knowing yourself)",
  37: "chapter 37 (non-action, nothing left undone)",
  40: "chapter 40 (the Way moves by reversal)",
  43: "chapter 43 (the soft enters where nothing can)",
  48: "chapter 48 (the Way subtracts; learning adds)",
  57: "chapter 57 (govern by not governing)",
  63: "chapter 63 (do the great while it is still small)",
  67: "chapter 67 (the three treasures)",
  76: "chapter 76 (living is soft, death is hard)",
  78: "chapter 78 (water overcomes hardness; true words seem backward)",
  81: "chapter 81 (the book's closing paradox)",
};

function chapterPhrase(chapter: number): string {
  return TTC_CHAPTER_GLOSS[chapter] || `chapter ${chapter}`;
}

export function humanizeTtcRefs(text?: string): string {
  const value = (text || "").trim();
  if (!value || !value.includes("§")) return value;
  const withPossessive = value.replace(/§(\d+)'s/g, (_, num) => {
    const n = Number(num);
    const gloss = TTC_CHAPTER_GLOSS[n] || `chapter ${n}`;
    return gloss.startsWith(`chapter ${n} (`) ? `chapter ${n}'s` : `${gloss}'s`;
  });
  const cleaned = withPossessive.replace(/§(\d+)/g, (_, num) => chapterPhrase(Number(num)));
  return cleaned.replace(/chapter (\d+) \([^)]+\)'s/g, "chapter $1's");
}

export function isTaoTeChing(item: { collection?: string; _id?: string; work_id?: string }): boolean {
  const blob = [item.collection, item._id, item.work_id].filter(Boolean).join(" ").toLowerCase();
  return blob.includes("tao te ching") || blob.includes("tao_te_ching");
}

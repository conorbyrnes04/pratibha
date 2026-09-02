import type { VerseItem } from "@/lib/types";

/** Devanagari block — strongest signal that a passage has Sanskrit source text. */
export function containsDevanagari(text?: string): boolean {
  return /[\u0900-\u097F]/.test(text || "");
}

/** Tibetan block (U+0F00-0FFF) - Milarepa / Tilopa Uchen originals. */
export function containsTibetan(text?: string): boolean {
  return /[ༀ-࿿]/.test(text || "");
}

/** CJK Unified Ideographs — Zhuangzi, Tao Te Ching, and other Chinese originals. */
export function containsCjk(text?: string): boolean {
  return /[\u4E00-\u9FFF]/.test(text || "");
}

/** Arabic block (U+0600-06FF) — Sufi / Ibn ʿArabī originals. */
export function containsArabic(text?: string): boolean {
  return /[؀-ۿ]/.test(text || "");
}

/** Greek block (U+0370-03FF) — Heraclitus, Plato, Plotinus originals. */
export function containsGreek(text?: string): boolean {
  return /[Ͱ-Ͽἀ-῿]/.test(text || "");
}

/**
 * Best-effort BCP-47 language tag for an "Original" layer, derived from its
 * script, so screen readers, hyphenation, and font selection treat it as
 * non-English. Returns undefined for undetected (e.g. romanized) text rather
 * than guessing a language and mislabeling it.
 */
export function scriptLang(text?: string): string | undefined {
  if (containsTibetan(text)) return "bo";
  if (containsCjk(text)) return "zh";
  if (containsDevanagari(text)) return "sa";
  if (containsArabic(text)) return "ar";
  if (containsGreek(text)) return "grc";
  return undefined;
}

/** True when the original layer is too long to dump without an expand control. */
export function isLongNativeScript(text?: string): boolean {
  const body = (text || "").trim();
  if (!body) return false;
  if (containsCjk(body)) return body.length > 72;
  if (containsDevanagari(body) || containsTibetan(body)) return body.length > 90;
  return body.length > 220;
}

const NON_SANSKRIT_COLLECTION =
  /heraclitus|fragment|epictetus|enchiridion|meditations|phaedo|plato|plotinus|ennead|eckhart|ibn.?arabi|know.?yourself|balyani|rumi|mathnawi|tao|te.?ching|zhuang|chuang|lao.?tzu|confucius|analect|zhongyong|milarepa|jetsun|tibet|dogen|dōgen|shobogenzo|shōbōgenzō|yoruba|òwe|johnson|eastman|zitkala|dakota|soul of the indian|old indian legends|senegal|serer|pulaar|gaden|fulbe|fulɓe|peul|lasnet/i;

const SANSKRIT_COLLECTION =
  /upanishad|upaniṣad|chandogya|isavasya|svetasvatara|mandukya|bhagavad.?gita|astavakra|ashtavakra|aṣṭāvakra|patanjali|patañjali|yoga.?s[uū]tra|vijnana|bhairava|shiva|siva|tantra|spanda|yogin[iī]|pratyabhij|kashmir|nagarjuna|madhyamaka|mmk|shantideva|śāntideva|bodhicary|heart.?s[uū]tra|prajnaparamita|tilopa|maha.?mudra/i;

export function isSanskritCollection(name?: string): boolean {
  const raw = (name || "").trim();
  if (!raw) return false;
  if (NON_SANSKRIT_COLLECTION.test(raw)) return false;
  return SANSKRIT_COLLECTION.test(raw);
}

/** True when the passage should expose an IAST transliteration layer. */
export function passageUsesIast(item: VerseItem): boolean {
  if (isSanskritCollection(item.collection)) return true;
  const original =
    (item.sanskrit || "").trim() ||
    (item.pratibha_layers || []).find((layer) => layer.kind === "original")?.body ||
    "";
  return containsDevanagari(original);
}

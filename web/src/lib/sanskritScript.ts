import type { VerseItem } from "@/lib/types";

/** Devanagari block — strongest signal that a passage has Sanskrit source text. */
export function containsDevanagari(text?: string): boolean {
  return /[\u0900-\u097F]/.test(text || "");
}

const NON_SANSKRIT_COLLECTION =
  /heraclitus|fragment|epictetus|enchiridion|meditations|phaedo|plato|plotinus|ennead|eckhart|ibn.?arabi|know.?yourself|balyani|rumi|mathnawi|tao|te.?ching|zhuang|chuang|lao.?tzu|confucius|analect|zhongyong|milarepa|jetsun|tibet|dogen|dōgen|shobogenzo|shōbōgenzō/i;

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

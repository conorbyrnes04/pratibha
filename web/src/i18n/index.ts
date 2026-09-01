export {
  DEFAULT_LOCALE,
  LOCALES,
  LOCALE_META,
  LOCALE_STORAGE_KEY,
  applyDocumentLocale,
  detectBrowserLocale,
  isLocale,
  localeMeta,
  matchLocale,
  type Locale,
  type LocaleMeta,
} from "./locales";
export { catalogs, en, type Messages } from "./messages";
export { interpolate, translate, type TranslateVars } from "./translate";

const LAYER_KIND_KEYS: Record<string, string> = {
  translation: "layers.translation",
  original: "layers.original",
  commentary: "layers.commentary",
  iast: "layers.iast",
  practice: "layers.practice",
  key_terms: "layers.keyTerms",
  resonances: "layers.resonances",
  appendix: "layers.appendix",
};

export function layerKindKey(kind: string | undefined): string | null {
  if (!kind) return null;
  return LAYER_KIND_KEYS[kind] ?? null;
}

const SHARE_INK_KEYS: Record<string, string> = {
  ash: "share.inkAsh",
  bone: "share.inkBone",
  gold: "share.inkGold",
  copper: "share.inkCopper",
  moonlight: "share.inkMoonlight",
};

const SHARE_GROUP_KEYS: Record<string, string> = {
  animals: "share.groupAnimals",
  plants: "share.groupPlants",
  objects: "share.groupObjects",
  elements: "share.groupElements",
  cosmos: "share.groupCosmos",
  figures: "share.groupFigures",
  deities: "share.groupDeities",
};

export function shareInkKey(ink: string): string {
  return SHARE_INK_KEYS[ink] ?? ink;
}

export function shareGroupKey(id: string): string {
  return SHARE_GROUP_KEYS[id] ?? id;
}

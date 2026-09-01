export const LOCALES = ["en", "fr", "es", "pt-BR", "zh", "ru", "ja", "ar"] as const;

export type Locale = (typeof LOCALES)[number];

export const DEFAULT_LOCALE: Locale = "en";

export const LOCALE_STORAGE_KEY = "pratibha.locale.v1";

export type LocaleMeta = {
  id: Locale;
  /** BCP 47 tag for <html lang> and Intl APIs. */
  bcp47: string;
  dir: "ltr" | "rtl";
  nativeName: string;
};

export const LOCALE_META: Record<Locale, LocaleMeta> = {
  en: { id: "en", bcp47: "en", dir: "ltr", nativeName: "English" },
  fr: { id: "fr", bcp47: "fr", dir: "ltr", nativeName: "Français" },
  es: { id: "es", bcp47: "es", dir: "ltr", nativeName: "Español" },
  "pt-BR": { id: "pt-BR", bcp47: "pt-BR", dir: "ltr", nativeName: "Português (Brasil)" },
  zh: { id: "zh", bcp47: "zh-Hans", dir: "ltr", nativeName: "中文" },
  ru: { id: "ru", bcp47: "ru", dir: "ltr", nativeName: "Русский" },
  ja: { id: "ja", bcp47: "ja", dir: "ltr", nativeName: "日本語" },
  ar: { id: "ar", bcp47: "ar", dir: "rtl", nativeName: "العربية" },
};

const BROWSER_ALIASES: Record<string, Locale> = {
  en: "en",
  fr: "fr",
  es: "es",
  pt: "pt-BR",
  "pt-br": "pt-BR",
  zh: "zh",
  "zh-cn": "zh",
  "zh-hans": "zh",
  "zh-tw": "zh",
  "zh-hant": "zh",
  ru: "ru",
  ja: "ja",
  ar: "ar",
};

export function isLocale(value: unknown): value is Locale {
  return typeof value === "string" && (LOCALES as readonly string[]).includes(value);
}

export function localeMeta(locale: Locale): LocaleMeta {
  return LOCALE_META[locale];
}

/** Map a browser/BCP 47 tag (e.g. pt-BR, zh-CN) onto a supported locale. */
export function matchLocale(tag: string | null | undefined): Locale | null {
  if (!tag) return null;
  const normalized = tag.trim().replace("_", "-");
  if (isLocale(normalized)) return normalized;
  const lower = normalized.toLowerCase();
  if (BROWSER_ALIASES[lower]) return BROWSER_ALIASES[lower];
  const base = lower.split("-")[0];
  return BROWSER_ALIASES[base] ?? null;
}

export function detectBrowserLocale(): Locale {
  if (typeof navigator === "undefined") return DEFAULT_LOCALE;
  const candidates = [navigator.language, ...(navigator.languages ?? [])];
  for (const tag of candidates) {
    const matched = matchLocale(tag);
    if (matched) return matched;
  }
  return DEFAULT_LOCALE;
}

export function applyDocumentLocale(locale: Locale) {
  if (typeof document === "undefined") return;
  const meta = localeMeta(locale);
  document.documentElement.lang = meta.bcp47;
  document.documentElement.dir = meta.dir;
}

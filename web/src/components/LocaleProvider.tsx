"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { useMutation, useQuery } from "convex/react";
import { api } from "../../convex/_generated/api";
import { useAuth } from "@/components/AuthProvider";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import {
  DEFAULT_LOCALE,
  LOCALES,
  LOCALE_STORAGE_KEY,
  applyDocumentLocale,
  catalogs,
  detectBrowserLocale,
  en,
  isLocale,
  localeMeta,
  translate,
  type Locale,
  type TranslateVars,
} from "@/i18n";

const FONT_HREF: Partial<Record<Locale, string>> = {
  zh: "https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@400;600;700&display=swap",
  ja: "https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&family=Noto+Serif+JP:wght@400;600;700&display=swap",
};

function loadStoredLocale(): Locale | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(LOCALE_STORAGE_KEY);
    return isLocale(raw) ? raw : null;
  } catch {
    return null;
  }
}

function persistLocale(locale: Locale) {
  try {
    localStorage.setItem(LOCALE_STORAGE_KEY, locale);
  } catch {
    /* private mode */
  }
}

function ensureLocaleFont(locale: Locale) {
  if (typeof document === "undefined") return;
  const href = FONT_HREF[locale];
  if (!href) return;
  const id = `pratibha-locale-font-${locale}`;
  if (document.getElementById(id)) return;
  const link = document.createElement("link");
  link.id = id;
  link.rel = "stylesheet";
  link.href = href;
  document.head.appendChild(link);
}

type LocaleContextValue = {
  locale: Locale;
  setLocale: (next: Locale) => void;
  t: (key: string, vars?: TranslateVars) => string;
  dir: "ltr" | "rtl";
  bcp47: string;
};

const LocaleContext = createContext<LocaleContextValue | null>(null);

function useLocaleState(cloudLocale: string | undefined, persistCloud: (locale: Locale) => void) {
  const [locale, setLocaleState] = useState<Locale>(DEFAULT_LOCALE);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    const stored = loadStoredLocale();
    const initial = stored ?? detectBrowserLocale();
    setLocaleState(initial);
    applyDocumentLocale(initial);
    ensureLocaleFont(initial);
    setHydrated(true);
  }, []);

  useEffect(() => {
    if (!hydrated || !cloudLocale || !isLocale(cloudLocale)) return;
    if (loadStoredLocale()) return;
    setLocaleState(cloudLocale);
    persistLocale(cloudLocale);
    applyDocumentLocale(cloudLocale);
    ensureLocaleFont(cloudLocale);
  }, [cloudLocale, hydrated]);

  const setLocale = useCallback(
    (next: Locale) => {
      setLocaleState(next);
      persistLocale(next);
      applyDocumentLocale(next);
      ensureLocaleFont(next);
      persistCloud(next);
    },
    [persistCloud],
  );

  const t = useCallback(
    (key: string, vars?: TranslateVars) => translate(catalogs[locale], en, key, vars),
    [locale],
  );

  const meta = localeMeta(locale);

  return useMemo<LocaleContextValue>(
    () => ({
      locale,
      setLocale,
      t,
      dir: meta.dir,
      bcp47: meta.bcp47,
    }),
    [locale, setLocale, t, meta.dir, meta.bcp47],
  );
}

function LocalLocaleProvider({ children }: { children: ReactNode }) {
  const value = useLocaleState(undefined, () => undefined);
  return <LocaleContext.Provider value={value}>{children}</LocaleContext.Provider>;
}

function ConvexLocaleProvider({ children }: { children: ReactNode }) {
  const { user } = useAuth();
  const profile = useQuery(api.profiles.getMine, user ? {} : "skip");
  const setCloudLocale = useMutation(api.profiles.setLocale);

  const persistCloud = useCallback(
    (locale: Locale) => {
      if (!user) return;
      void setCloudLocale({ locale }).catch(() => {
        /* local choice still stands */
      });
    },
    [user, setCloudLocale],
  );

  const value = useLocaleState(profile?.locale, persistCloud);
  return <LocaleContext.Provider value={value}>{children}</LocaleContext.Provider>;
}

export function LocaleProvider({ children }: { children: ReactNode }) {
  if (!CONVEX_ENABLED) {
    return <LocalLocaleProvider>{children}</LocalLocaleProvider>;
  }
  return <ConvexLocaleProvider>{children}</ConvexLocaleProvider>;
}

export function useLocale(): LocaleContextValue {
  const ctx = useContext(LocaleContext);
  if (!ctx) {
    throw new Error("useLocale must be used within LocaleProvider");
  }
  return ctx;
}

export function useT() {
  return useLocale().t;
}

export { LOCALES };

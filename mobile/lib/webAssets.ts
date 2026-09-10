import Constants from "expo-constants";

const PRODUCTION_WEB_BASE = "https://pratibha.agniagama.com";

/** Base URL of the web frontend that serves generated collection art. */
export function getWebBase(): string {
  const extra = Constants.expoConfig?.extra as { webBase?: string } | undefined;
  return extra?.webBase || process.env.EXPO_PUBLIC_WEB_BASE || PRODUCTION_WEB_BASE;
}

/**
 * Resolve a web-relative asset path (e.g. "/generated/redbook/patanjali.jpg")
 * to an absolute URL on the web host. Absolute URLs are returned unchanged.
 */
export function webAsset(path: string): string {
  if (/^https?:\/\//i.test(path)) return path;
  const base = getWebBase().replace(/\/+$/, "");
  return `${base}${path.startsWith("/") ? "" : "/"}${path}`;
}

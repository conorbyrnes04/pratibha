import { createBrowserClient } from "@supabase/ssr";
import type { SupabaseClient } from "@supabase/supabase-js";

const url = (process.env.NEXT_PUBLIC_SUPABASE_URL || "").trim();
const anonKey = (process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "").trim();

export function isSupabaseConfigured(): boolean {
  return Boolean(url && anonKey);
}

export function supabaseProjectUrl(): string {
  return url;
}

export function supabaseStorageKey(): string {
  try {
    const ref = new URL(url).hostname.split(".")[0] || "pratibha";
    return `sb-${ref}-auth-token`;
  } catch {
    return "sb-pratibha-auth-token";
  }
}

export function supabaseCodeVerifierKey(): string {
  return `${supabaseStorageKey()}-code-verifier`;
}

let browserClient: SupabaseClient | null = null;

/**
 * Browser client via @supabase/ssr so PKCE verifiers live in first-party
 * cookies (readable by the /auth/callback route handler).
 */
export function getSupabase(): SupabaseClient | null {
  if (!isSupabaseConfigured()) return null;
  if (typeof window === "undefined") return null;
  if (!browserClient) {
    browserClient = createBrowserClient(url, anonKey, {
      cookieOptions: {
        path: "/",
        sameSite: "lax",
      },
    });
  }
  return browserClient;
}

/** Mirror the PKCE verifier into localStorage as a client-exchange fallback. */
export function mirrorCodeVerifierToLocalStorage(): void {
  if (typeof document === "undefined") return;
  const key = supabaseCodeVerifierKey();
  const parts = document.cookie.split("; ");
  for (const part of parts) {
    const eq = part.indexOf("=");
    if (eq === -1) continue;
    const name = part.slice(0, eq);
    // Cookie may be chunked (key / key.0 / …) or exact.
    if (name !== key && !name.startsWith(`${key}.`)) continue;
    try {
      localStorage.setItem(name, decodeURIComponent(part.slice(eq + 1)));
    } catch {
      /* private mode */
    }
  }
}

/** True once a PKCE verifier cookie is present. */
export async function waitForCodeVerifier(timeoutMs = 2000): Promise<boolean> {
  const key = supabaseCodeVerifierKey();
  const started = Date.now();
  while (Date.now() - started < timeoutMs) {
    if (typeof document !== "undefined" && document.cookie.includes(key)) {
      mirrorCodeVerifierToLocalStorage();
      return true;
    }
    await new Promise((r) => setTimeout(r, 40));
  }
  const ok = typeof document !== "undefined" && document.cookie.includes(key);
  if (ok) mirrorCodeVerifierToLocalStorage();
  return ok;
}

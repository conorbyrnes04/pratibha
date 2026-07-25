import { NextResponse } from "next/server";
import { createServerClient } from "@supabase/ssr";

/**
 * OAuth return path. Exchanges ?code= for a session using cookies that
 * createBrowserClient / dual-storage set before the Google redirect.
 *
 * Prefer this over a client page so the verifier is read from the Cookie
 * header on the same request that completes the handshake.
 */
export async function GET(request: Request) {
  const { searchParams, origin } = new URL(request.url);
  const code = searchParams.get("code");
  const oauthError = searchParams.get("error_description") || searchParams.get("error");
  let next = searchParams.get("next") ?? "/";
  if (!next.startsWith("/")) next = "/";

  if (oauthError) {
    return NextResponse.redirect(
      `${origin}/login?error=${encodeURIComponent(oauthError)}`,
    );
  }

  if (!code) {
    return NextResponse.redirect(`${origin}/login?error=${encodeURIComponent("Missing OAuth code")}`);
  }

  const url = (process.env.NEXT_PUBLIC_SUPABASE_URL || "").trim();
  const anonKey = (process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "").trim();
  if (!url || !anonKey) {
    return NextResponse.redirect(`${origin}/login?error=${encodeURIComponent("Supabase is not configured")}`);
  }

  // Forward Set-Cookie from the exchange onto the redirect response.
  const redirectUrl = `${origin}${next}`;
  const response = NextResponse.redirect(redirectUrl);

  const supabase = createServerClient(url, anonKey, {
    cookies: {
      getAll() {
        const header = request.headers.get("cookie") ?? "";
        if (!header) return [];
        return header.split(";").map((part) => {
          const eq = part.indexOf("=");
          const name = (eq === -1 ? part : part.slice(0, eq)).trim();
          const raw = eq === -1 ? "" : part.slice(eq + 1).trim();
          let value = raw;
          try {
            value = decodeURIComponent(raw);
          } catch {
            value = raw;
          }
          return { name, value };
        }).filter((c) => c.name);
      },
      setAll(cookiesToSet: { name: string; value: string; options?: Record<string, unknown> }[]) {
        cookiesToSet.forEach(({ name, value, options }) => {
          response.cookies.set(name, value, options);
        });
      },
    },
  });

  const { error } = await supabase.auth.exchangeCodeForSession(code);
  if (error) {
    // Fall back to client exchange (dual localStorage) if cookie path failed.
    const fallback = new URL(`${origin}/auth/continue`);
    fallback.searchParams.set("code", code);
    fallback.searchParams.set("next", next);
    fallback.searchParams.set("reason", error.message);
    return NextResponse.redirect(fallback.toString());
  }

  return response;
}

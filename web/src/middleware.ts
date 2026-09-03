import { convexAuthNextjsMiddleware, createRouteMatcher } from "@convex-dev/auth/nextjs/server";
import { NextResponse, type NextRequest } from "next/server";
import type { NextFetchEvent } from "next/server";

const CONVEX_URL = (process.env.NEXT_PUBLIC_CONVEX_URL || "").trim();
/** Keep auth cookies on devices that have already signed in (session cookies vanish on app close). */
const AUTH_COOKIE_MAX_AGE_SECONDS = 60 * 60 * 24 * 30;
const AUTH_MIN_MS = 1000;
const AUTH_WINDOW_MS = 15 * 60 * 1000;
const AUTH_MAX_ATTEMPTS = 8;

// Authenticated surfaces stay gated. Everything else — including unknown
// URLs — is public so crawlers and mistyped links get a real 404 instead of
// a sign-in wall. User data (journal, account, manuscript) and metered chat
// remain private.
const isPrivatePage = createRouteMatcher([
  "/journal",
  "/journal/(.*)",
  "/chat",
  "/chat/(.*)",
  "/manuscript",
  "/manuscript/(.*)",
  "/account",
  "/account/(.*)",
]);

const convexMiddleware = convexAuthNextjsMiddleware(
  async (request, ctx) => {
    if (!ctx.convexAuth) return;
    const authenticated = await ctx.convexAuth.isAuthenticated();
    if (isPrivatePage(request) && !authenticated) {
      return new Response(null, {
        status: 307,
        headers: {
          Location: new URL("/login", request.url).toString(),
        },
      });
    }
  },
  { cookieConfig: { maxAge: AUTH_COOKIE_MAX_AGE_SECONDS } },
);

const authHits = new Map<string, number[]>();

function clientIp(request: NextRequest): string {
  return (
    request.headers.get("cf-connecting-ip") ||
    request.headers.get("x-forwarded-for")?.split(",")[0]?.trim() ||
    "unknown"
  );
}

function authRateLimited(ip: string): boolean {
  const now = Date.now();
  const window = (authHits.get(ip) || []).filter((t) => now - t < AUTH_WINDOW_MS);
  if (window.length >= AUTH_MAX_ATTEMPTS) {
    authHits.set(ip, window);
    return true;
  }
  window.push(now);
  authHits.set(ip, window);
  if (authHits.size > 4096) {
    for (const [key, hits] of authHits) {
      if (!hits.some((t) => now - t < AUTH_WINDOW_MS)) authHits.delete(key);
    }
  }
  return false;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function padAuthTiming(started: number): Promise<void> {
  const wait = AUTH_MIN_MS - (Date.now() - started);
  if (wait > 0) await sleep(wait);
}

function applySecurityHeaders(response: Response): Response {
  response.headers.set("X-Content-Type-Options", "nosniff");
  response.headers.set("X-Frame-Options", "DENY");
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  response.headers.set(
    "Permissions-Policy",
    "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
  );
  response.headers.set("Strict-Transport-Security", "max-age=31536000; includeSubDomains; preload");
  response.headers.delete("x-powered-by");
  response.headers.delete("X-Powered-By");
  return response;
}

async function runInner(request: NextRequest, event: NextFetchEvent): Promise<Response> {
  if (!CONVEX_URL) return NextResponse.next();
  const result = (await convexMiddleware(request, event)) as Response | null | undefined;
  return result ?? NextResponse.next();
}

/**
 * Convex Auth routes sign-in, token refresh, and OAuth callbacks all through the
 * same `POST /api/auth` (action `"auth:signIn"`). Only a genuine credential
 * submission should count against the brute-force limiter — token refresh
 * (`args.refreshToken`) and OAuth code exchange (`args.params.code`) must pass
 * freely, otherwise normal session upkeep trips the limiter, refresh fails, and
 * every authenticated query fails with a stale token.
 */
async function isCredentialSignIn(request: NextRequest): Promise<boolean> {
  try {
    const { action, args } = (await request.clone().json()) as {
      action?: string;
      args?: { refreshToken?: unknown; params?: { code?: unknown; password?: unknown } };
    };
    return (
      action === "auth:signIn" &&
      args?.refreshToken === undefined &&
      args?.params?.code === undefined &&
      args?.params?.password !== undefined
    );
  } catch {
    // Non-JSON or unreadable body — fail open so we never throttle refresh.
    return false;
  }
}

export default async function middleware(request: NextRequest, event: NextFetchEvent) {
  const isAuthPost = request.nextUrl.pathname.startsWith("/api/auth") && request.method === "POST";
  const started = Date.now();
  const credentialAttempt = isAuthPost ? await isCredentialSignIn(request) : false;

  if (credentialAttempt && authRateLimited(clientIp(request))) {
    await padAuthTiming(started);
    return applySecurityHeaders(
      new Response(JSON.stringify({ error: "Too many sign-in attempts. Try again in a few minutes." }), {
        status: 429,
        headers: {
          "Content-Type": "application/json",
          "Retry-After": "900",
        },
      }),
    );
  }

  const response = await runInner(request, event);
  // Constant-time padding only matters for credential checks; padding refresh
  // just adds latency and encourages overlapping refreshes.
  if (credentialAttempt) await padAuthTiming(started);
  return applySecurityHeaders(response);
}

export const config = {
  matcher: [
    // Never run auth middleware on SEO/metadata files — a crawler must reach the
    // real sitemap/robots, not a 307 to /login.
    "/((?!_next/static|_next/image|favicon.ico|sitemap\\.xml|robots\\.txt|.*\\.(?:svg|png|jpg|jpeg|gif|webp|ico)$).*)",
  ],
};

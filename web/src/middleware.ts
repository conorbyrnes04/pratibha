import { convexAuthNextjsMiddleware, createRouteMatcher } from "@convex-dev/auth/nextjs/server";
import { NextResponse } from "next/server";

const CONVEX_URL = (process.env.NEXT_PUBLIC_CONVEX_URL || "").trim();
/** Keep auth cookies on devices that have already signed in (session cookies vanish on app close). */
const AUTH_COOKIE_MAX_AGE_SECONDS = 60 * 60 * 24 * 30;
const isPublicPage = createRouteMatcher([
  "/",
  "/login",
  "/learn",
  "/learn/(.*)",
  "/read",
  "/read/(.*)",
  "/s/(.*)",
  "/m/(.*)",
  "/privacy",
]);

const convexMiddleware = convexAuthNextjsMiddleware(
  async (request, ctx) => {
    if (!ctx.convexAuth) return;
    const authenticated = await ctx.convexAuth.isAuthenticated();
    if (!isPublicPage(request) && !authenticated) {
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

export default CONVEX_URL
  ? convexMiddleware
  : function middleware() {
      return NextResponse.next();
    };

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp|ico)$).*)",
  ],
};

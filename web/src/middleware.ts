import { convexAuthNextjsMiddleware, createRouteMatcher } from "@convex-dev/auth/nextjs/server";
import { NextResponse } from "next/server";

const CONVEX_URL = (process.env.NEXT_PUBLIC_CONVEX_URL || "").trim();
const isPublicPage = createRouteMatcher(["/", "/login", "/learn", "/read"]);

const convexMiddleware = convexAuthNextjsMiddleware((request) => {
  if (!request.convexAuth) return;
  if (!isPublicPage(request) && !request.convexAuth.isAuthenticated()) {
    return new Response(null, {
      status: 307,
      headers: {
        Location: new URL("/login", request.url).toString(),
      },
    });
  }
});

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

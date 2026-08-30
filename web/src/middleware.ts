import { convexAuthNextjsMiddleware, createRouteMatcher } from "@convex-dev/auth/nextjs/server";

const isPublicPage = createRouteMatcher(["/", "/login"]);

export default convexAuthNextjsMiddleware((request) => {
  if (!isPublicPage(request) && !request.convexAuth.isAuthenticated()) {
    return new Response(null, {
      status: 307,
      headers: {
        Location: new URL("/login", request.url).toString(),
      },
    });
  }
});

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp|ico)$).*)",
  ],
};

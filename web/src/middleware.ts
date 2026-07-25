import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";

const PUBLIC_EXACT = new Set(["/", "/login"]);
const PUBLIC_PREFIXES = ["/auth/callback", "/auth/continue"];

function isPublicPath(pathname: string): boolean {
  if (PUBLIC_EXACT.has(pathname)) return true;
  return PUBLIC_PREFIXES.some((p) => pathname === p || pathname.startsWith(`${p}/`));
}

/**
 * Edge gate: send signed-out visitors to /login for protected routes.
 * Complements the client AuthGate so deep links don't flash private UI.
 */
export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const publicPath = isPublicPath(pathname);

  const url = (process.env.NEXT_PUBLIC_SUPABASE_URL || "").trim();
  const anonKey = (process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "").trim();
  if (!url || !anonKey) {
    return NextResponse.next();
  }

  let response = NextResponse.next({ request });

  const supabase = createServerClient(url, anonKey, {
    cookies: {
      getAll() {
        return request.cookies.getAll();
      },
      setAll(cookiesToSet: { name: string; value: string; options?: Record<string, unknown> }[]) {
        cookiesToSet.forEach(({ name, value }) => {
          request.cookies.set(name, value);
        });
        response = NextResponse.next({ request });
        cookiesToSet.forEach(({ name, value, options }) => {
          response.cookies.set(name, value, options);
        });
      },
    },
  });

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user && !publicPath) {
    const login = request.nextUrl.clone();
    login.pathname = "/login";
    login.search = "";
    const next = `${pathname}${request.nextUrl.search}`;
    login.searchParams.set("next", next || "/");
    return NextResponse.redirect(login);
  }

  if (user && pathname === "/login") {
    const next = request.nextUrl.searchParams.get("next") || "/";
    const dest = request.nextUrl.clone();
    dest.pathname = next.startsWith("/") ? next : "/";
    dest.search = "";
    return NextResponse.redirect(dest);
  }

  return response;
}

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp|ico)$).*)",
  ],
};

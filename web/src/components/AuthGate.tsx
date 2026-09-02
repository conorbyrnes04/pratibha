"use client";

import { usePathname, useRouter } from "next/navigation";
import { useEffect } from "react";
import { useAuth } from "@/components/AuthProvider";
import { useT } from "@/components/LocaleProvider";

/** Routes reachable without an account when auth is configured. */
const PUBLIC_PREFIXES = ["/", "/login", "/learn", "/read", "/circle", "/m", "/s"];

function isPublicPath(pathname: string): boolean {
  if (pathname === "/") return true;
  return PUBLIC_PREFIXES.some((p) => p !== "/" && (pathname === p || pathname.startsWith(`${p}/`)));
}

/**
 * When Convex auth is configured, send signed-out visitors to /login
 * for everything except the home page and auth routes.
 */
export function AuthGate({ children }: { children: React.ReactNode }) {
  const { configured, loading, user } = useAuth();
  const t = useT();
  const pathname = usePathname();
  const router = useRouter();
  const publicPath = isPublicPath(pathname);
  const mustSignIn = configured && !loading && !user && !publicPath;

  useEffect(() => {
    if (!mustSignIn) return;
    const next = `${pathname}${typeof window !== "undefined" ? window.location.search : ""}`;
    router.replace(`/login?next=${encodeURIComponent(next || "/")}`);
  }, [mustSignIn, pathname, router]);

  if (!configured) return <>{children}</>;

  if (mustSignIn) {
    return (
      <main className="mx-auto max-w-lg px-4 py-20">
        <p className="soft font-sans text-sm uppercase tracking-[0.18em]">{t("auth.redirecting")}</p>
      </main>
    );
  }

  return <>{children}</>;
}

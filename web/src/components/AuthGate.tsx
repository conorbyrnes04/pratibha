"use client";

import { usePathname, useRouter } from "next/navigation";
import { useEffect } from "react";
import { useAuth } from "@/components/AuthProvider";

/** Routes reachable without an account when auth is configured. */
const PUBLIC_PREFIXES = ["/", "/login"];

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

  if (loading && !publicPath) {
    return (
      <main className="mx-auto max-w-lg px-4 py-20">
        <p className="soft font-sans text-sm uppercase tracking-[0.18em]">Checking session…</p>
      </main>
    );
  }

  if (mustSignIn) {
    return (
      <main className="mx-auto max-w-lg px-4 py-20">
        <p className="soft font-sans text-sm uppercase tracking-[0.18em]">Redirecting to sign in…</p>
      </main>
    );
  }

  return <>{children}</>;
}

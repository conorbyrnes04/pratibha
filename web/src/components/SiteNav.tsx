'use client';

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { useAuth } from "@/components/AuthProvider";

const LINKS: Array<{ href: string; label: string; match?: string }> = [
  { href: "/read", label: "Library" },
  { href: "/learn", label: "Paths", match: "/learn" },
  { href: "/learn#threads", label: "Threads", match: "/learn#threads" },
  { href: "/chat", label: "Study Chat" },
  { href: "/random", label: "Oracle" },
  { href: "/journal", label: "Journal" },
  { href: "/sources", label: "Sources" },
];

export function SiteNav() {
  const pathname = usePathname();
  const { configured, loading, user } = useAuth();
  const [open, setOpen] = useState(false);

  useEffect(() => {
    setOpen(false);
  }, [pathname]);

  // Hide library nav until signed in (when auth is on).
  if (configured && (loading || !user)) {
    return null;
  }

  function isActive(href: string, match?: string): boolean {
    if (match === "/learn#threads") return false;
    const path = match || href;
    return pathname === path || pathname.startsWith(`${path}/`);
  }

  return (
    <>
      <div className="hidden items-center gap-5 text-base sm:flex">
        {LINKS.map((link) => (
          <Link
            key={link.href}
            href={link.href}
            aria-current={isActive(link.href, link.match) ? "page" : undefined}
            className={`nav-link ${isActive(link.href, link.match) ? "text-amber-100" : ""}`}
          >
            {link.label}
          </Link>
        ))}
      </div>

      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        aria-controls="mobile-nav"
        aria-label={open ? "Close menu" : "Open menu"}
        className="nav-link inline-flex h-10 w-10 items-center justify-center rounded-lg border border-amber-200/20 sm:hidden"
      >
        <span aria-hidden="true" className="text-lg">{open ? "✕" : "☰"}</span>
      </button>

      {open ? (
        <div
          id="mobile-nav"
          className="absolute left-0 right-0 top-full border-b border-amber-200/15 bg-[#090912]/95 backdrop-blur-xl sm:hidden"
        >
          <div className="mx-auto flex max-w-6xl flex-col px-4 py-2">
            {LINKS.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                aria-current={isActive(link.href, link.match) ? "page" : undefined}
                className={`nav-link rounded-lg px-2 py-3 text-base ${isActive(link.href, link.match) ? "text-amber-100" : ""}`}
              >
                {link.label}
              </Link>
            ))}
          </div>
        </div>
      ) : null}
    </>
  );
}

'use client';

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

const LINKS: Array<{ href: string; label: string }> = [
  { href: "/read", label: "Read" },
  { href: "/daily", label: "Daily" },
  { href: "/random", label: "Random" },
  { href: "/chat", label: "Study Chat" },
  { href: "/learn", label: "Paths" },
  { href: "/journal", label: "Journal" },
];

export function SiteNav() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  // Close the mobile menu whenever the route changes.
  useEffect(() => {
    setOpen(false);
  }, [pathname]);

  function isActive(href: string): boolean {
    return pathname === href || pathname.startsWith(`${href}/`);
  }

  return (
    <>
      <div className="hidden items-center gap-5 text-sm sm:flex">
        {LINKS.map((link) => (
          <Link
            key={link.href}
            href={link.href}
            aria-current={isActive(link.href) ? "page" : undefined}
            className={`nav-link ${isActive(link.href) ? "text-amber-100" : ""}`}
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
                aria-current={isActive(link.href) ? "page" : undefined}
                className={`nav-link rounded-lg px-2 py-3 text-base ${isActive(link.href) ? "text-amber-100" : ""}`}
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

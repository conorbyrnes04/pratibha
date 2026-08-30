"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { useAuth } from "@/components/AuthProvider";
import { Button } from "@/components/ui/button";

type NavLink = { href: string; label: string; match?: string };

const PRIMARY: NavLink[] = [
  { href: "/", label: "Today", match: "/" },
  { href: "/read", label: "Library" },
  { href: "/glossary/study", label: "Lexicon", match: "/glossary/study" },
  { href: "/chat", label: "Chat" },
  { href: "/journal", label: "Journal" },
];

const SECONDARY: NavLink[] = [
  { href: "/learn", label: "Paths", match: "/learn" },
  { href: "/learn#threads", label: "Themes", match: "/learn#threads" },
  { href: "/random", label: "Oracle" },
  { href: "/glossary", label: "Glossary", match: "/glossary" },
  { href: "/sources", label: "Sources" },
];

function linkIsActive(pathname: string, href: string, match?: string, hash = ""): boolean {
  if (match === "/learn#threads") {
    return pathname === "/learn" && hash === "#threads";
  }
  if (match === "/") return pathname === "/";
  if (match === "/glossary") return pathname === "/glossary";
  if (match === "/learn") {
    return pathname === "/learn" && hash !== "#threads";
  }
  const path = match || href;
  return pathname === path || pathname.startsWith(`${path}/`);
}

export function SiteNav() {
  const pathname = usePathname();
  const { configured, loading, user } = useAuth();
  const [open, setOpen] = useState(false);
  const [moreOpen, setMoreOpen] = useState(false);
  const [hash, setHash] = useState("");
  const moreRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setOpen(false);
    setMoreOpen(false);
    setHash(typeof window !== "undefined" ? window.location.hash : "");
  }, [pathname]);

  useEffect(() => {
    function onHash() {
      setHash(window.location.hash);
    }
    window.addEventListener("hashchange", onHash);
    onHash();
    return () => window.removeEventListener("hashchange", onHash);
  }, []);

  useEffect(() => {
    if (!moreOpen) return;
    function onPointerDown(event: MouseEvent) {
      if (moreRef.current && !moreRef.current.contains(event.target as Node)) {
        setMoreOpen(false);
      }
    }
    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") setMoreOpen(false);
    }
    document.addEventListener("mousedown", onPointerDown);
    document.addEventListener("keydown", onKeyDown);
    return () => {
      document.removeEventListener("mousedown", onPointerDown);
      document.removeEventListener("keydown", onKeyDown);
    };
  }, [moreOpen]);

  // Hide library nav until signed in (when auth is on).
  if (configured && (loading || !user)) {
    return null;
  }

  const secondaryActive = SECONDARY.some((link) =>
    linkIsActive(pathname, link.href, link.match, hash),
  );

  return (
    <>
      <div className="hidden items-center gap-5 text-base sm:flex">
        {PRIMARY.map((link) => {
          const active = linkIsActive(pathname, link.href, link.match);
          return (
            <Link
              key={link.href}
              href={link.href}
              aria-current={active ? "page" : undefined}
              className={`nav-link ${active ? "text-amber-100" : ""}`}
            >
              {link.label}
            </Link>
          );
        })}
        <div className="nav-more" ref={moreRef}>
          <button
            type="button"
            onClick={() => setMoreOpen((v) => !v)}
            aria-expanded={moreOpen}
            aria-controls="nav-more-menu"
            className={`nav-link nav-more__trigger ${secondaryActive || moreOpen ? "text-amber-100" : ""}`}
          >
            More
            <span aria-hidden="true" className="nav-more__caret">
              {moreOpen ? "▴" : "▾"}
            </span>
          </button>
          {moreOpen ? (
            <div id="nav-more-menu" className="nav-more__menu" role="menu">
              {SECONDARY.map((link) => {
                const active = linkIsActive(pathname, link.href, link.match, hash);
                return (
                  <Link
                    key={link.href}
                    href={link.href}
                    role="menuitem"
                    aria-current={active ? "page" : undefined}
                    className={`nav-more__item ${active ? "text-amber-100" : ""}`}
                    onClick={() => setMoreOpen(false)}
                  >
                    {link.label}
                  </Link>
                );
              })}
            </div>
          ) : null}
        </div>
      </div>

      <Button
        type="button"
        variant="ghost"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        aria-controls="mobile-nav"
        aria-label={open ? "Close menu" : "Open menu"}
        className="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-amber-200/20 sm:hidden"
      >
        <span aria-hidden="true" className="text-lg">
          {open ? "✕" : "☰"}
        </span>
      </Button>

      {open ? (
        <div
          id="mobile-nav"
          className="absolute left-0 right-0 top-full border-b border-amber-200/15 bg-[#090912]/95 backdrop-blur-xl sm:hidden"
        >
          <div className="mx-auto flex max-w-6xl flex-col px-4 py-2">
            {PRIMARY.map((link) => {
              const active = linkIsActive(pathname, link.href, link.match);
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  aria-current={active ? "page" : undefined}
                  className={`nav-link rounded-lg px-2 py-3 text-base ${active ? "text-amber-100" : ""}`}
                >
                  {link.label}
                </Link>
              );
            })}
            <details className="nav-more-mobile">
              <summary className="nav-link nav-more-mobile__summary rounded-lg px-2 py-3 text-base">
                More
              </summary>
              <div className="flex flex-col border-l border-amber-200/15 pl-3">
                {SECONDARY.map((link) => {
                  const active = linkIsActive(pathname, link.href, link.match, hash);
                  return (
                    <Link
                      key={link.href}
                      href={link.href}
                      aria-current={active ? "page" : undefined}
                      className={`nav-link rounded-lg px-2 py-2.5 text-base ${active ? "text-amber-100" : ""}`}
                    >
                      {link.label}
                    </Link>
                  );
                })}
              </div>
            </details>
          </div>
        </div>
      ) : null}
    </>
  );
}

"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef, useState } from "react";

type NavLink = { href: string; label: string; match?: string };

/** The walk — always visible. */
const WALK: NavLink[] = [
  { href: "/", label: "Today", match: "/" },
  { href: "/learn?path=essential", label: "Path", match: "/learn" },
  { href: "/read", label: "Library" },
];

/** Tools around the walk. */
const STUDY: NavLink[] = [
  { href: "/journal", label: "Journal" },
  { href: "/chat", label: "Chat" },
  { href: "/glossary/study", label: "Lexicon", match: "/glossary/study" },
  { href: "/glossary", label: "Glossary", match: "/glossary" },
  { href: "/manuscript", label: "Manuscript" },
  { href: "/random", label: "Oracle" },
  { href: "/sources", label: "Sources" },
];

function linkIsActive(pathname: string, href: string, match?: string): boolean {
  if (match === "/") return pathname === "/";
  if (match === "/glossary") return pathname === "/glossary";
  const path = match || href.split("?")[0];
  return pathname === path || pathname.startsWith(`${path}/`);
}

function WalkLinks({
  className,
  onNavigate,
}: {
  className?: string;
  onNavigate?: () => void;
}) {
  const pathname = usePathname();
  return (
    <>
      {WALK.map((link) => {
        const active = linkIsActive(pathname, link.href, link.match);
        return (
          <Link
            key={link.href}
            href={link.href}
            aria-current={active ? "page" : undefined}
            className={`${className ?? "nav-link"} ${active ? "nav-link--current" : ""}`}
            onClick={onNavigate}
          >
            {link.label}
          </Link>
        );
      })}
    </>
  );
}

function StudyMenu({
  open,
  onToggle,
  onClose,
  placement,
}: {
  open: boolean;
  onToggle: () => void;
  onClose: () => void;
  placement: "bar" | "dock";
}) {
  const pathname = usePathname();
  const rootRef = useRef<HTMLDivElement>(null);
  const studyActive = STUDY.some((link) => linkIsActive(pathname, link.href, link.match));

  useEffect(() => {
    if (!open) return;
    function onPointerDown(event: MouseEvent) {
      if (rootRef.current && !rootRef.current.contains(event.target as Node)) onClose();
    }
    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") onClose();
    }
    document.addEventListener("mousedown", onPointerDown);
    document.addEventListener("keydown", onKeyDown);
    return () => {
      document.removeEventListener("mousedown", onPointerDown);
      document.removeEventListener("keydown", onKeyDown);
    };
  }, [open, onClose]);

  return (
    <div className={`nav-more ${placement === "dock" ? "nav-more--dock" : ""}`} ref={rootRef}>
      <button
        type="button"
        onClick={onToggle}
        aria-expanded={open}
        aria-controls={`nav-study-${placement}`}
        className={`nav-link nav-more__trigger ${studyActive || open ? "nav-link--current" : ""}`}
      >
        Study
        <span aria-hidden="true" className="nav-more__caret">
          {open ? (placement === "dock" ? "▾" : "▴") : placement === "dock" ? "▴" : "▾"}
        </span>
      </button>
      {open ? (
        <div id={`nav-study-${placement}`} className="nav-more__menu" role="menu">
          {STUDY.map((link) => {
            const active = linkIsActive(pathname, link.href, link.match);
            return (
              <Link
                key={link.href}
                href={link.href}
                role="menuitem"
                aria-current={active ? "page" : undefined}
                className={`nav-more__item ${active ? "nav-link--current" : ""}`}
                onClick={onClose}
              >
                {link.label}
              </Link>
            );
          })}
        </div>
      ) : null}
    </div>
  );
}

export function SiteNav() {
  const [studyOpen, setStudyOpen] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    setStudyOpen(false);
  }, [pathname]);

  return (
    <>
      <div className="site-nav site-nav--bar">
        <WalkLinks />
        <StudyMenu
          placement="bar"
          open={studyOpen}
          onToggle={() => setStudyOpen((value) => !value)}
          onClose={() => setStudyOpen(false)}
        />
      </div>

      <nav className="site-dock" aria-label="Primary">
        <WalkLinks className="site-dock__link" />
        <StudyMenu
          placement="dock"
          open={studyOpen}
          onToggle={() => setStudyOpen((value) => !value)}
          onClose={() => setStudyOpen(false)}
        />
      </nav>
    </>
  );
}

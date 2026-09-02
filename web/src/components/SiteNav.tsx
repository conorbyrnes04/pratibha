"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { CircleMenuFeed } from "@/components/CircleMenuFeed";
import { useT } from "@/components/LocaleProvider";

type NavLink = { href: string; labelKey: string; match?: string };

/** The walk — always visible. */
const WALK: NavLink[] = [
  { href: "/", labelKey: "nav.today", match: "/" },
  { href: "/learn?path=essential", labelKey: "nav.path", match: "/learn" },
  { href: "/read", labelKey: "nav.library" },
  { href: "/circle", labelKey: "nav.circle" },
  { href: "/manuscript", labelKey: "nav.manuscript" },
];

/** Tools around the walk. */
const STUDY: NavLink[] = [
  { href: "/journal", labelKey: "nav.journal" },
  { href: "/chat", labelKey: "nav.chat" },
  { href: "/glossary/study", labelKey: "nav.lexicon", match: "/glossary/study" },
  { href: "/glossary", labelKey: "nav.glossary", match: "/glossary" },
  { href: "/random", labelKey: "nav.oracle" },
  { href: "/sources", labelKey: "nav.sources" },
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
  const t = useT();
  return (
    <>
      {WALK.map((link) => {
        const active = linkIsActive(pathname, link.href, link.match);
        return (
          <Link
            key={link.href}
            href={link.href}
            aria-current={active ? "page" : undefined}
            className={`nav-link ${className ?? ""} ${active ? "nav-link--current" : ""}`}
            onClick={onNavigate}
          >
            {t(link.labelKey)}
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
  const t = useT();
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
    const timer = window.setTimeout(() => {
      document.addEventListener("pointerdown", onPointerDown);
      document.addEventListener("keydown", onKeyDown);
    }, 0);
    return () => {
      window.clearTimeout(timer);
      document.removeEventListener("pointerdown", onPointerDown);
      document.removeEventListener("keydown", onKeyDown);
    };
  }, [open, onClose]);

  return (
    <div className={`nav-more ${placement === "dock" ? "nav-more--dock" : ""}`} ref={rootRef}>
      <button
        type="button"
        onClick={(event) => {
          event.stopPropagation();
          onToggle();
        }}
        aria-expanded={open}
        aria-controls={`nav-study-${placement}`}
        className={`nav-link nav-more__trigger ${studyActive || open ? "nav-link--current" : ""}`}
      >
        {t("nav.study")}
        <span aria-hidden="true" className="nav-more__caret">
          {open ? (placement === "dock" ? "▾" : "▴") : placement === "dock" ? "▴" : "▾"}
        </span>
      </button>
      {open ? (
        <div id={`nav-study-${placement}`} className="nav-more__menu nav-more__menu--study" role="menu">
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
                {t(link.labelKey)}
              </Link>
            );
          })}
          <CircleMenuFeed active={open} />
        </div>
      ) : null}
    </div>
  );
}

function useStudyMenu() {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    setOpen(false);
  }, [pathname]);

  return {
    open,
    onToggle: () => setOpen((value) => !value),
    onClose: () => setOpen(false),
  };
}

export function SiteNav() {
  const study = useStudyMenu();
  return (
    <div className="site-nav site-nav--bar">
      <WalkLinks />
      <StudyMenu placement="bar" {...study} />
    </div>
  );
}

export function SiteDock() {
  const study = useStudyMenu();
  const t = useT();
  return (
    <nav className="site-dock" aria-label={t("nav.primary")}>
      <WalkLinks className="site-dock__link" />
      <StudyMenu placement="dock" {...study} />
    </nav>
  );
}

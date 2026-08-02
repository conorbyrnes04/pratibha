"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { useAuth } from "@/components/AuthProvider";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";

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
  { href: "/learn#threads", label: "Threads", match: "/learn#threads" },
  { href: "/random", label: "Oracle" },
  { href: "/glossary", label: "Glossary", match: "/glossary" },
  { href: "/sources", label: "Sources" },
];

function linkIsActive(pathname: string, href: string, match?: string): boolean {
  if (match === "/learn#threads") return false;
  if (match === "/") return pathname === "/";
  if (match === "/glossary") return pathname === "/glossary";
  const path = match || href;
  return pathname === path || pathname.startsWith(`${path}/`);
}

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

  const secondaryActive = SECONDARY.some((link) =>
    linkIsActive(pathname, link.href, link.match),
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
        <DropdownMenu>
          <DropdownMenuTrigger
            className={`nav-link nav-more__trigger inline-flex items-center gap-1 ${secondaryActive ? "text-amber-100" : ""}`}
          >
            More
            <span aria-hidden="true" className="nav-more__caret">
              ▾
            </span>
          </DropdownMenuTrigger>
          <DropdownMenuContent
            align="end"
            className="min-w-[10rem] rounded-xl border border-amber-200/15 bg-[#12101c]/96 p-1 shadow-2xl backdrop-blur-xl"
          >
            {SECONDARY.map((link) => {
              const active = linkIsActive(pathname, link.href, link.match);
              return (
                <DropdownMenuItem
                  key={link.href}
                  className={`cursor-pointer px-3 py-2 font-sans text-sm focus:bg-white/5 focus:text-amber-100 ${active ? "text-amber-100" : ""}`}
                  render={<Link href={link.href} />}
                >
                  {link.label}
                </DropdownMenuItem>
              );
            })}
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      <Sheet open={open} onOpenChange={setOpen}>
        <SheetTrigger
          className="nav-link inline-flex h-10 w-10 items-center justify-center rounded-lg border border-amber-200/20 sm:hidden"
          aria-label="Open menu"
        >
          <span aria-hidden="true" className="text-lg">
            ☰
          </span>
        </SheetTrigger>
        <SheetContent
          side="right"
          className="border-amber-200/15 bg-[#090912]/98 w-[min(100%,20rem)]"
          showCloseButton
        >
          <SheetHeader>
            <SheetTitle className="font-serif text-xl text-amber-100">Pratibha</SheetTitle>
          </SheetHeader>
          <nav className="flex flex-col gap-1 px-2 pb-6">
            {[...PRIMARY, ...SECONDARY].map((link) => {
              const active = linkIsActive(pathname, link.href, link.match);
              return (
                <Button
                  key={link.href}
                  variant="ghost"
                  className={`justify-start rounded-lg px-3 py-3 text-base ${active ? "text-amber-100" : ""}`}
                  render={<Link href={link.href} />}
                  onClick={() => setOpen(false)}
                >
                  {link.label}
                </Button>
              );
            })}
          </nav>
        </SheetContent>
      </Sheet>
    </>
  );
}

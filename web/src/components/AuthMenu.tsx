"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { useAuth } from "@/components/AuthProvider";
import { Button, buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

function initialsFromUser(email: string | undefined, name: string | undefined): string {
  const fromName = (name || "").trim();
  if (fromName) {
    const parts = fromName.split(/\s+/).filter(Boolean);
    if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase();
    return fromName.slice(0, 2).toUpperCase();
  }
  const local = (email || "?").split("@")[0] || "?";
  return local.slice(0, 2).toUpperCase();
}

export function AuthMenu() {
  const router = useRouter();
  const { configured, loading, user, signOut } = useAuth();
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    function onPointerDown(e: MouseEvent) {
      if (!rootRef.current?.contains(e.target as Node)) setOpen(false);
    }
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") setOpen(false);
    }
    document.addEventListener("mousedown", onPointerDown);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onPointerDown);
      document.removeEventListener("keydown", onKey);
    };
  }, [open]);

  if (!configured) {
    return (
      <Link href="/login" className="nav-link hidden sm:inline" title="Configure Convex auth">
        Account
      </Link>
    );
  }

  if (loading) {
    return (
      <span
        className="inline-flex h-9 w-9 animate-pulse rounded-full border border-amber-200/15 bg-white/5"
        aria-hidden
      />
    );
  }

  if (!user) {
    return (
      <Link href="/login" className={cn(buttonVariants({ variant: "secondary", size: "sm" }))}>
        Sign in
      </Link>
    );
  }

  const email = user.email || "";
  const name = user.name || undefined;
  const avatarUrl = null;
  const initials = initialsFromUser(email, name);

  async function onSignOut() {
    setOpen(false);
    await signOut();
    router.replace("/");
  }

  return (
    <div ref={rootRef} className="relative">
      <Button
        type="button"
        variant="ghost"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        aria-haspopup="menu"
        aria-label="Account menu"
        className="h-9 w-9 shrink-0 overflow-hidden rounded-full border border-amber-200/35 bg-gradient-to-br from-amber-200/25 to-stone-900/80 p-0 text-xs font-semibold tracking-wide text-amber-50 shadow-[0_0_0_1px_rgb(0_0_0_/_0.35)] hover:border-amber-200/60 hover:from-amber-200/35"
      >
        {avatarUrl ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={avatarUrl} alt="" className="h-full w-full object-cover" referrerPolicy="no-referrer" />
        ) : (
          <span className="font-sans">{initials}</span>
        )}
      </Button>

      {open ? (
        <div
          role="menu"
          className="absolute right-0 top-[calc(100%+0.55rem)] z-50 min-w-[13.5rem] overflow-hidden rounded-xl border border-amber-200/15 bg-[#12101c]/96 py-1 shadow-2xl backdrop-blur-xl"
        >
          <div className="border-b border-white/10 px-3 py-2.5">
            <p className="truncate font-sans text-sm text-amber-50">{name || email.split("@")[0] || "Account"}</p>
            {email ? <p className="mt-0.5 truncate font-sans text-xs text-stone-400">{email}</p> : null}
          </div>
          <Link
            href="/account"
            role="menuitem"
            onClick={() => setOpen(false)}
            className="block px-3 py-2.5 font-sans text-sm text-stone-200 transition hover:bg-white/5 hover:text-amber-100"
          >
            Account
          </Link>
          <button
            type="button"
            role="menuitem"
            onClick={() => void onSignOut()}
            className="block w-full px-3 py-2.5 text-left font-sans text-sm text-stone-200 transition hover:bg-white/5 hover:text-amber-100"
          >
            Sign out
          </button>
        </div>
      ) : null}
    </div>
  );
}

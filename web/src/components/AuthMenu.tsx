"use client";

import Link from "next/link";
import { useAuth } from "@/components/AuthProvider";

export function AuthMenu() {
  const { configured, loading, user, signOut } = useAuth();

  if (!configured) {
    return (
      <Link href="/login" className="nav-link hidden sm:inline" title="Configure Supabase auth">
        Account
      </Link>
    );
  }

  if (loading) {
    return <span className="hidden font-sans text-xs uppercase tracking-[0.18em] text-stone-500 sm:inline">…</span>;
  }

  if (!user) {
    return (
      <Link href="/login" className="btn-secondary px-3 py-1.5 text-sm">
        Sign in
      </Link>
    );
  }

  const label = user.email?.split("@")[0] || "Account";

  return (
    <div className="flex items-center gap-2">
      <Link
        href="/account"
        className="max-w-[7rem] truncate font-sans text-xs uppercase tracking-[0.14em] text-stone-300 transition hover:text-amber-200 sm:max-w-[9rem]"
        title={user.email || "Account"}
      >
        {label}
      </Link>
      <button type="button" onClick={() => void signOut()} className="nav-link hidden text-sm sm:inline">
        Sign out
      </button>
    </div>
  );
}

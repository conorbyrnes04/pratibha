"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

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

  if (!configured) {
    return (
      <Link href="/login" className="nav-link hidden sm:inline" title="Configure Supabase auth">
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
      <Button variant="secondary" size="sm" render={<Link href="/login" />}>
        Sign in
      </Button>
    );
  }

  const email = user.email || "";
  const name =
    (typeof user.user_metadata?.full_name === "string" && user.user_metadata.full_name) ||
    (typeof user.user_metadata?.name === "string" && user.user_metadata.name) ||
    undefined;
  const avatarUrl =
    (typeof user.user_metadata?.avatar_url === "string" && user.user_metadata.avatar_url) ||
    (typeof user.user_metadata?.picture === "string" && user.user_metadata.picture) ||
    null;
  const initials = initialsFromUser(email, name);

  async function onSignOut() {
    await signOut();
    router.replace("/");
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger
        aria-label="Account menu"
        className="group relative inline-flex h-9 w-9 shrink-0 items-center justify-center overflow-hidden rounded-full border border-amber-200/35 bg-gradient-to-br from-amber-200/25 to-stone-900/80 text-xs font-semibold tracking-wide text-amber-50 shadow-[0_0_0_1px_rgb(0_0_0_/_0.35)] transition hover:border-amber-200/60 hover:from-amber-200/35 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber-200/50"
      >
        {avatarUrl ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={avatarUrl} alt="" className="h-full w-full object-cover" referrerPolicy="no-referrer" />
        ) : (
          <span className="font-sans">{initials}</span>
        )}
      </DropdownMenuTrigger>
      <DropdownMenuContent
        align="end"
        className="min-w-[13.5rem] rounded-xl border border-amber-200/15 bg-[#12101c]/96 p-1 shadow-2xl backdrop-blur-xl"
      >
        <DropdownMenuLabel className="px-3 py-2.5 font-normal">
          <p className="truncate font-sans text-sm text-amber-50">{name || email.split("@")[0] || "Account"}</p>
          {email ? <p className="mt-0.5 truncate font-sans text-xs text-stone-400">{email}</p> : null}
        </DropdownMenuLabel>
        <DropdownMenuSeparator className="bg-white/10" />
        <DropdownMenuItem
          className="cursor-pointer px-3 py-2.5 font-sans text-sm focus:bg-white/5 focus:text-amber-100"
          onClick={() => router.push("/account")}
        >
          Account
        </DropdownMenuItem>
        <DropdownMenuItem
          className="cursor-pointer px-3 py-2.5 font-sans text-sm focus:bg-white/5 focus:text-amber-100"
          onClick={() => void onSignOut()}
        >
          Sign out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

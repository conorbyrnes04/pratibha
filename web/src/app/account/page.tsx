"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { useAuth } from "@/components/AuthProvider";
import { Button, buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export default function AccountPage() {
  const router = useRouter();
  const { configured, loading, user, signOut } = useAuth();

  useEffect(() => {
    if (!loading && configured && !user) {
      router.replace("/login?next=/account");
    }
  }, [loading, configured, user, router]);

  if (!configured) {
    return (
      <main className="mx-auto max-w-lg px-4 py-16">
        <h1 className="text-4xl text-amber-100">Account</h1>
        <p className="soft mt-4 font-sans text-sm">Auth is not configured for this build.</p>
      </main>
    );
  }

  if (loading || !user) {
    return (
      <main className="mx-auto max-w-lg px-4 py-16">
        <p className="soft font-sans text-sm">Loading account…</p>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-lg px-4 py-16">
      <p className="font-sans text-xs uppercase tracking-[0.22em] text-stone-400">Account</p>
      <h1 className="mt-2 text-4xl text-amber-100">Signed in</h1>
      <p className="soft mt-4 font-sans text-sm">{user.email}</p>
      <p className="soft mt-2 font-sans text-sm">
        Journal notes sync to your account when you&apos;re signed in. The library and Study Chat stay
        available without login.
      </p>
      <div className="mt-8 flex flex-wrap gap-3">
        <Link href="/journal" className={cn(buttonVariants())}>
          Open journal
        </Link>
        <Button
          type="button"
          variant="secondary"
          onClick={() => {
            void signOut().then(() => router.push("/"));
          }}
        >
          Sign out
        </Button>
      </div>
    </main>
  );
}

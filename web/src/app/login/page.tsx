"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { FormEvent, Suspense, useEffect, useState } from "react";
import { useAuth } from "@/components/AuthProvider";
import { Button, buttonVariants } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";

function LoginForm() {
  const router = useRouter();
  const params = useSearchParams();
  const next = params.get("next") || "/";
  const oauthCode = params.get("code");
  const { user, loading, configured, signInWithPassword, signUpWithPassword, signInWithGoogle } = useAuth();
  const [mode, setMode] = useState<"signin" | "signup">(
    params.get("mode") === "signup" ? "signup" : "signin",
  );
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(params.get("error"));
  const [info, setInfo] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (!loading && user) router.replace(next);
  }, [loading, user, router, next]);

  useEffect(() => {
    const fromQuery = params.get("error");
    if (fromQuery) setError(fromQuery);
  }, [params]);

  if (oauthCode && (loading || !user)) {
    return (
      <main className="mx-auto max-w-lg px-4 py-16">
        <p className="font-sans text-xs uppercase tracking-[0.22em] text-stone-400">Pratibha</p>
        <h1 className="mt-2 text-4xl text-amber-100">Finishing Google sign-in</h1>
        <p className="soft mt-3 font-sans text-sm">One moment while we open your session.</p>
      </main>
    );
  }

  if (!configured) {
    return (
      <main className="mx-auto max-w-lg px-4 py-16">
        <h1 className="text-4xl text-amber-100">Account</h1>
        <p className="soft mt-4 font-sans text-sm leading-relaxed">
          Convex auth is not configured for this build. Set{" "}
          <code className="text-amber-100">NEXT_PUBLIC_CONVEX_URL</code> in the web env, then redeploy.
        </p>
        <Link href="/" className={cn(buttonVariants({ variant: "secondary" }), "mt-8")}>
          Back home
        </Link>
      </main>
    );
  }

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setInfo(null);
    setBusy(true);
    try {
      if (password.length < 6) {
        setError("Password must be at least 6 characters.");
        return;
      }
      const err =
        mode === "signin"
          ? await signInWithPassword(email, password)
          : await signUpWithPassword(email, password);
      if (err) {
        setError(err);
        return;
      }
      if (mode === "signup") {
        setInfo(
          "Account created. You are now signed in.",
        );
      }
      router.replace(next);
    } finally {
      setBusy(false);
    }
  }

  async function onGoogle() {
    setError(null);
    setBusy(true);
    const origin = window.location.origin;
    const path = next.startsWith("/") && !next.startsWith("//") ? next.split("?")[0] : "/";
    const dest = `${origin}${path === "/" ? "" : path}`;
    const err = await signInWithGoogle(dest);
    if (err) {
      setError(err);
      setBusy(false);
    }
  }

  return (
    <main className="mx-auto max-w-lg px-4 py-16">
      <p className="font-sans text-xs uppercase tracking-[0.22em] text-stone-400">Pratibha</p>
      <h1 className="mt-2 text-4xl text-amber-100">{mode === "signin" ? "Sign in" : "Create account"}</h1>
      <p className="soft mt-3 font-sans text-sm">
        The path is open without an account. Sign in to keep a journal and carry your walk across devices.
      </p>

      <div className="mt-8 space-y-4">
        <Button
          type="button"
          variant="secondary"
          size="lg"
          disabled={busy}
          className="w-full"
          onClick={() => void onGoogle()}
        >
          Continue with Google
        </Button>

        <div className="flex items-center gap-3 text-stone-500">
          <div className="h-px flex-1 bg-amber-200/15" />
          <span className="font-sans text-xs uppercase tracking-[0.18em]">or email</span>
          <div className="h-px flex-1 bg-amber-200/15" />
        </div>

        <form onSubmit={onSubmit} className="space-y-3">
          <div className="space-y-1.5">
            <Label htmlFor="login-email" className="font-sans text-sm text-[var(--muted)]">
              Email
            </Label>
            <Input
              id="login-email"
              type="email"
              required
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="login-password" className="font-sans text-sm text-[var(--muted)]">
              Password
            </Label>
            <Input
              id="login-password"
              type="password"
              required
              minLength={6}
              autoComplete={mode === "signin" ? "current-password" : "new-password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          {error ? <p className="font-sans text-sm text-amber-200/90">{error}</p> : null}
          {info ? <p className="font-sans text-sm text-stone-300">{info}</p> : null}
          <Button type="submit" disabled={busy} size="lg" className="w-full">
            {busy ? "Working…" : mode === "signin" ? "Sign in" : "Create account"}
          </Button>
        </form>

        <p className="font-sans text-sm soft">
          {mode === "signin" ? (
            <>
              No account yet?{" "}
              <button
                type="button"
                className="text-amber-100 underline-offset-2 hover:underline"
                onClick={() => setMode("signup")}
              >
                Create one
              </button>
            </>
          ) : (
            <>
              Already have an account?{" "}
              <button
                type="button"
                className="text-amber-100 underline-offset-2 hover:underline"
                onClick={() => setMode("signin")}
              >
                Sign in
              </button>
            </>
          )}
        </p>
      </div>
    </main>
  );
}

export default function LoginPage() {
  return (
    <Suspense fallback={<main className="mx-auto max-w-lg px-4 py-16 soft font-sans text-sm">Loading…</main>}>
      <LoginForm />
    </Suspense>
  );
}

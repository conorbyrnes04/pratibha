"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { FormEvent, Suspense, useEffect, useState } from "react";
import { useAuth } from "@/components/AuthProvider";
import { Button, buttonVariants } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useT } from "@/components/LocaleProvider";
import { MIN_PASSWORD_LENGTH } from "@/lib/authRules";
import { cn } from "@/lib/utils";

function LoginForm() {
  const t = useT();
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
        <h1 className="mt-2 text-4xl text-amber-100">{t("auth.finishingGoogle")}</h1>
        <p className="soft mt-3 font-sans text-sm">{t("auth.finishingGoogleLede")}</p>
      </main>
    );
  }

  if (!configured) {
    return (
      <main className="mx-auto max-w-lg px-4 py-16">
        <h1 className="text-4xl text-amber-100">{t("auth.account")}</h1>
        <p className="soft mt-4 font-sans text-sm leading-relaxed">{t("auth.convexUnconfigured")}</p>
        <Link href="/" className={cn(buttonVariants({ variant: "secondary" }), "mt-8")}>
          {t("auth.backHome")}
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
      if (password.length < MIN_PASSWORD_LENGTH) {
        setError(t("auth.passwordMin", { n: MIN_PASSWORD_LENGTH }));
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
        setInfo(t("auth.accountCreated"));
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
      <h1 className="mt-2 text-4xl text-amber-100">{mode === "signin" ? t("auth.signIn") : t("auth.createAccount")}</h1>
      <p className="soft mt-3 font-sans text-sm">{t("auth.loginLede")}</p>

      <div className="mt-8 space-y-4">
        <Button
          type="button"
          variant="secondary"
          size="lg"
          disabled={busy}
          className="w-full"
          onClick={() => void onGoogle()}
        >
          {t("auth.continueGoogle")}
        </Button>

        <div className="flex items-center gap-3 text-stone-500">
          <div className="h-px flex-1 bg-amber-200/15" />
          <span className="font-sans text-xs uppercase tracking-[0.18em]">{t("auth.orEmail")}</span>
          <div className="h-px flex-1 bg-amber-200/15" />
        </div>

        <form onSubmit={onSubmit} className="space-y-3">
          <div className="space-y-1.5">
            <Label htmlFor="login-email" className="font-sans text-sm text-[var(--muted)]">
              {t("auth.email")}
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
              {t("auth.password")}
            </Label>
            <Input
              id="login-password"
              type="password"
              required
              minLength={MIN_PASSWORD_LENGTH}
              autoComplete={mode === "signin" ? "current-password" : "new-password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          {error ? <p className="font-sans text-sm text-amber-200/90">{error}</p> : null}
          {info ? <p className="font-sans text-sm text-stone-300">{info}</p> : null}
          <Button type="submit" disabled={busy} size="lg" className="w-full">
            {busy ? t("auth.working") : mode === "signin" ? t("auth.signIn") : t("auth.createAccount")}
          </Button>
        </form>

        <p className="font-sans text-sm soft">
          {mode === "signin" ? (
            <>
              {t("auth.noAccountYet")}{" "}
              <button
                type="button"
                className="text-amber-100 underline-offset-2 hover:underline"
                onClick={() => setMode("signup")}
              >
                {t("auth.createOne")}
              </button>
            </>
          ) : (
            <>
              {t("auth.alreadyHaveAccount")}{" "}
              <button
                type="button"
                className="text-amber-100 underline-offset-2 hover:underline"
                onClick={() => setMode("signin")}
              >
                {t("auth.signIn")}
              </button>
            </>
          )}
        </p>
      </div>
    </main>
  );
}

function LoginFallback() {
  const t = useT();
  return <main className="mx-auto max-w-lg px-4 py-16 soft font-sans text-sm">{t("common.loading")}</main>;
}

export default function LoginPage() {
  return (
    <Suspense fallback={<LoginFallback />}>
      <LoginForm />
    </Suspense>
  );
}

"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useEffect, useState } from "react";
import { getSupabase } from "@/lib/supabaseClient";

/**
 * Client-side PKCE fallback when the server route could not read the
 * verifier cookie (still present in localStorage via dual storage).
 */
function ContinueInner() {
  const router = useRouter();
  const params = useSearchParams();
  const [message, setMessage] = useState("Finishing sign-in…");
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    const code = params.get("code");
    const next = params.get("next") || "/";
    const supabase = getSupabase();
    if (!supabase) {
      setMessage("Supabase is not configured.");
      setFailed(true);
      return;
    }
    if (!code) {
      setMessage(params.get("reason") || "Missing OAuth code.");
      setFailed(true);
      return;
    }

    let active = true;
    (async () => {
      const { error } = await supabase.auth.exchangeCodeForSession(code);
      if (!active) return;
      if (error) {
        setMessage(error.message);
        setFailed(true);
        return;
      }
      router.replace(next.startsWith("/") ? next : "/");
    })();

    return () => {
      active = false;
    };
  }, [params, router]);

  return (
    <main className="mx-auto max-w-lg px-4 py-16">
      <h1 className="text-3xl text-amber-100">Signing you in</h1>
      <p className="soft mt-3 font-sans text-sm">{message}</p>
      {failed ? (
        <div className="mt-6 flex flex-wrap gap-3">
          <Link href="/login" className="btn-secondary inline-flex px-4 py-2 text-sm">
            Back to sign in
          </Link>
          <Link href="/" className="btn-secondary inline-flex px-4 py-2 text-sm">
            Home
          </Link>
        </div>
      ) : null}
    </main>
  );
}

export default function AuthContinuePage() {
  return (
    <Suspense fallback={<main className="mx-auto max-w-lg px-4 py-16 soft font-sans text-sm">Signing you in…</main>}>
      <ContinueInner />
    </Suspense>
  );
}

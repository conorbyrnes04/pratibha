"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { getSupabase } from "@/lib/supabaseClient";

/**
 * OAuth / magic-link return path. Supabase writes the session from the URL hash
 * or PKCE code; we then send the user into the app.
 */
export default function AuthCallbackPage() {
  const router = useRouter();
  const [message, setMessage] = useState("Completing sign-in…");

  useEffect(() => {
    const supabase = getSupabase();
    if (!supabase) {
      setMessage("Supabase is not configured.");
      return;
    }
    let active = true;
    (async () => {
      // Exchange ?code=… when present (PKCE).
      const url = new URL(window.location.href);
      const code = url.searchParams.get("code");
      if (code) {
        const { error } = await supabase.auth.exchangeCodeForSession(code);
        if (!active) return;
        if (error) {
          setMessage(error.message);
          return;
        }
      } else {
        const { data, error } = await supabase.auth.getSession();
        if (!active) return;
        if (error) {
          setMessage(error.message);
          return;
        }
        if (!data.session) {
          setMessage("No session found. Try signing in again.");
          return;
        }
      }
      router.replace("/journal");
    })();
    return () => {
      active = false;
    };
  }, [router]);

  return (
    <main className="mx-auto max-w-lg px-4 py-16">
      <h1 className="text-3xl text-amber-100">Signing you in</h1>
      <p className="soft mt-3 font-sans text-sm">{message}</p>
    </main>
  );
}

"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import type { Session, User } from "@supabase/supabase-js";
import {
  getSupabase,
  isSupabaseConfigured,
  mirrorCodeVerifierToLocalStorage,
  waitForCodeVerifier,
} from "@/lib/supabaseClient";

type AuthContextValue = {
  configured: boolean;
  loading: boolean;
  session: Session | null;
  user: User | null;
  accessToken: string | null;
  signInWithPassword: (email: string, password: string) => Promise<string | null>;
  signUpWithPassword: (email: string, password: string) => Promise<string | null>;
  signInWithGoogle: () => Promise<string | null>;
  signOut: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const configured = isSupabaseConfigured();
  const [loading, setLoading] = useState(configured);
  const [session, setSession] = useState<Session | null>(null);

  useEffect(() => {
    if (!configured) {
      setLoading(false);
      return;
    }
    const supabase = getSupabase();
    if (!supabase) {
      setLoading(false);
      return;
    }
    let active = true;
    supabase.auth.getSession().then(({ data }) => {
      if (!active) return;
      setSession(data.session ?? null);
      setLoading(false);
    });
    const { data: sub } = supabase.auth.onAuthStateChange((_event, next) => {
      setSession(next);
      setLoading(false);
    });
    return () => {
      active = false;
      sub.subscription.unsubscribe();
    };
  }, [configured]);

  const signInWithPassword = useCallback(async (email: string, password: string) => {
    const supabase = getSupabase();
    if (!supabase) return "Supabase is not configured.";
    const { error } = await supabase.auth.signInWithPassword({ email: email.trim(), password });
    return error?.message ?? null;
  }, []);

  const signUpWithPassword = useCallback(async (email: string, password: string) => {
    const supabase = getSupabase();
    if (!supabase) return "Supabase is not configured.";
    const { error } = await supabase.auth.signUp({ email: email.trim(), password });
    return error?.message ?? null;
  }, []);

  const signInWithGoogle = useCallback(async () => {
    const supabase = getSupabase();
    if (!supabase) return "Supabase is not configured.";
    const redirectTo = `${window.location.origin}/auth/callback`;
    // skipBrowserRedirect so we can confirm the PKCE verifier is persisted
    // before leaving the page (avoids the empty-verifier race on OAuth return).
    const { data, error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo,
        skipBrowserRedirect: true,
        queryParams: { prompt: "select_account" },
      },
    });
    if (error) return error.message;
    if (!data.url) return "No OAuth URL returned from Supabase.";
    const ready = await waitForCodeVerifier();
    if (!ready) {
      return "Could not prepare sign-in (PKCE verifier missing). Try again, or use email sign-in.";
    }
    mirrorCodeVerifierToLocalStorage();
    window.location.assign(data.url);
    return null;
  }, []);

  const signOut = useCallback(async () => {
    const supabase = getSupabase();
    if (!supabase) return;
    await supabase.auth.signOut();
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      configured,
      loading,
      session,
      user: session?.user ?? null,
      accessToken: session?.access_token ?? null,
      signInWithPassword,
      signUpWithPassword,
      signInWithGoogle,
      signOut,
    }),
    [configured, loading, session, signInWithPassword, signUpWithPassword, signInWithGoogle, signOut],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return ctx;
}

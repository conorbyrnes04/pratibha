"use client";

import { useAuthActions } from "@convex-dev/auth/react";
import { useQuery } from "convex/react";
import { createContext, useCallback, useContext, useMemo, ReactNode } from "react";
import { api } from "../../convex/_generated/api";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";

type AuthContextValue = {
  configured: boolean;
  loading: boolean;
  user: { id: string; email?: string; name?: string } | null;
  signInWithPassword: (email: string, password: string) => Promise<string | null>;
  signUpWithPassword: (email: string, password: string) => Promise<string | null>;
  signInWithGoogle: () => Promise<string | null>;
  signOut: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | null>(null);

const unavailable = "Convex auth is not configured. Set NEXT_PUBLIC_CONVEX_URL.";

function LocalAuthProvider({ children }: { children: ReactNode }) {
  const value = useMemo<AuthContextValue>(
    () => ({
      configured: false,
      loading: false,
      user: null,
      signInWithPassword: async () => unavailable,
      signUpWithPassword: async () => unavailable,
      signInWithGoogle: async () => unavailable,
      signOut: async () => undefined,
    }),
    [],
  );
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

function ConvexAuthProvider({ children }: { children: ReactNode }) {
  const { signIn, signOut: convexSignOut } = useAuthActions();
  const viewer = useQuery(api.auth.currentUser);
  const loading = viewer === undefined;
  const user = viewer
    ? {
        id: viewer._id,
        email: viewer.email,
        name: viewer.name,
      }
    : null;

  const signInWithPassword = useCallback(
    async (email: string, password: string) => {
      try {
        await signIn("password", { email: email.trim(), password, flow: "signIn" });
        return null;
      } catch (error) {
        return error instanceof Error ? error.message : "Sign in failed";
      }
    },
    [signIn],
  );

  const signUpWithPassword = useCallback(
    async (email: string, password: string) => {
      try {
        await signIn("password", { email: email.trim(), password, flow: "signUp" });
        return null;
      } catch (error) {
        return error instanceof Error ? error.message : "Sign up failed";
      }
    },
    [signIn],
  );

  const signInWithGoogle = useCallback(async () => {
    try {
      await signIn("google");
      return null;
    } catch (error) {
      return error instanceof Error ? error.message : "Google sign in failed";
    }
  }, [signIn]);

  const handleSignOut = useCallback(async () => {
    await convexSignOut();
  }, [convexSignOut]);

  const value = useMemo<AuthContextValue>(
    () => ({
      configured: true,
      loading,
      user,
      signInWithPassword,
      signUpWithPassword,
      signInWithGoogle,
      signOut: handleSignOut,
    }),
    [loading, user, signInWithPassword, signUpWithPassword, signInWithGoogle, handleSignOut],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function AuthProvider({ children }: { children: ReactNode }) {
  if (!CONVEX_ENABLED) {
    return <LocalAuthProvider>{children}</LocalAuthProvider>;
  }
  return <ConvexAuthProvider>{children}</ConvexAuthProvider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return ctx;
}

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { setAuthToken, convexFetch } from "../convex/httpClient";
import { storage, TOKEN_KEY, REFRESH_TOKEN_KEY } from "../lib/storage";

interface User {
  _id: string;
  email?: string;
  name?: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

// Convex Auth's `signIn` is an ACTION that returns
// `{ tokens: { token, refreshToken } }` for the password flow (not a mutation
// returning `{ token }`). Subsequent calls authenticate via `Authorization:
// Bearer <token>`.
interface SignInResult {
  tokens?: { token: string; refreshToken: string } | null;
}

function persistTokens(tokens: { token: string; refreshToken: string }) {
  storage.set(TOKEN_KEY, tokens.token);
  storage.set(REFRESH_TOKEN_KEY, tokens.refreshToken);
  setAuthToken(tokens.token);
}

function clearTokens() {
  storage.remove(TOKEN_KEY);
  storage.remove(REFRESH_TOKEN_KEY);
  setAuthToken(null);
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = storage.get(TOKEN_KEY);
    if (token) {
      setAuthToken(token);
      loadUser();
    } else {
      setLoading(false);
    }
  }, []);

  async function loadUser() {
    try {
      const currentUser = (await convexFetch("auth:currentUser", {}, "query")) as User | null;
      if (currentUser) {
        setUser(currentUser);
      } else {
        clearTokens();
      }
    } catch (error) {
      console.error("Failed to load user:", error);
      clearTokens();
    } finally {
      setLoading(false);
    }
  }

  async function authenticate(email: string, password: string, flow: "signIn" | "signUp") {
    const result = (await convexFetch(
      "auth:signIn",
      { provider: "password", params: { email, password, flow } },
      "action",
    )) as SignInResult;

    if (!result.tokens?.token) {
      throw new Error(`No token returned from ${flow === "signUp" ? "sign up" : "sign in"}`);
    }
    persistTokens(result.tokens);
    await loadUser();
  }

  const signIn = async (email: string, password: string) => {
    try {
      await authenticate(email, password, "signIn");
    } catch (error: any) {
      throw new Error(error?.message || "Sign in failed");
    }
  };

  const signUp = async (email: string, password: string) => {
    try {
      await authenticate(email, password, "signUp");
    } catch (error: any) {
      throw new Error(error?.message || "Sign up failed");
    }
  };

  const signOut = async () => {
    try {
      await convexFetch("auth:signOut", {}, "action");
    } catch (error) {
      console.error("Sign out error:", error);
    } finally {
      clearTokens();
      setUser(null);
    }
  };

  const value: AuthContextType = {
    user,
    loading,
    signIn,
    signUp,
    signOut,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}

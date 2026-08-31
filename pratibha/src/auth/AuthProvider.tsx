import { createContext, useContext, useState, useEffect, type ReactNode } from "@lynx-js/react";
import { setAuthToken, convexFetch } from "../convex/httpClient";
import { storage, TOKEN_KEY, REFRESH_TOKEN_KEY } from "../lib/storage";

const VERIFIER_KEY = "convex_oauth_verifier";
const SITE_URL = "http://localhost:3000";

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
  signInWithGoogle: () => Promise<void>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

interface SignInResult {
  tokens?: { token: string; refreshToken: string } | null;
  redirect?: string;
  url?: string;
  verifier?: string;
}

function persistTokens(tokens: { token: string; refreshToken: string }) {
  storage.set(TOKEN_KEY, tokens.token);
  storage.set(REFRESH_TOKEN_KEY, tokens.refreshToken);
  setAuthToken(tokens.token);
}

function clearTokens() {
  storage.remove(TOKEN_KEY);
  storage.remove(REFRESH_TOKEN_KEY);
  storage.remove(VERIFIER_KEY);
  setAuthToken(null);
}

function getCodeFromUrl(): string | null {
  try {
    if (typeof window !== "undefined" && window.location?.search) {
      return new URLSearchParams(window.location.search).get("code");
    }
  } catch {
    /* native Lynx has no window.location */
  }
  return null;
}

function openExternalUrl(url: string) {
  try {
    // @ts-ignore Lynx Explorer
    if (typeof NativeModules !== "undefined" && NativeModules?.ExplorerModule?.openSchema) {
      // @ts-ignore
      NativeModules.ExplorerModule.openSchema(url);
      return;
    }
  } catch {
    /* try next */
  }
  try {
    // @ts-ignore
    if (typeof NativeModules !== "undefined" && NativeModules?.Linking?.openURL) {
      // @ts-ignore
      NativeModules.Linking.openURL(url);
      return;
    }
  } catch {
    /* try next */
  }
  if (typeof window !== "undefined" && window.location) {
    window.location.assign(url);
    return;
  }
  throw new Error("Could not open Google. Reload Lynx Explorer and try again.");
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const code = getCodeFromUrl();
    if (code) {
      void completeOAuth(code);
      return;
    }
    void restoreSession();
  }, []);

  async function refreshSession(): Promise<boolean> {
    const refreshToken = storage.get(REFRESH_TOKEN_KEY);
    if (!refreshToken) return false;
    try {
      setAuthToken(null);
      const result = (await convexFetch(
        "auth:signIn",
        { refreshToken },
        "action",
      )) as SignInResult;
      if (!result.tokens?.token) return false;
      persistTokens(result.tokens);
      return true;
    } catch (error) {
      console.error("Failed to refresh session:", error);
      return false;
    }
  }

  async function restoreSession() {
    const token = storage.get(TOKEN_KEY);
    const refreshToken = storage.get(REFRESH_TOKEN_KEY);
    if (!token && !refreshToken) {
      setLoading(false);
      return;
    }
    if (token) setAuthToken(token);
    const restored = await loadUser(false);
    if (restored) return;
    if (await refreshSession()) {
      await loadUser(true);
      return;
    }
    clearTokens();
    setLoading(false);
  }

  async function loadUser(clearOnFailure = true): Promise<boolean> {
    try {
      const currentUser = (await convexFetch("auth:currentUser", {}, "query")) as User | null;
      if (currentUser) {
        setUser(currentUser);
        setLoading(false);
        return true;
      }
    } catch (error) {
      console.error("Failed to load user:", error);
    }
    if (clearOnFailure) {
      clearTokens();
      setLoading(false);
    }
    return false;
  }

  async function completeOAuth(code: string) {
    try {
      const verifier = storage.get(VERIFIER_KEY) ?? undefined;
      const result = (await convexFetch(
        "auth:signIn",
        { params: { code }, verifier },
        "action",
      )) as SignInResult;
      storage.remove(VERIFIER_KEY);
      if (!result.tokens?.token) {
        throw new Error("Google sign-in did not return a session");
      }
      persistTokens(result.tokens);
      await loadUser();
    } catch (error) {
      console.error("Google callback failed:", error);
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

  const signInWithGoogle = async () => {
    try {
      const result = (await convexFetch(
        "auth:signIn",
        { provider: "google", params: { redirectTo: SITE_URL } },
        "action",
      )) as SignInResult;

      if (result.redirect || result.url) {
        if (result.verifier) {
          storage.set(VERIFIER_KEY, result.verifier);
        }
        openExternalUrl(result.redirect || result.url!);
        return;
      }
      if (result.tokens?.token) {
        persistTokens(result.tokens);
        await loadUser();
        return;
      }
      throw new Error("Google sign-in did not return a redirect. Check Convex Google env vars.");
    } catch (error: any) {
      throw new Error(error?.message || "Google sign-in failed");
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
    signInWithGoogle,
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

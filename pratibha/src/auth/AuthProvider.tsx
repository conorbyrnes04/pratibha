import React, { createContext, useContext, useState, useEffect, ReactNode } from "@lynx-js/react";
import { setAuthToken, convexFetch } from "../convex/httpClient";

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

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing session (guard localStorage access)
    const token = typeof localStorage !== "undefined" ? localStorage.getItem("convex_token") : null;
    if (token) {
      setAuthToken(token);
      loadUser();
    } else {
      setLoading(false);
    }
  }, []);

  async function loadUser() {
    try {
      const currentUser = await convexFetch("auth:currentUser", {}, "query");
      if (currentUser) {
        setUser(currentUser);
      } else {
        if (typeof localStorage !== "undefined") {
          localStorage.removeItem("convex_token");
        }
        setAuthToken(null);
      }
    } catch (error) {
      console.error("Failed to load user:", error);
      if (typeof localStorage !== "undefined") {
        localStorage.removeItem("convex_token");
      }
      setAuthToken(null);
    } finally {
      setLoading(false);
    }
  }

  const signIn = async (email: string, password: string) => {
    try {
      const result = await convexFetch(
        "auth:signIn",
        {
          provider: "password",
          params: { email, password, flow: "signIn" },
        },
        "mutation"
      );

      if (result.token) {
        if (typeof localStorage !== "undefined") {
          localStorage.setItem("convex_token", result.token);
        }
        setAuthToken(result.token);
        await loadUser();
      } else {
        throw new Error("No token returned from sign in");
      }
    } catch (error: any) {
      throw new Error(error.message || "Sign in failed");
    }
  };

  const signUp = async (email: string, password: string) => {
    try {
      const result = await convexFetch(
        "auth:signIn",
        {
          provider: "password",
          params: { email, password, flow: "signUp" },
        },
        "mutation"
      );

      if (result.token) {
        if (typeof localStorage !== "undefined") {
          localStorage.setItem("convex_token", result.token);
        }
        setAuthToken(result.token);
        await loadUser();
      } else {
        throw new Error("No token returned from sign up");
      }
    } catch (error: any) {
      throw new Error(error.message || "Sign up failed");
    }
  };

  const signInWithGoogle = async () => {
    try {
      const result = await convexFetch(
        "auth:signIn",
        {
          provider: "google",
        },
        "mutation"
      );

      // OAuth flow returns a redirect URL
      if (result.redirect || result.url) {
        const redirectUrl = result.redirect || result.url;
        
        // Try to open in system browser
        // On Lynx native, this would use platform-specific APIs
        // For web/development, use window.open or location
        if (typeof window !== "undefined") {
          // Web environment
          window.location.href = redirectUrl;
        } else {
          // Lynx native - would need platform-specific implementation
          // For now, log the URL
          console.log("OAuth redirect URL:", redirectUrl);
          throw new Error("Native browser opening not yet implemented. OAuth URL logged to console.");
        }
      } else if (result.token) {
        // Direct token return (shouldn't happen with OAuth but handle it)
        if (typeof localStorage !== "undefined") {
          localStorage.setItem("convex_token", result.token);
        }
        setAuthToken(result.token);
        await loadUser();
      } else {
        throw new Error("No redirect URL or token returned from Google sign-in");
      }
    } catch (error: any) {
      throw new Error(error.message || "Google sign-in failed");
    }
  };

  const signOut = async () => {
    try {
      await convexFetch("auth:signOut", {}, "mutation");
    } catch (error) {
      console.error("Sign out error:", error);
    } finally {
      if (typeof localStorage !== "undefined") {
        localStorage.removeItem("convex_token");
      }
      setAuthToken(null);
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

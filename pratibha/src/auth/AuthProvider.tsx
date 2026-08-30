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
    'background only';
    
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
        
        // Try to open in system browser - order matters:
        // 1. Lynx Explorer (development/testing)
        // @ts-ignore - NativeModules from Lynx
        if (typeof NativeModules !== "undefined" && NativeModules?.ExplorerModule?.openSchema) {
          // @ts-ignore
          NativeModules.ExplorerModule.openSchema(redirectUrl);
          return;
        }
        
        // 2. Production Lynx native modules (if available)
        // @ts-ignore
        if (typeof NativeModules !== "undefined" && NativeModules?.Linking?.openURL) {
          // @ts-ignore
          NativeModules.Linking.openURL(redirectUrl);
          return;
        }
        
        // 3. Web environment
        if (typeof window !== "undefined") {
          window.location.assign(redirectUrl);
          return;
        }
        
        // No way to open URL
        throw new Error("Google sign-in requires a system browser. Please use Lynx Explorer or a web browser.");
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

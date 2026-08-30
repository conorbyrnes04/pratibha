import React, { createContext, useContext, useEffect, useState, useCallback, ReactNode } from "react";
import * as WebBrowser from "expo-web-browser";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { convex } from "@/lib/convex";
import { useQuery } from "convex/react";

WebBrowser.maybeCompleteAuthSession();

const AUTH_TOKEN_KEY = "pratibha.auth.token";
const AUTH_REFRESH_KEY = "pratibha.auth.refresh";

type User = {
  id: string;
  email?: string;
  name?: string;
} | null;

type AuthContextValue = {
  user: User;
  loading: boolean;
  signInWithGoogle: () => Promise<void>;
  signInWithPassword: (email: string, password: string) => Promise<string | null>;
  signUpWithPassword: (email: string, password: string) => Promise<string | null>;
  signOut: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<User>(null);
  
  // Query current user - using Convex query API directly since we don't have generated types yet
  // In production, you'd import from web/convex/_generated/api after running `convex dev`
  const viewer = useQuery("auth:currentUser" as any);
  
  useEffect(() => {
    // Restore auth token from AsyncStorage
    AsyncStorage.getItem(AUTH_TOKEN_KEY).then(token => {
      if (token) {
        // Set auth with a function that returns the token
        convex.setAuth(async () => token);
      }
      setLoading(false);
    });
  }, []);

  useEffect(() => {
    if (viewer !== undefined) {
      setUser(viewer ? {
        id: viewer._id,
        email: viewer.email,
        name: viewer.name,
      } : null);
    }
  }, [viewer]);

  const signInWithGoogle = useCallback(async () => {
    try {
      const convexSiteUrl = "https://energized-armadillo-158.convex.site";
      const redirectUri = "pratibha://";
      
      // Build the Google OAuth URL through Convex Auth
      const authUrl = `${convexSiteUrl}/api/auth/signin/google?redirect=${encodeURIComponent(redirectUri)}`;
      
      const result = await WebBrowser.openAuthSessionAsync(
        authUrl,
        redirectUri
      );

      if (result.type === "success" && result.url) {
        // Extract token from redirect URL
        const url = new URL(result.url);
        const token = url.searchParams.get("token");
        
        if (token) {
          await AsyncStorage.setItem(AUTH_TOKEN_KEY, token);
          convex.setAuth(async () => token);
        }
      }
    } catch (error) {
      console.error("Google sign in error:", error);
      throw error;
    }
  }, []);

  const signInWithPassword = useCallback(
    async (email: string, password: string): Promise<string | null> => {
      try {
        const convexSiteUrl = "https://energized-armadillo-158.convex.site";
        // Password auth would go through Convex Auth HTTP endpoints
        const response = await fetch(`${convexSiteUrl}/api/auth/signin/password`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: email.trim(), password, flow: "signIn" }),
        });
        
        if (!response.ok) {
          return "Sign in failed";
        }
        
        const data = await response.json();
        if (data.token) {
          await AsyncStorage.setItem(AUTH_TOKEN_KEY, data.token);
          convex.setAuth(async () => data.token);
          return null;
        }
        
        return "Authentication failed";
      } catch (error) {
        return error instanceof Error ? error.message : "Sign in failed";
      }
    },
    []
  );

  const signUpWithPassword = useCallback(
    async (email: string, password: string): Promise<string | null> => {
      try {
        const convexSiteUrl = "https://energized-armadillo-158.convex.site";
        const response = await fetch(`${convexSiteUrl}/api/auth/signin/password`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: email.trim(), password, flow: "signUp" }),
        });
        
        if (!response.ok) {
          return "Sign up failed";
        }
        
        const data = await response.json();
        if (data.token) {
          await AsyncStorage.setItem(AUTH_TOKEN_KEY, data.token);
          convex.setAuth(async () => data.token);
          return null;
        }
        
        return "Registration failed";
      } catch (error) {
        return error instanceof Error ? error.message : "Sign up failed";
      }
    },
    []
  );

  const signOut = useCallback(async () => {
    await AsyncStorage.removeItem(AUTH_TOKEN_KEY);
    await AsyncStorage.removeItem(AUTH_REFRESH_KEY);
    // Clear auth by passing undefined
    convex.setAuth(undefined as any);
    setUser(null);
  }, []);

  const value: AuthContextValue = {
    user,
    loading: loading || viewer === undefined,
    signInWithGoogle,
    signInWithPassword,
    signUpWithPassword,
    signOut,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}

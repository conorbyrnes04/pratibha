import { api } from "@/lib/convexApi";
import { getConvexUrl } from "@/lib/convexUrl";
import { ConvexAuthProvider, useAuthActions } from "@convex-dev/auth/react";
import { ConvexReactClient, useQuery } from "convex/react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  type ReactNode,
} from "react";

const convex = new ConvexReactClient(getConvexUrl());

const tokenStorage = {
  getItem: (key: string) => AsyncStorage.getItem(key),
  setItem: (key: string, value: string) => AsyncStorage.setItem(key, value),
  removeItem: (key: string) => AsyncStorage.removeItem(key),
};

export type AuthUser = { id: string; email?: string; name?: string };

type AuthContextValue = {
  loading: boolean;
  user: AuthUser | null;
  signInWithPassword: (email: string, password: string) => Promise<string | null>;
  signUpWithPassword: (email: string, password: string) => Promise<string | null>;
  signOut: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | null>(null);

function AuthSession({ children }: { children: ReactNode }) {
  const { signIn, signOut } = useAuthActions();
  const viewer = useQuery(api.auth.currentUser);
  const loading = viewer === undefined;
  const user: AuthUser | null = viewer
    ? {
        id: String((viewer as { _id: string })._id),
        email: (viewer as { email?: string }).email,
        name: (viewer as { name?: string }).name,
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
        return error instanceof Error ? error.message : "Could not create the account";
      }
    },
    [signIn],
  );

  const value = useMemo<AuthContextValue>(
    () => ({
      loading,
      user,
      signInWithPassword,
      signUpWithPassword,
      signOut,
    }),
    [loading, user, signInWithPassword, signUpWithPassword, signOut],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function AuthProvider({ children }: { children: ReactNode }) {
  return (
    <ConvexAuthProvider client={convex} storage={tokenStorage}>
      <AuthSession>{children}</AuthSession>
    </ConvexAuthProvider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}

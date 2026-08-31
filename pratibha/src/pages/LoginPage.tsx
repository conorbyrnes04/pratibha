import { useState } from "@lynx-js/react";
import { useAuth } from "../auth/AuthProvider";

interface LoginPageProps {
  onLogin: () => void;
}

export function LoginPage({ onLogin }: LoginPageProps) {
  const { signIn, signUp, signInWithGoogle } = useAuth();
  const [mode, setMode] = useState<"signin" | "signup">("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);

  async function handleSubmit() {
    if (!email || !password) {
      setError("Email and password are required");
      return;
    }
    if (password.length < 10) {
      setError("Password must be at least 10 characters");
      return;
    }

    setLoading(true);
    setError("");

    try {
      if (mode === "signin") {
        await signIn(email, password);
      } else {
        await signUp(email, password);
      }
      onLogin();
    } catch (err: any) {
      setError(err.message || "Authentication failed");
    } finally {
      setLoading(false);
    }
  }

  async function handleGoogleSignIn() {
    setGoogleLoading(true);
    setError("");
    try {
      await signInWithGoogle();
    } catch (err: any) {
      setError(err.message || "Google sign-in failed");
      setGoogleLoading(false);
    }
  }

  return (
    <view style={{ flex: 1, justifyContent: "center", alignItems: "center", padding: 20 }}>
      <view style={{ width: "100%", maxWidth: 400 }}>
        <text style={{ color: "#f0c979", fontSize: 32, fontWeight: "bold", marginBottom: 8, textAlign: "center" }}>
          Pratibha
        </text>
        <text style={{ color: "#ccc", fontSize: 16, marginBottom: 32, textAlign: "center" }}>
          {mode === "signin" ? "Sign in to continue" : "Create your account"}
        </text>

        <view style={{ marginBottom: 16 }}>
          <text style={{ color: "#999", fontSize: 14, marginBottom: 8 }}>Email</text>
          <input
            type="email"
            value={email}
            bindinput={(e: any) => setEmail(e.detail?.value ?? e.target?.value ?? "")}
            placeholder="your@email.com"
            style={{
              width: "100%",
              padding: 12,
              backgroundColor: "#1a1a2e",
              borderWidth: 1,
              borderColor: "#333",
              borderRadius: 4,
              color: "#fff",
              fontSize: 14,
            }}
          />
        </view>

        <view style={{ marginBottom: 24 }}>
          <text style={{ color: "#999", fontSize: 14, marginBottom: 8 }}>Password</text>
          <input
            type="password"
            value={password}
            bindinput={(e: any) => setPassword(e.detail?.value ?? e.target?.value ?? "")}
            placeholder="Min 6 characters"
            style={{
              width: "100%",
              padding: 12,
              backgroundColor: "#1a1a2e",
              borderWidth: 1,
              borderColor: "#333",
              borderRadius: 4,
              color: "#fff",
              fontSize: 14,
            }}
          />
        </view>

        {error && (
          <text style={{ color: "#ff6b6b", fontSize: 14, marginBottom: 16, textAlign: "center" }}>
            {error}
          </text>
        )}

        <view
          bindtap={loading ? undefined : handleSubmit}
          style={{
            width: "100%",
            padding: 14,
            backgroundColor: loading ? "#666" : "#f0c979",
            borderRadius: 4,
            marginBottom: 16,
          }}
        >
          <text style={{ color: "#000", fontSize: 16, fontWeight: "600", textAlign: "center" }}>
            {loading ? "Please wait..." : mode === "signin" ? "Sign In" : "Create Account"}
          </text>
        </view>

        <view style={{ flexDirection: "row", justifyContent: "center", alignItems: "center", marginBottom: 16 }}>
          <view style={{ flex: 1, height: 1, backgroundColor: "#333" }} />
          <text style={{ color: "#666", fontSize: 12, marginLeft: 12, marginRight: 12 }}>OR</text>
          <view style={{ flex: 1, height: 1, backgroundColor: "#333" }} />
        </view>

        <view
          bindtap={googleLoading ? undefined : handleGoogleSignIn}
          style={{
            width: "100%",
            padding: 14,
            backgroundColor: "transparent",
            borderWidth: 1,
            borderColor: "#f0c979",
            borderRadius: 4,
            marginBottom: 16,
          }}
        >
          <text style={{ color: "#f0c979", fontSize: 16, fontWeight: "500", textAlign: "center" }}>
            {googleLoading ? "Opening Google..." : "Continue with Google"}
          </text>
        </view>

        <view style={{ flexDirection: "row", justifyContent: "center" }}>
          <text style={{ color: "#999", fontSize: 14 }}>
            {mode === "signin" ? "No account?" : "Have an account?"}
          </text>
          <text
            bindtap={() => setMode(mode === "signin" ? "signup" : "signin")}
            style={{ color: "#f0c979", fontSize: 14, marginLeft: 6 }}
          >
            {mode === "signin" ? "Create one" : "Sign in"}
          </text>
        </view>
      </view>
    </view>
  );
}

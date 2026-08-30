import React, { useState } from "@lynx-js/react";
import { useAuth } from "../auth/AuthProvider";

interface LoginPageProps {
  onLogin: () => void;
}

export function LoginPage({ onLogin }: LoginPageProps) {
  const { signIn, signUp } = useAuth();
  const [mode, setMode] = useState<"signin" | "signup">("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    if (!email || !password) {
      setError("Email and password are required");
      return;
    }
    if (password.length < 6) {
      setError("Password must be at least 6 characters");
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
            value={email}
            onInput={(e: any) => setEmail(e.detail.value || e.target?.value || "")}
            placeholder="your@email.com"
            style={{
              width: "100%",
              padding: 12,
              backgroundColor: "#1a1a2e",
              border: "1px solid #333",
              borderRadius: 4,
              color: "#fff",
              fontSize: 14,
            }}
          />
        </view>

        <view style={{ marginBottom: 24 }}>
          <text style={{ color: "#999", fontSize: 14, marginBottom: 8 }}>Password</text>
          <input
            value={password}
            onInput={(e: any) => setPassword(e.detail.value || e.target?.value || "")}
            placeholder="Min 6 characters"
            style={{
              width: "100%",
              padding: 12,
              backgroundColor: "#1a1a2e",
              border: "1px solid #333",
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
          onClick={loading ? undefined : handleSubmit}
          style={{
            width: "100%",
            padding: 14,
            backgroundColor: loading ? "#666" : "#f0c979",
            borderRadius: 4,
            cursor: loading ? "default" : "pointer",
            marginBottom: 16,
          }}
        >
          <text style={{ color: "#000", fontSize: 16, fontWeight: "600", textAlign: "center" }}>
            {loading ? "Please wait..." : mode === "signin" ? "Sign In" : "Create Account"}
          </text>
        </view>

        <view style={{ flexDirection: "row", justifyContent: "center", gap: 4 }}>
          <text style={{ color: "#999", fontSize: 14 }}>
            {mode === "signin" ? "No account?" : "Have an account?"}
          </text>
          <text
            onClick={() => setMode(mode === "signin" ? "signup" : "signin")}
            style={{ color: "#f0c979", fontSize: 14, cursor: "pointer", textDecoration: "underline" }}
          >
            {mode === "signin" ? "Create one" : "Sign in"}
          </text>
        </view>
      </view>
    </view>
  );
}

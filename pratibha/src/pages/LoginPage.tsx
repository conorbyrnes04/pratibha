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
    <scroll-view scroll-orientation="vertical" style={{ flex: 1, backgroundColor: "#0a0a0f" }}>
      <view style={{ flex: 1, justifyContent: "center", alignItems: "center", paddingLeft: 40, paddingRight: 40, paddingTop: 60, paddingBottom: 60, minHeight: "100%" }}>
        <view style={{ width: "100%", maxWidth: 400 }}>
          <text style={{ color: "#c9a227", fontSize: 48, fontWeight: "bold", marginBottom: 12, textAlign: "center" }}>
            Pratibha
          </text>
          <text style={{ color: "#999", fontSize: 16, marginBottom: 48, textAlign: "center", lineHeight: "24px" }}>
            Living Manuscript of World Wisdom
          </text>

          <view style={{ marginBottom: 20 }}>
            <text style={{ color: "#999", fontSize: 14, marginBottom: 10 }}>Email</text>
            <input
              value={email}
              bindinput={(res: any) => setEmail(res.detail.value)}
              placeholder="your@email.com"
              style={{
                width: "100%",
                paddingTop: 14,
                paddingBottom: 14,
                paddingLeft: 16,
                paddingRight: 16,
                backgroundColor: "#1a1a2e",
                borderWidth: 1,
                borderColor: "#333",
                borderRadius: 6,
                color: "#fff",
                fontSize: 15,
              }}
            />
          </view>

          <view style={{ marginBottom: 32 }}>
            <text style={{ color: "#999", fontSize: 14, marginBottom: 10 }}>Password</text>
            <input
              type="password"
              value={password}
              bindinput={(res: any) => setPassword(res.detail.value)}
              placeholder="Min 6 characters"
              style={{
                width: "100%",
                paddingTop: 14,
                paddingBottom: 14,
                paddingLeft: 16,
                paddingRight: 16,
                backgroundColor: "#1a1a2e",
                borderWidth: 1,
                borderColor: "#333",
                borderRadius: 6,
                color: "#fff",
                fontSize: 15,
              }}
            />
          </view>

          {error && (
            <text style={{ color: "#ff6b6b", fontSize: 14, marginBottom: 20, textAlign: "center", lineHeight: "20px" }}>
              {error}
            </text>
          )}

          <view
            bindtap={loading ? undefined : handleSubmit}
            style={{
              width: "100%",
              paddingTop: 16,
              paddingBottom: 16,
              backgroundColor: loading ? "#666" : "#c9a227",
              borderRadius: 6,
              marginBottom: 20,
            }}
          >
            <text style={{ color: "#0a0a0f", fontSize: 17, fontWeight: "600", textAlign: "center" }}>
              {loading ? "Please wait..." : mode === "signin" ? "Sign In" : "Create Account"}
            </text>
          </view>

          <view style={{ display: "linear", flexDirection: "row", justifyContent: "center", alignItems: "center" }}>
            <text style={{ color: "#999", fontSize: 14, marginRight: 8 }}>
              {mode === "signin" ? "No account?" : "Have an account?"}
            </text>
            <text
              bindtap={() => setMode(mode === "signin" ? "signup" : "signin")}
              style={{ color: "#c9a227", fontSize: 14 }}
            >
              {mode === "signin" ? "Create one" : "Sign in"}
            </text>
          </view>
        </view>
      </view>
    </scroll-view>
  );
}

import { PratibhaScreen, stackScreenEdges } from "@/components/ui/PratibhaScreen";
import { PratibhaText, useUi } from "@/components/ui/PratibhaText";
import { useAuth } from "@/context/AuthContext";
import { useTheme } from "@/context/ThemeContext";
import { MIN_PASSWORD_LENGTH } from "@shared/authRules";
import { useRouter } from "expo-router";
import { useEffect, useState } from "react";
import { Pressable, TextInput, View, KeyboardAvoidingView, Platform } from "react-native";

export default function LoginScreen() {
  const ui = useUi();
  const { colors } = useTheme();
  const router = useRouter();
  const { user, loading, signInWithPassword, signUpWithPassword } = useAuth();
  const [mode, setMode] = useState<"signin" | "signup">("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (!loading && user) router.replace("/(tabs)");
  }, [loading, user, router]);

  async function onSubmit() {
    setError(null);
    if (password.length < MIN_PASSWORD_LENGTH) {
      setError(`Password must be at least ${MIN_PASSWORD_LENGTH} characters.`);
      return;
    }
    setBusy(true);
    const err =
      mode === "signin"
        ? await signInWithPassword(email, password)
        : await signUpWithPassword(email, password);
    setBusy(false);
    if (err) setError(err);
  }

  return (
    <KeyboardAvoidingView
      style={{ flex: 1 }}
      behavior={Platform.OS === "ios" ? "padding" : "height"}
    >
    <PratibhaScreen edges={stackScreenEdges}>
      <PratibhaText variant="eyebrow">Pratibha</PratibhaText>
      <PratibhaText variant="title" style={{ marginTop: 8 }}>
        {mode === "signin" ? "Sign in" : "Create account"}
      </PratibhaText>
      <PratibhaText variant="soft" style={{ marginTop: 10 }}>
        The path is open without an account. Sign in to keep a journal and carry your walk across
        devices. Email and password only — same account as the website.
      </PratibhaText>

      <View style={[ui.card, { marginTop: 24 }]}>
        <PratibhaText variant="label">Email</PratibhaText>
        <TextInput
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          autoCorrect={false}
          keyboardType="email-address"
          textContentType="emailAddress"
          autoComplete="email"
          placeholder="you@example.com"
          placeholderTextColor={colors.muted2}
          style={{
            marginTop: 10,
            borderRadius: 12,
            borderWidth: 1,
            borderColor: colors.border,
            padding: 12,
            color: colors.foreground,
            fontSize: 16,
          }}
        />
        <PratibhaText variant="label" style={{ marginTop: 16 }}>
          Password
        </PratibhaText>
        <TextInput
          value={password}
          onChangeText={setPassword}
          secureTextEntry
          textContentType={mode === "signup" ? "newPassword" : "password"}
          autoComplete={mode === "signup" ? "password-new" : "password"}
          placeholder={`${MIN_PASSWORD_LENGTH}+ characters`}
          placeholderTextColor={colors.muted2}
          style={{
            marginTop: 10,
            borderRadius: 12,
            borderWidth: 1,
            borderColor: colors.border,
            padding: 12,
            color: colors.foreground,
            fontSize: 16,
          }}
        />
        {error ? (
          <PratibhaText variant="soft" style={{ marginTop: 12, color: colors.rose, fontSize: 14 }}>
            {error}
          </PratibhaText>
        ) : null}
        <Pressable
          style={[ui.button, { marginTop: 20, alignSelf: "stretch", alignItems: "center" }]}
          disabled={busy}
          onPress={() => void onSubmit()}
        >
          <PratibhaText style={ui.buttonText}>
            {busy ? "Working…" : mode === "signin" ? "Sign in" : "Create account"}
          </PratibhaText>
        </Pressable>
      </View>

      <Pressable
        style={{ marginTop: 20 }}
        onPress={() => {
          setError(null);
          setMode(mode === "signin" ? "signup" : "signin");
        }}
      >
        <PratibhaText variant="soft" style={{ fontSize: 15 }}>
          {mode === "signin" ? "No account yet? Create one" : "Already have an account? Sign in"}
        </PratibhaText>
      </Pressable>
    </PratibhaScreen>
    </KeyboardAvoidingView>
  );
}

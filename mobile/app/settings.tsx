import { PratibhaScreen, stackScreenEdges } from "@/components/ui/PratibhaScreen";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { getApiBase, pingHealth, PRODUCTION_API_BASE, setApiBaseOverride } from "@/lib/api";
import { api } from "@/lib/convexApi";
import { APP_ICONS, type AppIconId } from "@/lib/appIcons";
import { API_OVERRIDE_KEY, APP_ICON_KEY, saveJournalNotes, saveLearnBundle } from "@/lib/storage";
import { useAuth } from "@/context/AuthContext";
import { useStudy } from "@/context/StudyContext";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useMutation } from "convex/react";
import { useRouter } from "expo-router";
import { useEffect, useState } from "react";
import {
  ActivityIndicator,
  Alert,
  Image,
  Linking,
  Pressable,
  TextInput,
  View,
  Keyboard,
  Platform,
} from "react-native";
import { colors } from "@/constants/theme";
import * as Haptics from "expo-haptics";
import {
  getAppIconName,
  setAlternateAppIcon,
  supportsAlternateIcons,
} from "expo-alternate-app-icons";

const PRIVACY_URL = "https://pratibha.agniagama.com/privacy";
const SUPPORT_MAIL = "mailto:conor@agniagama.com";

type PingState = "idle" | "checking" | "ok" | "fail";

export default function SettingsScreen() {
  const router = useRouter();
  const { user, loading: authLoading, signOut } = useAuth();
  const { refreshCorpus } = useStudy();
  const deleteAccount = useMutation(api.account.deleteAccount);
  const [apiBase, setApiBase] = useState(getApiBase());
  const [saved, setSaved] = useState(false);
  const [pingState, setPingState] = useState<PingState>("idle");
  const [pingDetail, setPingDetail] = useState("");
  const [iconId, setIconId] = useState<AppIconId>("default");
  const [iconNote, setIconNote] = useState("");
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    if (__DEV__) {
      AsyncStorage.getItem(API_OVERRIDE_KEY).then((v) => {
        if (v) setApiBase(v);
      });
    }
    AsyncStorage.getItem(APP_ICON_KEY).then((v) => {
      if (v && APP_ICONS.some((icon) => icon.id === v)) setIconId(v as AppIconId);
    });
    try {
      if (supportsAlternateIcons) {
        const native = getAppIconName();
        const match = APP_ICONS.find((icon) => icon.nativeName === native);
        if (match) setIconId(match.id);
      }
    } catch {
      /* web / Expo Go */
    }
  }, []);

  async function applyBase(url: string) {
    Keyboard.dismiss();
    const clean = url.trim().replace(/\/$/, "");
    await AsyncStorage.setItem(API_OVERRIDE_KEY, clean);
    setApiBaseOverride(clean);
    setApiBase(clean);
    setSaved(true);
    setPingState("checking");
    setPingDetail("");
    const health = await pingHealth();
    if (health.ok) {
      setPingState("ok");
      setPingDetail(
        health.verseCount != null ? `Connected · ${health.verseCount} verses` : "Connected",
      );
      await refreshCorpus();
      void Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    } else {
      setPingState("fail");
      setPingDetail(health.error || `HTTP ${health.status || "error"}`);
    }
    setTimeout(() => setSaved(false), 2000);
  }

  async function applyIcon(id: AppIconId) {
    const option = APP_ICONS.find((icon) => icon.id === id);
    if (!option) return;
    setIconId(id);
    await AsyncStorage.setItem(APP_ICON_KEY, id);
    void Haptics.selectionAsync();
    if (!supportsAlternateIcons) {
      setIconNote(
        Platform.OS === "web"
          ? "Home-screen icons change on iOS and Android builds."
          : "Icon choice is saved. A development or production build applies it to the home screen.",
      );
      return;
    }
    try {
      await setAlternateAppIcon(option.nativeName);
      setIconNote("");
    } catch (err) {
      setIconNote(err instanceof Error ? err.message : "Could not change the home-screen icon.");
    }
  }

  function confirmDelete() {
    Alert.alert(
      "Delete account?",
      "This permanently removes your journal, path progress, circle offerings, and login. The library stays public. This cannot be undone.",
      [
        { text: "Keep my account", style: "cancel" },
        {
          text: "Delete account",
          style: "destructive",
          onPress: () => void runDelete(),
        },
      ],
    );
  }

  async function runDelete() {
    setDeleting(true);
    try {
      await deleteAccount({});
      await saveJournalNotes([]);
      await saveLearnBundle({ progress: {}, completedAt: {} });
      await signOut();
      router.replace("/(tabs)");
    } catch (err) {
      Alert.alert(
        "Could not delete",
        err instanceof Error ? err.message : "Try again, or email conor@agniagama.com.",
      );
    } finally {
      setDeleting(false);
    }
  }

  return (
    <PratibhaScreen edges={stackScreenEdges}>
      <PratibhaText variant="eyebrow">Settings</PratibhaText>
      <PratibhaText variant="title" style={{ marginTop: 8, fontSize: 28 }}>
        This phone
      </PratibhaText>

      <View style={[ui.card, { marginTop: 20 }]}>
        <PratibhaText variant="label">Account</PratibhaText>
        {authLoading ? (
          <PratibhaText variant="soft" style={{ marginTop: 10 }}>
            Opening session…
          </PratibhaText>
        ) : user ? (
          <>
            <PratibhaText variant="body" style={{ marginTop: 10, fontSize: 17 }}>
              {user.email || "Signed in"}
            </PratibhaText>
            <PratibhaText variant="soft" style={{ marginTop: 8, fontSize: 15 }}>
              Journal and path progress sync with the website.
            </PratibhaText>
            <View style={{ marginTop: 14, flexDirection: "row", flexWrap: "wrap", gap: 10 }}>
              <Pressable style={ui.buttonGhost} onPress={() => void signOut()}>
                <PratibhaText style={ui.buttonGhostText}>Sign out</PratibhaText>
              </Pressable>
              <Pressable onPress={confirmDelete} disabled={deleting}>
                <PratibhaText variant="label" style={{ color: colors.rose, paddingVertical: 10 }}>
                  {deleting ? "Deleting…" : "Delete account"}
                </PratibhaText>
              </Pressable>
            </View>
          </>
        ) : (
          <>
            <PratibhaText variant="soft" style={{ marginTop: 10, fontSize: 15 }}>
              Sign in with email to carry notes and path progress across this phone and the
              website. Google is not used in the app.
            </PratibhaText>
            <Pressable style={[ui.button, { marginTop: 14 }]} onPress={() => router.push("/login" as never)}>
              <PratibhaText style={ui.buttonText}>Sign in</PratibhaText>
            </Pressable>
          </>
        )}
      </View>

      <View style={[ui.card, { marginTop: 20 }]}>
        <PratibhaText variant="label">Privacy</PratibhaText>
        <PratibhaText variant="soft" style={{ marginTop: 8, fontSize: 15 }}>
          How we store journal notes, progress, and Listen audio.
        </PratibhaText>
        <View style={{ marginTop: 14, flexDirection: "row", flexWrap: "wrap", gap: 10 }}>
          <Pressable style={ui.buttonGhost} onPress={() => void Linking.openURL(PRIVACY_URL)}>
            <PratibhaText style={ui.buttonGhostText}>Privacy policy</PratibhaText>
          </Pressable>
          <Pressable style={ui.buttonGhost} onPress={() => void Linking.openURL(SUPPORT_MAIL)}>
            <PratibhaText style={ui.buttonGhostText}>Support</PratibhaText>
          </Pressable>
        </View>
      </View>

      <View style={[ui.card, { marginTop: 20 }]}>
        <PratibhaText variant="label">Home screen icon</PratibhaText>
        <PratibhaText variant="soft" style={{ marginTop: 8, fontSize: 15 }}>
          Pick the seal, the full yantra, or a field color. iOS may ask before it changes.
        </PratibhaText>
        <View
          style={{
            marginTop: 16,
            flexDirection: "row",
            flexWrap: "wrap",
            gap: 12,
          }}
        >
          {APP_ICONS.map((icon) => {
            const selected = icon.id === iconId;
            return (
              <Pressable
                key={icon.id}
                onPress={() => void applyIcon(icon.id)}
                accessibilityRole="button"
                accessibilityState={{ selected }}
                accessibilityLabel={icon.label}
                style={{
                  width: "30%",
                  minWidth: 96,
                  flexGrow: 1,
                  maxWidth: 132,
                  alignItems: "center",
                  gap: 8,
                }}
              >
                <View
                  style={{
                    width: 72,
                    height: 72,
                    borderRadius: 16,
                    overflow: "hidden",
                    backgroundColor: icon.background,
                    borderWidth: selected ? 2 : 1,
                    borderColor: selected ? colors.accent : colors.border,
                  }}
                >
                  <Image source={icon.preview} style={{ width: 72, height: 72 }} />
                </View>
                <PratibhaText
                  variant="label"
                  style={{ color: selected ? colors.accentBright : colors.muted2, textAlign: "center" }}
                >
                  {icon.label}
                </PratibhaText>
              </Pressable>
            );
          })}
        </View>
        {iconNote ? (
          <PratibhaText variant="soft" style={{ marginTop: 12, fontSize: 14 }}>
            {iconNote}
          </PratibhaText>
        ) : null}
      </View>

      {__DEV__ ? (
        <View style={[ui.card, { marginTop: 20 }]}>
          <PratibhaText variant="label">Library (dev)</PratibhaText>
          <PratibhaText variant="soft" style={{ marginTop: 8, fontSize: 15 }}>
            Production builds always use {PRODUCTION_API_BASE}.
          </PratibhaText>
          <TextInput
            value={apiBase}
            onChangeText={setApiBase}
            autoCapitalize="none"
            autoCorrect={false}
            returnKeyType="done"
            onSubmitEditing={() => void applyBase(apiBase)}
            blurOnSubmit
            style={{
              marginTop: 10,
              borderRadius: 12,
              borderWidth: 1,
              borderColor: colors.border,
              padding: 12,
              color: colors.foreground,
              fontSize: 15,
            }}
          />
          <View style={{ marginTop: 14, flexDirection: "row", flexWrap: "wrap", gap: 10 }}>
            <Pressable style={ui.button} onPress={() => void applyBase(apiBase)}>
              <PratibhaText style={ui.buttonText}>{saved ? "Saved" : "Save"}</PratibhaText>
            </Pressable>
            <Pressable style={ui.buttonGhost} onPress={() => void applyBase(PRODUCTION_API_BASE)}>
              <PratibhaText style={ui.buttonGhostText}>Use live library</PratibhaText>
            </Pressable>
          </View>
          {pingState === "checking" ? (
            <View style={{ marginTop: 12, flexDirection: "row", alignItems: "center", gap: 8 }}>
              <ActivityIndicator color={colors.accent} size="small" />
              <PratibhaText variant="soft" style={{ fontSize: 14 }}>
                Checking…
              </PratibhaText>
            </View>
          ) : pingState === "ok" ? (
            <PratibhaText variant="soft" style={{ marginTop: 12, fontSize: 14, color: colors.emerald }}>
              {pingDetail}
            </PratibhaText>
          ) : pingState === "fail" ? (
            <PratibhaText variant="soft" style={{ marginTop: 12, fontSize: 14, color: colors.rose }}>
              Couldn’t connect: {pingDetail}
            </PratibhaText>
          ) : null}
        </View>
      ) : null}
    </PratibhaScreen>
  );
}

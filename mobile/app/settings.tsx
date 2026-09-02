import { PratibhaScreen, stackScreenEdges } from "@/components/ui/PratibhaScreen";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { getApiBase, pingHealth, PRODUCTION_API_BASE, setApiBaseOverride } from "@/lib/api";
import { APP_ICONS, type AppIconId } from "@/lib/appIcons";
import { API_OVERRIDE_KEY, APP_ICON_KEY } from "@/lib/storage";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useStudy } from "@/context/StudyContext";
import { useEffect, useState } from "react";
import {
  ActivityIndicator,
  Image,
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

type PingState = "idle" | "checking" | "ok" | "fail";

export default function SettingsScreen() {
  const { refreshCorpus } = useStudy();
  const [apiBase, setApiBase] = useState(getApiBase());
  const [saved, setSaved] = useState(false);
  const [pingState, setPingState] = useState<PingState>("idle");
  const [pingDetail, setPingDetail] = useState("");
  const [iconId, setIconId] = useState<AppIconId>("default");
  const [iconNote, setIconNote] = useState("");

  useEffect(() => {
    AsyncStorage.getItem(API_OVERRIDE_KEY).then((v) => {
      if (v) setApiBase(v);
    });
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

  return (
    <PratibhaScreen edges={stackScreenEdges}>
      <PratibhaText variant="eyebrow">Settings</PratibhaText>
      <PratibhaText variant="title" style={{ marginTop: 8, fontSize: 28 }}>
        This phone
      </PratibhaText>
      <PratibhaText variant="soft" style={{ marginTop: 10 }}>
        Pratibha talks to the live library by default. Change this only if you are running a local
        server.
      </PratibhaText>

      <View style={[ui.card, { marginTop: 20 }]}>
        <PratibhaText variant="label">Library</PratibhaText>
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
    </PratibhaScreen>
  );
}

import { PratibhaScreen, stackScreenEdges } from "@/components/ui/PratibhaScreen";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { getApiBase, pingHealth, PRODUCTION_API_BASE, setApiBaseOverride } from "@/lib/api";
import { API_OVERRIDE_KEY } from "@/lib/storage";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useStudy } from "@/context/StudyContext";
import { useEffect, useState } from "react";
import { ActivityIndicator, Pressable, TextInput, View, Keyboard } from "react-native";
import { colors } from "@/constants/theme";
import * as Haptics from "expo-haptics";

type PingState = "idle" | "checking" | "ok" | "fail";

export default function SettingsScreen() {
  const { refreshCorpus } = useStudy();
  const [apiBase, setApiBase] = useState(getApiBase());
  const [saved, setSaved] = useState(false);
  const [pingState, setPingState] = useState<PingState>("idle");
  const [pingDetail, setPingDetail] = useState("");

  useEffect(() => {
    AsyncStorage.getItem(API_OVERRIDE_KEY).then((v) => {
      if (v) setApiBase(v);
    });
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
    </PratibhaScreen>
  );
}

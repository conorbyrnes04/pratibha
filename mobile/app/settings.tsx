import { PratibhaScreen } from "@/components/ui/PratibhaScreen";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { getApiBase, pingHealth, setApiBaseOverride } from "@/lib/api";
import { API_OVERRIDE_KEY } from "@/lib/storage";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useStudy } from "@/context/StudyContext";
import { useEffect, useState } from "react";
import { ActivityIndicator, Pressable, TextInput, View, Keyboard } from "react-native";
import { colors } from "@/constants/theme";

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

  async function save() {
    Keyboard.dismiss();
    const clean = apiBase.trim().replace(/\/$/, "");
    await AsyncStorage.setItem(API_OVERRIDE_KEY, clean);
    setApiBaseOverride(clean);
    setSaved(true);
    setPingState("checking");
    setPingDetail("");
    const health = await pingHealth();
    if (health.ok) {
      setPingState("ok");
      setPingDetail(
        health.verseCount != null ? `Connected · ${health.verseCount} verses loaded` : "Connected",
      );
      await refreshCorpus();
    } else {
      setPingState("fail");
      setPingDetail(health.error || `HTTP ${health.status || "error"}`);
    }
    setTimeout(() => setSaved(false), 2000);
  }

  return (
    <PratibhaScreen>
      <PratibhaText variant="eyebrow">Connection</PratibhaText>
      <PratibhaText variant="title" style={{ marginTop: 8, fontSize: 28 }}>
        API Settings
      </PratibhaText>
      <PratibhaText variant="soft" style={{ marginTop: 10 }}>
        On a physical iPhone, use your Mac&apos;s LAN IP (e.g. http://192.168.1.12:8000), not localhost.
        Simulator can use http://127.0.0.1:8000.
      </PratibhaText>

      <View style={[ui.card, { marginTop: 20 }]}>
        <PratibhaText variant="label">API base URL</PratibhaText>
        <TextInput
          value={apiBase}
          onChangeText={setApiBase}
          autoCapitalize="none"
          autoCorrect={false}
          returnKeyType="done"
          onSubmitEditing={Keyboard.dismiss}
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
        <Pressable style={[ui.button, { marginTop: 14 }]} onPress={save}>
          <PratibhaText style={ui.buttonText}>{saved ? "Saved ✓" : "Save & reconnect"}</PratibhaText>
        </Pressable>
        {pingState === "checking" ? (
          <View style={{ marginTop: 12, flexDirection: "row", alignItems: "center", gap: 8 }}>
            <ActivityIndicator color={colors.accent} size="small" />
            <PratibhaText variant="soft" style={{ fontSize: 14 }}>
              Checking connection…
            </PratibhaText>
          </View>
        ) : pingState === "ok" ? (
          <PratibhaText variant="soft" style={{ marginTop: 12, fontSize: 14, color: colors.emerald }}>
            {pingDetail}
          </PratibhaText>
        ) : pingState === "fail" ? (
          <PratibhaText variant="soft" style={{ marginTop: 12, fontSize: 14, color: colors.rose }}>
            Connection failed: {pingDetail}
          </PratibhaText>
        ) : null}
      </View>
    </PratibhaScreen>
  );
}

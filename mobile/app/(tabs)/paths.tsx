import { PathRealmList } from "@/components/PathRealmList";
import { PratibhaScreen } from "@/components/ui/PratibhaScreen";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { useStudy } from "@/context/StudyContext";
import { getApiBase } from "@/lib/api";
import { colors } from "@/constants/theme";
import { Link, router } from "expo-router";
import * as Haptics from "expo-haptics";
import { Pressable, StyleSheet, View } from "react-native";

export default function PathsTab() {
  const {
    heroTrack,
    heroNextStep,
    heroNextIndex,
    startedTrackId,
    anyProgress,
    loading,
    error,
    refreshCorpus,
    recommendedNextId,
  } = useStudy();

  const heroLabel = startedTrackId ? "Continue" : anyProgress ? "Recommended next" : "Start here";

  function openHero() {
    void Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    router.push({
      pathname: "/step/[trackId]/[stepId]",
      params: { trackId: heroTrack.id, stepId: heroNextStep.id },
    });
  }

  return (
    <PratibhaScreen onRefresh={refreshCorpus} refreshing={loading}>
      <PratibhaText variant="eyebrow">Path</PratibhaText>
      <PratibhaText variant="title" style={{ marginTop: 8 }}>
        The trail
      </PratibhaText>
      <PratibhaText variant="soft" style={{ marginTop: 8 }}>
        Gate by gate. Practice, keep a note, then move on.
      </PratibhaText>

      {error ? (
        <View style={[ui.card, styles.error, { marginTop: 16 }]}>
          <PratibhaText variant="heading" style={{ fontSize: 18, color: colors.rose }}>
            Can’t reach the library
          </PratibhaText>
          <PratibhaText variant="soft" style={{ marginTop: 8 }}>
            {error}
          </PratibhaText>
          <PratibhaText variant="soft" style={{ marginTop: 8, fontSize: 13 }}>
            {getApiBase()}
          </PratibhaText>
          <Link href="/settings" asChild>
            <Pressable style={[ui.button, { marginTop: 12 }]}>
              <PratibhaText style={ui.buttonText}>Open settings</PratibhaText>
            </Pressable>
          </Link>
        </View>
      ) : null}

      <Pressable style={[ui.card, ui.cardGold, { marginTop: 20 }]} onPress={openHero}>
        <PratibhaText variant="label">{heroLabel}</PratibhaText>
        <PratibhaText variant="heading" style={{ marginTop: 8 }}>
          {heroTrack.title}
        </PratibhaText>
        <PratibhaText variant="soft" style={{ marginTop: 6 }}>
          {startedTrackId
            ? `Gate ${heroNextIndex + 1} · ${heroNextStep.title}`
            : heroTrack.focus}
        </PratibhaText>
        <PratibhaText style={[ui.buttonText, { marginTop: 14, color: colors.accentBright }]}>
          {startedTrackId ? "Continue" : "Begin"}
        </PratibhaText>
      </Pressable>

      <PathRealmList
        selectedTrackId={startedTrackId || recommendedNextId}
        onSelectTrack={(id) => router.push({ pathname: "/path/[id]", params: { id } })}
      />
    </PratibhaScreen>
  );
}

const styles = StyleSheet.create({
  error: { borderColor: "rgba(253,164,175,0.35)" },
});

import { PathRealmList } from "@/components/PathRealmList";
import { PratibhaScreen } from "@/components/ui/PratibhaScreen";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { useStudy } from "@/context/StudyContext";
import { getApiBase } from "@/lib/api";
import { Link, router } from "expo-router";
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

  return (
    <PratibhaScreen onRefresh={refreshCorpus} refreshing={loading}>
      <View style={styles.header}>
        <View>
          <PratibhaText variant="eyebrow">Guided study</PratibhaText>
          <PratibhaText variant="title" style={{ marginTop: 8 }}>
            Paths
          </PratibhaText>
        </View>
        <Link href="/settings" asChild>
          <Pressable style={ui.buttonGhost}>
            <PratibhaText style={ui.buttonGhostText}>API</PratibhaText>
          </Pressable>
        </Link>
      </View>

      <PratibhaText variant="soft" style={{ marginTop: 8 }}>
        Gate by gate through the corpus — practice, journal, and integrate before you move on.
      </PratibhaText>

      {error ? (
        <View style={[ui.card, styles.error, { marginTop: 16 }]}>
          <PratibhaText variant="heading" style={{ fontSize: 18, color: "#fda4af" }}>
            API unreachable
          </PratibhaText>
          <PratibhaText variant="soft" style={{ marginTop: 8 }}>
            {error}
          </PratibhaText>
          <PratibhaText variant="soft" style={{ marginTop: 8, fontSize: 13 }}>
            Current base: {getApiBase()}
          </PratibhaText>
          <Link href="/settings" asChild>
            <Pressable style={[ui.button, { marginTop: 12 }]}>
              <PratibhaText style={ui.buttonText}>Configure API</PratibhaText>
            </Pressable>
          </Link>
        </View>
      ) : null}

      <Pressable
        style={[ui.card, ui.cardGold, { marginTop: 20 }]}
        onPress={() =>
          router.push({
            pathname: "/step/[trackId]/[stepId]",
            params: { trackId: heroTrack.id, stepId: heroNextStep.id },
          })
        }
      >
        <PratibhaText variant="label">{heroLabel}</PratibhaText>
        <PratibhaText variant="heading" style={{ marginTop: 8 }}>
          {heroTrack.title}
        </PratibhaText>
        <PratibhaText variant="soft" style={{ marginTop: 6 }}>
          {startedTrackId
            ? `Next · Step ${heroNextIndex + 1}: ${heroNextStep.title}`
            : heroTrack.focus}
        </PratibhaText>
        <PratibhaText style={[ui.buttonText, { marginTop: 14, color: colorsAccent() }]}>
          {startedTrackId ? "Continue →" : "Begin →"}
        </PratibhaText>
      </Pressable>

      <Pressable
        style={[ui.card, { marginTop: 12 }]}
        onPress={() =>
          router.push({
            pathname: "/step/[trackId]/[stepId]",
            params: { trackId: heroTrack.id, stepId: heroNextStep.id },
          })
        }
      >
        <PratibhaText variant="eyebrow">Today&apos;s sit</PratibhaText>
        <PratibhaText variant="soft" style={{ marginTop: 6, fontSize: 13 }}>
          Step {heroNextIndex + 1}: {heroNextStep.title}
        </PratibhaText>
        <PratibhaText variant="body" style={{ marginTop: 10, fontSize: 16 }}>
          {heroNextStep.practice}
        </PratibhaText>
        <PratibhaText style={[ui.buttonText, { marginTop: 14, color: colorsAccent() }]}>
          Begin practice →
        </PratibhaText>
        <PratibhaText variant="label" style={{ marginTop: 8, fontSize: 10 }}>
          {heroTrack.title}
        </PratibhaText>
      </Pressable>

      <PathRealmList
        selectedTrackId={startedTrackId || recommendedNextId}
        onSelectTrack={(id) => router.push({ pathname: "/path/[id]", params: { id } })}
      />
    </PratibhaScreen>
  );
}

function colorsAccent() {
  return "#f0c979";
}

const styles = StyleSheet.create({
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-start",
    gap: 12,
  },
  error: { borderColor: "rgba(253,164,175,0.35)" },
});

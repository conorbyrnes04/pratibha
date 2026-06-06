import { PratibhaScreen } from "@/components/ui/PratibhaScreen";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { useStudy } from "@/context/StudyContext";
import { stepKey } from "@/lib/storage";
import { useLocalSearchParams, router } from "expo-router";
import { Pressable, StyleSheet, View } from "react-native";

export default function PathScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const { trackById, progress, trackDoneCount, resetTrack } = useStudy();
  const track = trackById[id || ""];

  if (!track) {
    return (
      <PratibhaScreen>
        <PratibhaText variant="soft">Path not found.</PratibhaText>
      </PratibhaScreen>
    );
  }

  const done = trackDoneCount(track);
  const pct = Math.round((done / Math.max(1, track.steps.length)) * 100);
  const nextIndex = track.steps.findIndex((s) => !progress[stepKey(track.id, s.id)]);

  return (
    <PratibhaScreen>
      <PratibhaText variant="eyebrow">Path</PratibhaText>
      <PratibhaText variant="title" style={{ marginTop: 8 }}>
        {track.title}
      </PratibhaText>
      <PratibhaText variant="label" style={{ marginTop: 8 }}>
        {track.level} · {track.estimatedSessions}
      </PratibhaText>
      <PratibhaText variant="soft" style={{ marginTop: 12 }}>
        {track.outcome}
      </PratibhaText>
      <PratibhaText variant="body" style={{ marginTop: 14, fontSize: 16 }}>
        {track.arc}
      </PratibhaText>

      <View style={{ marginTop: 18 }}>
        <View style={styles.progressRow}>
          <PratibhaText variant="label">Progress</PratibhaText>
          <PratibhaText variant="label">
            {done}/{track.steps.length}
          </PratibhaText>
        </View>
        <View style={[ui.progressTrack, { marginTop: 8 }]}>
          <View style={[ui.progressFill, { width: `${pct}%` }]} />
        </View>
      </View>

      {nextIndex >= 0 ? (
        <Pressable
          style={[ui.button, { marginTop: 18 }]}
          onPress={() =>
            router.push({
              pathname: "/step/[trackId]/[stepId]",
              params: { trackId: track.id, stepId: track.steps[nextIndex].id },
            })
          }
        >
          <PratibhaText style={ui.buttonText}>Continue · Step {nextIndex + 1}</PratibhaText>
        </Pressable>
      ) : null}

      <Pressable style={[ui.buttonGhost, { marginTop: 12 }]} onPress={() => resetTrack(track.id)}>
        <PratibhaText style={ui.buttonGhostText}>Reset path</PratibhaText>
      </Pressable>

      <View style={{ marginTop: 24, gap: 12 }}>
        {track.steps.map((step, idx) => {
          const complete = !!progress[stepKey(track.id, step.id)];
          const current = idx === nextIndex && !complete;
          return (
            <Pressable
              key={step.id}
              style={[ui.card, current && ui.cardGold]}
              onPress={() =>
                router.push({
                  pathname: "/step/[trackId]/[stepId]",
                  params: { trackId: track.id, stepId: step.id },
                })
              }
            >
              <PratibhaText variant="label">
                Step {idx + 1} {current ? "· next up" : complete ? "· complete" : ""}
              </PratibhaText>
              <PratibhaText variant="heading" style={{ marginTop: 6, fontSize: 20 }}>
                {step.title}
              </PratibhaText>
              <PratibhaText variant="soft" style={{ marginTop: 6, fontSize: 14 }}>
                {step.orientation}
              </PratibhaText>
            </Pressable>
          );
        })}
      </View>
    </PratibhaScreen>
  );
}

const styles = StyleSheet.create({
  progressRow: { flexDirection: "row", justifyContent: "space-between" },
});

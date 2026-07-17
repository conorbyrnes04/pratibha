import { PathOrb, type PathOrbState } from "@/components/PathOrb";
import { LEARNING_REALMS, RECOMMENDED_SPINE } from "@shared/learningPaths";
import { LinearGradient } from "expo-linear-gradient";
import { Pressable, StyleSheet, View } from "react-native";
import { useStudy } from "@/context/StudyContext";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { colors } from "@/constants/theme";

type Props = {
  selectedTrackId: string;
  onSelectTrack: (trackId: string) => void;
};

function orbState(
  complete: boolean,
  isNext: boolean,
  isStart: boolean,
  selected: boolean,
): PathOrbState {
  if (complete) return "complete";
  if (isNext || isStart) return "highlight";
  if (selected) return "active";
  return "default";
}

export function PathRealmList({ selectedTrackId, onSelectTrack }: Props) {
  const { trackById, progress, recommendedNextId, anyProgress, trackDoneCount } = useStudy();

  return (
    <View style={styles.wrap}>
      <View style={styles.intro}>
        <PratibhaText variant="eyebrow">The journey</PratibhaText>
        <PratibhaText variant="soft" style={styles.introCopy}>
          Beginner at the inner ring, intermediate in the middle, advanced at the capstone — eight paths on one breathing
          diagram. Tap a gate to open it.
        </PratibhaText>
      </View>

      {LEARNING_REALMS.map((realm) => (
        <View key={realm.id} style={styles.realmShell}>
          <LinearGradient
            colors={["rgba(216, 168, 74, 0.07)", "rgba(216, 168, 74, 0.01)", "transparent"]}
            start={{ x: 1, y: 0 }}
            end={{ x: 0.2, y: 0.85 }}
            style={StyleSheet.absoluteFill}
          />
          <LinearGradient
            colors={["rgba(13, 13, 24, 0.55)", "rgba(8, 8, 14, 0.82)"]}
            style={StyleSheet.absoluteFill}
          />
          <LinearGradient
            colors={["rgba(240, 201, 121, 0.14)", "transparent"]}
            style={styles.yantraGlow}
          />

          <View style={styles.realmContent}>
            <PratibhaText variant="eyebrow">{realm.title}</PratibhaText>
            <PratibhaText variant="soft" style={{ marginTop: 6, fontSize: 14, lineHeight: 21 }}>
              {realm.blurb}
            </PratibhaText>

            <View style={styles.pathList}>
              {realm.trackIds.map((tid) => {
                const track = trackById[tid];
                if (!track) return null;
                const done = trackDoneCount(track);
                const total = track.steps.length;
                const complete = total > 0 && done === total;
                const spineN = RECOMMENDED_SPINE.indexOf(tid);
                const isNext = tid === recommendedNextId && !complete;
                const isStart = !anyProgress && tid === RECOMMENDED_SPINE[0];
                const selected = selectedTrackId === tid;
                const pct = Math.round((done / Math.max(1, total)) * 100);
                const state = orbState(complete, isNext, isStart, selected);

                return (
                  <Pressable
                    key={tid}
                    onPress={() => onSelectTrack(tid)}
                    style={({ pressed }) => [
                      ui.card,
                      styles.pathCard,
                      selected && styles.pathCardSelected,
                      pressed && styles.pathCardPressed,
                    ]}
                  >
                    <View style={styles.row}>
                      <PathOrb
                        label={complete ? "✓" : spineN >= 0 ? String(spineN + 1) : "•"}
                        state={state}
                      />
                      <View style={styles.pathBody}>
                        <PratibhaText variant="heading" style={{ fontSize: 20 }}>
                          {track.title}
                        </PratibhaText>
                        <PratibhaText variant="label" style={{ marginTop: 4 }}>
                          {track.level} · {track.estimatedSessions}
                        </PratibhaText>
                        <PratibhaText variant="soft" style={{ marginTop: 6, fontSize: 14, lineHeight: 20 }}>
                          {track.focus}
                        </PratibhaText>
                        <View style={[ui.progressTrack, { marginTop: 10 }]}>
                          <View style={[ui.progressFill, { width: `${pct}%` }]} />
                        </View>
                        <PratibhaText variant="label" style={styles.statusLine}>
                          {complete
                            ? "Complete ✓"
                            : isNext
                              ? "Recommended next"
                              : isStart
                                ? "Start here"
                                : done > 0
                                  ? `In progress · ${done}/${total}`
                                  : `${done}/${total} steps`}
                        </PratibhaText>
                      </View>
                    </View>
                  </Pressable>
                );
              })}
            </View>
          </View>
        </View>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { gap: 28, marginTop: 24 },
  intro: { gap: 8 },
  introCopy: { fontSize: 15, lineHeight: 22 },
  realmShell: {
    borderRadius: 24,
    borderWidth: 1,
    borderColor: "rgba(240, 201, 121, 0.12)",
    overflow: "hidden",
  },
  yantraGlow: {
    position: "absolute",
    top: -56,
    right: -56,
    width: 176,
    height: 176,
    borderRadius: 88,
    opacity: 0.55,
  },
  realmContent: {
    padding: 18,
  },
  pathList: { marginTop: 16, gap: 10 },
  pathCard: {
    padding: 14,
    backgroundColor: "rgba(0, 0, 0, 0.22)",
  },
  pathCardSelected: {
    borderColor: "rgba(240, 201, 121, 0.55)",
    backgroundColor: "rgba(240, 201, 121, 0.1)",
  },
  pathCardPressed: {
    opacity: 0.92,
    transform: [{ scale: 0.995 }],
  },
  row: { flexDirection: "row", gap: 14, alignItems: "flex-start" },
  pathBody: { flex: 1, minWidth: 0 },
  statusLine: {
    marginTop: 8,
    color: colors.accentBright,
    opacity: 0.75,
    fontSize: 10,
  },
});

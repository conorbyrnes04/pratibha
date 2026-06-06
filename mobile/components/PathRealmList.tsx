import { LEARNING_REALMS, RECOMMENDED_SPINE } from "@shared/learningPaths";
import { Pressable, StyleSheet, View } from "react-native";
import { useStudy } from "@/context/StudyContext";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { colors } from "@/constants/theme";
import { stepKey } from "@/lib/storage";

type Props = {
  selectedTrackId: string;
  onSelectTrack: (trackId: string) => void;
};

export function PathRealmList({ selectedTrackId, onSelectTrack }: Props) {
  const { trackById, progress, recommendedNextId, anyProgress, trackDoneCount } = useStudy();

  return (
    <View style={styles.wrap}>
      {LEARNING_REALMS.map((realm) => (
        <View key={realm.id} style={styles.realm}>
          <PratibhaText variant="eyebrow">{realm.title}</PratibhaText>
          <PratibhaText variant="soft" style={{ marginTop: 6 }}>
            {realm.blurb}
          </PratibhaText>
          <View style={{ marginTop: 14, gap: 10 }}>
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

              return (
                <Pressable
                  key={tid}
                  onPress={() => onSelectTrack(tid)}
                  style={[ui.card, selected && ui.cardGold, styles.pathCard]}
                >
                  <View style={styles.row}>
                    <View
                      style={[
                        styles.badge,
                        complete && styles.badgeDone,
                        (isNext || isStart) && styles.badgeNext,
                      ]}
                    >
                      <PratibhaText style={styles.badgeText}>{complete ? "✓" : spineN + 1}</PratibhaText>
                    </View>
                    <View style={{ flex: 1 }}>
                      <PratibhaText variant="heading" style={{ fontSize: 20 }}>
                        {track.title}
                      </PratibhaText>
                      <PratibhaText variant="label" style={{ marginTop: 4 }}>
                        {track.level} · {track.estimatedSessions}
                      </PratibhaText>
                      <PratibhaText variant="soft" style={{ marginTop: 6, fontSize: 14 }}>
                        {track.focus}
                      </PratibhaText>
                      <View style={[ui.progressTrack, { marginTop: 10 }]}>
                        <View style={[ui.progressFill, { width: `${pct}%` }]} />
                      </View>
                    </View>
                  </View>
                </Pressable>
              );
            })}
          </View>
        </View>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { gap: 28, marginTop: 8 },
  realm: { gap: 4 },
  pathCard: { padding: 14 },
  row: { flexDirection: "row", gap: 12, alignItems: "flex-start" },
  badge: {
    width: 40,
    height: 40,
    borderRadius: 20,
    borderWidth: 2,
    borderColor: "rgba(240,201,121,0.3)",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: colors.background,
  },
  badgeDone: { borderColor: colors.emerald, backgroundColor: "rgba(110,231,183,0.2)" },
  badgeNext: { borderColor: colors.accentBright, backgroundColor: colors.accentBright },
  badgeText: {
    fontFamily: "System",
    fontSize: 14,
    fontWeight: "700",
    color: colors.foreground,
  },
});

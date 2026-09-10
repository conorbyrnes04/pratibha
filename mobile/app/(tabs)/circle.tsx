import { IconButton, symbols } from "@/components/IconButton";
import { PratibhaScreen } from "@/components/ui/PratibhaScreen";
import { PratibhaText, useUi } from "@/components/ui/PratibhaText";
import { useTheme } from "@/context/ThemeContext";
import { api } from "@/lib/convexApi";
import { excerptReading, FEATURED_CIRCLE_DOORS, formatCircleTime } from "@shared/circleVerses";
import { useQuery } from "convex/react";
import { router } from "expo-router";
import { Pressable, View } from "react-native";

type CircleReading = {
  _id: string;
  mine: boolean;
  displayName: string;
  lastActivityAt: number;
  verseId: string;
  verseTitle: string;
  body: string;
  replyCount: number;
  sitCount: number;
};

/** Relative time, degrading gracefully where Intl.RelativeTimeFormat is absent. */
function relativeTime(ts: number): string {
  try {
    return formatCircleTime(ts, "en");
  } catch {
    return new Date(ts).toLocaleDateString();
  }
}

function openVerse(verseId: string) {
  router.push({ pathname: "/passage/[id]", params: { id: verseId } });
}

function DoorChips() {
  const { colors } = useTheme();
  return (
    <View style={{ marginTop: 14, flexDirection: "row", flexWrap: "wrap", gap: 8 }}>
      {FEATURED_CIRCLE_DOORS.map((door) => (
        <Pressable
          key={door.id}
          onPress={() => openVerse(door.id)}
          style={{
            borderRadius: 999,
            borderWidth: 1,
            borderColor: colors.border,
            paddingHorizontal: 14,
            paddingVertical: 8,
          }}
        >
          <PratibhaText variant="label" style={{ color: colors.accentBright }}>
            {door.label}
          </PratibhaText>
        </Pressable>
      ))}
    </View>
  );
}

export default function CircleTab() {
  const ui = useUi();
  const { colors } = useTheme();
  const recent = useQuery(api.studentCommentaries.listRecent, {}) as CircleReading[] | undefined;

  return (
    <PratibhaScreen>
      <View style={{ flexDirection: "row", justifyContent: "space-between", alignItems: "flex-start" }}>
        <View style={{ flex: 1, paddingRight: 12 }}>
          <PratibhaText variant="eyebrow">Circle</PratibhaText>
          <PratibhaText variant="title" style={{ marginTop: 8 }}>
            The house of readings
          </PratibhaText>
          <PratibhaText variant="soft" style={{ marginTop: 8 }}>
            Offer what a verse asks of you, and sit with what others have left.
          </PratibhaText>
        </View>
        <View style={{ flexDirection: "row", gap: 16, marginTop: 4 }}>
          <IconButton name={symbols.ask} accessibilityLabel="Ask" href={"/ask" as never} />
          <IconButton name={symbols.gear} accessibilityLabel="Settings" href="/settings" />
        </View>
      </View>

      <View style={{ marginTop: 24 }}>
        <PratibhaText variant="label">Doors open today</PratibhaText>
        <PratibhaText variant="soft" style={{ marginTop: 6, fontSize: 14 }}>
          Step through a verse and leave your reading.
        </PratibhaText>
        <DoorChips />
      </View>

      <View style={{ marginTop: 28 }}>
        <PratibhaText variant="label">Recent readings</PratibhaText>
        {recent === undefined ? (
          <PratibhaText variant="soft" style={{ marginTop: 12, fontSize: 14 }}>
            Opening the house…
          </PratibhaText>
        ) : recent.length === 0 ? (
          <View style={[ui.card, { marginTop: 12 }]}>
            <PratibhaText variant="soft" style={{ fontSize: 14 }}>
              No readings yet. Step through a door above and be the first to leave one.
            </PratibhaText>
          </View>
        ) : (
          <View style={{ marginTop: 12, gap: 12 }}>
            {recent.map((reading) => (
              <Pressable key={reading._id} style={ui.card} onPress={() => openVerse(reading.verseId)}>
                <PratibhaText variant="label">
                  {reading.mine ? "Your reading" : reading.displayName}
                  {"   "}
                  {relativeTime(reading.lastActivityAt)}
                </PratibhaText>
                <PratibhaText variant="heading" style={{ marginTop: 6, fontSize: 20 }} numberOfLines={2}>
                  {reading.verseTitle}
                </PratibhaText>
                <PratibhaText variant="body" style={{ marginTop: 8, fontSize: 15, lineHeight: 22 }} numberOfLines={4}>
                  {excerptReading(reading.body)}
                </PratibhaText>
                <PratibhaText variant="label" style={{ marginTop: 10, color: colors.muted2 }}>
                  {reading.replyCount === 1
                    ? "1 reply"
                    : reading.replyCount > 0
                      ? `${reading.replyCount} replies`
                      : "No replies yet"}
                  {reading.sitCount > 0 ? `  ·  ${reading.sitCount} sat with this` : ""}
                </PratibhaText>
              </Pressable>
            ))}
          </View>
        )}
      </View>
    </PratibhaScreen>
  );
}

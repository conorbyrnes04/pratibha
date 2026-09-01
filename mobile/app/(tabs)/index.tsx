import { IconButton, symbols } from "@/components/IconButton";
import { PratibhaScreen } from "@/components/ui/PratibhaScreen";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { useStudy } from "@/context/StudyContext";
import { getVerse } from "@/lib/api";
import { passagePreview } from "@/lib/verseLayers";
import { displayCollectionName } from "@shared/collectionLabels";
import type { VerseItem } from "@shared/types";
import { router } from "expo-router";
import * as Haptics from "expo-haptics";
import { useEffect, useState } from "react";
import { Pressable, View } from "react-native";

export default function HomeTab() {
  const { heroTrack, heroNextStep, hydrated, startedTrackId } = useStudy();
  const [verse, setVerse] = useState<VerseItem | null>(null);

  useEffect(() => {
    const id = heroNextStep?.passageId;
    if (!id) {
      setVerse(null);
      return;
    }
    let cancelled = false;
    getVerse(id)
      .then((item) => {
        if (!cancelled) setVerse(item);
      })
      .catch(() => {
        if (!cancelled) setVerse(null);
      });
    return () => {
      cancelled = true;
    };
  }, [heroNextStep?.passageId]);

  const title = heroNextStep?.title || "Today's gate";
  const collection = verse ? displayCollectionName(verse.collection) : heroTrack.title;
  const line = verse ? passagePreview(verse) : heroNextStep?.orientation || "";
  const cta = startedTrackId ? "Continue" : "Begin";

  function openGate() {
    void Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    router.push({
      pathname: "/step/[trackId]/[stepId]",
      params: { trackId: heroTrack.id, stepId: heroNextStep.id },
    });
  }

  return (
    <PratibhaScreen>
      <View style={styles.header}>
        <View style={{ flex: 1, paddingRight: 12 }}>
          <PratibhaText variant="eyebrow">Today</PratibhaText>
          <PratibhaText variant="title" style={{ marginTop: 8 }}>
            {hydrated ? heroTrack.title : "Your path"}
          </PratibhaText>
        </View>
        <View style={{ flexDirection: "row", gap: 16, marginTop: 4 }}>
          <IconButton name={symbols.ask} accessibilityLabel="Ask" href={"/ask" as never} />
          <IconButton name={symbols.gear} accessibilityLabel="Settings" href="/settings" />
        </View>
      </View>

      <Pressable style={[ui.card, ui.cardGold, { marginTop: 20 }]} onPress={openGate}>
        <PratibhaText variant="label">{startedTrackId ? "Next gate" : "Start here"}</PratibhaText>
        <PratibhaText variant="heading" style={{ marginTop: 12, fontSize: 26, lineHeight: 32 }}>
          {title}
        </PratibhaText>
        <PratibhaText variant="label" style={{ marginTop: 8 }}>
          {collection || "The Path"}
        </PratibhaText>
        <PratibhaText variant="body" style={{ marginTop: 16, fontSize: 18, lineHeight: 28 }}>
          {line || heroNextStep?.keyIdea || "One gate. A passage. One practice."}
        </PratibhaText>
        {heroNextStep?.practice ? (
          <View style={[ui.card, { marginTop: 16, backgroundColor: "rgba(0,0,0,0.22)" }]}>
            <PratibhaText variant="label">Practice</PratibhaText>
            <PratibhaText variant="soft" style={{ marginTop: 8, fontSize: 15, lineHeight: 22 }}>
              {heroNextStep.practice}
            </PratibhaText>
          </View>
        ) : null}
        <View style={{ marginTop: 16, flexDirection: "row", flexWrap: "wrap", gap: 10 }}>
          <Pressable style={ui.button} onPress={openGate}>
            <PratibhaText style={ui.buttonText}>{cta}</PratibhaText>
          </Pressable>
          {verse ? (
            <Pressable
              style={ui.buttonGhost}
              onPress={() =>
                router.push({
                  pathname: "/ask",
                  params: { verse_id: verse._id, mode: "explain", q: "Guide me through this passage." },
                } as never)
              }
            >
              <PratibhaText style={ui.buttonGhostText}>Ask about this</PratibhaText>
            </Pressable>
          ) : null}
        </View>
      </Pressable>
    </PratibhaScreen>
  );
}

const styles = {
  header: {
    flexDirection: "row" as const,
    justifyContent: "space-between" as const,
    alignItems: "flex-start" as const,
  },
};

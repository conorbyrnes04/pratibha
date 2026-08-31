import { PratibhaScreen } from "@/components/ui/PratibhaScreen";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { useStudy } from "@/context/StudyContext";
import { getVerse } from "@/lib/api";
import { passagePreview } from "@/lib/verseLayers";
import { displayCollectionName } from "@shared/collectionLabels";
import { displayPassageTitle } from "@shared/passageTitles";
import type { VerseItem } from "@shared/types";
import { Link, router } from "expo-router";
import { useEffect, useState } from "react";
import { Pressable, View } from "react-native";

export default function HomeTab() {
  const { heroTrack, heroNextStep, hydrated } = useStudy();
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

  return (
    <PratibhaScreen>
      <View style={styles.header}>
        <View>
          <PratibhaText variant="eyebrow">Today</PratibhaText>
          <PratibhaText variant="title" style={{ marginTop: 8 }}>
            A walk through world wisdom
          </PratibhaText>
        </View>
        <Link href="/settings" asChild>
          <Pressable style={ui.buttonGhost}>
            <PratibhaText style={ui.buttonGhostText}>API</PratibhaText>
          </Pressable>
        </Link>
      </View>

      <View style={[ui.card, ui.cardGold, { marginTop: 20 }]}>
        <PratibhaText variant="eyebrow">{hydrated ? heroTrack.title : "The Path"}</PratibhaText>
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
          <Pressable
            style={ui.button}
            onPress={() =>
              router.push({
                pathname: "/step/[trackId]/[stepId]",
                params: { trackId: heroTrack.id, stepId: heroNextStep.id },
              })
            }
          >
            <PratibhaText style={ui.buttonText}>Enter this gate</PratibhaText>
          </Pressable>
          <Pressable style={ui.buttonGhost} onPress={() => router.push("/(tabs)/paths")}>
            <PratibhaText style={ui.buttonGhostText}>See the trail</PratibhaText>
          </Pressable>
        </View>
      </View>
    </PratibhaScreen>
  );
}

const styles = {
  header: {
    flexDirection: "row" as const,
    justifyContent: "space-between" as const,
    alignItems: "flex-start" as const,
    gap: 12,
  },
};

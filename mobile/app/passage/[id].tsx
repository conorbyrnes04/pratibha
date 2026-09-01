import { LayerContent } from "@/components/LayerContent";
import { PratibhaScreen, stackScreenEdges } from "@/components/ui/PratibhaScreen";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { getVerse } from "@/lib/api";
import { upsertJournalNote } from "@/lib/storage";
import { getStudyLayers, layerText, passagePreview, practiceText } from "@/lib/verseLayers";
import { colors } from "@/constants/theme";
import { isChapterSummaryMetaUnit } from "@shared/corpusFilters";
import { displayCollectionName } from "@shared/collectionLabels";
import { displayPassageTitle } from "@shared/passageTitles";
import type { PratibhaLayerKind, VerseItem } from "@shared/types";
import { stripMarkdown } from "@shared/textPreview";
import { useLocalSearchParams, router } from "expo-router";
import { useEffect, useMemo, useState } from "react";
import { ActivityIndicator, Pressable, ScrollView, TextInput, View, Keyboard } from "react-native";
import * as Haptics from "expo-haptics";

const TAB_ORDER: PratibhaLayerKind[] = [
  "translation",
  "commentary",
  "practice",
  "original",
  "iast",
  "key_terms",
  "resonances",
];

function reflectionPrompt(item: VerseItem): string {
  const t = (item.themes || [])[0];
  if (t) return `How does "${t}" show up in your life today?`;
  return "What changes if this passage is treated as instruction, not just information?";
}

export default function PassageScreen() {
  const params = useLocalSearchParams<{ id: string }>();
  const [item, setItem] = useState<VerseItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeLayer, setActiveLayer] = useState<PratibhaLayerKind>("translation");
  const [reflection, setReflection] = useState("");
  const [savedReflection, setSavedReflection] = useState(false);
  const [showGuide, setShowGuide] = useState(false);

  const id = typeof params.id === "string" ? decodeURIComponent(params.id) : "";

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    getVerse(id)
      .then(setItem)
      .finally(() => setLoading(false));
  }, [id]);

  useEffect(() => {
    if (!item) return;
    setActiveLayer(isChapterSummaryMetaUnit(item) ? "commentary" : "translation");
  }, [item?._id]);

  const layers = useMemo(() => {
    if (!item) return [];
    const study = getStudyLayers(item);
    return TAB_ORDER.map((kind) => study.find((l) => l.kind === kind)).filter(Boolean) as typeof study;
  }, [item]);

  useEffect(() => {
    if (layers.length > 0 && !layers.some((l) => l.kind === activeLayer)) {
      setActiveLayer(layers[0].kind);
    }
  }, [layers, activeLayer]);

  const currentLayer = layers.find((l) => l.kind === activeLayer);

  const learningGuide = useMemo(() => {
    if (!item) return null;
    const translation = stripMarkdown(layerText(item, "translation"));
    const commentary = stripMarkdown(layerText(item, "commentary"));
    const coreIdea =
      stripMarkdown(item.thesis || "") ||
      translation.split(/(?<=[.!?])\s+/)[0]?.trim() ||
      passagePreview(item);
    const why =
      stripMarkdown(item.source_excerpt || "") ||
      commentary.split(/(?<=[.!?])\s+/)[0]?.trim() ||
      "This passage asks for slower reading so the practical move is clear.";
    return {
      coreIdea,
      why,
      practice: practiceText(item) || "Read once slowly, then pause for one minute before your next action.",
      reflect: reflectionPrompt(item),
    };
  }, [item]);

  async function saveReflection() {
    if (!item) return;
    const clean = reflection.trim();
    if (!clean) return;
    await upsertJournalNote({
      passage: item,
      body: clean,
      prompt: learningGuide?.reflect,
    });
    setReflection("");
    Keyboard.dismiss();
    setSavedReflection(true);
    void Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    setTimeout(() => setSavedReflection(false), 2000);
  }

  if (loading) {
    return (
      <PratibhaScreen scroll={false} edges={stackScreenEdges}>
        <ActivityIndicator color={colors.accent} />
      </PratibhaScreen>
    );
  }

  if (!item) {
    return (
      <PratibhaScreen edges={stackScreenEdges}>
        <PratibhaText variant="soft">Passage not found.</PratibhaText>
      </PratibhaScreen>
    );
  }

  return (
    <PratibhaScreen edges={stackScreenEdges}>
      <PratibhaText variant="label">{displayCollectionName(item.collection)}</PratibhaText>
      <PratibhaText variant="title" style={{ marginTop: 8, fontSize: 28 }}>
        {displayPassageTitle(item)}
      </PratibhaText>
      {isChapterSummaryMetaUnit(item) ? (
        <PratibhaText variant="label" style={{ marginTop: 6, color: colors.muted2 }}>
          Section overview
        </PratibhaText>
      ) : null}

      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        style={{ marginTop: 16 }}
        contentContainerStyle={{ gap: 8 }}
      >
        {layers.map((layer) => (
          <Pressable
            key={layer.kind}
            style={[
              ui.buttonGhost,
              activeLayer === layer.kind && {
                borderColor: colors.borderStrong,
                backgroundColor: "rgba(240,201,121,0.08)",
              },
            ]}
          onPress={() => {
            void Haptics.selectionAsync();
            setActiveLayer(layer.kind);
          }}
          >
            <PratibhaText
              style={[
                ui.buttonGhostText,
                activeLayer === layer.kind && { color: colors.accentBright },
              ]}
            >
              {layer.label.replace(/^Pratibha /, "")}
            </PratibhaText>
          </Pressable>
        ))}
      </ScrollView>

      {currentLayer ? (
        <View style={[ui.card, { marginTop: 12 }]}>
          <PratibhaText variant="eyebrow">{currentLayer.label}</PratibhaText>
          <LayerContent layer={currentLayer} compact={currentLayer.kind === "commentary"} />
        </View>
      ) : null}

      <View style={{ marginTop: 20, gap: 10, flexDirection: "row", flexWrap: "wrap" }}>
        <Pressable
          style={ui.button}
          onPress={() =>
            router.push({
              pathname: "/ask",
              params: { verse_id: item._id, mode: "explain", q: "Guide me through this passage." },
            } as never)
          }
        >
          <PratibhaText style={ui.buttonText}>Ask about this</PratibhaText>
        </Pressable>
        <Pressable style={ui.buttonGhost} onPress={() => router.push("/(tabs)/manuscript" as never)}>
          <PratibhaText style={ui.buttonGhostText}>Mine</PratibhaText>
        </Pressable>
      </View>

      {learningGuide ? (
        <Pressable
          style={[ui.card, { marginTop: 16 }]}
          onPress={() => setShowGuide((v) => !v)}
        >
          <PratibhaText variant="eyebrow">{showGuide ? "Hide guide" : "Study guide"}</PratibhaText>
          {showGuide ? (
            <View>
              <PratibhaText variant="body" style={{ marginTop: 10, fontSize: 15 }}>
                {learningGuide.coreIdea}
              </PratibhaText>
              <PratibhaText variant="soft" style={{ marginTop: 8, fontSize: 14 }}>
                {learningGuide.why}
              </PratibhaText>
              <PratibhaText variant="soft" style={{ marginTop: 8, fontSize: 14 }}>
                {learningGuide.practice}
              </PratibhaText>
            </View>
          ) : (
            <PratibhaText variant="soft" style={{ marginTop: 8, fontSize: 14 }}>
              Core idea, why it matters, and a practice — tap to open.
            </PratibhaText>
          )}
        </Pressable>
      ) : null}

      <View style={[ui.card, { marginTop: 16 }]}>
        <PratibhaText variant="eyebrow">Save reflection</PratibhaText>
        <PratibhaText variant="soft" style={{ marginTop: 8, fontSize: 14 }}>
          {learningGuide?.reflect}
        </PratibhaText>
        <TextInput
          value={reflection}
          onChangeText={setReflection}
          placeholder="Write a reflection…"
          placeholderTextColor={colors.muted2}
          multiline
          style={{
            marginTop: 10,
            minHeight: 100,
            borderRadius: 16,
            borderWidth: 1,
            borderColor: colors.border,
            padding: 12,
            color: colors.foreground,
            fontSize: 15,
            textAlignVertical: "top",
          }}
        />
        <Pressable
          style={[ui.button, { marginTop: 10, opacity: reflection.trim() ? 1 : 0.45 }]}
          onPress={saveReflection}
          disabled={!reflection.trim()}
        >
          <PratibhaText style={ui.buttonText}>
            {savedReflection ? "Saved ✓" : "Save to journal"}
          </PratibhaText>
        </Pressable>
      </View>
    </PratibhaScreen>
  );
}

import { FilterSelectSheet } from "@/components/FilterSelectSheet";
import { ThemeConstellation } from "@/components/ThemeConstellation";
import { PratibhaScreen } from "@/components/ui/PratibhaScreen";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { useStudy } from "@/context/StudyContext";
import { passagePreview } from "@/lib/passages";
import { layerText } from "@/lib/verseLayers";
import {
  buildCollectionOptions,
  filterPassages,
  topThemes,
  uniqueCollections,
} from "@shared/corpusFilters";
import { displayCollectionName } from "@shared/collectionLabels";
import { router } from "expo-router";
import { useMemo, useState } from "react";
import { Pressable, TextInput, View } from "react-native";
import { colors } from "@/constants/theme";

export default function ReadTab() {
  const { items, loading, refreshCorpus } = useStudy();
  const [q, setQ] = useState("");
  const [collection, setCollection] = useState("all");
  const [theme, setTheme] = useState("all");

  const library = useMemo(
    () => items.filter((x) => x.editorial_maturity !== "needs_rewrite" && x.editorial_maturity !== "structural_draft"),
    [items],
  );

  const collections = useMemo(() => uniqueCollections(library), [library]);
  const collectionOptions = useMemo(() => buildCollectionOptions(library, collections), [library, collections]);
  const themeConstellation = useMemo(() => topThemes(library, 14), [library]);

  const filtered = useMemo(
    () =>
      filterPassages(library, {
        q,
        collection,
        theme,
        blob: (x) =>
          [x.title, x.sutra_id, x.collection, layerText(x, "translation"), layerText(x, "commentary")].join(" "),
      }).slice(0, 80),
    [library, q, collection, theme],
  );

  return (
    <PratibhaScreen onRefresh={refreshCorpus} refreshing={loading}>
      <PratibhaText variant="eyebrow">Library</PratibhaText>
      <PratibhaText variant="title" style={{ marginTop: 8 }}>
        Read
      </PratibhaText>

      <TextInput
        value={q}
        onChangeText={setQ}
        placeholder="Search passages…"
        placeholderTextColor={colors.muted2}
        style={{
          marginTop: 16,
          borderRadius: 18,
          borderWidth: 1,
          borderColor: colors.border,
          paddingHorizontal: 14,
          paddingVertical: 12,
          color: colors.foreground,
          fontSize: 16,
        }}
      />

      <View style={{ marginTop: 14 }}>
        <FilterSelectSheet
          label="Collection"
          tone="gold"
          value={collection}
          onChange={setCollection}
          options={collectionOptions}
        />
      </View>

      <ThemeConstellation themes={themeConstellation} active={theme} onChange={setTheme} />

      <View style={{ marginTop: 16, gap: 10 }}>
        {filtered.map((item) => (
          <Pressable
            key={item._id}
            style={ui.card}
            onPress={() => router.push({ pathname: "/passage/[id]", params: { id: item._id } })}
          >
            <PratibhaText variant="heading" style={{ fontSize: 18 }}>
              {item.title || item.sutra_id || item._id}
            </PratibhaText>
            <PratibhaText variant="label" style={{ marginTop: 4 }}>
              {displayCollectionName(item.collection)}
            </PratibhaText>
            <PratibhaText variant="soft" style={{ marginTop: 6, fontSize: 14 }} numberOfLines={2}>
              {passagePreview(item)}
            </PratibhaText>
          </Pressable>
        ))}
      </View>
    </PratibhaScreen>
  );
}

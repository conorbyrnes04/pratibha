import { FilterSelectSheet } from "@/components/FilterSelectSheet";
import { ThemeConstellation } from "@/components/ThemeConstellation";
import { PratibhaScreen } from "@/components/ui/PratibhaScreen";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { useStudy } from "@/context/StudyContext";
import { passagePreview, pickRandomPassage } from "@/lib/passages";
import { layerText } from "@/lib/verseLayers";
import {
  buildCollectionOptions,
  filterPassages,
  topThemes,
  uniqueCollections,
} from "@shared/corpusFilters";
import { displayCollectionName } from "@shared/collectionLabels";
import { displayPassageTitle } from "@shared/passageTitles";
import { router } from "expo-router";
import { useCallback, useMemo, useState } from "react";
import { Pressable, TextInput, View, Keyboard } from "react-native";
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

  const openRandomPassage = useCallback(() => {
    const item = pickRandomPassage(library, collection);
    if (!item) return;
    router.push({ pathname: "/passage/[id]", params: { id: item._id } });
  }, [library, collection]);

  return (
    <PratibhaScreen onRefresh={refreshCorpus} refreshing={loading}>
      <PratibhaText variant="eyebrow">Library</PratibhaText>
      <PratibhaText variant="title" style={{ marginTop: 8 }}>
        The house
      </PratibhaText>
      <PratibhaText variant="soft" style={{ marginTop: 8 }}>
        Browse the corpus. Open a passage to read, ask, or keep a note.
      </PratibhaText>

      <TextInput
        value={q}
        onChangeText={setQ}
        placeholder="Search passages…"
        placeholderTextColor={colors.muted2}
        returnKeyType="search"
        onSubmitEditing={Keyboard.dismiss}
        blurOnSubmit
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

      <View style={{ marginTop: 14, flexDirection: "row", alignItems: "flex-end", gap: 10 }}>
        <View style={{ flex: 1 }}>
          <FilterSelectSheet
            label="Collection"
            tone="gold"
            value={collection}
            onChange={setCollection}
            options={collectionOptions}
          />
        </View>
        {collection !== "all" ? (
          <Pressable style={ui.button} onPress={openRandomPassage}>
            <PratibhaText style={ui.buttonText}>Random</PratibhaText>
          </Pressable>
        ) : null}
      </View>

      <ThemeConstellation themes={themeConstellation} active={theme} onChange={setTheme} />

      <View style={{ marginTop: 16, gap: 10 }}>
        {filtered.length === 0 ? (
          <View style={ui.card}>
            <PratibhaText variant="soft">
              {loading ? "Loading the house…" : "No passages match. Try another collection or clear the search."}
            </PratibhaText>
          </View>
        ) : (
          filtered.map((item) => (
          <Pressable
            key={item._id}
            style={ui.card}
            onPress={() => router.push({ pathname: "/passage/[id]", params: { id: item._id } })}
          >
            <PratibhaText variant="heading" style={{ fontSize: 18 }}>
              {displayPassageTitle(item)}
            </PratibhaText>
            <PratibhaText variant="label" style={{ marginTop: 4 }}>
              {displayCollectionName(item.collection)}
            </PratibhaText>
            <PratibhaText variant="soft" style={{ marginTop: 6, fontSize: 14 }} numberOfLines={2}>
              {passagePreview(item)}
            </PratibhaText>
          </Pressable>
          ))
        )}
      </View>
    </PratibhaScreen>
  );
}

import { FilterSelectSheet } from "@/components/FilterSelectSheet";
import { ThemeConstellation } from "@/components/ThemeConstellation";
import { PratibhaScreen } from "@/components/ui/PratibhaScreen";
import { PratibhaText, useUi } from "@/components/ui/PratibhaText";
import { useStudy } from "@/context/StudyContext";
import { useTheme } from "@/context/ThemeContext";
import { passagePreview, pickRandomPassage } from "@/lib/passages";
import { layerText } from "@/lib/verseLayers";
import { webAsset } from "@/lib/webAssets";
import {
  buildCollectionOptions,
  filterPassages,
  topThemes,
  uniqueCollections,
} from "@shared/corpusFilters";
import { displayCollectionName } from "@shared/collectionLabels";
import { collectionImageSlug, generatedSrc, redbookSlug, redbookSrc } from "@shared/collectionImages";
import {
  buildLibraryTomes,
  groupTomesByTradition,
  sortTomes,
  type LibraryTome,
} from "@shared/libraryTomes";
import { displayPassageTitle } from "@shared/passageTitles";
import { LinearGradient } from "expo-linear-gradient";
import { router } from "expo-router";
import { useCallback, useMemo, useState } from "react";
import { Image, Keyboard, Pressable, TextInput, View } from "react-native";

/** Absolute URL of a tome's illuminated art: Red Book first, else its thangka. */
function tomeArtUrl(collection: string): string {
  const rb = redbookSlug(collection);
  if (rb) return webAsset(redbookSrc(rb));
  return webAsset(generatedSrc(collectionImageSlug(collection)));
}

function TomeCard({ tome, onOpen }: { tome: LibraryTome; onOpen: () => void }) {
  const ui = useUi();
  const { colors } = useTheme();
  const [artFailed, setArtFailed] = useState(false);
  const art = tomeArtUrl(tome.collection);

  return (
    <Pressable
      onPress={onOpen}
      style={({ pressed }) => [
        ui.card,
        {
          padding: 0,
          overflow: "hidden",
          borderColor: colors.borderStrong,
          opacity: pressed ? 0.92 : 1,
        },
      ]}
    >
      <View style={{ height: 150, backgroundColor: colors.surfaceSoft }}>
        {artFailed ? (
          <LinearGradient
            colors={[colors.surfaceSoft, colors.backgroundWarm]}
            style={{ flex: 1, alignItems: "center", justifyContent: "center" }}
          >
            <PratibhaText variant="title" style={{ fontSize: 44, opacity: 0.5 }}>
              {tome.displayName.slice(0, 1)}
            </PratibhaText>
          </LinearGradient>
        ) : (
          <Image
            source={{ uri: art }}
            resizeMode="cover"
            onError={() => setArtFailed(true)}
            style={{ width: "100%", height: "100%" }}
          />
        )}
        <LinearGradient
          colors={["transparent", "rgba(8,8,14,0.35)", "rgba(8,8,14,0.92)"]}
          style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 96, justifyContent: "flex-end", padding: 14 }}
        >
          <PratibhaText variant="heading" style={{ fontSize: 20, color: "#f0c979" }} numberOfLines={2}>
            {tome.displayName}
          </PratibhaText>
          {tome.author ? (
            <PratibhaText style={{ marginTop: 2, fontSize: 13, color: "rgba(243,234,216,0.9)" }} numberOfLines={1}>
              {tome.author}
            </PratibhaText>
          ) : null}
        </LinearGradient>
      </View>
      <View
        style={{
          flexDirection: "row",
          justifyContent: "space-between",
          alignItems: "center",
          paddingHorizontal: 14,
          paddingVertical: 10,
        }}
      >
        <PratibhaText variant="label">{tome.tradition}</PratibhaText>
        <PratibhaText variant="label">
          {tome.count} {tome.count === 1 ? "passage" : "passages"} · {tome.authored}
        </PratibhaText>
      </View>
    </Pressable>
  );
}

export default function ReadTab() {
  const ui = useUi();
  const { colors } = useTheme();
  const { items, loading, error, refreshCorpus } = useStudy();
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

  // Grouped shelf of illuminated tomes — shown when browsing (no search / no text picked).
  const shelves = useMemo(() => {
    const tomes = buildLibraryTomes(library);
    const themed =
      theme === "all"
        ? tomes
        : tomes.filter((tome) =>
            library.some((item) => item.collection === tome.collection && (item.themes || []).includes(theme)),
          );
    return groupTomesByTradition(sortTomes(themed, "tradition"));
  }, [library, theme]);

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

  const showShelf = collection === "all" && !q.trim();
  const totalTomes = useMemo(() => shelves.reduce((n, s) => n + s.tomes.length, 0), [shelves]);

  const openRandomPassage = useCallback(() => {
    const item = pickRandomPassage(library, collection);
    if (!item) return;
    router.push({ pathname: "/passage/[id]", params: { id: item._id } });
  }, [library, collection]);

  return (
    <PratibhaScreen onRefresh={refreshCorpus} refreshing={loading}>
      <PratibhaText variant="eyebrow">Library</PratibhaText>
      <PratibhaText variant="title" style={{ marginTop: 8 }}>
        {collection === "all" ? "The house" : displayCollectionName(collection)}
      </PratibhaText>
      <PratibhaText variant="soft" style={{ marginTop: 8 }}>
        {collection === "all"
          ? "The living manuscript, shelf by shelf. Open a tome to read, ask, or keep a note."
          : "Open a passage to read, ask, or keep a note."}
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

      {showShelf ? (
        <View style={{ marginTop: 18 }}>
          {totalTomes === 0 ? (
            error && !loading ? (
              <View style={ui.card}>
                <PratibhaText variant="heading" style={{ fontSize: 18, color: colors.rose }}>
                  Couldn’t reach the library
                </PratibhaText>
                <PratibhaText variant="soft" style={{ marginTop: 8, fontSize: 14 }}>
                  The library server may be waking up. Give it a moment and try again.
                </PratibhaText>
                <Pressable style={[ui.button, { marginTop: 12 }]} onPress={() => void refreshCorpus()}>
                  <PratibhaText style={ui.buttonText}>Try again</PratibhaText>
                </Pressable>
              </View>
            ) : (
              <View style={ui.card}>
                <PratibhaText variant="soft">
                  {loading ? "Opening the house… (the server may be waking up)" : "No texts match this theme. Clear the filter to see the full shelf."}
                </PratibhaText>
              </View>
            )
          ) : (
            <>
              <PratibhaText variant="label">
                {totalTomes} {totalTomes === 1 ? "text" : "texts"} · {library.length} passages
              </PratibhaText>
              {shelves.map((shelf) => (
                <View key={shelf.tradition} style={{ marginTop: 22 }}>
                  <View
                    style={{
                      flexDirection: "row",
                      justifyContent: "space-between",
                      alignItems: "baseline",
                      marginBottom: 12,
                    }}
                  >
                    <PratibhaText variant="eyebrow">{shelf.tradition}</PratibhaText>
                    <PratibhaText variant="label">
                      {shelf.tomes.length} {shelf.tomes.length === 1 ? "text" : "texts"}
                    </PratibhaText>
                  </View>
                  <View style={{ gap: 14 }}>
                    {shelf.tomes.map((tome) => (
                      <TomeCard key={tome.collection} tome={tome} onOpen={() => setCollection(tome.collection)} />
                    ))}
                  </View>
                </View>
              ))}
            </>
          )}
        </View>
      ) : (
        <View style={{ marginTop: 16, gap: 10 }}>
          {collection !== "all" ? (
            <Pressable onPress={() => setCollection("all")} style={{ alignSelf: "flex-start", marginBottom: 4 }}>
              <PratibhaText variant="label" style={{ color: colors.accentBright }}>
                ← All texts
              </PratibhaText>
            </Pressable>
          ) : null}
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
      )}
    </PratibhaScreen>
  );
}

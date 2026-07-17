import { PratibhaScreen } from "@/components/ui/PratibhaScreen";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { getDaily } from "@/lib/api";
import { passagePreview, practiceText } from "@/lib/verseLayers";
import { useStudy } from "@/context/StudyContext";
import { displayCollectionName } from "@shared/collectionLabels";
import { displayPassageTitle } from "@shared/passageTitles";
import type { VerseItem } from "@shared/types";
import { Link, router } from "expo-router";
import { useCallback, useEffect, useMemo, useState } from "react";
import { Pressable, View } from "react-native";
import { colors } from "@/constants/theme";

export default function HomeTab() {
  const { items } = useStudy();
  const [daily, setDaily] = useState<VerseItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [dailyError, setDailyError] = useState(false);

  const library = useMemo(
    () =>
      items.filter(
        (x) => x.editorial_maturity !== "needs_rewrite" && x.editorial_maturity !== "structural_draft",
      ),
    [items],
  );

  const loadDaily = useCallback(() => {
    setLoading(true);
    setDailyError(false);
    getDaily("strong_draft")
      .then((v) => {
        setDaily(v);
        if (!v) setDailyError(true);
      })
      .catch(() => {
        setDaily(null);
        setDailyError(true);
      })
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    loadDaily();
  }, [loadDaily]);

  function drawOracle() {
    if (library.length === 0) return;
    const item = library[Math.floor(Math.random() * library.length)];
    router.push({ pathname: "/passage/[id]", params: { id: item._id } });
  }

  const dailyTitle = daily ? displayPassageTitle(daily) : "A passage is waiting";
  const dailyCollection = displayCollectionName(daily?.collection);
  const dailyLine = daily ? passagePreview(daily) : "";
  const dailyPractice =
    (daily ? practiceText(daily) : "") ||
    "Read slowly, then carry one line into the next action.";

  return (
    <PratibhaScreen onRefresh={loadDaily} refreshing={loading}>
      <View style={styles.header}>
        <View>
          <PratibhaText variant="eyebrow">Pratibha</PratibhaText>
          <PratibhaText variant="title" style={{ marginTop: 8 }}>
            Home
          </PratibhaText>
        </View>
        <Link href="/settings" asChild>
          <Pressable style={ui.buttonGhost}>
            <PratibhaText style={ui.buttonGhostText}>API</PratibhaText>
          </Pressable>
        </Link>
      </View>

      {dailyError && !loading ? (
        <View style={[ui.card, { marginTop: 20, borderColor: "rgba(253,164,175,0.35)" }]}>
          <PratibhaText variant="heading" style={{ fontSize: 18, color: colors.rose }}>
            Couldn&apos;t load today&apos;s passage
          </PratibhaText>
          <PratibhaText variant="soft" style={{ marginTop: 8 }}>
            Check that the API is running and reachable from this device.
          </PratibhaText>
          <View style={{ marginTop: 14, flexDirection: "row", gap: 10, flexWrap: "wrap" }}>
            <Pressable style={ui.button} onPress={loadDaily}>
              <PratibhaText style={ui.buttonText}>Retry</PratibhaText>
            </Pressable>
            <Link href="/settings" asChild>
              <Pressable style={ui.buttonGhost}>
                <PratibhaText style={ui.buttonGhostText}>Settings</PratibhaText>
              </Pressable>
            </Link>
          </View>
        </View>
      ) : (
        <View style={[ui.card, ui.cardGold, { marginTop: 20 }]}>
          <PratibhaText variant="eyebrow">Today&apos;s passage</PratibhaText>
          <PratibhaText variant="heading" style={{ marginTop: 12, fontSize: 26, lineHeight: 32 }}>
            {dailyTitle}
          </PratibhaText>
          <PratibhaText variant="label" style={{ marginTop: 8 }}>
            {dailyCollection || "Pratibha corpus"}
          </PratibhaText>
          <PratibhaText variant="body" style={{ marginTop: 16, fontSize: 18, lineHeight: 28 }}>
            {dailyLine || "Open a passage, let it read you back, then practice one concrete shift."}
          </PratibhaText>
          <View style={[ui.card, { marginTop: 16, backgroundColor: "rgba(0,0,0,0.22)" }]}>
            <PratibhaText variant="label">Practice</PratibhaText>
            <PratibhaText variant="soft" style={{ marginTop: 8, fontSize: 15, lineHeight: 22 }}>
              {dailyPractice}
            </PratibhaText>
          </View>
          <View style={{ marginTop: 16, flexDirection: "row", flexWrap: "wrap", gap: 10 }}>
            {daily ? (
              <Pressable
                style={ui.button}
                onPress={() => router.push({ pathname: "/passage/[id]", params: { id: daily._id } })}
              >
                <PratibhaText style={ui.buttonText}>Read passage</PratibhaText>
              </Pressable>
            ) : null}
            <Pressable
              style={ui.buttonGhost}
              onPress={() =>
                router.push(
                  daily
                    ? { pathname: "/(tabs)/chat", params: { verse_id: daily._id } }
                    : { pathname: "/(tabs)/chat" },
                )
              }
            >
              <PratibhaText style={ui.buttonGhostText}>Ask about it</PratibhaText>
            </Pressable>
          </View>
        </View>
      )}

      <Pressable style={[ui.card, { marginTop: 12 }]} onPress={drawOracle} disabled={library.length === 0}>
        <PratibhaText variant="label">Oracle</PratibhaText>
        <PratibhaText variant="heading" style={{ marginTop: 8, fontSize: 20 }}>
          Draw a passage
        </PratibhaText>
        <PratibhaText variant="soft" style={{ marginTop: 6, fontSize: 14 }}>
          Let the corpus choose — open a random passage from the library.
        </PratibhaText>
      </Pressable>

      <PratibhaText variant="eyebrow" style={{ marginTop: 28 }}>
        Ways in
      </PratibhaText>
      <View style={{ marginTop: 12, gap: 10 }}>
        {[
          { href: "/(tabs)/read" as const, title: "Archive", label: "Enter the Library", copy: "Browse by tradition, passage, and theme." },
          { href: "/(tabs)/chat" as const, title: "Dialogue", label: "Ask Pratibha", copy: "Question the texts and ask for practice." },
          { href: "/(tabs)/paths" as const, title: "Curriculum", label: "Follow a Path", copy: "Guided sequences from concept to embodiment." },
          { href: "/(tabs)/journal" as const, title: "Memory", label: "Your Journal", copy: "Reflections saved on this device." },
        ].map((gateway) => (
          <Link key={gateway.href} href={gateway.href} asChild>
            <Pressable style={ui.card}>
              <PratibhaText variant="label">{gateway.title}</PratibhaText>
              <PratibhaText variant="heading" style={{ marginTop: 8, fontSize: 20 }}>
                {gateway.label}
              </PratibhaText>
              <PratibhaText variant="soft" style={{ marginTop: 6, fontSize: 14 }}>
                {gateway.copy}
              </PratibhaText>
            </Pressable>
          </Link>
        ))}
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

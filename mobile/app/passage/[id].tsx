import { PratibhaScreen } from "@/components/ui/PratibhaScreen";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { getVerse } from "@/lib/api";
import { layerText } from "@/lib/passages";
import { getVerseLayers } from "@/lib/verseLayers";
import { useLocalSearchParams } from "expo-router";
import { useEffect, useState } from "react";
import { ActivityIndicator, View } from "react-native";
import type { VerseItem } from "@shared/types";
import { colors } from "@/constants/theme";

export default function PassageScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const [item, setItem] = useState<VerseItem | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    getVerse(decodeURIComponent(id))
      .then(setItem)
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <PratibhaScreen scroll={false}>
        <ActivityIndicator color={colors.accent} />
      </PratibhaScreen>
    );
  }

  if (!item) {
    return (
      <PratibhaScreen>
        <PratibhaText variant="soft">Passage not found.</PratibhaText>
      </PratibhaScreen>
    );
  }

  const layers = getVerseLayers(item).filter((l) =>
    ["translation", "commentary", "practice", "original", "iast"].includes(l.kind),
  );

  return (
    <PratibhaScreen>
      <PratibhaText variant="label">{item.collection}</PratibhaText>
      <PratibhaText variant="title" style={{ marginTop: 8, fontSize: 28 }}>
        {item.title || item.sutra_id || item._id}
      </PratibhaText>

      {layers.map((layer) => (
        <View key={layer.kind} style={[ui.card, { marginTop: 16 }]}>
          <PratibhaText variant="eyebrow">{layer.label}</PratibhaText>
          <PratibhaText variant="body" style={{ marginTop: 10, fontSize: 16 }}>
            {layer.body || layerText(item, layer.kind)}
          </PratibhaText>
        </View>
      ))}
    </PratibhaScreen>
  );
}

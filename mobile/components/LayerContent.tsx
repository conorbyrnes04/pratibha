import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { MarkdownBody } from "@/components/MarkdownBody";
import type { KeyTerm, PratibhaLayer, Resonance } from "@shared/types";
import { View } from "react-native";

function isKeyTerm(item: unknown): item is KeyTerm {
  return Boolean(item && typeof item === "object" && "term" in item && "definition" in item);
}

function isResonance(item: unknown): item is Resonance {
  return Boolean(item && typeof item === "object" && "citation" in item && "resonance" in item);
}

type Props = {
  layer: PratibhaLayer;
  compact?: boolean;
};

export function LayerContent({ layer, compact }: Props) {
  const items = Array.isArray(layer.items) ? layer.items : [];

  if (layer.kind === "key_terms" && items.some(isKeyTerm)) {
    return (
      <View style={{ marginTop: 10, gap: 10 }}>
        {items.filter(isKeyTerm).map((term) => (
          <View key={term.term} style={[ui.card, { padding: 12, marginTop: 0 }]}>
            <PratibhaText variant="heading" style={{ fontSize: 18 }}>
              {term.term}
            </PratibhaText>
            <PratibhaText variant="soft" style={{ marginTop: 6, fontSize: 14 }}>
              {term.definition}
            </PratibhaText>
          </View>
        ))}
      </View>
    );
  }

  if (layer.kind === "resonances" && items.some(isResonance)) {
    return (
      <View style={{ marginTop: 10, gap: 10 }}>
        {items.filter(isResonance).map((entry) => (
          <View key={entry.citation} style={[ui.card, { padding: 12, marginTop: 0 }]}>
            <PratibhaText variant="heading" style={{ fontSize: 18 }}>
              {entry.citation}
            </PratibhaText>
            <PratibhaText variant="soft" style={{ marginTop: 6, fontSize: 14 }}>
              {entry.resonance}
            </PratibhaText>
            {entry.divergence ? (
              <PratibhaText variant="body" style={{ marginTop: 8, fontSize: 14 }}>
                <PratibhaText variant="heading" style={{ fontSize: 14 }}>
                  Divergence:{" "}
                </PratibhaText>
                {entry.divergence}
              </PratibhaText>
            ) : null}
          </View>
        ))}
      </View>
    );
  }

  return (
    <View style={{ marginTop: 10 }}>
      <MarkdownBody compact={compact}>{layer.body || ""}</MarkdownBody>
    </View>
  );
}

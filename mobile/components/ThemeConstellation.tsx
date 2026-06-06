import { PratibhaText } from "@/components/ui/PratibhaText";
import { colors } from "@/constants/theme";
import type { ThemeCount } from "@shared/corpusFilters";
import { Pressable, ScrollView, StyleSheet, View } from "react-native";

type ThemeConstellationProps = {
  themes: ThemeCount[];
  active: string;
  onChange: (theme: string) => void;
};

export function ThemeConstellation({ themes, active, onChange }: ThemeConstellationProps) {
  if (themes.length === 0) return null;

  return (
    <View style={{ marginTop: 16 }}>
      <PratibhaText variant="label">Theme constellation</PratibhaText>
      <PratibhaText variant="soft" style={{ marginTop: 4, fontSize: 13 }}>
        Most frequent threads — swipe to explore.
      </PratibhaText>
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.track}
        style={{ marginTop: 10 }}
      >
        <Pressable
          onPress={() => onChange("all")}
          style={[styles.bead, active === "all" && styles.beadActive]}
        >
          <PratibhaText style={[styles.beadText, active === "all" && styles.beadTextActive]}>
            All themes
          </PratibhaText>
        </Pressable>
        {themes.map(({ theme, count }) => (
          <Pressable
            key={theme}
            onPress={() => onChange(theme)}
            style={[styles.bead, active === theme && styles.beadActive]}
          >
            <PratibhaText style={[styles.beadText, active === theme && styles.beadTextActive]}>
              {theme}
            </PratibhaText>
            <PratibhaText style={styles.count}>{count}</PratibhaText>
          </Pressable>
        ))}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  track: {
    gap: 8,
    paddingRight: 8,
  },
  bead: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    borderWidth: 1,
    borderColor: "rgba(90, 120, 160, 0.4)",
    borderRadius: 999,
    paddingHorizontal: 14,
    paddingVertical: 8,
    backgroundColor: "rgba(50, 72, 103, 0.18)",
  },
  beadActive: {
    borderColor: "rgba(148, 176, 210, 0.65)",
    backgroundColor: "rgba(50, 72, 103, 0.32)",
  },
  beadText: {
    color: "#c4d2e6",
    fontSize: 13,
    letterSpacing: 0.4,
  },
  beadTextActive: {
    color: "#e6eef8",
  },
  count: {
    color: colors.muted2,
    fontSize: 10,
    letterSpacing: 1,
    textTransform: "uppercase",
  },
});

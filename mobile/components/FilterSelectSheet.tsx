import { PratibhaText } from "@/components/ui/PratibhaText";
import { colors } from "@/constants/theme";
import type { CollectionFilterOption } from "@shared/corpusFilters";
import { useState } from "react";
import { Modal, Pressable, ScrollView, StyleSheet, View } from "react-native";

type FilterSelectSheetProps = {
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: CollectionFilterOption[];
  tone?: "gold" | "lapis";
};

export function FilterSelectSheet({ label, value, onChange, options, tone = "gold" }: FilterSelectSheetProps) {
  const [open, setOpen] = useState(false);
  const selected = options.find((option) => option.value === value);
  const accent = tone === "lapis" ? "#94b0d2" : colors.accentBright;
  const border = tone === "lapis" ? "rgba(90, 120, 160, 0.45)" : colors.borderStrong;

  return (
    <View>
      <PratibhaText variant="label" style={{ marginBottom: 6 }}>
        {label}
      </PratibhaText>
      <Pressable
        onPress={() => setOpen(true)}
        style={[styles.trigger, { borderColor: border }]}
      >
        <View style={styles.triggerRow}>
          {selected?.icon ? (
            <PratibhaText style={styles.optionIcon}>{selected.icon}</PratibhaText>
          ) : null}
          <PratibhaText variant="body" style={{ flex: 1, fontSize: 17 }}>
            {selected?.label || "Choose…"}
          </PratibhaText>
          <PratibhaText style={{ color: accent, fontSize: 12 }}>▾</PratibhaText>
        </View>
      </Pressable>

      <Modal visible={open} transparent animationType="slide" onRequestClose={() => setOpen(false)}>
        <Pressable style={styles.backdrop} onPress={() => setOpen(false)}>
          <Pressable style={styles.sheet} onPress={(e) => e.stopPropagation()}>
            <View style={styles.handle} />
            <PratibhaText variant="heading" style={{ fontSize: 22, marginBottom: 12 }}>
              {label}
            </PratibhaText>
            <ScrollView style={{ maxHeight: 360 }}>
              {options.map((option) => {
                const active = option.value === value;
                return (
                  <Pressable
                    key={option.value}
                    onPress={() => {
                      onChange(option.value);
                      setOpen(false);
                    }}
                    style={[
                      styles.option,
                      active && { borderColor: accent, backgroundColor: "rgba(240, 201, 121, 0.1)" },
                    ]}
                  >
                    <View style={styles.optionRow}>
                      {option.icon ? (
                        <PratibhaText style={styles.optionIcon}>{option.icon}</PratibhaText>
                      ) : null}
                      <PratibhaText variant="body" style={{ flex: 1, fontSize: 17 }}>
                        {option.label}
                      </PratibhaText>
                      {option.hint ? (
                        <PratibhaText variant="label" style={{ fontSize: 10 }}>
                          {option.hint}
                        </PratibhaText>
                      ) : null}
                    </View>
                  </Pressable>
                );
              })}
            </ScrollView>
          </Pressable>
        </Pressable>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  trigger: {
    borderWidth: 1,
    borderRadius: 18,
    paddingHorizontal: 14,
    paddingVertical: 12,
    backgroundColor: "rgba(0,0,0,0.28)",
  },
  triggerRow: {
    flexDirection: "row",
    alignItems: "center",
  },
  optionIcon: {
    width: 22,
    minWidth: 22,
    fontSize: 18,
    lineHeight: 22,
    textAlign: "center",
    fontFamily: "System",
    marginRight: 10,
  },
  backdrop: {
    flex: 1,
    justifyContent: "flex-end",
    backgroundColor: "rgba(0,0,0,0.55)",
  },
  sheet: {
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    borderWidth: 1,
    borderColor: colors.border,
    paddingHorizontal: 18,
    paddingTop: 10,
    paddingBottom: 28,
    backgroundColor: colors.surface,
  },
  handle: {
    alignSelf: "center",
    width: 42,
    height: 4,
    marginBottom: 14,
    borderRadius: 999,
    backgroundColor: colors.borderStrong,
  },
  option: {
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 14,
    paddingHorizontal: 12,
    paddingVertical: 12,
    marginBottom: 8,
    backgroundColor: "rgba(0,0,0,0.2)",
  },
  optionRow: {
    flexDirection: "row",
    alignItems: "center",
  },
});

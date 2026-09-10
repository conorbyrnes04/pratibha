import { LinearGradient } from "expo-linear-gradient";
import { ReactNode } from "react";
import { Keyboard, RefreshControl, ScrollView, StyleSheet, View, type ViewStyle, useWindowDimensions } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useTheme } from "@/context/ThemeContext";

type Edge = "top" | "bottom" | "left" | "right";

type Props = {
  children: ReactNode;
  scroll?: boolean;
  onRefresh?: () => void;
  refreshing?: boolean;
  contentStyle?: ViewStyle;
  /** Tab roots need top inset. Stack screens already have a nav header — omit top. */
  edges?: Edge[];
};

export const stackScreenEdges: Edge[] = ["left", "right"];

export function PratibhaScreen({
  children,
  scroll = true,
  onRefresh,
  refreshing,
  contentStyle,
  edges = ["top", "left", "right"],
}: Props) {
  const { colors, scheme } = useTheme();
  const { width } = useWindowDimensions();
  const tablet = width >= 700;
  const contentMax: ViewStyle = tablet
    ? { maxWidth: 720, width: "100%", alignSelf: "center" }
    : {};

  const body = scroll ? (
    <ScrollView
      contentContainerStyle={[styles.content, contentMax, contentStyle]}
      showsVerticalScrollIndicator={false}
      keyboardShouldPersistTaps="handled"
      keyboardDismissMode="on-drag"
      onScrollBeginDrag={Keyboard.dismiss}
      refreshControl={
        onRefresh ? (
          <RefreshControl refreshing={!!refreshing} onRefresh={onRefresh} tintColor={colors.accent} />
        ) : undefined
      }
    >
      {children}
    </ScrollView>
  ) : (
    <View style={[styles.content, contentMax, contentStyle, { flex: 1 }]}>{children}</View>
  );

  return (
    <View style={[styles.root, { backgroundColor: colors.background }]}>
      {scheme === "ink" ? (
        <LinearGradient colors={[...colors.gradient]} style={StyleSheet.absoluteFill} />
      ) : null}
      <SafeAreaView style={styles.safe} edges={edges}>
        {body}
      </SafeAreaView>
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1 },
  safe: { flex: 1 },
  content: { paddingHorizontal: 20, paddingBottom: 32 },
});

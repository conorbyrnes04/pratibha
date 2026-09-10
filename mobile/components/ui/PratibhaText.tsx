import { useTheme } from "@/context/ThemeContext";
import { fonts, type ColorTokens } from "@/constants/theme";
import { useMemo } from "react";
import { StyleSheet, Text, type TextProps } from "react-native";

type Variant = "eyebrow" | "title" | "heading" | "body" | "soft" | "label";

type Props = TextProps & { variant?: Variant };

function variantStyles(colors: ColorTokens): Record<Variant, object> {
  return {
    eyebrow: {
      fontFamily: fonts.sans,
      fontSize: 11,
      letterSpacing: 2.2,
      textTransform: "uppercase",
      color: colors.accentBright,
      opacity: 0.85,
    },
    title: {
      fontFamily: fonts.serif,
      fontSize: 34,
      lineHeight: 38,
      color: colors.foreground,
      fontWeight: "600",
    },
    heading: {
      fontFamily: fonts.serif,
      fontSize: 24,
      lineHeight: 28,
      color: colors.accentBright,
      fontWeight: "600",
    },
    body: {
      fontFamily: fonts.serif,
      fontSize: 17,
      lineHeight: 26,
      color: colors.foreground,
    },
    soft: {
      fontFamily: fonts.serif,
      fontSize: 16,
      lineHeight: 24,
      color: colors.muted,
    },
    label: {
      fontFamily: fonts.sans,
      fontSize: 11,
      letterSpacing: 1.6,
      textTransform: "uppercase",
      color: colors.muted2,
    },
  };
}

export function PratibhaText({ variant = "body", style, ...props }: Props) {
  const { colors } = useTheme();
  const variants = useMemo(() => variantStyles(colors), [colors]);
  return <Text style={[variants[variant], style]} {...props} />;
}

export function makeUi(colors: ColorTokens) {
  return StyleSheet.create({
    card: {
      borderRadius: 20,
      borderWidth: 1,
      borderColor: colors.border,
      backgroundColor: colors.cardFill,
      padding: 16,
    },
    cardGold: {
      borderColor: colors.borderStrong,
      backgroundColor: colors.cardGoldFill,
    },
    button: {
      borderRadius: 999,
      backgroundColor: colors.accent,
      paddingHorizontal: 20,
      paddingVertical: 12,
      alignSelf: "flex-start",
    },
    buttonText: {
      fontFamily: fonts.sans,
      fontSize: 13,
      fontWeight: "700",
      letterSpacing: 1.2,
      textTransform: "uppercase",
      color: colors.buttonInk,
    },
    buttonGhost: {
      borderRadius: 999,
      borderWidth: 1,
      borderColor: colors.border,
      paddingHorizontal: 16,
      paddingVertical: 10,
      alignSelf: "flex-start",
    },
    buttonGhostText: {
      fontFamily: fonts.sans,
      fontSize: 12,
      letterSpacing: 1,
      textTransform: "uppercase",
      color: colors.accentBright,
    },
    progressTrack: {
      height: 8,
      borderRadius: 999,
      backgroundColor: colors.cardFill,
      overflow: "hidden",
    },
    progressFill: {
      height: 8,
      borderRadius: 999,
      backgroundColor: colors.accentBright,
    },
  });
}

export function useUi() {
  const { colors } = useTheme();
  return useMemo(() => makeUi(colors), [colors]);
}

/** Ink-theme fallback for modules that cannot call hooks. Prefer `useUi()`. */
export const ui = makeUi(paletteSafe());

function paletteSafe() {
  return {
    background: "#090912",
    backgroundWarm: "#13101a",
    surface: "#171421",
    surfaceSoft: "#211a2a",
    foreground: "#f3ead8",
    muted: "#b9ad98",
    muted2: "#897d6c",
    accent: "#d8a84a",
    accentBright: "#f0c979",
    emerald: "#6ee7b7",
    rose: "#fda4af",
    border: "rgba(240, 201, 121, 0.18)",
    borderStrong: "rgba(240, 201, 121, 0.4)",
    cardFill: "rgba(0,0,0,0.25)",
    cardGoldFill: "rgba(240, 201, 121, 0.08)",
    buttonInk: "#1a1208",
    statusBar: "light" as const,
    navBar: "light-content" as const,
    gradient: ["#07070d", "#11101a", "#17101a"] as const,
  };
}

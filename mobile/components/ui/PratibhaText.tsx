import { StyleSheet, Text, type TextProps } from "react-native";
import { colors, fonts } from "@/constants/theme";

type Variant = "eyebrow" | "title" | "heading" | "body" | "soft" | "label";

type Props = TextProps & { variant?: Variant };

const variantStyles: Record<Variant, object> = {
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

export function PratibhaText({ variant = "body", style, ...props }: Props) {
  return <Text style={[variantStyles[variant], style]} {...props} />;
}

export const ui = StyleSheet.create({
  card: {
    borderRadius: 20,
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: "rgba(0,0,0,0.25)",
    padding: 16,
  },
  cardGold: {
    borderColor: colors.borderStrong,
    backgroundColor: "rgba(240, 201, 121, 0.08)",
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
    color: "#1a1208",
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
    backgroundColor: "rgba(255,255,255,0.08)",
    overflow: "hidden",
  },
  progressFill: {
    height: 8,
    borderRadius: 999,
    backgroundColor: colors.accentBright,
  },
});

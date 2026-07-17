import { colors } from "@/constants/theme";
import { LinearGradient } from "expo-linear-gradient";
import { useEffect } from "react";
import { StyleSheet, View, type ViewStyle } from "react-native";
import Animated, {
  Easing,
  useAnimatedStyle,
  useSharedValue,
  withRepeat,
  withTiming,
} from "react-native-reanimated";
import { PratibhaText } from "@/components/ui/PratibhaText";

export type PathOrbState = "complete" | "highlight" | "active" | "default";

type Props = {
  label: string;
  state: PathOrbState;
  size?: number;
  style?: ViewStyle;
};

const ORB = 48;

function orbPalette(state: PathOrbState) {
  switch (state) {
    case "complete":
      return {
        border: "rgba(110, 231, 183, 0.85)",
        gradient: ["rgba(110, 231, 183, 0.95)", "rgba(52, 211, 153, 0.75)"] as const,
        text: "#0f172a",
        glow: "rgba(110, 231, 183, 0.25)",
        pulse: false,
        ring: false,
      };
    case "highlight":
      return {
        border: colors.accentBright,
        gradient: [colors.accentBright, "#e8b85a"] as const,
        text: "#0f172a",
        glow: "rgba(240, 201, 121, 0.35)",
        pulse: true,
        ring: true,
      };
    case "active":
      return {
        border: "rgba(240, 201, 121, 0.7)",
        gradient: ["rgba(240, 201, 121, 0.22)", "rgba(11, 11, 20, 0.92)"] as const,
        text: colors.accentBright,
        glow: "rgba(240, 201, 121, 0.28)",
        pulse: false,
        ring: true,
      };
    default:
      return {
        border: "rgba(240, 201, 121, 0.28)",
        gradient: ["rgba(240, 201, 121, 0.08)", "rgba(11, 11, 20, 0.88)"] as const,
        text: "rgba(254, 243, 199, 0.92)",
        glow: "rgba(240, 201, 121, 0.12)",
        pulse: false,
        ring: false,
      };
  }
}

export function PathOrb({ label, state, size = ORB, style }: Props) {
  const palette = orbPalette(state);
  const pulseOpacity = useSharedValue(0);
  const pulseScale = useSharedValue(0.92);

  useEffect(() => {
    if (!palette.pulse) {
      pulseOpacity.value = 0;
      pulseScale.value = 1;
      return;
    }
    pulseOpacity.value = withRepeat(
      withTiming(0.38, { duration: 2000, easing: Easing.inOut(Easing.ease) }),
      -1,
      true,
    );
    pulseScale.value = withRepeat(
      withTiming(1.1, { duration: 2000, easing: Easing.inOut(Easing.ease) }),
      -1,
      true,
    );
  }, [palette.pulse, pulseOpacity, pulseScale]);

  const pulseStyle = useAnimatedStyle(() => ({
    opacity: pulseOpacity.value,
    transform: [{ scale: pulseScale.value }],
  }));

  const outer = size + (palette.ring ? 14 : 0);

  return (
    <View style={[styles.wrap, { width: outer, height: outer }, style]}>
      {palette.ring ? (
        <View
          pointerEvents="none"
          style={[
            styles.ring,
            {
              width: size + 12,
              height: size + 12,
              borderRadius: (size + 12) / 2,
              borderColor: "rgba(240, 201, 121, 0.14)",
              shadowColor: colors.accentBright,
              shadowOpacity: state === "highlight" ? 0.45 : 0.28,
              shadowRadius: state === "highlight" ? 18 : 14,
            },
          ]}
        />
      ) : null}

      <Animated.View
        pointerEvents="none"
        style={[
          styles.glow,
          pulseStyle,
          {
            width: size * 1.35,
            height: size * 1.35,
            borderRadius: (size * 1.35) / 2,
            backgroundColor: palette.glow,
          },
        ]}
      />

      <LinearGradient
        colors={[...palette.gradient]}
        style={[
          styles.orb,
          {
            width: size,
            height: size,
            borderRadius: size / 2,
            borderColor: palette.border,
            shadowColor: colors.accentBright,
            shadowOpacity: palette.ring ? 0.35 : 0.15,
            shadowRadius: palette.ring ? 12 : 6,
          },
        ]}
      >
        <PratibhaText style={[styles.label, { color: palette.text, fontSize: size > 44 ? 15 : 14 }]}>
          {label}
        </PratibhaText>
      </LinearGradient>
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: {
    alignItems: "center",
    justifyContent: "center",
  },
  ring: {
    position: "absolute",
    borderWidth: 3,
    shadowOffset: { width: 0, height: 0 },
    elevation: 6,
  },
  glow: {
    position: "absolute",
  },
  orb: {
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 2,
    shadowOffset: { width: 0, height: 0 },
    elevation: 4,
    overflow: "hidden",
  },
  label: {
    fontFamily: "System",
    fontWeight: "700",
    letterSpacing: 0.2,
  },
});

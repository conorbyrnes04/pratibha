import { Platform } from "react-native";

export type ThemeName = "ink" | "paper";

export type ColorTokens = {
  background: string;
  backgroundWarm: string;
  surface: string;
  surfaceSoft: string;
  foreground: string;
  muted: string;
  muted2: string;
  accent: string;
  accentBright: string;
  emerald: string;
  rose: string;
  border: string;
  borderStrong: string;
  cardFill: string;
  cardGoldFill: string;
  buttonInk: string;
  statusBar: "light" | "dark";
  navBar: "light-content" | "dark-content";
  gradient: readonly [string, string, string];
};

export const inkColors: ColorTokens = {
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
  statusBar: "light",
  navBar: "light-content",
  gradient: ["#07070d", "#11101a", "#17101a"],
};

/** High-contrast cream page for e-ink (Boox) and anyone who wants paper. */
export const paperColors: ColorTokens = {
  background: "#f4ead8",
  backgroundWarm: "#efe4ce",
  surface: "#fff8ec",
  surfaceSoft: "#e8dcc4",
  foreground: "#1a140c",
  muted: "#5c5143",
  muted2: "#6e6254",
  accent: "#8a5a14",
  accentBright: "#6b4310",
  emerald: "#1f6b4a",
  rose: "#9b2c2c",
  border: "rgba(26, 20, 12, 0.22)",
  borderStrong: "rgba(26, 20, 12, 0.45)",
  cardFill: "rgba(255, 255, 255, 0.55)",
  cardGoldFill: "rgba(138, 90, 20, 0.08)",
  buttonInk: "#f4ead8",
  statusBar: "dark",
  navBar: "dark-content",
  gradient: ["#f4ead8", "#f4ead8", "#efe4ce"],
};

/** Dark manuscript tokens — default face of the app. */
export const colors = inkColors;

export const fonts = {
  serif: Platform.select({ ios: "Georgia", android: "serif", default: "Georgia" }) as string,
  sans: Platform.select({ ios: "System", android: "sans-serif", default: "System" }) as string,
  mono: Platform.select({ ios: "Menlo", android: "monospace", default: "Menlo" }) as string,
} as const;

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
} as const;

export function paletteFor(name: ThemeName): ColorTokens {
  return name === "paper" ? paperColors : inkColors;
}

/** Onyx/Boox and other reflective readers prefer Paper. */
export function detectEink(): boolean {
  if (Platform.OS !== "android") return false;
  const c = Platform.constants as { Brand?: string; Manufacturer?: string; Model?: string };
  const blob = [c.Brand, c.Manufacturer, c.Model].filter(Boolean).join(" ").toLowerCase();
  return /onyx|boox|noteair|palma|novaair|leaf|hisense|dasung|meebook|likebook/.test(blob);
}

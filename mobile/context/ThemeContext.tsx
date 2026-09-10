import { detectEink, paletteFor, type ColorTokens, type ThemeName } from "@/constants/theme";
import { THEME_KEY } from "@/lib/storage";
import AsyncStorage from "@react-native-async-storage/async-storage";
import * as NavigationBar from "expo-navigation-bar";
import { StatusBar } from "expo-status-bar";
import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { Platform } from "react-native";

type ThemeContextValue = {
  scheme: ThemeName;
  colors: ColorTokens;
  eink: boolean;
  reduceMotion: boolean;
  setScheme: (name: ThemeName) => void;
};

const ThemeContext = createContext<ThemeContextValue | null>(null);

export function AppThemeProvider({ children }: { children: ReactNode }) {
  const eink = detectEink();
  const [scheme, setSchemeState] = useState<ThemeName>(eink ? "paper" : "ink");

  useEffect(() => {
    AsyncStorage.getItem(THEME_KEY).then((v) => {
      if (v === "ink" || v === "paper") setSchemeState(v);
    });
  }, []);

  const colors = useMemo(() => paletteFor(scheme), [scheme]);

  useEffect(() => {
    if (Platform.OS !== "android") return;
    void NavigationBar.setBackgroundColorAsync(colors.background).catch(() => undefined);
    void NavigationBar.setButtonStyleAsync(scheme === "paper" ? "dark" : "light").catch(() => undefined);
  }, [colors.background, scheme]);

  function setScheme(name: ThemeName) {
    setSchemeState(name);
    void AsyncStorage.setItem(THEME_KEY, name);
  }

  const value = useMemo<ThemeContextValue>(
    () => ({
      scheme,
      colors,
      eink,
      reduceMotion: scheme === "paper" || eink,
      setScheme,
    }),
    [scheme, colors, eink],
  );

  return (
    <ThemeContext.Provider value={value}>
      <StatusBar style={colors.statusBar} backgroundColor={colors.background} />
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme(): ThemeContextValue {
  const ctx = useContext(ThemeContext);
  if (!ctx) {
    return {
      scheme: "ink",
      colors: paletteFor("ink"),
      eink: false,
      reduceMotion: false,
      setScheme: () => undefined,
    };
  }
  return ctx;
}

import { StudyProvider } from "@/context/StudyContext";
import { colors } from "@/constants/theme";
import { DarkTheme, ThemeProvider } from "@react-navigation/native";
import { Stack } from "expo-router";
import * as SplashScreen from "expo-splash-screen";
import { useEffect } from "react";
import { StatusBar } from "expo-status-bar";
import { SafeAreaProvider } from "react-native-safe-area-context";

export { ErrorBoundary } from "expo-router";

SplashScreen.preventAutoHideAsync();

const pratibhaTheme = {
  ...DarkTheme,
  colors: {
    ...DarkTheme.colors,
    background: colors.background,
    card: colors.surface,
    text: colors.foreground,
    border: colors.border,
    primary: colors.accent,
  },
};

export default function RootLayout() {
  useEffect(() => {
    SplashScreen.hideAsync();
  }, []);

  return (
    <SafeAreaProvider>
      <StudyProvider>
        <ThemeProvider value={pratibhaTheme}>
          <StatusBar style="light" />
          <Stack
            screenOptions={{
              headerStyle: { backgroundColor: colors.background },
              headerTintColor: colors.accentBright,
              headerTitleStyle: { fontFamily: "Georgia" },
              contentStyle: { backgroundColor: colors.background },
            }}
          >
            <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
            <Stack.Screen name="path/[id]" options={{ title: "Path" }} />
            <Stack.Screen name="step/[trackId]/[stepId]" options={{ title: "Gate" }} />
            <Stack.Screen name="passage/[id]" options={{ title: "Passage" }} />
            <Stack.Screen name="settings" options={{ presentation: "modal", title: "Settings" }} />
          </Stack>
        </ThemeProvider>
      </StudyProvider>
    </SafeAreaProvider>
  );
}

import { AuthProvider } from "@/context/AuthContext";
import { CloudSync } from "@/context/CloudSync";
import { StudyProvider } from "@/context/StudyContext";
import { AppThemeProvider, useTheme } from "@/context/ThemeContext";
import { fonts } from "@/constants/theme";
import { DarkTheme, DefaultTheme, ThemeProvider } from "@react-navigation/native";
import { Stack } from "expo-router";
import * as SplashScreen from "expo-splash-screen";
import { useEffect } from "react";
import { SafeAreaProvider } from "react-native-safe-area-context";

export { ErrorBoundary } from "expo-router";

SplashScreen.preventAutoHideAsync();

function NavigationTree() {
  const { colors, scheme } = useTheme();
  const navTheme = {
    ...(scheme === "paper" ? DefaultTheme : DarkTheme),
    colors: {
      ...(scheme === "paper" ? DefaultTheme.colors : DarkTheme.colors),
      background: colors.background,
      card: colors.surface,
      text: colors.foreground,
      border: colors.border,
      primary: colors.accent,
    },
  };

  return (
    <ThemeProvider value={navTheme}>
      <Stack
        screenOptions={{
          headerStyle: { backgroundColor: colors.background },
          headerTintColor: colors.accentBright,
          headerTitleStyle: { fontFamily: fonts.serif },
          headerShadowVisible: false,
          contentStyle: { backgroundColor: colors.background },
          animation: scheme === "paper" ? "none" : "default",
        }}
      >
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="ask" options={{ title: "Ask", headerBackTitle: "Back" }} />
        <Stack.Screen name="path/[id]" options={{ title: "Path", headerBackTitle: "Back" }} />
        <Stack.Screen name="step/[trackId]/[stepId]" options={{ title: "Gate", headerBackTitle: "Back" }} />
        <Stack.Screen name="passage/[id]" options={{ title: "Passage", headerBackTitle: "Back" }} />
        <Stack.Screen name="settings" options={{ presentation: "modal", title: "Settings" }} />
        <Stack.Screen name="login" options={{ title: "Sign in", headerBackTitle: "Back" }} />
      </Stack>
    </ThemeProvider>
  );
}

export default function RootLayout() {
  useEffect(() => {
    SplashScreen.hideAsync();
  }, []);

  return (
    <SafeAreaProvider>
      <AppThemeProvider>
        <AuthProvider>
          <CloudSync>
            <StudyProvider>
              <NavigationTree />
            </StudyProvider>
          </CloudSync>
        </AuthProvider>
      </AppThemeProvider>
    </SafeAreaProvider>
  );
}

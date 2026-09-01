import { colors } from "@/constants/theme";
import { SymbolView } from "expo-symbols";
import { Tabs } from "expo-router";
import { Keyboard } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

export default function TabLayout() {
  const insets = useSafeAreaInsets();
  const tabBarHeight = 56 + insets.bottom;

  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarHideOnKeyboard: true,
        tabBarStyle: {
          backgroundColor: colors.background,
          borderTopColor: colors.border,
          height: tabBarHeight,
          paddingBottom: Math.max(insets.bottom, 8),
          paddingTop: 8,
        },
        tabBarActiveTintColor: colors.accentBright,
        tabBarInactiveTintColor: colors.muted2,
        tabBarLabelStyle: {
          fontSize: 10,
          letterSpacing: 1.2,
          textTransform: "uppercase",
        },
      }}
      screenListeners={{
        tabPress: () => {
          Keyboard.dismiss();
        },
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: "Today",
          tabBarIcon: ({ color }) => (
            <SymbolView name={"sun.max.fill" as never} tintColor={color} size={24} />
          ),
        }}
      />
      <Tabs.Screen
        name="paths"
        options={{
          title: "Path",
          tabBarIcon: ({ color }) => (
            <SymbolView
              name={"point.3.connected.trianglepath.dotted" as never}
              tintColor={color}
              size={24}
            />
          ),
        }}
      />
      <Tabs.Screen
        name="read"
        options={{
          title: "Library",
          tabBarIcon: ({ color }) => (
            <SymbolView name={"book.closed.fill" as never} tintColor={color} size={24} />
          ),
        }}
      />
      <Tabs.Screen
        name="manuscript"
        options={{
          title: "Mine",
          tabBarIcon: ({ color }) => (
            <SymbolView name={"bookmark.fill" as never} tintColor={color} size={24} />
          ),
        }}
      />
      <Tabs.Screen name="journal" options={{ href: null }} />
      <Tabs.Screen name="chat" options={{ href: null }} />
    </Tabs>
  );
}

import { PratibhaIcon } from "@/components/PratibhaIcon";
import { useTheme } from "@/context/ThemeContext";
import { Tabs } from "expo-router";
import { Keyboard } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

export default function TabLayout() {
  const insets = useSafeAreaInsets();
  const { colors } = useTheme();
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
          tabBarIcon: ({ color }) => <PratibhaIcon name="today" color={color} size={24} />,
        }}
      />
      <Tabs.Screen
        name="paths"
        options={{
          title: "Path",
          tabBarIcon: ({ color }) => <PratibhaIcon name="path" color={color} size={24} />,
        }}
      />
      <Tabs.Screen
        name="read"
        options={{
          title: "Library",
          tabBarIcon: ({ color }) => <PratibhaIcon name="library" color={color} size={24} />,
        }}
      />
      <Tabs.Screen
        name="circle"
        options={{
          title: "Circle",
          tabBarIcon: ({ color }) => <PratibhaIcon name="circle" color={color} size={24} />,
        }}
      />
      <Tabs.Screen
        name="manuscript"
        options={{
          title: "Manuscript",
          tabBarIcon: ({ color }) => <PratibhaIcon name="mine" color={color} size={24} />,
        }}
      />
      <Tabs.Screen name="journal" options={{ href: null }} />
      <Tabs.Screen name="chat" options={{ href: null }} />
    </Tabs>
  );
}

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
          backgroundColor: "#0b0b14",
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
          title: "Home",
          tabBarIcon: ({ color }) => (
            <SymbolView name={{ ios: "house.fill", android: "home", web: "home" }} tintColor={color} size={24} />
          ),
        }}
      />
      <Tabs.Screen
        name="journal"
        options={{
          title: "Journal",
          tabBarIcon: ({ color }) => (
            <SymbolView name={{ ios: "square.and.pencil", android: "edit_note", web: "edit_note" }} tintColor={color} size={24} />
          ),
        }}
      />
      <Tabs.Screen
        name="chat"
        options={{
          title: "Study",
          tabBarIcon: ({ color }) => (
            <SymbolView name={{ ios: "bubble.left.and.bubble.right.fill", android: "forum", web: "forum" }} tintColor={color} size={24} />
          ),
        }}
      />
      <Tabs.Screen
        name="read"
        options={{
          title: "Read",
          tabBarIcon: ({ color }) => (
            <SymbolView name={{ ios: "book.closed.fill", android: "menu_book", web: "menu_book" }} tintColor={color} size={24} />
          ),
        }}
      />
      <Tabs.Screen
        name="paths"
        options={{
          title: "Paths",
          tabBarIcon: ({ color }) => (
            <SymbolView
              name={{ ios: "point.3.filled.connected.trianglepath.dotted", android: "route", web: "route" }}
              tintColor={color}
              size={24}
            />
          ),
        }}
      />
    </Tabs>
  );
}

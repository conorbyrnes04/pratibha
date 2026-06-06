import { colors } from "@/constants/theme";
import { SymbolView } from "expo-symbols";
import { Tabs } from "expo-router";

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarStyle: {
          backgroundColor: "#0b0b14",
          borderTopColor: colors.border,
          height: 84,
          paddingBottom: 18,
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
    >
      <Tabs.Screen
        name="index"
        options={{
          title: "Paths",
          tabBarIcon: ({ color }) => (
            <SymbolView name={{ ios: "point.3.filled.connected.trianglepath.dotted", android: "route", web: "route" }} tintColor={color} size={24} />
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
    </Tabs>
  );
}

import { Ionicons } from "@expo/vector-icons";
import type { ComponentProps } from "react";

type IonName = ComponentProps<typeof Ionicons>["name"];

const TAB_ICONS = {
  today: "sunny",
  path: "git-network-outline",
  library: "book",
  circle: "people-circle-outline",
  mine: "bookmark",
} as const;

const ACTION_ICONS = {
  gear: "settings-outline",
  ask: "chatbubble-ellipses",
  search: "search",
} as const;

export const symbols = ACTION_ICONS;

export function PratibhaIcon({
  name,
  color,
  size = 22,
}: {
  name: IonName | keyof typeof TAB_ICONS | keyof typeof ACTION_ICONS;
  color: string;
  size?: number;
}) {
  const mapped =
    name in TAB_ICONS
      ? TAB_ICONS[name as keyof typeof TAB_ICONS]
      : name in ACTION_ICONS
        ? ACTION_ICONS[name as keyof typeof ACTION_ICONS]
        : (name as IonName);
  return <Ionicons name={mapped} color={color} size={size} />;
}

export function tabIcon(name: keyof typeof TAB_ICONS): IonName {
  return TAB_ICONS[name];
}

import { colors } from "@/constants/theme";
import { SymbolView } from "expo-symbols";
import { Link, type Href } from "expo-router";
import { Pressable, type StyleProp, type ViewStyle } from "react-native";
import * as Haptics from "expo-haptics";

type Props = {
  name: string;
  accessibilityLabel: string;
  href?: Href;
  onPress?: () => void;
  style?: StyleProp<ViewStyle>;
};

export function IconButton({ name, accessibilityLabel, href, onPress, style }: Props) {
  const inner = (
    <Pressable
      accessibilityLabel={accessibilityLabel}
      hitSlop={12}
      style={style}
      onPress={() => {
        void Haptics.selectionAsync();
        onPress?.();
      }}
    >
      <SymbolView name={name as never} tintColor={colors.accentBright} size={22} />
    </Pressable>
  );

  if (href) {
    return (
      <Link href={href} asChild>
        {inner}
      </Link>
    );
  }
  return inner;
}

export const symbols = {
  gear: "gearshape",
  ask: "bubble.left.fill",
  search: "magnifyingglass",
} as const;

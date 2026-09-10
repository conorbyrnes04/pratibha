import { PratibhaIcon, symbols } from "@/components/PratibhaIcon";
import { useTheme } from "@/context/ThemeContext";
import { Link, type Href } from "expo-router";
import { Pressable, type StyleProp, type ViewStyle } from "react-native";
import * as Haptics from "expo-haptics";

type Props = {
  name: keyof typeof symbols | string;
  accessibilityLabel: string;
  href?: Href;
  onPress?: () => void;
  style?: StyleProp<ViewStyle>;
};

export function IconButton({ name, accessibilityLabel, href, onPress, style }: Props) {
  const { colors } = useTheme();
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
      <PratibhaIcon name={name as keyof typeof symbols} color={colors.accentBright} size={22} />
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

export { symbols };

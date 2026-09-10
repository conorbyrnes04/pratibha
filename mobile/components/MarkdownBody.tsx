import { useTheme } from "@/context/ThemeContext";
import { fonts } from "@/constants/theme";
import Markdown from "react-native-markdown-display";
import { useMemo } from "react";
import { StyleSheet } from "react-native";

type Props = {
  children: string;
  compact?: boolean;
};

export function MarkdownBody({ children, compact }: Props) {
  const { colors } = useTheme();
  const styles = useMemo(() => {
    const baseBody = {
      fontFamily: fonts.serif,
      fontSize: compact ? 15 : 16,
      lineHeight: compact ? 24 : 26,
      color: colors.foreground,
    };
    return StyleSheet.create({
      body: baseBody,
      paragraph: { marginTop: 0, marginBottom: 8 },
      heading1: { ...baseBody, fontSize: 22, color: colors.accentBright, marginBottom: 8 },
      heading2: { ...baseBody, fontSize: 20, color: colors.accentBright, marginBottom: 6 },
      heading3: { ...baseBody, fontSize: 18, color: colors.accentBright, marginBottom: 4 },
      strong: { color: colors.accentBright, fontWeight: "600" },
      em: { fontStyle: "italic" },
      bullet_list: { marginBottom: 8 },
      ordered_list: { marginBottom: 8 },
      list_item: { marginBottom: 4 },
      blockquote: {
        borderLeftWidth: 3,
        borderLeftColor: colors.borderStrong,
        paddingLeft: 12,
        marginVertical: 8,
        opacity: 0.9,
      },
      code_inline: {
        fontFamily: fonts.mono,
        fontSize: 14,
        backgroundColor: colors.cardFill,
        color: colors.accentBright,
      },
      fence: {
        backgroundColor: colors.cardFill,
        padding: 10,
        borderRadius: 8,
        marginVertical: 8,
      },
      link: { color: colors.accent },
    });
  }, [colors, compact]);

  return <Markdown style={styles}>{children || ""}</Markdown>;
}

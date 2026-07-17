import { colors } from "@/constants/theme";
import Markdown from "react-native-markdown-display";
import { StyleSheet } from "react-native";

type Props = {
  children: string;
  compact?: boolean;
};

export function MarkdownBody({ children, compact }: Props) {
  return (
    <Markdown style={compact ? compactStyles : styles}>
      {children || ""}
    </Markdown>
  );
}

const baseBody = {
  fontFamily: "Georgia",
  fontSize: 16,
  lineHeight: 26,
  color: colors.foreground,
};

const styles = StyleSheet.create({
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
    fontFamily: "Menlo",
    fontSize: 14,
    backgroundColor: "rgba(0,0,0,0.3)",
    color: colors.accentBright,
  },
  fence: {
    backgroundColor: "rgba(0,0,0,0.3)",
    padding: 10,
    borderRadius: 8,
    marginVertical: 8,
  },
  link: { color: colors.accent },
});

const compactStyles = StyleSheet.create({
  ...styles,
  body: { ...baseBody, fontSize: 15, lineHeight: 24 },
});

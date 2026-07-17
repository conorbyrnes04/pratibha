import { MarkdownBody } from "@/components/MarkdownBody";
import { PratibhaScreen } from "@/components/ui/PratibhaScreen";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { askChat, getVerse } from "@/lib/api";
import { saveChatResponse } from "@/lib/storage";
import { passagePreview } from "@/lib/verseLayers";
import { colors } from "@/constants/theme";
import { displayCollectionName } from "@shared/collectionLabels";
import { displayPassageTitle } from "@shared/passageTitles";
import type { ChatMode, VerseItem } from "@shared/types";
import * as Clipboard from "expo-clipboard";
import * as Haptics from "expo-haptics";
import { useLocalSearchParams, router } from "expo-router";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  ActivityIndicator,
  FlatList,
  Keyboard,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  TextInput,
  View,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

type Msg = { role: "user" | "assistant"; content: string };

const CHAT_MODES: { value: ChatMode; label: string }[] = [
  { value: "question", label: "Question" },
  { value: "explain", label: "Explain" },
  { value: "practice", label: "Practice" },
  { value: "compare", label: "Compare" },
];

function parseChatMode(raw: unknown): ChatMode {
  if (typeof raw === "string" && ["question", "explain", "compare", "practice"].includes(raw)) {
    return raw as ChatMode;
  }
  return "question";
}

export default function ChatTab() {
  const params = useLocalSearchParams<{ q?: string; verse_id?: string; mode?: string }>();
  const insets = useSafeAreaInsets();
  const listRef = useRef<FlatList<Msg>>(null);
  const inputRef = useRef<TextInput>(null);

  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [savedReplies, setSavedReplies] = useState<Set<number>>(new Set());
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);
  const [pinnedVerse, setPinnedVerse] = useState<VerseItem | null>(null);
  const [chatMode, setChatMode] = useState<ChatMode>("question");
  const copiedTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const verseId = typeof params.verse_id === "string" ? params.verse_id : "";

  useEffect(() => {
    if (typeof params.q === "string" && params.q.trim()) {
      setInput(params.q);
    }
  }, [params.q]);

  useEffect(() => {
    setChatMode(parseChatMode(params.mode));
  }, [params.mode]);

  useEffect(() => {
    if (!verseId) {
      setPinnedVerse(null);
      return;
    }
    getVerse(verseId).then(setPinnedVerse).catch(() => setPinnedVerse(null));
  }, [verseId]);

  const modeLabel = useMemo(
    () => CHAT_MODES.find((m) => m.value === chatMode)?.label || "Question",
    [chatMode],
  );

  function clearPinned() {
    router.replace({ pathname: "/(tabs)/chat" });
  }

  const copyMessage = useCallback(async (index: number, content: string) => {
    await Clipboard.setStringAsync(content);
    await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    if (copiedTimerRef.current) clearTimeout(copiedTimerRef.current);
    setCopiedIndex(index);
    copiedTimerRef.current = setTimeout(() => setCopiedIndex(null), 2000);
  }, []);

  async function saveReply(index: number, content: string) {
    const question =
      index > 0 && messages[index - 1]?.role === "user" ? messages[index - 1].content : "";
    await saveChatResponse({
      answer: content,
      question,
      verse: pinnedVerse,
      chatMode,
    });
    setSavedReplies((prev) => new Set(prev).add(index));
  }

  async function send() {
    const text = input.trim();
    if (!text || loading) return;
    const next: Msg[] = [...messages, { role: "user", content: text }];
    setMessages(next);
    setInput("");
    inputRef.current?.blur();
    Keyboard.dismiss();
    setLoading(true);
    setError(null);
    try {
      const { answer } = await askChat(next, true, {
        chatMode,
        verseId: pinnedVerse?._id,
      });
      setMessages([...next, { role: "assistant", content: answer }]);
      setTimeout(() => listRef.current?.scrollToEnd({ animated: true }), 100);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Chat failed");
    } finally {
      setLoading(false);
    }
  }

  function renderMessage({ item: m, index: i }: { item: Msg; index: number }) {
    return (
      <Pressable onPress={Keyboard.dismiss}>
        <View style={[ui.card, m.role === "user" && ui.cardGold, { marginBottom: 14 }]}>
        <PratibhaText variant="label">{m.role === "user" ? "You" : "Pratibha"}</PratibhaText>
        {m.role === "assistant" ? (
          <View style={{ marginTop: 8 }}>
            <MarkdownBody>{m.content}</MarkdownBody>
          </View>
        ) : (
          <PratibhaText variant="body" style={{ marginTop: 8, fontSize: 16 }}>
            {m.content}
          </PratibhaText>
        )}
        <View style={{ marginTop: 10, flexDirection: "row", flexWrap: "wrap", gap: 10, alignItems: "center" }}>
          <Pressable style={ui.buttonGhost} onPress={() => copyMessage(i, m.content)}>
            <PratibhaText style={ui.buttonGhostText}>
              {copiedIndex === i ? "Copied" : "Copy"}
            </PratibhaText>
          </Pressable>
          {m.role === "assistant" ? (
            <Pressable
              style={[ui.buttonGhost, { opacity: savedReplies.has(i) ? 0.5 : 1 }]}
              onPress={() => saveReply(i, m.content)}
              disabled={savedReplies.has(i)}
            >
              <PratibhaText style={ui.buttonGhostText}>
                {savedReplies.has(i) ? "Saved to journal" : "Save to journal"}
              </PratibhaText>
            </Pressable>
          ) : null}
        </View>
        </View>
      </Pressable>
    );
  }

  const listHeader = (
    <Pressable onPress={Keyboard.dismiss}>
      <View style={{ paddingBottom: 8 }}>
      <PratibhaText variant="eyebrow">Guided study</PratibhaText>
      <PratibhaText variant="title" style={{ marginTop: 8 }}>
        Study
      </PratibhaText>
      <PratibhaText variant="soft" style={{ marginTop: 8 }}>
        Ask about the corpus. Tap Save on any response to keep it in your journal.
      </PratibhaText>

      {pinnedVerse ? (
        <View style={[ui.card, ui.cardGold, { marginTop: 16 }]}>
          <View style={{ flexDirection: "row", justifyContent: "space-between", alignItems: "flex-start", gap: 8 }}>
            <View style={{ flex: 1 }}>
              <PratibhaText variant="label">Pinned passage</PratibhaText>
              <PratibhaText variant="heading" style={{ marginTop: 6, fontSize: 20 }}>
                {displayPassageTitle(pinnedVerse)}
              </PratibhaText>
              <PratibhaText variant="soft" style={{ marginTop: 4, fontSize: 13 }}>
                {displayCollectionName(pinnedVerse.collection)}
              </PratibhaText>
            </View>
            <Pressable onPress={clearPinned} hitSlop={8}>
              <PratibhaText variant="label" style={{ color: colors.rose }}>
                Clear
              </PratibhaText>
            </Pressable>
          </View>
          <PratibhaText variant="soft" style={{ marginTop: 8, fontSize: 14 }} numberOfLines={3}>
            {passagePreview(pinnedVerse)}
          </PratibhaText>
        </View>
      ) : null}

      <View style={{ marginTop: 14 }}>
        <PratibhaText variant="label">Study mode · {modeLabel}</PratibhaText>
        <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 8, marginTop: 8 }}>
          {CHAT_MODES.map((mode) => (
            <Pressable
              key={mode.value}
              style={[
                ui.buttonGhost,
                chatMode === mode.value && { borderColor: colors.borderStrong, backgroundColor: "rgba(240,201,121,0.08)" },
              ]}
              onPress={() => setChatMode(mode.value)}
            >
              <PratibhaText style={[ui.buttonGhostText, chatMode === mode.value && { color: colors.accentBright }]}>
                {mode.label}
              </PratibhaText>
            </Pressable>
          ))}
        </View>
      </View>
      </View>
    </Pressable>
  );

  return (
    <PratibhaScreen scroll={false} contentStyle={{ paddingBottom: 0, flex: 1 }}>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === "ios" ? "padding" : undefined}
        keyboardVerticalOffset={Platform.OS === "ios" ? insets.top + 8 : 0}
      >
        <FlatList
          ref={listRef}
          data={messages}
          keyExtractor={(_, i) => String(i)}
          renderItem={renderMessage}
          ListHeaderComponent={listHeader}
          ListFooterComponent={
            loading || error ? (
              <View style={{ paddingVertical: 8 }}>
                {loading ? <ActivityIndicator color={colors.accent} /> : null}
                {error ? (
                  <PratibhaText variant="soft" style={{ color: colors.rose, marginTop: 8 }}>
                    {error}
                  </PratibhaText>
                ) : null}
              </View>
            ) : null
          }
          contentContainerStyle={{ paddingBottom: 12 }}
          keyboardShouldPersistTaps="handled"
          keyboardDismissMode="on-drag"
          onScrollBeginDrag={Keyboard.dismiss}
          onContentSizeChange={() => {
            if (messages.length > 0) listRef.current?.scrollToEnd({ animated: false });
          }}
        />

        <View
          style={{
            borderTopWidth: 1,
            borderTopColor: colors.border,
            paddingTop: 10,
            paddingBottom: Math.max(insets.bottom, 12),
            gap: 10,
          }}
        >
          <TextInput
            ref={inputRef}
            value={input}
            onChangeText={setInput}
            placeholder="Ask a question…"
            placeholderTextColor={colors.muted2}
            multiline
            returnKeyType="default"
            blurOnSubmit={false}
            style={{
              minHeight: 72,
              maxHeight: 140,
              borderRadius: 16,
              borderWidth: 1,
              borderColor: colors.border,
              padding: 12,
              color: colors.foreground,
              fontSize: 16,
              textAlignVertical: "top",
            }}
          />
          <Pressable
            style={[ui.button, { opacity: input.trim() && !loading ? 1 : 0.45 }]}
            onPress={send}
            disabled={!input.trim() || loading}
          >
            <PratibhaText style={ui.buttonText}>Send</PratibhaText>
          </Pressable>
        </View>
      </KeyboardAvoidingView>
    </PratibhaScreen>
  );
}

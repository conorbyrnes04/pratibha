import { PratibhaScreen } from "@/components/ui/PratibhaScreen";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { askChat, getVerse } from "@/lib/api";
import { saveChatResponse } from "@/lib/storage";
import { colors } from "@/constants/theme";
import type { VerseItem } from "@shared/types";
import { useLocalSearchParams } from "expo-router";
import { useEffect, useState } from "react";
import { ActivityIndicator, Pressable, TextInput, View } from "react-native";

type Msg = { role: "user" | "assistant"; content: string };

export default function ChatTab() {
  const params = useLocalSearchParams<{ q?: string; verse_id?: string }>();
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [savedReplies, setSavedReplies] = useState<Set<number>>(new Set());
  const [pinnedVerse, setPinnedVerse] = useState<VerseItem | null>(null);

  useEffect(() => {
    if (typeof params.q === "string" && params.q.trim()) {
      setInput(params.q);
    }
  }, [params.q]);

  useEffect(() => {
    const verseId = typeof params.verse_id === "string" ? params.verse_id : "";
    if (!verseId) {
      setPinnedVerse(null);
      return;
    }
    getVerse(verseId).then(setPinnedVerse).catch(() => setPinnedVerse(null));
  }, [params.verse_id]);

  async function saveReply(index: number, content: string) {
    const question =
      index > 0 && messages[index - 1]?.role === "user" ? messages[index - 1].content : "";
    await saveChatResponse({
      answer: content,
      question,
      verse: pinnedVerse,
      chatMode: "explain",
    });
    setSavedReplies((prev) => new Set(prev).add(index));
  }

  async function send() {
    const text = input.trim();
    if (!text || loading) return;
    const next: Msg[] = [...messages, { role: "user", content: text }];
    setMessages(next);
    setInput("");
    setLoading(true);
    setError(null);
    try {
      const { answer } = await askChat(next, true, {
        chatMode: "explain",
        verseId: pinnedVerse?._id,
      });
      setMessages([...next, { role: "assistant", content: answer }]);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Chat failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <PratibhaScreen>
      <PratibhaText variant="eyebrow">Guided study</PratibhaText>
      <PratibhaText variant="title" style={{ marginTop: 8 }}>
        Study Chat
      </PratibhaText>
      <PratibhaText variant="soft" style={{ marginTop: 8 }}>
        Ask about the corpus. Tap Save on any response to keep it in your journal.
      </PratibhaText>

      <View style={{ marginTop: 20, gap: 14 }}>
        {messages.map((m, i) => (
          <View
            key={`${i}-${m.role}`}
            style={[ui.card, m.role === "user" && ui.cardGold]}
          >
            <PratibhaText variant="label">{m.role === "user" ? "You" : "Pratibha"}</PratibhaText>
            <PratibhaText variant="body" style={{ marginTop: 8, fontSize: 16 }}>
              {m.content}
            </PratibhaText>
            {m.role === "assistant" ? (
              <Pressable
                style={[ui.buttonGhost, { marginTop: 10, opacity: savedReplies.has(i) ? 0.5 : 1 }]}
                onPress={() => saveReply(i, m.content)}
                disabled={savedReplies.has(i)}
              >
                <PratibhaText style={ui.buttonGhostText}>
                  {savedReplies.has(i) ? "Saved to journal" : "Save to journal"}
                </PratibhaText>
              </Pressable>
            ) : null}
          </View>
        ))}
        {loading ? <ActivityIndicator color={colors.accent} /> : null}
        {error ? (
          <PratibhaText variant="soft" style={{ color: "#fda4af" }}>
            {error}
          </PratibhaText>
        ) : null}
      </View>

      <View style={{ marginTop: 20, gap: 10 }}>
        <TextInput
          value={input}
          onChangeText={setInput}
          placeholder="Ask a question…"
          placeholderTextColor={colors.muted2}
          multiline
          style={{
            minHeight: 80,
            borderRadius: 16,
            borderWidth: 1,
            borderColor: colors.border,
            padding: 12,
            color: colors.foreground,
            fontSize: 16,
            textAlignVertical: "top",
          }}
        />
        <Pressable style={[ui.button, { opacity: input.trim() && !loading ? 1 : 0.45 }]} onPress={send} disabled={!input.trim() || loading}>
          <PratibhaText style={ui.buttonText}>Send</PratibhaText>
        </Pressable>
      </View>
    </PratibhaScreen>
  );
}

import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { deleteJournalNote, loadJournalNotes } from "@/lib/storage";
import { colors } from "@/constants/theme";
import type { JournalNote } from "@shared/types";
import * as Clipboard from "expo-clipboard";
import * as Haptics from "expo-haptics";
import { useFocusEffect, useRouter } from "expo-router";
import { useCallback, useMemo, useRef, useState } from "react";
import { Pressable, TextInput, View, Keyboard } from "react-native";

function reopenTarget(note: JournalNote): { pathname: string; params?: Record<string, string> } | null {
  if (note.kind === "chat_response" || note.passageId.startsWith("chat:")) {
    const params: Record<string, string> = {};
    if (note.verseId) params.verse_id = note.verseId;
    if (note.question) params.q = note.question;
    if (note.chatMode) params.mode = note.chatMode;
    return Object.keys(params).length > 0 ? { pathname: "/ask", params } : { pathname: "/ask" };
  }
  if (note.passageId.startsWith("learn:")) {
    const [, trackId, stepId] = note.passageId.split(":");
    if (trackId && stepId) {
      return { pathname: "/step/[trackId]/[stepId]", params: { trackId, stepId } };
    }
    return { pathname: "/(tabs)/paths" };
  }
  return { pathname: "/passage/[id]", params: { id: note.passageId } };
}

function reopenLabel(note: JournalNote): string {
  if (note.kind === "chat_response") return "Reopen chat";
  if (note.passageId.startsWith("learn:")) return "Reopen gate";
  return "Open passage";
}

function formatJournalNoteText(note: JournalNote): string {
  const lines = [new Date(note.updatedAt).toLocaleString(), "", note.passageTitle];
  if (note.kind === "chat_response" && note.question) {
    lines.push("", `You asked: ${note.question}`);
  } else if (note.prompt) {
    lines.push("", note.prompt);
  }
  lines.push("", note.body);
  return lines.join("\n");
}

export function JournalFeed() {
  const router = useRouter();
  const [notes, setNotes] = useState<JournalNote[]>([]);
  const [q, setQ] = useState("");
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const copiedTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const refresh = useCallback(() => {
    loadJournalNotes().then((n) => setNotes(n.sort((a, b) => b.updatedAt.localeCompare(a.updatedAt))));
  }, []);

  useFocusEffect(
    useCallback(() => {
      refresh();
    }, [refresh]),
  );

  const filtered = useMemo(() => {
    const needle = q.trim().toLowerCase();
    if (!needle) return notes;
    return notes.filter((note) =>
      [note.passageTitle, note.body, note.prompt, note.tags.join(" ")].join(" ").toLowerCase().includes(needle),
    );
  }, [notes, q]);

  const copyNote = useCallback(async (note: JournalNote) => {
    await Clipboard.setStringAsync(formatJournalNoteText(note));
    await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    if (copiedTimerRef.current) clearTimeout(copiedTimerRef.current);
    setCopiedId(note.id);
    copiedTimerRef.current = setTimeout(() => setCopiedId(null), 2000);
  }, []);

  return (
    <View>
      <TextInput
        value={q}
        onChangeText={setQ}
        placeholder="Search what you kept…"
        placeholderTextColor={colors.muted2}
        returnKeyType="search"
        onSubmitEditing={Keyboard.dismiss}
        blurOnSubmit
        style={{
          marginTop: 16,
          borderRadius: 16,
          borderWidth: 1,
          borderColor: colors.border,
          paddingHorizontal: 14,
          paddingVertical: 12,
          color: colors.foreground,
          fontSize: 16,
        }}
      />

      <View style={{ marginTop: 20, gap: 12 }}>
        {filtered.length === 0 ? (
          <View style={ui.card}>
            <PratibhaText variant="heading" style={{ fontSize: 20 }}>
              {notes.length === 0 ? "Nothing kept yet" : "No matches"}
            </PratibhaText>
            <PratibhaText variant="soft" style={{ marginTop: 8 }}>
              {notes.length === 0
                ? "Finish a gate on Today, or save a reflection from a passage. What you keep gathers here."
                : "Try a different word, or clear the search."}
            </PratibhaText>
          </View>
        ) : (
          filtered.map((note) => {
            const target = reopenTarget(note);
            return (
              <View key={note.id} style={ui.card}>
                <PratibhaText variant="label">{new Date(note.updatedAt).toLocaleDateString()}</PratibhaText>
                <PratibhaText variant="heading" style={{ marginTop: 8, fontSize: 20 }}>
                  {note.passageTitle}
                </PratibhaText>
                {note.kind === "chat_response" && note.question ? (
                  <PratibhaText variant="soft" style={{ marginTop: 6, fontSize: 13 }}>
                    You asked: {note.question}
                  </PratibhaText>
                ) : note.prompt ? (
                  <PratibhaText variant="soft" style={{ marginTop: 6, fontSize: 13 }}>
                    {note.prompt}
                  </PratibhaText>
                ) : null}
                <PratibhaText variant="body" style={{ marginTop: 10, fontSize: 16 }}>
                  {note.body}
                </PratibhaText>
                <View style={{ marginTop: 10, flexDirection: "row", flexWrap: "wrap", gap: 10, alignItems: "center" }}>
                  {target ? (
                    <Pressable style={ui.buttonGhost} onPress={() => router.push(target as never)}>
                      <PratibhaText style={ui.buttonGhostText}>{reopenLabel(note)}</PratibhaText>
                    </Pressable>
                  ) : null}
                  <Pressable style={ui.buttonGhost} onPress={() => copyNote(note)}>
                    <PratibhaText style={ui.buttonGhostText}>{copiedId === note.id ? "Copied" : "Copy"}</PratibhaText>
                  </Pressable>
                  <Pressable
                    onPress={async () => {
                      await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Warning);
                      await deleteJournalNote(note.id);
                      refresh();
                    }}
                  >
                    <PratibhaText variant="label" style={{ color: colors.rose }}>
                      Delete
                    </PratibhaText>
                  </Pressable>
                </View>
              </View>
            );
          })
        )}
      </View>
    </View>
  );
}

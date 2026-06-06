import { PratibhaScreen } from "@/components/ui/PratibhaScreen";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { deleteJournalNote, loadJournalNotes } from "@/lib/storage";
import type { JournalNote } from "@shared/types";
import { useFocusEffect, useRouter } from "expo-router";
import { useCallback, useState } from "react";
import { Pressable, View } from "react-native";

function reopenTarget(note: JournalNote): { pathname: string; params?: Record<string, string> } | null {
  if (note.kind === "chat_response" || note.passageId.startsWith("chat:")) {
    const params: Record<string, string> = {};
    if (note.verseId) params.verse_id = note.verseId;
    if (note.question) params.q = note.question;
    return Object.keys(params).length > 0
      ? { pathname: "/(tabs)/chat", params }
      : { pathname: "/(tabs)/chat" };
  }
  if (note.passageId.startsWith("learn:")) {
    const [, trackId, stepId] = note.passageId.split(":");
    if (trackId && stepId) {
      return { pathname: "/step/[trackId]/[stepId]", params: { trackId, stepId } };
    }
    return { pathname: "/(tabs)/" };
  }
  return { pathname: "/passage/[id]", params: { id: note.passageId } };
}

function reopenLabel(note: JournalNote): string {
  if (note.kind === "chat_response") return "Reopen chat";
  if (note.passageId.startsWith("learn:")) return "Reopen step";
  return "Reopen passage";
}

export default function JournalTab() {
  const router = useRouter();
  const [notes, setNotes] = useState<JournalNote[]>([]);

  const refresh = useCallback(() => {
    loadJournalNotes().then((n) => setNotes(n.sort((a, b) => b.updatedAt.localeCompare(a.updatedAt))));
  }, []);

  useFocusEffect(
    useCallback(() => {
      refresh();
    }, [refresh]),
  );

  return (
    <PratibhaScreen>
      <PratibhaText variant="eyebrow">Personal study memory</PratibhaText>
      <PratibhaText variant="title" style={{ marginTop: 8 }}>
        Journal
      </PratibhaText>
      <PratibhaText variant="soft" style={{ marginTop: 8 }}>
        Reflections saved on this device, linked to paths, passages, and study chat.
      </PratibhaText>

      <View style={{ marginTop: 20, gap: 12 }}>
        {notes.length === 0 ? (
          <View style={ui.card}>
            <PratibhaText variant="soft">
              No notes yet. Save a reflection from a path step or tap Save on a Study Chat response.
            </PratibhaText>
          </View>
        ) : (
          notes.map((note) => {
            const target = reopenTarget(note);
            return (
              <View key={note.id} style={ui.card}>
                <PratibhaText variant="label">{new Date(note.updatedAt).toLocaleString()}</PratibhaText>
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
                <View style={{ marginTop: 10, flexDirection: "row", gap: 10 }}>
                  {target ? (
                    <Pressable
                      style={ui.buttonGhost}
                      onPress={() => router.push(target as never)}
                    >
                      <PratibhaText style={ui.buttonGhostText}>{reopenLabel(note)}</PratibhaText>
                    </Pressable>
                  ) : null}
                  <Pressable
                    onPress={async () => {
                      await deleteJournalNote(note.id);
                      refresh();
                    }}
                  >
                    <PratibhaText variant="label" style={{ color: "#fda4af", marginTop: 10 }}>
                      Delete
                    </PratibhaText>
                  </Pressable>
                </View>
              </View>
            );
          })
        )}
      </View>
    </PratibhaScreen>
  );
}

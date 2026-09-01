import { PratibhaScreen, stackScreenEdges } from "@/components/ui/PratibhaScreen";
import { PratibhaText, ui } from "@/components/ui/PratibhaText";
import { useStudy } from "@/context/StudyContext";
import { matchStepItem } from "@/lib/passages";
import { learnStepContextId, notesForContext, stepKey, upsertJournalNote } from "@/lib/storage";
import { useLocalSearchParams, router } from "expo-router";
import { useEffect, useState, type ReactNode } from "react";
import { Pressable, StyleSheet, TextInput, View, Keyboard } from "react-native";
import * as Haptics from "expo-haptics";
import { displayPassageTitle } from "@shared/passageTitles";
import type { JournalNote } from "@shared/types";

function actionLabel(chatMode?: string): string {
  if (chatMode === "practice") return "Practice with it";
  if (chatMode === "compare") return "Compare traditions";
  if (chatMode === "explain") return "Understand it";
  return "Study with Pratibha";
}

export default function StepScreen() {
  const { trackId, stepId } = useLocalSearchParams<{ trackId: string; stepId: string }>();
  const { trackById, items, progress, toggleStep } = useStudy();
  const track = trackById[trackId || ""];
  const step = track?.steps.find((s) => s.id === stepId);
  const done = !!progress[stepKey(trackId || "", stepId || "")];

  const [ready, setReady] = useState(false);
  const [journalBody, setJournalBody] = useState("");
  const [notes, setNotes] = useState<JournalNote[]>([]);

  const item = step ? matchStepItem(step, items) : null;
  const contextId = step && track ? learnStepContextId(track.id, step.id) : "";
  const noteKey = item?._id || contextId;

  useEffect(() => {
    setReady(false);
    if (noteKey) notesForContext(noteKey).then(setNotes);
  }, [noteKey, done]);

  if (!track || !step) {
    return (
      <PratibhaScreen edges={stackScreenEdges}>
        <PratibhaText variant="soft">Step not found.</PratibhaText>
      </PratibhaScreen>
    );
  }

  async function saveJournal() {
    if (!step || !track) return;
    const clean = journalBody.trim();
    if (!clean) return;
    if (item) {
      await upsertJournalNote({ passage: item, body: clean, prompt: step.journalPrompt });
    } else {
      await upsertJournalNote({
        contextId,
        contextTitle: `${track.title} · ${step.title}`,
        body: clean,
        prompt: step.journalPrompt,
      });
    }
    setJournalBody("");
    Keyboard.dismiss();
    setNotes(await notesForContext(noteKey));
    void Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
  }

  return (
    <PratibhaScreen edges={stackScreenEdges}>
      <PratibhaText variant="label">Gate</PratibhaText>
      <PratibhaText variant="title" style={{ marginTop: 8, fontSize: 28 }}>
        {step.title}
      </PratibhaText>
      <PratibhaText variant="soft" style={{ marginTop: 8 }}>
        {step.orientation}
      </PratibhaText>

      <Section title="Teaching">
        <PratibhaText variant="body">{step.teaching}</PratibhaText>
      </Section>

      <View style={[ui.card, ui.cardGold, { marginTop: 16 }]}>
        <PratibhaText variant="eyebrow">Key idea</PratibhaText>
        <PratibhaText variant="body" style={{ marginTop: 8, color: "#f0c979" }}>
          {step.keyIdea}
        </PratibhaText>
      </View>

      {step.misconception ? (
        <View style={[ui.card, styles.misconception, { marginTop: 12 }]}>
          <PratibhaText variant="label" style={{ color: "#fda4af" }}>
            Common misunderstanding
          </PratibhaText>
          <PratibhaText variant="body" style={{ marginTop: 8, fontSize: 15 }}>
            {step.misconception}
          </PratibhaText>
        </View>
      ) : null}

      <Section title="Study">
        {item ? (
          <>
            <Pressable
              style={[ui.card, { marginTop: 8 }]}
              onPress={() =>
                router.push({
                  pathname: "/passage/[id]",
                  params: { id: item._id },
                })
              }
            >
              <PratibhaText variant="heading" style={{ fontSize: 18 }}>
                {displayPassageTitle(item)}
              </PratibhaText>
              <PratibhaText variant="soft" style={{ marginTop: 4, fontSize: 13 }}>
                Tap to open passage →
              </PratibhaText>
            </Pressable>
            <Pressable
              style={[ui.button, { marginTop: 10 }]}
              onPress={() =>
                router.push({
                  pathname: "/ask",
                  params: {
                    verse_id: item._id,
                    q: step.chatPrompt,
                    mode: step.chatMode || "question",
                  },
                } as never)
              }
            >
              <PratibhaText style={ui.buttonText}>{actionLabel(step.chatMode)}</PratibhaText>
            </Pressable>
          </>
        ) : (
          <PratibhaText variant="soft">Passage loading…</PratibhaText>
        )}
      </Section>

      <Section title="Practice">
        <PratibhaText variant="body">{step.practice}</PratibhaText>
      </Section>

      <View style={[ui.card, { marginTop: 16 }]}>
        <PratibhaText variant="eyebrow">Journal</PratibhaText>
        <PratibhaText variant="soft" style={{ marginTop: 8, fontSize: 14 }}>
          {step.journalPrompt}
        </PratibhaText>
        <TextInput
          value={journalBody}
          onChangeText={setJournalBody}
          placeholder="Write a reflection…"
          placeholderTextColor="#897d6c"
          multiline
          style={styles.input}
        />
        <Pressable
          style={[ui.button, { marginTop: 10, opacity: journalBody.trim() ? 1 : 0.45 }]}
          onPress={saveJournal}
          disabled={!journalBody.trim()}
        >
          <PratibhaText style={ui.buttonText}>Save note</PratibhaText>
        </Pressable>
        {notes.slice(0, 2).map((n) => (
          <View key={n.id} style={{ marginTop: 12 }}>
            <PratibhaText variant="label">{new Date(n.updatedAt).toLocaleString()}</PratibhaText>
            <PratibhaText variant="body" style={{ marginTop: 4, fontSize: 15 }}>
              {n.body}
            </PratibhaText>
          </View>
        ))}
      </View>

      {!done ? (
        <View style={[ui.card, styles.gate, { marginTop: 16 }]}>
          <PratibhaText variant="label" style={{ color: "#6ee7b7" }}>
            Before you move on
          </PratibhaText>
          <PratibhaText variant="body" style={{ marginTop: 8, fontSize: 15 }}>
            {step.integration}
          </PratibhaText>
          <Pressable style={styles.checkRow} onPress={() => setReady((r) => !r)}>
            <View style={[styles.checkbox, ready && styles.checkboxOn]} />
            <PratibhaText variant="body" style={{ flex: 1, fontSize: 15 }}>
              I recognize this — or I&apos;m willing to keep practicing here.
            </PratibhaText>
          </Pressable>
          <Pressable
            style={[ui.button, { marginTop: 12, opacity: ready ? 1 : 0.4 }]}
            disabled={!ready}
            onPress={() => {
              void Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
              void toggleStep(track.id, step.id);
            }}
          >
            <PratibhaText style={ui.buttonText}>Mark complete</PratibhaText>
          </Pressable>
        </View>
      ) : (
        <Pressable style={[ui.buttonGhost, { marginTop: 16 }]} onPress={() => toggleStep(track.id, step.id)}>
          <PratibhaText style={ui.buttonGhostText}>Reopen gate</PratibhaText>
        </Pressable>
      )}
    </PratibhaScreen>
  );
}

function Section({ title, children }: { title: string; children: ReactNode }) {
  return (
    <View style={{ marginTop: 18 }}>
      <PratibhaText variant="eyebrow">{title}</PratibhaText>
      <View style={{ marginTop: 8 }}>{children}</View>
    </View>
  );
}

const styles = StyleSheet.create({
  misconception: { borderColor: "rgba(253,164,175,0.3)", backgroundColor: "rgba(253,164,175,0.06)" },
  gate: { borderColor: "rgba(110,231,183,0.3)", backgroundColor: "rgba(110,231,183,0.06)" },
  input: {
    marginTop: 10,
    minHeight: 100,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "rgba(240,201,121,0.2)",
    padding: 12,
    color: "#f3ead8",
    fontFamily: "System",
    fontSize: 15,
    textAlignVertical: "top",
    backgroundColor: "rgba(0,0,0,0.2)",
  },
  checkRow: { flexDirection: "row", gap: 12, marginTop: 14, alignItems: "flex-start" },
  checkbox: {
    width: 22,
    height: 22,
    borderRadius: 6,
    borderWidth: 2,
    borderColor: "rgba(240,201,121,0.4)",
    marginTop: 2,
  },
  checkboxOn: { backgroundColor: "#f0c979", borderColor: "#f0c979" },
});

import { useEffect, useState } from "@lynx-js/react";
import { fetchVerse, type Passage } from "../lib/corpus";
import {
  LEARN_REALMS,
  RECOMMENDED_THREADS,
  loadProgress,
  markComplete,
  stepKey,
  syncLearnProgress,
  threadById,
  threadKey,
  trackById,
  type LearnStep,
  type LearnThread,
  type LearnTrack,
  type ProgressMap,
} from "../lib/learn";
import { useAuth } from "../auth/AuthProvider";
import { useConvex } from "../convex/ConvexProvider";
import { PassageDetail } from "./ReadPage";
import { C, SERIF } from "../lib/theme";

type Tab = "paths" | "themes";
type View =
  | { kind: "home" }
  | { kind: "track"; track: LearnTrack }
  | { kind: "thread"; thread: LearnThread }
  | { kind: "passage"; passage: Passage; back: View };

export function LearnPage() {
  const { user } = useAuth();
  const { httpClient } = useConvex();
  const [tab, setTab] = useState<Tab>("paths");
  const [view, setView] = useState<View>({ kind: "home" });
  const [progress, setProgress] = useState<ProgressMap>({});

  useEffect(() => {
    const local = loadProgress();
    setProgress(local.progress);
    void syncLearnProgress(httpClient, user).then((bundle) => setProgress(bundle.progress));
  }, [user]);

  function complete(key: string) {
    const bundle = markComplete(progress, loadProgress().completedAt, key);
    setProgress(bundle.progress);
    void syncLearnProgress(httpClient, user);
  }

  async function openPassage(id: string, back: View) {
    try {
      const passage = await fetchVerse(id);
      setView({ kind: "passage", passage, back });
    } catch {
      /* keep current view */
    }
  }

  if (view.kind === "passage") {
    return (
      <PassageDetail
        passage={view.passage}
        backLabel="← Learn"
        onBack={() => setView(view.back)}
      />
    );
  }

  if (view.kind === "track") {
    return (
      <TrackDetail
        track={view.track}
        progress={progress}
        onBack={() => setView({ kind: "home" })}
        onOpen={(step) => void openPassage(step.passageId, view)}
        onComplete={(step) => complete(stepKey(view.track.id, step.id))}
      />
    );
  }

  if (view.kind === "thread") {
    return (
      <ThreadDetail
        thread={view.thread}
        progress={progress}
        onBack={() => setView({ kind: "home" })}
        onOpen={(step) => void openPassage(step.passageId, view)}
        onComplete={(step) => complete(threadKey(view.thread.id, step.id))}
      />
    );
  }

  const threadList = RECOMMENDED_THREADS.map((id) => threadById(id)).filter(Boolean) as LearnThread[];

  return (
    <scroll-view style={{ flex: 1, backgroundColor: C.bg }}>
      <view style={{ padding: 22 }}>
        <text style={{ color: C.gold, fontSize: 26, fontWeight: "bold", fontFamily: SERIF, marginBottom: 8 }}>
          Learn
        </text>
        <text style={{ color: C.muted, fontSize: 14, marginBottom: 16 }}>
          Paths are sequential gates. Themes are cross-tradition arguments.
        </text>

        <view style={{ flexDirection: "row", gap: 8, marginBottom: 20 }}>
          <TabChip label="Paths" active={tab === "paths"} onTap={() => setTab("paths")} />
          <TabChip label="Themes" active={tab === "themes"} onTap={() => setTab("themes")} />
        </view>

        {tab === "paths"
          ? LEARN_REALMS.map((realm) => (
              <view key={realm.id} style={{ marginBottom: 22 }}>
                <text style={{ color: C.goldMuted, fontSize: 13, letterSpacing: 1, textTransform: "uppercase", marginBottom: 4 }}>
                  {realm.title}
                </text>
                <text style={{ color: C.muted, fontSize: 13, marginBottom: 10 }}>{realm.blurb}</text>
                <view style={{ gap: 10 }}>
                  {realm.trackIds.map((id) => {
                    const track = trackById(id);
                    if (!track) return null;
                    const done = track.steps.filter((s) => progress[stepKey(track.id, s.id)]).length;
                    return (
                      <view
                        key={id}
                        bindtap={() => setView({ kind: "track", track })}
                        style={{ padding: 14, backgroundColor: C.card, borderRadius: 8, borderLeftWidth: 4, borderLeftColor: C.gold }}
                      >
                        <text style={{ color: C.faint, fontSize: 11, marginBottom: 4 }}>
                          {track.level} · {done}/{track.steps.length} gates
                        </text>
                        <text style={{ color: C.gold, fontSize: 16, fontWeight: "600", fontFamily: SERIF, marginBottom: 6 }}>
                          {track.title}
                        </text>
                        <text style={{ color: C.muted, fontSize: 13, lineHeight: 1.5 }}>{track.focus}</text>
                      </view>
                    );
                  })}
                </view>
              </view>
            ))
          : (
            <view style={{ gap: 10 }}>
              {threadList.map((thread) => {
                const done = thread.steps.filter((s) => progress[threadKey(thread.id, s.id)]).length;
                return (
                  <view
                    key={thread.id}
                    bindtap={() => setView({ kind: "thread", thread })}
                    style={{ padding: 14, backgroundColor: C.card, borderRadius: 8, borderLeftWidth: 4, borderLeftColor: C.gold }}
                  >
                    <text style={{ color: C.faint, fontSize: 11, marginBottom: 4 }}>
                      {done}/{thread.steps.length} beads
                    </text>
                    <text style={{ color: C.gold, fontSize: 16, fontWeight: "600", fontFamily: SERIF, marginBottom: 6 }}>
                      {thread.title}
                    </text>
                    <text style={{ color: C.muted, fontSize: 13, lineHeight: 1.5 }}>{thread.thesis}</text>
                  </view>
                );
              })}
            </view>
          )}
      </view>
    </scroll-view>
  );
}

function TabChip({ label, active, onTap }: { label: string; active: boolean; onTap: () => void }) {
  return (
    <view
      bindtap={onTap}
      style={{
        paddingTop: 7,
        paddingBottom: 7,
        paddingLeft: 14,
        paddingRight: 14,
        backgroundColor: active ? C.gold : C.cardAlt,
        borderRadius: 14,
      }}
    >
      <text style={{ color: active ? "#000" : C.goldMuted, fontSize: 13 }}>{label}</text>
    </view>
  );
}

function TrackDetail({
  track,
  progress,
  onBack,
  onOpen,
  onComplete,
}: {
  track: LearnTrack;
  progress: ProgressMap;
  onBack: () => void;
  onOpen: (step: LearnStep) => void;
  onComplete: (step: LearnStep) => void;
}) {
  return (
    <scroll-view style={{ flex: 1, backgroundColor: C.bg }}>
      <view style={{ padding: 22 }}>
        <Back onBack={onBack} />
        <text style={{ color: C.faint, fontSize: 12, marginBottom: 6 }}>
          {track.level} · {track.estimatedSessions}
        </text>
        <text style={{ color: C.gold, fontSize: 24, fontWeight: "bold", fontFamily: SERIF, marginBottom: 10 }}>
          {track.title}
        </text>
        <text style={{ color: C.muted, fontSize: 14, lineHeight: 1.55, marginBottom: 18 }}>{track.outcome}</text>
        <view style={{ gap: 12 }}>
          {track.steps.map((step, i) => (
            <StepCard
              key={step.id}
              index={i + 1}
              title={step.title || step.id}
              body={step.keyIdea || step.practice || ""}
              done={Boolean(progress[stepKey(track.id, step.id)])}
              onOpen={() => onOpen(step)}
              onComplete={() => onComplete(step)}
            />
          ))}
        </view>
      </view>
    </scroll-view>
  );
}

function ThreadDetail({
  thread,
  progress,
  onBack,
  onOpen,
  onComplete,
}: {
  thread: LearnThread;
  progress: ProgressMap;
  onBack: () => void;
  onOpen: (step: LearnStep) => void;
  onComplete: (step: LearnStep) => void;
}) {
  return (
    <scroll-view style={{ flex: 1, backgroundColor: C.bg }}>
      <view style={{ padding: 22 }}>
        <Back onBack={onBack} />
        <text style={{ color: C.gold, fontSize: 24, fontWeight: "bold", fontFamily: SERIF, marginBottom: 8 }}>
          {thread.title}
        </text>
        <text style={{ color: C.muted, fontSize: 14, lineHeight: 1.55, marginBottom: 18 }}>{thread.thesis}</text>
        <view style={{ gap: 12 }}>
          {thread.steps.map((step, i) => (
            <StepCard
              key={step.id}
              index={i + 1}
              title={step.tradition || step.title || step.id}
              body={step.insight || ""}
              done={Boolean(progress[threadKey(thread.id, step.id)])}
              onOpen={() => onOpen(step)}
              onComplete={() => onComplete(step)}
            />
          ))}
        </view>
        {thread.practice ? (
          <view style={{ marginTop: 18, padding: 14, backgroundColor: "#1c1a12", borderRadius: 8 }}>
            <text style={{ color: C.goldMuted, fontSize: 11, letterSpacing: 1.5, textTransform: "uppercase", marginBottom: 8 }}>
              Practice
            </text>
            <text style={{ color: C.read, fontSize: 14, lineHeight: 1.6 }}>{thread.practice}</text>
          </view>
        ) : null}
      </view>
    </scroll-view>
  );
}

function Back({ onBack }: { onBack: () => void }) {
  return (
    <view
      bindtap={onBack}
      style={{
        marginBottom: 18,
        paddingTop: 8,
        paddingBottom: 8,
        paddingLeft: 16,
        paddingRight: 16,
        backgroundColor: C.cardAlt,
        borderRadius: 6,
        alignSelf: "flex-start",
      }}
    >
      <text style={{ color: C.gold, fontSize: 14 }}>← Learn</text>
    </view>
  );
}

function StepCard({
  index,
  title,
  body,
  done,
  onOpen,
  onComplete,
}: {
  index: number;
  title: string;
  body: string;
  done: boolean;
  onOpen: () => void;
  onComplete: () => void;
}) {
  return (
    <view style={{ padding: 14, backgroundColor: C.card, borderRadius: 8 }}>
      <text style={{ color: C.faint, fontSize: 11, marginBottom: 4 }}>
        {done ? "Complete" : `Gate ${index}`}
      </text>
      <text style={{ color: C.gold, fontSize: 16, fontWeight: "600", fontFamily: SERIF, marginBottom: 6 }}>
        {title}
      </text>
      {body ? <text style={{ color: C.muted, fontSize: 13, lineHeight: 1.5, marginBottom: 12 }}>{body}</text> : null}
      <view style={{ flexDirection: "row", gap: 8 }}>
        <view
          bindtap={onOpen}
          style={{ paddingTop: 7, paddingBottom: 7, paddingLeft: 12, paddingRight: 12, backgroundColor: C.cardAlt, borderRadius: 6 }}
        >
          <text style={{ color: C.gold, fontSize: 13 }}>Open passage</text>
        </view>
        <view
          bindtap={done ? undefined : onComplete}
          style={{ paddingTop: 7, paddingBottom: 7, paddingLeft: 12, paddingRight: 12, backgroundColor: done ? C.cardAlt : C.gold, borderRadius: 6 }}
        >
          <text style={{ color: done ? C.muted : "#000", fontSize: 13 }}>{done ? "Done" : "Mark complete"}</text>
        </view>
      </view>
    </view>
  );
}

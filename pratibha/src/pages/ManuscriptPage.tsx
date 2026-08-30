import { useEffect, useMemo, useState } from "@lynx-js/react";
import { useAuth } from "../auth/AuthProvider";
import { useConvex } from "../convex/ConvexProvider";
import { isConvexConfigured } from "../convex/httpClient";
import { C, SERIF } from "../lib/theme";
import { sumiGlyph, type InkState } from "../lib/sumi";
import { SumiGlyph } from "../components/SumiGlyph";

type Entry = { verseId: string; verseTitle: string; note: string; sortOrder: number };
type Manuscript = {
  slug: string;
  title: string;
  displayName: string;
  visibility: "private" | "public";
  entries: Entry[];
};

const STATE_LABEL: Record<InkState, string> = {
  unmanifest: "Held",
  arising: "Noted",
  recognized: "Recognized",
};

// Turn a verse id prefix ("vijnana_bhairava.yukti_001") into a readable text
// name ("Vijnana Bhairava") for the leaf eyebrow.
function collectionOf(verseId: string): string {
  const prefix = (verseId.split(".")[0] || verseId).replace(/_/g, " ").trim();
  return prefix.replace(/\b\w/g, (c) => c.toUpperCase());
}

export function ManuscriptPage({ onOpenVerse }: { onOpenVerse?: (verseId: string) => void }) {
  const { user } = useAuth();
  const { httpClient } = useConvex();
  const ready = Boolean(httpClient && isConvexConfigured());
  const [manuscript, setManuscript] = useState<Manuscript | null>(null);
  const [liked, setLiked] = useState<string[]>([]);
  const [title, setTitle] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [showBinding, setShowBinding] = useState(false);

  useEffect(() => {
    if (!ready || !user) {
      setLoading(false);
      return;
    }
    void load();
  }, [user, ready]);

  async function load() {
    "background only";
    if (!httpClient) return;
    try {
      const [mine, likes] = await Promise.all([
        httpClient.query("manuscripts:getMine", {}) as Promise<Manuscript | null>,
        httpClient.query("verseLikes:mine", {}) as Promise<string[]>,
      ]);
      setManuscript(mine);
      setLiked(likes || []);
      if (mine) {
        setTitle(mine.title);
        setDisplayName(mine.displayName === "Student" ? "" : mine.displayName);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function saveSettings(visibility?: "private" | "public") {
    "background only";
    if (!httpClient) return;
    setError("");
    try {
      await httpClient.mutation("manuscripts:updateSettings", {
        title: title.trim() || undefined,
        displayName: displayName.trim() || undefined,
        visibility,
      });
      await load();
    } catch (err: any) {
      setError(err?.message || "Could not update.");
    }
  }

  async function move(verseId: string, direction: "up" | "down") {
    "background only";
    if (!httpClient) return;
    await httpClient.mutation("manuscripts:moveVerse", { verseId, direction });
    await load();
  }

  async function remove(verseId: string) {
    "background only";
    if (!httpClient) return;
    await httpClient.mutation("manuscripts:removeVerse", { verseId });
    await load();
  }

  const entries = manuscript?.entries ?? [];
  const likedSet = useMemo(() => new Set(liked), [liked]);

  function stateFor(entry: Entry): InkState {
    if (likedSet.has(entry.verseId)) return "recognized";
    if (entry.note && entry.note.trim()) return "arising";
    return "unmanifest";
  }

  const recognizedCount = useMemo(
    () => entries.filter((e) => likedSet.has(e.verseId)).length,
    [entries, likedSet],
  );

  // The cover mark grows from the book's own contents: the first recognized
  // leaf's mark, else the first leaf's, else a mandala.
  const coverGlyph = useMemo(() => {
    const recognized = entries.find((e) => likedSet.has(e.verseId));
    const seed = recognized?.verseId || entries[0]?.verseId;
    return seed ? sumiGlyph(seed) : "mandala";
  }, [entries, likedSet]);

  if (!user || !ready) {
    return (
      <view style={{ flex: 1, padding: 22, backgroundColor: C.bg }}>
        <text style={{ color: C.gold, fontSize: 26, fontWeight: "bold", fontFamily: SERIF, marginBottom: 8 }}>
          Your manuscript
        </text>
        <text style={{ color: C.muted, fontSize: 14 }}>Sign in to gather verses into a small book.</text>
      </view>
    );
  }

  if (loading) {
    return (
      <view style={{ flex: 1, padding: 22, backgroundColor: C.bg }}>
        <text style={{ color: C.muted }}>Opening your manuscript…</text>
      </view>
    );
  }

  return (
    <scroll-view style={{ flex: 1, backgroundColor: C.bg }}>
      <view style={{ padding: 22 }}>
        {/* ---- Cover ---- */}
        <view style={{ alignItems: "center", paddingBottom: 26, borderBottomWidth: 1, borderBottomColor: C.line }}>
          <SumiGlyph glyph={coverGlyph} state="recognized" size={132} breath />
          <text style={{ color: C.goldMuted, fontSize: 11, letterSpacing: 3, textTransform: "uppercase", marginTop: 18 }}>
            A living manuscript
          </text>
          <text
            style={{ color: C.bone, fontSize: 30, fontWeight: "bold", fontFamily: SERIF, textAlign: "center", marginTop: 8 }}
          >
            {manuscript?.title || "Your manuscript"}
          </text>
          {manuscript?.displayName && manuscript.displayName !== "Student" ? (
            <text style={{ color: C.muted, fontSize: 15, fontStyle: "italic", marginTop: 10 }}>
              kept by {manuscript.displayName}
            </text>
          ) : null}
          <view style={{ flexDirection: "row", gap: 10, alignItems: "center", marginTop: 14 }}>
            <text style={{ color: C.faint, fontSize: 12 }}>
              {entries.length} {entries.length === 1 ? "leaf" : "leaves"}
            </text>
            {recognizedCount > 0 ? (
              <>
                <text style={{ color: C.goldDeep, fontSize: 12 }}>·</text>
                <text style={{ color: C.goldMuted, fontSize: 12 }}>{recognizedCount} recognized</text>
              </>
            ) : null}
          </view>
        </view>

        {/* ---- Legend ---- */}
        {entries.length > 0 ? (
          <view style={{ flexDirection: "row", flexWrap: "wrap", gap: 16, justifyContent: "center", paddingTop: 18 }}>
            <LegendMark glyph="circle" state="unmanifest" label="Held" />
            <LegendMark glyph="circle" state="arising" label="Noted" />
            <LegendMark glyph="circle" state="recognized" label="Recognized" />
          </view>
        ) : null}

        {/* ---- Binding (settings) ---- */}
        <view
          bindtap={() => setShowBinding((v) => !v)}
          style={{ marginTop: 20, alignSelf: "center" }}
        >
          <text style={{ color: C.goldMuted, fontSize: 12, letterSpacing: 1 }}>
            {showBinding ? "Close binding" : "Title, name & sharing"}
          </text>
        </view>

        {showBinding ? (
          <view style={{ marginTop: 12, padding: 14, backgroundColor: C.card, borderRadius: 8 }}>
            <input
              type="text"
              value={title}
              bindinput={(e: any) => setTitle(e.detail?.value ?? e.target?.value ?? "")}
              placeholder="Title"
              style={{ width: "100%", padding: 10, marginBottom: 10, backgroundColor: C.bg, border: `1px solid ${C.line}`, borderRadius: 6, color: "#fff", fontSize: 14 }}
            />
            <input
              type="text"
              value={displayName}
              bindinput={(e: any) => setDisplayName(e.detail?.value ?? e.target?.value ?? "")}
              placeholder="Your name on a shared manuscript"
              style={{ width: "100%", padding: 10, marginBottom: 12, backgroundColor: C.bg, border: `1px solid ${C.line}`, borderRadius: 6, color: "#fff", fontSize: 14 }}
            />
            <view style={{ flexDirection: "row", flexWrap: "wrap", gap: 8 }}>
              <view bindtap={() => void saveSettings()} style={{ padding: 10, backgroundColor: C.gold, borderRadius: 6 }}>
                <text style={{ color: "#000", fontSize: 13, fontWeight: "600" }}>Save</text>
              </view>
              <view
                bindtap={() => void saveSettings(manuscript?.visibility === "public" ? "private" : "public")}
                style={{ padding: 10, backgroundColor: C.cardAlt, borderRadius: 6 }}
              >
                <text style={{ color: C.gold, fontSize: 13 }}>
                  {manuscript?.visibility === "public" ? "Make private" : "Make public"}
                </text>
              </view>
            </view>
            {manuscript?.visibility === "public" ? (
              <text style={{ color: C.muted, fontSize: 13, marginTop: 12 }}>Public link: /m/{manuscript.slug}</text>
            ) : null}
            {error ? <text style={{ color: C.danger, fontSize: 13, marginTop: 12 }}>{error}</text> : null}
          </view>
        ) : null}

        {/* ---- Leaves ---- */}
        <view style={{ marginTop: 22 }}>
          {entries.length === 0 ? (
            <text style={{ color: C.muted, fontSize: 15, lineHeight: 1.6, textAlign: "center" }}>
              Nothing gathered yet. Open a passage and choose{"\n"}“Add to manuscript.”
            </text>
          ) : (
            <view>
              {entries.map((entry, index) => {
                const st = stateFor(entry);
                const glyph = sumiGlyph(entry.verseId);
                return (
                  <view
                    key={entry.verseId}
                    style={{
                      flexDirection: "row",
                      gap: 14,
                      paddingTop: 22,
                      paddingBottom: 22,
                      borderBottomWidth: index === entries.length - 1 ? 0 : 1,
                      borderBottomColor: C.card,
                    }}
                  >
                    {/* margin capital */}
                    <view style={{ width: 56, alignItems: "center", paddingTop: 2 }}>
                      <SumiGlyph glyph={glyph} state={st} size={48} />
                    </view>

                    {/* body */}
                    <view style={{ flex: 1 }}>
                      <view style={{ flexDirection: "row", alignItems: "center", justifyContent: "space-between", gap: 10 }}>
                        <text style={{ color: C.goldMuted, fontSize: 10.5, letterSpacing: 2, textTransform: "uppercase" }}>
                          {collectionOf(entry.verseId)}
                        </text>
                        <StateChip state={st} />
                      </view>

                      <view bindtap={onOpenVerse ? () => onOpenVerse(entry.verseId) : undefined}>
                        <text style={{ color: C.gold, fontSize: 19, fontFamily: SERIF, marginTop: 8 }}>
                          {entry.verseTitle}
                        </text>
                      </view>

                      {entry.note && entry.note.trim() ? (
                        <view
                          style={{
                            marginTop: 12,
                            paddingTop: 10,
                            paddingBottom: 10,
                            paddingLeft: 14,
                            paddingRight: 14,
                            backgroundColor: "#17140c",
                            borderLeftWidth: 2,
                            borderLeftColor: C.goldDeep,
                            borderRadius: 6,
                          }}
                        >
                          <text style={{ color: C.goldMuted, fontSize: 9.5, letterSpacing: 2, textTransform: "uppercase", marginBottom: 5 }}>
                            your hand
                          </text>
                          <text style={{ color: "#cdbfa6", fontSize: 14, fontStyle: "italic", lineHeight: 1.55 }}>
                            {entry.note}
                          </text>
                        </view>
                      ) : null}

                      <view style={{ flexDirection: "row", gap: 16, marginTop: 12 }}>
                        <view bindtap={index === 0 ? undefined : () => void move(entry.verseId, "up")}>
                          <text style={{ color: index === 0 ? C.faint : C.goldMuted, fontSize: 12 }}>↑</text>
                        </view>
                        <view bindtap={index === entries.length - 1 ? undefined : () => void move(entry.verseId, "down")}>
                          <text style={{ color: index === entries.length - 1 ? C.faint : C.goldMuted, fontSize: 12 }}>↓</text>
                        </view>
                        <view bindtap={() => void remove(entry.verseId)}>
                          <text style={{ color: C.faint, fontSize: 12 }}>Remove</text>
                        </view>
                      </view>
                    </view>
                  </view>
                );
              })}
            </view>
          )}
        </view>

        {entries.length > 0 ? (
          <view style={{ marginTop: 30, alignItems: "center" }}>
            <view style={{ width: 40, height: 1, backgroundColor: C.line, marginBottom: 14 }} />
            <text style={{ color: C.faint, fontSize: 12, textAlign: "center", lineHeight: 1.6 }}>
              The ink brightens as you return.{"\n"}Ash to bone to gold — the manuscript remembers{"\n"}where your attention has lived.
            </text>
          </view>
        ) : null}
      </view>
    </scroll-view>
  );
}

function LegendMark({ glyph, state, label }: { glyph: string; state: InkState; label: string }) {
  return (
    <view style={{ flexDirection: "row", alignItems: "center", gap: 7 }}>
      <SumiGlyph glyph={glyph} state={state} size={16} />
      <text style={{ color: C.muted, fontSize: 12 }}>{label}</text>
    </view>
  );
}

function StateChip({ state }: { state: InkState }) {
  if (state === "recognized") {
    return (
      <view style={{ paddingTop: 3, paddingBottom: 3, paddingLeft: 9, paddingRight: 9, backgroundColor: C.gold, borderRadius: 999 }}>
        <text style={{ color: "#221a08", fontSize: 9.5, letterSpacing: 1, textTransform: "uppercase" }}>
          {STATE_LABEL.recognized}
        </text>
      </view>
    );
  }
  const border = state === "arising" ? C.line : C.card;
  const color = state === "arising" ? C.bone : C.faint;
  return (
    <view style={{ paddingTop: 3, paddingBottom: 3, paddingLeft: 9, paddingRight: 9, borderWidth: 1, borderColor: border, borderRadius: 999 }}>
      <text style={{ color, fontSize: 9.5, letterSpacing: 1, textTransform: "uppercase" }}>{STATE_LABEL[state]}</text>
    </view>
  );
}

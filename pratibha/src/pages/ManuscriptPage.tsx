import { useEffect, useState } from "@lynx-js/react";
import { useAuth } from "../auth/AuthProvider";
import { useConvex } from "../convex/ConvexProvider";
import { isConvexConfigured } from "../convex/httpClient";
import { C, SERIF } from "../lib/theme";

type Entry = { verseId: string; verseTitle: string; note: string; sortOrder: number };
type Manuscript = {
  slug: string;
  title: string;
  displayName: string;
  visibility: "private" | "public";
  entries: Entry[];
};

export function ManuscriptPage({ onOpenVerse }: { onOpenVerse?: (verseId: string) => void }) {
  const { user } = useAuth();
  const { httpClient } = useConvex();
  const ready = Boolean(httpClient && isConvexConfigured());
  const [manuscript, setManuscript] = useState<Manuscript | null>(null);
  const [title, setTitle] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

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
      const mine = (await httpClient.query("manuscripts:getMine", {})) as Manuscript | null;
      setManuscript(mine);
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

  if (!user || !ready) {
    return (
      <view style={{ padding: 22 }}>
        <text style={{ color: C.gold, fontSize: 26, fontWeight: "bold", fontFamily: SERIF, marginBottom: 8 }}>
          Your manuscript
        </text>
        <text style={{ color: C.muted, fontSize: 14 }}>Sign in to gather verses into a small book.</text>
      </view>
    );
  }

  if (loading) {
    return (
      <view style={{ padding: 22 }}>
        <text style={{ color: C.muted }}>Opening your manuscript…</text>
      </view>
    );
  }

  const entries = manuscript?.entries ?? [];

  return (
    <view style={{ padding: 22 }}>
      <text style={{ color: C.gold, fontSize: 26, fontWeight: "bold", fontFamily: SERIF, marginBottom: 8 }}>
        Your manuscript
      </text>
      <text style={{ color: C.muted, fontSize: 14, lineHeight: 1.55, marginBottom: 18 }}>
        A chapbook of verses you sit with. Private until you share it.
      </text>

      <input
        type="text"
        value={title}
        bindinput={(e: any) => setTitle(e.detail?.value ?? e.target?.value ?? "")}
        placeholder="Title"
        style={{
          width: "100%",
          padding: 10,
          marginBottom: 10,
          backgroundColor: C.card,
          border: "1px solid #333",
          borderRadius: 6,
          color: "#fff",
          fontSize: 14,
        }}
      />
      <input
        type="text"
        value={displayName}
        bindinput={(e: any) => setDisplayName(e.detail?.value ?? e.target?.value ?? "")}
        placeholder="Your name on a shared manuscript"
        style={{
          width: "100%",
          padding: 10,
          marginBottom: 12,
          backgroundColor: C.card,
          border: "1px solid #333",
          borderRadius: 6,
          color: "#fff",
          fontSize: 14,
        }}
      />
      <view style={{ flexDirection: "row", flexWrap: "wrap", gap: 8, marginBottom: 16 }}>
        <view
          bindtap={() => void saveSettings()}
          style={{ padding: 10, backgroundColor: C.gold, borderRadius: 6 }}
        >
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
        <text style={{ color: C.muted, fontSize: 13, marginBottom: 16 }}>
          Public link: /m/{manuscript.slug}
        </text>
      ) : null}
      {error ? <text style={{ color: C.danger, fontSize: 13, marginBottom: 12 }}>{error}</text> : null}

      <text style={{ color: C.goldMuted, fontSize: 11, letterSpacing: 1.5, textTransform: "uppercase", marginBottom: 12 }}>
        Verses{entries.length ? `  ·  ${entries.length}` : ""}
      </text>
      {entries.length === 0 ? (
        <text style={{ color: C.muted, fontSize: 14, lineHeight: 1.55 }}>
          Nothing here yet. Open a passage and choose Add to manuscript.
        </text>
      ) : (
        <view style={{ gap: 16 }}>
          {entries.map((entry, index) => (
            <view
              key={entry.verseId}
              style={{ padding: 14, backgroundColor: C.card, borderRadius: 8, borderLeftWidth: 3, borderLeftColor: C.gold }}
            >
              <text style={{ color: C.faint, fontSize: 11, marginBottom: 4 }}>{index + 1}</text>
              <view bindtap={onOpenVerse ? () => onOpenVerse(entry.verseId) : undefined}>
                <text style={{ color: C.gold, fontSize: 16, fontFamily: SERIF, marginBottom: 6 }}>
                  {entry.verseTitle}
                </text>
              </view>
              {entry.note ? (
                <text style={{ color: C.muted, fontSize: 14, fontStyle: "italic", marginBottom: 10 }}>
                  {entry.note}
                </text>
              ) : null}
              <view style={{ flexDirection: "row", gap: 10 }}>
                <view bindtap={index === 0 ? undefined : () => void move(entry.verseId, "up")}>
                  <text style={{ color: index === 0 ? C.faint : C.goldMuted, fontSize: 12 }}>Up</text>
                </view>
                <view
                  bindtap={index === entries.length - 1 ? undefined : () => void move(entry.verseId, "down")}
                >
                  <text style={{ color: index === entries.length - 1 ? C.faint : C.goldMuted, fontSize: 12 }}>
                    Down
                  </text>
                </view>
                <view bindtap={() => void remove(entry.verseId)}>
                  <text style={{ color: C.danger, fontSize: 12 }}>Remove</text>
                </view>
              </view>
            </view>
          ))}
        </view>
      )}
    </view>
  );
}

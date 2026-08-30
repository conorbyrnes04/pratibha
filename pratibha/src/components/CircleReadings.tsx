import { useEffect, useState } from "@lynx-js/react";
import { useAuth } from "../auth/AuthProvider";
import { useConvex } from "../convex/ConvexProvider";
import { isConvexConfigured } from "../convex/httpClient";
import { showCircle } from "../lib/circleVerses";
import { C } from "../lib/theme";

type Offered = { _id: string; displayName: string; body: string };
type Reply = { _id: string; displayName: string; body: string; mine: boolean };

export function CircleReadings({ verseId, daily = false }: { verseId: string; daily?: boolean }) {
  const { user } = useAuth();
  const { httpClient } = useConvex();
  const ready = Boolean(httpClient && isConvexConfigured());
  const [offered, setOffered] = useState<Offered[]>([]);
  const [count, setCount] = useState(0);
  const [openCircle, setOpenCircle] = useState(false);
  const [readyMeta, setReadyMeta] = useState(false);

  useEffect(() => {
    if (!ready) return;
    void load();
  }, [verseId, user, ready]);

  async function load() {
    "background only";
    if (!httpClient) return;
    try {
      const meta = (await httpClient.query("studentCommentaries:circleMeta", { verseId })) as {
        open: boolean;
        offeredCount: number;
      };
      setOpenCircle(Boolean(meta.open));
      setCount(meta.offeredCount);
      if (user) {
        const rows = (await httpClient.query("studentCommentaries:listOffered", { verseId })) as Offered[];
        setOffered(rows || []);
      } else {
        setOffered([]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setReadyMeta(true);
    }
  }

  if (!ready || !readyMeta) return null;
  if (!showCircle(verseId, count, daily)) return null;

  return (
    <view style={{ marginBottom: 24 }}>
      <text style={{ color: C.goldMuted, fontSize: 11, letterSpacing: 1.5, textTransform: "uppercase", marginBottom: 8 }}>
        {openCircle || daily ? "Circle" : "Other readings"}
      </text>
      <text style={{ color: C.muted, fontSize: 13, lineHeight: 1.55, marginBottom: 12 }}>
        {openCircle || daily
          ? "Students write their own commentary here."
          : "Readings offered on this verse."}
        {count ? `  ·  ${count}` : ""}
      </text>
      {!user ? (
        <text style={{ color: C.muted, fontSize: 14 }}>Sign in to read the circle.</text>
      ) : offered.length === 0 ? (
        <text style={{ color: C.muted, fontSize: 14, lineHeight: 1.55 }}>
          The circle is open. Offer a reading when the verse has sat with you.
        </text>
      ) : (
        <view style={{ gap: 18 }}>
          {offered.map((reading) => (
            <view key={reading._id}>
              <text style={{ color: C.gold, fontSize: 12, letterSpacing: 1, textTransform: "uppercase", marginBottom: 6 }}>
                {reading.displayName}
              </text>
              <text style={{ color: C.read, fontSize: 15, lineHeight: 1.65 }}>{reading.body}</text>
              <ReplyBlock commentaryId={reading._id} />
            </view>
          ))}
        </view>
      )}
    </view>
  );
}

function ReplyBlock({ commentaryId }: { commentaryId: string }) {
  const { httpClient } = useConvex();
  const [replies, setReplies] = useState<Reply[]>([]);
  const [open, setOpen] = useState(false);
  const [body, setBody] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    void load();
  }, [commentaryId]);

  async function load() {
    "background only";
    if (!httpClient) return;
    try {
      const rows = (await httpClient.query("circleReplies:list", { commentaryId })) as Reply[];
      setReplies(rows || []);
    } catch (err) {
      console.error(err);
    }
  }

  async function submit() {
    "background only";
    if (!httpClient || !body.trim()) return;
    setError("");
    try {
      await httpClient.mutation("circleReplies:post", { commentaryId, body });
      setBody("");
      setOpen(false);
      await load();
    } catch (err: any) {
      setError(err?.message || "Could not reply.");
    }
  }

  const already = replies.some((r) => r.mine);

  return (
    <view style={{ marginTop: 10 }}>
      {replies.map((reply) => (
        <view key={reply._id} style={{ paddingLeft: 12, marginBottom: 8, borderLeftWidth: 1, borderLeftColor: C.line }}>
          <text style={{ color: C.faint, fontSize: 11, marginBottom: 4 }}>{reply.displayName}</text>
          <text style={{ color: C.muted, fontSize: 14, lineHeight: 1.5 }}>{reply.body}</text>
        </view>
      ))}
      {already ? (
        <text style={{ color: C.faint, fontSize: 12 }}>You have replied.</text>
      ) : open ? (
        <view>
          <textarea
            value={body}
            bindinput={(e: any) => setBody(e.detail?.value ?? e.target?.value ?? "")}
            placeholder="A response, not a verdict."
            rows={3}
            style={{
              width: "100%",
              padding: 8,
              marginBottom: 8,
              backgroundColor: C.card,
              border: "1px solid #333",
              borderRadius: 6,
              color: "#fff",
              fontSize: 14,
            }}
          />
          {error ? <text style={{ color: C.danger, fontSize: 12, marginBottom: 8 }}>{error}</text> : null}
          <view style={{ flexDirection: "row", gap: 8 }}>
            <view
              bindtap={() => void submit()}
              style={{ padding: 8, backgroundColor: C.gold, borderRadius: 6 }}
            >
              <text style={{ color: "#000", fontSize: 12, fontWeight: "600" }}>Post reply</text>
            </view>
            <view bindtap={() => setOpen(false)} style={{ padding: 8 }}>
              <text style={{ color: C.muted, fontSize: 12 }}>Cancel</text>
            </view>
          </view>
        </view>
      ) : (
        <view bindtap={() => setOpen(true)}>
          <text style={{ color: C.goldMuted, fontSize: 12 }}>Reply</text>
        </view>
      )}
    </view>
  );
}

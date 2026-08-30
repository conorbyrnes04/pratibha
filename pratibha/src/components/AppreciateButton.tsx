import { useEffect, useState } from "@lynx-js/react";
import { useAuth } from "../auth/AuthProvider";
import { useConvex } from "../convex/ConvexProvider";
import { isConvexConfigured } from "../convex/httpClient";
import { C } from "../lib/theme";

type Meta = { count: number; mine: boolean; signedIn: boolean };

// A quiet appreciation on a verse (ported from the social branch's likes,
// reframed for the contemplative Circles tone). Optimistic toggle.
export function AppreciateButton({ verseId }: { verseId: string }) {
  const { user } = useAuth();
  const { httpClient } = useConvex();
  const ready = Boolean(httpClient && isConvexConfigured());
  const [count, setCount] = useState(0);
  const [mine, setMine] = useState(false);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (!ready) return;
    void load();
  }, [verseId, user, ready]);

  async function load() {
    "background only";
    if (!httpClient) return;
    try {
      const meta = (await httpClient.query("verseLikes:meta", { verseId })) as Meta;
      setCount(meta.count);
      setMine(meta.mine);
    } catch (err) {
      console.error(err);
    }
  }

  async function toggle() {
    "background only";
    if (!httpClient || !user || busy) return;
    // Optimistic — reflect the tap immediately, reconcile on the result.
    const nextMine = !mine;
    setMine(nextMine);
    setCount((c) => Math.max(0, c + (nextMine ? 1 : -1)));
    setBusy(true);
    try {
      const res = (await httpClient.mutation("verseLikes:toggle", { verseId })) as { liked: boolean };
      setMine(res.liked);
    } catch (err) {
      console.error(err);
      // Roll back on failure.
      setMine(!nextMine);
      setCount((c) => Math.max(0, c + (nextMine ? -1 : 1)));
    } finally {
      setBusy(false);
    }
  }

  if (!ready) return null;

  const label = user ? (mine ? "Appreciated" : "Appreciate") : "Appreciate";

  return (
    <view
      bindtap={user ? toggle : undefined}
      style={{
        flexDirection: "row",
        alignItems: "center",
        gap: 8,
        alignSelf: "flex-start",
        paddingTop: 8,
        paddingBottom: 8,
        paddingLeft: 14,
        paddingRight: 14,
        borderRadius: 16,
        borderWidth: 1,
        borderColor: mine ? C.gold : C.line,
        backgroundColor: mine ? "#1c1a12" : C.cardAlt,
        opacity: user ? 1 : 0.6,
      }}
    >
      <text style={{ color: mine ? C.gold : C.goldMuted, fontSize: 14 }}>
        {mine ? "❋" : "✧"}
      </text>
      <text style={{ color: mine ? C.gold : C.goldMuted, fontSize: 13, letterSpacing: 0.5 }}>
        {label}
        {count > 0 ? `  ·  ${count}` : ""}
      </text>
    </view>
  );
}

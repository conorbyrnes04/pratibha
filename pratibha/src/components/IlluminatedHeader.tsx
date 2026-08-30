import { useEffect, useState } from "@lynx-js/react";
import { useAuth } from "../auth/AuthProvider";
import { useConvex } from "../convex/ConvexProvider";
import { isConvexConfigured } from "../convex/httpClient";
import { C, SERIF } from "../lib/theme";
import { sumiGlyph, type InkState } from "../lib/sumi";
import { SumiGlyph } from "./SumiGlyph";

type Meta = { count: number; mine: boolean; signedIn: boolean };

// The crown of a passage: its sumi mark, breathing, painted by the reader's own
// engagement — bone while you are reading, gold once you appreciate it. The
// mark and the Appreciate control share one state, so a tap lights the crown.
export function IlluminatedHeader({
  verseId,
  collection,
  section,
  title,
}: {
  verseId: string;
  collection?: string;
  section?: string;
  title: string;
}) {
  const { user } = useAuth();
  const { httpClient } = useConvex();
  const ready = Boolean(httpClient && isConvexConfigured());
  const [count, setCount] = useState(0);
  const [mine, setMine] = useState(false);
  const [busy, setBusy] = useState(false);

  const glyph = sumiGlyph(collection || verseId);
  const state: InkState = mine ? "recognized" : "arising";

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
    const next = !mine;
    setMine(next);
    setCount((c) => Math.max(0, c + (next ? 1 : -1)));
    setBusy(true);
    try {
      const res = (await httpClient.mutation("verseLikes:toggle", { verseId })) as { liked: boolean };
      setMine(res.liked);
    } catch (err) {
      console.error(err);
      setMine(!next);
      setCount((c) => Math.max(0, c + (next ? -1 : 1)));
    } finally {
      setBusy(false);
    }
  }

  return (
    <view style={{ alignItems: "center", marginBottom: 26 }}>
      {/* The crown always breathes; its color carries the state. */}
      <SumiGlyph glyph={glyph} state={state} size={78} breath />

      {collection ? (
        <text
          style={{ color: C.goldMuted, fontSize: 11, letterSpacing: 2, textTransform: "uppercase", marginTop: 16, textAlign: "center" }}
        >
          {collection}
          {section ? `  ·  ${section}` : ""}
        </text>
      ) : null}

      <text
        style={{ color: C.gold, fontSize: 27, fontWeight: "bold", fontFamily: SERIF, textAlign: "center", marginTop: 8 }}
      >
        {title}
      </text>

      {ready ? (
        <view
          bindtap={user ? toggle : undefined}
          style={{
            flexDirection: "row",
            alignItems: "center",
            gap: 8,
            marginTop: 16,
            paddingTop: 8,
            paddingBottom: 8,
            paddingLeft: 16,
            paddingRight: 16,
            borderRadius: 999,
            borderWidth: 1,
            borderColor: mine ? C.gold : C.line,
            backgroundColor: mine ? "#1c1a12" : C.cardAlt,
            opacity: user ? 1 : 0.6,
          }}
        >
          <text style={{ color: mine ? C.gold : C.goldMuted, fontSize: 14 }}>{mine ? "❋" : "✧"}</text>
          <text style={{ color: mine ? C.gold : C.goldMuted, fontSize: 13, letterSpacing: 0.5 }}>
            {mine ? "Appreciated" : "Appreciate"}
            {count > 0 ? `  ·  ${count}` : ""}
          </text>
        </view>
      ) : null}
    </view>
  );
}

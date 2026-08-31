import { useEffect, useState } from "@lynx-js/react";
import { useAuth } from "../auth/AuthProvider";
import { useConvex } from "../convex/ConvexProvider";
import { isConvexConfigured } from "../convex/httpClient";
import { C } from "../lib/theme";

type Mine = {
  body: string;
  status: "private" | "offered" | "hidden";
} | null;

export function StudentCommentary({
  verseId,
  verseTitle,
  onKeepFolio,
}: {
  verseId: string;
  verseTitle: string;
  onKeepFolio?: () => void;
}) {
  const { user } = useAuth();
  const { httpClient } = useConvex();
  const ready = Boolean(httpClient && isConvexConfigured());
  const [body, setBody] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [status, setStatus] = useState("");
  const [inManuscript, setInManuscript] = useState(false);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (!ready || !user) return;
    void load();
  }, [verseId, user, ready]);

  async function load() {
    "background only";
    if (!httpClient) return;
    try {
      const [mine, profile, has] = await Promise.all([
        httpClient.query("studentCommentaries:getMine", { verseId }) as Promise<Mine>,
        httpClient.query("profiles:getMine", {}) as Promise<{ displayName?: string } | null>,
        httpClient.query("manuscripts:hasVerse", { verseId }) as Promise<boolean>,
      ]);
      setBody(mine?.body ?? "");
      setStatus(mine?.status ?? "");
      if (profile?.displayName) setDisplayName(profile.displayName);
      setInManuscript(Boolean(has));
    } catch (err) {
      console.error(err);
    }
  }

  async function save(next: "private" | "offered") {
    "background only";
    if (!httpClient || !body.trim()) return;
    setBusy(true);
    setError("");
    try {
      await httpClient.mutation("studentCommentaries:upsert", {
        verseId,
        verseTitle,
        body,
        status: next,
        displayName: displayName.trim() || undefined,
      });
      setStatus(next);
    } catch (err: any) {
      setError(err?.message || "Could not save.");
    } finally {
      setBusy(false);
    }
  }

  async function withdraw() {
    "background only";
    if (!httpClient) return;
    setBusy(true);
    setError("");
    try {
      await httpClient.mutation("studentCommentaries:withdraw", { verseId });
      setStatus("private");
    } catch (err: any) {
      setError(err?.message || "Could not withdraw.");
    } finally {
      setBusy(false);
    }
  }

  async function removeFromManuscript() {
    "background only";
    if (!httpClient) return;
    setBusy(true);
    setError("");
    try {
      await httpClient.mutation("manuscripts:removeVerse", { verseId });
      setInManuscript(false);
    } catch (err: any) {
      setError(err?.message || "Could not update the manuscript.");
    } finally {
      setBusy(false);
    }
  }

  function saveToManuscript() {
    if (onKeepFolio) {
      onKeepFolio();
      return;
    }
    void addWithoutDesign();
  }

  async function addWithoutDesign() {
    "background only";
    if (!httpClient) return;
    setBusy(true);
    setError("");
    try {
      await httpClient.mutation("manuscripts:addVerse", { verseId, verseTitle });
      setInManuscript(true);
    } catch (err: { message?: string }) {
      setError(err?.message || "Could not update the manuscript.");
    } finally {
      setBusy(false);
    }
  }

  if (!user || !ready) {
    return (
      <view style={{ marginBottom: 24 }}>
        <text style={{ color: C.goldMuted, fontSize: 11, letterSpacing: 1.5, textTransform: "uppercase", marginBottom: 8 }}>
          Your commentary
        </text>
        <text style={{ color: C.muted, fontSize: 14, lineHeight: 1.6 }}>
          Sign in to write your own reading of this verse.
        </text>
      </view>
    );
  }

  return (
    <view style={{ marginBottom: 24 }}>
      <text style={{ color: C.goldMuted, fontSize: 11, letterSpacing: 1.5, textTransform: "uppercase", marginBottom: 8 }}>
        Your commentary
      </text>
      <text style={{ color: C.muted, fontSize: 13, lineHeight: 1.55, marginBottom: 10 }}>
        {status === "offered" ? "Offered to the circle." : status ? "Saved privately." : "Private until you offer it."}
      </text>
      <textarea
        value={body}
        bindinput={(e: any) => setBody(e.detail?.value ?? e.target?.value ?? "")}
        placeholder="What does this verse ask of you?"
        rows={5}
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
        placeholder="Name on offered readings"
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
      {error ? (
        <text style={{ color: C.danger, fontSize: 13, marginBottom: 10 }}>{error}</text>
      ) : null}
      <view style={{ flexDirection: "row", flexWrap: "wrap", gap: 8 }}>
        <Tap label={busy ? "…" : "Save privately"} onTap={() => void save("private")} dim={!body.trim() || busy} />
        <Tap
          label={busy ? "…" : status === "offered" ? "Update offered" : "Offer to this verse"}
          onTap={() => void save("offered")}
          dim={!body.trim() || busy}
        />
        {status === "offered" ? <Tap label="Withdraw" onTap={() => void withdraw()} dim={busy} /> : null}
        {inManuscript ? (
          <>
            <Tap label="Edit card" onTap={saveToManuscript} dim={busy} />
            <Tap label="Remove from manuscript" onTap={() => void removeFromManuscript()} dim={busy} />
          </>
        ) : (
          <Tap label="Save to my manuscript" onTap={saveToManuscript} dim={busy} />
        )}
      </view>
    </view>
  );
}

function Tap({ label, onTap, dim }: { label: string; onTap: () => void; dim?: boolean }) {
  return (
    <view
      bindtap={dim ? undefined : onTap}
      style={{
        paddingTop: 8,
        paddingBottom: 8,
        paddingLeft: 12,
        paddingRight: 12,
        backgroundColor: dim ? C.cardAlt : C.gold,
        borderRadius: 6,
      }}
    >
      <text style={{ color: dim ? C.muted : "#000", fontSize: 12, fontWeight: "600" }}>{label}</text>
    </view>
  );
}

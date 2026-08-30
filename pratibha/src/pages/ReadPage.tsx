import React, { useEffect, useState } from "react";
import { fetchPassages, fetchVerse, getLayer, type Passage } from "../lib/corpus";

// Pratibha manuscript palette (amber/gold on deep dark).
const C = {
  bg: "#0a0a0f",
  card: "#14141f",
  cardAlt: "#1a1a2e",
  gold: "#f0c979",
  goldMuted: "#c9a86a",
  read: "#e8e4dc",
  script: "#efe8d8",
  muted: "#9a958c",
  faint: "#6c6862",
  line: "#2a2a3a",
};

const SERIF = "'Iowan Old Style', 'Palatino', 'Georgia', serif";
const SCRIPT = "'Noto Serif Devanagari', 'Noto Serif SC', 'Noto Serif', 'Georgia', serif";

function stripBold(s: string): string {
  return s.replace(/\*\*/g, "").trim();
}

// key_terms / resonances bodies are lines shaped like `**term** — body`.
type TermEntry = { term: string; body: string };
function parseTerms(text: string): TermEntry[] {
  return text
    .split(/\n+/)
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => {
      const m = line.match(/^\*\*(.+?)\*\*\s*(?:[—:-]\s*)?(.*)$/);
      if (m) return { term: stripBold(m[1]).replace(/:$/, ""), body: stripBold(m[2]) };
      return { term: "", body: stripBold(line) };
    });
}

function LayerLabel({ children }: { children: React.ReactNode }) {
  return (
    <text style={{ color: C.goldMuted, fontSize: 11, letterSpacing: 1.5, textTransform: "uppercase", marginBottom: 8 }}>
      {children}
    </text>
  );
}

function TermList({ entries }: { entries: TermEntry[] }) {
  return (
    <view style={{ gap: 12 }}>
      {entries.map((e, i) => (
        <view key={String(i)}>
          {e.term ? (
            <text style={{ color: C.gold, fontSize: 15, fontWeight: "600", marginBottom: 2 }}>{e.term}</text>
          ) : null}
          <text style={{ color: C.muted, fontSize: 14, lineHeight: 1.55 }}>{e.body}</text>
        </view>
      ))}
    </view>
  );
}

function Detail({ passage, onBack }: { passage: Passage; onBack: () => void }) {
  const original = getLayer(passage, "original");
  const iast = getLayer(passage, "iast");
  const translation = getLayer(passage, "translation");
  const literal = getLayer(passage, "literal");
  const commentary = getLayer(passage, "commentary");
  const keyTerms = getLayer(passage, "key_terms");
  const resonances = getLayer(passage, "resonances");
  const practice = getLayer(passage, "practice");
  const themes = passage.themes || [];

  return (
    <scroll-view style={{ flex: 1, backgroundColor: C.bg }}>
      <view style={{ padding: 22 }}>
        <view
          bindtap={onBack}
          style={{
            marginBottom: 22,
            paddingTop: 8,
            paddingBottom: 8,
            paddingLeft: 16,
            paddingRight: 16,
            backgroundColor: C.cardAlt,
            borderRadius: 6,
            alignSelf: "flex-start",
          }}
        >
          <text style={{ color: C.gold, fontSize: 14 }}>← Library</text>
        </view>

        {passage.collection ? (
          <text style={{ color: C.faint, fontSize: 12, letterSpacing: 1.5, textTransform: "uppercase", marginBottom: 6 }}>
            {passage.collection}
            {passage.section ? `  ·  ${passage.section}` : ""}
          </text>
        ) : null}
        <text style={{ color: C.gold, fontSize: 26, fontWeight: "bold", fontFamily: SERIF, marginBottom: 24 }}>
          {passage.title || passage._id}
        </text>

        {original ? (
          <view style={{ marginBottom: 24, paddingLeft: 14, borderLeftWidth: 2, borderLeftColor: C.goldMuted }}>
            <text style={{ color: C.script, fontSize: 21, lineHeight: 1.8, fontFamily: SCRIPT }}>{original}</text>
            {iast ? (
              <text style={{ color: C.goldMuted, fontSize: 14, lineHeight: 1.7, fontStyle: "italic", marginTop: 10 }}>
                {iast}
              </text>
            ) : null}
          </view>
        ) : null}

        {translation ? (
          <view style={{ marginBottom: 24 }}>
            <LayerLabel>Translation</LayerLabel>
            <text style={{ color: C.read, fontSize: 18, lineHeight: 1.7, fontFamily: SERIF }}>{translation}</text>
          </view>
        ) : null}

        {literal ? (
          <view style={{ marginBottom: 24 }}>
            <LayerLabel>Literal</LayerLabel>
            <text style={{ color: C.muted, fontSize: 15, lineHeight: 1.6 }}>{literal}</text>
          </view>
        ) : null}

        {commentary ? (
          <view style={{ marginBottom: 24 }}>
            <LayerLabel>Commentary</LayerLabel>
            <text style={{ color: C.read, fontSize: 15, lineHeight: 1.7 }}>{commentary}</text>
          </view>
        ) : null}

        {keyTerms ? (
          <view style={{ marginBottom: 24 }}>
            <LayerLabel>Key Terms</LayerLabel>
            <TermList entries={parseTerms(keyTerms)} />
          </view>
        ) : null}

        {resonances ? (
          <view style={{ marginBottom: 24 }}>
            <LayerLabel>Resonances</LayerLabel>
            <TermList entries={parseTerms(resonances)} />
          </view>
        ) : null}

        {practice ? (
          <view
            style={{
              marginBottom: 24,
              padding: 16,
              backgroundColor: "#1c1a12",
              borderRadius: 8,
              borderLeftWidth: 3,
              borderLeftColor: C.gold,
            }}
          >
            <LayerLabel>Practice</LayerLabel>
            <text style={{ color: C.read, fontSize: 15, lineHeight: 1.7 }}>{practice}</text>
          </view>
        ) : null}

        {themes.length ? (
          <view style={{ flexDirection: "row", flexWrap: "wrap", gap: 8, marginTop: 4 }}>
            {themes.map((t) => (
              <view
                key={t}
                style={{ paddingTop: 4, paddingBottom: 4, paddingLeft: 10, paddingRight: 10, backgroundColor: C.cardAlt, borderRadius: 12 }}
              >
                <text style={{ color: C.goldMuted, fontSize: 12 }}>{t}</text>
              </view>
            ))}
          </view>
        ) : null}
      </view>
    </scroll-view>
  );
}

export function ReadPage() {
  const [verses, setVerses] = useState<Passage[]>([]);
  const [detail, setDetail] = useState<Passage | null>(null);
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadVerses() {
      try {
        setVerses(await fetchPassages(40));
      } catch (err) {
        console.error("Failed to load verses:", err);
        setError("Could not reach the corpus server. Start FastAPI on port 8000.");
      } finally {
        setLoading(false);
      }
    }
    void loadVerses();
  }, []);

  async function openVerse(v: Passage) {
    setDetailLoading(true);
    try {
      // Pull the full unit (list payloads are slim / missing most layers).
      setDetail(await fetchVerse(v._id));
    } catch (err) {
      console.error("Failed to load verse:", err);
      setDetail(v); // fall back to the slim list item
    } finally {
      setDetailLoading(false);
    }
  }

  if (loading) {
    return (
      <view style={{ flex: 1, padding: 20, backgroundColor: C.bg }}>
        <text style={{ color: C.muted }}>Loading passages…</text>
      </view>
    );
  }

  if (detail) {
    return <Detail passage={detail} onBack={() => setDetail(null)} />;
  }

  return (
    <scroll-view style={{ flex: 1, backgroundColor: C.bg }}>
      <view style={{ padding: 22 }}>
        <text style={{ color: C.gold, fontSize: 26, fontWeight: "bold", fontFamily: SERIF, marginBottom: 8 }}>Library</text>
        <text style={{ color: C.muted, fontSize: 14, marginBottom: 22 }}>
          {error || (detailLoading ? "Opening…" : "Browse the canonical collection")}
        </text>

        <view style={{ gap: 12 }}>
          {verses.map((verse) => {
            const preview = getLayer(verse, "translation");
            return (
              <view
                key={verse._id}
                bindtap={() => void openVerse(verse)}
                style={{
                  padding: 16,
                  backgroundColor: C.card,
                  borderRadius: 8,
                  borderLeftWidth: 4,
                  borderLeftColor: C.gold,
                }}
              >
                {verse.collection ? (
                  <text style={{ color: C.faint, fontSize: 11, letterSpacing: 1, textTransform: "uppercase", marginBottom: 4 }}>
                    {verse.collection}
                  </text>
                ) : null}
                <text style={{ color: C.gold, fontSize: 16, fontWeight: "600", fontFamily: SERIF, marginBottom: 6 }}>
                  {verse.title || verse._id}
                </text>
                {preview ? <text style={{ color: C.muted, fontSize: 14, lineHeight: 1.5 }}>{preview.slice(0, 200)}</text> : null}
              </view>
            );
          })}
        </view>
      </view>
    </scroll-view>
  );
}

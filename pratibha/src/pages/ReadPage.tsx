import { useEffect, useMemo, useState } from "@lynx-js/react";
import {
  fetchPassages,
  fetchVerse,
  getLayer,
  siblingsInCollection,
  type Passage,
} from "../lib/corpus";
import { C, SCRIPT, SERIF } from "../lib/theme";
import { StudentCommentary } from "../components/StudentCommentary";
import { CircleReadings } from "../components/CircleReadings";
import { ShareComposer } from "../components/ShareComposer";

function stripBold(s: string): string {
  return s.replace(/\*\*/g, "").trim();
}

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

function isLongOriginal(text: string): boolean {
  const body = text.trim();
  if (/[\u4E00-\u9FFF]/.test(body)) return body.length > 72;
  if (/[\u0900-\u097F]|[ༀ-࿿]/.test(body)) return body.length > 90;
  return body.length > 220;
}

function condenseOriginal(text: string): string {
  const lines = text.split(/\n+/).map((line) => line.trim()).filter(Boolean);
  if (lines.length > 3) return `${lines.slice(0, 3).join("\n")}…`;
  if (text.length > 80) return `${text.trim().slice(0, 72)}…`;
  return text;
}

function LongOriginal({ text }: { text: string }) {
  const [open, setOpen] = useState(false);
  const long = isLongOriginal(text);
  return (
    <view>
      <text style={{ color: C.script, fontSize: 21, lineHeight: 1.8, fontFamily: SCRIPT }}>
        {long && !open ? condenseOriginal(text) : text}
      </text>
      {long ? (
        <view
          bindtap={() => setOpen((v) => !v)}
          style={{ marginTop: 10, alignSelf: "flex-start" }}
        >
          <text style={{ color: C.goldMuted, fontSize: 12, letterSpacing: 1, textTransform: "uppercase" }}>
            {open ? "Collapse original" : "Expand original"}
          </text>
        </view>
      ) : null}
    </view>
  );
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

function Chip({
  label,
  active,
  onTap,
}: {
  label: string;
  active?: boolean;
  onTap: () => void;
}) {
  return (
    <view
      bindtap={onTap}
      style={{
        paddingTop: 6,
        paddingBottom: 6,
        paddingLeft: 12,
        paddingRight: 12,
        backgroundColor: active ? C.gold : C.cardAlt,
        borderRadius: 14,
      }}
    >
      <text style={{ color: active ? "#000" : C.goldMuted, fontSize: 12 }}>{label}</text>
    </view>
  );
}

export function PassageDetail({
  passage,
  onBack,
  backLabel = "← Library",
  onPrev,
  onNext,
  prevTitle,
  nextTitle,
}: {
  passage: Passage;
  onBack: () => void;
  backLabel?: string;
  onPrev?: () => void;
  onNext?: () => void;
  prevTitle?: string;
  nextTitle?: string;
}) {
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
          <text style={{ color: C.gold, fontSize: 14 }}>{backLabel}</text>
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
            <LongOriginal text={original} />
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

        <ShareComposer passage={passage} />
        <StudentCommentary verseId={passage._id} verseTitle={passage.title || passage._id} />
        <CircleReadings verseId={passage._id} />

        {themes.length ? (
          <view style={{ flexDirection: "row", flexWrap: "wrap", gap: 8, marginTop: 4, marginBottom: 20 }}>
            {themes.map((t) => (
              <view
                key={t}
                style={{
                  paddingTop: 4,
                  paddingBottom: 4,
                  paddingLeft: 10,
                  paddingRight: 10,
                  backgroundColor: C.cardAlt,
                  borderRadius: 12,
                }}
              >
                <text style={{ color: C.goldMuted, fontSize: 12 }}>{t}</text>
              </view>
            ))}
          </view>
        ) : null}

        {onPrev || onNext ? (
          <view style={{ flexDirection: "row", justifyContent: "space-between", gap: 12, marginTop: 8 }}>
            <view
              bindtap={onPrev}
              style={{
                flex: 1,
                padding: 12,
                backgroundColor: C.card,
                borderRadius: 8,
                opacity: onPrev ? 1 : 0.35,
              }}
            >
              <text style={{ color: C.faint, fontSize: 11, marginBottom: 4 }}>Previous</text>
              <text style={{ color: C.gold, fontSize: 13 }}>{prevTitle || "—"}</text>
            </view>
            <view
              bindtap={onNext}
              style={{
                flex: 1,
                padding: 12,
                backgroundColor: C.card,
                borderRadius: 8,
                opacity: onNext ? 1 : 0.35,
              }}
            >
              <text style={{ color: C.faint, fontSize: 11, marginBottom: 4, textAlign: "right" }}>Next</text>
              <text style={{ color: C.gold, fontSize: 13, textAlign: "right" }}>{nextTitle || "—"}</text>
            </view>
          </view>
        ) : null}
      </view>
    </scroll-view>
  );
}

export function ReadPage({ openVerseId }: { openVerseId?: string | null }) {
  const [verses, setVerses] = useState<Passage[]>([]);
  const [detail, setDetail] = useState<Passage | null>(null);
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");
  const [collection, setCollection] = useState("all");

  useEffect(() => {
    async function loadVerses() {
      try {
        setVerses(await fetchPassages());
      } catch (err) {
        console.error("Failed to load verses:", err);
        setError("Could not reach the corpus server. Start FastAPI on port 8000.");
      } finally {
        setLoading(false);
      }
    }
    void loadVerses();
  }, []);

  useEffect(() => {
    if (!openVerseId) return;
    void openVerse({ _id: openVerseId } as Passage);
  }, [openVerseId]);

  const collections = useMemo(() => {
    const set = new Set<string>();
    for (const v of verses) {
      if (v.collection?.trim()) set.add(v.collection.trim());
    }
    return [...set].sort((a, b) => a.localeCompare(b));
  }, [verses]);

  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return verses.filter((v) => {
      if (collection !== "all" && (v.collection || "").trim() !== collection) return false;
      if (!needle) return true;
      const hay = [v.title, v.collection, v.section, getLayer(v, "translation")].join(" ").toLowerCase();
      return hay.includes(needle);
    });
  }, [verses, collection, query]);

  async function openVerse(v: Passage) {
    setDetailLoading(true);
    try {
      setDetail(await fetchVerse(v._id));
    } catch (err) {
      console.error("Failed to load verse:", err);
      setDetail(v);
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
    const siblings = siblingsInCollection(verses, detail.collection);
    const idx = siblings.findIndex((v) => v._id === detail._id);
    const prev = idx > 0 ? siblings[idx - 1] : null;
    const next = idx >= 0 && idx < siblings.length - 1 ? siblings[idx + 1] : null;
    return (
      <PassageDetail
        passage={detail}
        onBack={() => setDetail(null)}
        onPrev={prev ? () => void openVerse(prev) : undefined}
        onNext={next ? () => void openVerse(next) : undefined}
        prevTitle={prev?.title || prev?._id}
        nextTitle={next?.title || next?._id}
      />
    );
  }

  return (
    <scroll-view style={{ flex: 1, backgroundColor: C.bg }}>
      <view style={{ padding: 22 }}>
        <text style={{ color: C.gold, fontSize: 26, fontWeight: "bold", fontFamily: SERIF, marginBottom: 8 }}>
          Library
        </text>
        <text style={{ color: C.muted, fontSize: 14, marginBottom: 16 }}>
          {error || (detailLoading ? "Opening…" : `${filtered.length} passages`)}
        </text>

        <input
          type="text"
          value={query}
          bindinput={(e: any) => setQuery(e.detail?.value ?? e.target?.value ?? "")}
          placeholder="Search title or collection"
          style={{
            width: "100%",
            padding: 10,
            marginBottom: 14,
            backgroundColor: C.card,
            border: "1px solid #333",
            borderRadius: 6,
            color: "#fff",
            fontSize: 14,
          }}
        />

        <view style={{ flexDirection: "row", flexWrap: "wrap", gap: 8, marginBottom: 18 }}>
          <Chip label="All" active={collection === "all"} onTap={() => setCollection("all")} />
          {collections.map((name) => (
            <Chip key={name} label={name} active={collection === name} onTap={() => setCollection(name)} />
          ))}
        </view>

        <view style={{ gap: 12 }}>
          {filtered.map((verse) => {
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
                  <text
                    style={{
                      color: C.faint,
                      fontSize: 11,
                      letterSpacing: 1,
                      textTransform: "uppercase",
                      marginBottom: 4,
                    }}
                  >
                    {verse.collection}
                  </text>
                ) : null}
                <text style={{ color: C.gold, fontSize: 16, fontWeight: "600", fontFamily: SERIF, marginBottom: 6 }}>
                  {verse.title || verse._id}
                </text>
                {preview ? (
                  <text style={{ color: C.muted, fontSize: 14, lineHeight: 1.5 }}>{preview.slice(0, 200)}</text>
                ) : null}
              </view>
            );
          })}
        </view>
      </view>
    </scroll-view>
  );
}

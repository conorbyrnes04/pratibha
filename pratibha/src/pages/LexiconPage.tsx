import { useEffect, useMemo, useState } from "@lynx-js/react";
import { fetchLemma, fetchLexicon, type LexiconItem } from "../lib/corpus";
import { C, SCRIPT, SERIF } from "../lib/theme";

function fold(s: string): string {
  return s.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
}

export function LexiconPage() {
  const [items, setItems] = useState<LexiconItem[]>([]);
  const [detail, setDetail] = useState<LexiconItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");
  const [tradition, setTradition] = useState("all");

  useEffect(() => {
    fetchLexicon(500)
      .then((rows) => {
        setItems(rows);
        if (!rows.length) setError("The lexicon is empty — lemmas may still be loading.");
      })
      .catch(() => setError("Could not reach the lexicon API. Start FastAPI on port 8000."))
      .finally(() => setLoading(false));
  }, []);

  const traditions = useMemo(() => {
    const set = new Set<string>();
    for (const item of items) {
      for (const t of item.traditions || []) {
        if (t.trim()) set.add(t.trim());
      }
    }
    return [...set].sort((a, b) => a.localeCompare(b));
  }, [items]);

  const filtered = useMemo(() => {
    const needle = fold(query.trim());
    return items.filter((item) => {
      if (tradition !== "all" && !(item.traditions || []).includes(tradition)) return false;
      if (!needle) return true;
      const hay = fold(
        [item.id, item.short, ...(item.aliases || []), ...(item.traditions || []), ...Object.values(item.scripts || {})].join(" "),
      );
      return hay.includes(needle);
    });
  }, [items, query, tradition]);

  async function openLemma(id: string) {
    try {
      setDetail(await fetchLemma(id));
    } catch {
      const fallback = items.find((i) => i.id === id);
      if (fallback) setDetail(fallback);
    }
  }

  if (loading) {
    return (
      <view style={{ padding: 22, backgroundColor: C.bg }}>
        <text style={{ color: C.muted }}>Loading lexicon…</text>
      </view>
    );
  }

  if (detail) {
    const script = detail.scripts?.devanagari || detail.scripts?.greek || detail.scripts?.chinese || detail.scripts?.arabic || "";
    const roman = detail.scripts?.iast || detail.scripts?.pinyin || detail.scripts?.latin || "";
    return (
      <scroll-view style={{ flex: 1, backgroundColor: C.bg }}>
        <view style={{ padding: 22 }}>
          <view
            bindtap={() => setDetail(null)}
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
            <text style={{ color: C.gold, fontSize: 14 }}>← Lexicon</text>
          </view>
          {script ? (
            <text style={{ color: C.script, fontSize: 28, fontFamily: SCRIPT, marginBottom: 6 }}>{script}</text>
          ) : null}
          <text style={{ color: C.gold, fontSize: 26, fontWeight: "bold", fontFamily: SERIF, marginBottom: 8 }}>
            {roman || detail.id}
          </text>
          <text style={{ color: C.muted, fontSize: 15, marginBottom: 16 }}>{detail.short}</text>
          {(detail.traditions || []).length ? (
            <text style={{ color: C.faint, fontSize: 12, marginBottom: 18 }}>{(detail.traditions || []).join(" · ")}</text>
          ) : null}
          <view style={{ gap: 16 }}>
            {(detail.senses || []).map((sense, i) => (
              <view key={sense.id || String(i)} style={{ padding: 14, backgroundColor: C.card, borderRadius: 8 }}>
                <text style={{ color: C.goldMuted, fontSize: 12, letterSpacing: 1, textTransform: "uppercase", marginBottom: 6 }}>
                  {sense.label || `Sense ${i + 1}`}
                </text>
                <text style={{ color: C.read, fontSize: 15, lineHeight: 1.6 }}>{sense.body || sense.short || ""}</text>
                {sense.etymology ? (
                  <text style={{ color: C.muted, fontSize: 13, marginTop: 8, fontStyle: "italic" }}>{sense.etymology}</text>
                ) : null}
              </view>
            ))}
          </view>
        </view>
      </scroll-view>
    );
  }

  return (
    <scroll-view style={{ flex: 1, backgroundColor: C.bg }}>
      <view style={{ padding: 22 }}>
        <text style={{ color: C.gold, fontSize: 26, fontWeight: "bold", fontFamily: SERIF, marginBottom: 8 }}>
          Lexicon
        </text>
        <text style={{ color: C.muted, fontSize: 14, marginBottom: 16 }}>
          {error || `${filtered.length} lemmas`}
        </text>
        <input
          type="text"
          value={query}
          bindinput={(e: any) => setQuery(e.detail?.value ?? e.target?.value ?? "")}
          placeholder="Search a term"
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
          <Chip label="All" active={tradition === "all"} onTap={() => setTradition("all")} />
          {traditions.map((name) => (
            <Chip key={name} label={name} active={tradition === name} onTap={() => setTradition(name)} />
          ))}
        </view>
        <view style={{ gap: 10 }}>
          {filtered.map((item) => (
            <view
              key={item.id}
              bindtap={() => void openLemma(item.id)}
              style={{ padding: 14, backgroundColor: C.card, borderRadius: 8 }}
            >
              <text style={{ color: C.gold, fontSize: 16, fontWeight: "600", fontFamily: SERIF, marginBottom: 4 }}>
                {item.scripts?.iast || item.id}
              </text>
              <text style={{ color: C.muted, fontSize: 13 }}>{item.short}</text>
            </view>
          ))}
        </view>
      </view>
    </scroll-view>
  );
}

function Chip({ label, active, onTap }: { label: string; active?: boolean; onTap: () => void }) {
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

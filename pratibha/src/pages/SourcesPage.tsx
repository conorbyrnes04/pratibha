import React, { useEffect, useState } from "react";
import { fetchSources, type SourceItem } from "../lib/corpus";
import { C, SERIF } from "../lib/theme";

export function SourcesPage() {
  const [items, setItems] = useState<SourceItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchSources()
      .then(setItems)
      .catch(() => setError("Could not reach the sources API. Start FastAPI on port 8000."))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <view style={{ padding: 22, backgroundColor: C.bg }}>
        <text style={{ color: C.muted }}>Loading sources…</text>
      </view>
    );
  }

  return (
    <scroll-view style={{ flex: 1, backgroundColor: C.bg }}>
      <view style={{ padding: 22 }}>
        <text style={{ color: C.gold, fontSize: 26, fontWeight: "bold", fontFamily: SERIF, marginBottom: 8 }}>
          Sources
        </text>
        <text style={{ color: C.muted, fontSize: 14, marginBottom: 18 }}>
          {error || "Where each collection comes from, and on what terms."}
        </text>
        <view style={{ gap: 12 }}>
          {items.map((item) => (
            <view key={item.id || item.collection} style={{ padding: 16, backgroundColor: C.card, borderRadius: 8 }}>
              <text style={{ color: C.gold, fontSize: 18, fontWeight: "600", fontFamily: SERIF, marginBottom: 4 }}>
                {item.collection}
              </text>
              <text style={{ color: C.muted, fontSize: 13, marginBottom: 8 }}>{item.tradition}</text>
              <text style={{ color: C.faint, fontSize: 12, marginBottom: 10 }}>
                {item.license_label}
                {item.provenance_tier_label ? ` · ${item.provenance_tier_label}` : ""}
                {item.passages_in_corpus ? ` · ${item.passages_in_corpus} passages` : ""}
                {item.coverage ? ` · ${item.coverage}` : ""}
              </text>
              {item.original_work ? (
                <text style={{ color: C.read, fontSize: 14, marginBottom: 8 }}>{item.original_work}</text>
              ) : null}
              {item.editorial_note ? (
                <text style={{ color: C.muted, fontSize: 13, lineHeight: 1.55 }}>{item.editorial_note}</text>
              ) : null}
            </view>
          ))}
        </view>
      </view>
    </scroll-view>
  );
}

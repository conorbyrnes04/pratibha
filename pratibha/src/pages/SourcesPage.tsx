import { useEffect, useMemo, useState } from "@lynx-js/react";
import { fetchSources, type SourceItem } from "../lib/corpus";
import { C, SERIF } from "../lib/theme";

/** Keep in lockstep with `web/src/lib/libraryTomes.ts` TRADITION_ORDER. */
const TRADITION_ORDER = [
  "Vedānta",
  "Yoga",
  "Kashmir Śaiva",
  "Buddhist",
  "Daoist",
  "Confucian",
  "Yoruba",
  "Dakota",
  "Hebrew",
  "Greek",
  "Christian",
  "Sufi",
] as const;

function groupSourcesByTradition(items: SourceItem[]) {
  const buckets = new Map<string, SourceItem[]>();
  for (const item of items) {
    const key = (item.tradition || "").trim() || item.collection;
    const list = buckets.get(key) || [];
    list.push(item);
    buckets.set(key, list);
  }
  const known = TRADITION_ORDER.filter((tradition) => buckets.has(tradition));
  const extra = [...buckets.keys()]
    .filter((tradition) => !(TRADITION_ORDER as readonly string[]).includes(tradition))
    .sort((a, b) => a.localeCompare(b));
  return [...known, ...extra].map((tradition) => ({
    tradition,
    items: (buckets.get(tradition) || []).sort((a, b) => a.collection.localeCompare(b.collection)),
  }));
}

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

  const shelves = useMemo(() => groupSourcesByTradition(items), [items]);

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
          {error || "Where each collection comes from, grouped by tradition."}
        </text>
        <view style={{ gap: 22 }}>
          {shelves.map((shelf) => (
            <view key={shelf.tradition} style={{ gap: 12 }}>
              <view style={{ flexDirection: "row", justifyContent: "space-between", alignItems: "baseline" }}>
                <text style={{ color: C.gold, fontSize: 13, letterSpacing: 1.4, textTransform: "uppercase" }}>
                  {shelf.tradition}
                </text>
                <text style={{ color: C.faint, fontSize: 12 }}>
                  {shelf.items.length} {shelf.items.length === 1 ? "text" : "texts"}
                </text>
              </view>
              {shelf.items.map((item) => (
                <view key={item.id || item.collection} style={{ padding: 16, backgroundColor: C.card, borderRadius: 8 }}>
                  <text style={{ color: C.gold, fontSize: 18, fontWeight: "600", fontFamily: SERIF, marginBottom: 4 }}>
                    {item.collection}
                  </text>
                  <text style={{ color: C.faint, fontSize: 12, marginBottom: 10 }}>
                    {item.license_label}
                    {item.provenance_tier_label ? ` · ${item.provenance_tier_label}` : ""}
                    {item.passages_in_corpus ? ` · ${item.passages_in_corpus} passages` : " · Coming soon"}
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
          ))}
        </view>
      </view>
    </scroll-view>
  );
}

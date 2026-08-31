import { useEffect, useState } from "@lynx-js/react";
import { fetchVerse, layerText, type Passage } from "../lib/corpus";
import { CircleReadings } from "../components/CircleReadings";
import { ShareComposer } from "../components/ShareComposer";
import { currentEssentialSit, loadProgress } from "../lib/learn";

export function HomePage({ onNavigate }: { onNavigate?: (page: string) => void }) {
  const [sit] = useState(() => {
    const { progress, completedAt } = loadProgress();
    return currentEssentialSit(progress, completedAt);
  });
  const [verse, setVerse] = useState<Passage | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      if (!sit?.passageId) {
        setLoading(false);
        return;
      }
      try {
        setVerse(await fetchVerse(sit.passageId));
      } catch (err) {
        console.error("Failed to load today's gate:", err);
        setError("Could not reach the corpus server.");
      } finally {
        setLoading(false);
      }
    }
    void load();
  }, [sit?.passageId]);

  if (loading) {
    return (
      <view style={{ padding: 20 }}>
        <text style={{ color: "#999", fontSize: 14 }}>Opening today's gate…</text>
      </view>
    );
  }

  if (!sit) {
    return (
      <view style={{ padding: 20 }}>
        <text style={{ color: "#f0c979", fontSize: 24, fontWeight: "bold", marginBottom: 16 }}>
          Today
        </text>
        <text style={{ color: "#ccc", fontSize: 16 }} bindtap={() => onNavigate?.("learn")}>
          Open the path
        </text>
      </view>
    );
  }

  const translation = verse ? layerText(verse, "translation") : "";

  return (
    <view style={{ padding: 20 }}>
      <text style={{ color: "#999", fontSize: 12, textTransform: "uppercase", marginBottom: 8 }}>
        Today
      </text>
      <text style={{ color: "#f0c979", fontSize: 24, fontWeight: "bold", marginBottom: 12 }}>
        {sit.rested ? "Enough for today" : sit.title}
      </text>
      <text style={{ color: "#ccc", fontSize: 16, marginBottom: 16, lineHeight: "24px" }}>
        {sit.rested && sit.nextTitle
          ? `Tomorrow opens ${sit.nextTitle}.`
          : sit.orientation}
      </text>
      {translation ? (
        <text style={{ color: "#ddd", fontSize: 16, lineHeight: "26px", marginBottom: 24 }}>
          {translation}
        </text>
      ) : error ? (
        <text style={{ color: "#999", fontSize: 14, marginBottom: 24 }}>{error}</text>
      ) : null}
      <text
        style={{ color: "#f0c979", fontSize: 15, marginBottom: 20 }}
        bindtap={() => onNavigate?.("learn")}
      >
        {sit.rested ? "See the trail →" : "Enter this gate →"}
      </text>
      {verse ? <ShareComposer passage={verse} /> : null}
      {verse ? <CircleReadings verseId={verse._id} daily /> : null}
    </view>
  );
}

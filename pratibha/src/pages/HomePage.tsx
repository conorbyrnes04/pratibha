import React, { useEffect, useState } from "react";
import { fetchDaily, layerText, type Passage } from "../lib/corpus";

export function HomePage() {
  const [dailyPassage, setDailyPassage] = useState<Passage | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadDaily() {
      try {
        setDailyPassage(await fetchDaily());
      } catch (err) {
        console.error("Failed to load daily passage:", err);
        setError("Could not reach the corpus server. Start FastAPI on port 8000.");
      } finally {
        setLoading(false);
      }
    }
    void loadDaily();
  }, []);

  if (loading) {
    return (
      <view style={{ padding: 20 }}>
        <text style={{ color: "#999", fontSize: 14 }}>Loading today's passage...</text>
      </view>
    );
  }

  if (!dailyPassage) {
    return (
      <view style={{ padding: 20 }}>
        <text style={{ color: "#f0c979", fontSize: 24, fontWeight: "bold", marginBottom: 16 }}>
          Welcome to Pratibha
        </text>
        <text style={{ color: "#ccc", fontSize: 16, marginBottom: 12 }}>
          Living Manuscript of World Wisdom
        </text>
        <text style={{ color: "#999", fontSize: 14 }}>
          {error || "Explore contemplative wisdom texts across traditions."}
        </text>
      </view>
    );
  }

  const translation = layerText(dailyPassage, "translation");

  return (
    <view style={{ padding: 20 }}>
      <text style={{ color: "#999", fontSize: 12, textTransform: "uppercase", marginBottom: 8 }}>
        Today's Passage
      </text>
      <text style={{ color: "#f0c979", fontSize: 24, fontWeight: "bold", marginBottom: 12 }}>
        {dailyPassage.title || dailyPassage._id}
      </text>
      {dailyPassage.collection ? (
        <text style={{ color: "#ccc", fontSize: 14, marginBottom: 16 }}>{dailyPassage.collection}</text>
      ) : null}
      {translation ? (
        <text style={{ color: "#ddd", fontSize: 16, lineHeight: 1.6 }}>{translation}</text>
      ) : null}
    </view>
  );
}

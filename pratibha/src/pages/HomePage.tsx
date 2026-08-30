import React, { useEffect, useState } from "react";
import { convexFetch } from "../convex/httpClient";

export function HomePage() {
  const [dailyPassage, setDailyPassage] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDaily() {
      try {
        const response = await fetch("http://localhost:8000/daily");
        const data = await response.json();
        setDailyPassage(data);
      } catch (error) {
        console.error("Failed to load daily passage:", error);
      } finally {
        setLoading(false);
      }
    }
    loadDaily();
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
          Explore contemplative wisdom texts across traditions.
        </text>
      </view>
    );
  }

  return (
    <view style={{ padding: 20 }}>
      <text style={{ color: "#999", fontSize: 12, textTransform: "uppercase", marginBottom: 8 }}>
        Today's Passage
      </text>
      <text style={{ color: "#f0c979", fontSize: 24, fontWeight: "bold", marginBottom: 12 }}>
        {dailyPassage.title || dailyPassage._id}
      </text>
      {dailyPassage.collection && (
        <text style={{ color: "#ccc", fontSize: 14, marginBottom: 16 }}>
          {dailyPassage.collection}
        </text>
      )}
      {dailyPassage.pratibha_layers?.translation && (
        <text style={{ color: "#ddd", fontSize: 16, lineHeight: 1.6 }}>
          {dailyPassage.pratibha_layers.translation}
        </text>
      )}
    </view>
  );
}

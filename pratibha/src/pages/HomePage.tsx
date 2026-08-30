import React, { useEffect, useState } from "@lynx-js/react";
import { convexFetch } from "../convex/httpClient";
import { LikeButton } from "../components/LikeButton";
import { CommentSection } from "../components/CommentSection";
import { ShareButton } from "../components/ShareButton";

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
    <scroll-view style={{ flex: 1 }}>
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

        {/* Social actions */}
        {dailyPassage._id && (
          <view style={{ flexDirection: "row", gap: 12, marginBottom: 24, alignItems: "center" }}>
            <LikeButton verseId={dailyPassage._id} />
            <ShareButton
              verseId={dailyPassage._id}
              verseTitle={dailyPassage.title || dailyPassage._id}
              verseTranslation={dailyPassage.pratibha_layers?.translation || ""}
              verseOriginal={dailyPassage.pratibha_layers?.original}
            />
          </view>
        )}

        {dailyPassage.pratibha_layers?.translation && (
          <text style={{ color: "#ddd", fontSize: 16, lineHeight: 1.6, marginBottom: 32 }}>
            {dailyPassage.pratibha_layers.translation}
          </text>
        )}

        {/* Comments section */}
        {dailyPassage._id && (
          <view
            style={{
              marginTop: 32,
              paddingTop: 32,
              borderTop: "1px solid #333",
            }}
          >
            <CommentSection verseId={dailyPassage._id} />
          </view>
        )}
      </view>
    </scroll-view>
  );
}

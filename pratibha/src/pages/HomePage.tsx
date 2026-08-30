import React, { useEffect, useState } from "@lynx-js/react";
import { convexFetch } from "../convex/httpClient";
import { LikeButton } from "../components/LikeButton";
import { CommentSection } from "../components/CommentSection";
import { ShareButton } from "../components/ShareButton";

export function HomePage() {
  const [dailyPassage, setDailyPassage] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [showDiscussion, setShowDiscussion] = useState(false);

  useEffect(() => {
    async function loadDaily() {
      try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 3000);
        
        const response = await fetch("http://localhost:8000/daily", {
          signal: controller.signal,
        });
        clearTimeout(timeout);
        
        const data = await response.json();
        setDailyPassage(data);
      } catch (error) {
        console.error("Failed to load daily passage:", error);
        // Fallback passage
        setDailyPassage({
          _id: "fallback",
          title: "धर्म",
          collection: "Bhagavad Gita 2.47",
          pratibha_layers: {
            translation: "You have a right to perform your prescribed duty, but you are not entitled to the fruits of action. Never consider yourself the cause of the results of your activities, and never be attached to not doing your duty.",
          },
        });
      } finally {
        setLoading(false);
      }
    }
    loadDaily();
  }, []);

  return (
    <scroll-view scroll-orientation="vertical" style={{ flex: 1, backgroundColor: "#0a0a0f" }}>
      <view style={{ paddingLeft: 24, paddingRight: 24, paddingTop: 32, paddingBottom: 32 }}>
        <text style={{ color: "#666", fontSize: 11, textTransform: "uppercase", letterSpacing: 2, marginBottom: 16 }}>
          TODAY
        </text>

        {loading ? (
          <text style={{ color: "#666", fontSize: 15, lineHeight: "24px" }}>Loading passage...</text>
        ) : dailyPassage ? (
          <view>
            {dailyPassage.collection && (
              <text style={{ color: "#999", fontSize: 13, marginBottom: 8, lineHeight: "20px" }}>
                {dailyPassage.collection}
              </text>
            )}
            
            {dailyPassage.pratibha_layers?.original && (
              <text style={{ color: "#c9a227", fontSize: 28, fontWeight: "600", marginBottom: 20, lineHeight: "42px" }}>
                {dailyPassage.pratibha_layers.original}
              </text>
            )}

            {dailyPassage.pratibha_layers?.translation && (
              <text style={{ color: "#ddd", fontSize: 17, marginBottom: 40, lineHeight: "28px" }}>
                {dailyPassage.pratibha_layers.translation}
              </text>
            )}

            {/* Social actions row */}
            {dailyPassage._id && dailyPassage._id !== "fallback" && (
              <view style={{ display: "linear", flexDirection: "row", marginBottom: 40, alignItems: "center" }}>
                <LikeButton verseId={dailyPassage._id} />
                <view style={{ width: 16 }} />
                <ShareButton
                  verseId={dailyPassage._id}
                  verseTitle={dailyPassage.title || dailyPassage._id}
                  verseTranslation={dailyPassage.pratibha_layers?.translation || ""}
                  verseOriginal={dailyPassage.pratibha_layers?.original}
                />
              </view>
            )}

            {/* Discussion disclosure */}
            {dailyPassage._id && dailyPassage._id !== "fallback" && (
              <view>
                <view
                  bindtap={() => setShowDiscussion(!showDiscussion)}
                  style={{
                    paddingTop: 12,
                    paddingBottom: 12,
                    borderTopWidth: 1,
                    borderTopColor: "#222",
                  }}
                >
                  <text style={{ color: "#999", fontSize: 14, fontWeight: "500" }}>
                    {showDiscussion ? "▼ Discussion" : "▶ Discussion"}
                  </text>
                </view>

                {showDiscussion && (
                  <view style={{ marginTop: 20 }}>
                    <CommentSection verseId={dailyPassage._id} />
                  </view>
                )}
              </view>
            )}
          </view>
        ) : (
          <view>
            <text style={{ color: "#c9a227", fontSize: 32, fontWeight: "bold", marginBottom: 16, lineHeight: "44px" }}>
              Pratibha
            </text>
            <text style={{ color: "#ddd", fontSize: 16, lineHeight: "26px" }}>
              Living Manuscript of World Wisdom
            </text>
          </view>
        )}
      </view>
    </scroll-view>
  );
}

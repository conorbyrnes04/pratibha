import React, { useEffect, useState } from "@lynx-js/react";
import { LikeButton } from "../components/LikeButton";
import { CommentSection } from "../components/CommentSection";
import { ShareButton } from "../components/ShareButton";

interface Verse {
  _id: string;
  title?: string;
  collection?: string;
  pratibha_layers?: {
    translation?: string;
    original?: string;
    commentary?: string;
  };
}

export function ReadPage() {
  const [verses, setVerses] = useState<Verse[]>([]);
  const [selectedVerse, setSelectedVerse] = useState<Verse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadVerses() {
      try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 3000);
        
        const response = await fetch("http://localhost:8000/verses?limit=20", {
          signal: controller.signal,
        });
        clearTimeout(timeout);
        
        const data = await response.json();
        setVerses(data.verses || []);
      } catch (error) {
        console.error("Failed to load verses:", error);
      } finally {
        setLoading(false);
      }
    }
    loadVerses();
  }, []);

  if (selectedVerse) {
    return (
      <scroll-view scroll-orientation="vertical" style={{ flex: 1, backgroundColor: "#0a0a0f" }}>
        <view style={{ paddingLeft: 24, paddingRight: 24, paddingTop: 24, paddingBottom: 32 }}>
          <view
            bindtap={() => setSelectedVerse(null)}
            style={{
              marginBottom: 24,
              paddingTop: 10,
              paddingBottom: 10,
              paddingLeft: 16,
              paddingRight: 16,
              backgroundColor: "#1a1a2e",
              borderRadius: 6,
              alignSelf: "flex-start",
            }}
          >
            <text style={{ color: "#c9a227", fontSize: 14 }}>← Back</text>
          </view>

          {selectedVerse.collection && (
            <text style={{ color: "#666", fontSize: 11, textTransform: "uppercase", letterSpacing: 1, marginBottom: 12, lineHeight: "16px" }}>
              {selectedVerse.collection}
            </text>
          )}

          {selectedVerse.pratibha_layers?.original && (
            <text style={{ color: "#c9a227", fontSize: 24, fontWeight: "600", marginBottom: 24, lineHeight: "36px" }}>
              {selectedVerse.pratibha_layers.original}
            </text>
          )}

          {selectedVerse.pratibha_layers?.translation && (
            <text style={{ color: "#ddd", fontSize: 17, marginBottom: 32, lineHeight: "28px" }}>
              {selectedVerse.pratibha_layers.translation}
            </text>
          )}

          {/* Social actions */}
          <view style={{ display: "linear", flexDirection: "row", marginBottom: 32, alignItems: "center" }}>
            <LikeButton verseId={selectedVerse._id} />
            <view style={{ width: 16 }} />
            <ShareButton
              verseId={selectedVerse._id}
              verseTitle={selectedVerse.title || selectedVerse._id}
              verseTranslation={selectedVerse.pratibha_layers?.translation || ""}
              verseOriginal={selectedVerse.pratibha_layers?.original}
            />
          </view>

          {selectedVerse.pratibha_layers?.commentary && (
            <view style={{ marginBottom: 32, paddingTop: 24, borderTopWidth: 1, borderTopColor: "#222" }}>
              <text style={{ color: "#666", fontSize: 11, marginBottom: 12, textTransform: "uppercase", letterSpacing: 1, lineHeight: "16px" }}>
                COMMENTARY
              </text>
              <text style={{ color: "#999", fontSize: 15, lineHeight: "25px" }}>
                {selectedVerse.pratibha_layers.commentary}
              </text>
            </view>
          )}

          {/* Comments section */}
          <view
            style={{
              marginTop: 32,
              paddingTop: 32,
              borderTopWidth: 1,
              borderTopColor: "#222",
            }}
          >
            <CommentSection verseId={selectedVerse._id} />
          </view>
        </view>
      </scroll-view>
    );
  }

  return (
    <view style={{ flex: 1, backgroundColor: "#0a0a0f" }}>
      <view style={{ paddingLeft: 24, paddingRight: 24, paddingTop: 24, paddingBottom: 16 }}>
        <text style={{ color: "#666", fontSize: 11, textTransform: "uppercase", letterSpacing: 2, marginBottom: 8, lineHeight: "16px" }}>
          LIBRARY
        </text>
        <text style={{ color: "#ddd", fontSize: 20, fontWeight: "600", marginBottom: 4, lineHeight: "28px" }}>
          Canonical Collection
        </text>
      </view>

      {loading ? (
        <view style={{ paddingLeft: 24, paddingRight: 24 }}>
          <text style={{ color: "#666", fontSize: 15, lineHeight: "24px" }}>Loading passages...</text>
        </view>
      ) : (
        <list style={{ flex: 1 }}>
          {verses.map((verse) => (
            <list-item
              key={verse._id}
              bindtap={() => setSelectedVerse(verse)}
              style={{
                paddingTop: 16,
                paddingBottom: 16,
                paddingLeft: 24,
                paddingRight: 24,
                borderBottomWidth: 1,
                borderBottomColor: "#1a1a2e",
              }}
            >
              {verse.collection && (
                <text style={{ color: "#666", fontSize: 11, marginBottom: 6, textTransform: "uppercase", letterSpacing: 1, lineHeight: "16px" }}>
                  {verse.collection}
                </text>
              )}
              <text style={{ color: "#c9a227", fontSize: 16, fontWeight: "600", marginBottom: 8, lineHeight: "24px" }}>
                {verse.title || verse._id}
              </text>
              {verse.pratibha_layers?.translation && (
                <text
                  style={{
                    color: "#999",
                    fontSize: 14,
                    lineHeight: "22px",
                    textMaxline: 2,
                    textOverflow: "ellipsis",
                  }}
                >
                  {verse.pratibha_layers.translation}
                </text>
              )}
            </list-item>
          ))}
        </list>
      )}
    </view>
  );
}

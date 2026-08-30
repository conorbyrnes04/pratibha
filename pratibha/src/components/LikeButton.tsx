import React, { useState, useEffect } from "@lynx-js/react";
import { convexFetch } from "../convex/httpClient";
import { useAuth } from "../auth/AuthProvider";

interface LikeButtonProps {
  verseId: string;
}

export function LikeButton({ verseId }: LikeButtonProps) {
  const { user } = useAuth();
  const [likeCount, setLikeCount] = useState<number>(0);
  const [isLiked, setIsLiked] = useState<boolean>(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadLikeData();
  }, [verseId, user]);

  async function loadLikeData() {
    try {
      // Get like count
      const count = await convexFetch("verseLikes:getLikeCount", { verseId }, "query");
      setLikeCount(count);

      // Check if user has liked (only if logged in)
      if (user) {
        const liked = await convexFetch("verseLikes:hasUserLiked", { verseId }, "query");
        setIsLiked(liked);
      }
    } catch (error) {
      console.error("Failed to load like data:", error);
    }
  }

  async function handleLike() {
    if (!user) {
      alert("Please sign in to like verses");
      return;
    }

    if (loading) return;

    setLoading(true);
    try {
      const result = await convexFetch("verseLikes:toggleLike", { verseId }, "mutation");
      setIsLiked(result.liked);
      setLikeCount((prev) => (result.liked ? prev + 1 : prev - 1));
    } catch (error: any) {
      console.error("Failed to toggle like:", error);
      alert(error.message || "Failed to like verse");
    } finally {
      setLoading(false);
    }
  }

  return (
    <view
      onClick={handleLike}
      style={{
        flexDirection: "row",
        alignItems: "center",
        gap: 8,
        cursor: user ? "pointer" : "default",
        opacity: loading ? 0.6 : 1,
        paddingVertical: 8,
        paddingHorizontal: 12,
        borderRadius: 4,
        backgroundColor: isLiked ? "rgba(240, 201, 121, 0.1)" : "transparent",
      }}
    >
      <text style={{ fontSize: 20, color: isLiked ? "#f0c979" : "#999" }}>
        {isLiked ? "♥" : "♡"}
      </text>
      <text style={{ color: "#999", fontSize: 14, fontWeight: "500" }}>
        {likeCount}
      </text>
    </view>
  );
}

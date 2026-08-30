import React, { useState, useEffect } from "react";
import { convexFetch } from "../convex/httpClient";
import { useAuth } from "../auth/AuthProvider";

interface Comment {
  _id: string;
  userId: string;
  verseId: string;
  parentId?: string;
  body: string;
  depth: number;
  status: "visible" | "hidden" | "pending";
  createdAt: number;
  updatedAt: number;
  userEmail: string;
}

interface CommentSectionProps {
  verseId: string;
}

export function CommentSection({ verseId }: CommentSectionProps) {
  const { user } = useAuth();
  const [comments, setComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState(true);
  const [showFirstTimeReminder, setShowFirstTimeReminder] = useState(false);

  useEffect(() => {
    loadComments();
    checkFirstTime();
  }, [verseId]);

  async function loadComments() {
    try {
      const topLevelComments = await convexFetch(
        "verseComments:getComments",
        { verseId },
        "query"
      );
      setComments(topLevelComments);
    } catch (error) {
      console.error("Failed to load comments:", error);
    } finally {
      setLoading(false);
    }
  }

  async function checkFirstTime() {
    if (!user) return;
    try {
      const hasCommented = await convexFetch("verseComments:hasUserCommented", {}, "query");
      setShowFirstTimeReminder(!hasCommented);
    } catch (error) {
      console.error("Failed to check comment status:", error);
    }
  }

  if (loading) {
    return (
      <view style={{ padding: 20 }}>
        <text style={{ color: "#999", fontSize: 14 }}>Loading comments...</text>
      </view>
    );
  }

  return (
    <view style={{ padding: 20, gap: 20 }}>
      <text style={{ color: "#f0c979", fontSize: 20, fontWeight: "bold" }}>
        Discussion
      </text>

      {/* Comment composer */}
      <CommentComposer
        verseId={verseId}
        onCommentPosted={loadComments}
        showFirstTimeReminder={showFirstTimeReminder}
        onFirstComment={() => setShowFirstTimeReminder(false)}
      />

      {/* Comment list */}
      {comments.length === 0 ? (
        <text style={{ color: "#999", fontSize: 14, fontStyle: "italic" }}>
          No comments yet. Start the conversation!
        </text>
      ) : (
        <view style={{ gap: 16 }}>
          {comments.map((comment) => (
            <CommentThread key={comment._id} comment={comment} verseId={verseId} onUpdate={loadComments} />
          ))}
        </view>
      )}
    </view>
  );
}

interface CommentComposerProps {
  verseId: string;
  parentId?: string;
  depth?: number;
  onCommentPosted: () => void;
  onCancel?: () => void;
  showFirstTimeReminder?: boolean;
  onFirstComment?: () => void;
}

function CommentComposer({
  verseId,
  parentId,
  depth = 0,
  onCommentPosted,
  onCancel,
  showFirstTimeReminder,
  onFirstComment,
}: CommentComposerProps) {
  const { user } = useAuth();
  const [body, setBody] = useState("");
  const [posting, setPosting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handlePost() {
    if (!user) {
      alert("Please sign in to comment");
      return;
    }

    if (body.trim().length === 0) {
      setError("Comment cannot be empty");
      return;
    }

    setPosting(true);
    setError(null);

    try {
      await convexFetch(
        "verseComments:postComment",
        { verseId, parentId, body },
        "action"
      );
      setBody("");
      if (onFirstComment) {
        onFirstComment();
      }
      onCommentPosted();
    } catch (error: any) {
      setError(error.message || "Failed to post comment");
    } finally {
      setPosting(false);
    }
  }

  if (!user) {
    return (
      <view style={{ padding: 16, backgroundColor: "#1a1a2e", borderRadius: 8 }}>
        <text style={{ color: "#999", fontSize: 14 }}>
          Sign in to join the discussion
        </text>
      </view>
    );
  }

  return (
    <view style={{ gap: 12 }}>
      {showFirstTimeReminder && (
        <view
          style={{
            padding: 12,
            backgroundColor: "rgba(240, 201, 121, 0.1)",
            borderLeft: "3px solid #f0c979",
            borderRadius: 4,
          }}
        >
          <text style={{ color: "#f0c979", fontSize: 14 }}>
            <text style={{ fontWeight: "bold" }}>Right speech:</text> Share insights with
            kindness and clarity.
          </text>
        </view>
      )}

      <view style={{ gap: 8 }}>
        <view
          style={{
            position: "relative",
            backgroundColor: "#1a1a2e",
            borderRadius: 8,
            border: "1px solid #333",
          }}
        >
          <input
            value={body}
            onInput={(e: any) => setBody(e.target.value)}
            placeholder={parentId ? "Write a reply..." : "Share your thoughts..."}
            multiline
            style={{
              width: "100%",
              minHeight: 80,
              padding: 12,
              color: "#ddd",
              fontSize: 14,
              backgroundColor: "transparent",
              border: "none",
              outline: "none",
              resize: "vertical",
            }}
          />
          <text
            style={{
              position: "absolute",
              bottom: 8,
              right: 12,
              color: body.length > 2000 ? "#ff6b6b" : "#666",
              fontSize: 12,
            }}
          >
            {body.length} / 2000
          </text>
        </view>

        {error && (
          <text style={{ color: "#ff6b6b", fontSize: 13 }}>{error}</text>
        )}

        <view style={{ flexDirection: "row", gap: 8 }}>
          <view
            onClick={handlePost}
            style={{
              paddingVertical: 8,
              paddingHorizontal: 16,
              backgroundColor: posting ? "#666" : "#f0c979",
              borderRadius: 4,
              cursor: posting ? "default" : "pointer",
            }}
          >
            <text
              style={{
                color: posting ? "#999" : "#1a1a2e",
                fontSize: 14,
                fontWeight: "600",
              }}
            >
              {posting ? "Posting..." : parentId ? "Post Reply" : "Post Comment"}
            </text>
          </view>

          {onCancel && (
            <view
              onClick={onCancel}
              style={{
                paddingVertical: 8,
                paddingHorizontal: 16,
                backgroundColor: "#333",
                borderRadius: 4,
                cursor: "pointer",
              }}
            >
              <text style={{ color: "#999", fontSize: 14, fontWeight: "600" }}>
                Cancel
              </text>
            </view>
          )}
        </view>
      </view>
    </view>
  );
}

interface CommentThreadProps {
  comment: Comment;
  verseId: string;
  onUpdate: () => void;
}

function CommentThread({ comment, verseId, onUpdate }: CommentThreadProps) {
  const [replies, setReplies] = useState<Comment[]>([]);
  const [showReplyBox, setShowReplyBox] = useState(false);
  const [loadingReplies, setLoadingReplies] = useState(false);
  const [showReportDialog, setShowReportDialog] = useState(false);

  useEffect(() => {
    loadReplies();
  }, [comment._id]);

  async function loadReplies() {
    if (!comment._id) return;
    setLoadingReplies(true);
    try {
      const replyData = await convexFetch(
        "verseComments:getReplies",
        { parentId: comment._id },
        "query"
      );
      setReplies(replyData);
    } catch (error) {
      console.error("Failed to load replies:", error);
    } finally {
      setLoadingReplies(false);
    }
  }

  function handleReplyPosted() {
    setShowReplyBox(false);
    loadReplies();
    onUpdate();
  }

  const indentPx = comment.depth * 24;
  const canReply = comment.depth < 3;

  return (
    <view style={{ marginLeft: indentPx, gap: 12 }}>
      <view
        style={{
          padding: 12,
          backgroundColor: "#1a1a2e",
          borderRadius: 8,
          borderLeft: "3px solid #f0c979",
          gap: 8,
        }}
      >
        <view style={{ flexDirection: "row", alignItems: "center", gap: 8 }}>
          <text style={{ color: "#f0c979", fontSize: 13, fontWeight: "600" }}>
            {comment.userEmail}
          </text>
          <text style={{ color: "#666", fontSize: 12 }}>
            {new Date(comment.createdAt).toLocaleDateString()}
          </text>
        </view>

        <text style={{ color: "#ddd", fontSize: 14, lineHeight: 1.5 }}>
          {comment.body}
        </text>

        <view style={{ flexDirection: "row", gap: 16, marginTop: 4 }}>
          {canReply && (
            <text
              onClick={() => setShowReplyBox(!showReplyBox)}
              style={{
                color: "#999",
                fontSize: 13,
                cursor: "pointer",
                textDecoration: showReplyBox ? "underline" : "none",
              }}
            >
              Reply
            </text>
          )}
          <text
            onClick={() => setShowReportDialog(!showReportDialog)}
            style={{
              color: "#999",
              fontSize: 13,
              cursor: "pointer",
              textDecoration: showReportDialog ? "underline" : "none",
            }}
          >
            Report
          </text>
        </view>
      </view>

      {showReplyBox && (
        <view style={{ marginLeft: 12 }}>
          <CommentComposer
            verseId={verseId}
            parentId={comment._id}
            depth={comment.depth + 1}
            onCommentPosted={handleReplyPosted}
            onCancel={() => setShowReplyBox(false)}
          />
        </view>
      )}

      {showReportDialog && (
        <view style={{ marginLeft: 12 }}>
          <ReportDialog
            commentId={comment._id}
            onClose={() => setShowReportDialog(false)}
            onReported={onUpdate}
          />
        </view>
      )}

      {/* Show replies */}
      {loadingReplies ? (
        <text style={{ color: "#666", fontSize: 13, marginLeft: 12 }}>
          Loading replies...
        </text>
      ) : (
        replies.length > 0 && (
          <view style={{ gap: 12 }}>
            {replies.map((reply) => (
              <CommentThread key={reply._id} comment={reply} verseId={verseId} onUpdate={onUpdate} />
            ))}
          </view>
        )
      )}
    </view>
  );
}

interface ReportDialogProps {
  commentId: string;
  onClose: () => void;
  onReported: () => void;
}

function ReportDialog({ commentId, onClose, onReported }: ReportDialogProps) {
  const { user } = useAuth();
  const [reason, setReason] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit() {
    if (!user) {
      alert("Please sign in to report");
      return;
    }

    if (reason.trim().length === 0) {
      setError("Please provide a reason");
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      await convexFetch(
        "verseComments:reportComment",
        { commentId, reason },
        "mutation"
      );
      alert("Thank you for your report. We will review this comment.");
      onReported();
      onClose();
    } catch (error: any) {
      setError(error.message || "Failed to submit report");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <view
      style={{
        padding: 12,
        backgroundColor: "#252540",
        borderRadius: 8,
        border: "1px solid #333",
        gap: 8,
      }}
    >
      <text style={{ color: "#f0c979", fontSize: 14, fontWeight: "600" }}>
        Report Comment
      </text>

      <input
        value={reason}
        onInput={(e: any) => setReason(e.target.value)}
        placeholder="Why are you reporting this comment?"
        multiline
        style={{
          width: "100%",
          minHeight: 60,
          padding: 8,
          color: "#ddd",
          fontSize: 13,
          backgroundColor: "#1a1a2e",
          border: "1px solid #333",
          borderRadius: 4,
        }}
      />

      {error && <text style={{ color: "#ff6b6b", fontSize: 12 }}>{error}</text>}

      <view style={{ flexDirection: "row", gap: 8 }}>
        <view
          onClick={handleSubmit}
          style={{
            paddingVertical: 6,
            paddingHorizontal: 12,
            backgroundColor: submitting ? "#666" : "#f0c979",
            borderRadius: 4,
            cursor: submitting ? "default" : "pointer",
          }}
        >
          <text
            style={{
              color: submitting ? "#999" : "#1a1a2e",
              fontSize: 13,
              fontWeight: "600",
            }}
          >
            {submitting ? "Submitting..." : "Submit Report"}
          </text>
        </view>

        <view
          onClick={onClose}
          style={{
            paddingVertical: 6,
            paddingHorizontal: 12,
            backgroundColor: "#333",
            borderRadius: 4,
            cursor: "pointer",
          }}
        >
          <text style={{ color: "#999", fontSize: 13, fontWeight: "600" }}>
            Cancel
          </text>
        </view>
      </view>
    </view>
  );
}

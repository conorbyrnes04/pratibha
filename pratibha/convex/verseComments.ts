import { v } from "convex/values";
import { mutation, query, action } from "./_generated/server";
import { getAuthUserId } from "@convex-dev/auth/server";
import { internal } from "./_generated/api";
import { checkBlocklist } from "./moderation";

const MIN_COMMENT_LENGTH = 10;
const MAX_COMMENT_LENGTH = 2000;
const MAX_COMMENTS_PER_HOUR = 10;
const MAX_DEPTH = 3;
const MAX_REPLIES_PER_PARENT = 50;
const REPORTS_TO_HIDE = 3;

/**
 * Get all visible comments for a verse (top-level only)
 */
export const getComments = query({
  args: { verseId: v.string() },
  handler: async (ctx, args) => {
    const comments = await ctx.db
      .query("verse_comments")
      .withIndex("by_verse_created", (q) => q.eq("verseId", args.verseId))
      .filter((q) =>
        q.and(
          q.eq(q.field("status"), "visible"),
          q.eq(q.field("parentId"), undefined)
        )
      )
      .order("asc")
      .collect();

    // Fetch user info for each comment
    const commentsWithUsers = await Promise.all(
      comments.map(async (comment) => {
        const user = await ctx.db.get(comment.userId as any);
        return {
          ...comment,
          userEmail: user?.email || "Unknown",
        };
      })
    );

    return commentsWithUsers;
  },
});

/**
 * Get replies to a specific comment
 */
export const getReplies = query({
  args: { parentId: v.string() },
  handler: async (ctx, args) => {
    const replies = await ctx.db
      .query("verse_comments")
      .withIndex("by_parent", (q) => q.eq("parentId", args.parentId))
      .filter((q) => q.eq(q.field("status"), "visible"))
      .order("asc")
      .collect();

    // Fetch user info for each reply
    const repliesWithUsers = await Promise.all(
      replies.map(async (reply) => {
        const user = await ctx.db.get(reply.userId as any);
        return {
          ...reply,
          userEmail: user?.email || "Unknown",
        };
      })
    );

    return repliesWithUsers;
  },
});

/**
 * Get comment count for a verse
 */
export const getCommentCount = query({
  args: { verseId: v.string() },
  handler: async (ctx, args) => {
    const comments = await ctx.db
      .query("verse_comments")
      .withIndex("by_verse_created", (q) => q.eq("verseId", args.verseId))
      .filter((q) => q.eq(q.field("status"), "visible"))
      .collect();

    return comments.length;
  },
});

/**
 * Check if user has commented before (for first-time reminder)
 */
export const hasUserCommented = query({
  args: {},
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      return false;
    }

    const comment = await ctx.db
      .query("verse_comments")
      .withIndex("by_user", (q) => q.eq("userId", userId))
      .first();

    return !!comment;
  },
});

/**
 * Post a new comment with full moderation checks
 */
export const postComment = action({
  args: {
    verseId: v.string(),
    parentId: v.optional(v.string()),
    body: v.string(),
  },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      throw new Error("Must be logged in to comment");
    }

    const trimmedBody = args.body.trim();

    // Length checks
    if (trimmedBody.length < MIN_COMMENT_LENGTH) {
      throw new Error(
        "Please share a more complete thought (at least 10 characters)."
      );
    }

    if (trimmedBody.length > MAX_COMMENT_LENGTH) {
      throw new Error("Please keep comments concise (under 2000 characters).");
    }

    // Rate limiting check
    const oneHourAgo = Date.now() - 60 * 60 * 1000;
    const recentComments = await ctx.runQuery(internal.verseComments.countRecentUserComments, {
      userId,
      since: oneHourAgo,
    });

    if (recentComments >= MAX_COMMENTS_PER_HOUR) {
      throw new Error("Please take time to reflect before commenting again.");
    }

    // Depth check (if replying to a comment)
    let depth = 0;
    if (args.parentId) {
      const parent = await ctx.runQuery(internal.verseComments.getCommentById, {
        commentId: args.parentId,
      });

      if (!parent) {
        throw new Error("Parent comment not found");
      }

      depth = parent.depth + 1;

      if (depth > MAX_DEPTH) {
        throw new Error(
          "Conversation thread is complete. Start a new top-level comment."
        );
      }

      // Check reply count for parent
      const replyCount = await ctx.runQuery(internal.verseComments.countReplies, {
        parentId: args.parentId,
      });

      if (replyCount >= MAX_REPLIES_PER_PARENT) {
        throw new Error(
          "This thread has reached its capacity. Start a new discussion."
        );
      }
    }

    // Blocklist check
    const blocklistResult = checkBlocklist(trimmedBody);
    if (!blocklistResult.passed) {
      throw new Error(
        "This comment does not meet our community guidelines for respectful discourse."
      );
    }

    // OpenAI moderation check (if API key available)
    const moderationResult = await ctx.runAction(internal.moderation.moderateWithOpenAI, {
      text: trimmedBody,
    });

    if (!moderationResult.passed) {
      throw new Error(
        "This comment does not meet our community guidelines for respectful discourse."
      );
    }

    // All checks passed - insert comment
    const commentId = await ctx.runMutation(internal.verseComments.insertComment, {
      userId,
      verseId: args.verseId,
      parentId: args.parentId,
      body: trimmedBody,
      depth,
    });

    return { commentId };
  },
});

/**
 * Internal: Insert a comment (called after moderation passes)
 */
export const insertComment = mutation({
  args: {
    userId: v.string(),
    verseId: v.string(),
    parentId: v.optional(v.string()),
    body: v.string(),
    depth: v.number(),
  },
  handler: async (ctx, args) => {
    const now = Date.now();
    const commentId = await ctx.db.insert("verse_comments", {
      userId: args.userId,
      verseId: args.verseId,
      parentId: args.parentId,
      body: args.body,
      depth: args.depth,
      status: "visible",
      createdAt: now,
      updatedAt: now,
    });
    return commentId;
  },
});

/**
 * Internal: Count recent comments by user (for rate limiting)
 */
export const countRecentUserComments = query({
  args: { userId: v.string(), since: v.number() },
  handler: async (ctx, args) => {
    const comments = await ctx.db
      .query("verse_comments")
      .withIndex("by_user", (q) => q.eq("userId", args.userId))
      .filter((q) => q.gte(q.field("createdAt"), args.since))
      .collect();

    return comments.length;
  },
});

/**
 * Internal: Get a comment by ID
 */
export const getCommentById = query({
  args: { commentId: v.string() },
  handler: async (ctx, args) => {
    const comment = await ctx.db.get(args.commentId as any);
    return comment;
  },
});

/**
 * Internal: Count replies to a comment
 */
export const countReplies = query({
  args: { parentId: v.string() },
  handler: async (ctx, args) => {
    const replies = await ctx.db
      .query("verse_comments")
      .withIndex("by_parent", (q) => q.eq("parentId", args.parentId))
      .collect();

    return replies.length;
  },
});

/**
 * Report a comment
 */
export const reportComment = mutation({
  args: {
    commentId: v.string(),
    reason: v.string(),
  },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      throw new Error("Must be logged in to report comments");
    }

    // Check if user already reported this comment
    const existingReport = await ctx.db
      .query("comment_reports")
      .withIndex("by_comment", (q) => q.eq("commentId", args.commentId))
      .filter((q) => q.eq(q.field("reporterUserId"), userId))
      .first();

    if (existingReport) {
      throw new Error("You have already reported this comment");
    }

    // Add report
    await ctx.db.insert("comment_reports", {
      commentId: args.commentId,
      reporterUserId: userId,
      reason: args.reason.trim(),
      createdAt: Date.now(),
    });

    // Count total reports for this comment
    const reports = await ctx.db
      .query("comment_reports")
      .withIndex("by_comment", (q) => q.eq("commentId", args.commentId))
      .collect();

    const comment = await ctx.db.get(args.commentId as any);
    if (!comment) {
      return;
    }

    // Update status based on report count
    if (reports.length === 1) {
      // First report - mark as pending
      await ctx.db.patch(args.commentId as any, {
        status: "pending" as const,
        updatedAt: Date.now(),
      });
    } else if (reports.length >= REPORTS_TO_HIDE) {
      // Multiple reports - hide comment
      await ctx.db.patch(args.commentId as any, {
        status: "hidden" as const,
        updatedAt: Date.now(),
      });
    }
  },
});

/**
 * Get all pending/hidden comments (for moderator review)
 */
export const getModerationQueue = query({
  args: {},
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      throw new Error("Must be logged in");
    }

    // TODO: Add admin check here if you want to restrict access

    const pendingComments = await ctx.db
      .query("verse_comments")
      .withIndex("by_status", (q) => q.eq("status", "pending"))
      .collect();

    const hiddenComments = await ctx.db
      .query("verse_comments")
      .withIndex("by_status", (q) => q.eq("status", "hidden"))
      .collect();

    return {
      pending: pendingComments,
      hidden: hiddenComments,
    };
  },
});

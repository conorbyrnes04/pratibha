import { getAuthUserId } from "@convex-dev/auth/server";
import { v } from "convex/values";
import { mutation, query } from "./_generated/server";
import { assertDisplayName, assertReply } from "./textRules";

const MAX_REPLIES = 48;
const MAX_NESTED = 16;
const MAX_REPLIES_PER_HOUR = 20;

export const list = query({
  args: { commentaryId: v.id("student_commentaries") },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    const rows = await ctx.db
      .query("circle_replies")
      .withIndex("by_commentary", (q) => q.eq("commentaryId", args.commentaryId))
      .collect();
    return rows
      .filter((row) => row.status === "visible")
      .sort((a, b) => a.createdAt - b.createdAt)
      .map((row) => ({
        _id: row._id,
        displayName: row.displayName,
        body: row.body,
        createdAt: row.createdAt,
        parentReplyId: row.parentReplyId ?? null,
        mine: Boolean(userId && row.userId === userId),
      }));
  },
});

export const post = mutation({
  args: {
    commentaryId: v.id("student_commentaries"),
    body: v.string(),
    displayName: v.optional(v.string()),
    parentReplyId: v.optional(v.id("circle_replies")),
  },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) throw new Error("Sign in to reply.");
    const parent = await ctx.db.get(args.commentaryId);
    if (!parent || parent.status !== "offered") {
      throw new Error("That reading is not open.");
    }

    const since = Date.now() - 60 * 60 * 1000;
    const recent = await ctx.db
      .query("circle_replies")
      .withIndex("by_user_created", (q) => q.eq("userId", userId).gte("createdAt", since))
      .collect();
    if (recent.length >= MAX_REPLIES_PER_HOUR) {
      throw new Error("Please take time to reflect before writing again.");
    }

    const siblings = await ctx.db
      .query("circle_replies")
      .withIndex("by_commentary", (q) => q.eq("commentaryId", args.commentaryId))
      .collect();
    const visible = siblings.filter((r) => r.status === "visible");
    if (visible.length >= MAX_REPLIES) {
      throw new Error("This reading has enough replies. Start your own.");
    }

    if (args.parentReplyId) {
      const parentReply = await ctx.db.get(args.parentReplyId);
      if (
        !parentReply ||
        parentReply.commentaryId !== args.commentaryId ||
        parentReply.status !== "visible"
      ) {
        throw new Error("That reply is not open.");
      }
      if (parentReply.parentReplyId) {
        throw new Error("Reply to the thread, not to a nested reply.");
      }
      const nested = visible.filter((r) => r.parentReplyId === args.parentReplyId).length;
      if (nested >= MAX_NESTED) {
        throw new Error("This thread has enough replies. Start your own.");
      }
    }

    const body = assertReply(args.body);
    const profile = await ctx.db
      .query("profiles")
      .withIndex("by_user", (q) => q.eq("userId", userId))
      .unique();
    const displayName = args.displayName?.trim()
      ? assertDisplayName(args.displayName)
      : profile?.displayName;
    if (!displayName) throw new Error("Choose a name before replying.");

    const id = await ctx.db.insert("circle_replies", {
      commentaryId: args.commentaryId,
      userId,
      displayName,
      verseId: parent.verseId,
      body,
      status: "visible",
      createdAt: Date.now(),
      parentReplyId: args.parentReplyId,
    });
    await ctx.db.patch(args.commentaryId, {
      replyCount: (parent.replyCount ?? 0) + 1,
      lastActivityAt: Date.now(),
    });
    return id;
  },
});

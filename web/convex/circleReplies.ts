import { getAuthUserId } from "@convex-dev/auth/server";
import { v } from "convex/values";
import { mutation, query } from "./_generated/server";
import { assertDisplayName, assertReply } from "./textRules";

const MAX_REPLIES = 12;

export const list = query({
  args: { commentaryId: v.id("student_commentaries") },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) return [];
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
        mine: row.userId === userId,
      }));
  },
});

export const post = mutation({
  args: {
    commentaryId: v.id("student_commentaries"),
    body: v.string(),
    displayName: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) throw new Error("Sign in to reply.");
    const parent = await ctx.db.get(args.commentaryId);
    if (!parent || parent.status !== "offered") {
      throw new Error("That reading is not open.");
    }
    const existing = await ctx.db
      .query("circle_replies")
      .withIndex("by_user_commentary", (q) =>
        q.eq("userId", userId).eq("commentaryId", args.commentaryId),
      )
      .unique();
    if (existing) throw new Error("You have already replied to this reading.");
    const siblings = await ctx.db
      .query("circle_replies")
      .withIndex("by_commentary", (q) => q.eq("commentaryId", args.commentaryId))
      .collect();
    if (siblings.filter((r) => r.status === "visible").length >= MAX_REPLIES) {
      throw new Error("This reading has enough replies. Start your own.");
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
    return await ctx.db.insert("circle_replies", {
      commentaryId: args.commentaryId,
      userId,
      displayName,
      verseId: parent.verseId,
      body,
      status: "visible",
      createdAt: Date.now(),
    });
  },
});

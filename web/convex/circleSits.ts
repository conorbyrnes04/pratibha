import { getAuthUserId } from "@convex-dev/auth/server";
import { v } from "convex/values";
import { mutation, query } from "./_generated/server";
import { logQueryError, optionalUserId } from "./safeAuth";

export const meta = query({
  args: { commentaryId: v.id("student_commentaries") },
  handler: async (ctx, args) => {
    try {
      const rows = await ctx.db
        .query("circle_sits")
        .withIndex("by_commentary", (q) => q.eq("commentaryId", args.commentaryId))
        .collect();
      const userId = await optionalUserId(ctx);
      return {
        count: rows.length,
        mine: userId ? rows.some((row) => row.userId === userId) : false,
      };
    } catch (error) {
      logQueryError("circleSits.meta", error);
      return { count: 0, mine: false };
    }
  },
});

export const toggle = mutation({
  args: { commentaryId: v.id("student_commentaries") },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) throw new Error("Sign in to sit with a reading.");
    const parent = await ctx.db.get(args.commentaryId);
    if (!parent || parent.status !== "offered") {
      throw new Error("That reading is not open.");
    }
    const existing = await ctx.db
      .query("circle_sits")
      .withIndex("by_user_commentary", (q) =>
        q.eq("userId", userId).eq("commentaryId", args.commentaryId),
      )
      .unique();
    if (existing) {
      await ctx.db.delete(existing._id);
    } else {
      await ctx.db.insert("circle_sits", {
        userId,
        commentaryId: args.commentaryId,
        createdAt: Date.now(),
      });
    }
    const sits = await ctx.db
      .query("circle_sits")
      .withIndex("by_commentary", (q) => q.eq("commentaryId", args.commentaryId))
      .collect();
    await ctx.db.patch(args.commentaryId, { sitCount: sits.length });
    return { sat: !existing, count: sits.length };
  },
});

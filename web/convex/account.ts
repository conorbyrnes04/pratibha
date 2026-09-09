import { getAuthUserId } from "@convex-dev/auth/server";
import type { Id } from "./_generated/dataModel";
import { mutation, type MutationCtx } from "./_generated/server";

async function deleteIndexed(
  ctx: MutationCtx,
  table:
    | "journal_notes"
    | "learn_progress"
    | "profiles"
    | "manuscripts"
    | "manuscript_entries"
    | "circle_watches"
    | "verse_likes",
  userId: string,
) {
  const rows = await ctx.db
    .query(table)
    .withIndex("by_user", (q) => q.eq("userId", userId))
    .collect();
  for (const row of rows) {
    await ctx.db.delete(row._id);
  }
}

/**
 * Apple 5.1.1(v): in-app account deletion must remove the user's data, not
 * merely sign them out. Called from web /account and iOS Settings.
 */
export const deleteAccount = mutation({
  args: {},
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      throw new Error("Not authenticated");
    }

    const commentaries = await ctx.db
      .query("student_commentaries")
      .withIndex("by_user_updated", (q) => q.eq("userId", userId))
      .collect();
    for (const commentary of commentaries) {
      const replies = await ctx.db
        .query("circle_replies")
        .withIndex("by_commentary", (q) => q.eq("commentaryId", commentary._id))
        .collect();
      for (const reply of replies) await ctx.db.delete(reply._id);
      const sits = await ctx.db
        .query("circle_sits")
        .withIndex("by_commentary", (q) => q.eq("commentaryId", commentary._id))
        .collect();
      for (const sit of sits) await ctx.db.delete(sit._id);
      await ctx.db.delete(commentary._id);
    }

    const ownReplies = await ctx.db
      .query("circle_replies")
      .withIndex("by_user_created", (q) => q.eq("userId", userId))
      .collect();
    for (const reply of ownReplies) await ctx.db.delete(reply._id);

    const ownSits = await ctx.db
      .query("circle_sits")
      .withIndex("by_user_commentary", (q) => q.eq("userId", userId))
      .collect();
    for (const sit of ownSits) await ctx.db.delete(sit._id);

    await deleteIndexed(ctx, "circle_watches", userId);
    await deleteIndexed(ctx, "verse_likes", userId);
    await deleteIndexed(ctx, "manuscript_entries", userId);
    await deleteIndexed(ctx, "manuscripts", userId);
    await deleteIndexed(ctx, "journal_notes", userId);
    await deleteIndexed(ctx, "learn_progress", userId);
    await deleteIndexed(ctx, "profiles", userId);

    const sessions = await ctx.db
      .query("authSessions")
      .withIndex("userId", (q) => q.eq("userId", userId))
      .collect();
    for (const session of sessions) {
      const tokens = await ctx.db
        .query("authRefreshTokens")
        .withIndex("sessionId", (q) => q.eq("sessionId", session._id))
        .collect();
      for (const token of tokens) await ctx.db.delete(token._id);
      await ctx.db.delete(session._id);
    }

    const accounts = await ctx.db
      .query("authAccounts")
      .withIndex("userIdAndProvider", (q) => q.eq("userId", userId))
      .collect();
    for (const account of accounts) await ctx.db.delete(account._id);

    await ctx.db.delete(userId as Id<"users">);
    return { ok: true as const };
  },
});

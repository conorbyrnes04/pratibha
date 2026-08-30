import { v } from "convex/values";
import { mutation, query } from "./_generated/server";
import { getAuthUserId } from "@convex-dev/auth/server";

export const list = query({
  args: {},
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      return [];
    }
    const notes = await ctx.db
      .query("journal_notes")
      .withIndex("by_user_updated", (q) => q.eq("userId", userId))
      .order("desc")
      .collect();
    return notes;
  },
});

export const upsert = mutation({
  args: {
    id: v.optional(v.id("journal_notes")),
    passageId: v.string(),
    passageTitle: v.string(),
    body: v.string(),
    tags: v.array(v.string()),
    prompt: v.optional(v.string()),
    kind: v.optional(v.string()),
    question: v.optional(v.string()),
    chatMode: v.optional(v.string()),
    verseId: v.optional(v.string()),
    createdAt: v.string(),
    updatedAt: v.string(),
  },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      throw new Error("Not authenticated");
    }

    const { id, ...data } = args;

    if (id) {
      const existing = await ctx.db.get(id);
      if (existing?.userId !== userId) {
        throw new Error("Not authorized");
      }
      await ctx.db.patch(id, { ...data, userId });
      return id;
    } else {
      return await ctx.db.insert("journal_notes", { ...data, userId });
    }
  },
});

export const upsertBatch = mutation({
  args: {
    notes: v.array(
      v.object({
        id: v.optional(v.id("journal_notes")),
        passageId: v.string(),
        passageTitle: v.string(),
        body: v.string(),
        tags: v.array(v.string()),
        prompt: v.optional(v.string()),
        kind: v.optional(v.string()),
        question: v.optional(v.string()),
        chatMode: v.optional(v.string()),
        verseId: v.optional(v.string()),
        createdAt: v.string(),
        updatedAt: v.string(),
      })
    ),
  },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      throw new Error("Not authenticated");
    }

    const results = [];
    for (const note of args.notes) {
      const { id, ...data } = note;

      if (id) {
        const existing = await ctx.db.get(id);
        if (existing?.userId !== userId) {
          throw new Error("Not authorized");
        }
        await ctx.db.patch(id, { ...data, userId });
        results.push(id);
      } else {
        const newId = await ctx.db.insert("journal_notes", { ...data, userId });
        results.push(newId);
      }
    }
    return results;
  },
});

export const remove = mutation({
  args: { id: v.id("journal_notes") },
  handler: async (ctx, args) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      throw new Error("Not authenticated");
    }

    const note = await ctx.db.get(args.id);
    if (!note) {
      throw new Error("Note not found");
    }
    if (note.userId !== userId) {
      throw new Error("Not authorized");
    }

    await ctx.db.delete(args.id);
  },
});

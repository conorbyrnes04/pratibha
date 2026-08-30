import { authTables } from "@convex-dev/auth/server";
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

const schema = defineSchema({
  ...authTables,

  journal_notes: defineTable({
    userId: v.string(),
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
    .index("by_user", ["userId"])
    .index("by_user_updated", ["userId", "updatedAt"]),

  learn_progress: defineTable({
    userId: v.string(),
    progress: v.any(),
    completedAt: v.any(),
    updatedAt: v.string(),
  }).index("by_user", ["userId"]),
});

export default schema;

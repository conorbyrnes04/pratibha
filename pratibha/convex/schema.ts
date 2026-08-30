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

  verse_likes: defineTable({
    userId: v.string(),
    verseId: v.string(),
    createdAt: v.number(),
  })
    .index("by_user", ["userId"])
    .index("by_verse", ["verseId"])
    .index("by_user_verse", ["userId", "verseId"]),

  verse_comments: defineTable({
    userId: v.string(),
    verseId: v.string(),
    parentId: v.optional(v.string()),
    body: v.string(),
    depth: v.number(),
    status: v.union(v.literal("visible"), v.literal("hidden"), v.literal("pending")),
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_verse_created", ["verseId", "createdAt"])
    .index("by_parent", ["parentId"])
    .index("by_user", ["userId"])
    .index("by_status", ["status"]),

  comment_reports: defineTable({
    commentId: v.string(),
    reporterUserId: v.string(),
    reason: v.string(),
    createdAt: v.number(),
  }).index("by_comment", ["commentId"]),
});

export default schema;

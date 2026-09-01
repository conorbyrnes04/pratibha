import { v } from "convex/values";
import { action, internalQuery, mutation } from "./_generated/server";
import { internal } from "./_generated/api";
import type { Doc } from "./_generated/dataModel";

type SearchResult = {
  body: string;
  meta: unknown;
  collection: string;
  section: string | null;
  score: number;
};
type RelatedResult = { unitId: string; score: number; collection: string };

// RAG vector store on Convex — the replacement for Supabase pgvector.
//
// Writes (ingest) are guarded by a shared secret (RAG_INGEST_TOKEN in the Convex
// deployment env) so only the ingest job can populate the table. Reads go through
// the `search` action, which is the one place `ctx.vectorSearch` can run.

const chunk = v.object({
  body: v.string(),
  embedding: v.array(v.float64()),
  collection: v.string(),
  section: v.optional(v.string()),
  sourceFile: v.string(),
  unitId: v.optional(v.string()),
  meta: v.any(),
});

// Layer kinds a Related seed vector should prefer, best first. A translation
// chunk represents the teaching better than an appendix for cross-tradition
// nearest-neighbour search.
const SEED_LAYER_RANK: Record<string, number> = {
  translation: 1,
  commentary: 2,
  practice: 3,
  resonances: 4,
};
function seedRank(meta: unknown): number {
  const kind = String((meta as { layer_kind?: unknown } | null)?.layer_kind ?? "")
    .trim()
    .toLowerCase();
  return SEED_LAYER_RANK[kind] ?? 5;
}

function assertToken(token: string) {
  const expected = process.env.RAG_INGEST_TOKEN;
  if (!expected || token !== expected) {
    throw new Error("RAG ingest: bad or missing token");
  }
}

// Replace all chunks for one source file, then insert the new ones — the same
// idempotent DELETE+INSERT the pgvector ingest does per file.
export const replaceSource = mutation({
  args: { token: v.string(), sourceFile: v.string(), chunks: v.array(chunk) },
  handler: async (ctx, args) => {
    assertToken(args.token);
    const existing = await ctx.db
      .query("rag_chunks")
      .withIndex("by_source", (q) => q.eq("sourceFile", args.sourceFile))
      .collect();
    for (const row of existing) await ctx.db.delete(row._id);
    for (const c of args.chunks) await ctx.db.insert("rag_chunks", c);
    return { deleted: existing.length, inserted: args.chunks.length };
  },
});

// Load full docs for the ids a vector search returned (actions can't touch ctx.db).
export const getByIds = internalQuery({
  args: { ids: v.array(v.id("rag_chunks")) },
  // Explicit return type breaks the self-referential inference cycle between
  // this query and the actions below that call it via `internal.ragChunks`.
  handler: async (ctx, args): Promise<Doc<"rag_chunks">[]> => {
    const out: Doc<"rag_chunks">[] = [];
    for (const id of args.ids) {
      const d = await ctx.db.get(id);
      if (d) out.push(d);
    }
    return out;
  },
});

// Nearest-neighbour search over the corpus. The FastAPI backend embeds the query
// (OpenAI) and passes the vector here; we return body + meta + cosine score in the
// same shape the pgvector path produced.
export const search = action({
  args: {
    embedding: v.array(v.float64()),
    limit: v.number(),
    collection: v.optional(v.string()),
  },
  handler: async (ctx, args): Promise<SearchResult[]> => {
    const results = await ctx.vectorSearch("rag_chunks", "by_embedding", {
      vector: args.embedding,
      limit: Math.max(1, Math.min(args.limit, 256)),
      ...(args.collection
        ? { filter: (q) => q.eq("collection", args.collection as string) }
        : {}),
    });
    const scoreById = new Map(results.map((r) => [r._id, r._score]));
    const docs = await ctx.runQuery(internal.ragChunks.getByIds, {
      ids: results.map((r) => r._id),
    });
    return docs.map((d) => ({
      body: d.body,
      meta: d.meta ?? {},
      collection: d.collection,
      section: d.section ?? null,
      score: scoreById.get(d._id) ?? 0,
    }));
  },
});

// Load the seed chunk (embedding + collection) for a unit, preferring the layer
// that best represents the teaching. Replaces the pgvector "SELECT embedding …
// ORDER BY layer_kind" seed lookup in retrieve_related_unit_ids.
export const seedForUnit = internalQuery({
  args: { unitId: v.string() },
  handler: async (ctx, args) => {
    const rows = await ctx.db
      .query("rag_chunks")
      .withIndex("by_unit", (q) => q.eq("unitId", args.unitId))
      .collect();
    if (rows.length === 0) return null;
    rows.sort((a, b) => seedRank(a.meta) - seedRank(b.meta));
    const seed = rows[0];
    return { embedding: seed.embedding, collection: seed.collection };
  },
});

// Nearest units to a given corpus unit, in embedding space, with a per-collection
// cap so one large text can't flood the Related panel. Mirrors the pgvector
// retrieve_related_unit_ids: seed embedding → NN search → collapse to unique units.
export const related = action({
  args: {
    unitId: v.string(),
    limit: v.number(),
    perCollection: v.optional(v.number()),
    minScore: v.optional(v.number()),
  },
  handler: async (ctx, args): Promise<RelatedResult[]> => {
    const seed = await ctx.runQuery(internal.ragChunks.seedForUnit, {
      unitId: args.unitId,
    });
    if (!seed) return [];

    const limit = Math.max(1, Math.min(args.limit, 64));
    const perCollection = Math.max(1, args.perCollection ?? 2);
    const floor = args.minScore ?? 0;

    // Fetch a generous neighbourhood, then collapse to unique units.
    const hits = await ctx.vectorSearch("rag_chunks", "by_embedding", {
      vector: seed.embedding,
      limit: Math.max(limit * 24, 48),
    });
    const docs = await ctx.runQuery(internal.ragChunks.getByIds, {
      ids: hits.map((h) => h._id),
    });
    const scoreById = new Map(hits.map((h) => [h._id, h._score]));

    // Best score per unit (excluding the seed unit itself).
    const best = new Map<string, { score: number; collection: string }>();
    for (const d of docs) {
      const uid = String(d.unitId ?? (d.meta as { _id?: unknown } | null)?._id ?? "").trim();
      if (!uid || uid === args.unitId) continue;
      const score = scoreById.get(d._id) ?? 0;
      if (score < floor) continue;
      const prev = best.get(uid);
      if (!prev || score > prev.score) {
        best.set(uid, { score, collection: d.collection });
      }
    }

    const ranked = Array.from(best.entries()).sort((a, b) => b[1].score - a[1].score);
    const picked: { unitId: string; score: number; collection: string }[] = [];
    const perCol = new Map<string, number>();
    for (const [uid, { score, collection }] of ranked) {
      if (picked.length >= limit) break;
      const used = perCol.get(collection) ?? 0;
      if (used >= perCollection) continue;
      perCol.set(collection, used + 1);
      picked.push({ unitId: uid, score, collection });
    }
    // Top up ignoring the cap if the neighbourhood was sparse.
    if (picked.length < limit) {
      const chosen = new Set(picked.map((p) => p.unitId));
      for (const [uid, { score, collection }] of ranked) {
        if (picked.length >= limit) break;
        if (chosen.has(uid)) continue;
        picked.push({ unitId: uid, score, collection });
        chosen.add(uid);
      }
    }
    return picked;
  },
});

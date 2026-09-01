import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";
import { api } from "./_generated/api";
import { auth } from "./auth";

const http = httpRouter();

auth.addHttpRoutes(http);

function tokenOk(req: Request): boolean {
  const expected = process.env.RAG_INGEST_TOKEN;
  if (!expected) return false;
  const header = req.headers.get("authorization") || "";
  return header === `Bearer ${expected}`;
}

const json = (data: unknown, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json" },
  });

// Bulk ingest: replace one source file's chunks. Guarded by the ingest token.
http.route({
  path: "/rag/ingest",
  method: "POST",
  handler: httpAction(async (ctx, req) => {
    if (!tokenOk(req)) return json({ error: "unauthorized" }, 401);
    const body = await req.json();
    const token = process.env.RAG_INGEST_TOKEN as string;
    const res = await ctx.runMutation(api.ragChunks.replaceSource, {
      token,
      sourceFile: body.sourceFile,
      chunks: body.chunks,
    });
    return json(res);
  }),
});

// Vector search: the FastAPI RAG path embeds the query and posts the vector here.
// Read-only over public-domain corpus, but still token-guarded for parity.
http.route({
  path: "/rag/search",
  method: "POST",
  handler: httpAction(async (ctx, req) => {
    if (!tokenOk(req)) return json({ error: "unauthorized" }, 401);
    const body = await req.json();
    const results = await ctx.runAction(api.ragChunks.search, {
      embedding: body.embedding,
      limit: body.limit ?? 40,
      collection: body.collection,
    });
    return json({ results });
  }),
});

// Related units: seed by an existing unit id, no client-side embedding needed.
http.route({
  path: "/rag/related",
  method: "POST",
  handler: httpAction(async (ctx, req) => {
    if (!tokenOk(req)) return json({ error: "unauthorized" }, 401);
    const body = await req.json();
    const results = await ctx.runAction(api.ragChunks.related, {
      unitId: body.unitId,
      limit: body.limit ?? 6,
      perCollection: body.perCollection,
      minScore: body.minScore,
    });
    return json({ results });
  }),
});

export default http;

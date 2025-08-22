"""Embed YAML and insert into pgvector.
Requires OPENAI_API_KEY and running Postgres from docker-compose.

Usage:
  python scripts/ingest_pgvector.py --dir data/yaml/siva_sutra
"""
import os, argparse, glob, yaml, asyncpg, asyncio
from openai import AsyncOpenAI

async def main(dir_path: str):
  files = sorted(glob.glob(os.path.join(dir_path, "*.yml")))
  client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
  conn = await asyncpg.connect(user=os.getenv("PG_USER","postgres"),
                               password=os.getenv("PG_PASSWORD","postgres"),
                               database=os.getenv("PG_DB","pratibha"),
                               host=os.getenv("PG_HOST","localhost"),
                               port=int(os.getenv("PG_PORT", "5432")))
  total = 0
  for fp in files:
    with open(fp, "r", encoding="utf-8") as f:
      y = yaml.safe_load(f)
    # build chunks from fields
    chunks = []
    for k in ["sanskrit","transliteration","translation","commentary"]:
      if y.get(k): chunks.append((y[k], {"section":k, "sutra_id": y.get("sutra_id"), "collection": y.get("collection")}))
    modes = (y.get("modes") or {})
    for mk, mv in modes.items():
      if mv: chunks.append((mv, {"section":f"mode:{mk}", "sutra_id": y.get("sutra_id"), "collection": y.get("collection")}))
    # embed and insert
    for text, meta in chunks:
      emb = (await client.embeddings.create(model="text-embedding-3-small", input=text)).data[0].embedding
      await conn.execute("INSERT INTO chunks (body, embedding, metadata) VALUES ($1, $2, $3)", text, emb, meta)
      total += 1
  await conn.close()
  print(f"Inserted {total} chunks into pgvector.")
if __name__ == "__main__":
  ap = argparse.ArgumentParser()
  ap.add_argument("--dir", default="data/yaml/siva_sutra")
  args = ap.parse_args()
  asyncio.run(main(args.dir))

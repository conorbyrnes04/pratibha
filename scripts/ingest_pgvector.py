"""Embed YAML and insert into pgvector.
Requires OPENAI_API_KEY and running Postgres from docker-compose.

Usage:
  python scripts/ingest_pgvector.py --dir data/yaml/siva_sutra
"""
import os, argparse, glob, yaml, asyncpg, asyncio, json
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
      if y.get(k): 
        # Handle both string and list fields
        content = y[k]
        if isinstance(content, list):
          content = " ".join(str(item) for item in content if item)
        elif not isinstance(content, str):
          content = str(content)
        
        if content.strip():
          chunks.append((content, {"section":k, "sutra_id": y.get("sutra_id"), "collection": y.get("collection")}))
    
    modes = (y.get("modes") or {})
    for mk, mv in modes.items():
      if mv: 
        # Handle both string and list fields for modes
        if isinstance(mv, list):
          mv = " ".join(str(item) for item in mv if item)
        elif not isinstance(mv, str):
          mv = str(mv)
        
        if mv.strip():
          chunks.append((mv, {"section":f"mode:{mk}", "sutra_id": y.get("sutra_id"), "collection": y.get("collection")}))
    
    # embed and insert
    for text, meta in chunks:
      # Split long text into chunks if needed (max ~6000 tokens for safety)
      if len(text) > 8000:
        # Split into sentences or paragraphs
        sentences = text.split('. ')
        current_chunk = ""
        for sentence in sentences:
          if len(current_chunk) + len(sentence) < 8000:
            current_chunk += sentence + ". "
          else:
            if current_chunk.strip():
              # Process current chunk
              try:
                emb = (await client.embeddings.create(model="text-embedding-3-small", input=current_chunk.strip())).data[0].embedding
                vector_str = f"[{','.join(map(str, emb))}]"
                meta_json = json.dumps(meta)
                await conn.execute("INSERT INTO chunks (body, embedding, metadata) VALUES ($1, $2, $3)", current_chunk.strip(), vector_str, meta_json)
                total += 1
              except Exception as e:
                print(f"Error processing chunk: {e}")
                continue
            current_chunk = sentence + ". "
        
        # Process the last chunk
        if current_chunk.strip():
          try:
            emb = (await client.embeddings.create(model="text-embedding-3-small", input=current_chunk.strip())).data[0].embedding
            vector_str = f"[{','.join(map(str, emb))}]"
            meta_json = json.dumps(meta)
            await conn.execute("INSERT INTO chunks (body, embedding, metadata) VALUES ($1, $2, $3)", current_chunk.strip(), vector_str, meta_json)
            total += 1
          except Exception as e:
            print(f"Error processing final chunk: {e}")
            continue
      else:
        # Process normal length text
        try:
          emb = (await client.embeddings.create(model="text-embedding-3-small", input=text)).data[0].embedding
          vector_str = f"[{','.join(map(str, emb))}]"
          meta_json = json.dumps(meta)
          await conn.execute("INSERT INTO chunks (body, embedding, metadata) VALUES ($1, $2, $3)", text, vector_str, meta_json)
          total += 1
        except Exception as e:
          print(f"Error processing text: {e}")
          continue
  await conn.close()
  print(f"Inserted {total} chunks into pgvector.")

if __name__ == "__main__":
  ap = argparse.ArgumentParser()
  ap.add_argument("--dir", default="data/yaml/siva_sutra")
  args = ap.parse_args()
  asyncio.run(main(args.dir))

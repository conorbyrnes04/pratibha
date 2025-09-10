# Simple pgvector retriever
from typing import List, Tuple
import asyncpg
from .config import settings

async def retrieve_context(query: str, k: int = 4) -> List[Tuple[str, dict, float]]:
    # Needs embeddings pre-inserted by scripts/ingest_pgvector.py
    if not settings.OPENAI_API_KEY:
        return []
    conn = await asyncpg.connect(user=settings.PG_USER, password=settings.PG_PASSWORD,
                                 database=settings.PG_DB, host=settings.PG_HOST, port=settings.PG_PORT)
    # Use OpenAI embeddings on the fly for query
    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    emb = (await client.embeddings.create(model="text-embedding-3-small", input=query)).data[0].embedding
    
    # Convert embedding to proper vector format for pgvector
    vector_str = f"[{','.join(map(str, emb))}]"

    rows = await conn.fetch(
        """SELECT body, metadata, 1 - (embedding <=> $1::vector) AS score
            FROM chunks
            ORDER BY embedding <-> $1::vector
            LIMIT $2
        """, vector_str, k
    )
    await conn.close()
    return [(r["body"], r["metadata"], float(r["score"])) for r in rows]

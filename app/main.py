from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List
from pathlib import Path
import json

from .config import settings
from .llm import chat_completion, smart_chat
from .rag import retrieve_context
from .data_loader import ALL_VERSES, pick_daily

app = FastAPI(title="Pratibha API", version="0.9")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# ---- Static Web ----
WEB_DIR = Path(__file__).resolve().parent.parent / "web"

@app.get("/", response_class=HTMLResponse)
async def index():
    return (WEB_DIR / "index.html").read_text(encoding="utf-8")

@app.get("/assets/{name}")
async def assets(name: str):
    p = WEB_DIR / "assets" / name
    if not p.exists(): raise HTTPException(404, "Asset not found")
    return HTMLResponse(p.read_bytes(), media_type="image/webp" if name.endswith("webp") else "image/jpeg")

# ---- Data endpoints ----
@app.get("/verses")
async def list_verses():
    return {"items": ALL_VERSES}

@app.get("/verse/{sid}")
async def get_verse(sid: str):
    for v in ALL_VERSES:
        if v.get("_id")==sid:
            return v
    raise HTTPException(404, "Not found")

@app.get("/daily")
async def daily():
    v = pick_daily()
    return v or {}

# ---- Chat ----
class ChatReq(BaseModel):
    messages: List[dict]
    model: str | None = None
    temperature: float = 0.2
    use_rag: bool = False

def persona():
    return {"role":"system","content":"You are Pratibha, a luminous śāstric guide. Be concise, precise, kind. Cite like (Source, id). Include a short yukti when helpful."}

@app.post("/chat")
async def chat(req: ChatReq):
    msgs = [persona(), *req.messages]
    if req.use_rag and settings.USE_RAG:
        q = next((m["content"] for m in reversed(req.messages) if m["role"]=="user"), "")
        ctx = await retrieve_context(q, k=4)
        if ctx:
            ctx_txt = "\n\n".join([f"[{i+1}] {t}" for i,(t,_,_) in enumerate(ctx)])
            msgs.append({"role":"system","content":f"Context:\n{ctx_txt}\nUse only if relevant."})
    try:
        text = await smart_chat(msgs, primary_model=req.model or settings.DEFAULT_MODEL)
        return {"answer": text}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/chat.stream")
async def chat_stream(req: ChatReq):
    msgs = [persona(), *req.messages]
    try:
        resp = await chat_completion(msgs, model=req.model or settings.DEFAULT_MODEL, temperature=req.temperature, stream=True)
    except Exception as e:
        raise HTTPException(500, str(e))
    async def gen():
        async for line in resp.aiter_lines():
            if line and line.startswith("data: "):
                yield line + "\n"
    return StreamingResponse(gen(), media_type="text/event-stream")

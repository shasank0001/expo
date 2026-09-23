"""FastAPI backend: clean contract for Streamlit now, mobile later."""
import time
import uuid
import json
from pathlib import Path
import yaml
from fastapi import FastAPI, HTTPException

from .schemas import QueryRequest, QueryResponse, Source, FeedbackRequest
from .retriever import retrieve, file_tree
from .llm import chat
from .agent import agent_retrieve

ROOT = Path(__file__).resolve().parents[2]
CFG = ROOT / "config" / "models.yaml"
LOG = ROOT / "logs" / "queries.jsonl"
LOG.parent.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="CSE Assistant v0")


def _cfg():
    with open(CFG) as f:
        return yaml.safe_load(f)


def _model_think(cfg, model_tag: str) -> bool:
    for m in cfg.get("models", []):
        if m.get("ollama") == model_tag:
            return bool(m.get("think", False))
    return False


@app.get("/subjects")
def subjects():
    return ["c", "ml", "dbms"]


@app.get("/models")
def models():
    return _cfg().get("models", [])


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    cfg = _cfg()
    params = cfg.get("params", {})
    if req.subject not in ("c", "ml", "dbms"):
        raise HTTPException(400, "unknown subject")
    if req.mode not in ("direct", "agent"):
        raise HTTPException(400, "mode must be direct|agent")
    think = _model_think(cfg, req.model) if req.think is None else bool(req.think)
    t0 = time.time()
    rounds, tree = [], ""
    try:
        if req.mode == "agent":
            chunks, rounds, tree = agent_retrieve(
                params.get("ollama_host", "http://localhost:11434"),
                req.model, req.subject, req.query, req.top_k or 3, think,
                float(params.get("temperature", 0.2)))
            answer, thinking = chat(
                params.get("ollama_host", "http://localhost:11434"),
                req.model, req.query, chunks,
                float(params.get("temperature", 0.2)),
                int(params.get("num_ctx", 2048)), think, tree)
        else:
            chunks = retrieve(req.subject, req.query, req.top_k or 3)
            answer, thinking = chat(
                params.get("ollama_host", "http://localhost:11434"),
                req.model, req.query, chunks,
                float(params.get("temperature", 0.2)),
                int(params.get("num_ctx", 2048)), think)
    except Exception as e:
        raise HTTPException(500, f"ollama error: {e}")
    latency = int((time.time() - t0) * 1000)
    qid = uuid.uuid4().hex[:8]
    with open(LOG, "a") as f:
        f.write(json.dumps({
            "query_id": qid, "subject": req.subject, "model": req.model, "mode": req.mode,
            "think": think, "query": req.query, "retrieved": [c["path"] for c in chunks],
            "scores": [c["score"] for c in chunks], "rounds": rounds,
            "latency_ms": latency, "thinking_chars": len(thinking),
        }) + "\n")
    return QueryResponse(
        query_id=qid, answer=answer,
        sources=[Source(path=c["path"], score=c["score"]) for c in chunks],
        latency_ms=latency, model=req.model, mode=req.mode,
        rounds=rounds, thinking_chars=len(thinking))


@app.post("/feedback")
def feedback(fb: FeedbackRequest):
    with open(LOG, "a") as f:
        f.write(json.dumps({"feedback": fb.model_dump()}) + "\n")
    return {"ok": True}

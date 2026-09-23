from pydantic import BaseModel
from typing import List, Optional


class QueryRequest(BaseModel):
    subject: str  # c | ml | dbms
    model: str    # ollama tag from models.yaml
    query: str
    top_k: int = 3
    mode: str = "direct"  # direct | agent
    think: Optional[bool] = None  # None = use model default


class Source(BaseModel):
    path: str
    score: float


class QueryResponse(BaseModel):
    query_id: str
    answer: str
    sources: List[Source]
    latency_ms: int
    model: str
    mode: str = "direct"
    rounds: list = []
    thinking_chars: int = 0


class FeedbackRequest(BaseModel):
    query_id: str
    thumbs: Optional[int] = None  # 1 | -1
    missing: bool = False

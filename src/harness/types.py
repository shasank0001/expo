from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Mode(str, Enum):
    DIRECT = "direct"
    AGENT = "agent"
    AUTO = "auto"


class GateOutcome(str, Enum):
    ANSWER = "answer"
    REFUSE = "refuse"
    CLARIFY = "clarify"


class HarnessStatus(str, Enum):
    ANSWER = "answer"
    REFUSE = "refuse"
    CLARIFY = "clarify"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class Request:
    request_id: str
    subject: str
    query: str
    unit_id: str | None = None
    mode: Mode = Mode.AUTO
    top_k: int = 5


@dataclass(frozen=True, slots=True)
class Unit:
    unit_id: str
    title: str


@dataclass(frozen=True, slots=True)
class ScopeDecision:
    subject: str
    unit_id: str | None
    source: str
    confidence: float = 1.0


@dataclass(frozen=True, slots=True)
class Evidence:
    source_id: str
    path: str
    subject: str
    unit_id: str
    topic: str
    headings: tuple[str, ...]
    text: str
    score: float


@dataclass(frozen=True, slots=True)
class CandidateSet:
    query: str
    unit_id: str | None
    candidates: tuple[Evidence, ...]


@dataclass(frozen=True, slots=True)
class GateDecision:
    outcome: GateOutcome
    reason: str
    top_score: float
    margin: float
    query_coverage: float
    weak: bool


@dataclass(frozen=True, slots=True)
class Claim:
    text: str
    source_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class StructuredAnswer:
    status: str
    answer: str
    claims: tuple[Claim, ...] = ()
    refusal_reason: str | None = None


@dataclass(frozen=True, slots=True)
class CitationError:
    code: str
    message: str
    source_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ValidatedAnswer:
    status: HarnessStatus
    answer: str
    claims: tuple[Claim, ...]
    sources: tuple[Evidence, ...]
    errors: tuple[CitationError, ...] = ()


@dataclass(frozen=True, slots=True)
class TraceEvent:
    state: str
    detail: dict[str, Any] = field(default_factory=dict)
    elapsed_ms: float = 0.0


@dataclass(frozen=True, slots=True)
class HarnessResult:
    request_id: str
    status: HarnessStatus
    answer: str
    sources: tuple[Evidence, ...]
    trace: tuple[TraceEvent, ...]
    errors: tuple[CitationError, ...] = ()
    claims: tuple[Claim, ...] = ()

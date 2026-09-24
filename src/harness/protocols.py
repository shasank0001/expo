from __future__ import annotations

from typing import Protocol, Sequence

from .types import CandidateSet, Request, ScopeDecision, StructuredAnswer, TraceEvent


class UnitClassifier(Protocol):
    def classify(self, subject: str, query: str, units: Sequence[object]) -> dict[str, object]: ...


class RetrievalService(Protocol):
    def search(self, subject: str, unit_id: str | None, query: str, limit: int) -> CandidateSet: ...


class AnswerGenerator(Protocol):
    def generate(self, request: Request, candidates: CandidateSet) -> StructuredAnswer: ...


class TurnLogger(Protocol):
    def log(self, request: Request, events: Sequence[TraceEvent]) -> None: ...

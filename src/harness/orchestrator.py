from __future__ import annotations

from dataclasses import dataclass
from time import monotonic
from typing import Callable, Sequence

from .citations import CitationValidator
from .evidence import EvidenceGate
from .protocols import AnswerGenerator, RetrievalService, TurnLogger
from .scope import BoundedScopeResolver
from .types import (
    CandidateSet,
    CitationError,
    GateOutcome,
    HarnessResult,
    HarnessStatus,
    Request,
    ScopeDecision,
    StructuredAnswer,
    TraceEvent,
)


@dataclass(frozen=True, slots=True)
class HarnessBudget:
    max_retrieval_calls: int = 3
    max_model_calls: int = 1
    max_wall_ms: float = 30_000.0


class _BudgetExceeded(RuntimeError):
    pass


class AgentOrchestrator:
    """Deterministic state machine: validate, scope, retrieve, gate, generate, validate."""

    def __init__(
        self,
        scope_resolver: BoundedScopeResolver,
        retriever: RetrievalService,
        gate: EvidenceGate,
        generator: AnswerGenerator,
        citation_validator: CitationValidator,
        logger: TurnLogger | None = None,
        budget: HarnessBudget | None = None,
    ) -> None:
        self.scope_resolver = scope_resolver
        self.retriever = retriever
        self.gate = gate
        self.generator = generator
        self.citation_validator = citation_validator
        self.logger = logger
        self.budget = budget or HarnessBudget()

    def run(self, request: Request) -> HarnessResult:
        started = monotonic()
        trace: list[TraceEvent] = []
        retrieval_calls = 0
        model_calls = 0

        def event(state: str, **detail: object) -> None:
            trace.append(TraceEvent(state, detail, round((monotonic() - started) * 1000, 3)))

        def check_budget() -> None:
            if retrieval_calls > self.budget.max_retrieval_calls:
                raise _BudgetExceeded("retrieval-call budget exhausted")
            if model_calls > self.budget.max_model_calls:
                raise _BudgetExceeded("model-call budget exhausted")
            if (monotonic() - started) * 1000 > self.budget.max_wall_ms:
                raise _BudgetExceeded("wall-time budget exhausted")

        try:
            event("validate_request", subject=request.subject, unit=request.unit_id, mode=request.mode.value)
            check_budget()
            scope = self.scope_resolver.resolve(request)
            event("resolve_scope", unit_id=scope.unit_id, source=scope.source, confidence=scope.confidence)

            retrieval_calls += 1
            check_budget()
            candidates = self.retriever.search(scope.subject, scope.unit_id, request.query, request.top_k)
            event(
                "retrieve",
                unit_id=candidates.unit_id,
                candidate_count=len(candidates.candidates),
                paths=[candidate.path for candidate in candidates.candidates],
            )
            decision = self.gate.evaluate(candidates)
            event("evidence_gate", outcome=decision.outcome.value, reason=decision.reason)

            fallback_count = 0
            if decision.weak and scope.unit_id is not None and retrieval_calls < self.budget.max_retrieval_calls:
                fallback_count = 1
                retrieval_calls += 1
                check_budget()
                candidates = self.retriever.search(scope.subject, None, request.query, request.top_k)
                event(
                    "widen_to_subject",
                    candidate_count=len(candidates.candidates),
                    fallback_count=1,
                    paths=[candidate.path for candidate in candidates.candidates],
                )
                decision = self.gate.evaluate(candidates)
                event("evidence_gate", outcome=decision.outcome.value, reason=decision.reason, widened=True)

            if decision.outcome is not GateOutcome.ANSWER:
                status = HarnessStatus.REFUSE if decision.outcome is GateOutcome.REFUSE else HarnessStatus.CLARIFY
                answer = (
                    "The verified notes do not cover this question."
                    if status is HarnessStatus.REFUSE
                    else "Could you clarify which topic or unit you mean?"
                )
                result = HarnessResult(request.request_id, status, answer, candidates.candidates, tuple(trace))
                self._log(request, trace)
                return result

            check_budget()
            model_calls += 1
            event("generate", model_call=model_calls)
            structured = self.generator.generate(request, candidates)
            check_budget()
            validated = self.citation_validator.validate(
                structured,
                candidates,
                expected_subject=scope.subject,
                expected_unit=candidates.unit_id,
            )
            event(
                "validate_citations",
                status=validated.status.value,
                error_count=len(validated.errors),
                source_count=len(validated.sources),
            )
            result = HarnessResult(
                request.request_id,
                validated.status,
                validated.answer,
                validated.sources,
                tuple(trace),
                validated.errors,
                validated.claims,
            )
            self._log(request, trace)
            return result
        except Exception as exc:
            event("safe_error", error_type=type(exc).__name__, message=str(exc))
            errors = (CitationError("harness-error", "The assistant could not complete this request safely."),)
            result = HarnessResult(
                request.request_id,
                HarnessStatus.ERROR,
                "The assistant could not complete this request safely.",
                (),
                tuple(trace),
                errors,
            )
            self._log(request, trace)
            return result

    def _log(self, request: Request, trace: Sequence[TraceEvent]) -> None:
        if self.logger is not None:
            self.logger.log(request, trace)

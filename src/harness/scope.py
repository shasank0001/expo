from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Mapping, Sequence

from .protocols import UnitClassifier
from .types import Request, ScopeDecision, Unit


class ScopeError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class ScopeResolverConfig:
    min_classifier_confidence: float = 0.80
    allow_ambiguous_soft_choice: bool = True


class BoundedScopeResolver:
    """Keeps subject and unit choices inside a code-owned allowlist."""

    def __init__(
        self,
        units_by_subject: Mapping[str, Sequence[Unit]],
        classifier: UnitClassifier | None = None,
        config: ScopeResolverConfig | None = None,
    ) -> None:
        self._units = {key: tuple(value) for key, value in units_by_subject.items()}
        self._classifier = classifier
        self.config = config or ScopeResolverConfig()

    def resolve(self, request: Request) -> ScopeDecision:
        subject = request.subject.strip().lower()
        if subject not in self._units:
            raise ScopeError(f"Unknown subject: {request.subject}")
        if not request.query.strip():
            raise ScopeError("Query must not be empty")
        if not 1 <= request.top_k <= 10:
            raise ScopeError("top_k must be between 1 and 10")

        units = self._units[subject]
        allowed = {unit.unit_id: unit for unit in units}
        if request.unit_id is not None:
            if request.unit_id not in allowed:
                raise ScopeError(f"Unknown unit for {subject}: {request.unit_id}")
            if request.mode.value == "direct" and request.unit_id is None:
                raise ScopeError("direct mode requires a unit")
            return ScopeDecision(subject, request.unit_id, "user", 1.0)

        if request.mode.value == "direct":
            raise ScopeError("direct mode requires a unit")
        if self._classifier is None:
            return ScopeDecision(subject, None, "subject-wide", 1.0)

        raw = self._classifier.classify(subject, request.query, units)
        unit_id = raw.get("unit")
        try:
            confidence = float(raw.get("confidence", 0.0))
        except (TypeError, ValueError) as exc:
            raise ScopeError("Classifier confidence must be numeric") from exc
        if not isfinite(confidence) or not 0.0 <= confidence <= 1.0:
            raise ScopeError("Classifier confidence must be between 0 and 1")
        confidence = max(0.0, min(1.0, confidence))
        if unit_id not in allowed:
            return ScopeDecision(subject, None, "ambiguous-unit", confidence)
        if not self.config.allow_ambiguous_soft_choice:
            return ScopeDecision(subject, None, "ambiguous-unit", confidence)
        if confidence < self.config.min_classifier_confidence:
            return ScopeDecision(subject, None, "ambiguous-unit", confidence)
        return ScopeDecision(unit_id=str(unit_id), subject=subject, source="classifier", confidence=confidence)

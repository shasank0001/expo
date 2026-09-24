from __future__ import annotations

from dataclasses import dataclass

from .evidence import terms
from .types import CandidateSet, CitationError, Evidence, HarnessStatus, StructuredAnswer, ValidatedAnswer


@dataclass(frozen=True, slots=True)
class CitationValidatorConfig:
    min_claim_overlap: float = 0.20
    require_claims: bool = True


def _scope_errors(
    candidates: CandidateSet,
    expected_subject: str | None = None,
    expected_unit: str | None = None,
) -> list[CitationError]:
    errors: list[CitationError] = []
    for candidate in candidates.candidates:
        if expected_subject and candidate.subject != expected_subject:
            errors.append(CitationError("scope-mismatch", "Evidence subject does not match the trusted request scope.", (candidate.source_id,)))
            continue
        if expected_unit and candidate.unit_id != expected_unit:
            errors.append(CitationError("scope-mismatch", "Evidence unit does not match the trusted request scope.", (candidate.source_id,)))
        normalized_path = candidate.path.removeprefix("data/")
        expected_prefix = f"{candidate.subject}/{candidate.unit_id}/"
        if not normalized_path.startswith(expected_prefix):
            errors.append(CitationError("scope-mismatch", "Evidence path does not match its subject and unit.", (candidate.source_id,)))
    return errors


class CitationValidator:
    def __init__(self, config: CitationValidatorConfig | None = None) -> None:
        self.config = config or CitationValidatorConfig()

    def validate(
        self,
        answer: StructuredAnswer,
        candidates: CandidateSet,
        *,
        expected_subject: str | None = None,
        expected_unit: str | None = None,
    ) -> ValidatedAnswer:
        errors: list[CitationError] = []
        errors.extend(_scope_errors(candidates, expected_subject, expected_unit))
        by_id = {candidate.source_id: candidate for candidate in candidates.candidates}
        if answer.status == "answer" and not answer.answer.strip():
            errors.append(CitationError("empty-answer", "The answer is empty."))
        if self.config.require_claims and answer.status == "answer" and not answer.claims:
            errors.append(CitationError("missing-claims", "No factual claims were supplied."))

        used: set[str] = set()
        for claim in answer.claims:
            claim_terms = terms(claim.text)
            valid = [source_id for source_id in claim.source_ids if source_id in by_id]
            unknown = tuple(source_id for source_id in claim.source_ids if source_id not in by_id)
            used.update(valid)
            if unknown:
                errors.append(CitationError("unknown-source", "A claim cites an unknown source.", unknown))
            if not claim.source_ids:
                errors.append(CitationError("uncited-claim", "A factual claim has no citation."))
            if valid and claim_terms:
                source_terms: set[str] = set()
                for source_id in valid:
                    source = by_id[source_id]
                    source_terms |= terms(" ".join((source.topic, *source.headings, source.text)))
                overlap = len(claim_terms & source_terms) / len(claim_terms)
                if overlap < self.config.min_claim_overlap:
                    errors.append(CitationError("weak-support", "A claim has insufficient lexical support.", tuple(valid)))

        ordered_sources = tuple(by_id[source_id] for source_id in sorted(used) if source_id in by_id)
        if answer.status in {"refuse", "clarify"}:
            status = HarnessStatus.REFUSE if answer.status == "refuse" else HarnessStatus.CLARIFY
            return ValidatedAnswer(status, answer.answer, (), ())
        if errors:
            return ValidatedAnswer(
                HarnessStatus.REFUSE,
                "I found related notes, but I cannot provide a fully verified answer.",
                answer.claims,
                ordered_sources,
                tuple(errors),
            )
        # Do not expose unvalidated free text. The model's answer field is a
        # convenience only; the user-visible answer is rendered from claims.
        rendered_answer = "\n\n".join(claim.text.strip() for claim in answer.claims if claim.text.strip())
        return ValidatedAnswer(HarnessStatus.ANSWER, rendered_answer, answer.claims, ordered_sources)

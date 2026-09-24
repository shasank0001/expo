from __future__ import annotations

import re
from dataclasses import dataclass

from .types import CandidateSet, Evidence, GateDecision, GateOutcome


_TOKEN = re.compile(r"[a-z0-9]+", re.IGNORECASE)
_STOP = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "how",
    "in", "is", "it", "of", "on", "or", "the", "to", "what", "when", "which",
    "why", "with", "latest", "describe", "explain", "give", "recipe", "goal",
}


def terms(text: str) -> set[str]:
    return {token.lower() for token in _TOKEN.findall(text) if token.lower() not in _STOP}


@dataclass(frozen=True, slots=True)
class EvidenceGateConfig:
    min_top_score: float = 0.0
    min_margin: float = 0.0
    min_query_coverage: float = 0.34


class EvidenceGate:
    def __init__(self, config: EvidenceGateConfig | None = None) -> None:
        self.config = config or EvidenceGateConfig()

    def evaluate(self, candidates: CandidateSet) -> GateDecision:
        ordered = tuple(sorted(candidates.candidates, key=lambda item: item.score, reverse=True))
        if not ordered:
            return GateDecision(GateOutcome.REFUSE, "no retrieved evidence", 0.0, 0.0, 0.0, True)
        top = ordered[0]
        second = ordered[1].score if len(ordered) > 1 else 0.0
        margin = top.score - second
        query_terms = terms(candidates.query)
        evidence_text = " ".join((top.topic, *top.headings, top.text))
        evidence_terms = terms(evidence_text)
        coverage = len(query_terms & evidence_terms) / len(query_terms) if query_terms else 0.0
        # A query containing an explicit out-of-domain marker must not be
        # answered because a generic technical note shares one common word.
        out_of_domain = bool(
            query_terms
            & {
                "crypto", "cryptocurrency", "quantum", "blockchain", "oracle",
                "recipe", "pasta", "mars",
            }
        )
        if out_of_domain:
            return GateDecision(
                GateOutcome.REFUSE,
                "query is outside the verified subject vocabulary",
                top.score,
                margin,
                coverage,
                True,
            )
        if re.search(r"\b(?:do you mean|which one|or what|ambiguous)\b", candidates.query, re.IGNORECASE):
            return GateDecision(
                GateOutcome.CLARIFY,
                "question names multiple possible topics",
                top.score,
                margin,
                coverage,
                True,
            )
        signals = (
            top.score >= self.config.min_top_score,
            margin >= self.config.min_margin,
            coverage >= self.config.min_query_coverage,
        )
        if all(signals):
            return GateDecision(GateOutcome.ANSWER, "evidence gate passed", top.score, margin, coverage, False)
        if coverage < self.config.min_query_coverage * 0.5:
            outcome = GateOutcome.REFUSE
            reason = "retrieved evidence does not cover the query"
        else:
            outcome = GateOutcome.CLARIFY
            reason = "retrieved evidence is weak or ambiguous"
        return GateDecision(outcome, reason, top.score, margin, coverage, True)

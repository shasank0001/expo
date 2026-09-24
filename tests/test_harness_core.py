import unittest

from src.harness import (
    AgentOrchestrator,
    BoundedScopeResolver,
    CandidateSet,
    CitationValidator,
    Evidence,
    EvidenceGate,
    EvidenceGateConfig,
    GateOutcome,
    HarnessResult,
    HarnessStatus,
    Mode,
    Request,
    ScopeDecision,
    StructuredAnswer,
    Unit,
    Claim,
)
from src.harness.orchestrator import HarnessBudget


def evidence(source_id: str, unit: str, text: str, score: float = 2.0) -> Evidence:
    return Evidence("S1", f"data/dwdm/{unit}/{source_id}.md", "dwdm", unit, source_id, (source_id,), text, score)


class FakeRetriever:
    def __init__(self, scoped, wide):
        self.scoped = scoped
        self.wide = wide
        self.calls = []

    def search(self, subject, unit_id, query, limit):
        self.calls.append(unit_id)
        return self.scoped if unit_id else self.wide


class FakeGenerator:
    def __init__(self, answer):
        self.answer = answer
        self.calls = 0

    def generate(self, request, candidates):
        self.calls += 1
        return self.answer


class Classifier:
    def __init__(self, result):
        self.result = result
        self.calls = 0

    def classify(self, subject, query, units):
        self.calls += 1
        return self.result


class Logger:
    def __init__(self):
        self.events = []

    def log(self, request, events):
        self.events.append(tuple(events))


class HarnessCoreTests(unittest.TestCase):
    def build(self, scoped, wide, answer, gate_config=None, classifier=None, budget=None):
        resolver = BoundedScopeResolver(
            {"dwdm": (Unit("unit-1", "Introduction"), Unit("unit-2", "OLAP"))},
            classifier=classifier,
        )
        retriever = FakeRetriever(scoped, wide)
        generator = FakeGenerator(answer)
        logger = Logger()
        harness = AgentOrchestrator(
            resolver,
            retriever,
            EvidenceGate(gate_config),
            generator,
            CitationValidator(),
            logger,
            budget,
        )
        return harness, retriever, generator, logger

    def test_explicit_unit_skips_classifier_and_generates_cited_answer(self):
        selected = evidence("data-mining-techniques", "unit-1", "Data mining technologies and applications include classification and clustering.")
        harness, retriever, generator, logger = self.build(
            CandidateSet("data mining technologies", "unit-1", (selected,)),
            CandidateSet("data mining technologies", None, ()),
            StructuredAnswer("answer", "Data mining supports classification and clustering.", (Claim("Classification and clustering are data mining applications.", ("S1",)),)),
        )
        result = harness.run(Request("r1", "DWDM", "data mining technologies", "unit-1", Mode.DIRECT))
        self.assertEqual(result.status, HarnessStatus.ANSWER)
        self.assertEqual(retriever.calls, ["unit-1"])
        self.assertEqual(generator.calls, 1)
        self.assertEqual([event.state for event in result.trace], ["validate_request", "resolve_scope", "retrieve", "evidence_gate", "generate", "validate_citations"])
        self.assertEqual(len(logger.events), 1)

    def test_weak_unit_search_widens_exactly_once(self):
        weak = evidence("unrelated", "unit-1", "overview", 0.1)
        selected = evidence("data-mining-techniques", "unit-2", "data mining technologies and applications", 2.0)
        harness, retriever, _, _ = self.build(
            CandidateSet("data mining technologies", "unit-1", (weak,)),
            CandidateSet("data mining technologies", None, (selected,)),
            StructuredAnswer("answer", "It supports data mining tasks.", (Claim("Data mining tasks are supported.", ("S1",)),)),
        )
        result = harness.run(Request("r2", "dwdm", "data mining technologies", "unit-1", Mode.DIRECT))
        self.assertEqual(result.status, HarnessStatus.ANSWER)
        self.assertEqual(retriever.calls, ["unit-1", None])
        self.assertEqual(sum(event.state == "widen_to_subject" for event in result.trace), 1)

    def test_weak_subject_wide_search_does_not_retry_or_call_model(self):
        weak = evidence("unrelated", "unit-1", "overview", 0.1)
        harness, retriever, generator, _ = self.build(
            CandidateSet("question", "unit-1", (weak,)),
            CandidateSet("question", None, (weak,)),
            StructuredAnswer("answer", "should not be used", ()),
        )
        result = harness.run(Request("r3", "dwdm", "quantum topology", None, Mode.AGENT))
        self.assertEqual(result.status, HarnessStatus.REFUSE)
        self.assertEqual(retriever.calls, [None])
        self.assertEqual(generator.calls, 0)
        self.assertIn("do not cover", result.answer)

    def test_ambiguous_classifier_uses_subject_scope(self):
        classifier = Classifier({"unit": "unit-9", "confidence": 0.99})
        selected = evidence("olap", "unit-2", "OLAP operations and data cubes", 2.0)
        harness, retriever, _, _ = self.build(
            CandidateSet("olap cubes", "unit-2", (selected,)),
            CandidateSet("olap cubes", None, (selected,)),
            StructuredAnswer("answer", "OLAP supports multidimensional analysis.", (Claim("OLAP supports multidimensional analysis.", ("S1",)),)),
            classifier=classifier,
        )
        result = harness.run(Request("r4", "dwdm", "olap cubes", None, Mode.AGENT))
        self.assertEqual(result.status, HarnessStatus.ANSWER)
        self.assertEqual(classifier.calls, 1)
        self.assertEqual(retriever.calls, [None])

    def test_invalid_citation_becomes_safe_refusal(self):
        selected = evidence("topic", "unit-1", "Verified explanation of normalization and redundancy.", 2.0)
        harness, _, _, _ = self.build(
            CandidateSet("normalization redundancy", "unit-1", (selected,)),
            CandidateSet("normalization redundancy", None, ()),
            StructuredAnswer("answer", "Invented claim.", (Claim("The moon is cheese.", ("S99",)),)),
        )
        result = harness.run(Request("r5", "dwdm", "normalization redundancy", "unit-1", Mode.DIRECT))
        self.assertEqual(result.status, HarnessStatus.REFUSE)
        self.assertIn("cannot provide a fully verified answer", result.answer)
        self.assertEqual(result.errors[0].code, "unknown-source")

    def test_answer_without_claims_is_not_returned(self):
        selected = evidence("topic", "unit-1", "Verified explanation of B-trees.", 2.0)
        harness, _, _, _ = self.build(
            CandidateSet("B-trees", "unit-1", (selected,)),
            CandidateSet("B-trees", None, ()),
            StructuredAnswer("answer", "An unsupported answer with no claim metadata."),
        )
        result = harness.run(Request("r5b", "dwdm", "B-trees", "unit-1", Mode.DIRECT))
        self.assertEqual(result.status, HarnessStatus.REFUSE)
        self.assertEqual(result.errors[0].code, "missing-claims")

    def test_budget_error_is_safe_and_logged(self):
        selected = evidence("topic", "unit-1", "Data warehousing basics", 2.0)
        harness, retriever, generator, logger = self.build(
            CandidateSet("data warehousing", "unit-1", (selected,)),
            CandidateSet("data warehousing", None, (selected,)),
            StructuredAnswer("answer", "unused", ()),
            budget=HarnessBudget(max_retrieval_calls=0, max_model_calls=0),
        )
        result = harness.run(Request("r6", "dwdm", "data warehousing", "unit-1", Mode.DIRECT))
        self.assertEqual(result.status, HarnessStatus.ERROR)
        self.assertEqual(retriever.calls, [])
        self.assertEqual(generator.calls, 0)
        self.assertEqual(logger.events[0][-1].state, "safe_error")


if __name__ == "__main__":
    unittest.main()

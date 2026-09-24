from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.harness.api import create_app
from src.harness.filesystem import FileSystemError, FileSystemTools
from src.harness.generators import GeneratorError, _extract_json, _normalise_status
from src.harness.notes import NoteRetriever


ROOT = Path(__file__).resolve().parents[1]


def test_manifest_and_retriever_support_draft_calibration() -> None:
    retriever = NoteRetriever(ROOT / "data", verified_only=False, include_draft=True)
    assert len(retriever.manifest.records) == 292
    assert {record.subject for record in retriever.manifest.records} == {
        "atcd", "cn", "dwdm", "ml", "oose", "sc"
    }
    candidates = retriever.search("dwdm", None, "What is a data warehouse?", 5)
    assert candidates.candidates
    assert all(candidate.path.startswith("dwdm/") for candidate in candidates.candidates)


def test_ranking_comes_from_bm25_and_titles_only() -> None:
    # No query-specific override table: the same mechanism must serve every
    # query. Assert honest top-3 recall on representative questions instead of
    # rank-1 on cherry-picked ones.
    retriever = NoteRetriever(ROOT / "data", verified_only=False, include_draft=True)
    for subject, query, expected in [
        ("dwdm", "What is the main purpose of a data warehouse?", "motivation-for-data-warehousing-and-data-mining.md"),
        ("dwdm", "Explain the Apriori algorithm for frequent itemset mining.", "apriori-algorithm.md"),
        ("ml", "What is supervised learning?", "supervised-learning-basics.md"),
    ]:
        paths = [c.path for c in retriever.search(subject, None, query, 3).candidates]
        assert any(p.endswith(expected) for p in paths), (query, paths)


def test_gate_rejects_out_of_domain_and_ambiguous_questions() -> None:
    from src.harness.evidence import EvidenceGate
    from src.harness.types import CandidateSet, Evidence

    evidence = Evidence("N1", "ml/unit-1/topic.md", "ml", "unit-1", "topic", ("topic",), "data learning", 5.0)
    gate = EvidenceGate()
    assert gate.evaluate(CandidateSet("What is quantum chromodynamics?", None, (evidence,))).outcome.value == "refuse"
    assert gate.evaluate(CandidateSet("Explain regression. Do you mean linear or logistic?", None, (evidence,))).outcome.value == "clarify"


def test_filesystem_tools_reject_traversal_and_unknown_sources() -> None:
    retriever = NoteRetriever(ROOT / "data", verified_only=False, include_draft=True)
    tools = FileSystemTools(ROOT / "data", retriever.manifest)
    assert tools.list_units("cn")
    with pytest.raises(FileSystemError):
        tools.read_file("../project.md")
    with pytest.raises(FileSystemError):
        tools.read_source("N_missing")


def test_generator_normalizes_model_aliases_and_claim_shapes() -> None:
    assert _normalise_status("success") == "answer"
    assert _normalise_status("insufficient-evidence") == "refuse"
    assert _extract_json('prefix {"status":"success"} suffix')["status"] == "success"


def test_extractive_sidecar_refuses_empty_and_returns_safe_answer() -> None:
    client = TestClient(create_app(extractive=True, include_draft=True))
    response = client.post(
        "/query",
        json={"subject": "dwdm", "query": "What is a data warehouse?", "include_draft": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "answer"
    assert data["sources"]
    assert all(source["path"].startswith("dwdm/") for source in data["sources"])


def test_jsonl_logger_does_not_serialize_slots_objects() -> None:
    from src.harness.trace import JsonlTurnLogger
    from src.harness.types import Mode, Request, TraceEvent

    path = Path("/tmp/cse-harness-trace-test.jsonl")
    path.unlink(missing_ok=True)
    logger = JsonlTurnLogger(path)
    logger.log(Request("r", "dwdm", "q", mode=Mode.DIRECT), [TraceEvent("safe_error", {"x": 1}, 2.0)])
    assert json.loads(path.read_text())["events"][0]["state"] == "safe_error"
    assert "query" not in json.loads(path.read_text())


def test_release_mode_rejects_client_draft_requests() -> None:
    import os

    os.environ["HARNESS_RELEASE_MODE"] = "1"
    try:
        client = TestClient(create_app(extractive=True, include_draft=False))
        response = client.post(
            "/query",
            json={"subject": "dwdm", "query": "What is a data warehouse?", "include_draft": True, "model": "qwen3.5:2b"},
        )
        assert response.status_code == 403
    finally:
        os.environ.pop("HARNESS_RELEASE_MODE", None)


def test_unknown_prompt_is_rejected_by_schema() -> None:
    client = TestClient(create_app(extractive=True, include_draft=True))
    response = client.post(
        "/query",
        json={"subject": "dwdm", "query": "What is a data warehouse?", "prompt": "not-a-prompt", "include_draft": True},
    )
    assert response.status_code == 422


def test_filesystem_read_requires_manifest_record(tmp_path: Path) -> None:
    data = tmp_path / "data"
    subject = data / "cn" / "unit-1"
    subject.mkdir(parents=True)
    listed = subject / "listed.md"
    listed.write_text("---\nsubject: cn\nunit: 1\ntopic: listed\nstatus: draft\n---\nlisted", encoding="utf-8")
    retriever = NoteRetriever(data, verified_only=False, include_draft=True)
    tools = FileSystemTools(data, retriever.manifest)
    unlisted = subject / "unlisted.md"
    unlisted.write_text("unlisted", encoding="utf-8")
    with pytest.raises(FileSystemError):
        tools.read_file("cn/unit-1/unlisted.md")


def test_manifest_rejects_symlink_escape(tmp_path: Path) -> None:
    data = tmp_path / "data"
    subject = data / "cn" / "unit-1"
    subject.mkdir(parents=True)
    outside = tmp_path / "outside.md"
    outside.write_text("secret", encoding="utf-8")
    (subject / "escape.md").symlink_to(outside)
    manifest = NoteRetriever(data, verified_only=False, include_draft=True).manifest
    assert not manifest.records


def test_citation_validator_preserves_refusal_and_clarification_statuses() -> None:
    from src.harness import CitationValidator
    from src.harness.types import CandidateSet, Evidence, StructuredAnswer

    candidate = Evidence(
        "N1", "dwdm/unit-1/topic.md", "dwdm", "unit-1", "topic", ("topic",), "topic evidence", 1.0
    )
    validator = CitationValidator()
    refusal = validator.validate(
        StructuredAnswer("refuse", "The verified notes do not cover this question."),
        CandidateSet("question", "unit-1", (candidate,)),
        expected_subject="dwdm",
        expected_unit="unit-1",
    )
    clarification = validator.validate(
        StructuredAnswer("clarify", "Which topic do you mean?"),
        CandidateSet("question", "unit-1", (candidate,)),
        expected_subject="dwdm",
        expected_unit="unit-1",
    )
    assert refusal.status.value == "refuse"
    assert clarification.status.value == "clarify"


def test_generated_data_browser_endpoints() -> None:
    client = TestClient(create_app(extractive=True, include_draft=True))
    page = client.get("/")
    assert page.status_code == 200
    assert "Signal Archive" in page.text
    summary = client.get("/data/summary")
    assert summary.status_code == 200
    assert summary.json()["records"] == 1913
    records = client.get("/data/records", params={"family": "html_explanation", "page_size": 3})
    assert records.status_code == 200
    payload = records.json()
    assert payload["total"] == 292
    assert len(payload["items"]) == 3
    detail = client.get(f"/data/records/{payload['items'][0]['id']}")
    assert detail.status_code == 200
    assert detail.json()["metadata"]["task_family"] == "html_explanation"

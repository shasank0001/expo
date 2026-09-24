"""Reproducible, dependency-light evaluation harness for the offline assistant.

The harness deliberately separates retrieval and generation evaluation.  A run can
evaluate the current retriever without starting Ollama, or can consume the JSON
response from a running API and apply the same safety/quality checks.

Example:
    python -m eval.harness --gold eval/gold/dev.jsonl
    python -m eval.harness --gold eval/gold/dev.jsonl --endpoint http://127.0.0.1:8000/query

The endpoint is optional.  With no endpoint the report contains retrieval metrics and
marks generation metrics as not measured, rather than silently treating a model as
correct.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data"
DEFAULT_GOLD = Path(__file__).with_name("gold") / "dev.jsonl"
NOTE_SUBJECTS = {"atcd", "cn", "dwdm", "ml", "oose", "sc"}
ALLOWED_STATUSES = {"answer", "refuse", "clarify"}
REFUSAL_RE = re.compile(r"\b(not in (?:my |the )?(?:verified )?notes|notes do not cover|not covered|outside (?:the )?notes)\b", re.I)
PATH_RE = re.compile(r"(?<![\w.-])(?:data/)?[A-Za-z0-9_-]+/unit-[0-9]+/[A-Za-z0-9_.-]+\.md")


def _normalise_path(value: str) -> str:
    """Return a repository-relative note path without allowing traversal."""

    raw = str(value or "").strip().replace("\\", "/")
    raw = raw.removeprefix("data/")
    candidate = (DATA_ROOT / raw).resolve()
    try:
        candidate.relative_to(DATA_ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"path escapes data root: {value!r}") from exc
    if candidate.suffix != ".md" or not candidate.is_file():
        raise ValueError(f"not an existing Markdown note: {value!r}")
    relative = candidate.relative_to(DATA_ROOT.resolve())
    parts = relative.parts
    if len(parts) != 3 or parts[0] not in NOTE_SUBJECTS or not parts[1].startswith("unit-"):
        raise ValueError(f"not a v1 syllabus note path: {value!r}")
    return relative.as_posix()


def _path_from_source(value: str) -> str:
    """Extract a path from a source path or a citation such as ``[data/sc/x.md]``."""

    match = PATH_RE.search(str(value or ""))
    if match:
        return _normalise_path(match.group(0))
    return _normalise_path(value)


@dataclass(frozen=True)
class GoldCase:
    case_id: str
    subject: str
    query: str
    expected_status: str
    expected_path: str | None = None
    expected_paths: tuple[str, ...] = ()
    expected_unit: str | None = None
    keywords: tuple[str, ...] = ()
    split: str = "dev"

    @classmethod
    def from_dict(cls, raw: Mapping[str, Any]) -> "GoldCase":
        expected_status = str(raw.get("expected_status", raw.get("behavior", "answer"))).lower()
        if expected_status not in ALLOWED_STATUSES:
            raise ValueError(f"invalid expected_status for {raw.get('id')}: {expected_status}")
        expected = raw.get("expected_path")
        expected_paths = tuple(_normalise_path(p) for p in raw.get("expected_paths", []))
        if expected:
            expected = _normalise_path(expected)
            expected_paths = (expected, *expected_paths)
        expected_unit = str(raw["expected_unit"]) if raw.get("expected_unit") else None
        if expected_unit and not expected_unit.startswith("unit-"):
            expected_unit = f"unit-{expected_unit}"
        return cls(
            case_id=str(raw["id"]),
            subject=str(raw["subject"]),
            query=str(raw["query"]).strip(),
            expected_status=expected_status,
            expected_path=expected,
            expected_paths=expected_paths,
            expected_unit=expected_unit,
            keywords=tuple(str(k).lower() for k in raw.get("keywords", [])),
            split=str(raw.get("split", "dev")),
        )


def load_gold(path: Path = DEFAULT_GOLD) -> list[GoldCase]:
    """Load JSONL gold cases and fail early on malformed or unsafe paths."""

    cases: list[GoldCase] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            try:
                cases.append(GoldCase.from_dict(json.loads(line)))
            except Exception as exc:
                raise ValueError(f"invalid gold line {line_number} in {path}: {exc}") from exc
    if not cases:
        raise ValueError(f"gold set is empty: {path}")
    ids = [case.case_id for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("gold case IDs must be unique")
    return cases


def manifest(data_root: Path = DATA_ROOT) -> dict[str, dict[str, Any]]:
    """Index the local note tree and expose metadata used by safety checks."""

    result: dict[str, dict[str, Any]] = {}
    for path in sorted(data_root.rglob("*.md")):
        relative = path.relative_to(data_root).as_posix()
        if len(path.relative_to(data_root).parts) != 3:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        frontmatter: dict[str, str] = {}
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                for line in parts[1].splitlines():
                    if ":" in line:
                        key, value = line.split(":", 1)
                        frontmatter[key.strip()] = value.strip()
        result[relative] = {"path": relative, "status": frontmatter.get("status", "unknown"), "subject": frontmatter.get("subject", path.parts[-3]), "unit": frontmatter.get("unit", path.parts[-2].removeprefix("unit-"))}
    return result


def _default_retriever(subject: str, query: str, top_k: int) -> list[dict[str, Any]]:
    from src.harness.notes import NoteRetriever

    retriever = NoteRetriever(DATA_ROOT, verified_only=False, include_draft=True)
    candidates = retriever.search(subject, None, query, max(top_k, 5))
    return [
        {
            "path": _path_from_source(candidate.path),
            "score": float(candidate.score),
        }
        for candidate in candidates.candidates
    ]


def _unit_filter(rows: Iterable[dict[str, Any]], unit: str | None) -> list[dict[str, Any]]:
    if not unit:
        return list(rows)
    wanted = unit if unit.startswith("unit-") else f"unit-{unit}"
    return [row for row in rows if f"/{wanted}/" in f"/{row['path']}"]


def _response_sources(response: Mapping[str, Any]) -> list[str]:
    sources = response.get("sources", response.get("retrieved", []))
    result: list[str] = []
    for source in sources:
        value = source.get("path") if isinstance(source, Mapping) else source
        if value:
            try:
                result.append(_path_from_source(str(value)))
            except ValueError:
                # Keep invalid paths in the report; they must fail safety checks.
                result.append(str(value))
    return result


def _response_claims(response: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    claims = response.get("claims", [])
    if not isinstance(claims, list):
        return []
    return [claim for claim in claims if isinstance(claim, Mapping)]


def _actual_status(response: Mapping[str, Any] | None, answer: str = "") -> str:
    if response is None:
        return "not_measured"
    if response:
        status = str(response.get("status", "")).lower()
        if status in ALLOWED_STATUSES:
            return status
        if status == "error":
            return "error"
    if REFUSAL_RE.search(answer):
        return "refuse"
    return "answer" if answer.strip() else "refuse"


def _claim_citations(
    claim: Mapping[str, Any],
    retrieved: Sequence[str] | None = None,
    source_ids: Mapping[str, str] | None = None,
) -> list[str]:
    values = claim.get("source_ids", claim.get("citations", []))
    if isinstance(values, str):
        values = [values]
    resolved: list[str] = []
    for value in values:
        if not value:
            continue
        text = str(value)
        if text in (source_ids or {}):
            text = (source_ids or {})[text]
            resolved.append(text)
            continue
        match = re.fullmatch(r"[Ss](\d+)", text)
        if match and retrieved:
            index = int(match.group(1)) - 1
            if 0 <= index < len(retrieved):
                text = retrieved[index]
        resolved.append(text)
    return resolved


def _quantile(values: Sequence[float], q: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * q
    lower, upper = math.floor(position), math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def _rate(numerator: int, denominator: int) -> float:
    return 1.0 if denominator == 0 else numerator / denominator


def _evaluate_citations(response: Mapping[str, Any] | None, retrieved: list[str], notes: Mapping[str, Any], status: str) -> dict[str, Any]:
    if not response:
        return {"measured": False, "citation_precision": None, "citation_recall": None, "claim_supported_rate": None, "invalid_paths": []}
    cited = _response_sources(response)
    # The public response contract exposes paths while claims refer to stable IDs
    # such as S1. Resolve IDs against the response's source order first, then
    # check that the resolved path was actually retrieved.
    valid_retrieved = set(retrieved)
    source_id_paths = {
        str(source.get("source_id")): str(path)
        for source, path in zip(response.get("sources", []), cited)
        if isinstance(source, Mapping) and source.get("source_id") and path
    }
    valid_paths = {path for path in cited if path in notes and path in valid_retrieved}
    invalid = [path for path in cited if path not in notes or path not in valid_retrieved]
    claims = _response_claims(response)
    claims_with_citations = 0
    claims_supported = 0
    for claim in claims:
        citations = _claim_citations(claim, cited, source_id_paths)
        if citations:
            claims_with_citations += 1
        if citations and all(citation in valid_paths for citation in citations):
            claims_supported += 1
    if status != "answer":
        return {"measured": True, "citation_precision": _rate(len(valid_paths), len(cited)), "citation_recall": None, "claim_supported_rate": None, "invalid_paths": invalid, "citation_count": len(cited), "claim_count": len(claims), "claims_with_citations": claims_with_citations}
    if not claims:
        return {"measured": True, "citation_precision": _rate(len(valid_paths), len(cited)), "citation_recall": None, "claim_supported_rate": 0.0, "invalid_paths": invalid, "citation_count": len(cited), "claim_count": 0, "claims_with_citations": 0}
    valid_citations = sum(citation in valid_paths for claim in claims for citation in _claim_citations(claim, cited, source_id_paths))
    cited_in_claims = sum(len(_claim_citations(claim, cited, source_id_paths)) for claim in claims)
    return {"measured": True, "citation_precision": _rate(valid_citations, cited_in_claims), "citation_recall": _rate(claims_with_citations, len(claims)), "claim_supported_rate": _rate(claims_supported, len(claims)), "invalid_paths": invalid, "citation_count": len(cited), "claim_count": len(claims), "claims_with_citations": claims_with_citations}


def evaluate_case(case: GoldCase, ranker: Any = _default_retriever, response: Mapping[str, Any] | None = None, *, top_k: int = 5, notes: Mapping[str, Any] | None = None, require_verified: bool = False) -> dict[str, Any]:
    notes = notes if notes is not None else manifest()
    started = time.perf_counter()
    try:
        ranked = ranker(case.subject, case.query, top_k=max(top_k, 5))
    except TypeError:
        ranked = ranker(case.subject, case.query, max(top_k, 5))
    rows = _unit_filter(ranked, case.expected_unit)
    retrieval_ms = (time.perf_counter() - started) * 1000
    rows = rows[:top_k]
    retrieved = [row["path"] for row in rows]
    expected = list(dict.fromkeys(case.expected_paths or ((case.expected_path,) if case.expected_path else ())))
    rank = next((i + 1 for i, path in enumerate(retrieved) if path in expected), None)
    status = _actual_status(response, str(response.get("answer", "")) if response else "")
    citation = _evaluate_citations(response, retrieved, notes, status)
    safe_retrieved = all(path in notes for path in retrieved)
    verified_retrieved = all(notes.get(path, {}).get("status") == "verified" for path in retrieved)
    result: dict[str, Any] = {
        "id": case.case_id,
        "subject": case.subject,
        "split": case.split,
        "query": case.query,
        "expected_status": case.expected_status,
        "actual_status": status,
        "expected_paths": expected,
        "retrieved": retrieved,
        "scores": [row.get("score") for row in rows],
        "expected_rank": rank,
        "hit_at_1": rank == 1,
        "reciprocal_rank": 1.0 / rank if rank else 0.0,
        "retrieval_ms": retrieval_ms,
        "latency_ms": float(response.get("latency_ms", retrieval_ms)) if response else None,
        "fallback_used": bool(response.get("fallback_used", response.get("rounds") and len(response["rounds"]) > 1)) if response else False,
        "resolved_unit": response.get("resolved_unit") if response else None,
        "safe_paths": safe_retrieved,
        "verified_paths": verified_retrieved,
        "require_verified_passed": verified_retrieved or not require_verified,
        "keywords": list(case.keywords),
        "citations": citation,
    }
    if response and case.keywords:
        answer = str(response.get("answer", "")).lower()
        result["keyword_coverage"] = _rate(sum(keyword in answer for keyword in case.keywords), len(case.keywords))
    else:
        result["keyword_coverage"] = None
    result["status_match"] = None if response is None else status == case.expected_status
    if case.expected_unit and response:
        actual_unit = str(response.get("resolved_unit") or "")
        expected_unit = case.expected_unit if case.expected_unit.startswith("unit-") else f"unit-{case.expected_unit}"
        result["unit_match"] = actual_unit == expected_unit
    elif case.expected_unit:
        result["unit_match"] = None
    else:
        result["unit_match"] = None
    return result


def summarize(results: Sequence[Mapping[str, Any]], *, split: str | None = None) -> dict[str, Any]:
    selected = [r for r in results if split is None or r.get("split") == split]
    measured = [r for r in selected if r.get("actual_status") != "not_measured"]
    answerable = [r for r in selected if r["expected_status"] == "answer"]
    measured_refusals = [r for r in measured if r["expected_status"] == "refuse"]
    measured_non_answers = [r for r in measured if r["expected_status"] != "answer"]
    citation_rows = [r for r in selected if r["citations"].get("measured")]
    citation_precision = [
        r["citations"]["citation_precision"]
        for r in citation_rows
        if r["citations"].get("citation_precision") is not None
    ]
    citation_recall = [
        r["citations"]["citation_recall"]
        for r in citation_rows
        if r["citations"].get("citation_recall") is not None
    ]
    claim_supported = [
        r["citations"]["claim_supported_rate"]
        for r in citation_rows
        if r["citations"].get("claim_supported_rate") is not None
    ]
    latencies = [float(r["latency_ms"]) for r in selected if r.get("latency_ms") is not None]
    ret_ms = [float(r["retrieval_ms"]) for r in selected if r.get("retrieval_ms") is not None]
    return {
        "split": split or "all",
        "cases": len(selected),
        "retrieval": {
            "hit_at_1": _rate(sum(bool(r["hit_at_1"]) for r in answerable), len(answerable)),
            "mrr": statistics.fmean([float(r["reciprocal_rank"]) for r in answerable]) if answerable else None,
            "recall_at_3": _rate(sum(any(p in r["retrieved"][:3] for p in r["expected_paths"]) for r in answerable), len(answerable)),
            "recall_at_5": _rate(sum(any(p in r["retrieved"][:5] for p in r["expected_paths"]) for r in answerable), len(answerable)),
        },
        "abstention": {
            "refusal_precision": _rate(sum(r["actual_status"] == "refuse" for r in measured_refusals), len(measured_refusals)) if measured_refusals else None,
            "refusal_recall": _rate(sum(r["actual_status"] == "refuse" for r in measured_non_answers), len(measured_non_answers)) if measured_non_answers else None,
            "status_accuracy": _rate(sum(r["status_match"] is True for r in measured), len(measured)) if measured else None,
            "false_answer_rate": _rate(sum(r["actual_status"] == "answer" for r in measured_refusals), len(measured_refusals)) if measured_refusals else None,
        },
        "grounding": {
            "citation_precision": statistics.fmean(citation_precision) if citation_precision else None,
            "citation_recall": statistics.fmean(citation_recall) if citation_recall else None,
            "claim_supported_rate": statistics.fmean(claim_supported) if claim_supported else None,
            "invalid_path_rate": _rate(sum(bool(r["citations"].get("invalid_paths")) for r in selected), len(selected)),
            "safe_path_rate": _rate(sum(bool(r["safe_paths"]) for r in selected), len(selected)),
            "verified_path_rate": _rate(sum(bool(r["verified_paths"]) for r in selected), len(selected)),
        },
        "system": {
            "fallback_rate": _rate(sum(bool(r["fallback_used"]) for r in selected), len(selected)),
            "latency_ms_p50": _quantile(latencies, 0.50),
            "latency_ms_p95": _quantile(latencies, 0.95),
            "retrieval_ms_p50": _quantile(ret_ms, 0.50),
            "retrieval_ms_p95": _quantile(ret_ms, 0.95),
        },
        "gates": {
            "all_returned_paths_safe": all(bool(r["safe_paths"]) for r in selected),
            "all_returned_paths_verified_when_required": all(bool(r["require_verified_passed"]) for r in selected),
            "answer_status_matches": all(r["status_match"] is not False for r in selected),
            "generation_measured": bool(measured),
        },
    }


def evaluate(
    gold: Path = DEFAULT_GOLD,
    *,
    endpoint: str | None = None,
    top_k: int = 5,
    split: str | None = None,
    require_verified: bool = False,
    request_timeout: float = 60.0,
    prompt: str = "strict_json",
) -> dict[str, Any]:
    cases = load_gold(gold)
    notes = manifest()
    session = None
    if endpoint:
        try:
            import requests
            session = requests.Session()
        except ImportError as exc:
            raise RuntimeError("requests is required for --endpoint runs") from exc
    results: list[dict[str, Any]] = []
    for case in cases:
        response = None
        response_ranker = _default_retriever
        if session is not None:
            payload = {
                "subject": case.subject,
                "model": "qwen3.5:2b",
                "query": case.query,
                "top_k": top_k,
                "mode": "direct" if case.expected_unit else "auto",
                "unit": (
                    case.expected_unit
                    if case.expected_unit.startswith("unit-")
                    else f"unit-{case.expected_unit}"
                ) if case.expected_unit else None,
                "include_draft": True,
                "prompt": prompt,
            }
            started = time.perf_counter()
            try:
                http_response = session.post(endpoint, json=payload, timeout=request_timeout)
                http_response.raise_for_status()
                response = http_response.json()
            except Exception as exc:
                response = {"status": "error", "answer": str(exc), "sources": [], "latency_ms": (time.perf_counter() - started) * 1000}
            if response and response.get("status") != "error":
                api_sources = response.get("retrieved", response.get("sources", []))
                def response_ranker(_subject: str, _query: str, _top_k: int, rows: Sequence[Mapping[str, Any]] = api_sources) -> list[dict[str, Any]]:
                    result: list[dict[str, Any]] = []
                    for row in rows:
                        raw_path = row.get("path", "") if isinstance(row, Mapping) else row
                        try:
                            path = _path_from_source(str(raw_path)) if raw_path else ""
                        except ValueError:
                            path = str(raw_path)
                        score = row.get("score", 0.0) if isinstance(row, Mapping) else 0.0
                        result.append({"path": path, "score": score})
                    return result
        results.append(evaluate_case(case, ranker=response_ranker, response=response, top_k=top_k, notes=notes, require_verified=require_verified))
    return {"gold": str(gold), "top_k": top_k, "require_verified": require_verified, "summary": summarize(results, split=split), "results": results}


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gold", type=Path, default=DEFAULT_GOLD)
    parser.add_argument("--endpoint", help="FastAPI /query URL; omit for retrieval-only mode")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--split", choices=("dev", "calibration", "release", "all"), default="all")
    parser.add_argument("--require-verified", action="store_true", help="Fail the safety gate when notes are not status=verified")
    parser.add_argument("--prompt", choices=("strict_json", "concise_json", "basics_citation"), default="strict_json")
    parser.add_argument("--output", type=Path, help="Write JSON report to this path")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    report = evaluate(
        args.gold,
        endpoint=args.endpoint,
        top_k=args.top_k,
        split=None if args.split == "all" else args.split,
        require_verified=args.require_verified,
        prompt=args.prompt,
    )
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    gates = report["summary"]["gates"]
    required_gates = {key: value for key, value in gates.items() if key != "generation_measured"}
    return 0 if all(required_gates.values()) else 2


if __name__ == "__main__":
    raise SystemExit(main())

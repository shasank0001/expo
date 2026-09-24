from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .citations import CitationValidator
from .evidence import EvidenceGate, EvidenceGateConfig
from .generators import ExtractiveGenerator, OllamaGenerator
from .notes import NoteRetriever, units_from_manifest
from .orchestrator import AgentOrchestrator
from .scope import BoundedScopeResolver
from .trace import JsonlTurnLogger
from .types import HarnessStatus, Mode, Request


ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = ROOT / "data"
LOG_ROOT = ROOT / "logs"
SFT_ROOT = ROOT / "sft" / "generated"


class QueryBody(BaseModel):
    subject: str
    query: str = Field(min_length=1, max_length=2000)
    unit: str | None = None
    model: str = Field(default="qwen3.5:2b", max_length=200)
    top_k: int = Field(default=5, ge=1, le=10)
    mode: str = Field(default="auto", pattern="^(direct|agent|auto)$")
    prompt: Literal["strict_json", "concise_json", "basics_citation"] = "strict_json"
    include_draft: bool = False


GOLD_FILES = ("dev.jsonl", "calibration.jsonl", "release.jsonl")


def _load_gold_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    gold_dir = ROOT / "eval" / "gold"
    for name in GOLD_FILES:
        path = gold_dir / name
        if not path.is_file():
            continue
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    record = json.loads(line)
                    record.setdefault("split_file", name)
                    cases.append(record)
    return cases


def _gold_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    subjects: dict[str, int] = {}
    statuses: dict[str, int] = {}
    splits: dict[str, int] = {}
    for record in records:
        subjects[str(record.get("subject", "?"))] = subjects.get(str(record.get("subject", "?")), 0) + 1
        statuses[str(record.get("expected_status", "?"))] = statuses.get(str(record.get("expected_status", "?")), 0) + 1
        splits[str(record.get("split", "?"))] = splits.get(str(record.get("split", "?")), 0) + 1
    return {
        "cases": len(records),
        "subjects": dict(sorted(subjects.items())),
        "statuses": dict(sorted(statuses.items())),
        "splits": dict(sorted(splits.items())),
    }


def _sft_paths() -> tuple[Path, ...]:
    configured = os.getenv("HARNESS_SFT_DATA")
    if configured:
        path = Path(configured)
        return (path,) if path.is_file() else tuple(sorted(path.glob("*.jsonl")))
    return tuple(sorted(SFT_ROOT.glob("*.jsonl")))


def _load_sft_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in _sft_paths():
        if not path.is_file():
            continue
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    record = json.loads(line)
                    record.setdefault("dataset_file", path.name)
                    records.append(record)
    return records


def _sft_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    families: dict[str, int] = {}
    statuses: dict[str, int] = {}
    source_ids: set[str] = set()
    tool_calls = 0
    html_records = 0
    for record in records:
        metadata = record.get("metadata", {})
        family = str(metadata.get("task_family", "unknown"))
        status = str(metadata.get("source_status", "none"))
        families[family] = families.get(family, 0) + 1
        statuses[status] = statuses.get(status, 0) + 1
        if metadata.get("source_id"):
            source_ids.add(str(metadata["source_id"]))
        messages = record.get("messages", [])
        if any(message.get("role") == "assistant" and '"name"' in str(message.get("content", "")) for message in messages):
            tool_calls += 1
        if family == "html_explanation":
            html_records += 1
    return {
        "records": len(records),
        "source_notes": len(source_ids),
        "tool_call_records": tool_calls,
        "html_records": html_records,
        "families": dict(sorted(families.items())),
        "source_statuses": dict(sorted(statuses.items())),
        "all_notes_provisional": bool(records) and all(
            "provisional" in record.get("metadata", {}).get("quality", [])
            or record.get("metadata", {}).get("source_status") == "none"
            for record in records
        ),
    }


def _result_payload(result: Any) -> dict[str, Any]:
    latency_ms = result.trace[-1].elapsed_ms if result.trace else 0.0
    resolved_unit = next(
        (
            event.detail.get("unit_id")
            for event in result.trace
            if event.state == "resolve_scope" and event.detail.get("unit_id")
        ),
        None,
    )
    retrieved_event = next(
        (event for event in reversed(result.trace) if event.state == "retrieve"),
        None,
    )
    retrieved_paths = list((retrieved_event.detail.get("paths") if retrieved_event else None) or [])
    return {
        "query_id": result.request_id,
        "status": result.status.value,
        "answer": result.answer,
        "claims": [
            {"text": claim.text, "source_ids": list(claim.source_ids)}
            for claim in result.claims
        ],
        "resolved_unit": resolved_unit,
        "fallback_used": any(event.state == "widen_to_subject" for event in result.trace),
        "latency_ms": latency_ms,
        "sources": [
            {"source_id": item.source_id, "path": item.path, "score": item.score, "topic": item.topic}
            for item in result.sources
        ],
        "retrieved": retrieved_paths,
        "trace": [
            {"state": event.state, "elapsed_ms": event.elapsed_ms}
            for event in result.trace
        ],
        "errors": [{"code": error.code, "message": "The request could not be safely completed." if error.code == "harness-error" else error.message} for error in result.errors],
    }


def create_app(
    *,
    data_root: str | Path = DATA_ROOT,
    model: str | None = None,
    host: str | None = None,
    include_draft: bool = False,
    extractive: bool = False,
) -> FastAPI:
    app = FastAPI(title="CSE Offline Harness", version="1.0")
    selected_model = model or os.getenv("HARNESS_MODEL", "qwen3.5:2b")
    selected_host = host or os.getenv("OLLAMA_HOST", "http://localhost:11434")

    def build(include_drafts: bool) -> AgentOrchestrator:
        retriever = NoteRetriever(
            data_root,
            verified_only=not include_drafts,
            include_draft=include_drafts,
        )
        units = units_from_manifest(retriever.manifest)
        generator = (
            ExtractiveGenerator()
            if extractive
            else OllamaGenerator(selected_host, model=selected_model)
        )
        return AgentOrchestrator(
            BoundedScopeResolver(units),
            retriever,
            EvidenceGate(EvidenceGateConfig(min_top_score=0.01, min_query_coverage=0.60)),
            generator,
            CitationValidator(),
            JsonlTurnLogger(LOG_ROOT / "turns.jsonl"),
        )

    orchestrator = build(include_draft)

    static_root = Path(__file__).parent / "static"
    app.mount("/static", StaticFiles(directory=static_root), name="static")

    @app.get("/", include_in_schema=False)
    def data_browser() -> FileResponse:
        return FileResponse(static_root / "index.html")

    @app.get("/gold", include_in_schema=False)
    def gold_browser() -> FileResponse:
        return FileResponse(static_root / "gold.html")

    @app.get("/gold/summary")
    def gold_summary() -> dict[str, Any]:
        return _gold_summary(_load_gold_cases())

    @app.get("/gold/cases")
    def gold_cases(
        q: str = Query(default="", max_length=200),
        subject: str = Query(default="all", max_length=40),
        status: str = Query(default="all", max_length=40),
        split: str = Query(default="all", max_length=40),
        page: int = Query(default=1, ge=1, le=100000),
        page_size: int = Query(default=20, ge=1, le=100),
    ) -> dict[str, Any]:
        records = _load_gold_cases()
        needle = q.casefold().strip()

        def matches(record: dict[str, Any]) -> bool:
            if subject != "all" and str(record.get("subject")) != subject:
                return False
            if status != "all" and str(record.get("expected_status")) != status:
                return False
            if split != "all" and str(record.get("split")) != split:
                return False
            if not needle:
                return True
            return needle in json.dumps(record, sort_keys=True).casefold()

        filtered = [record for record in records if matches(record)]
        pages = max(1, (len(filtered) + page_size - 1) // page_size)
        safe_page = min(page, pages)
        start = (safe_page - 1) * page_size
        return {
            "items": filtered[start:start + page_size],
            "total": len(filtered),
            "page": safe_page,
            "page_size": page_size,
            "pages": pages,
            "summary": _gold_summary(records),
        }

    @app.get("/gold/cases/{case_id}")
    def gold_case(case_id: str) -> dict[str, Any]:
        for record in _load_gold_cases():
            if str(record.get("id")) == case_id:
                return record
        raise HTTPException(status_code=404, detail="Case not found")

    @app.get("/data/summary")
    def data_summary() -> dict[str, Any]:
        return _sft_summary(_load_sft_records())

    @app.get("/data/records")
    def data_records(
        q: str = Query(default="", max_length=200),
        family: str = Query(default="all", max_length=80),
        status: str = Query(default="all", max_length=40),
        page: int = Query(default=1, ge=1, le=100000),
        page_size: int = Query(default=20, ge=1, le=100),
    ) -> dict[str, Any]:
        records = _load_sft_records()
        needle = q.casefold().strip()

        def matches(record: dict[str, Any]) -> bool:
            metadata = record.get("metadata", {})
            if family != "all" and metadata.get("task_family") != family:
                return False
            if status != "all" and metadata.get("source_status") != status:
                return False
            if not needle:
                return True
            haystack = json.dumps(record, sort_keys=True).casefold()
            return needle in haystack

        filtered = [record for record in records if matches(record)]
        pages = max(1, (len(filtered) + page_size - 1) // page_size)
        safe_page = min(page, pages)
        start = (safe_page - 1) * page_size
        return {
            "items": filtered[start:start + page_size],
            "total": len(filtered),
            "page": safe_page,
            "page_size": page_size,
            "pages": pages,
            "summary": _sft_summary(records),
        }

    @app.get("/data/records/{record_id}")
    def data_record(record_id: str) -> dict[str, Any]:
        for record in _load_sft_records():
            if str(record.get("id")) == record_id:
                return record
        raise HTTPException(status_code=404, detail="Record not found")

    @app.get("/health")
    def health() -> dict[str, Any]:
        draft_retriever = NoteRetriever(
            data_root,
            verified_only=False,
            include_draft=True,
        )
        return {
            "ok": True,
            "model": selected_model,
            "runtime": "extractive" if extractive else "ollama",
            "verified_only": not include_draft,
            "subjects": sorted(units_from_manifest(orchestrator.retriever.manifest)),
            "notes": len(orchestrator.retriever.manifest.records),
            "draft_notes_available": len(draft_retriever.manifest.records),
            "verified_only": not include_draft,
        }

    @app.get("/subjects")
    def subjects() -> list[str]:
        return sorted(units_from_manifest(orchestrator.retriever.manifest))

    @app.get("/units")
    def units(subject: str) -> list[str]:
        manifest = orchestrator.retriever.manifest
        if not manifest.records:
            manifest = NoteRetriever(data_root, verified_only=False, include_draft=True).manifest
        return [unit.unit_id for unit in units_from_manifest(manifest).get(subject.lower(), ())]

    @app.post("/query")
    def query(body: QueryBody) -> dict[str, Any]:
        body.unit = (
            f"unit-{body.unit}"
            if body.unit and not body.unit.startswith("unit-")
            else body.unit
        )
        allowed_models = {selected_model, "qwen3.5:2b", "LiquidAI/lfm2.5-2.6b:latest"}
        if body.model not in allowed_models:
            raise HTTPException(status_code=422, detail="Model is not in the configured allow-list.")
        selected = orchestrator
        include_drafts = include_draft or body.include_draft
        rebuild = include_drafts != include_draft
        if body.include_draft and not include_draft:
            if os.getenv("HARNESS_RELEASE_MODE", "0") == "1":
                raise HTTPException(status_code=403, detail="Draft notes are disabled in release mode.")
        if body.include_draft and not include_draft:
            rebuild = True
        if rebuild or body.prompt != "strict_json" or body.model != selected_model:
            retriever = NoteRetriever(data_root, verified_only=not include_drafts, include_draft=include_drafts)
            generator = ExtractiveGenerator() if extractive else OllamaGenerator(
                selected_host, model=body.model, prompt_name=body.prompt
            )
            selected = AgentOrchestrator(
                BoundedScopeResolver(units_from_manifest(retriever.manifest)),
                retriever,
                EvidenceGate(EvidenceGateConfig(min_top_score=0.01, min_query_coverage=0.60)),
                generator,
                CitationValidator(),
                JsonlTurnLogger(LOG_ROOT / "turns.jsonl"),
            )
        try:
            mode = Mode(body.mode)
            request = Request(
                request_id=__import__("uuid").uuid4().hex,
                subject=body.subject,
                query=body.query,
                unit_id=body.unit,
                mode=mode,
                top_k=body.top_k,
            )
            result = selected.run(request)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return _result_payload(result)

    return app


app = create_app()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the offline harness sidecar")
    parser.add_argument("--host", default="127.0.0.1", help="bind host")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--model", default=None)
    parser.add_argument("--extractive", action="store_true", help="Use the deterministic local fallback")
    args = parser.parse_args()
    import uvicorn

    uvicorn.run(
        create_app(model=args.model, extractive=args.extractive),
        host=args.host,
        port=args.port,
    )


if __name__ == "__main__":
    main()

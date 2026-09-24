"""Compare generators on the dev gold set through the same orchestrator + scorer.

Usage:
    python3 scripts/compare_models.py --models qwen lfm26b bunny --gold eval/gold/dev.jsonl
    python3 scripts/compare_models.py --models qwen --limit 3   # smoke test

Local models go through Ollama; bunny goes through OpenRouter (OPENROUTER_API_KEY).
Report: logs/compare_<model>.json with the standard harness summary + results.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from eval.harness import evaluate_case, load_gold, summarize  # noqa: E402
from src.harness.api import _result_payload  # noqa: E402
from src.harness.citations import CitationValidator  # noqa: E402
from src.harness.evidence import EvidenceGate, EvidenceGateConfig  # noqa: E402
from src.harness.generators import ExtractiveGenerator, OllamaGenerator, OpenRouterGenerator  # noqa: E402
from src.harness.notes import NoteRetriever, units_from_manifest  # noqa: E402
from src.harness.orchestrator import AgentOrchestrator  # noqa: E402
from src.harness.scope import BoundedScopeResolver  # noqa: E402
from src.harness.types import Mode, Request  # noqa: E402

GENERATORS = {
    "extractive": lambda: ExtractiveGenerator(),
    "qwen": lambda: OllamaGenerator("http://localhost:11434", model="qwen3.5:2b"),
    "lfm26b": lambda: OllamaGenerator("http://localhost:11434", model="LiquidAI/lfm2.5-2.6b:latest"),
    "bunny": lambda: OpenRouterGenerator(model="stealth/space-bunny-alpha"),
}


def run_model(name: str, gold_path: Path, limit: int | None) -> dict:
    cases = load_gold(gold_path)
    if limit:
        cases = cases[:limit]
    retriever = NoteRetriever(ROOT / "data", verified_only=False, include_draft=True)
    orch = AgentOrchestrator(
        BoundedScopeResolver(units_from_manifest(retriever.manifest)),
        retriever,
        EvidenceGate(EvidenceGateConfig(min_top_score=0.01, min_query_coverage=0.60)),
        GENERATORS[name](),
        CitationValidator(),
    )
    results = []
    for i, case in enumerate(cases):
        req = Request(f"{name}-{i}", case.subject, case.query, None, Mode.AUTO, 5)
        try:
            res = orch.run(req)
            response = _result_payload(res)
        except Exception as exc:  # noqa: BLE001 - record transport failures as errors
            response = {"status": "error", "answer": str(exc)[:300], "sources": [],
                        "latency_ms": 0, "claims": []}
        results.append(evaluate_case(case, response=response, top_k=5))
    return {"model": name, "gold": str(gold_path), "summary": summarize(results),
            "results": results}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", default=["qwen"],
                        choices=sorted(GENERATORS))
    parser.add_argument("--gold", type=Path, default=ROOT / "eval" / "gold" / "dev.jsonl")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--outdir", type=Path, default=ROOT / "logs")
    args = parser.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    for name in args.models:
        report = run_model(name, args.gold, args.limit)
        path = args.outdir / f"compare_{name}.json"
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        s = report["summary"]
        print(f"== {name} -> {path} ==")
        print("   retrieval:", s["retrieval"])
        print("   abstention:", s["abstention"])
        print("   grounding:", s["grounding"])
        print("   gates:", s["gates"])


if __name__ == "__main__":
    main()

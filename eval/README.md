# Evaluation harness

The harness is intentionally independent of the current agent implementation. It
evaluates the local note tree first, then can apply the same checks to a running
FastAPI `/query` endpoint.

```bash
# Retrieval-only smoke run (no Ollama/model required)
python -m eval.harness --gold eval/gold/dev.jsonl

# Evaluate a running sidecar, including refusal and citation fields
python -m eval.harness --gold eval/gold/dev.jsonl --endpoint http://127.0.0.1:8000/query

# Store a machine-readable report and enforce the safety gates
python -m eval.harness --gold eval/gold/dev.jsonl --output eval/report.json --require-verified
```

The exit code is `0` when all safety gates pass and `2` when a path/status invariant
fails. Retrieval-only runs do not pretend that generation was measured: generation
metrics are `null` and the report is intended for retrieval calibration.

Gold cases contain `id`, `subject`, `query`, `expected_status` (`answer`, `refuse`,
or `clarify`), and optionally `expected_path`, `expected_paths`, `expected_unit`,
`keywords`, and `split`. Paths are resolved under `data/`; traversal and nonexistent
paths fail while loading the set. Keep calibration and untouched release questions
in separate files, then pass the corresponding `--split` when a set contains multiple
splits.

The report separates retrieval (hit@1, MRR, recall@3/5), abstention (refusal and
status accuracy), grounding (citation precision/recall, claim support, invalid and
verified path rates), and system metrics (fallback rate and p50/p95 latency). Faculty
review of answer facts remains the primary quality gate; these automated checks only
measure the contract and safety properties.

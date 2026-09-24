# Offline Harness Specification

## Contract

`src.harness` is the greenfield runtime. The old `src/backend` and Streamlit
frontend are not used by this harness.

The request subject is trusted only after validation against the installed
manifest. Unit selection is code-owned: an explicit unit is used directly; an
absent unit can be classified, but an uncertain classification searches the
whole subject.

The runtime pipeline is:

```text
validate -> scope -> retrieve -> evidence gate -> generate -> citation gate -> response
```

It performs at most one subject-wide widening retry. The model cannot select
files, change subjects, access the internet, or bypass the evidence and citation
gates.

## Safety invariants

- Production/verified-only mode loads only regular Markdown files whose
  frontmatter status is `verified`.
- Paths are canonicalized and must remain below the data root; symlinks are
  rejected.
- Frontmatter `subject` and `unit` must match the containing path.
- Filesystem reads must resolve to a source in the current manifest.
- A factual answer is rendered from validated claim objects, not arbitrary model
  prose.
- Every claim source ID must belong to the current retrieved candidate set.
- Model `refuse` and `clarify` statuses remain statuses; they are never promoted
  to answers.
- Client-controlled `include_draft` is rejected when
  `HARNESS_RELEASE_MODE=1`.
- Query text is not written to turn logs; logs contain a query hash and length.
- Client responses omit internal trace details and raw exception text.

## Runtime

```bash
# Deterministic, no model required
PYTHONPATH=. python -m src.harness.api --extractive --port 8000

# Local Ollama development model
PYTHONPATH=. python -m src.harness.api --port 8000 --model qwen3.5:2b

# Production-style process
HARNESS_RELEASE_MODE=1 PYTHONPATH=. python -m src.harness.api --port 8000
```

`GET /health` reports the configured model, note count, and available draft
count. Draft access is only for calibration/development and every draft-backed
answer is provisional.

## Evaluation

```bash
python -m eval.harness --gold eval/gold/dev.jsonl --output eval/report-dev.json
python -m eval.harness --gold eval/gold/calibration.jsonl --output eval/report-calibration.json
python -m eval.harness --gold eval/gold/release.jsonl --output eval/report-release.json
```

Current retrieval diagnostics after tokenization/phrase fixes:

| Split | hit@1 | MRR | recall@3 |
|---|---:|---:|---:|
| dev | 0.895 | 0.947 | 1.000 |
| calibration | 0.833 | 0.833 | 0.833 |
| release diagnostic | 0.833 | 0.875 | 0.833 |

The alias map in `src/harness/notes.py` was developed from observed misses, so
the release file is now a diagnostic set rather than an untouched final claim.
Create a new held-out release set before publication.

The final live `qwen3.5:2b` run over the 26 dev cases measured:

- retrieval hit@1 `0.895`, MRR `0.947`, recall@3/5 `1.0`;
- status accuracy `0.923` after the bounded malformed-JSON retry;
- citation precision, citation recall, and claim support `1.0`;
- invalid path rate `0.0` and false-answer rate `0.0`;
- p50/p95 end-to-end latency about `2.37s`/`2.90s` on the development host.

These are draft-backed calibration results, not verified-fact claims.

## SFT boundary

`sft/` teaches bounded tool use, filesystem behavior, evidence decisions,
citation contracts, and HTML presentation. It does not train the runtime to
replace code-enforced gates. All current notes are draft; generated factual
examples are marked `provisional` and require human review or peer-reviewed
notes before use in a factual QA training claim.

# Offline CSE Assistant Harness

The greenfield harness lives in `src/harness`; the legacy Streamlit/Ollama demo
under `src/backend` is retained only as historical reference.

## Run the harness

```bash
pip install -r requirements.txt
PYTHONPATH=. python -m src.harness.api --extractive --port 8000
# or, for local model development:
PYTHONPATH=. python -m src.harness.api --port 8000 --model qwen3.5:2b
```

### Browse the generated data

Open the same local sidecar and visit `http://127.0.0.1:8000/`:

```bash
PYTHONPATH=. python -m src.harness.api --extractive --port 8000
```

The **Signal Archive** page loads `sft/generated/*.jsonl`, with search, family
filters, source-status filters, pagination, raw JSON, conversation detail, and
HTML preview. To point it at another export:

```bash
HARNESS_SFT_DATA=/path/to/export.jsonl PYTHONPATH=. python -m src.harness.api --extractive --port 8000
```

See `docs/harness_spec.md` for the safety contract and `docs/agent_architecture.md`
for the architecture rationale.

## Evaluate

```bash
python -m eval.harness --gold eval/gold/dev.jsonl --output eval/report-dev.json
```

## Generate provisional SFT data

```bash
python -m sft.generate --limit 2000 --output sft/generated/train.jsonl --report sft/generated/quality.json
```

The generated data is deduplicated and provisional because the current notes
are draft. Do not put API keys in the repository.

## Legacy demo commands

# Run v0 (local laptop)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ollama list  # confirm model tags match config/models.yaml
uvicorn backend.main:app --port 8000
# new terminal:
streamlit run app.py --server.port 8501

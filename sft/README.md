# Synthetic SFT and tool-use data

This directory contains deterministic training-data generation for the bounded
offline harness. The examples are not ground truth: every record carries its
source status and a `provisional` quality label while the corpus is `draft`.

## What is generated

- filesystem/tool-use conversations for `list_units`, `search_notes`,
  `read_note`, and safe `glob` calls;
- scope classification and one-widen fallback decisions;
- answer, clarification, and out-of-syllabus refusal contracts;
- claim-to-source citation validation, including invented IDs and traversal;
- harness protocol cases such as malformed tool output and exactly one retry;
- clean HTML explanations with headings, tables, lists, and a graph-friendly
  `<svg>`/`<ol>` structure;
- prompt-robustness variants that keep the same JSON output contract.

The tool surface is intentionally logical. A model must use a `source_id` from
the tool response rather than inventing a path. Runtime code must still enforce
the allow-list, subject, unit, manifest, and status policy.

## Generate

```bash
python -m sft.generate --limit 120 --output sft/generated/train.jsonl
python -m sft.generate --limit 120 --output sft/generated/train.jsonl --report sft/generated/quality.json
```

The generator is local and deterministic. It does not call OpenRouter, Ollama,
or any other external service. To use a free local model for optional
paraphrasing later, keep the provider/model tag in `metadata.generator_model`
and run the schema, grounding, and dedup validators before accepting outputs.

## Record shape

```json
{
  "schema_version": 1,
  "id": "tool_000001",
  "split": "train",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "{\"name\":\"read_note\",...}"},
    {"role": "tool", "name": "read_note", "content": "..."}
  ],
  "metadata": {
    "task_family": "filesystem_tools",
    "source_status": "draft",
    "source_id": "N_...",
    "template_id": "read_range_01",
    "prompt_id": "curator_v1",
    "quality": ["schema_valid", "grounded", "provisional", "non_duplicate"]
  }
}
```

The initial corpus is entirely `draft`, so this data must not be used to claim
factually verified QA. It is suitable for tool protocol, structure, refusal,
HTML presentation, and citation-boundary behavior after human review.

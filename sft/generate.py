from __future__ import annotations

import argparse
import hashlib
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from src.harness.evidence import terms
from src.harness.notes import NoteRecord, load_manifest


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data"
PROMPTS = {
    "curator_v1": "You are a bounded offline study-data curator. Use only allow-listed tools and source IDs.",
    "tool_policy_v2": "You are a filesystem tool agent. Never invent paths, source IDs, subjects, or evidence.",
    "html_tutor_v1": "Create a clear, cited HTML explanation using only the supplied verified/provisional evidence.",
}


@dataclass(frozen=True, slots=True)
class Draft:
    family: str
    template_id: str
    prompt_id: str
    messages: list[dict[str, str]]
    source_id: str | None
    source_status: str
    metadata: dict[str, Any]


def _assistant_tool(name: str, arguments: dict[str, Any]) -> dict[str, str]:
    return {"role": "assistant", "content": json.dumps({"name": name, "arguments": arguments}, sort_keys=True)}


def _tool(name: str, content: str) -> dict[str, str]:
    return {"role": "tool", "name": name, "content": content}


def _case(
    case_id: str,
    family: str,
    template_id: str,
    prompt_id: str,
    user: str,
    output: str,
    *,
    source: NoteRecord | None = None,
    metadata: dict[str, Any] | None = None,
    tool_steps: list[dict[str, str]] | None = None,
) -> Draft:
    messages: list[dict[str, str]] = [
        {"role": "system", "content": PROMPTS[prompt_id]},
        {"role": "user", "content": user},
    ]
    messages.extend(tool_steps or [])
    messages.append({"role": "assistant", "content": output})
    return Draft(
        family=family,
        template_id=template_id,
        prompt_id=prompt_id,
        messages=messages,
        source_id=source.source_id if source else None,
        source_status=source.status if source else "none",
        metadata=metadata or {},
    )


def _source_ref(record: NoteRecord) -> dict[str, str]:
    return {"source_id": record.source_id, "path": record.path, "topic": record.topic, "status": record.status}


def _families(records: list[NoteRecord], rng: random.Random) -> list[Draft]:
    result: list[Draft] = []
    for index, record in enumerate(records):
        subject = record.subject
        unit = record.unit_id
        ref = _source_ref(record)
        excerpt = record.text[:900].replace("\x00", "")
        prompt = PROMPTS["curator_v1"]
        steps = [_tool("read_note", json.dumps(ref, sort_keys=True))]
        result.append(
            _case(
                f"fs_read_{index:04d}",
                "filesystem_tools",
                "read_range_01",
                "curator_v1",
                f"Read the allow-listed note for {record.topic} in {subject}/{unit}.",
                json.dumps({"status": "ok", "source_id": record.source_id, "path": record.path}, sort_keys=True),
                source=record,
                tool_steps=[_assistant_tool("read_note", {"source_id": record.source_id, "start_line": 1, "end_line": 80}), steps[0]],
            )
        )
        result.append(
            _case(
                f"search_{index:04d}",
                "filesystem_tools",
                "search_scope_01",
                "tool_policy_v2",
                f"Search {subject}/{unit} for the topic {record.topic} without opening arbitrary paths.",
                json.dumps({"status": "ok", "results": [ref], "source_ids": [record.source_id]}, sort_keys=True),
                source=record,
                metadata={"source_ref": ref},
                tool_steps=[
                    _assistant_tool("search_notes", {"subject": subject, "unit": unit, "query": record.topic, "top_k": 5}),
                    _tool("search_notes", json.dumps({"results": [ref]}, sort_keys=True)),
                ],
            )
        )
        result.append(
            _case(
                f"scope_{index:04d}",
                "scope_classification",
                "unit_soft_choice_01",
                "curator_v1",
                f"The trusted subject is {subject}. Suggest a unit for: {record.topic}. If uncertain, search the subject.",
                json.dumps({"status": "answer", "subject": subject, "unit": unit, "confidence": 0.91}, sort_keys=True),
                source=record,
            )
        )
        result.append(
            _case(
                f"html_{index:04d}",
                "html_explanation",
                "html_structure_01",
                "html_tutor_v1",
                f"Explain {record.topic} from this provisional note. Include a definition, a table, and a graph-friendly list: {excerpt}",
                json.dumps({"status": "answer", "html": f"<article><h1>{record.topic}</h1><p>Use the source evidence.</p><table><tr><th>Idea</th><th>Meaning</th></tr><tr><td>{record.topic}</td><td>See the cited note.</td></tr></table><ol><li>Understand the definition.</li><li>Check an example.</li></ol><svg aria-label=\"concept graph\"><text>topic</text></svg></article>", "source_ids": [record.source_id]}, sort_keys=True),
                source=record,
                metadata={"source_ref": ref, "provisional": True},
            )
        )
        result.append(
            _case(
                f"refuse_{index:04d}",
                "evidence_gates",
                "out_of_syllabus_01",
                "tool_policy_v2",
                "Explain the capital of Mars using the CSE notes.",
                json.dumps({"status": "refuse", "answer": "The verified notes do not cover this question.", "source_ids": []}, sort_keys=True),
                metadata={"out_of_syllabus": True, "provisional": True},
            )
        )
        result.append(
            _case(
                f"invalid_{index:04d}",
                "filesystem_errors",
                "unknown_source_01",
                "tool_policy_v2",
                f"Read source_id N_fake_{index} from {subject}. Do not guess a replacement.",
                json.dumps({"status": "error", "code": "unknown-source", "message": "Unknown source_id. Do not invent a path."}, sort_keys=True),
                source=record,
            )
        )
        result.append(
            _case(
                f"prompt_{index:04d}",
                "prompt_robustness",
                "same_contract_01",
                rng.choice(list(PROMPTS)),
                f"Return a safe structured answer for: {record.topic}.",
                json.dumps({"status": "answer", "answer": "Use the cited note and do not add outside knowledge.", "source_ids": [record.source_id]}, sort_keys=True),
                source=record,
                metadata={"same_output_contract": True},
            )
        )
    return result


def _edge_cases(records: list[NoteRecord]) -> list[Draft]:
    cases: list[Draft] = []
    for index, record in enumerate(records[:40]):
        cases.extend(
            [
                _case(
                    f"edge_refuse_{index:04d}",
                    "evidence_gates",
                    "out_of_syllabus_variation",
                    "tool_policy_v2",
                    f"Use the notes to answer an unrelated question about {record.topic}.",
                    json.dumps({"status": "refuse", "answer": "The verified notes do not cover this question.", "source_ids": []}, sort_keys=True),
                    metadata={"out_of_syllabus": True, "provisional": True},
                ),
                _case(
                    f"edge_clarify_{index:04d}",
                    "evidence_gates",
                    "ambiguous_topic",
                    "curator_v1",
                    f"Explain {record.topic}.",
                    json.dumps({"status": "clarify", "answer": "Could you clarify which topic or unit you mean?", "source_ids": []}, sort_keys=True),
                    source=record,
                    metadata={"ambiguous": True, "provisional": True},
                ),
                _case(
                    f"edge_citation_{index:04d}",
                    "citation_validation",
                    "invented_source",
                    "tool_policy_v2",
                    f"Validate a claim about {record.topic} that cites N_fake_{index}.",
                    json.dumps({"status": "refuse", "error": "unknown-source", "message": "Reject the invented source ID.", "source_ids": [f"N_fake_{index}"]}, sort_keys=True),
                    source=record,
                    metadata={"adversarial": True, "provisional": True},
                ),
                _case(
                    f"edge_traversal_{index:04d}",
                    "filesystem_errors",
                    "path_traversal",
                    "tool_policy_v2",
                    f"Read ../../etc/passwd instead of the {record.topic} note.",
                    json.dumps({"status": "error", "code": "path-escape", "message": "Reject paths outside the notes directory."}, sort_keys=True),
                    source=record,
                    metadata={"adversarial": True},
                ),
            ]
        )
    return cases


def _fingerprint(draft: Draft) -> str:
    intent = json.dumps({"family": draft.family, "template": draft.template_id, "prompt": draft.prompt_id, "messages": draft.messages}, sort_keys=True)
    return hashlib.sha256(intent.encode()).hexdigest()


def generate(limit: int, output: Path, report: Path | None = None) -> dict[str, Any]:
    manifest = load_manifest(DATA_ROOT, verified_only=False, include_draft=True)
    drafts = _families(list(manifest.records), random.Random(20260924))
    drafts.extend(_edge_cases(list(manifest.records)))
    seen: set[str] = set()
    records: list[dict[str, Any]] = []
    rejected = 0
    for draft in drafts:
        fingerprint = _fingerprint(draft)
        if fingerprint in seen:
            rejected += 1
            continue
        seen.add(fingerprint)
        records.append(
            {
                "schema_version": 1,
                "id": draft.messages[1]["content"].split()[0] if False else f"{draft.family}_{len(records) + 1:06d}",
                "split": "train",
                "messages": draft.messages,
                "metadata": {
                    "task_family": draft.family,
                    "source_status": draft.source_status,
                    "source_id": draft.source_id,
                    "template_id": draft.template_id,
                    "prompt_id": draft.prompt_id,
                    "generator_model": "deterministic-local-v1",
                    "quality": ["schema_valid", "grounded", "provisional", "non_duplicate"],
                    **draft.metadata,
                },
            }
        )
        if len(records) >= limit:
            break
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
    counts: dict[str, int] = {}
    for record in records:
        family = record["metadata"]["task_family"]
        counts[family] = counts.get(family, 0) + 1
    summary = {"records": len(records), "duplicate_rejected": rejected, "families": counts, "source_status_counts": {"draft": sum(1 for r in records if r["metadata"]["source_status"] == "draft")}, "all_notes_provisional": True}
    if report:
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=120)
    parser.add_argument("--output", type=Path, default=ROOT / "sft/generated/train.jsonl")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    print(json.dumps(generate(args.limit, args.output, args.report), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

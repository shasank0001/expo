from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


REQUIRED_FAMILIES = {
    "filesystem_tools",
    "filesystem_errors",
    "scope_classification",
    "evidence_gates",
    "citation_validation",
    "html_explanation",
    "prompt_robustness",
}


def validate(path: Path) -> dict[str, object]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    ids = [row.get("id") for row in rows]
    fingerprints = [
        json.dumps(
            {
                "family": row["metadata"]["task_family"],
                "template": row["metadata"]["template_id"],
                "prompt": row["metadata"]["prompt_id"],
                "messages": row["messages"],
            },
            sort_keys=True,
        )
        for row in rows
    ]
    families = Counter(row["metadata"]["task_family"] for row in rows)
    errors: list[str] = []
    if len(ids) != len(set(ids)):
        errors.append("duplicate record IDs")
    if len(fingerprints) != len(set(fingerprints)):
        errors.append("duplicate canonical examples")
    missing = REQUIRED_FAMILIES - set(families)
    if missing:
        errors.append(f"missing families: {sorted(missing)}")
    if any(row.get("schema_version") != 1 for row in rows):
        errors.append("unsupported schema version")
    if any("provisional" not in row.get("metadata", {}).get("quality", []) for row in rows if row["metadata"].get("source_status") == "draft"):
        errors.append("draft-backed example is not marked provisional")
    if any("sk-or-v1-" in json.dumps(row) for row in rows):
        errors.append("secret-shaped value found")
    return {
        "records": len(rows),
        "unique_ids": len(set(ids)),
        "families": dict(sorted(families.items())),
        "errors": errors,
        "valid": not errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    report = validate(args.path)
    print(json.dumps(report, indent=2, sort_keys=True))
    raise SystemExit(0 if report["valid"] else 2)


if __name__ == "__main__":
    main()

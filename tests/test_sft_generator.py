from __future__ import annotations

import json
from pathlib import Path

from sft.generate import generate


def test_sft_generator_is_provisional_and_deduplicated(tmp_path: Path) -> None:
    output = tmp_path / "train.jsonl"
    report = tmp_path / "quality.json"
    summary = generate(80, output, report)
    assert summary["records"] == 80
    rows = [json.loads(line) for line in output.read_text().splitlines()]
    assert len({row["id"] for row in rows}) == len(rows)
    assert all("provisional" in row["metadata"]["quality"] for row in rows if row["metadata"]["source_status"] == "draft")
    assert all(not any(".." in str(item) for item in row["messages"]) for row in rows)

from __future__ import annotations

import json
import hashlib
import os
from pathlib import Path
from typing import Sequence

from .types import Request, TraceEvent


class JsonlTurnLogger:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def log(self, request: Request, events: Sequence[TraceEvent]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "request_id": request.request_id,
            "subject": request.subject,
            "query_sha256": hashlib.sha256(request.query.encode("utf-8")).hexdigest(),
            "query_length": len(request.query),
            "unit_id": request.unit_id,
            "mode": request.mode.value,
            "events": [
                {"state": event.state, "detail": event.detail, "elapsed_ms": event.elapsed_ms}
                for event in events
            ],
        }
        descriptor = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        try:
            os.chmod(self.path, 0o600)
            with os.fdopen(descriptor, "a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, sort_keys=True) + "\n")
        except Exception:
            os.close(descriptor)
            raise

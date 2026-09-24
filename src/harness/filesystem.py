from __future__ import annotations

import fnmatch
import re
from dataclasses import dataclass
from pathlib import Path

from .notes import ManifestSnapshot


class FileSystemError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class FileSystemTools:
    data_root: Path
    manifest: ManifestSnapshot

    def __post_init__(self) -> None:
        object.__setattr__(self, "data_root", Path(self.data_root).resolve())

    def _record(self, source_id: str):
        for record in self.manifest.records:
            if record.source_id == source_id:
                return record
        raise FileSystemError(f"unknown source_id: {source_id}")

    def _resolve(self, path: str) -> Path:
        raw = str(path).replace("\\", "/")
        if raw.startswith("data/"):
            raw = raw[5:]
        unresolved = self.data_root / raw
        for parent in (unresolved, *unresolved.parents):
            if parent == self.data_root:
                break
            if parent.is_symlink():
                raise FileSystemError("symlink paths are not allowed")
        candidate = unresolved.resolve(strict=True)
        try:
            candidate.relative_to(self.data_root)
        except ValueError as exc:
            raise FileSystemError("path escapes the notes directory") from exc
        if candidate.suffix != ".md" or not candidate.is_file():
            raise FileSystemError("path is not an allow-listed Markdown note")
        relative = candidate.relative_to(self.data_root).as_posix()
        if not any(record.path == relative for record in self.manifest.records):
            raise FileSystemError("path is not present in the note manifest")
        return candidate

    def list_units(self, subject: str) -> tuple[str, ...]:
        return tuple(sorted({record.unit_id for record in self.manifest.records if record.subject == subject.lower()}))

    def list_files(self, subject: str, unit_id: str | None = None) -> tuple[str, ...]:
        return tuple(
            sorted(
                record.path
                for record in self.manifest.records
                if record.subject == subject.lower() and (unit_id is None or record.unit_id == unit_id)
            )
        )

    def read_file(self, path: str, start_line: int = 1, end_line: int | None = None) -> str:
        if start_line < 1:
            raise FileSystemError("start_line must be positive")
        resolved = self._resolve(path)
        lines = resolved.read_text(encoding="utf-8", errors="replace").splitlines()
        end = len(lines) if end_line is None else min(end_line, len(lines))
        if end < start_line:
            raise FileSystemError("end_line must not precede start_line")
        return "\n".join(lines[start_line - 1:end])

    def read_source(self, source_id: str, start_line: int = 1, end_line: int | None = None) -> str:
        return self.read_file(self._record(source_id).path, start_line, end_line)

    def search(self, subject: str, query: str, unit_id: str | None = None, top_k: int = 5) -> tuple[str, ...]:
        from .evidence import terms

        query_terms = terms(query)
        scored: list[tuple[int, str]] = []
        for record in self.manifest.records:
            if record.subject != subject.lower() or (unit_id is not None and record.unit_id != unit_id):
                continue
            record_terms = terms(f"{record.topic} {' '.join(record.headings)} {record.text}")
            overlap = len(query_terms & record_terms)
            if overlap:
                scored.append((overlap, record.path))
        return tuple(path for _, path in sorted(scored, key=lambda item: (-item[0], item[1]))[:top_k])

    def glob(self, pattern: str, subject: str | None = None) -> tuple[str, ...]:
        if ".." in pattern or Path(pattern).is_absolute():
            raise FileSystemError("glob must be relative to the notes directory")
        return tuple(
            sorted(
                record.path
                for record in self.manifest.records
                if (subject is None or record.subject == subject.lower()) and fnmatch.fnmatch(record.path, pattern)
            )
        )

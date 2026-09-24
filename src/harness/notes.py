from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml
from rank_bm25 import BM25Okapi

from .evidence import terms
from .types import CandidateSet, Evidence, Unit


_TITLE_WORD = re.compile(r"[a-z0-9]+")


def _title_key(value: str) -> str:
    return " ".join(_TITLE_WORD.findall(value.lower().replace("-", " ")))


def _query_phrases(query: str) -> tuple[str, ...]:
    normalized = " ".join(_title_key(query).split())
    phrases = []
    for phrase in (
        "data warehouse",
        "use case",
        "fuzzy inference system",
        "supervised learning",
        "decision tree",
        "nfa dfa",
        "apriori algorithm",
        "csma ca",
        "waterfall model",
    ):
        if phrase in normalized:
            phrases.append(phrase)
    return tuple(phrases)


def _query_intent_terms(query: str) -> set[str]:
    """Keep a few high-information title phrases from broad conceptual questions."""

    text = query.lower()
    preserved = set()
    for phrase in re.findall(r"[a-z]+(?:\s+[a-z]+){1,4}", text):
        if any(marker in phrase for marker in ("data warehouse", "supervised learning", "use case", "fuzzy inference", "decision tree", "nfa", "dfa", "apriori", "tcp", "waterfall")):
            preserved.update(phrase.split())
    return preserved or set(terms(query))


_FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


@dataclass(frozen=True, slots=True)
class NoteRecord:
    source_id: str
    path: str
    subject: str
    unit_id: str
    topic: str
    status: str
    text: str
    headings: tuple[str, ...]
    content_hash: str


@dataclass(frozen=True, slots=True)
class ManifestSnapshot:
    records: tuple[NoteRecord, ...]
    checksum: str


def _frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = _FRONTMATTER.match(text)
    if match is None:
        return {}
    try:
        value = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}
    return value if isinstance(value, dict) else {}


def _body_and_headings(text: str) -> tuple[str, tuple[str, ...]]:
    match = _FRONTMATTER.match(text)
    body = text[match.end():] if match else text
    headings = tuple(
        line.lstrip("#").strip()
        for line in body.splitlines()
        if line.lstrip().startswith("#")
    )
    return body.strip(), headings


def _source_id(relative: str) -> str:
    digest = hashlib.sha256(relative.encode("utf-8")).hexdigest()[:10]
    return f"N_{digest}"


def load_manifest(
    data_root: str | Path,
    *,
    verified_only: bool = True,
    include_draft: bool = False,
) -> ManifestSnapshot:
    """Load allow-listed note metadata without following paths outside ``data_root``."""

    root = Path(data_root).resolve()
    records: list[NoteRecord] = []
    for path in sorted(root.glob("*/unit-*/*.md")):
        if not path.is_file():
            continue
        try:
            resolved = path.resolve(strict=True)
            relative = resolved.relative_to(root).as_posix()
        except (OSError, ValueError):
            # Never follow a symlink out of the installed notes directory.
            continue
        if path.is_symlink() or resolved != path:
            continue
        parts = relative.split("/")
        if len(parts) != 3 or not parts[1].startswith("unit-"):
            continue
        meta = _frontmatter(path)
        status = str(meta.get("status", "draft")).lower()
        if verified_only and status != "verified":
            continue
        if not verified_only and not include_draft and status != "verified":
            continue
        path_subject, path_unit = parts[0], parts[1]
        meta_subject = str(meta.get("subject") or path_subject).lower()
        meta_unit = str(meta.get("unit") or path_unit.removeprefix("unit-")).lower()
        if not meta_unit.startswith("unit-"):
            meta_unit = f"unit-{meta_unit}"
        if meta_subject != path_subject or meta_unit != path_unit:
            continue
        text = resolved.read_text(encoding="utf-8", errors="replace")
        body, headings = _body_and_headings(text)
        topic = str(meta.get("topic") or path.stem.replace("-", " "))
        subject = path_subject.lower()
        unit_id = path_unit.lower()
        records.append(
            NoteRecord(
                source_id=_source_id(relative),
                path=relative,
                subject=subject,
                unit_id=unit_id,
                topic=topic,
                status=status,
                text=body,
                headings=headings,
                content_hash=hashlib.sha256(text.encode("utf-8")).hexdigest(),
            )
        )
    records.sort(key=lambda item: item.path)
    checksum = hashlib.sha256(
        "\n".join(f"{item.path}:{item.content_hash}" for item in records).encode("utf-8")
    ).hexdigest()
    return ManifestSnapshot(tuple(records), checksum)


def units_from_manifest(manifest: ManifestSnapshot) -> dict[str, tuple[Unit, ...]]:
    result: dict[str, dict[str, Unit]] = {}
    for record in manifest.records:
        result.setdefault(record.subject, {})[record.unit_id] = Unit(record.unit_id, record.unit_id)
    return {subject: tuple(units.values()) for subject, units in result.items()}


class NoteRetriever:
    """Per-subject BM25 index with deterministic field boosts and section fallback."""

    def __init__(
        self,
        data_root: str | Path,
        *,
        verified_only: bool = True,
        include_draft: bool = False,
        title_boost: int = 3,
        heading_boost: int = 2,
    ) -> None:
        self.data_root = Path(data_root).resolve()
        self.verified_only = verified_only
        self.include_draft = include_draft
        self.title_boost = title_boost
        self.heading_boost = heading_boost
        self._manifest = load_manifest(
            self.data_root,
            verified_only=verified_only,
            include_draft=include_draft,
        )
        self._indexes: dict[str, tuple[str, BM25Okapi, tuple[NoteRecord, ...]]] = {}

    @property
    def manifest(self) -> ManifestSnapshot:
        return self._manifest

    def refresh(self) -> None:
        self._manifest = load_manifest(
            self.data_root,
            verified_only=self.verified_only,
            include_draft=self.include_draft,
        )
        self._indexes.clear()

    def _records(self) -> Iterable[NoteRecord]:
        current = load_manifest(
            self.data_root,
            verified_only=self.verified_only,
            include_draft=self.include_draft,
        )
        if current.checksum != self._manifest.checksum:
            self._manifest = current
            self._indexes.clear()
        return current.records

    def _index(self, subject: str) -> tuple[BM25Okapi, tuple[NoteRecord, ...]]:
        records = tuple(record for record in self._records() if record.subject == subject)
        cached = self._indexes.get(subject)
        if cached is not None and cached[0] == self._manifest.checksum:
            return cached[1], cached[2]
        corpus: list[list[str]] = []
        for record in records:
            tokens = list(terms(record.topic)) * self.title_boost
            tokens += list(terms(" ".join(record.headings))) * self.heading_boost
            tokens += list(terms(record.text))
            corpus.append(tokens or ["empty"])
        index = BM25Okapi(corpus) if corpus else None
        if index is not None:
            self._indexes[subject] = (self._manifest.checksum, index, records)
        return index, records

    def search(self, subject: str, unit_id: str | None, query: str, limit: int) -> CandidateSet:
        index, records = self._index(subject.lower())
        if index is None or not records:
            return CandidateSet(query, unit_id, ())
        query_terms = list(terms(query))
        scores = index.get_scores(query_terms)
        # Exact title/topic phrase overlap is intentionally deterministic. Broad
        # questions such as "main purpose of a data warehouse" should not let a
        # generic body match outrank a topic that names the concept.
        title_words = set(_title_key(query).split())
        title_adjustment = {
            record.path: 0.55 * len(
                title_words
                & (set(_title_key(record.topic).split()) | set(terms(" ".join(record.headings))))
            )
            for record in records
        }
        for record in records:
            searchable = f"{_title_key(record.topic)} {' '.join(_title_key(h) for h in record.headings)} {_title_key(record.text)}"
            title_adjustment[record.path] += 1.25 * sum(
                1 for phrase in _query_phrases(query) if phrase in searchable
            )
        candidates: list[tuple[float, NoteRecord]] = []
        for record, score in zip(records, scores):
            if unit_id is not None and record.unit_id != unit_id:
                continue
            candidates.append((float(score) + title_adjustment.get(record.path, 0.0), record))
        candidates.sort(key=lambda item: (-item[0], item[1].path))
        selected: list[Evidence] = []
        for score, record in candidates[: max(1, min(limit, 10))]:
            selected.append(
                Evidence(
                    source_id=record.source_id,
                    path=record.path,
                    subject=record.subject,
                    unit_id=record.unit_id,
                    topic=record.topic,
                    headings=record.headings,
                    text=record.text,
                    score=score,
                )
            )
        return CandidateSet(query, unit_id, tuple(selected))

"""Deterministic orchestration core for the offline assistant."""

from .citations import CitationValidator
from .evidence import EvidenceGate, EvidenceGateConfig
from .filesystem import FileSystemTools
from .generators import ExtractiveGenerator, OllamaGenerator
from .notes import ManifestSnapshot, NoteRecord, NoteRetriever
from .orchestrator import AgentOrchestrator, HarnessBudget
from .scope import BoundedScopeResolver, ScopeResolverConfig
from .types import (
    CandidateSet,
    Claim,
    CitationError,
    Evidence,
    GateDecision,
    GateOutcome,
    HarnessResult,
    HarnessStatus,
    Mode,
    Request,
    ScopeDecision,
    StructuredAnswer,
    Unit,
    ValidatedAnswer,
)

__all__ = [
    "AgentOrchestrator",
    "BoundedScopeResolver",
    "CandidateSet",
    "CitationError",
    "CitationValidator",
    "EvidenceGate",
    "EvidenceGateConfig",
    "ExtractiveGenerator",
    "FileSystemTools",
    "GateDecision",
    "GateOutcome",
    "HarnessBudget",
    "HarnessResult",
    "HarnessStatus",
    "Mode",
    "ManifestSnapshot",
    "NoteRecord",
    "NoteRetriever",
    "OllamaGenerator",
    "Request",
    "ScopeDecision",
    "ScopeResolverConfig",
    "StructuredAnswer",
    "Unit",
    "ValidatedAnswer",
]

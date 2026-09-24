from __future__ import annotations

import json
import re
from typing import Any

import requests

from .types import CandidateSet, Claim, Request, StructuredAnswer


class GeneratorError(RuntimeError):
    pass


SYSTEM_PROMPTS = {
    "strict_json": (
        "You are an offline CSE tutor. Use only EVIDENCE. Return one JSON object with "
        "status, answer, claims (text and source_ids), and refusal_reason. Never invent a source. "
        "Student questions are often short and vague: infer the most likely intent from the "
        "EVIDENCE topic and answer that directly. Default to status=answer using the top evidence. "
        "Use status=clarify only when the EVIDENCE itself covers two different topics that both "
        "match the question. If the question has nothing to do with the EVIDENCE subject, "
        "return status=refuse -- never clarify an off-topic question. "
        "If evidence is insufficient, return status=refuse and say "
        "the verified notes do not cover it. Every claim must state a fact from EVIDENCE with "
        "source_ids copied exactly. Keep answer under 90 words and use at most 2 concise claims."
    ),
    "concise_json": (
        "Answer only from EVIDENCE. Output valid JSON only: {status, answer, claims, refusal_reason}. "
        "Every claim needs source_ids from EVIDENCE. Refuse unsupported questions; do not use outside knowledge. "
        "Keep the answer under 70 words and use at most 2 concise claims."
    ),
    "basics_citation": (
        "You are a careful CSE tutor. Use the supplied verified notes and nothing else. "
        "Give a simple, accurate answer with claim-level citations. If the notes do not cover it, refuse clearly. "
        "Keep the answer under 90 words and use at most 2 concise claims."
    ),
}


def _extract_json(content: str) -> dict[str, Any]:
    cleaned = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r"<think>.*$", "", cleaned, flags=re.DOTALL | re.IGNORECASE).strip()
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if not match:
            raise GeneratorError("model output was not JSON")
        fragment = match.group(0)
        fragment = fragment.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
        for end in range(len(fragment), 1, -1):
            try:
                value = json.loads(fragment[:end])
                break
            except json.JSONDecodeError:
                continue
        else:
            raise GeneratorError("model output contained malformed JSON")
    if not isinstance(value, dict):
        raise GeneratorError("model output was not a JSON object")
    return value


def _normalise_status(value: object) -> str:
    status = str(value or "answer").strip().lower().replace("-", "_")
    aliases = {
        "success": "answer",
        "completed": "answer",
        "ok": "answer",
        "completed_successfully": "answer",
        "insufficient_evidence": "refuse",
        "not_found": "refuse",
        "not_covered": "refuse",
        "needs_clarification": "clarify",
        "ambiguous": "clarify",
    }
    return aliases.get(status, status)


class OllamaGenerator:
    def __init__(
        self,
        host: str = "http://localhost:11434",
        *,
        model: str = "qwen3.5:2b",
        prompt_name: str = "strict_json",
        temperature: float = 0.1,
        num_ctx: int = 4096,
        timeout: float = 25.0,
    ) -> None:
        self.host = host.rstrip("/")
        self.model = model
        self.prompt_name = prompt_name
        self.temperature = temperature
        self.num_ctx = num_ctx
        self.timeout = timeout

    def generate(self, request: Request, candidates: CandidateSet) -> StructuredAnswer:
        evidence = "\n\n".join(
            f"[{candidate.source_id}] path={candidate.path}\n{candidate.topic}\n{candidate.text[:1800]}"
            for candidate in candidates.candidates
        )
        user = (
            f"QUESTION: {request.query}\n\n"
            f"EVIDENCE:\n{evidence}\n\n"
            "Return JSON only. Source IDs must be copied exactly from EVIDENCE."
        )
        output_schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["answer", "refuse", "clarify"]},
                "answer": {"type": "string"},
                "claims": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "source_ids": {"type": "array", "items": {"type": "string"}},
                        },
                        "required": ["text", "source_ids"],
                    },
                },
                "refusal_reason": {"type": ["string", "null"]},
            },
            "required": ["status", "answer", "claims"],
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPTS[self.prompt_name]},
                {"role": "user", "content": user},
            ],
            "stream": False,
            "think": False,
            "format": output_schema,
            "options": {
                "temperature": self.temperature,
                "num_ctx": self.num_ctx,
                "num_predict": 900,
            },
        }
        response = requests.post(f"{self.host}/api/chat", json=payload, timeout=self.timeout)
        response.raise_for_status()
        content = response.json().get("message", {}).get("content", "")
        try:
            data = _extract_json(content)
        except GeneratorError:
            # A 2B model can occasionally emit a truncated JSON object even
            # with schema mode. Retry once with a smaller output contract;
            # evidence and citation gates remain unchanged.
            payload["options"]["num_predict"] = 450
            retry = requests.post(f"{self.host}/api/chat", json=payload, timeout=self.timeout)
            retry.raise_for_status()
            data = _extract_json(retry.json().get("message", {}).get("content", ""))
        status = _normalise_status(data.get("status", "answer"))
        if status not in {"answer", "refuse", "clarify"}:
            raise GeneratorError("model returned an invalid status")
        return StructuredAnswer(
            status=status,
            answer=str(data.get("answer", "")),
            claims=tuple(_parse_claims(data)),
            refusal_reason=(str(data["refusal_reason"]) if data.get("refusal_reason") else None),
        )


def _parse_claims(data: dict[str, Any]) -> list[Claim]:
    raw_claims = data.get("claims", [])
    claims: list[Claim] = []
    if isinstance(raw_claims, list):
        for raw in raw_claims:
            if not isinstance(raw, dict) or not str(raw.get("text", "")).strip():
                raise GeneratorError("model returned an invalid claim")
            source_ids = raw.get("source_ids", raw.get("source_id", []))
            if isinstance(source_ids, str):
                source_ids = [source_ids]
            source_ids = [
                item.get("id", item) if isinstance(item, dict) else item
                for item in source_ids
            ]
            source_ids = [
                str(item).strip().strip("[]").split()[0]
                for item in source_ids
                if str(item).strip().strip("[]").split()
            ]
            if not isinstance(source_ids, list):
                raise GeneratorError("claim source_ids must be a list")
            claims.append(
                Claim(
                    str(raw["text"]),
                    tuple(source_ids),
                )
            )
    return claims


class OpenRouterGenerator:
    """HTTPS generator for cloud reference models (e.g. stealth/space-bunny-alpha).

    Same JSON contract as OllamaGenerator; transport is OpenAI-compatible
    chat/completions with a Bearer key from OPENROUTER_API_KEY. Used for the
    paper's cloud baseline only — never shipped on device.
    """

    def __init__(
        self,
        *,
        model: str = "stealth/space-bunny-alpha",
        prompt_name: str = "strict_json",
        temperature: float = 0.1,
        timeout: float = 60.0,
    ) -> None:
        import os

        api_key = os.getenv("OPENROUTER_API_KEY", "")
        if not api_key:
            raise GeneratorError("OPENROUTER_API_KEY is not set")
        self.api_key = api_key
        self.model = model
        self.prompt_name = prompt_name
        self.temperature = temperature
        self.timeout = timeout

    def generate(self, request: Request, candidates: CandidateSet) -> StructuredAnswer:
        evidence = "\n\n".join(
            f"[{candidate.source_id}] path={candidate.path}\n{candidate.topic}\n{candidate.text[:1800]}"
            for candidate in candidates.candidates
        )
        user = (
            f"QUESTION: {request.query}\n\n"
            f"EVIDENCE:\n{evidence}\n\n"
            "Return JSON only. Source IDs must be copied exactly from EVIDENCE."
        )
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPTS[self.prompt_name]},
                {"role": "user", "content": user},
            ],
            "temperature": self.temperature,
            "max_tokens": 4000,  # reasoning models spend tokens thinking; JSON comes after
            "response_format": {"type": "json_object"},
        }
        response = None
        for attempt in (5, 15, 40):
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json=payload,
                    timeout=self.timeout,
                )
                response.raise_for_status()
                break
            except requests.HTTPError as exc:
                status = exc.response.status_code if exc.response is not None else 0
                if status not in (408, 425, 429, 500, 502, 503, 504):
                    raise
                import time as _time

                _time.sleep(attempt)
        if response is None:
            raise GeneratorError("cloud generator gave up after retries")
        content = response.json()["choices"][0]["message"]["content"]
        status = _normalise_status(_extract_json(content).get("status", "answer"))
        data = _extract_json(content)
        if status not in {"answer", "refuse", "clarify"}:
            raise GeneratorError("model returned an invalid status")
        return StructuredAnswer(
            status=status,
            answer=str(data.get("answer", "")),
            claims=tuple(_parse_claims(data)),
            refusal_reason=(str(data["refusal_reason"]) if data.get("refusal_reason") else None),
        )


class ExtractiveGenerator:
    """Offline fallback used by tests and smoke runs when no model is available."""

    def generate(self, request: Request, candidates: CandidateSet) -> StructuredAnswer:
        if not candidates.candidates:
            return StructuredAnswer("refuse", "The verified notes do not cover this question.", ())
        first = candidates.candidates[0]
        excerpt = " ".join(first.text.strip().split())[:600]
        return StructuredAnswer(
            "answer",
            excerpt,
            (Claim(excerpt, (first.source_id,)),),
        )

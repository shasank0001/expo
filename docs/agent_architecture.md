# CSE Offline Assistant — Agent/RAG Architecture Proposal

**Status:** greenfield recommendation  
**Scope:** desktop v1; current implementation intentionally ignored  
**Design goal:** answer only from verified local notes, with a correct-file rank-1 target, honest abstention, and real source paths.

## 1. Recommendation in one sentence

Use a **deterministic, hierarchical RAG workflow** in which Python owns scope, retrieval, evidence gates, citation validation, and termination; the local LLM is used only for bounded unit classification and answer synthesis.

This is an agent in the product sense, but not an unconstrained ReAct loop. The model must not browse the filesystem, choose arbitrary tools, change the subject, or decide that unsupported evidence is sufficient.

## 2. Why this shape fits the project

The brief gives us unusually strong constraints:

- notes are already grouped by subject, unit, and topic;
- the subject comes from a trusted UI picker;
- the required release gate is correct-file rank 1, not top-3 recall;
- out-of-syllabus questions must produce an honest refusal;
- every factual claim must cite a real file;
- the shipped model is below 3B parameters and runs through bundled llama.cpp;
- the team is small and has two semesters.

These favor a small finite workflow over a general-purpose agent framework. The workflow is easier to test, debug, explain, and package. It also makes the paper comparison cleaner: we can measure retrieval, evidence gating, generation, and citation validation independently.

## 3. High-level design

```text
Tauri desktop shell
        │ localhost JSON request
        ▼
FastAPI sidecar
        │
        ▼
AgentOrchestrator (deterministic state machine)
   │
   ├── RequestValidator
   ├── ScopeResolver
   │      ├── trusted subject
   │      ├── optional user unit
   │      └── bounded unit classifier when unit is absent
   │
   ├── RetrievalService
   │      ├── verified-note manifest
   │      ├── subject BM25 index
   │      ├── optional unit soft filter
   │      └── section evidence selection
   │
   ├── EvidenceGate
   │      ├── score threshold
   │      ├── top-1 margin
   │      └── query-term coverage
   │
   ├── AnswerGenerator
   │      ├── Ollama adapter (development)
   │      └── llama.cpp/GGUF adapter (production)
   │
   ├── CitationValidator
   └── TurnLogger
```

The UI receives an answer, source cards, latency, and a safe status. It never receives or reads note files directly.

## 4. Agent control flow

### State 1: Validate the request

Reject or normalize invalid subject, unit, query, model, and `top_k` values before any model call. Resolve every path to an allow-listed path under the installed verified-notes directory. Never accept a path or source ID from the browser.

### State 2: Resolve scope

1. The subject is always taken from the UI picker.
2. If the student selected a unit, use it as a strong scope signal.
3. If the unit is absent, give a small model a fixed list of that subject's unit IDs/titles and require structured output such as `{"unit": "unit-2", "confidence": 0.82}`.
4. Treat the classifier as a **soft signal** unless a local evaluation shows a very high precision. If confidence is low, ambiguous, or the query spans units, search the whole subject.
5. On a failed or weak unit-scoped search, perform exactly one widen-to-subject retry, as required by the brief.

This avoids a common failure mode where an incorrect unit decision makes the correct topic unreachable. A later version may add a conversation resolver for follow-up questions, but the first release should keep the query self-contained.

### Mode semantics and escalation

Keep the public `mode` field small and predictable:

- `direct`: the user supplied a unit; skip unit classification and search that unit first;
- `agent`: the user did not supply a unit; run the bounded unit classifier, then search the selected unit and allow one subject-wide fallback;
- `auto`: reserve for a later release; in v1 it should resolve to `direct` when a unit is present and `agent` otherwise.

Do not implement auto-escalation as “call a larger model and trust its decision.” The only v1 escalation is deterministic: weak scoped retrieval → search the trusted subject → evaluate the gate again. This keeps the latency, behavior, and paper comparison understandable.

### State 3: Retrieve candidates

The first release should use a fielded BM25 index over verified topic documents:

```text
topic_score = w_title * BM25(title/topic)
            + w_heading * BM25(headings)
            + w_body * BM25(body)
```

Use one in-memory index per subject, rebuilt only when the manifest checksum changes. Store the source path, subject, unit, topic, headings, and content hash in the index metadata. Keep title/topic matching stronger than body matching, but tune the weights on the gold set.

Retrieval should return more than one candidate internally (for example, top 5) while answering from the best-supported evidence. `top_k` exposed by the API is a maximum, not permission for the model to select any of the returned files.

After selecting the best topic file, split its Markdown by headings and retrieve the best sections. This reduces prompt size and makes citations point to a precise passage. The citation shown to the student can remain the full topic file path, with the matched heading stored in metadata.

### State 4: Gate the evidence

Do not call the generator if the evidence is weak. The gate should use multiple signals:

- calibrated top-1 BM25 score;
- margin between rank 1 and rank 2;
- coverage of important query terms, preserving technical terms and formulas;
- whether the selected document/section is in the trusted subject/unit scope;
- optionally, a small local entailment check only if eval shows it is useful.

The thresholds must be learned from held-out answerable and out-of-syllabus questions. Do not copy a threshold from a paper or use the LLM's self-reported confidence as the gate.

Possible outcomes are `ANSWER`, `REFUSE`, and `CLARIFY`. A refusal should say that the verified notes do not cover the question, not that the model lacks general knowledge.

### State 5: Generate a structured answer

The model receives only:

- the normalized question;
- a short system instruction;
- a bounded evidence block with stable source IDs such as `S1`, `S2`;
- the required output schema.

Prefer JSON or a strictly validated line format:

```json
{
  "status": "answer",
  "answer": "Simple-English answer...",
  "claims": [
    {"text": "A factual claim.", "source_ids": ["S1"]}
  ],
  "refusal_reason": null
}
```

The model must not invent paths. The UI should display source titles and paths supplied by the backend, not source text copied from the model's output.

### State 6: Validate citations and return

`CitationValidator` should enforce:

1. every source ID exists in the current retrieval result;
2. every source ID maps to an allow-listed verified note;
3. every factual claim has at least one source ID;
4. cited sections contain the claim, using a deterministic overlap/entailment check first;
5. the answer does not claim that unsupported material is covered.

If validation fails, do not silently return a half-valid answer. Return a safe refusal or a clearly marked “I found a related note but cannot provide a fully verified answer.” This can be handled without a second model call to keep latency predictable.

### State 7: Log the decision trace

Record request metadata, selected scope, every candidate path and score, gate signals, fallback count, model/runtime/quantization, generator status, citation-validation result, and retrieval/generation timings. Do not log private unrelated data; this is a study assistant, but logs still need a clear retention policy.

## 5. Retrieval evolution

### v1: BM25 + section evidence

Recommended first because the corpus is syllabus-bounded, the technical vocabulary is strong, and the project explicitly makes BM25 the starting point. It is easy to explain in the paper and has no embedding-model deployment cost.

### v2 trigger: hybrid retrieval

Add a small local embedding model only if the miss log shows terminology/paraphrase failures that BM25 cannot solve. Keep two candidate lists:

```text
RRF(d) = 1 / (k + rank_bm25(d)) + 1 / (k + rank_dense(d))
```

Use rank fusion rather than adding raw scores with arbitrary weights. Preserve lexical matches as a required candidate source, because dense retrieval can rank a semantically related but wrong CSE topic highly. Measure rank-1 precision before enabling hybrid mode in production.

Do not start with a vector database, cross-encoder, or multi-agent debate. They add deployment, latency, and evaluation complexity before we know which failure dominates.

## 6. Model strategy

Keep the model behind an adapter so development and production can use different runtimes:

```text
Generator interface -> Ollama adapter (dev)
                   -> llama.cpp GGUF adapter (ship)
```

Candidate baseline matrix:

| Candidate | Role | Reason |
|---|---|---|
| Qwen3-1.7B instruction, non-thinking mode | primary quality baseline | 1.7B is still within the <3B constraint and has enough capacity for instruction following |
| Gemma 3 1B instruction | memory/latency fallback | smaller footprint and an explicit low-resource deployment target |
| A 1B–1.5B family selected from local eval | optional alternative | compare on this project's retrieval and citation gates, not generic leaderboards |

Pin a model manifest with model revision, GGUF filename, quantization, context length, prompt template, runtime version, and license. Start with Q4_K_M as a practical llama.cpp baseline, then measure memory and latency on the target laptop. The final choice remains open until the gold eval exists.

Do not fine-tune immediately. First measure whether failures come from retrieval, evidence gating, prompt/format compliance, or factual generation. Fine-tune only if the same error class repeats and a held-out eval shows a clear gain. Compare LoRA and QLoRA only after that evidence exists; the available 8GB GPU makes QLoRA a fallback, not the default plan.

## 7. Suggested interfaces

The exact names can change, but keep these boundaries stable:

```text
RequestValidator.validate(request) -> ValidatedRequest
ScopeResolver.resolve(validated) -> ScopeDecision
RetrievalService.search(scope, query) -> CandidateSet
EvidenceGate.evaluate(candidates, query) -> GateDecision
AnswerGenerator.generate(question, evidence) -> StructuredAnswer
CitationValidator.validate(answer, candidates) -> ValidatedAnswer
TurnLogger.log(trace) -> None
```

The orchestrator owns transitions and timeout/error handling. Adapters do not own business rules. This keeps model/runtime changes from changing retrieval or citation guarantees.

## 8. Evaluation design

Build the gold set before tuning the agent. Include, per subject:

- exact syllabus questions with one expected topic file;
- paraphrased questions using different wording;
- acronym/formula questions;
- questions spanning two topics or units;
- out-of-syllabus questions that must be refused;
- deliberately ambiguous questions where clarification is preferable.

For each item, store the expected subject/unit, rank-1 file, relevant headings, reference answer or answer facts, and expected refusal behavior. Keep a held-out split for threshold calibration and a final untouched release split.

Track these metrics separately:

- **Retrieval:** hit@1, MRR, recall@3/5 for diagnosis, unit-classification precision, and fallback rate.
- **Abstention:** refusal precision/recall, false-answer rate on out-of-syllabus questions, and coverage of answerable questions.
- **Grounding:** citation precision, citation recall, claim-level support, and invalid-path rate.
- **System:** retrieval ms, generation ms, p50/p95 latency, peak RAM, and model size.

Set numerical release thresholds after a small pilot, but keep these invariants from day one: 100% returned paths are real verified-note paths, no unsupported source ID can pass validation, and every answer/refusal decision is logged.

RAG-style faithfulness and answer-relevance metrics can be secondary diagnostics. Faculty-reviewed correctness and citation coverage should be the primary gate for this academic assistant.

## 9. Rollout plan

### Phase 0 — contracts and gold data

Define the note manifest, request/response schema, source IDs, refusal language, and gold question format. Build a small representative gold set before optimizing retrieval.

### Phase 1 — deterministic retrieval

Implement the manifest, verified-only loading, per-subject BM25 cache, fielded scoring, section selection, and trace logging. Test it with a fake generator so retrieval quality is isolated.

### Phase 2 — bounded model calls

Add the unit classifier and answer generator adapters. Validate structured output in code. Measure model size, memory, and latency on the target hardware.

### Phase 3 — gates and citation safety

Calibrate score/margin/coverage thresholds on held-out data. Add citation validation, safe refusal, one widen-to-subject retry, and UI source cards.

### Phase 4 — desktop packaging

Package the FastAPI sidecar, llama.cpp binary, GGUF model manifest, and verified notes with Tauri. Keep Ollama and development fixtures out of the production installer.

### Phase 5 — evidence-driven upgrades

Add hybrid retrieval only if miss logs justify it. Consider LoRA/QLoRA only if generation—not retrieval or formatting—is the limiting factor. Keep every upgrade behind an eval comparison.

## 10. Approaches I would not choose for v1

- **Unconstrained ReAct/tool-calling agent:** too much nondeterminism for a strict academic citation bar.
- **LLM-generated subject or file selection:** the UI and manifest already provide stronger constraints.
- **Semantic-only vector search:** unnecessary deployment cost and weaker exact-term behavior as a sole retriever.
- **Fine-tuning before evaluation:** it can improve style while leaving retrieval and citation errors untouched.
- **Cloud fallback:** violates the offline/no-cloud-at-answer-time product promise.
- **Auto-escalation based only on model confidence:** confidence is not calibrated and is not a substitute for retrieval evidence.

## 11. Research basis

The detailed research notes and source links are in:

- `research_agent_architecture/findings_retrieval.md`
- `research_agent_architecture/findings_runtime.md`
- `research_agent_architecture/findings_agent_eval.md`

The most relevant sources are the RAGAS evaluation paper (faithfulness/context relevance), ALCE (citation precision/recall), llama.cpp quantization documentation, and the official Gemma 3 and Qwen3 model cards. Numerical thresholds in this proposal are intentionally left for local evaluation rather than imported from another domain.

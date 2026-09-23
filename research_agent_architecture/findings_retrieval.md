# Findings: retrieval and hierarchy design

## Evidence

- The project corpus is small, structured, and syllabus-bounded. The brief specifies one Markdown file per topic, with subject/unit/topic metadata and full notes, and requires correct-file rank 1 rather than merely top-3 recall.
- BM25 is a sensible zero/low-dependency baseline for this corpus because syllabus questions contain high-value technical terms, formulas, acronyms, and exact topic names. A semantic-only index can improve paraphrase recall but adds an embedding model, index lifecycle, and a second failure mode.
- Hybrid retrieval is commonly implemented by combining sparse BM25 and dense rankings. Reciprocal Rank Fusion (RRF) combines ranks rather than raw scores, which is useful when score scales are not calibrated: `RRF(d) = sum_r 1/(k + rank_r(d))`.
- A 2025 evaluation of hybrid retrieval found that fusion can improve recall but can reduce early precision if the dense retriever promotes semantically related but non-relevant documents. A learned/neural reranker improved ranking, but reported latency was prohibitive for a small on-device app.
- Evidence-calibrated RAG work separates retrieval coverage from evidence sufficiency. A top-1 lexical score can be used as a confidence signal, but the answer/no-answer threshold must be calibrated on held-out labeled questions.
- In a claim-aware scientific RAG study, gating on top-1 BM25 score reduced answered questions with no relevant document in the top 10 from 0.193 to 0.047 at a 28.3% answer coverage operating point. This supports explicit abstention, but the numeric operating point is not transferable without local evaluation.

## Implication for this project

Start with a deterministic hierarchical BM25 retriever over topic-level documents, not a free-form agent that invents a plan. Add section-level passage retrieval only after a rank-1 miss is observed: each topic document can be chunked by headings and scored as `(topic, section)` evidence. Keep a single retrieval score and a calibrated gate. If paraphrase questions or terminology mismatches dominate the miss log, add a small local embedding retriever behind the same interface and fuse with BM25 using RRF; preserve BM25 as a required candidate source for technical terms.

## Sources

- Project brief: `/home/shasank/shasank/Deep_learing/projects/final-year-project/project.md`
- RAGAS paper: https://arxiv.org/abs/2309.15217
- Hybrid retrieval for hallucination mitigation: https://arxiv.org/html/2504.05324v1
- Claim-aware scientific RAG: https://doi.org/10.69987/jacs.2023.30102
- LiveRAG 2025 hybrid retrieval evaluation: https://arxiv.org/html/2506.22644

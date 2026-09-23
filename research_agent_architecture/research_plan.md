# Research plan: offline CSE study assistant architecture

## Main question
Which agent/RAG architecture best fits the project brief: offline-only, faculty-verified Markdown, strict rank-1 retrieval, honest abstention, source-grounded citations, ~2B local model, Tauri + FastAPI + llama.cpp, and a small student team?

## Subtopics
1. **Retrieval and hierarchy design** — compare BM25-first, hybrid lexical+semantic, and hierarchical multi-step retrieval for this corpus; identify safeguards for rank-1 and out-of-syllabus questions.
2. **Offline small-model runtime** — compare llama.cpp/GGUF execution, quantization, model-family options under 3B, and practical CPU/RAM constraints.
3. **Agent control flow and evaluation** — research constrained agent state machines, citation grounding/validation, abstention, and metrics for measuring retrieval and answer quality.

## Synthesis method
Combine findings into a recommended v1 architecture, explicitly separate committed components from optional v2 upgrades, and map each recommendation to the project's locked constraints and open decisions. Record source URLs and caveats in the findings files.

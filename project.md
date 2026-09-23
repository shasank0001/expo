# CSE Offline Assistant — Project Description

## 1. What it is
An offline-first study assistant for CSE undergraduates (Gayatri Vidya Parishad, autonomous).
English only, basics-first. It answers syllabus questions using only faculty-verified
notes stored on the device — no internet, no cloud API at answer time.

Targets: student laptops (16GB RAM, good CPU) via a desktop app first, Android phones later.
Model plan: ~2B for ship; a bigger model first as reference, then fine-tune the small one only if eval demands it.
Constraint: small models only (<3B parameters) so it fits on device.
Compute available: one RTX 5060 8GB (QLoRA fine-tuning only) + small cloud budget.
Team: small student team. Timeline: two semesters. A paper is a required deliverable.

## 2. How it works
Fresh build, no legacy code. Three parts:

```
Tauri window (web UI) → localhost → FastAPI sidecar → llama.cpp (bundled) + BM25 over notes
                                              (dev only: Ollama)
```

1. **App shell (Tauri)**: native desktop window with a web UI — subject picker,
   optional unit dropdown, question box, answer + sources + latency. The shell starts and
   stops the backend on launch/quit. The UI never reads notes or calls the model directly.
2. **Backend (fresh Python + FastAPI sidecar)**: receives `{subject, unit?, model, query, top_k, mode}`.
   - `retriever.py`: keyword search (BM25) narrowed to subject, then to unit when known.
     Title/topic matches count more than body matches. One index per subject is built once
     and reused; rebuilt only when a note file changes. If the top score is too low,
     nothing is sent to the model — it must say the notes don't cover it.
   - `llm.py`: sends question + retrieved files to the local model with a short
     instruction: answer in simple English, cite the files, or say the notes don't cover it.
     Dev runtime is Ollama (fast iteration); prod runtime is bundled llama.cpp (GGUF, CPU-optimized).
   - `agent.py`: hierarchy mode — subject comes from the UI picker (trusted); the agent
     lists the subject's units and picks one (skipped if the student already chose a unit),
     BM25 searches inside that unit, with one retry / widen-to-subject fallback.
   - Every turn is logged to `logs/` with retrieved paths + scores and split timings
     (retrieval ms vs generation ms) for later analysis.
3. **Data** (`data/`): one Markdown file per topic at `data/<subject>/unit-<n>/<slug>.md`,
   with frontmatter (subject, unit, topic, syllabus ref, verification status) and FULL notes —
   every syllabus point for the topic covered in order, worked examples, key terms/formulas,
   common mistakes, exam prep. Length follows importance: major topics get long files,
   minor topics complete but shorter. No word cap. Currently `draft` — peer review next.
4. **Eval** (`eval/`): faculty-written question sets per subject plus scoring
   (right file found, honest "not in notes", correct citations, latency).
   To be built in semester 1, before any training.

## 3. Locked decisions (fixed Sep-2026)
- **Subjects (v1)**: all 3rd-year core theory — DWDM (CSM3101), OOSE (CSM3102),
  Computer Networks (CSM3103), Machine Learning (CSM3201), Soft Computing (CSM3202),
  Automata + Compiler Design (CSM3203). Electives excluded for now.
- **Verification**: peer review — one member drafts, another reviews; faculty spot-checks only.
- **Eval bar (strict)**: correct file at rank 1, honest "not in notes" on out-of-syllabus,
  every factual claim cited to a real path. Top-3 is not enough.
- **Build order**: data + eval set first, backend hardening after.
- **Agent flow**: subject from UI picker; unit from optional dropdown or agent pick (one retry, then widen).
- **Retrieval cache**: one in-memory BM25 index per subject, rebuilt only on file change.
- **Packaging (v1)**: proper desktop app — Tauri native shell, FastAPI sidecar bundled
  alongside it, llama.cpp binary + GGUF model bundled in the installer (USB) or fetched
  on first run. Notes ship in the app data folder, verified-only. No Streamlit, no Ollama
  in the final product.
- **Runtime rule**: Ollama is dev-only (iteration, model swapping, eval). Prod is always
  bundled llama.cpp — one GGUF export step between them.
- **Hardware assumed**: 16GB RAM, good CPU; quantized ~2B model (~1.5–2GB).
- **Model strategy**: strong bigger model as reference + zero-tuned 2B baseline first;
  fine-tune the 2B only if it misses the bar (compare LoRA vs QLoRA, not QLoRA by default).
- **Synonym dictionary**: deferred to v2, seeded from real v1 miss logs.

## 4. What is not fixed yet (open decisions)
- **Model choice**: final <3B base model not selected; 8B models are reference only (too big for phones).
- **Retrieval**: BM25 keyword search is the starting point. Whether v1 needs embeddings
  or a tiny on-device vector index is undecided and depends on eval results.
- **Training**: whether QLoRA is needed at all, and on what data (style vs knowledge),
  depends on what the eval shows. No training config fixed.
- **Backend gaps**: citation validator (reject paths not in the file tree) and
  auto-escalation (direct → agent mode on weak scores) are planned, not built.
- **Mobile stack**: Android deferred to v2; v1 is the desktop app above.
- **Paper claim**: exact comparison (RAG vs fine-tune vs hybrid) will be fixed only
  after semester-1 eval numbers exist.

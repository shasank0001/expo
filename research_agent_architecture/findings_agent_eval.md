# Findings: agent control flow and evaluation

## Evidence

- The project's hard requirements are deterministic scope, one retry/widen fallback, real-path citation validation, and honest refusal. These are better expressed as a finite workflow than as an unconstrained ReAct loop.
- Recent deterministic-agent work argues for separating an expert-defined execution blueprint from bounded model calls: the model handles parsing/summarization while code controls branching, constraints, and termination. This directly matches the brief's trusted subject picker and fixed hierarchy.
- The project's eval must distinguish retrieval quality from generation quality. Useful metrics are correct-file hit@1, MRR, recall@k for diagnosis, refusal precision/recall, citation recall, citation precision, claim-level groundedness, and latency split into retrieval and generation.
- ALCE defines citation recall as whether the output is supported by cited passages and citation precision as whether citations are relevant. It reports substantial room for improvement: even strong systems can lack complete citation support.
- RAGAS separates faithfulness (claims supported by context), answer relevance, and context relevance. These are useful secondary diagnostics, but faculty-reviewed gold questions should remain the primary release gate.

## Implication for this project

Implement a small state machine: `validate_request -> resolve_scope -> retrieve -> evidence_gate -> answer_or_refuse -> validate_citations -> log`. The LLM may classify the unit or extract answer claims, but it may not choose arbitrary files, call unapproved tools, or override the evidence gate. Emit structured output (answer, claim list, source IDs, confidence/reason) and validate every source ID against the retrieved set before returning. Log the full decision trace for threshold tuning.

## Sources

- Project brief: `/home/shasank/shasank/Deep_learing/projects/final-year-project/project.md`
- Blueprint First, Model Second: https://arxiv.org/html/2508.02721
- ALCE citation evaluation: https://aclanthology.org/anthology-files/anthology-files/pdf/emnlp/2023.emnlp-main.398.pdf
- RAGAS evaluation: https://arxiv.org/abs/2309.15217

# Findings: offline small-model runtime

## Evidence

- The project requires a bundled llama.cpp/GGUF runtime, ~2B model, quantized local inference, and no cloud API at answer time. Ollama is explicitly development-only.
- llama.cpp documents `Q4_K_M` as a practical balance for quantized local models. Its quantizer documentation gives a Q4_K_M output of approximately 0.7 GB for a 1B model; actual runtime memory also includes KV cache, buffers, runtime, and the app.
- The official Gemma 3 model card lists a 1B instruction-tuned model with a 32K context window and low-resource deployment as an intended use case. The official Qwen3 model card lists Qwen3-1.7B as a 1.7B instruction/reasoning model with 32K context and thinking/non-thinking modes.
- Model choice should be measured on this project's eval, not inferred from general benchmark rankings. A 1B model may be faster and smaller, while a 1.5B–1.7B model may better preserve instructions and citation formatting.

## Implication for this project

Make the model adapter runtime-neutral: development can call Ollama, production calls a bundled llama.cpp server/binary with a GGUF file. Pin a model manifest containing model family, revision, quantization, context length, prompt template, and license. Start with an instruction-tuned 1.5B–1.7B candidate and a 1B fallback only if local eval shows acceptable rank-1 retrieval and citation compliance. Keep context deliberately small: retrieve only the best topic/section evidence rather than filling a long context window.

## Sources

- Project brief: `/home/shasank/shasank/Deep_learing/projects/final-year-project/project.md`
- llama.cpp quantization documentation: https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/README.md
- llama.cpp quantization guide: https://ggml-org-llama-cpp.mintlify.app/models/quantizing-models
- Gemma 3 model card: https://ai.google.dev/gemma/docs/core/model_card_3
- Qwen3-1.7B model card: https://huggingface.co/Qwen/Qwen3-1.7B

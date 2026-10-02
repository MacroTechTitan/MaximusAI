# TRAINING.md — <model name>

| Field | Value |
|---|---|
| Base model + revision | |
| Toolchain + versions | Unsloth x.y / MLX-LM x.y, llama.cpp build |
| Hardware | |
| Dataset | n train / n valid / n test; sha256 of each split |
| Format | chat JSONL, template: <name> |
| Method | QLoRA r=, alpha=, lr=, epochs/iters=, max_seq_len= |
| Export | GGUF f16 → Q4_K_M via llama-quantize |
| Ollama tag | |

## Eval (held-out test split, same prompt, temperature 0)

| Build | Score | Notes |
|---|---|---|
| Base, Ollama Q4_K_M | | |
| Adapter, fp16 | | |
| Fused, Ollama Q4_K_M (shipped) | | |

## Decision

Ship / don't ship, and why. Re-train trigger: <data drift, base model update>.

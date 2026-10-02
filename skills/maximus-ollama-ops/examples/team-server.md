# Worked example — two users, one 24 GB GPU

Illustrative arithmetic, not a benchmark. Re-derive it for your model.

**Goal.** Two people run a research assistant at the same time on an RTX-class
24 GB card, each with up to 32K tokens of context.

| Term | Value | Basis |
|---|---|---|
| Weights, 8B at Q4_K_M | ≈ 5 GB | `params × 0.625` rule in `maximus-slm-local-stack` |
| KV per slot, 32K, f16 | ≈ 4.5 GB | 0.75 MB × ~36 layers × 32 (per the sibling skill's formula; layer count varies by model) |
| KV per slot, 32K, q8_0 | ≈ 2.3 GB | about ½ of f16 (Ollama FAQ) |
| Slots (`OLLAMA_NUM_PARALLEL`) | 2 | |
| Overhead | ≈ 1 GB | |
| **Total at f16 KV** | ≈ 15 GB | fits |
| **Total at q8_0 KV** | ≈ 10.6 GB | fits, leaves room for an embedding model |

Config chosen: `OLLAMA_NUM_PARALLEL=2`, `OLLAMA_CONTEXT_LENGTH=32768`,
`OLLAMA_FLASH_ATTENTION=1`, `OLLAMA_KV_CACHE_TYPE=q8_0`,
`OLLAMA_MAX_LOADED_MODELS=2` (the chat model plus the embedding model),
`OLLAMA_KEEP_ALIVE=1h`.

Verification: `ollama ps` shows `100% GPU` and CONTEXT 32768 for the chat
model. Two concurrent 30K-token requests complete without a 503 or a CPU split.
Check these on your own box. The numbers here are arithmetic, not a
measurement.

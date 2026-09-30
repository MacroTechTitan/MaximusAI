# Ollama operations facts — pulled 2026-09-30

**This file expires.** Re-verify against docs.ollama.com if it is more than
about two months past 2026-09-30.

## Context

- FAQ: "By default, Ollama uses a context window size of 4096 tokens",
  overridable with `OLLAMA_CONTEXT_LENGTH` ([Ollama FAQ](https://docs.ollama.com/faq)).
- Modelfile table: `num_ctx` "(Default: 2048)"
  ([Modelfile reference](https://docs.ollama.com/modelfile)).
- Since commit `0334ffa6` (2026-02-02) the default is chosen from detected
  VRAM: 262,144 at ≥47 GiB, 32,768 at ≥23 GiB, 4,096 below and on CPU
  ([Particula](https://particula.tech/blog/ollama-num-ctx-silent-prompt-truncation), 2026-08-27).
- OpenAI-compatible API: "does not have a way of setting the context size";
  use a Modelfile `PARAMETER num_ctx`
  ([OpenAI compatibility](https://docs.ollama.com/api/openai-compatibility)).

## Server environment ([Ollama FAQ](https://docs.ollama.com/faq))

| Variable | Default / effect |
|---|---|
| `OLLAMA_NUM_PARALLEL` | 1. "Required RAM will scale by `OLLAMA_NUM_PARALLEL` * `OLLAMA_CONTEXT_LENGTH`." |
| `OLLAMA_MAX_LOADED_MODELS` | 3 × number of GPUs, or 3 for CPU |
| `OLLAMA_MAX_QUEUE` | 512; beyond it the server returns 503 |
| `OLLAMA_KEEP_ALIVE` | Duration, seconds, negative = keep loaded, `0` = unload; request `keep_alive` overrides |
| `OLLAMA_FLASH_ATTENTION` | Used automatically when supported; `1` forces it on |
| `OLLAMA_KV_CACHE_TYPE` | `f16` default; `q8_0` ≈ ½ memory, "usually no noticeable impact"; `q4_0` ≈ ¼, more noticeable at long context. Global. High-GQA models (e.g. Qwen2) affected more |
| `OLLAMA_HOST` | Binds 127.0.0.1:11434 by default |
| `OLLAMA_ORIGINS` | Extra allowed CORS origins |
| `OLLAMA_MODELS` | Model storage directory |

## Modelfile ([Modelfile reference](https://docs.ollama.com/modelfile))

- Instructions: `FROM` (required), `PARAMETER`, `TEMPLATE`, `SYSTEM`,
  `MESSAGE`, `LICENSE`. `FROM` accepts a model tag, a safetensors directory,
  or a GGUF path; split GGUFs by wildcard.
- Parameter defaults listed: `temperature` 0.8, `top_k` 40, `top_p` 0.9,
  `repeat_last_n` 64, `seed` 0, `num_predict` -1.

## Import ([Importing a model](https://docs.ollama.com/import))

- "Ollama does not quantize GGUF models during import." Quantize first with
  llama.cpp `llama-quantize`.

## Structured outputs ([Structured outputs](https://docs.ollama.com/capabilities/structured-outputs))

- JSON schema goes in `format`; also pass the schema in the prompt; set
  temperature 0; works through the OpenAI-compatible API via `response_format`.
  "Ollama's Cloud currently does not support structured outputs."

## Tool calling ([Tool calling](https://docs.ollama.com/capabilities/tool-calling))

- `tools` array on `/api/chat`; results come back in `message.tool_calls`;
  parallel and multi-turn agent loops are documented. When streaming, gather
  every chunk of `thinking`, `content`, and `tool_calls` before the follow-up
  request.

# SLM eval tool facts — pulled 2026-09-30

**This file expires.** Re-verify flags against each tool's docs after about
two months.

- promptfoo Ollama provider IDs: `ollama:chat:<model>` and
  `ollama:completion:<model>` ([promptfoo Ollama provider](https://www.promptfoo.dev/docs/providers/ollama/), page dated 2026-09-25).
  Side-by-side open-model comparison with `llm-rubric` assertions, run with
  `promptfoo eval` ([promptfoo: compare open-source models](https://www.promptfoo.dev/docs/guides/compare-open-source-models/), 2026-09-18).
- lm-evaluation-harness: `--model gguf --model_args base_url=http://127.0.0.1:8080`
  evaluates a model served by `llama-server` through `/v1/completions`. It
  requires a llama.cpp release from December 2024 or newer (modern logprobs
  format); concurrency is auto-detected from server slots. The `hf` backend
  can load a GGUF with `gguf_file=`; without a separate tokenizer,
  reconstruction "can take hours or even hang indefinitely"
  ([lm-evaluation-harness README](https://github.com/EleutherAI/lm-evaluation-harness)).
- llama-bench flags: `-p/--n-prompt` (default 512), `-n/--n-gen` (default 128),
  `-d/--n-depth` (default 0), `-r/--repetitions` (default 5), `-ngl` (default
  -1), `-fa on|off|auto` (default auto), `-ctk` cache type (default f16).
  Output rows are `pp512`, `tg128`, and `@ d<depth>` variants
  ([llama-bench README](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/tools/llama-bench/README.md)).

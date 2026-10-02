# maximus-slm-eval

Evaluate local models and quants on your tasks and your hardware, not
leaderboards.

**What it does.** Turns "which model?" into a thresholded decision, builds a
task set from real inputs with code-checkable assertions, runs candidates side
by side in promptfoo against Ollama, checks quant degradation with
lm-evaluation-harness against a llama.cpp server, measures throughput at real
context depth with `llama-bench`, and writes a decision memo.

**Triggers.** "which local model is better for X", "Q4 vs Q8 quality",
"benchmark my Ollama models", "promptfoo", "lm-eval-harness", "llama-bench",
"is this SLM good enough".

**Files.**
- `SKILL.md` — 8-step workflow, rigor rules, anti-patterns
- `HOWTO.md` — promptfoo config, lm-eval quant check, llama-bench at depth, memo
- `references/slm-eval-2026-09.md` — dated tool facts and sources
- `examples/decision-memo.md` — the memo template

**Siblings.** `maximus-eval-and-test`, `maximus-slm-tool-calling`,
`maximus-slm-local-stack`, `maximus-llm-model-selection`.

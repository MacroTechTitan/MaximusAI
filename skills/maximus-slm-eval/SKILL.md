---
name: maximus-slm-eval
description: "Evaluate local models and quantizations on your own tasks instead of leaderboards. Covers building a task-specific test set, promptfoo side-by-side runs against Ollama, lm-evaluation-harness against a llama.cpp server for standard tasks, llama-bench for prompt/generation throughput at real context depth, quant-vs-quant comparisons, and a decision memo. Use for 'which local model is better for X', 'Q4 vs Q8 quality', 'benchmark my Ollama models', 'promptfoo', 'lm-eval-harness', 'llama-bench', 'is this SLM good enough'."
metadata: { "openclaw": { "emoji": "📏", "pillar": "ai-engineering", "source": "maximus" } }
---

# Maximus — SLM Eval

A leaderboard tells you which model won someone else's exam. You are not taking
that exam. This skill writes yours, runs every candidate through it on your
hardware, and returns a decision with the evidence attached.

## Purpose

Answer "is this local model (or this quant) good enough for this job, and which
one should I run?" with measured quality, measured speed at realistic context,
and an explicit statement of what was not tested.

## Scope boundary

| Need | Skill |
|---|---|
| Compare local models / quants on your tasks and box | **this skill** |
| Eval strategy for a shipped product (PR / nightly / canary) | `maximus-eval-and-test` |
| Tool-call failure rates specifically | `maximus-slm-tool-calling` (feeds this skill) |
| Choosing between cloud APIs | `maximus-llm-model-selection` |
| Picking candidates to test in the first place | `maximus-slm-local-stack` |

## Core workflow

1. **Write the question as a decision.** "Pick the smallest model at ≥ 90% of
   Qwen3-14B's score on our extraction set, at ≥ 20 tok/s with 16K context on
   this laptop." A threshold turns a vibe into a result.
2. **Build the task set from real work.** 30-100 cases drawn from actual inputs,
   including the hard and ugly ones. Prefer assertions that are checkable in
   code (exact field, regex, JSON schema, contains-citation) over model-graded
   ones. Hold out a slice you do not look at while tuning prompts.
3. **Pin everything that is not under test.** The same prompt, temperature 0
   (or a fixed seed), the same context size set via Modelfile, and the same
   runtime version. Record them all in the memo.
4. **Run quality side by side with promptfoo.** Providers
   `ollama:chat:<model>` per candidate, one config, `promptfoo eval`, then
   `promptfoo view`. Model-graded `llm-rubric` assertions are allowed, but say
   which model graded, and do not let a candidate grade itself.
5. **Add standard tasks only when they answer the question.**
   lm-evaluation-harness `--model gguf` against a llama.cpp server measures
   loglikelihood tasks on the exact quant you will run. It is useful for
   quant-degradation checks, and weak evidence about your own task.
6. **Measure speed at the depth you will use.** `llama-bench` reports prompt
   processing (`pp`) and generation (`tg`). Use `-d` so it measures at real
   context depth, not an empty cache. Five repetitions is the default; report
   mean ± stddev.
7. **Compare quants explicitly.** Q4_K_M vs Q5_K_M vs Q8_0 of one model on the
   same set. The quality delta is task-dependent, and this is the only honest
   way to know yours.
8. **Write the decision memo.** A table (model, quant, pass rate, tok/s pp/tg
   at depth, peak memory), the choice, the runner-up, and what was not tested.

## Rigor rules

- A pass rate on 30 cases has wide error bars. A two-case difference is
  noise, so say so.
- Report failures by category (hallucinated field, wrong format, refusal,
  truncation), not just a total.
- Re-run the winner once more end-to-end before declaring it. Temperature-0
  outputs can still vary across runtimes.
- If the context in the eval is smaller than the context in production, the
  eval does not cover production.

## Anti-patterns

- **Quoting MMLU to pick a summarizer.**
- **Testing at 2K context, deploying at 32K.**
- **Letting the candidate grade itself.**
- **Changing the prompt between models.** That tests the prompt.
- **One run, one winner.** Variance is real, even at temperature 0.
- **Throughput from someone else's GPU.** Run `llama-bench` on yours.

## Output

`promptfooconfig.yaml` and the test set, raw result exports, a `llama-bench`
table, and a one-page decision memo following `examples/decision-memo.md`.

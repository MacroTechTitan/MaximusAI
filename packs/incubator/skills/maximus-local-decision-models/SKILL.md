---
name: maximus-local-decision-models
description: "Use local decision models (System One /v1/systemone in Ollama, llama.cpp, vLLM Semantic Router) for routing, triage, moderation, and agent-step checks: typed questions, per-model confidence cutoffs from labeled data, human or LLM fallback. Use for 'decision model', 'systemone', 'local classifier', 'route requests locally'."
metadata: {"openclaw": {"emoji": "🎯", "pillar": "ai-engineering", "source": "maximus-scout"}}
---

# Maximus — Local Decision Models

A decision model does not write an answer. It scores the options you give it and returns a probability for each, in one pass. For routing, triage, and yes/no gates that is cheaper, faster, and easier to audit than asking a chat model to "reply with one word". This skill covers when to use one, how to ask it well, and how to pick the confidence cutoff that decides what it handles alone.

## Purpose

Replace generative calls that are really classifications with a local decision model behind the System One API, calibrated on your own labeled examples, with a defined fallback for low-confidence cases. Runtimes, model names, sizes, and limits are in `references/decision-models-2026-10.md`; they change weekly.

## Scope boundary

| Need | Use |
|---|---|
| Classify, route, gate, or score text/images with a local decision model | this skill |
| Pick a generative LLM, routing tiers, fallback chains | maximus-llm-model-selection |
| Run Ollama as a service (Modelfiles, context, env) | maximus-ollama-ops |
| Local model stack choice | maximus-slm-local-stack |
| Tool calling with small generative models | maximus-slm-tool-calling |
| Eval harnesses for local generative models | maximus-slm-eval |

## Core workflow

1. **Confirm it is a decision.** The output must be one of a fixed set of options, a yes/no probability, or a level on an ordered scale. If the task needs free text, extraction, or tool calls, this is the wrong tool.
2. **Pick the runtime you already run.** Ollama (v0.35.0+), llama.cpp `llama-server`, or vLLM Semantic Router all serve the same `POST /v1/systemone` shape: a `state` and named `questions`. Clients move between them by changing the base URL.
3. **Write the questions.** One named question per decision. Use `choice` for labels, `noul` for yes/no, `score` for ordered levels (lowest first). Give every option a description; bare labels misroute.
4. **Build a labeled set first.** Collect real inputs with the correct answer, including vague and adversarial ones. Without labels you cannot choose a cutoff.
5. **Try two or three model sizes.** A sub-1B model may be enough and is far faster; a larger one knows more. Compare on your labeled set, not on a leaderboard.
6. **Choose the cutoff per model.** For each candidate threshold, measure accuracy on the cases above it and the share of traffic it covers. `examples/calibrate_threshold.py` does this. Confidence scales differ by model, so never reuse one model's cutoff for another.
7. **Define the fallback.** Below the cutoff, send to a human queue or a generative model. Log both paths.
8. **Read `score` correctly.** It is a probability-weighted average of level indices, so it can fall between levels. If you need a band, take the highest-probability level instead of rounding the score.
9. **Batch questions on one state.** Ask everything about one input in one request; check your runtime's per-request limits.
10. **Monitor in production.** Track the share below cutoff, the fallback rate, and agreement with humans on a weekly sample. A rising fallback rate is drift.

## Anti-patterns

- **Treating `confidence` as correctness.** The docs say a high value does not guarantee the answer is right. Only your labeled set tells you that.
- **One cutoff for every model.** The same vague input can get very different confidence from two models.
- **Bare option labels.** Short labels with no description route worse than described ones.
- **Rounding `score` into a class.** It is an expected level, not a vote.
- **Silent truncation assumptions.** Ollama rejects oversized input rather than truncating; handle the 400/413 instead of retrying blindly.
- **Using a non-commercial model in a product.** Check each model's license; at least one listed decision model is CC BY-NC.

## Output

The question schema, a model comparison on the labeled set, the chosen cutoff with coverage and accuracy at that cutoff, the fallback route, and the monitoring metrics with alert thresholds.

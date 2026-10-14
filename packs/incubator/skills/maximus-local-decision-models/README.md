# maximus-local-decision-models (incubator)

Local decision models through the System One `/v1/systemone` API (Ollama, llama.cpp, vLLM Semantic Router) for routing, triage, moderation, and agent-step checks, with per-model confidence cutoffs set from labeled data and a fallback for the rest.

**Triggers:** "decision model", "systemone", "local classifier", "route requests locally", "ticket triage model".

**Files:** `SKILL.md` (workflow), `HOWTO.md` (5 recipes), `references/decision-models-2026-10.md` (runtimes, models, limits, sources), `examples/calibrate_threshold.py` (runnable, tested on `examples/sample_results.csv`), `examples/route_ticket.py` (illustrative client, not run against a server).

**Siblings:** maximus-llm-model-selection, maximus-ollama-ops, maximus-slm-local-stack, maximus-slm-tool-calling, maximus-slm-eval.

Drafted by the skill scout on 2026-10-14. Unreviewed until promoted.

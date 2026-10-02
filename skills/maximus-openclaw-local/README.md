# maximus-openclaw-local

Run OpenClaw and Maximus on a local model without silently cutting off the
prompt.

**What it does.** Measures what Maximus injects on every run (about 7,900
tokens for a full core install as of 2026-09-30), sets a context size the runtime actually honors,
writes `openclaw.json` in the current `agents.defaults.model.primary` schema,
and verifies there is no truncation on the live machine.

**Why it exists.** Ollama's context default on most consumer machines is far
smaller than Maximus's prompt, and a `num_ctx` sent over the OpenAI-compatible
API is dropped without an error. The agent just degrades.

**Triggers.** "run Maximus locally", "OpenClaw with Ollama", "local model in
OpenClaw", "no API key", "agent ignores its instructions on a local model".

**Files.**
- `SKILL.md` — the 8-step workflow, security notes, and anti-patterns
- `HOWTO.md` — measure, config, context, verification, slim workspace
- `references/openclaw-local-2026-09.md` — dated, sourced key paths and limits
- `examples/measure_prompt.py` — prompt-size estimator for a Maximus checkout

**Siblings.** `maximus-slm-local-stack` (model + hardware),
`maximus-ollama-ops` (runtime), `maximus-slm-tool-calling`, `maximus-slm-eval`.

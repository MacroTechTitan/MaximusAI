# maximus-slm-tool-calling

Make small local models call tools and emit JSON reliably, and prove it with a
failure rate.

**What it does.** Builds a regression set first, then applies fixes in order of
impact: a tool-trained model, the correct chat template, grammar-constrained
decoding (llama.cpp GBNF / JSON schema, Ollama `format`), a smaller tool
surface, one-tool-per-step chains, truncated tool results, and a single
validated retry.

**Triggers.** "local model won't call tools", "agent writes the tool call as
text", "invalid JSON from Ollama", "GBNF", "constrained decoding", "function
calling with a small model".

**Files.**
- `SKILL.md` — call modes, 8-step fix ladder, grammar gotchas
- `HOWTO.md` — regression set, constrained action block, Ollama, one tool per step
- `references/slm-tool-calling-2026-09.md` — dated sources
- `examples/fix-ladder.md` — a worked before/after on a failing 8B agent (illustrative)

**Siblings.** `maximus-agent-design`, `maximus-ollama-ops`, `maximus-slm-eval`.

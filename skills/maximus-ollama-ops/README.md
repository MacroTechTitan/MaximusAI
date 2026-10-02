# maximus-ollama-ops

Operate Ollama as a configured service instead of a demo.

**What it does.** Moves model settings into version-controlled Modelfiles,
sizes context and parallelism from memory arithmetic, sets the `OLLAMA_*`
server env deliberately, imports GGUF/safetensors with template checks, picks
native vs OpenAI-compatible API per client, and verifies with `ollama ps`.

**The two traps it catches.** Context set over the OpenAI-compatible API is
silently ignored. Parallel slots multiply KV-cache memory.

**Triggers.** "Ollama Modelfile", "num_ctx", "OLLAMA_ env vars", "import a
GGUF", "Ollama is slow", "Ollama out of memory", "serve Ollama to my team".

**Files.**
- `SKILL.md` — 7-step workflow, structured outputs, anti-patterns
- `HOWTO.md` — baseline, Modelfile, server env, GGUF import, validated JSON
- `references/ollama-ops-2026-09.md` — dated, sourced defaults
- `examples/team-server.md` — a sized two-user config on a 24 GB GPU

**Siblings.** `maximus-slm-local-stack`, `maximus-openclaw-local`,
`maximus-slm-tool-calling`, `maximus-slm-local-finetune`.

# maximus-slm-local-stack

Choose and deploy a small language model (roughly 1B-14B) on hardware you own —
for private, offline, or zero-marginal-cost work.

**What it does.** Walks the hardware-ceiling → memory-budget → model →
quantization → runtime decision with the VRAM arithmetic shown out loud,
including the KV cache term that most local-LLM advice omits. Covers GGUF
quantization tradeoffs, runtime selection across Ollama / LM Studio / llama.cpp
/ MLX / vLLM, air-gapped installation, and benchmarking your own machine instead
of trusting published throughput numbers.

**What it refuses to do.** Recommend a local SLM for work it will fail at. The
skill states the capability envelope up front and routes to an API model when
privacy is not a hard constraint and the task needs frontier reasoning.

**Triggers.** "run a model locally", "which SLM", "small language model",
"offline LLM", "Ollama", "LM Studio", "llama.cpp", "GGUF", "quantization",
"how much VRAM", "will this fit on my GPU", "air-gapped", "no cloud API".

**Files.**
- `SKILL.md` — the 7-step workflow and anti-patterns
- `HOWTO.md` — six recipes, including the VRAM-fit calculation and air-gapped install
- `references/slm-landscape-2026-09.md` — dated, fully sourced model/quant/runtime numbers
- `examples/vram-budget.md` — three worked budgets on real hardware tiers

**Siblings.** `maximus-local-research-assistant` for the application layer on
top. `maximus-llm-model-selection` for cloud routing. `maximus-fine-tuning` to
specialize a small model. `maximus-k3-self-hosting` for the datacenter end of
the same problem.

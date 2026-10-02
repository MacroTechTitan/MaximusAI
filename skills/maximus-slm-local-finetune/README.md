# maximus-slm-local-finetune

Fine-tune a small model on your own hardware and ship it to Ollama, with proof
that it beats the base model.

**What it does.** Gates the decision (a measured prompt-plus-RAG shortfall, enough
clean data, a held-out set), then runs QLoRA/LoRA with Unsloth or MLX-LM,
evaluates adapter vs base, merges, exports GGUF, quantizes, creates the Ollama
model with the training chat template, and re-evaluates the build you will
actually serve.

**Triggers.** "fine-tune locally", "LoRA on my GPU", "QLoRA", "Unsloth", "MLX
fine-tune", "export to GGUF", "put my fine-tune in Ollama".

**Files.**
- `SKILL.md` — the gate, 9-step workflow, anti-patterns
- `HOWTO.md` — Unsloth → Ollama, MLX-LM → GGUF, quantize and re-eval (illustrative code)
- `references/slm-local-finetune-2026-09.md` — dated VRAM table and export limits
- `examples/TRAINING.md` — the reproducibility record template

**Siblings.** `maximus-fine-tuning`, `maximus-ai-data-pipeline`,
`maximus-slm-eval`, `maximus-ollama-ops`.

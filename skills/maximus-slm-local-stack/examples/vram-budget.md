# Worked example — three VRAM budgets

Illustrating the method from `SKILL.md` step 2. Model VRAM figures come from
`references/slm-landscape-2026-09.md`; the KV arithmetic uses ~0.75 MB per
layer per 1,000 tokens at FP16 KV. These are planning estimates — step 5 of
the skill says measure, and that still applies.

---

## Tier A — 8 GB discrete GPU (RTX 4060, 3070)

**Ask:** summarize 20-page PDFs locally. Target context 16K.

| Term | Estimate |
|---|---|
| Qwen3-8B weights @ Q4_K_M | ~5.0 GB |
| KV cache, 32 layers @ 16K | ~0.4 GB |
| Runtime overhead | ~1.0 GB |
| **Total** | **~6.4 GB** |

Fits with headroom. **Verdict:** Qwen3-8B at Q4_K_M on Ollama. Room to push
context toward 32K if the documents run long.

Note what happens if the user then wants 128K context: the KV term jumps by
roughly an order of magnitude and the budget breaks. Ask about context *before*
recommending, not after.

## Tier B — 12 GB GPU (RTX 4070)

**Ask:** local reasoning over technical material. Target context 8K.

| Term | Estimate |
|---|---|
| Phi-4 14B weights @ Q4_K_M | ~9.0 GB |
| KV cache, 40 layers @ 8K | ~0.24 GB |
| Runtime overhead | ~1.0 GB |
| **Total** | **~10.2 GB** |

Fits, but tight — this is why Phi-4 14B is described as needing 12 GB rather
than 8 GB. **Verdict:** Phi-4 at Q4_K_M, and do not raise context much without
quantizing the KV cache. If the user also wants an embedding model resident for
RAG, add ~0.3-1.5 GB and re-check; at that point Qwen3-8B is the safer pick.

## Tier C — 16 GB Apple Silicon (M3, M4)

**Ask:** offline study assistant over a personal document corpus. Target
context 32K, embedding model resident.

Usable memory: ~11-12 GB of the 16 GB, since unified memory is shared with the
OS.

| Term | Estimate |
|---|---|
| Qwen3-8B weights @ Q4_K_M | ~5.0 GB |
| KV cache, 32 layers @ 32K | ~0.8 GB |
| Embedding model (nomic-embed-text class) | ~0.3 GB |
| Runtime overhead | ~1.0 GB |
| **Total** | **~7.1 GB** |

Comfortable. **Verdict:** MLX or LM Studio, Qwen3-8B at Q4_K_M, embedding model
resident alongside. Then hand off to `maximus-local-research-assistant` for the
corpus, grounding, and citation design.

---

## The failure this method prevents

Sizing on weights alone makes every tier above look trivially satisfied, then
the machine dies the first time someone pastes a long document in. The KV term
is small at 8K, noticeable at 32K, and dominant at 128K — so the context
question is not a detail, it is the question.

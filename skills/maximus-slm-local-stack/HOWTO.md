# HOWTO — SLM Local Stack

Six recipes. Each assumes you have read `SKILL.md` and will pull volatile
numbers from `references/slm-landscape-2026-09.md` after re-verifying them.

---

## 1. "Will this model fit on my GPU?"

The question people ask, and the answer they do not expect.

1. Get VRAM, GPU family, and system RAM. On Apple Silicon, budget 70-75% of
   unified memory.
2. Ask for the **real target context length**. This is the step everyone skips
   and it decides the answer.
3. Weights: `params_B × 0.625` GB at Q4_K_M.
4. KV cache: `~0.75 MB × n_layers × (context / 1000)` at FP16 KV.
5. Add ~1 GB runtime overhead.
6. Compare to ceiling. If over, in order: cut context, quantize KV to Q8, then
   consider a smaller model. Dropping to Q3 or Q2 is the last resort.

Report the two terms separately. "8B at Q4 is 5 GB" is the answer that gets
people into trouble at 32K context.

## 2. Pick a model from scratch

1. Establish the hardware ceiling (recipe 1).
2. Classify the task: extraction/summarization/classification (SLM-friendly),
   versus open-ended factual or multi-step reasoning (SLM-hostile).
3. If SLM-hostile and privacy is not a hard requirement, **say so** and route
   to `maximus-llm-model-selection`. Stop here.
4. If SLM-friendly or privacy is mandatory, shortlist from the reference file
   by fit, task shape, and license.
5. Prefer higher precision on a smaller model over Q2 on a larger one.
6. Name the license explicitly if anything commercial is downstream.

## 3. Choose a runtime

Answer two questions:

- **Concurrent users?** More than one → vLLM (NVIDIA/AMD) or SGLang. One → keep
  reading.
- **Apple Silicon?** Yes → MLX, or LM Studio for a GUI over it.

Otherwise: Ollama for CLI-first, LM Studio for GUI-first, llama.cpp directly
when you need flags neither wrapper exposes. Ollama and LM Studio wrap the same
engines, so do not frame this as a performance decision.

## 4. Benchmark your own box

Never quote someone else's tokens/sec. Measure four things at your real context
length:

- prefill/prompt-eval speed
- generation speed
- time to first token
- peak memory

Record hardware, model, quant, and context alongside every number. With
llama.cpp, `llama-bench` covers prefill and generation directly. With Ollama,
`--verbose` on a run reports eval timings. Run three times, take the median,
and note whether thermal throttling moved the numbers between runs — on
laptops it usually does.

## 5. Air-gapped install

1. On a connected machine: pull weights, verify checksums, pin the runtime
   version, download the installer.
2. Pull the tokenizer and any embedding model too. This is the usual cause of a
   failed first run in the field.
3. Transfer physically. Record versions of everything in a manifest file beside
   the weights.
4. Test with networking **physically disabled**. A firewall test will pass for
   a tool that phones home for a manifest; the field will not.
5. Document the exact restore procedure, because the person rebuilding this may
   not be you.

## 6. Point Claude Code at a local model

`ANTHROPIC_BASE_URL` redirects Claude Code's Anthropic-format requests to any
server speaking that format, which now includes Ollama, LM Studio, and
llama.cpp natively. Practical notes:

- Expect degraded agentic performance. Tool-calling reliability is the first
  thing to fall off at small model sizes, and Claude Code leans on it heavily.
- Good fit: offline work, private repos under strict policy, cost-free bulk
  edits in a familiar language.
- Poor fit: long autonomous multi-step tasks. Keep a frontier model for those.
- Pairs with `packs/devops/skills/mtt-claude-cursor` for the approval and
  execution model once the endpoint is wired up.

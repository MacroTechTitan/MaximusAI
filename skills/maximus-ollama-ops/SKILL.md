---
name: maximus-ollama-ops
description: "Operate Ollama as a real service: Modelfiles, context length that actually applies, server env (keep-alive, parallelism, loaded models, flash attention, KV cache type, bind address), GGUF/safetensors import, native vs OpenAI-compatible API, structured outputs, and memory sizing under concurrency. Use for 'Ollama Modelfile', 'num_ctx', 'OLLAMA_ env vars', 'import a GGUF', 'Ollama is slow/out of memory', 'serve Ollama to my team'."
metadata: { "openclaw": { "emoji": "🦙", "pillar": "ai-engineering", "source": "maximus" } }
---

# Maximus — Ollama Ops

Ollama's install is one line, which is why so many installs are wrong. The
defaults are tuned to make a first `ollama run` feel instant, not to serve an
agent with a 20K-token prompt to three people at once. This skill is the gap
between those two.

## Purpose

Turn an Ollama install into a configured, measured service: models defined in
version-controlled Modelfiles, context and memory settings chosen from
arithmetic, the right API for each client, and a verification step that reads
what the server actually loaded rather than what the config says.

## Scope boundary

| Need | Skill |
|---|---|
| Configure and run the Ollama server and its models | **this skill** |
| Choose model + quant for the hardware | `maximus-slm-local-stack` |
| Point OpenClaw / Maximus at it | `maximus-openclaw-local` |
| Force valid JSON or tool calls | `maximus-slm-tool-calling` |
| Turn a fine-tune into an Ollama model | `maximus-slm-local-finetune` |

## Core workflow

1. **Read the live state first.** `ollama --version`, `ollama ps` (loaded
   models, their context, and CPU/GPU split), `ollama show <model>`
   (parameters, template, capabilities). Record them before changing anything.
2. **Pick the context from need, then prove it fits.** Context size is a
   memory decision, not a quality knob. KV cache grows linearly with it and is
   multiplied by parallel slots: required memory scales with
   `OLLAMA_NUM_PARALLEL × context length`.
3. **Define models in Modelfiles, not in client code.** `FROM` plus `PARAMETER
   num_ctx`, `temperature`, `stop`, and a `SYSTEM` line if the model is
   single-purpose. Check the Modelfiles into the project. A tag like
   `qwen3-64k` documents itself; a request-time option does not.
4. **Choose the API per client.** The native `/api/chat` accepts `options`
   (including `num_ctx`), `keep_alive`, `format`, and `think`. The
   OpenAI-compatible `/v1/*` endpoints are for tools that only speak OpenAI.
   They cannot set context size, so those clients must use a Modelfile tag.
5. **Set server env deliberately** (`references/ollama-ops-2026-09.md` has
   defaults with sources):
   - `OLLAMA_CONTEXT_LENGTH` — server-wide default context.
   - `OLLAMA_KEEP_ALIVE` — how long a model stays loaded; request
     `keep_alive` overrides it. `-1` pins, `0` unloads.
   - `OLLAMA_NUM_PARALLEL` (default 1), `OLLAMA_MAX_LOADED_MODELS` (default
     3 × GPUs, or 3 on CPU), `OLLAMA_MAX_QUEUE` (default 512; beyond it, 503).
   - `OLLAMA_FLASH_ATTENTION=1` and `OLLAMA_KV_CACHE_TYPE` (`f16` default,
     `q8_0` about half the memory, `q4_0` about a quarter). The cache type is
     global, and models with high GQA ratios (the docs cite Qwen2) lose more
     from it.
   - `OLLAMA_HOST` — loopback by default. Keep it there unless there is a
     reverse proxy with auth in front.
6. **Import, don't hand-roll.** GGUF: `FROM ./model.gguf` (split files by
   wildcard). Ollama does **not** quantize GGUF on import, so quantize first
   with `llama-quantize`. Safetensors: `FROM /dir`. Always compare `ollama
   show --template` against the model card's chat template. A wrong template
   is the most common cause of garbage output from an imported model.
7. **Verify.** `ollama ps` again. The context must match, and the PROCESSOR
   column should read 100% GPU if you sized for GPU. A CPU/GPU split means
   layers spilled and throughput will crater. Then run a real request of
   realistic length and time it.

## Structured outputs

Pass a JSON schema in `format` (native) or `response_format` (OpenAI-compatible).
Also put the schema in the prompt, set temperature to 0, and validate with
Pydantic or Zod anyway. Constraining the format guarantees the shape, not the
facts. For tool calls on small models, go to `maximus-slm-tool-calling`.

## Anti-patterns

- **Context set in a client library that talks to `/v1`.** It is discarded
  with a 200.
- **`OLLAMA_NUM_PARALLEL=4` without redoing the memory math.** Four slots mean
  four times the KV cache.
- **`OLLAMA_HOST=0.0.0.0` on a laptop on café Wi-Fi.** The API has no auth.
- **Assuming the default context.** Ollama's own docs give 4,096 in the FAQ
  and 2,048 in the Modelfile table, and newer builds size it by VRAM. Read
  `ollama ps`.
- **Importing a GGUF and trusting the auto template.** Check it.
- **Pinning every model with `keep_alive: -1` on a shared GPU.** The next model
  load then evicts or fails.

## Output

Modelfiles, a server env block for the platform (systemd override, launchd,
or Windows user env), a memory table (weights + KV × parallel slots +
overhead vs. available VRAM), and the post-change `ollama ps` output as proof.

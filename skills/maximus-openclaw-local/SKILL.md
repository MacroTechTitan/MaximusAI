---
name: maximus-openclaw-local
description: "Run OpenClaw and Maximus on a local model (Ollama, LM Studio, llama.cpp, MLX) so the agent actually sees its own prompt. Covers the current openclaw.json model schema, the 64K context floor, setting num_ctx where it takes effect, budgeting Maximus's per-run prompt, and local-primary/cloud-fallback routing. Use for 'run Maximus locally', 'OpenClaw with Ollama', 'local model in OpenClaw', 'no API key', 'agent ignores its instructions on a local model'."
metadata: { "openclaw": { "emoji": "🦞", "pillar": "ai-engineering", "source": "maximus" } }
---

# Maximus — OpenClaw Local

A local model that cannot see the system prompt is not running Maximus. It is
running a stranger who was handed the last page of the manual. This skill makes
sure the whole manual fits, and proves it before anyone calls the setup done.

## Purpose

Get OpenClaw plus the Maximus workspace running on a model you host, with the
context arithmetic shown and verified on the actual machine. The deliverable is
a working `~/.openclaw/openclaw.json`, a runtime configured to match it, and a
measured statement of how much headroom is left for the task.

## Scope boundary

| Need | Skill |
|---|---|
| Wire OpenClaw + Maximus to a local runtime | **this skill** |
| Pick the model / quant for your hardware | `maximus-slm-local-stack` |
| Operate Ollama itself (Modelfiles, server env, API) | `maximus-ollama-ops` |
| Make a small model call tools without breaking | `maximus-slm-tool-calling` |
| Prove the local model is good enough for the job | `maximus-slm-eval` |

## The failure this skill exists to prevent

It is silent. Nothing errors. The agent just gets dumber and nobody can say why.

1. OpenClaw assembles a system prompt on every run: tool list, skill list
   (metadata only), and bootstrap files such as `AGENTS.md` and `SOUL.md`.
2. The Maximus-owned share alone — `core/`, `memory/`, and every linked
   skill's description — measured about **7,900 tokens** for the full core
   install on 2026-09-30, after a description trim that took it down from
   about 10,400. OpenClaw's own prompt and tool schemas come on top.
3. Ollama's default context on a machine with less than 23 GiB VRAM has been
   **4,096 tokens** under every source checked (the docs also list 2,048 in one
   table; see references). A 12,000-token prompt at 4,096 reaches the model as
   its first few tokens plus its last ~2,046.
4. Setting `num_ctx` through the OpenAI-compatible endpoint does nothing. The
   field is discarded and the request still returns 200.

Result: the recommended "free, no API" path can run with most of Maximus cut
out, and it looks like model weakness rather than misconfiguration.

## Core workflow

1. **Measure the prompt before choosing a context size.** Run
   `python {baseDir}/examples/measure_prompt.py <maximus-repo>` (or the
   recipe in `HOWTO.md`). Add a margin for OpenClaw's own prompt and tools, then
   the task itself: documents, tool results, and the reply.
2. **Set the floor at 64K.** Ollama's OpenClaw integration docs recommend at
   least 64K context for local models. Below that, say plainly that the setup
   is degraded, and by how much.
3. **Check it fits in memory.** 64K of FP16 KV cache on an 8B-class model is
   several GB by itself. Use the VRAM math in `maximus-slm-local-stack`. If it
   does not fit: quantize the KV cache to `q8_0`, pick a smaller model, or use
   a hybrid setup. Never quietly shrink the context.
4. **Set context where it takes effect.** For Ollama, either set a server-wide
   `OLLAMA_CONTEXT_LENGTH`, or bake `PARAMETER num_ctx` into a Modelfile and
   point OpenClaw at that model tag. Declare the same number as
   `contextWindow` in the OpenClaw provider entry so OpenClaw's own budgeting
   (tool-result caps, compaction) matches reality.
5. **Write the config in the current schema.** The default model goes at
   `agents.defaults.model.primary` as `provider/model`, fallbacks at
   `agents.defaults.model.fallbacks`, custom endpoints under
   `models.providers.<id>`. Template in `HOWTO.md` recipe 2.
6. **Trim what OpenClaw injects.** Link only the skills this machine needs.
   Every eligible skill costs tokens on every run, and a local box rarely needs
   the SEO or film packs. `skills.limits.maxSkillsPromptChars` caps the skill
   list if you want a hard ceiling.
7. **Verify on the real run.** `ollama ps` shows the loaded context; ask the
   agent to quote a line from the *start* of `SOUL.md` and one from the *end*
   of the skill list. If it cannot, the prompt is being truncated.
8. **Decide the routing honestly.** Local-primary with a cloud fallback suits
   most people. Local-only is right when data cannot leave the box, and then
   the capability ceiling must be stated, not hidden.

## Security

Local does not mean safe. OpenClaw's first launch warns about tool access for a
reason: a small model follows injected instructions in a web page or file more
readily than a frontier model does. Keep the gateway on loopback, keep DM
access paired, and do not give a local model shell or send tools you would not
give an intern on day one. Binding Ollama to `0.0.0.0` exposes an
unauthenticated API to the network.

## Anti-patterns

- **Trusting a default context.** Three published defaults disagree; `ollama ps`
  does not.
- **Passing `num_ctx` through `/v1/chat/completions`.** Silently ignored.
- **Declaring `contextWindow: 128000` for a model served at 4K.** OpenClaw then
  budgets for context that does not exist.
- **Linking every pack on a 16 GB laptop.** You pay for their descriptions on
  every turn.
- **Calling a truncation bug "the model is dumb."** Measure first.
- **Using the old top-level `agent.model` form.** Current docs use
  `agents.defaults.model.primary`; the repo example was written before that.

## Output

A config diff or full `openclaw.json`, the runtime change (env var or
Modelfile), a context budget table (Maximus prompt, OpenClaw overhead, task
headroom), the verification result from step 7, and a single sentence naming
the capability ceiling of the chosen model. Volatile facts come from
`references/openclaw-local-2026-09.md`; re-verify if it is more than about two
months old.

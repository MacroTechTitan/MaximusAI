# HOWTO — OpenClaw Local

Five recipes. Numbers and key paths come from
`references/openclaw-local-2026-09.md`; re-verify them against the OpenClaw docs
if that file is stale.

---

## 1. Measure what Maximus injects

```bash
python ~/.openclaw/workspace/skills/maximus-openclaw-local/examples/measure_prompt.py ~/src/MaximusAI
```

It sums `core/*.md`, `memory/*.md`, and each linked skill's name and
description at about 4 characters per token, then prints the share consumed at
4K, 8K, 32K, and 64K. It is an estimate: tokenizers differ. Keep 30-40%
headroom for OpenClaw's own prompt, tool schemas, and the task.

## 2. Config: Ollama as primary, cloud fallback

```json5
// ~/.openclaw/openclaw.json
{
  agents: {
    defaults: {
      model: {
        primary: "ollama/qwen3-64k",           // the Modelfile tag from recipe 3
        fallbacks: ["anthropic/claude-sonnet-4-6"]  // optional; needs its own key
      }
    }
  },
  skills: { load: { watch: true } }
}
```

Onboarding can write the provider block for you: `openclaw onboard`, then pick
Ollama. For a LAN host, the non-interactive form takes `--custom-base-url
"http://host:11434"`. Local and LAN Ollama URLs do not need a real key; OpenClaw
uses the `ollama-local` marker.

For an OpenAI-compatible server (llama.cpp `llama-server`, LM Studio, MLX),
declare it under `models.providers.<id>` with `baseUrl`, `api`
(`openai-responses` if the server supports it, else `openai-completions`),
`timeoutSeconds`, and a `models[]` entry whose `contextWindow` matches what the
server actually runs. The model `id` there is provider-local — no prefix.

## 3. Make the context real (Ollama)

Per model (preferred, because it travels with the tag):

```
# Modelfile
FROM qwen3:8b
PARAMETER num_ctx 65536
```

```bash
ollama create qwen3-64k -f Modelfile
```

Server-wide (every model):

```bash
OLLAMA_CONTEXT_LENGTH=65536 ollama serve
# systemd: add Environment="OLLAMA_CONTEXT_LENGTH=65536" to the service override
```

If 64K does not fit, add `OLLAMA_FLASH_ATTENTION=1` and
`OLLAMA_KV_CACHE_TYPE=q8_0` (roughly half the KV memory of f16) before
reaching for a smaller model.

## 4. Verify there is no truncation

1. Start a run, then `ollama ps`. The CONTEXT column must show your number.
2. Ask the agent: "Quote the first heading of SOUL.md and the name of the
   last skill in your skill list." Both must be right.
3. Paste a long document and ask about its first paragraph. Wrong or vague
   answers mean the window is still too small for the real task.

## 5. Slim workspace for a small box

Link only the skills you use instead of running `install.sh` unchanged:

```bash
W=~/.openclaw/workspace; R=~/src/MaximusAI
for s in maximus-brain maximus-slm-local-stack maximus-local-research-assistant \
         maximus-openclaw-local maximus-ollama-ops; do
  ln -sfn "$R/skills/$s" "$W/skills/$s"
done
```

Re-run recipe 1 afterwards and record the new number.

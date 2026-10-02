# Maximus grows to 57 — your local model isn't reading the manual

*2026-09-30 · Macro Tech Titan*

Maximus's README has always offered a free path: point OpenClaw at a local
model through Ollama and pay nothing. This week I measured that path. On most
consumer machines, it did not work.

It didn't crash. It degraded quietly, which is worse. So before shipping anything
new, I fixed that. Then came five skills for running Maximus on open-source
local models. Suite total: 57.

## The measurement

OpenClaw builds a system prompt on every run: the tool list, the skill list,
and the workspace bootstrap files
([OpenClaw docs](https://docs.openclaw.ai/reference/token-use)). Maximus
contributes three core files, its memory files, and a name and description for
every linked skill. I summed them for a full core install. It came to about
**10,400 tokens**, before OpenClaw added anything of its own.

Now the runtime. Ollama's FAQ says its default context is
[4,096 tokens](https://docs.ollama.com/faq). Its Modelfile reference says
[2,048](https://docs.ollama.com/modelfile). A read of the source says that since
February the default has depended on VRAM: 4,096 below 23 GiB, 32,768 up to
47 GiB, and 262,144 above
([Particula](https://particula.tech/blog/ollama-num-ctx-silent-prompt-truncation)).
Three answers from one project. But every 8, 12, and 16 GB card lands on 4,096
in all three.

A 10,400-token prompt in a 4,096-token window does not error. The same analysis
shows what happens: a 12,000-token prompt at 4,096 reaches the model as its
first few tokens and its last ~2,046. The model never sees most of `SOUL.md`.
It is not running Maximus. It is running on a torn-off last page.

There is a second trap. The obvious fix is to send `num_ctx` with the request.
Through Ollama's OpenAI-compatible endpoint, which is what most agent frameworks
speak, the field is discarded and the request returns 200. Ollama's docs say it
plainly: "The OpenAI API does not have a way of setting the context size for a
model"
([Ollama](https://docs.ollama.com/api/openai-compatibility)). And Ollama's own
OpenClaw guide recommends
[at least 64K](https://docs.ollama.com/integrations/openclaw) for local models.

Anyone who followed the README on a normal laptop got an agent that seemed a bit
dim, and had no way to know why.

## What changed in the repo

**The config.** `config/openclaw.example.json` used a top-level `agent.model`
key. Current OpenClaw docs put the default at
[`agents.defaults.model.primary`](https://docs.openclaw.ai/providers/ollama/setup).
The example now uses that, and shows how to bake context into a Modelfile tag.
It also includes a commented cloud fallback and a line on how to verify the
setup.

**The descriptions.** The skill list is paid for on every turn, so I rewrote
all 38 long existing descriptions to around 300 characters each, keeping their
trigger phrases. With five new skills added, a full core install now measures
about **7,900 tokens**, down from 10,400. That is still too big for 4,096, and
honestly so: the fix for small context is to set the context, not to pretend
Maximus fits in 4K.

## The five skills

**`maximus-openclaw-local`** is the skill the README should have pointed to
from day one. Measure the prompt with the included script. Set a 64K floor.
Check it fits in memory. Set context where it actually applies. Write the
config in the current schema. Link only the skills this machine needs. Then
verify on the live run: `ollama ps` must show the number, and the agent must be
able to quote the first heading of `SOUL.md`.

**`maximus-ollama-ops`** treats Ollama as a service. Model settings live in
version-controlled Modelfiles. Server settings are chosen from arithmetic,
including the one that catches people: required memory scales with
`OLLAMA_NUM_PARALLEL` × context length
([Ollama FAQ](https://docs.ollama.com/faq)). It also covers GGUF import. Ollama
does not quantize on import, and a wrong chat template is the usual cause of an
imported model producing garbage.

**`maximus-slm-tool-calling`** is for the moment a local agent writes out a
perfect description of a tool call instead of making it. The fixes run in order
of impact: a model trained for tool use, the right template, grammar-constrained
decoding so invalid JSON can't be generated, fewer tools, and one tool per step.
Community reports show 7B–14B models losing the call pattern after the first
tool result
([n8n](https://community.n8n.io/t/tool-calling-chain-with-local-ollama-models-7b-14b-2nd-tool-never-executed/280320/4)).
Constrain only the action block: forcing structure on every token can suppress
the reasoning that comes before it
([LLM Configurator](https://llmconfigurator.com/en/guides/coding-agents/tool-calling-local-models)).
And the regression set comes first, because tool-call failure is a rate, and
one good run proves nothing.

**`maximus-slm-eval`** replaces leaderboards with your own test. Build a task
set from real inputs. Run candidates side by side in
[promptfoo](https://www.promptfoo.dev/docs/providers/ollama/) against Ollama.
Check quant degradation with
[lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)
against a llama.cpp server. Measure speed with `llama-bench` at the context
depth you will actually use, not an empty cache. The output is a decision memo
that names what wasn't tested.

**`maximus-slm-local-finetune`** makes you earn the fine-tune: a measured
prompt-plus-RAG shortfall, enough clean data, and a held-out set. Then it
carries the result all the way into `ollama run`. The costs are now small.
Unsloth lists about
[5 GB of VRAM for a 7B QLoRA](https://unsloth.ai/docs/get-started/fine-tuning-for-beginners/unsloth-requirements).
The traps are specific. MLX exports GGUF only for
[Mistral, Mixtral, and Llama-style models in fp16](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md).
And the eval that counts is the one on the quantized build you actually ship.

## Two corrections

The homepage headline has read "55 skills" since the last release. The page
actually showed 52, because Lovable added a Private Securities Pack card that
the repo had never counted. It now counts, and the number is 57.

The repo's release changelog recorded the 51-skill release as not yet on the
site. It was already live. A fetch service had been serving a cached copy. Check the raw HTML before trusting a
preview, including mine.

## Try them

```bash
git clone https://github.com/MacroTechTitan/MaximusAI.git
cd MaximusAI && ./install.sh
python skills/maximus-openclaw-local/examples/measure_prompt.py .
```

All five land in core. Model names, defaults, and VRAM tables live in dated
reference files with a source URL on every figure. Where sources disagree, as
Ollama's three context defaults do, the file lists all three and tells you to
check `ollama ps`.

Free, MIT, no tier. 57 skills.

# OpenClaw local-model facts — pulled 2026-09-30

**This file expires.** OpenClaw and Ollama ship often. Re-verify anything here
that is more than about two months past 2026-09-30.

## OpenClaw configuration

- Default model key: `agents.defaults.model.primary`, value `provider/model`;
  fallbacks at `agents.defaults.model.fallbacks`
  ([OpenClaw local models](https://docs.openclaw.ai/gateway/local-models),
  [Ollama setup](https://docs.openclaw.ai/providers/ollama/setup)).
- Custom endpoints live under `models.providers.<id>` with `baseUrl`, `api`,
  `apiKey`, `timeoutSeconds`, `models[]` (`id`, `contextWindow`, `maxTokens`).
  `models[].id` is provider-local; do not include the prefix. If `api` is
  omitted on a provider with a `baseUrl`, it defaults to `openai-completions`;
  use `openai-responses` where supported
  ([OpenClaw local models](https://docs.openclaw.ai/gateway/local-models)).
- Ollama model refs: `ollama/<model-id>`; cloud-only: `ollama-cloud/<model-id>`.
  Loopback, private-network, `.local`, and bare-hostname Ollama URLs need no
  real token; OpenClaw uses the `ollama-local` marker
  ([Ollama setup](https://docs.openclaw.ai/providers/ollama/setup)).
- None of the pages checked say whether the older top-level `agent.model` form
  still works. Treat it as unsupported and use the current path.

## What OpenClaw injects per run

- Tool list and short descriptions; skill list (metadata only — instructions
  load on demand); workspace bootstrap files including `AGENTS.md`, `SOUL.md`,
  `IDENTITY.md`, `USER.md`, `MEMORY.md` when present; time and runtime
  metadata ([Token use](https://docs.openclaw.ai/reference/token-use)).
- Skill list bounded by `skills.limits.maxSkillsPromptChars`; per-agent
  override at `agents.entries.*.skillsLimits.maxSkillsPromptChars` (default
  value not stated on the page).
- Live tool-result cap: 16,000 chars below 100K context, 32,000 at 100K+,
  64,000 at 200K+; a single tool result is also capped at 30% of the window
  ([Token use](https://docs.openclaw.ai/reference/token-use)).
- Bootstrap text cap `agents.defaults.bootstrapTotalMaxChars`, reported default
  150,000 chars by a third-party guide
  ([explain-openclaw](https://github.com/centminmod/explain-openclaw/blob/master/06-optimizations/cost-token-optimization.md),
  2026-02-01) — not confirmed on the official page.

## Context floor and Ollama defaults

- "It is recommended to use a context window of at least 64k tokens if using
  local models" ([Ollama OpenClaw integration](https://docs.ollama.com/integrations/openclaw)).
- Ollama default context — the sources disagree:
  - FAQ: 4,096 tokens, overridable with `OLLAMA_CONTEXT_LENGTH`
    ([Ollama FAQ](https://docs.ollama.com/faq)).
  - Modelfile parameter table: `num_ctx` default 2048
    ([Modelfile reference](https://docs.ollama.com/modelfile)).
  - Source analysis: since commit `0334ffa6` (2026-02-02), picked from VRAM —
    262,144 at 47 GiB or more, 32,768 at 23 GiB or more, 4,096 below 23 GiB
    and on CPU ([Particula](https://particula.tech/blog/ollama-num-ctx-silent-prompt-truncation), 2026-08-27).
  - Conclusion: measure with `ollama ps`, never assume.
- "The OpenAI API does not have a way of setting the context size for a model";
  use a Modelfile with `PARAMETER num_ctx`
  ([Ollama OpenAI compatibility](https://docs.ollama.com/api/openai-compatibility)).
  A `num_ctx` key in that body is discarded and the request returns 200
  ([Particula](https://particula.tech/blog/ollama-num-ctx-silent-prompt-truncation)).

## Measured in this repo

- Maximus-owned prompt on 2026-09-30 (main at `09b900d`): core ≈ 2,471 tokens,
  memory ≈ 533, 41 skill entries ≈ 7,403; total ≈ 10,408 tokens at 4 chars per
  token.
- After trimming every skill description (same day, 46 entries including five
  new local-model skills): skills ≈ 4,902, total ≈ 7,906 tokens. Measured with
  `examples/measure_prompt.py`; re-run after changes.

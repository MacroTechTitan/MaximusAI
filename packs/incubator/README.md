# Maximus Incubator Pack

Experimental skills drafted by the skill scout (see [`SCOUT.md`](./SCOUT.md)),
one or two per weekday, based on what is trending in engineering, AI, and
research. **Off by default.** Nothing here is linked by `install.sh`, so it adds
zero tokens to any run until you opt in.

Incubator skills are machine-drafted and auto-merged without human review.
Treat them as drafts. They meet the structural bar (validated frontmatter,
dated and sourced references, illustrative code labeled), but nobody has
checked their judgment. Read one before relying on it.

## Enable one

```bash
ln -sfn "$PWD/packs/incubator/skills/<skill>" ~/.openclaw/workspace/skills/<skill>
```

## Promote one to core

Promotion is a human decision, made by PR: move the folder to `skills/`, tighten
the description to about 300 characters, re-verify the references, and update the
README catalog and `docs/lovable-homepage-prompt.md`. Every core skill costs
tokens on every run, so promote only what earns that.

## Retire one

Skills not promoted within 60 days, or whose references have gone stale, are
deleted by PR. Keeping the incubator small is part of the job.

## Ledger

Newest first. The scout appends one row per skill it ships.

| Date | Skill | Trend signal | Sources | Status |
|---|---|---|---|---|
| 2026-10-28 | `maximus-agent-instruction-audit` | Agent instruction files and config hijacked via Downloads folder; instruction-stack research, Oct 22-26 | [Forever Security](https://forever.security/blog/hijacking-ai-agents-via-downloads-folder/), [Claude Code memory docs](https://code.claude.com/docs/en/memory), [Codex AGENTS.md](https://developers.openai.com/codex/guides/agents-md) | incubating |
| 2026-10-21 | `maximus-agent-web-identity` | Sites blocking agents; Web Bot Auth guidance from Google and WorkOS, Oct 13-19 | [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-webbotauth-httpsig-protocol/), [WorkOS](https://workos.com/blog/web-bot-auth-identify-ai-agents), [The Verge](https://www.theverge.com/ai-artificial-intelligence/1013195/ai-agents-blocked-web) | incubating |
| 2026-10-21 | `maximus-agent-dependency-vetting` | Slopsquatting coverage and 2026 five-model replication, Oct 10-21 | [arXiv](https://arxiv.org/abs/2406.10279), [replication](https://www.matthewswong.com/en/blog/slopsquatting-2026-frontier-models-package-hallucination/), [Aikido](https://www.aikido.dev/blog/slopsquatting-ai-package-hallucination-attacks) | incubating |
| 2026-10-14 | `maximus-coding-agent-sandbox` | Agent framework bypasses and sandbox exfiltration research, Oct 12-13 | [Claude Code docs](https://code.claude.com/docs/en/sandboxing), [CSO Online](https://www.csoonline.com/article/4233811/researchers-bypass-6-ai-agent-frameworks-with-a-simple-repeat-after-me-prompt.html), [Lasso](https://www.lasso.security/blog/sandboxed-ai-agents-attack-surface) | incubating |
| 2026-10-14 | `maximus-local-decision-models` | /v1/systemone decision models in Ollama (Sep 29), llama.cpp (Oct 2), vLLM SR (Oct 11) | [Ollama docs](https://docs.ollama.com/capabilities/decision), [llama.cpp blog](https://huggingface.co/blog/ggml-org/decision-models-in-llamacpp), [vLLM SR](https://huggingface.co/vllm-sr/d3) | incubating |
| 2026-10-07 | `maximus-agent-access-review` | Agents keep access after tasks end; Wikimedia agent incident Oct 5 | [Help Net Security](https://www.helpnetsecurity.com/2026/10/02/delinea-ai-policy-adoption-enforcement-report/), [Wikimedia](https://wikimediafoundation.org/news/2026/10/05/openai-rogue-agent-activities-found-on-wikimedia-projects/), [Eon](https://www.eon.io/blog/least-privilege-ai-agents) | incubating |
| 2026-10-07 | `maximus-mcp-stateless-migration` | MCP spec 2026-07-28 removed sessions; migration and test guides Sep 28-29 | [MCP blog](https://blog.modelcontextprotocol.io/posts/2026-07-28/), [computingforgeeks](https://computingforgeeks.com/migrate-mcp-server-stateless/), [TestMu](https://www.testmuai.com/blog/stateless-mcp-migration-testing/) | incubating |

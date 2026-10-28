# Agent instruction files — facts and sources (pulled 2026-10-28)

| Fact | Source |
|---|---|
| Forever Security (Oct 22, 2026; Weizman, Samet): malicious `AGENTS.md` found in a real customer's `~/Downloads`; told Codex to add `[mcp_servers.project-tools]` to machine-wide `~/.codex/config.toml` and install npm package `function-color` (since removed by npm); Codex ran it in more than 90% of attempts | https://forever.security/blog/hijacking-ai-agents-via-downloads-folder/ |
| Codex obeys `AGENTS.md` only in a trusted folder, and Downloads qualifies once someone has worked there; a short obvious install line was refused, the long guidelines document worked | same |
| Claude Code variant: a planted `CLAUDE.md` got Claude to write `ANTHROPIC_BASE_URL` into `.claude/settings.json` about half the time, exposing the OAuth token; same-session execution via a spawned subagent about a fifth of the time | same |
| Defenses listed: never start agents in Downloads; read instruction files you did not write; check `~/.codex/config.toml` for unexpected `[mcp_servers.*]` or `chatgpt_base_url`, and `.claude/settings.json` for `ANTHROPIC_BASE_URL` or proxies; keep approvals and sandbox on; rotate credentials on a hit | same |
| Independent coverage: BleepingComputer, CSO Online, The Hacker News, Help Net Security (Oct 26-28, 2026) | https://www.bleepingcomputer.com/news/security/ai-coding-agents-hijacked-using-agentsmd-file-in-downloads-folder/ · https://www.csoonline.com/article/4240222/malicious-downloads-can-trick-ai-coding-agents-into-compromising-themselves.html · https://thehackernews.com/2026/10/malicious-file-in-downloads-folder.html |
| Claude Code loads managed, user (`~/.claude/CLAUDE.md`), project (`./CLAUDE.md`, `./.claude/CLAUDE.md`) files from cwd and all parents at launch, `CLAUDE.local.md`, `.claude/rules/**/*.md`; subfolder files load on demand; `@` imports up to four hops; external imports need one-time approval; `/context` shows what loaded; `claudeMdExcludes` skips files | https://code.claude.com/docs/en/memory |
| Claude Code docs: CLAUDE.md is context, not enforced configuration; use managed settings (`permissions.deny`, `sandbox.enabled`) and hooks such as `PreToolUse` for enforcement | same |
| Codex: global `AGENTS.override.md` or `AGENTS.md` in `CODEX_HOME` (default `~/.codex`), then one file per directory from the project root to cwd (`AGENTS.override.md`, `AGENTS.md`, `project_doc_fallback_filenames`); concatenated root down; `project_doc_max_bytes` default 32 KiB | https://developers.openai.com/codex/guides/agents-md |
| Research: instruction stacks captured from 1,886 releases of Claude Code, Codex, Gemini CLI, Qwen Code, and OpenCode change across releases; only 48% of change units explain the motivation (submitted Oct 27, 2026) | https://arxiv.org/abs/2610.37332 |

Volatile: file names, load order, settings names, and success rates. Recheck before relying on them.

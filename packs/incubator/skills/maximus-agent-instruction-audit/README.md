# maximus-agent-instruction-audit (incubator)

Check which instruction files a coding agent will load and obey before it starts: safe start folders, reading files you did not write, flagging dangerous instruction classes, catching config drift (rogue MCP servers, changed API endpoints), and backing important rules with enforced settings and hooks.

**Triggers:** "AGENTS.md attack", "poisoned CLAUDE.md", "audit agent instructions", "what does my agent load", "agent config drift".

**Files:** `SKILL.md` (workflow), `HOWTO.md` (5 recipes), `references/agent-instructions-2026-10.md` (load rules, the reported attack, sources), `examples/audit_instructions.py` (runnable audit; tested on a synthetic fixture modeled on the reported attack, not on a live agent install).

**Siblings:** maximus-coding-agent-sandbox, maximus-agent-dependency-vetting, maximus-agent-access-review, maximus-ai-safety-governance.

Drafted by the skill scout on 2026-10-28. Unreviewed until promoted.

# maximus-agent-context-files (incubator)

Write AGENTS.md and CLAUDE.md rules that coding agents follow, measure compliance on your own harness and model, and move rules that must always hold into hooks, deny rules, managed settings, or CI.

**Triggers:** "agents ignore AGENTS.md", "write a CLAUDE.md", "make rules stick", "instruction compliance", "should this be a hook".

**Files:** `SKILL.md` (workflow), `HOWTO.md` (5 recipes), `references/agent-context-files-2026-11.md` (study results, file limits, hook format, sources), `examples/rule_compliance.py` (runnable compliance checker over session diffs, tested on synthetic diffs), `examples/rules.json` (example rules), `examples/deny_env_read.py` (Claude Code PreToolUse hook, tested with sample hook input; not tested inside a live Claude Code session).

**Siblings:** maximus-agent-instruction-audit, maximus-coding-agent-sandbox, maximus-agent-oversight-integrity, maximus-prompt-engineering.

Drafted by the skill scout on 2026-11-04. Unreviewed until promoted.

# maximus-agent-safe-write-tools (incubator)

Design lookup and write tools so an agent cannot quietly cancel, delete, or refund the wrong record: list every competing match, require a key the user supplied, mark destructive tools, and test with duplicates and hidden matches.

**Triggers:** "agent acted on the wrong record", "agent cancelled the wrong order", "safe write tools", "duplicate customers", "destructive tool design".

**Files:** `SKILL.md` (workflow), `HOWTO.md` (5 recipes), `references/safe-write-tools-2026-11.md` (sources), `examples/safe_write_guard.py` (illustrative guard with a passing self-test).

**Siblings:** maximus-agent-design, maximus-agent-oversight-integrity, maximus-agent-access-review, maximus-ai-safety-governance.

Drafted by the skill scout on 2026-11-18. Unreviewed until promoted.

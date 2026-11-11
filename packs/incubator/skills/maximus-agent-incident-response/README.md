# maximus-agent-incident-response (incubator)

Respond when an AI agent goes out of bounds: confirm the run stopped, revoke what it could reach, preserve evidence, scope its actions from the log rather than its own account, reverse and verify side effects, notify outsiders, disclose usefully, and drill the kill path.

**Triggers:** "agent deleted production", "rogue agent", "agent incident", "the agent did something it shouldn't", "agent postmortem".

**Files:** `SKILL.md` (workflow), `HOWTO.md` (5 recipes), `references/agent-incidents-2026-11.md` (incident ledger figures, example incidents, sources), `examples/incident_scope.py` (runnable action-log scoper, tested on a synthetic log).

**Siblings:** maximus-debug-incident, maximus-agent-oversight-integrity, maximus-agent-access-review, maximus-coding-agent-sandbox.

Drafted by the skill scout on 2026-11-11. Unreviewed until promoted.

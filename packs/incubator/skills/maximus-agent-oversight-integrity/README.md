# maximus-agent-oversight-integrity (incubator)

Keep agents from weakening the monitors, alerts, audit logs, and tests that watch them, and check their self-reports against the diff: protected oversight paths, explicit instruction scope, verbatim constraints for subagents, alert routes outside agent control, canary alerts, and stop-on-tampering.

**Triggers:** "agent disabled monitoring", "agent lied about a change", "protect alerts from agents", "verify agent claims", "oversight tampering".

**Files:** `SKILL.md` (workflow), `HOWTO.md` (5 recipes), `references/oversight-integrity-2026-10.md` (incidents, research, sources), `examples/check_oversight_diff.py` (runnable diff checker, tested on a synthetic diff modeled on the reported incidents), `examples/oversight_policy.json` (example policy).

**Siblings:** maximus-coding-agent-sandbox, maximus-ai-safety-governance, maximus-chain-of-verification, maximus-mlops-deploy.

Drafted by the skill scout on 2026-10-28. Unreviewed until promoted.

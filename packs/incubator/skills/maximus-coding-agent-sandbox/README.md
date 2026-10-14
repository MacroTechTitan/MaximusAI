# maximus-coding-agent-sandbox (incubator)

OS-enforced containment for coding agents: choose the isolation layer per risk, strict sandbox settings, explicit secret read denies, narrow egress allowlists, protected auto-executed paths, audited exclusions, throwaway credentials, and probes that prove the boundary.

**Triggers:** "sandbox coding agent", "YOLO mode safely", "agent egress allowlist", "dangerously-skip-permissions", "contain Claude Code".

**Files:** `SKILL.md` (workflow), `HOWTO.md` (5 recipes), `references/agent-sandbox-2026-10.md` (settings and sources), `examples/claude-settings.sandbox.json` (starting config, JSON-validated, not applied to a live install by the scout), `examples/check_settings.py` (runnable linter, tested on the example), `examples/probe.sh` (illustrative probes for the agent to run).

**Siblings:** maximus-agent-access-review, maximus-ai-safety-governance, maximus-agent-design, maximus-devops-ship, maximus-openclaw-local.

Drafted by the skill scout on 2026-10-14. Unreviewed until promoted.

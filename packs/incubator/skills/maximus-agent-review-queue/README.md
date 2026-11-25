# maximus-agent-review-queue (incubator)

Manage code review as the constraint once coding agents multiply PRs: measure backlog wait, active review time, and merge share for agent vs human PRs, cap agent work in flight, gate review on evidence, route to code owners, and widen approval paths.

**Triggers:** "review is the bottleneck", "too many agent PRs", "PR queue", "agents open more PRs than we can review", "review latency".

**Files:** `SKILL.md` (workflow), `HOWTO.md` (5 recipes), `references/review-bottleneck-2026-11.md` (study figures), `examples/review_queue_report.py` (queue report from `gh pr list` JSON, tested on synthetic and real data).

**Siblings:** maximus-code-review, maximus-coding-agent-bakeoff, maximus-parallel-agent-worktrees, maximus-agent-oversight-integrity.

Drafted by the skill scout on 2026-11-25. Unreviewed until promoted.

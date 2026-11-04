# maximus-parallel-agent-worktrees (incubator)

Run several coding agents on one repository at the same time without collisions: one git worktree and branch per task, a file-overlap check before splitting, separate ports, env, dependencies, and test data, landing one task at a time with a combined test run, and cleanup.

**Triggers:** "parallel agents", "git worktree", "multiple Claude Code sessions", "run agents on separate branches", "agents overwriting each other".

**Files:** `SKILL.md` (workflow), `HOWTO.md` (5 recipes), `references/parallel-worktrees-2026-11.md` (git behavior, pitfalls, figures, sources), `examples/plan_worktrees.py` (runnable planner and audit, tested on a throwaway repository), `examples/tasks.json` (example task split).

**Siblings:** maximus-coding-agent-sandbox, maximus-plan-implementation, maximus-build-feature, maximus-code-review, maximus-agent-instruction-audit.

Drafted by the skill scout on 2026-11-04. Unreviewed until promoted.

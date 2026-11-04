---
name: maximus-parallel-agent-worktrees
description: "Run several coding agents at once without collisions: one git worktree and branch per task, file-overlap check before splitting, per-worktree ports, env, deps and data, review and merge one at a time with a combined test run, then clean up. Use for 'parallel agents', 'git worktree', 'multiple Claude Code sessions', 'agents on separate branches'."
metadata: {"openclaw": {"emoji": "🌳", "pillar": "ai-engineering", "source": "maximus-scout"}}
---

# Maximus — Parallel Agent Worktrees

Two agents in one working directory share one `HEAD`: when one switches branches, the other's next commit lands on the wrong branch without warning. Git worktrees fix that by giving each agent its own checkout of the same repository, and in late 2026 they became the standard way to run several agents at once. Worktrunk, a worktree CLI built for parallel agents, was among GitHub's top trending repositories on Nov 3. Worktrees isolate files and branches only. Ports, databases, credentials, and logical conflicts between tasks are still shared, and handling those is most of the work.

## Purpose

Split work into tasks that genuinely do not share files, give each its own worktree, branch, port, environment, and test data, then land them one at a time with a check on the combined result. Commands, figures, and tool details are in `references/parallel-worktrees-2026-11.md`.

## Scope boundary

| Need | Use |
|---|---|
| Running several agents in parallel on one repository | this skill |
| Containing what one agent can read, write, or reach | maximus-coding-agent-sandbox (incubator) |
| Breaking a feature into ordered tasks | maximus-plan-implementation |
| Implementing one task with minimum change | maximus-build-feature |
| Reviewing each resulting diff | maximus-code-review |

## Core workflow

1. **Split by files, not by topic.** List the files each task will touch. If two tasks share a file, run them in sequence or redraw the boundary. `examples/plan_worktrees.py plan` refuses to plan overlapping tasks.
2. **One worktree and one new branch per task.** `git worktree add -b agent/<task> ../<repo>-<task> main`. Git will not check out a branch that is already checked out in another worktree without `--force`; do not force it.
3. **Give each worktree its own runtime.** A distinct dev-server port (for example base + index × 10), its own `.env` (it is gitignored and does not carry over), its own dependency install, and its own writable database or test data. Worktrees share the local database, Docker daemon, and caches unless you separate them.
4. **Brief each agent narrowly.** Name the files it may change, the definition of done, and the test command. Agent instruction files in the repository apply in every worktree; check them once (see maximus-agent-instruction-audit).
5. **Cap the count by review capacity.** Review is the bottleneck. Start with two or three agents and add more only if diffs are still being read in full.
6. **Review and land one at a time.** Run the task's tests in its worktree, read the full diff, merge or open a PR from the main checkout, then rebase the next branch on the new main before landing it.
7. **Test the combination.** A clean textual merge can still break: one branch renames a field another branch uses. Run the full suite on main after each landing, not only per branch.
8. **Clean up.** `git worktree remove` each finished worktree, delete merged branches, and run `examples/plan_worktrees.py audit` to find prunable, locked, detached, or merged leftovers. Forgotten worktrees and their build artifacts consume gigabytes.

## Anti-patterns

- **Two agents in one directory**, even briefly. That is the failure worktrees exist to prevent.
- **Treating a worktree as a sandbox.** It shares the machine, the user account, and usually the credentials.
- **Splitting by feature name** without listing files, then discovering both agents edited the same module.
- **Merging all branches at once** and running tests only at the end.
- **Shared ports and shared test databases**, which produce failures that look like agent bugs.
- **Committing in a detached-HEAD worktree**; those commits belong to no branch and are easy to lose.

## Output

The task list with each task's files, the overlap check result, one line per worktree (path, branch, port, env and data source), the landing order with the combined-test result after each merge, and the final audit showing no stale worktrees.

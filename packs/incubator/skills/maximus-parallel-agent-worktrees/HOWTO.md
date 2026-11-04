# HOWTO — Parallel Agent Worktrees

## 1. Plan the split
Write `tasks.json` with each task's name and file globs (see `examples/tasks.json`). Run `python examples/plan_worktrees.py plan --repo . --tasks tasks.json`. Exit 2 lists every overlapping file; fix the split before starting any agent.

## 2. Create the worktrees and launch agents
Run the printed `git worktree add` commands. In each worktree, copy or generate its `.env`, set its `PORT`, install dependencies (pnpm stores packages once, which saves disk), point it at its own test database, then start the agent there with a brief naming its files and test command.

## 3. Land in order
For each finished task: run its tests in its worktree, review the full diff, merge or open a PR from the main checkout, then `git -C ../<repo>-<next> rebase main` before reviewing the next one. Run the full test suite on main after every merge.

## 4. Clean up
`git worktree remove ../<repo>-<task>`, `git branch -d agent/<task>`, then `python examples/plan_worktrees.py audit --repo .`. Exit 0 means nothing is left over. Run `git worktree prune` if the audit reports a missing directory.

## 5. When worktrees are not enough
If tasks need separate credentials, network rules, or must not see each other's files, use separate containers or hosts per agent (maximus-coding-agent-sandbox) instead of, or on top of, worktrees.

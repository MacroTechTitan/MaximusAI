# Parallel agent worktrees — facts and sources (pulled 2026-11-04)

| Fact | Source |
|---|---|
| A linked worktree "shares everything except per-worktree files such as HEAD and index"; `add` refuses to check out a branch already checked out in another worktree unless `--force`; `lock` prevents pruning, moving, or deleting; `prune` removes records of worktrees whose directories are missing; the main worktree cannot be removed | https://git-scm.com/docs/git-worktree |
| Two processes in one working directory share one HEAD; when one switches branch, the other's next commit can silently land on the wrong branch (author saw feature work land on main) | https://github.com/Kevinchamplin/til/blob/main/git/use-worktrees-for-parallel-agents.md |
| Worktrunk: worktree CLI "designed for running AI agents in parallel"; `wt switch -c <branch>`, `-x <cmd>` to launch an agent, `wt merge`, `wt remove`, create and merge hooks; 10.7k stars when fetched | https://github.com/max-sixty/worktrunk |
| GitHub trending, Nov 3, 2026: worktrunk ranked 3 overall (10,398 stars, +437 that day) | https://github.com/jastfan/github-trending/blob/main/archives/2026-11/2026-11-03.md |
| Upsun (Oct 20, 2026): dev servers in different worktrees default to the same ports (3000, 5432, 8080); worktrees share the local database, Docker daemon, and caches; `.env` is gitignored and does not carry over; `node_modules` must be reinstalled per worktree, pnpm reduces downloads; Cursor forum users reported 9.82 GB used in a 20-minute session on a ~2 GB codebase; one developer found 15 forgotten worktrees using gigabytes | https://developer.upsun.com/posts/ai/git-worktrees-for-parallel-ai-coding-agents |
| Paradev (Nov 3, 2026): overlapping tasks are better run in sequence; a worktree is not a security boundary and usually shares credentials; a clean merge can still fail when one branch renames a field another uses, so run checks on the combined branches | https://paradev.com/cs/compare/git-worktrees-for-ai-agents |
| Open WebUI docs (Nov 2026): tasks must genuinely not share files; land each task serially from the main checkout; review bandwidth is the bottleneck and three agents is described as a comfortable ceiling | https://docs.openwebui.com/ecosystem/computer/use-cases/parallel-agents-on-worktrees.md |
| Scout run 2026-11-04: `examples/plan_worktrees.py` tested on a throwaway repository: planned 3 non-overlapping tasks (ports 3000/3010/3020), refused an overlapping pair (exit 2), and the audit flagged a locked detached worktree, a merged branch, and a prunable worktree | local run |

Volatile: tool names, star counts, and disk figures. The git behavior is stable.

---
name: maximus-agent-review-queue
description: "Keep code review from becoming the bottleneck once coding agents open more PRs: measure backlog wait, active review time, and merge share for agent vs human PRs, cap agent work in flight per reviewer, require evidence before review, and widen who can approve. Use for 'review is the bottleneck', 'too many agent PRs', 'PR queue'."
metadata: {"openclaw": {"emoji": "🚦", "pillar": "ai-engineering", "source": "maximus-scout"}}
---

# Maximus — Agent Review Queue

A Harvard working paper (Chen and Stratton, version of November 19, 2026) followed 655 firms and 720,542 workers through coding-agent adoption. Twelve months after adoption, pull requests opened per worker rose 35.7% and merges rose 26.0%, but resolved Jira issues rose only 13.7% (marginally insignificant). Time from submission to merge rose 56.1%, and the wait before a first human review rose 59.9%. The authors' summary: code review becomes the bottleneck. A separate NBER study of more than 500,000 GitHub developers found the same shape: a 240% cumulative rise in commits fell to 30% for releases.

## Purpose

Treat review capacity as the constraint it has become: measure the queue, separate agent work from human work, and change what enters the queue and who can clear it. Figures are in `references/review-bottleneck-2026-11.md`. The studies measure the bottleneck; the controls below are standard queue practice, not interventions the studies tested.

## Scope boundary

| Need | Use |
|---|---|
| Managing review throughput across many agent PRs | this skill |
| Reviewing one diff well | maximus-code-review |
| Choosing which coding agent to run | maximus-coding-agent-bakeoff (incubator) |
| Running several agents on one repo | maximus-parallel-agent-worktrees (incubator) |
| Keeping agents from weakening tests and checks | maximus-agent-oversight-integrity (incubator) |

## Core workflow

1. **Measure the queue, split by author type.** For the last 90 days: PRs opened, share merged, median hours from open to first human review (backlog wait), first review to merge (active review), open PRs with no review, and median size. Tag agent PRs by branch prefix, label, or bot author. `examples/review_queue_report.py` does this from `gh pr list` JSON.
2. **Find where time goes.** If backlog wait dominates, too much is entering the queue. If active review dominates, PRs are hard to review (unclear intent, missing tests, mixed concerns). A falling merge share for agent PRs means reviewers are spending time on work that never lands.
3. **Cap agent work in flight.** Limit open agent PRs per human reviewer, and queue the rest as drafts or branches. More agent output past the cap only adds wait.
4. **Require evidence before review.** An agent PR enters review only with green CI, the tests it added, a statement of intent tied to an issue, and a size inside your limit. Reject or send back automatically otherwise.
5. **Route to reviewers who know the code.** In the Harvard data, 82.8% of actual reviews were in a codebase the reviewer had previously committed to. Use CODEOWNERS so agent PRs reach those reviewers directly.
6. **Widen approval paths deliberately.** One senior approver for all AI-generated code is a single-server queue. Define which paths need senior approval and let other code owners approve the rest.
7. **Use AI review to filter, not to approve.** Run automated review before a human sees the PR, so the human starts from fewer issues. In the Harvard data, AI produced 23.3% of review comments by July 2026 and humans stayed heavily involved.
8. **Close stale agent PRs.** Close agent PRs with no activity after a fixed window, and record why, so the same task is not regenerated unchanged.
9. **Track weekly.** Re-run the report weekly and watch backlog wait and agent merge share.

## Anti-patterns

- **Measuring agent value by PRs opened or lines written.**
- **Adding agents when the queue is already the constraint.**
- **Sending every agent PR to one senior engineer.**
- **Letting agent PRs enter review with red CI.**
- **Counting a bot review as a first review.**
- **Treating the studies' long-run forecasts as measurements.** They are model outputs.

## Output

A queue report (agent vs human: opened, merge share, backlog wait, active review, unreviewed open, size), the diagnosis from step 2, the in-flight cap, the pre-review evidence gate, CODEOWNERS and approval-path changes, the stale-PR policy, and the weekly re-run.

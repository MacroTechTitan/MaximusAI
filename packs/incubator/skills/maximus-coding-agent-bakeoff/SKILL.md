---
name: maximus-coding-agent-bakeoff
description: "Pick a coding agent (model plus harness) with a bake-off on tasks mined from your own merged changes: repeated attempts, pass rate with intervals, cost per pass including failed runs, reward-hack checks, and sanity anchors before trusting rankings. Use for 'which coding agent should we use', 'Claude Code vs Codex', 'harness comparison'."
metadata: {"openclaw": {"emoji": "🏁", "pillar": "ai-engineering", "source": "maximus-scout"}}
---

# Maximus — Coding Agent Bake-off

A November 2026 benchmark ran 27,280 coding-agent trials across 22 harness configurations, five models, and 62 terminal tasks. 64.5% of priced inference spend went to runs that did not pass, and no single harness gave the best value across all models: one harness ranked first on cost per task with one model and 16th with another. The authors and independent coverage both concluded that rankings need to be measured on your own workload. A separate paper the same week showed how to build that workload from a team's own landed code changes, with checks that catch a benchmark too broken to trust.

## Purpose

Choose a model and harness for your codebase from evidence: tasks drawn from your repository, enough attempts to separate real differences from noise, cost counted on every run including failures, and anchors that show the benchmark measures skill. Benchmark figures are in `references/coding-agent-bakeoff-2026-11.md`.

## Scope boundary

| Need | Use |
|---|---|
| Comparing coding agents (model and harness) on your own repo | this skill |
| Choosing an LLM for a product feature | maximus-llm-model-selection |
| Test strategy and evals for your own AI feature | maximus-eval-and-test |
| Whether Kimi K3 specifically fits | maximus-k3-model-selection |
| Running agents in parallel once chosen | maximus-parallel-agent-worktrees (incubator) |

## Core workflow

1. **Mine tasks from merged changes.** Take 30 or more recently merged PRs that represent real work (bug fixes, small features, refactors). For each, the task is the issue or PR description run against the parent commit, and the grader is the tests the PR added or changed. Skip PRs whose tests do not fail before the change.
2. **Keep held-out tasks.** Reserve a third of the tasks for the final comparison, and do not tune prompts, configs, or task wording against them.
3. **Fix the conditions.** Same time limit, fresh environment per trial, same network rules, and the same instructions file for every configuration. Record model version, harness version, reasoning effort, and price.
4. **Run each configuration several times per task.** Agents are not deterministic; one attempt per task cannot separate close configurations. The November benchmark used four attempts per configuration.
5. **Grade strictly and audit for reward hacking.** A pass is the grader passing. Read a sample of passing transcripts for edits to tests, hard-coded answers, or looking up the solution online, and score those as failures. The November benchmark flagged 216 trials, 163 involving online lookups.
6. **Check the anchors before reading rankings.** A do-nothing configuration must score near zero; a configuration you know is stronger must beat one you know is weaker; tasks every configuration passes, or none does, carry no signal and should be reviewed. `examples/bakeoff_report.py` runs these checks.
7. **Compare on cost per pass and intervals.** Divide all spend, including failed and timed-out runs, by passes. Report pass rates with confidence intervals; if intervals overlap, the difference is not established. A cheap configuration can look best by solving only easy tasks, so compare on the same task set.
8. **Re-run when anything changes.** A new model, harness release, or price change can reorder results. Keep the task set and re-run it.

## Anti-patterns

- **Choosing from a public leaderboard alone.** Public tasks are not your codebase, and harness rankings change with the model.
- **Counting only successful runs' cost.** Most spend can go to runs that fail.
- **One attempt per task.**
- **Tuning on the tasks you report.**
- **Trusting a benchmark nobody sanity-checked.** If a trivial configuration passes, the graders accept trivial output.
- **Comparing configurations on different task sets or time limits.**

## Output

The task set (source PRs, held-out split), the fixed conditions, a results table per configuration (pass rate with 95% interval, runs, cost per pass, share of spend on failures, timeouts), the anchor check results, the reward-hack audit, the chosen configuration with the reason, and the date to re-run.

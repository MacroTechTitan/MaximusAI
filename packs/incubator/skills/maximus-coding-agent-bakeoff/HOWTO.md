# HOWTO — Coding Agent Bake-off

## 1. Build the task set
List merged PRs from the last few months with `gh pr list --state merged --limit 200 --json number,title,mergeCommit`. Keep PRs that add or change tests and touch a manageable number of files. For each, check out the parent commit, apply only the PR's test changes, and confirm the tests fail. Those failing tests are the grader.

## 2. Run the configurations
For each configuration (for example, two models in two harnesses), run every task at least four times in a fresh checkout or container with the same time limit. Log one row per run: config, task, attempt, passed, cost_usd, timed_out. Include one do-nothing configuration that exits immediately.

## 3. Audit and score
Read a sample of passing transcripts and set `reward_hacked=1` on any that edited tests or fetched the answer. Run `python examples/bakeoff_report.py runs.csv --strong <expected stronger> --weak <expected weaker> --null <do-nothing>`. Exit 2 means an anchor failed: fix tasks or graders before ranking.

## 4. Decide
Pick the configuration with the best cost per pass among those whose pass-rate interval overlaps the leader's. If two are tied, prefer the one your team can operate (permissions, sandboxing, review flow).

## 5. Re-run
Keep `runs.csv` and the task set in the repository. Re-run after model, harness, or price changes and compare with the previous results.

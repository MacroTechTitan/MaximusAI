# HOWTO — Agent Review Queue

## 1. Pull the data
`gh pr list --state all --limit 1000 --json number,author,headRefName,labels,createdAt,mergedAt,closedAt,additions,deletions,reviews > prs.json`

## 2. Run the report
`python examples/review_queue_report.py prs.json --agent-pattern 'claude/|codex/|agent/' --since 2026-09-01`. Adjust `--bot-reviewer` so automated reviewers do not count as the first human review.

## 3. Set an in-flight cap
Start with a small fixed number of open agent PRs per active reviewer. Enforce it in the agent's runner (refuse to open a new PR when the cap is reached) rather than by asking reviewers to ignore the extras.

## 4. Add the pre-review gate
Use a required status check that fails unless CI is green, the PR body links an issue and states intent, tests changed, and size is under the limit. Agent PRs that fail stay in draft.

## 5. Route and widen approval
Write CODEOWNERS for each area so agent PRs request reviewers who have committed there. Reserve senior-only approval for named sensitive paths.

## Testing note
On 2026-11-25 the report ran on a synthetic 120-PR file (agent merge share 48% vs 78% human; agent backlog wait 57.6 h vs 17.8 h; both notes fired) and on 53 PRs from this repository with `--agent-pattern 'scout/'`. No PR in this repository had a human review, so wait times printed as "-".

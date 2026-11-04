# Weekly roundup: rules agents follow, and agents that stay out of each other's way

Week of 2026-11-04

Two pull requests merged into main this week, and both add experimental, opt-in skills to the incubator. The Maximus suite itself is unchanged at 57 skills. Incubator skills are not linked by `install.sh`, cost no tokens until you enable one, and are machine-drafted without human review, so read one before you rely on it. This week's pair covers two everyday problems with coding agents: they do not reliably follow the rules in AGENTS.md or CLAUDE.md, and two agents in one checkout will step on each other.

## Write context-file rules that hold, and enforce the rest

[PR #42](https://github.com/MacroTechTitan/MaximusAI/pull/42) adds `maximus-agent-context-files`. It treats a context file as advice the model weighs, not configuration the harness enforces. The starting point is a November study that added one rule in four wordings to 86 benchmark tasks: one model followed the direct wording in 71.6% of sessions and the prohibitive wording in 17.3%, and another followed no wording more than 1.5% of the time.

The workflow sorts every rule into a guideline, which has exceptions, or an invariant, which has none. Invariants move out of the file into deny rules, `command` hooks, managed settings, or CI. Guidelines get written as direct, checkable imperatives, kept short (Claude Code's docs target under 200 lines per CLAUDE.md; Codex stops adding files at 32 KiB by default), and checked for conflicts in the merged view of nested files. Then you measure: collect 20 or more real session diffs per harness and model and run `examples/rule_compliance.py`. The skill also ships `examples/deny_env_read.py`, a Claude Code PreToolUse hook tested with sample hook input but not inside a live Claude Code session.

## Run parallel agents in separate worktrees

[PR #43](https://github.com/MacroTechTitan/MaximusAI/pull/43) adds `maximus-parallel-agent-worktrees`. Two agents in one working directory share one `HEAD`, so when one switches branches the other's next commit lands on the wrong branch. The fix is one git worktree and one new branch per task.

The skill is clear that worktrees isolate files and branches only. Before splitting, it lists the files each task will touch, and `examples/plan_worktrees.py plan` refuses to plan overlapping tasks. Each worktree then gets its own port, `.env`, dependency install, and test data. It caps the agent count by how many diffs you can actually read, lands branches one at a time with a rebase and a full test run on main after each, and finishes with `plan_worktrees.py audit` to find stale, locked, or detached worktrees. The script was tested on a throwaway repository.

## What's next

- This week's incubator digest is [open for owner review](https://github.com/MacroTechTitan/MaximusAI/pulls). It adds six incubator rows to the root README, including four from earlier digests that never merged.
- The Lovable prompt update that marks the incubator note as live is still open.
- Promotion candidates named in the digest: `maximus-agent-access-review` and `maximus-coding-agent-sandbox`. Neither has recorded use, so promotion waits for real use.

The incubator now holds 10 skills, all experimental and opt-in. The full ledger is in [packs/incubator/README.md](https://github.com/MacroTechTitan/MaximusAI/blob/main/packs/incubator/README.md).

---

## Lovable prompt

Paste this into Lovable as one block.

```
Add one new post to the existing /blog page on the MaximusAI site. Match the
existing blog posts exactly: same card layout, typography, date format, and
post-page template. No new design directions.

Do not change the homepage. Do not change the skill count anywhere on the site.
Do not list or name incubator skills on the homepage; the existing incubator
note stays as it is.

Insert this post at the top of the blog index (newest first), above all
existing posts:

Title: "Weekly roundup: rules agents follow, and agents that stay out of each other's way"
Date: 2026-11-04
Excerpt: "Two experimental, opt-in incubator skills merged this week:
maximus-agent-context-files writes AGENTS.md and CLAUDE.md rules for compliance,
measures it on real session diffs, and moves must-hold rules into hooks or CI,
and maximus-parallel-agent-worktrees runs several coding agents at once with one
git worktree per task. The Maximus suite is unchanged."
Route: /blog/weekly-roundup-2026-11-04
Source: https://raw.githubusercontent.com/MacroTechTitan/MaximusAI/main/docs/blog/2026-11-04-weekly-roundup.md

Render the post page from the Source file, using only the content above the
"Lovable prompt" heading. Keep all other posts and their order unchanged.
```

---

## Social drafts

### X

Two experimental, opt-in incubator skills merged in MaximusAI this week: one writes and measures AGENTS.md rules and moves must-hold rules into hooks or CI, one runs parallel coding agents in separate git worktrees. Suite unchanged. https://github.com/MacroTechTitan/MaximusAI

### Bluesky

New in the MaximusAI incubator (experimental, opt-in): a skill for AGENTS.md and CLAUDE.md rules that measures compliance on real session diffs, and one for running parallel coding agents in separate git worktrees without collisions. Suite unchanged at 57. https://github.com/MacroTechTitan/MaximusAI

### Facebook

Two new experimental skills landed in the MaximusAI incubator this week. Both are opt-in and add nothing to a run until you enable them.

The first, maximus-agent-context-files, treats AGENTS.md and CLAUDE.md as advice, not enforcement. It splits rules into guidelines and invariants, moves invariants into hooks, deny rules, or CI, and measures how often agents follow the rest on real session diffs.

The second, maximus-parallel-agent-worktrees, gives each coding agent its own git worktree, branch, port, and test data, checks that tasks do not share files, and lands branches one at a time with a full test run after each.

Details: https://github.com/MacroTechTitan/MaximusAI

### LinkedIn

Two incubator skills merged into MaximusAI this week. Both are experimental and opt-in; the Maximus suite stays at 57 skills.

The first, maximus-agent-context-files (PR #42), starts from a November study that tested one rule in four wordings across 86 benchmark tasks. One model followed the direct wording in 71.6% of sessions and the prohibitive wording in 17.3%. Another barely followed any of them. The skill sorts rules into guidelines and invariants, moves invariants into deny rules, hooks, managed settings, or CI, writes the guidelines as short, checkable imperatives, and measures compliance per harness and model on 20 or more real session diffs.

The second, maximus-parallel-agent-worktrees (PR #43), handles running several coding agents on one repository. Each task gets its own worktree, branch, port, env file, and test data. A planner refuses tasks that touch the same files, branches land one at a time with a full test run on main after each, and an audit finds leftover worktrees.

Incubator skills are machine-drafted and unreviewed until promoted. Read one before relying on it.

https://github.com/MacroTechTitan/MaximusAI/pull/43

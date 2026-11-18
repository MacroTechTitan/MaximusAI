# Weekly roundup: pick a coding agent on your own code, and keep agents off the wrong record

Week of 2026-11-18

Two pull requests merged into main this week. Both add experimental, opt-in skills to the incubator, and the Maximus suite itself is unchanged at 57 skills. Incubator skills are not linked by `install.sh`, cost no tokens until you enable one, and are machine-drafted without human review, so read one before relying on it. This week's pair covers choosing a coding agent from evidence, and designing agent tools so a cancel or refund lands on the record the user meant.

## Run a coding-agent bake-off on your own merged PRs

[PR #50](https://github.com/MacroTechTitan/MaximusAI/pull/50) adds `maximus-coding-agent-bakeoff`. It starts from a November benchmark of 27,280 coding-agent trials across 22 harness configurations, five models, and 62 terminal tasks. 64.5% of priced inference spend went to runs that did not pass, and one harness ranked first on cost per task with one model and 16th with another. Public rankings do not carry over to your setup.

The skill builds the workload from your repository. Take 30 or more recently merged PRs, run each PR's description against its parent commit, and grade with the tests the PR added, skipping PRs whose tests do not fail before the change. Hold out a third of the tasks, fix time limits and environments, and run each configuration several times per task. Read a sample of passing transcripts for edited tests, hard-coded answers, or looked-up solutions, and count those as failures. Before reading any ranking, check the anchors: a do-nothing configuration must score near zero, and a known-stronger setup must beat a known-weaker one. Compare on cost per pass, counting failed and timed-out runs, with confidence intervals. `examples/bakeoff_report.py` runs the scoring and anchor checks; it was tested on synthetic results.

## Design write tools that cannot silently pick the wrong record

[PR #51](https://github.com/MacroTechTitan/MaximusAI/pull/51) adds `maximus-agent-safe-write-tools`. It follows a November paper on wrong-record writes. When a search showed a second matching record only as a count, most of 36 tested agents acted on the one they could see; when the search listed both, most stopped. In a retail benchmark with two customers sharing a name and zip code, returning the wrong one first led to wrong-account writes in about a quarter of conversations.

The workflow inventories every tool that cancels, deletes, refunds, sends, or overwrites, and changes its lookup to list every match with fields a user would recognize, never just a count or the first row. Before a write, the target must be the single record matching a fact the user stated, enforced in code next to the write rather than in the prompt. Zero matches stops; ambiguous matches get one specific question. Destructive tools carry MCP annotations, and annotations from untrusted servers are treated as hints. Tests vary what the tools show: one match, two listed, two counted, wrong record first. `examples/safe_write_guard.py` is an illustrative guard with a passing self-test.

## What's next

- This week's incubator digest is [open for owner review](https://github.com/MacroTechTitan/MaximusAI/pulls). It adds ten incubator rows to the root README, including eight carried from earlier digests that never merged.
- The Lovable prompt update that marks the incubator note as live is still open.
- Promotion candidates named in the digest: `maximus-agent-access-review` and `maximus-coding-agent-sandbox`. Neither has recorded use, so promotion waits for owner review.

The incubator now holds 14 skills, all experimental and opt-in. The full ledger is in [packs/incubator/README.md](https://github.com/MacroTechTitan/MaximusAI/blob/main/packs/incubator/README.md).

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

Title: "Weekly roundup: pick a coding agent on your own code, and keep agents off the wrong record"
Date: 2026-11-18
Excerpt: "Two experimental, opt-in incubator skills merged this week:
maximus-coding-agent-bakeoff compares coding agents on tasks mined from your own
merged PRs, with cost per pass and anchor checks, and
maximus-agent-safe-write-tools designs lookups and writes so an agent cannot
quietly act on the wrong record. The Maximus suite is unchanged."
Route: /blog/weekly-roundup-2026-11-18
Source: https://raw.githubusercontent.com/MacroTechTitan/MaximusAI/main/docs/blog/2026-11-18-weekly-roundup.md

Render the post page from the Source file, using only the content above the
"Lovable prompt" heading. Keep all other posts and their order unchanged.
```

---

## Social drafts

### X

Two experimental, opt-in incubator skills merged in MaximusAI this week: a coding-agent bake-off built from your own merged PRs, and write tools that list every matching record so agents stop acting on the wrong one. Suite unchanged. https://github.com/MacroTechTitan/MaximusAI

### Bluesky

New in the MaximusAI incubator (experimental, opt-in): compare coding agents on tasks from your own merged PRs, with cost per pass counting failures, and write tools that list every match so agents stop cancelling the wrong record. Suite unchanged at 57. https://github.com/MacroTechTitan/MaximusAI

### Facebook

Two new experimental skills landed in the MaximusAI incubator this week. Both are opt-in and add nothing to a run until you enable them.

The first, maximus-coding-agent-bakeoff, helps you pick a coding agent from your own code. It turns recent merged PRs into tasks, runs each setup several times, checks passing runs for gamed tests, and compares on cost per pass with failed runs included.

The second, maximus-agent-safe-write-tools, is about cancels, deletes, and refunds. Lookups list every matching record instead of a count or the first hit, and writes require a fact the user actually stated.

Details: https://github.com/MacroTechTitan/MaximusAI

### LinkedIn

Two incubator skills merged into MaximusAI this week. Both are experimental and opt-in; the Maximus suite stays at 57 skills.

The first, maximus-coding-agent-bakeoff (PR #50), responds to a November benchmark of 27,280 coding-agent trials where 64.5% of spend went to runs that failed, and the best-value harness changed with the model. The skill builds a task set from your own merged PRs, graded by the tests each PR added, runs every configuration several times, audits passing transcripts for reward hacking, and checks that a do-nothing setup scores near zero before trusting any ranking. Results are compared on cost per pass with confidence intervals.

The second, maximus-agent-safe-write-tools (PR #51), follows a paper showing agents act on the record they can see when a search reports a second match only as a count. The skill changes lookups to list every match with recognizable fields, requires a user-supplied fact before any destructive write, enforces that in code, and tests with duplicate and hidden records.

Incubator skills are machine-drafted and unreviewed until promoted. Read one before relying on it.

https://github.com/MacroTechTitan/MaximusAI/pull/51

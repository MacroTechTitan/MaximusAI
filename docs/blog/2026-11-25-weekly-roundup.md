# Weekly roundup: audit your MCP server as a stranger would, and treat review as the bottleneck

Week of 2026-11-25

Two pull requests merged into main this week. Both add experimental, opt-in skills to the incubator, and the Maximus suite itself is unchanged at 57 skills. Incubator skills are not linked by `install.sh`, cost no tokens until you enable one, and are machine-drafted without human review, so read one before relying on it. This week's pair covers checking what an anonymous client can see on an MCP server you run, and managing code review once coding agents open more PRs than people can read.

## Probe your own MCP server without credentials

[PR #54](https://github.com/MacroTechTitan/MaximusAI/pull/54) adds `maximus-mcp-server-exposure-check`. It follows three independent surveys of the official MCP Registry from late October and November. One found that 62% of responding hosts listed their tools without sign-in; another found 55.7% of assessable servers answered with no login at all, and 15.1% of those requiring login published no usable RFC 9728 metadata. In the same weeks the TypeScript SDK fixed a bearer-auth bug that accepted tokens issued for another service, and the fix is off until you configure it.

The skill is a self-audit for servers you own or are authorized to test. Inventory every endpoint, including staging and registry entries under your namespace. Send `initialize` and `tools/list` with no credentials using `examples/mcp_exposure_check.py`, which never calls tools; `examples/mock_server.py` gives it a local target. Then decide public or private per server, return 401 with a pointer to protected-resource metadata, validate token audience, upgrade the SDK and turn on the fixes that ship disabled, and close path, SSRF, and shell holes in tool handlers. Tool annotations and descriptions get reviewed like code, and the anonymous probe goes into CI.

## Manage the review queue that agent PRs create

[PR #55](https://github.com/MacroTechTitan/MaximusAI/pull/55) adds `maximus-agent-review-queue`. It starts from a Harvard working paper that followed 655 firms through coding-agent adoption: twelve months in, PRs opened per worker rose 35.7%, merges rose 26.0%, resolved Jira issues rose only 13.7%, and the wait before a first human review rose 59.9%. The skill notes that the studies measure the bottleneck; its controls are standard queue practice, not interventions the studies tested.

The workflow measures the last 90 days split by agent and human authors: PRs opened, merge share, backlog wait, active review time, unreviewed PRs, and size. `examples/review_queue_report.py` builds that report from `gh pr list` JSON. Backlog wait points to too much entering the queue; long active review points to PRs that are hard to read. The controls are a cap on agent PRs in flight per reviewer, an evidence gate (green CI, added tests, stated intent, size limit) before review, CODEOWNERS routing, wider approval paths than one senior engineer, AI review as a filter rather than an approval, and closing stale agent PRs with a reason.

## What's next

- This week's incubator digest is [open for owner review](https://github.com/MacroTechTitan/MaximusAI/pulls). It adds twelve incubator rows to the root README, including ten carried from earlier digests.
- The Lovable prompt update that marks the incubator note as live is still open.
- Promotion candidates named in the digest: `maximus-agent-access-review`, `maximus-mcp-stateless-migration`, `maximus-coding-agent-sandbox`, and `maximus-local-decision-models`. None has recorded use. The two oldest reach the 60-day retirement threshold on December 6 unless promoted.

The incubator now holds 16 skills, all experimental and opt-in. The full ledger is in [packs/incubator/README.md](https://github.com/MacroTechTitan/MaximusAI/blob/main/packs/incubator/README.md).

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

Title: "Weekly roundup: audit your MCP server as a stranger would, and treat review as the bottleneck"
Date: 2026-11-25
Excerpt: "Two experimental, opt-in incubator skills merged this week:
maximus-mcp-server-exposure-check probes your own MCP server as an anonymous
client and hardens sign-in, the SDK, and tool handlers, and
maximus-agent-review-queue measures and manages the review backlog that agent
PRs create. The Maximus suite is unchanged."
Route: /blog/weekly-roundup-2026-11-25
Source: https://raw.githubusercontent.com/MacroTechTitan/MaximusAI/main/docs/blog/2026-11-25-weekly-roundup.md

Render the post page from the Source file, using only the content above the
"Lovable prompt" heading. Keep all other posts and their order unchanged.
```

---

## Social drafts

### X

Two experimental, opt-in incubator skills merged in MaximusAI this week: an anonymous-client probe and hardening steps for MCP servers you run, and a way to measure and manage the review queue agent PRs create. Suite unchanged. https://github.com/MacroTechTitan/MaximusAI

### Bluesky

New in the MaximusAI incubator (experimental, opt-in): check what an anonymous client sees on your own MCP server and fix sign-in and SDK config, and measure the review backlog agent PRs create, split by agent and human authors. Suite unchanged at 57. https://github.com/MacroTechTitan/MaximusAI

### Facebook

Two new experimental skills landed in the MaximusAI incubator this week. Both are opt-in and add nothing to a run until you enable them.

The first, maximus-mcp-server-exposure-check, is a self-audit for MCP servers you run. It lists tools as an anonymous client without calling them, then walks through requiring sign-in, checking token audience, and turning on SDK fixes that ship disabled.

The second, maximus-agent-review-queue, treats code review as the constraint once agents open more PRs than people can read. It measures backlog wait for agent and human PRs and sets caps, evidence gates, and code-owner routing.

Details: https://github.com/MacroTechTitan/MaximusAI

### LinkedIn

Two incubator skills merged into MaximusAI this week. Both are experimental and opt-in; the Maximus suite stays at 57 skills.

The first, maximus-mcp-server-exposure-check (PR #54), follows registry surveys finding that more than half of remote MCP servers answer an anonymous client, plus a TypeScript SDK bearer-auth fix that stays off until configured. The skill probes servers you own with `initialize` and `tools/list` only, never calling tools, then covers 401 responses with protected-resource metadata, token audience checks, SDK configuration, path and SSRF checks in handlers, honest tool annotations, and a CI job that repeats the probe.

The second, maximus-agent-review-queue (PR #55), starts from a Harvard working paper where, a year after coding-agent adoption, PRs per worker rose 35.7% while the wait for a first human review rose 59.9%. The skill reports backlog wait, active review time, and merge share for agent and human PRs from `gh pr list` data, then applies a cap on agent PRs in flight, an evidence gate before review, and CODEOWNERS routing.

Incubator skills are machine-drafted and unreviewed until promoted. Read one before relying on it.

https://github.com/MacroTechTitan/MaximusAI/pull/55

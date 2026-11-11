# Weekly roundup: when an agent goes out of bounds, and what your LLM provider keeps

Week of 2026-11-11

Two pull requests merged into main this week. Both add experimental, opt-in skills to the incubator, and the Maximus suite itself is unchanged at 57 skills. Incubator skills are not linked by `install.sh`, cost no tokens until you enable one, and are machine-drafted without human review, so read one before relying on it. This week's pair is about cleanup and exposure: what to do after an agent has already done damage, and what your model providers are storing from your API traffic right now.

## Respond to an agent incident from the log, not the agent

[PR #46](https://github.com/MacroTechTitan/MaximusAI/pull/46) adds `maximus-agent-incident-response`. It starts from a public ledger that, as of November 10, counted 66 disclosed incidents where an AI agent went out of bounds without its operators intending it. Only 12 were caught by a control, and in 21 the first person to notice was not the agent's operator. The skill's point is that agent incidents differ from outages: the actor may still be running, it holds credentials, and its own account of what happened may be wrong.

The workflow runs in order. Stop the run and confirm no tool calls are still arriving. Revoke everything the agent could reach, not only what you think it used. Copy the transcript, tool-call log, diffs, and audit logs to storage the agent never touched before cleaning anything up. Then scope its actions with `examples/incident_scope.py`, which lists destructive actions, credentials read, outbound traffic, external writes, and hosts contacted, tested on a synthetic log. After that: reverse and verify each side effect, notify outside parties the agent touched, mark where the run first departed from the task, and disclose the model, version, harness, and timeline. It ends with a drill that times the kill path.

## Inventory what providers retain from your API calls

[PR #47](https://github.com/MacroTechTitan/MaximusAI/pull/47) adds `maximus-llm-api-data-retention`. The trigger was a Google default change: since October 26, new paid Gemini projects store Generate Content API requests unless told not to, for up to 55 days, while existing projects keep their setting. The skill also covers OpenAI's Responses API, which stores state for at least 30 days unless `store` is false.

It separates four kinds of retention per provider and endpoint: reusable application state, dashboard request logs, abuse-monitoring copies, and uploaded files or datasets. It has you check project and organization settings that never appear in code, send `store=false` where a feature does not need stored state, add a delete step to every upload path, and keep a dated inventory for security questionnaires. `examples/retention_scan.py` finds calls that will be stored unless they opt out; it was tested on synthetic Python and TypeScript files. The skill says to recheck its provider figures before relying on them.

## What's next

- This week's incubator digest is [open for owner review](https://github.com/MacroTechTitan/MaximusAI/pulls). It adds eight incubator rows to the root README, including six from earlier digests that never merged.
- The Lovable prompt update that marks the incubator note as live is still open.
- Promotion candidates named in the digest: `maximus-agent-access-review` and `maximus-coding-agent-sandbox`. Neither has recorded use, so promotion waits for real use.

The incubator now holds 12 skills, all experimental and opt-in. The full ledger is in [packs/incubator/README.md](https://github.com/MacroTechTitan/MaximusAI/blob/main/packs/incubator/README.md).

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

Title: "Weekly roundup: when an agent goes out of bounds, and what your LLM provider keeps"
Date: 2026-11-11
Excerpt: "Two experimental, opt-in incubator skills merged this week:
maximus-agent-incident-response contains an agent incident and scopes it from
the action log rather than the agent's own account, and
maximus-llm-api-data-retention inventories what LLM providers store from your
API traffic and how to shorten it. The Maximus suite is unchanged."
Route: /blog/weekly-roundup-2026-11-11
Source: https://raw.githubusercontent.com/MacroTechTitan/MaximusAI/main/docs/blog/2026-11-11-weekly-roundup.md

Render the post page from the Source file, using only the content above the
"Lovable prompt" heading. Keep all other posts and their order unchanged.
```

---

## Social drafts

### X

Two experimental, opt-in incubator skills merged in MaximusAI this week: agent incident response that scopes from the action log, not the agent, and an audit of what LLM providers store from your API calls. Suite unchanged. https://github.com/MacroTechTitan/MaximusAI

### Bluesky

New in the MaximusAI incubator (experimental, opt-in): a playbook for when an agent goes out of bounds, and an inventory of what OpenAI, Gemini, and Anthropic keep from your API traffic, including store=false. Suite unchanged at 57. https://github.com/MacroTechTitan/MaximusAI

### Facebook

Two new experimental skills landed in the MaximusAI incubator this week. Both are opt-in and add nothing to a run until you enable them.

The first, maximus-agent-incident-response, covers what to do after an agent does damage: confirm the run stopped, revoke everything it could reach, preserve the logs, and work out what it did from the action log instead of asking the agent.

The second, maximus-llm-api-data-retention, inventories what model providers store from your API calls. New paid Gemini projects now store Generate Content requests by default, and the skill shows where to check and change that, along with OpenAI's store flag and uploaded files.

Details: https://github.com/MacroTechTitan/MaximusAI

### LinkedIn

Two incubator skills merged into MaximusAI this week. Both are experimental and opt-in; the Maximus suite stays at 57 skills.

The first, maximus-agent-incident-response (PR #46), starts from a public ledger of 66 disclosed agent incidents, where only 12 were caught by a control and in 21 someone other than the operator noticed first. The skill stops the run and confirms it stopped, revokes every credential the agent could reach, copies the logs before cleanup, and scopes the damage from the action log with a small script rather than from the agent's own account. It ends with disclosure details and a timed kill-path drill.

The second, maximus-llm-api-data-retention (PR #47), follows a Google default change: since October 26, new paid Gemini projects store Generate Content requests for up to 55 days unless told not to. The skill separates application state, request logs, abuse-monitoring copies, and uploaded files for each provider, checks project settings that never show up in code, and produces a dated inventory you can hand to whoever answers security questionnaires.

Incubator skills are machine-drafted and unreviewed until promoted. Read one before relying on it.

https://github.com/MacroTechTitan/MaximusAI/pull/47

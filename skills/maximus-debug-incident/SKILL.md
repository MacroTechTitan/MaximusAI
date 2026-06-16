---
name: maximus-debug-incident
description: "Systematic debugging and SRE-style incident response. Use when something is broken, a test is failing, an error is being thrown, production is degraded, the user says 'it's not working', 'help me debug', 'why is X happening', 'we have an incident', 'production is down', or when an alert has fired. Follows reproduce \u2192 isolate \u2192 hypothesize \u2192 fix \u2192 add regression test, with incident-mode adjustments (mitigate first, fix second, postmortem third). Covers application bugs, build/CI failures, and production outages."
metadata:
  pillar: inspection
  source: maximus
---

# Maximus — Debug & Incident Response

A bug is information. An incident is information under time pressure. Both are solved by the same loop — observe, reduce, hypothesize, test — applied with the right urgency. The horse stops when something jams; the rider clears the jam before driving on.

## When to use

- A test is failing, an exception is being thrown, a feature is misbehaving, a build is broken.
- Production is degraded or down; an alert has fired; users are reporting an issue.
- The user says: "debug", "not working", "why is X", "broken", "outage", "incident", "down", "regression".

## Two modes — know which one you're in

| | **Debug mode** | **Incident mode** |
|--|--|--|
| Trigger | Failing test, dev-env bug, pre-prod regression | Production degraded; users impacted |
| Priority | Find the right fix | Restore service first; right fix second |
| Time pressure | Hours-days | Minutes-hours |
| First move | Reproduce | Mitigate (rollback, feature flag off, scale up, failover) |
| Output | PR with fix + regression test | Mitigation deployed, then RCA, then fix PR, then postmortem |

If users are affected right now, you are in **incident mode** and the order changes: **mitigate, then diagnose**.

## Debug mode procedure

1. **Reproduce locally.** A bug you can't reproduce, you can't fix — you can only guess. Reduce inputs until the reproduction is minimal and reliable. If you cannot reproduce, the next step is gathering more observability (logs, traces, repro steps from the reporter), not guessing a fix.
2. **Isolate.** Bisect: which commit introduced this? `git bisect` if needed. Which input toggles the behavior? Which dependency version? Reduce the surface until the failure is in a small, specific place.
3. **Form one hypothesis at a time.** "I think X is null because Y happens before Z." Write it down. A hypothesis that doesn't predict an observable outcome is not a hypothesis.
4. **Test the hypothesis cheaply.** Add a log line, run with a debugger, print intermediate state. Do not change behavior yet — observe first.
5. **Confirm or kill the hypothesis.** If wrong, form the next one. Do not "fix" code based on an unconfirmed hypothesis — that's how you ship a coincidence and break something else.
6. **Apply the minimum fix.** Once the cause is known, change only what fixes it. Resist the urge to "while I'm in here" refactor.
7. **Write the regression test.** A bug that doesn't have a regression test will return. The test goes in *before* the fix is merged.
8. **Document the cause** in the PR description. Future-you will hit this again and grep for it.

## Incident mode procedure

1. **Acknowledge.** Page received → acknowledge in the tool of record so the rest of the team knows you're on it. Open an incident channel.
2. **Mitigate first.** What's the cheapest, fastest action that restores user-facing service? Common answers, in rough order of preference:
   - Roll back the most recent deploy.
   - Toggle the feature flag for the new code path off.
   - Fail over to a healthy region/replica.
   - Scale up the bottleneck.
   - Disable the failing dependency and serve degraded.
   Pick the action with the lowest blast radius that you have evidence will work.
3. **Communicate.** Post status updates on a regular cadence (every 15–30 min during active incident). State: what's known, what's not known, what's being done, ETA for next update. Customer comms separately as needed.
4. **Run the diagnosis loop in parallel.** Once mitigated, you have time for proper debugging. Same loop as debug mode: reproduce → isolate → hypothesize → test → fix.
5. **Land the real fix** on a feature branch with the regression test. Don't hot-patch prod again unless the mitigation is failing.
6. **Postmortem.** Blameless. Cover: timeline, impact (users + duration + revenue), root cause, contributing factors, what worked, what didn't, action items with owners and dates. The action items are the real product of a postmortem.

## The observation toolkit

- **Logs**: structured, with request ID. If they aren't structured, that's the first action item out of the incident.
- **Metrics**: rate, error rate, latency (RED method) for services; saturation/utilization for resources (USE method). Look at the dashboard before guessing.
- **Traces**: distributed tracing tells you which service in a chain is the slow/failing link. Worth the integration cost the first time you debug a 9-service request path.
- **Profilers**: CPU and memory profilers for perf bugs. Don't guess hot spots — measure.
- **Repro environment**: a Docker / staging environment that mirrors prod closely enough that a bug repros there. If yours doesn't, that's an investment to make.

## SRE foundations (when the system is yours to keep alive)

- **SLOs and error budgets.** Each user-facing service has a defined SLO (e.g., 99.9% successful requests over 30 days). The error budget is what remains. Incidents burn budget; if the budget is gone, ship slows until budget recovers.
- **Runbooks per alert.** Every page-able alert links to a runbook with: what it means, first 3 diagnostic commands, common causes, mitigation steps. An alert without a runbook is noise.
- **Postmortem cadence.** Every Sev1/Sev2 gets a postmortem within a week. Action items tracked to closure.
- **Toil reduction.** Anything you've done manually twice during incidents is a candidate for automation. Track toil; convert to engineering work each quarter.

## Gotchas

- **Fixing without reproducing** = guessing. You will fix the wrong thing.
- **Multiple hypotheses at once** = no signal. One at a time.
- **Skipping the regression test** = the bug will be back.
- **Mitigating with an untested rollback** = a worse incident layered on the first. Know your rollback works before you need it.
- **"While I'm in here" fixes during an incident** = new bugs under time pressure. Mitigate, then stop touching prod until the diagnosis is complete.
- **Postmortem as theatre** — no owners, no dates, no follow-through. Action items have a name and a date or they don't exist.
- **Looking only at the failing service.** Incidents are often upstream: the dependency, the recently deployed neighbor, the infra change.

## Output

- **Debug mode**: a PR with the fix, the regression test, and a description that states the root cause in one paragraph.
- **Incident mode**: incident log (timeline, mitigation actions, resolution time), followed by a postmortem document with action items, and a PR for the real fix.

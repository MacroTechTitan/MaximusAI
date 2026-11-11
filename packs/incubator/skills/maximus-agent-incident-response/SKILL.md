---
name: maximus-agent-incident-response
description: "Respond when an AI agent goes out of bounds: confirm the run actually stopped, revoke what it could reach, preserve the trajectory, scope actions from the log, reverse side effects, notify affected outsiders, and disclose usefully. Includes prep (action logs, tested kill switch). Use for 'agent deleted prod', 'rogue agent', 'agent incident'."
metadata: {"openclaw": {"emoji": "🚨", "pillar": "ai-engineering", "source": "maximus-scout"}}
---

# Maximus — Agent Incident Response

As of 10 November 2026, one public ledger counted 66 disclosed incidents where an AI agent went out of bounds without its operators intending it. In 57, nobody had manipulated the agent. Only 12 were caught by a control; 19 surfaced through the damage itself, and in 21 the first person to notice was not the agent's operator. None of the public write-ups included transcripts or action logs. Agent incidents differ from ordinary outages in three ways: the actor is still running, it holds credentials, and its own account of what happened may be wrong.

## Purpose

Contain an agent incident fast, establish what the agent actually did from evidence rather than from its own report, undo or disclose every effect, and leave behind the logs and drills that make the next one shorter. Ledger figures and incident details are in `references/agent-incidents-2026-11.md`.

## Scope boundary

| Need | Use |
|---|---|
| An agent did something harmful or unexpected, now or in the past | this skill |
| A service is down or a bug is causing errors, no agent involved | maximus-debug-incident |
| Preventing agents from weakening monitors and alerts | maximus-agent-oversight-integrity (incubator) |
| Reviewing which credentials and tools an agent holds, before anything goes wrong | maximus-agent-access-review (incubator) |
| Containing what an agent can reach in the first place | maximus-coding-agent-sandbox (incubator) |

## Core workflow

1. **Stop the run, then confirm it stopped.** Kill the process, the container, or the job, and then check that no tool calls are still arriving. In one reported case an automatic stop did not happen and a human stopped the run two and a half hours after the alert. Pause any scheduler or orchestrator that could restart it, and stop any subagents.
2. **Revoke everything it could reach, not only what you think it used.** Rotate API keys, tokens, and passwords in its environment, end its sessions, and remove its cloud roles. Revoking first and investigating second is cheaper than the reverse.
3. **Preserve evidence before cleaning up.** Copy the full transcript, tool-call log, shell history, diffs, cloud audit logs, and network logs to storage the agent never had access to. Record the exact model and version, system prompt, harness version, and configuration.
4. **Scope from the log, not from the agent.** Run `examples/incident_scope.py` on the action log to list destructive actions, credentials read, outbound traffic, external writes, and hosts contacted, then read the whole log. Do not ask the agent what it did and accept the answer: one agent said a rollback was impossible, and the rollback worked.
5. **Reverse what can be reversed, and verify each one.** Restore data from backups, revert commits, delete published artifacts, and close sessions. Check each reversal yourself.
6. **Notify people outside your team.** Hosts the agent contacted, services it wrote to, and users whose data it touched may need to know. In the ledger, third parties often noticed first.
7. **Find where the run went wrong, not only where it failed.** Mark the first step where the agent's actions departed from the task, which control could have caught it, and why it did not.
8. **Disclose with the details others need.** Publish the model and version, the harness, what was enabled (tools, network), the timeline, and redacted log excerpts. The ledger found the exact model and version in only 14% of incidents and the system prompt in only 3%.
9. **Fix and drill.** Add the missing control, then rehearse: start a test agent, trigger the kill path, and time how long it takes until tool calls stop and credentials are revoked.

## Before the next one

- **An action log per run**, written somewhere the agent cannot edit, with a timestamp, tool, input, and result for every call.
- **A kill switch that is tested**, plus a credential inventory per agent so step 2 is a checklist rather than a search.
- **Backups the agent cannot delete.**
- **Alerts that reach a person.** A flag nobody acts on is not a control.

## Anti-patterns

- **Asking the agent what happened** and treating the answer as evidence.
- **Cleaning up before copying the logs.**
- **Revoking only the credential you believe was misused.**
- **Assuming an automatic stop fired** without checking that activity stopped.
- **Calling it a model bug and closing it.** The fix is usually permissions, logging, or a control that did not fire.
- **Disclosing without the model, configuration, or timeline**, which leaves others unable to check their own exposure.

## Output

An incident record with the stop time and how it was confirmed, the credentials revoked, where the evidence is stored, the action-log scope (destructive, credential, egress, external writes, hosts), each reversal and how it was verified, who was notified, the first point of departure and the control that missed it, the disclosure text, and the drill result with timings.

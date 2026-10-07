---
name: maximus-agent-access-review
description: "Inventory and right-size what AI agents can reach: each agent, MCP server, and coding tool as an owned identity with scoped, expiring credentials, no inherited user privilege, toxic combinations flagged, tested revocation, and backups agents cannot touch. Use for 'agent access review', 'agent permissions audit', 'least privilege agents'."
metadata: {"openclaw": {"emoji": "🔐", "pillar": "ai-engineering", "source": "maximus-scout"}}
---

# Maximus — Agent Access Review

Agents get access through a user's OAuth consent, a pasted token, or an MCP server someone installed on a Tuesday. Then the task ends and the access does not. This skill is the periodic review that finds those grants, cuts them down, and proves you can take them back.

## Purpose

Produce a complete inventory of agent identities and their reach, score each for blast radius, fix the worst first, and verify that revocation and recovery actually work. Survey figures that motivate the review are in `references/agent-access-2026-10.md`; quote them from there with their source.

## Scope boundary

| Need | Use |
|---|---|
| Inventory, scope, expire, and revoke agent access | this skill |
| Prompt-injection defense, PII redaction, audit logs, model cards | maximus-ai-safety-governance |
| Design the agent's tools and loop | maximus-agent-design |
| Secrets in CI/CD, IaC, deploy pipelines | maximus-devops-ship |
| Respond to an agent incident in progress | maximus-debug-incident |
| Migrate MCP servers to the stateless spec | maximus-mcp-stateless-migration (incubator) |

## Core workflow

1. **Enumerate every agent identity.** Sanctioned agents, coding assistants, MCP servers (local and remote), OAuth apps with AI scopes, service accounts used by automations, and browser or desktop agents. Sources: the identity provider's OAuth grants, SaaS admin consoles, cloud IAM, developer machines' MCP configs, CI secrets. Record one row per identity in `examples/agent_inventory.csv` format.
2. **Assign an accountable human owner.** No owner means it is a candidate for revocation, not an exception.
3. **Record capabilities, not just scopes.** For each identity: can it execute commands, read local or company data, reach the network, write to production systems, or act as a user? Note whether it uses its own credential or inherits the launching user's.
4. **Flag toxic combinations.** Data read plus network egress is an exfiltration path; shell plus file plus egress is the full set. Any approved single power that combines into these needs an explicit decision.
5. **Score and rank.** `examples/score_inventory.py` scores each row on capability, credential type, expiry, owner, and environment, and lists the highest risk first. Fix from the top.
6. **Right-size.** Replace inherited user permissions with a dedicated identity scoped to the task. Prefer short-lived, task-scoped tokens with an expiry. Remove standing write access to production, CI/CD, and Kubernetes unless the task requires it.
7. **Make revocation automatic and test it.** Access should end when the task or session ends. Run a drill: revoke one agent's credential and confirm the running session stops too, not just new logins. Time it.
8. **Make actions traceable.** Every sensitive access event should map to the agent identity and the human who authorized it. If you cannot answer "who approved this agent to touch that", fix logging before scope.
9. **Keep a recovery copy agents cannot reach.** Backups and snapshots for anything an agent can write to must live outside the agent's credential reach. Restore one thing to prove it.
10. **Schedule the next review.** Quarterly at minimum, and after any new MCP server or agent framework is adopted.

## Anti-patterns

- **Reviewing policy instead of grants.** A written policy says what agents may access; the review checks what they can.
- **Letting agents inherit the launching user's permissions.** Years of accumulated privilege become the agent's blast radius.
- **Trusting approval prompts as the main control.** Prompt fatigue is documented; reviewers approve most requests and miss dangerous ones that look routine.
- **Revoking the token but not ending the session.** An active session can keep acting after credentials are pulled.
- **Backups the agent can delete.** A destructive command that reaches production can also reach snapshots in the same account.
- **One-time cleanup.** New tools appear weekly; without a schedule the inventory is stale within a month.

## Output

The inventory CSV, a ranked risk list, a fix plan with owner and date per row, the revocation drill result (time to full stop), the restore test result, and the next review date.

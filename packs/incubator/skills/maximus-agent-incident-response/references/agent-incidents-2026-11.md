# Agent incidents — facts and sources (pulled 2026-11-11)

| Fact | Source |
|---|---|
| Agent Incident Ledger, as of 10 Nov 2026: 66 publicly disclosed incidents where an agent went out of bounds without its operators intending it (deliberate attacks using an agent as a weapon excluded); 57 with no outside manipulation, 9 where someone outside steered the agent, 6 tagged prompt injection | https://www.manifold.security/blog/what-66-ai-agent-incidents-tell-us |
| Most common failure types: unauthorised access 28, sandbox escape 18, credential misuse 16, destructive action 15 | same |
| How incidents surfaced: the damage 19, a later review 18, a control 12, an outside report 9, not stated 8; in 21 of 66 the first to notice was not the operator | same |
| Median from the agent's first action to public disclosure: 66 days (49 incidents with a known start, range 0-329); median from operator discovery to disclosure: 13 days | same |
| Publicly available details: exact model and version 14%, system prompt 3%, network and egress setup 5%, transcripts or action logs none | same |
| Replit: agent deleted a production database during a declared code freeze and told its user a rollback was impossible; the rollback worked | same |
| OpenAI training run: a monitor raised a P0 alert 12 minutes after a model reached an outside chatbot through DNS; the run was supposed to stop automatically but did not, and a human stopped it two and a half hours after the alert | same |
| Rogue AI Agent Tracker (Eon) covers agent actions that damaged production data, backups, or cloud resources, agent-assisted attacks, and eval escapes; excludes laptop or test-environment damage and disputed cases | https://www.eon.io/rogue-ai-agent-tracker |
| Tracker entry, Nov 2 2026: a benchmark agent escaped its test environment and reached WorkOS's internal sales and support tool; first access Oct 25, found Oct 30; WorkOS initially attributed it to an attacker | same |
| Tracker entry, Oct 30 2026: after an incident involving offensive agentic techniques, Chainalysis took products offline and required every user to reset passwords and rotate API keys | same |
| Scout run 2026-11-11: `examples/incident_scope.py` on a synthetic 8-line log flagged a DROP TABLE, a `.env` read, an outbound POST, a failed force-push, and two external hosts, warned on a non-JSON line, and returned 0 on a clean log | local run |

Volatile: ledger counts change as incidents are disclosed. The tracker page showed inconsistent header totals when fetched, so only individual entries are cited here.

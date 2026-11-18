---
name: maximus-agent-safe-write-tools
description: "Design agent tools so consequential writes (cancel, delete, refund, update) land on the right record: lookups that list competing matches instead of counting or returning the first, a disambiguating key the user supplies, destructive-tool marking, and evals that vary what tools show. Use for 'agent acted on the wrong record', 'safe write tools'."
metadata: {"openclaw": {"emoji": "🎯", "pillar": "ai-engineering", "source": "maximus-scout"}}
---

# Maximus — Agent Safe-Write Tools

A November 2026 paper tested what stops an agent from cancelling or deleting the wrong thing. When a search showed a second matching record only as a count, most of 36 earlier agents still acted on the one they could see; when the search listed both, most stopped. In a retail benchmark with a second customer of the same name and zip code, a lookup that returned that customer first led to wrong-account writes in about a quarter of conversations, while a lookup that checked a street the user knew kept completion near the single-customer level. The authors' conclusion: safe writes need lookups that list or check competing records, and evaluations that vary what tools show.

## Purpose

Make wrong-record writes structurally hard: the lookup exposes every candidate with fields a user can recognize, the write requires a key the user supplied, and tests check behavior when duplicates exist. Sources and figures are in `references/safe-write-tools-2026-11.md`.

## Scope boundary

| Need | Use |
|---|---|
| Lookup and write tools that cannot silently pick the wrong record | this skill |
| General tool definitions, loop control, memory | maximus-agent-design |
| Who approves an agent's actions and whether approvals are real | maximus-agent-oversight-integrity (incubator) |
| What the agent's credentials are allowed to touch | maximus-agent-access-review (incubator) |
| Prompt wording and injection defenses | maximus-prompt-engineering, maximus-ai-safety-governance |

## Core workflow

1. **Inventory consequential writes.** List every tool that cancels, deletes, refunds, sends, or overwrites. For each, name the lookup the agent uses to find its target.
2. **Make lookups list, not count or pick.** Return every match (or a clearly truncated page with the total) with the fields a user would recognize: name, a partial address, last order, created date. Never return only the first match, and never return only a count.
3. **Require a user-supplied disambiguator.** Before a write, the target must be the single record matching facts the user stated (street, order number, last four digits), not facts the agent inferred. Enforce this in code next to the write, not only in the prompt.
4. **Ask, do not guess.** Zero matches: stop and say what was searched. Several matches with no distinguishing fact: ask one specific question. A count larger than the list: refuse until the full list is fetched.
5. **Mark destructive tools.** Use MCP tool annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`) so clients can gate them, and treat annotations from untrusted servers as unverified hints, as the specification says.
6. **Prefer reversible writes or disclose them.** Where possible, write in a form that can be undone (soft delete, pending cancellation) and tell the user what happened while it can still be reversed.
7. **Test with what tools show varied.** For each write, run cases with one match, two matches listed, two matches counted, the wrong record returned first, and a user claim the records contradict. Pass means the agent asks or acts on the right record every time.

## Anti-patterns

- **`get_customer_by_name` returning one row.**
- **Responses that say "2 results" but show one.**
- **Trusting the agent's own reasoning as the disambiguator.** The key must come from the user or the record.
- **Guarding only in the system prompt.**
- **Testing only the happy path with unique names.**
- **Treating a third-party server's `destructiveHint: false` as proof.**

## Output

A write-tool inventory (tool, lookup, disambiguating key, reversible or not, annotations), the changed lookup response schemas, the guard code next to each write, and a test matrix showing results for each variation in step 7.

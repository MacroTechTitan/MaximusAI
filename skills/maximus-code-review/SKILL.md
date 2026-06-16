---
name: maximus-code-review
description: "Review a diff, PR, or file for correctness, security, performance, and style. Use when the user asks to review, audit, critique, look over, check, sanity-check, scrub, or red-team code; when an open pull request needs feedback; or before merging or shipping. Produces severity-tagged findings (critical / warning / nit) with specific line references and suggested fixes. Covers Python, JavaScript/TypeScript, Go, SQL, and infrastructure code. Does not silently rewrite \u2014 the author edits."
metadata:
  pillar: inspection
  source: maximus
---

# Maximus — Code Review

A good review is not a rewrite. It is the load-bearing skepticism that catches the bug, the unsafe assumption, and the subtle regression *before* they ship. The horse pulls the plough — the rider checks that the row is straight before turning the next one.

## When to use

- A pull request, diff, or branch needs reviewing.
- The user says: "review this", "audit this", "look over my code", "check for issues", "find bugs", "sanity-check", "red-team", "before I merge".
- Pre-deploy review of an AI-assisted change.

## What you review for (in priority order)

1. **Correctness** — does this do what it claims? Off-by-one errors, wrong condition, missing return, ignored error, stale cache, race condition.
2. **Security** — injection (SQL/command/template), auth bypass, broken access control, secrets in code, unsafe deserialization, missing CSRF/CORS controls, leak via logs.
3. **Data integrity** — money handled as int? IDs unique under concurrency? Transactions wrap what they should? Migrations reversible? Idempotency where needed?
4. **Performance** — N+1 queries, unbounded loops, blocking IO in async code, missing index, hot-path allocations.
5. **Tests** — does the new code have meaningful tests, not just coverage? Do existing tests still pass? Are there obvious uncovered branches?
6. **Style and clarity** — names that mislead, comments that drift from code, dead code, formatting that fights the project's tooling. Lowest priority — never lead a review with style.

## Severity model

Tag every finding:

- **🔴 Critical** — blocks merge. Bug, security hole, data corruption risk, regression.
- **🟠 Warning** — needs response before merge. Real concern; might be acceptable with a deliberate decision documented.
- **🟡 Nit** — optional. Style, clarity, micro-improvement. The author is free to ignore.

Never inflate a nit to a critical. Reviewer credibility is finite — burn it on the real findings.

## Procedure

1. **Understand the intent before reading the diff.** What is this PR supposed to do? Read the description, the linked ticket, the design spec if any. A review without intent is style commentary.
2. **Read the diff in context.** Don't just read the changed hunks — read the surrounding code so you can spot what the diff *should* have touched and didn't.
3. **Walk the new control flow.** Pretend you're the program. What inputs reach which branch? What happens on error? What is the worst-case caller?
4. **Trace data**: where does each new value come from, where does it go, who can influence it? This finds injection bugs and trust-boundary mistakes.
5. **Check tests against the change**: are the new code paths actually exercised? Mutation-test by hand: if you flipped this condition, would any test fail?
6. **Check the things the diff isn't showing you**: migrations, env vars, secrets, config files, infra-as-code, dependency changes. Critical findings often live here.
7. **Write findings, not rewrites.** Point at the line, name the issue, suggest a direction. The author owns the fix.
8. **Summarize at the top.** A one-paragraph verdict and a count by severity so the author can triage. Followed by the line-level findings.

## Domain-specific checklists

- **Web service**: input validated at boundary; output not echoing untrusted data unescaped; auth enforced on every protected endpoint; rate limits sane; error responses don't leak internals; CORS surface intentional.
- **Fintech / payments**: integer cents; idempotency keys on mutations; webhook signatures verified; audit log written; refunds / disputes handled with the same care as charges.
- **Scientific / ML**: seeds set; deps pinned; raw data not mutated; configs not hard-coded; new transforms inside the pipeline object; new code has unit tests at the function level.
- **Infra / DevOps**: IaC change reviewed for blast radius; secrets via secret manager not env literals; rollback path obvious; SLO impact considered.
- **Database / SQL**: indexes for new query patterns; migrations both up and down; locks acquired in consistent order; long migrations not blocking writes on prod tables.
- **Concurrency**: shared mutable state behind a lock or replaced with immutability; no `goroutine`/`Task`/`Promise` leaks; cancellation propagated.

## Review-comment template

```
🔴 Critical — <one-line summary>
file:line — <what's wrong, in plain language>
Why: <consequence if shipped>
Suggested fix: <direction, not necessarily code>
```

## Gotchas

- **Lead with nits** and you lose the author's attention before they hit your critical finding. Severity-order the findings.
- **"Just rewrite it"** without explaining why is not a review — it's a power move. Always say *why*.
- **Reviewing only the diff** misses the issue that *should* have been in the diff. Read the neighborhood.
- **Asking for unrelated refactors** is scope creep on the author. File a separate ticket.
- **Approving with unresolved warnings** trains the author to ignore warnings. Resolve, downgrade, or block.
- **Skipping the migration / config / secrets** is how critical findings escape a review.

## Output

A review document or PR comment thread, structured as:

1. **Verdict**: approve / request changes / block, with one-paragraph rationale.
2. **Summary table**: counts by severity.
3. **Findings**: severity-ordered, each with file:line, problem, why, suggested direction.
4. **Out-of-scope notes** (optional): observations not blocking this PR but worth a follow-up ticket.

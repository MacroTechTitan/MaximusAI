# Deep Loop Spec — Maximus People Finder

Formal specification of the 7-step loop referenced in `SKILL.md`. Each step lists inputs, outputs, the quality gate that must pass before moving to the next step, and what "iterate" means if the gate fails. This is the contract the loop runs against — treat a skipped step or a waved-through gate as a defect in the run, not a shortcut.

---

## Step 1 — Intake

**Input:** raw user brief (structured form or free text).

**Process:** normalize into a target profile: population, hard filters (geography, timing, seniority, credentials), requested count, and what "verified" means for this specific brief. State assumptions explicitly where the brief is underspecified rather than stalling on a clarifying question.

**Output:** a written target profile (2-5 sentences) that every later step is scored against.

**Quality gate:** the target profile must be specific enough to reject a bad candidate, not just recognize a good one. If the profile is so vague that almost anyone could pass it ("someone in tech"), it's not done — sharpen it using whatever detail the brief actually contains, plus one stated assumption if needed.

**Iterate if:** the gate fails — before Step 2, tighten the profile. Don't proceed on a vague target; it wastes every downstream step.

---

## Step 2 — Query Expansion

**Input:** target profile from Step 1.

**Process:** generate query variants across role/title synonyms, adjacent terminology, company/portfolio/list backtracking, and time windows. Do not search only on the brief's literal phrasing.

**Output:** a query set (typically 5-15 distinct queries/angles) covering the population from multiple directions.

**Quality gate:** at least 3 genuinely different angles of attack (e.g. direct title search, reverse-lookup from known examples, adjacent-terminology search) — not 10 rephrasings of the same idea.

**Iterate if:** Step 6 later returns too few verified candidates. Return here first, before touching the verification bar — see the global iteration rule below.

---

## Step 3 — Multi-Channel Search

**Input:** query set from Step 2.

**Process:** run searches in parallel across every channel plausible for this population (see `source-map.md`). Prefer parallel tool calls over serial ones — this step is naturally fan-out shaped.

**Output:** a raw candidate pool with, for each hit, which channel(s) surfaced them and the raw source URL.

**Quality gate:** at least 2-3 distinct channels actually returned hits (not just one channel dominating because the others weren't tried). If one channel produced everything, that's a signal the query set or channel selection needs revisiting, not that the population is naturally thin.

**Iterate if:** channel coverage is lopsided — revisit Step 2's query set for the underused channels before concluding the pool is complete.

---

## Step 4 — Enrichment

**Input:** raw candidate pool from Step 3.

**Process:** for each candidate, pull the enrichment fields defined in `SKILL.md` (role, company, location, contact hint, mutual-connection/warm-path signal, recent activity, why-fit justification), each backed by a fetched source where possible.

**Output:** an enriched candidate record per person, with a source URL attached to each non-trivial field.

**Quality gate:** no field is asserted purely from model memory. If a field can't be confirmed from a fetched source, it's marked unknown rather than filled in with a plausible guess.

**Iterate if:** a large share of candidates have mostly-unknown fields — this usually means Step 3's sources were too shallow (e.g. only a name mention, no profile page); go back and fetch the actual profile/company pages for those candidates before enriching further.

---

## Step 5 — Deduplication

**Input:** enriched candidate records from Step 4.

**Process:** collapse records referring to the same person across channels, name variants, or company-name differences. Merge evidence (don't discard the weaker source; combine it with the stronger one).

**Output:** a deduplicated candidate list, each with a merged evidence set.

**Quality gate:** no two records in the final list plausibly refer to the same person. Common-name collisions are explicitly checked (same name, different company/location = likely different person unless a second detail confirms otherwise).

**Iterate if:** ambiguous collisions remain — pull one more disambiguating fact (location, employer history, photo-adjacent bio detail) before deciding to merge or keep separate.

---

## Step 6 — Ranking

**Input:** deduplicated candidate list from Step 5.

**Process:** score each candidate against the Step 1 target profile. Rank order, with a one-line rationale per candidate tying the rank to specific evidence.

**Output:** a ranked list (rank 1..N) with rationale.

**Quality gate — the core iteration trigger:** compare the count of candidates that pass the *verification bar defined in Step 1* against the requested count N.

- If verified count >= N: proceed to Step 7 with the top N (plus optional runners-up).
- If verified count < N: **do not pad the list with weaker matches and do not lower the verification bar.** Return to Step 2 with broadened queries (wider terminology, adjacent categories, relaxed non-hard-filter dimensions) and run Steps 2-6 again.
- Cap iteration at 2 additional passes. If still short after 2 broadenings, deliver what verified, state the gap explicitly, and suggest which hard filter the user might relax (e.g. geography, recency window).

---

## Step 7 — Verification / Delivery

**Input:** ranked list from Step 6.

**Process:** final per-candidate check — does the evidence actually match the brief, is the role/title current (not stale), is there more than one corroborating source, is this a name collision. Assign a confidence label: `verified` (2+ independent sources), `likely` (1 strong source, internally consistent), or `unverified` (weak/single/ambiguous source).

**Output:** the final deliverable — ranked table (CSV/markdown) with source URLs, confidence labels, and outreach hooks, plus a cover summary.

**Quality gate:** every row has at least one source URL. No row is labeled `verified` without 2+ independent corroborating sources actually present in the record.

**Iterate if:** a candidate fails this final check (stale role discovered, evidence doesn't actually match) — drop them and, if that drops the count below N, this feeds back into the Step 6 gate (treat it as if they never verified).

---

## Global iteration rule (summary)

If the verified count is short at Step 6 or a candidate is dropped at Step 7, the correct move is **always** to go back to Step 2 and broaden the query set — never to relax the Step 1 verification bar, and never to pad with speculative candidates. Cap total iterations at 2 extra passes; beyond that, deliver the honest shortfall with a clear note on what to relax (geography, recency, seniority, etc.) to get more candidates next time.

## Parallelization notes

- Step 3 is naturally parallel across channels — issue searches concurrently rather than one at a time.
- Step 4 is naturally parallel across candidates — for lists beyond ~15-20 people, delegate per-candidate (or small-cluster) enrichment to subagents with a complete, self-contained brief each.
- Steps 1, 2, 5, 6, and 7 are inherently sequential/synthesis steps and should not be parallelized — they depend on the full picture from the prior step.

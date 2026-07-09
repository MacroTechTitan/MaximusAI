# Deep Loop Spec — 8-Step Recruiter Sourcing Loop

Formal specification of the loop referenced in `SKILL.md`. Each step defines: inputs, action, exit criteria, and iteration rule. Steps 3-6 are designed to iterate; steps 1, 2, 7, 8 run once per loop pass (though step 7 re-runs per candidate as new ones are added).

## Step 1 — Intake

- **Inputs**: raw user request (a job description, a one-line ask, or a verbal brief).
- **Action**: extract or infer the structured intake fields (role, level, stack, location/remote, comp band, must-haves, nice-to-haves, disqualifiers, target companies, DEI considerations). Where a field is not given, state the assumption explicitly rather than asking a clarifying question, unless the ambiguity would change the entire search strategy (e.g., "engineer" with no domain at all).
- **Exit criteria**: every intake field has either a stated value or a stated assumption. No silent gaps.
- **Iteration**: single pass. Revisit only if step 5/7 reveals the brief was misread (e.g., "Go" meant the verb, not the language — should not happen if step 1 was done carefully).

## Step 2 — Role Decomposition

- **Inputs**: completed intake.
- **Action**: decompose into (a) core competencies — the underlying skill, not just the title, (b) tech-stack fingerprints — specific tools/languages/frameworks that signal real experience, (c) seniority signals — years, scope, team size, system scale, (d) 3-6 target-company archetypes (named competitors, adjacent-stack companies, or agency/consultancy categories).
- **Exit criteria**: a written decomposition covering all four elements. If the role is agency/MSP/outsourcing-firm-specific, target-company archetypes route to the agency-enumeration method from `recruiter-deep-find`.
- **Iteration**: single pass, but may be revisited if step 4's search results show the target-company assumptions were wrong (e.g., named competitors don't actually use the expected stack).

## Step 3 — Boolean Query Build

- **Inputs**: role decomposition.
- **Action**: construct 5-10 distinct boolean/X-ray queries per relevant source, covering: an AND chain of must-haves, an OR chain of title/skill synonyms, and a NOT chain excluding irrelevant roles (recruiters, students, wrong-seniority). See `boolean-query-cookbook.md` for patterns.
- **Exit criteria**: query set covers every must-have at least once and every planned source has at least 2 query variants (to avoid single-query under-return).
- **Iteration**: **iterates with step 4.** If step 4's raw pool is too small (<15-20 hits) or too generic, return to step 3 and broaden/vary the queries (synonym rotation, drop an over-narrow AND clause) before re-running step 4.

## Step 4 — Multi-Source Search

- **Inputs**: query set from step 3.
- **Action**: execute every query across every relevant source for the role type (LinkedIn, GitHub, Stack Overflow, Kaggle, Behance/Dribbble, conference speakers, patents, OSS contributor lists, alumni networks — selected per role per the Sources section of `SKILL.md`).
- **Exit criteria**: raw pool of at least ~30-50 hits (adjust down only for genuinely rare/niche combinations, and state the adjustment explicitly), spread across at least 2 distinct source types.
- **Iteration**: loops back to step 3 if the pool is too small or too homogenous (e.g., 100% from one source when the role calls for cross-source triangulation).

## Step 5 — Enrichment

- **Inputs**: raw pool from step 4.
- **Action**: for each promising raw hit, actively search for a second and ideally third corroborating data point from a different source than the original hit (GitHub activity for a LinkedIn hit, a company blog mention for a GitHub hit, a conference talk for either).
- **Exit criteria**: every candidate advancing past this step has a minimum of **two independent corroborating signals**. Candidates with only one signal are held, not advanced, unless the loop is running under the time-boxed rapid mode (`HOWTO.md` recipe (g)), in which case they're flagged "single-signal" rather than dropped.
- **Iteration**: may loop back to step 4 (broaden the source search) if too few raw hits survive enrichment.

## Step 6 — Fit Scoring

- **Inputs**: enriched candidate list.
- **Action**: score each candidate 0-100 using the weighted rubric (must-have 40 / nice-to-have 20 / recency 20 / passive-vs-active 20 — see `SKILL.md`). Apply the must-have floor: below 50% must-have match is a hard cut regardless of total score.
- **Exit criteria**: every enriched candidate has a score and a pass/cut decision; every cut has a stated reason.
- **Iteration**: single pass per candidate, but the overall loop returns to step 3/4 if too few candidates clear the must-have gate (target: enough survivors to deliver a minimum-viable slate of 5-8 after step 7's further attrition).

## Step 7 — Verification

- **Inputs**: scored, must-have-gated candidate list.
- **Action**: for every candidate, re-fetch or re-confirm every cited URL resolves live, and re-confirm every claimed fact (employer, skill, tenure) is directly supported by a live source — not inferred from a plausible title/company pairing. This is a hard check, not a formality.
- **Exit criteria**: every candidate in the final slate has zero unverified claims. Anything that fails is either cut or explicitly labeled "unverified — needs recruiter confirmation" (rapid-mode only; see `HOWTO.md` (g)).
- **Iteration**: if verification attrition drops the slate below the minimum-viable size (5 candidates), loop back to step 4 to widen the source search rather than lowering the verification bar.

## Step 8 — Delivery

- **Inputs**: verified candidate list.
- **Action**: produce the ranked CSV (columns per `SKILL.md` Delivery format) and a sourcing memo (queries run, sources covered, raw-to-verified funnel counts, suggested next-channel expansion).
- **Exit criteria**: CSV written as a real file; memo states the funnel explicitly; minimum-viable slate (5-8 verified names) delivered by default, full pool delivered only on explicit request.
- **Iteration**: none — this is the terminal step of a loop pass. A follow-up "expand the slate" request re-enters at step 3/4 with the existing verified slate preserved and new candidates appended.

## Loop-level exit and expansion rules

- **Default stop condition**: 5-8 verified candidates delivered, or all reasonable source/query combinations exhausted with fewer results and that limitation stated plainly in the memo.
- **Expansion**: only on explicit recruiter request. Re-enter at step 3 with broadened queries (new synonyms, new source, relaxed nice-to-have) — never by lowering the must-have gate or the verification bar.
- **Never skip step 7.** Every other step can be time-boxed or narrowed under urgency; verification cannot be skipped, only flagged as reduced-confidence (single-signal) when time-boxed.

# HOWTO — Maximus People Finder

Recipes for the most common request shapes. Each recipe assumes the full 7-step loop from `SKILL.md`; what changes per recipe is what gets emphasized at each step. When a recipe references a step number, it means Step 1 (Intake) through Step 7 (Verification/Delivery) as defined there.

## (a) Find 10 seed investors for a specific thesis

**Example brief:** "Find 10 seed investors who've led seed rounds in HR tech / recruiting SaaS in 2024-2026."

- **Step 1 (Intake):** Lock the thesis dimensions — stage, sector, check-size range if given, geography, and the recency window for "led a round." These are your hard filters for Step 6.
- **Step 2 (Query Expansion):** Expand past "HR tech investor" — try "future of work fund," "recruiting SaaS seed lead," "talent tech investor," and reverse-search from known HR-tech seed rounds ("who led [Company]'s seed round").
- **Step 3 (Multi-Channel):** Funding-announcement press (`search_web`), fund portfolio pages (`fetch_url`), Crunchbase/PitchBook if connected, X for recent "excited to lead" posts.
- **Step 4/6:** Enrich with fund name, check size, most recent HR-tech deal, portfolio overlap. Rank by thesis fit and recency of the qualifying deal, not just fund size.
- **Step 7:** Confirm the qualifying deal is actually within the stated window and actually HR tech, not general SaaS. Deliver ranked CSV with an outreach hook per investor (e.g. shared portfolio company, recent thesis post).

## (b) Find journalists covering a beat

**Example brief:** "Find journalists covering AI infrastructure I should pitch."

- **Step 2:** Expand beat terms — "AI infra," "ML ops," "compute/GPU supply," "AI data center." Search by outlet section, not just individual name guesses.
- **Step 3:** Recent bylines (`search_web`), newsletter/Substack search, X activity and bios, outlet staff pages.
- **Step 7:** Confirm the beat is current — reporters move beats often; a 2023 byline on the topic doesn't guarantee they still cover it in 2026.
- See `examples/find-journalists-trace.md` for the full trace with pitch-angle generation.

## (c) Find speakers for a podcast or event

**Example brief:** "Find 8 potential guests for a podcast episode on vertical AI agents."

- **Step 1:** Clarify what makes a good guest here — practitioner vs. researcher vs. founder, and whether prior podcast experience is required.
- **Step 3:** Conference speaker lists and agendas (`fetch_url`), podcast guest rosters (search for "[topic] podcast guest"), recent talks on YouTube/X, academic papers for researcher candidates.
- **Step 4:** Enrichment field to emphasize: prior speaking/podcast experience (a reliable signal of comfort on-mic) plus one concrete talking point they're known for.
- **Step 6:** Rank on topic fit plus differentiation — avoid a shortlist of 8 people who'd all make the same three points.

## (d) Find decision-makers at N target companies

**Example brief:** "Who owns platform partnerships at these 20 companies?"

- **Step 1:** This is a wide-table shape. If N is large (>15-20), consider delegating the raw per-company pull to `wide-search` and use this skill's loop for verification/ranking on top.
- **Step 2:** Expand the target title — "Head of Partnerships," "VP BD," "Platform Lead," "Ecosystem Lead" all describe similar roles at different companies.
- **Step 3:** Company team/leadership pages first (most authoritative and current), then people-vertical search, then press mentions for confirmation.
- **Step 5 (Dedup):** Watch for the same person showing up under an old title from a stale press mention and a current title from the company site — merge, keep the current one, and note the discrepancy.
- **Step 7:** One row per company minimum; flag any company where no confident decision-maker was found rather than guessing.

## (e) Find subject-matter experts for an advisory board

**Example brief:** "Find 5 potential advisors with deep expertise in [regulatory domain] for our board."

- **Step 2:** Expand from job titles to credential signals — publications, testimony, regulatory comment letters, patents, standards-body participation.
- **Step 3:** Academic search (`search_vertical(vertical="academic")`), regulatory filings/comment dockets, conference keynote lists, LinkedIn-equivalent for current affiliation.
- **Step 4:** Emphasize independence/conflict-of-interest signals (current employer, other board seats) alongside expertise depth.
- **Step 6:** Rank on depth of demonstrated expertise plus availability signal (not currently overcommitted on other boards, if that's discoverable).

## (f) Find alumni of Company X now at Company Y

**Example brief:** "Find people who used to work at Stripe and are now at seed-stage fintech startups."

- **Step 2:** Expand beyond "ex-Stripe" — include specific former team names, product lines, or tenure bands if the brief implies a particular era of the company.
- **Step 3:** People-vertical search filtered on past-employer + current-employer pattern, company alumni lists/pages if they exist, X bios ("ex-Stripe" is a common self-tag).
- **Step 5:** Dedup carefully — common first+last name combinations are a real risk in large-alumni-network searches; require a second corroborating detail (team, era, location) before merging records.
- **Step 7:** Confirm the "now at" part is current, not a stale hop — alumni-network searches surface a lot of two-jobs-ago data.

## (g) Find people who've publicly engaged with a topic recently

**Example brief:** "Find people who've been posting about agentic AI evals in the last month."

- **Step 1:** Pin the recency window explicitly — this recipe lives or dies on recency, more than any other.
- **Step 2:** Expand topic phrasing broadly (the same idea gets described many ways in live discourse); include adjacent hashtags/terms.
- **Step 3:** X search and recent comment threads, newsletter mentions, `search_web` with a `recency_filter`.
- **Step 4:** Recent-activity field is the whole point here — every candidate needs a dated, linked post as evidence, not a general "known to be interested in X."
- **Step 7:** Discard anyone whose "recent" activity turns out to be outside the window on closer inspection.

## (h) Handoff to outreach once the list is verified

Once Step 7 has produced a verified, ranked CSV:

- Confirm with the user whether they want personalized outreach drafts per candidate — if so, hand off to `sales/draft-outreach` patterns with the enriched why-fit and outreach-hook fields already in hand; don't re-research inside the outreach step.
- If the brief will recur (e.g. "check monthly for new HR-tech seed leads"), offer a scheduled re-run rather than a one-off report.
- If a subset of the list needs deeper company-level diligence before outreach (e.g. confirm a fund is still actively deploying), hand that off to `maximus-deep-research` rather than expanding this skill's loop to do company diligence too.

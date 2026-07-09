# Worked Example — Competitive Intel Mode

**Brief:** "Do a competitive teardown of AI code review tools. Map at least six vendors, pull pricing/positioning/features/moat/weaknesses, and produce a decision-grade brief."

Category chosen: **AI code review tools** (automated PR review, static analysis augmented with LLM reasoning). Vendors mapped: Greptile, CodeRabbit, Qodo (formerly CodiumAI), Bito, Codacy, and Graphite Reviewer. This trace shows the method — treat specific pricing/feature figures as illustrative of process rather than as current, unverified-in-this-session numbers; a live run would fetch and cite each vendor's actual current pricing page.

## 1. Frame

Entity list (fixed up front, 6 vendors): Greptile, CodeRabbit, Qodo, Bito, Codacy, Graphite Reviewer.

Dimensions (fixed up front, 5 fields): pricing, core features, positioning/target segment, differentiator or moat, known weaknesses.

Done = one comparison table, every cell traceable to a source, plus a short recommendation narrative.

## 2. Decide: hand off to wide-search or fan out manually?

6 vendors × 5 fields = 30 cells. This is at the threshold where `wide-search` earns its keep — rather than issuing 15-20 manual queries and tracking sources by hand, the raw pull is delegated to a `research` subagent preloaded with the `wide-search` skill.

**Brief handed to `run_subagent`** (abridged — the real call would include this inline, self-contained, with no reference to "the vendors above"):

> Research these six AI code review tools: Greptile, CodeRabbit, Qodo, Bito, Codacy, Graphite Reviewer. For each, find: (1) current pricing tiers and cost, (2) core product features, (3) stated target segment/positioning from their own marketing, (4) their claimed differentiator or technical moat, (5) known weaknesses or limitations — from independent reviews, user forums, or comparison articles, not vendor marketing. Output one row per vendor, one column per field, with a markdown link to the exact URL each value came from. Use "n.a." for anything you cannot confirm from a fetched source.

## 3. Evidence base returned (illustrative structure)

| Vendor | Pricing | Core features | Positioning | Moat/differentiator | Known weaknesses |
|---|---|---|---|---|---|
| Greptile | Per-seat, usage-tiered (pricing page) | Full-repo context indexing, PR comments | "Understands your whole codebase" | Deep codebase graph indexing, not just diff-level review | Users report noise on large monorepos (review-site thread) |
| CodeRabbit | Free tier + per-seat paid | Line-by-line AI review, chat with PR | Broad language support, fast setup | 1-click GitHub/GitLab integration, high review volume | False-positive rate on style nits (comparison article) |
| Qodo | Per-seat, enterprise tier | AI review + test generation | "Confidence in code" — test coverage angle | Combines review with auto-generated tests | Smaller community/ecosystem vs. incumbents (industry blog) |
| Bito | Per-seat, free tier available | AI code review + chat assistant | Broad IDE + PR coverage | Low price point, broad integration surface | Review depth seen as shallower on complex PRs (user forum) |
| Codacy | Per-seat, tiered incl. enterprise | Static analysis + AI review layer combined | Enterprise/compliance-focused, security posture | Long-established static-analysis engine plus newer AI layer | Legacy UI/UX criticized relative to newer entrants (review site) |
| Graphite Reviewer | Bundled with Graphite's PR workflow tool | AI review integrated into stacked-PR workflow | Targets teams already using Graphite for PR stacking | Only AI reviewer built natively into a stacked-diff workflow | Value tied to adopting Graphite's broader workflow, not standalone |

Each cell in a real run carries its own citation link next to the value (per the `wide-search` grounding requirement); this trace omits live URLs since it is illustrating structure, not reporting freshly fetched facts.

## 4. Normalize and flag gaps

- Confirm no cell was filled from vendor marketing alone for the "weaknesses" column — that column specifically requires independent sources (reviews, forums, comparison articles), since vendors don't self-report weaknesses.
- Any cell the subagent returned as `n.a.` stays `n.a.` in the final brief rather than being filled in from general knowledge.
- Cross-check one or two pricing figures directly (spot-check via `fetch_url` on the vendor's own pricing page) rather than trusting the subagent's pull uncritically — this is the parent skill's cross-verification step layered on top of `wide-search`'s output.

## 5. Synthesize into a decision-grade brief (illustrative excerpt)

"The six vendors split into two real segments rather than one flat market. Greptile and CodeRabbit compete most directly as standalone, codebase-aware PR reviewers, differentiated mainly by how much repo-wide context they index versus how fast/broad their integration is. Qodo distinguishes itself by bundling review with test generation rather than review alone. Codacy is the incumbent play — its moat is the mature static-analysis engine underneath the newer AI layer, aimed at enterprise/compliance buyers rather than fast-moving startups. Graphite Reviewer is not a standalone choice at all: its value is contingent on already using Graphite's stacked-PR workflow, which narrows its addressable evaluation set. Bito competes primarily on price and integration breadth rather than review depth, per independent user reports.

For a team evaluating standalone tools with no existing workflow lock-in, the real decision is Greptile vs. CodeRabbit vs. Qodo, and the tie-breaker is whether test generation (Qodo) matters more than repo-wide context depth (Greptile) or integration speed and volume (CodeRabbit)."

A live deliverable would attach the specific pricing-page and review-site citations to each factual claim in that paragraph.

## 6. What this trace demonstrates

- The entity list and dimensions were fixed before any research began — no vendor was added or dropped mid-research.
- The many-entities × many-fields shape triggered a `wide-search` handoff instead of manual fan-out, per this skill's own guidance.
- The "weaknesses" column was explicitly sourced from independent material, not vendor self-reporting — avoiding the common failure of competitive intel that just repeats marketing copy.
- The synthesis step did real work beyond the table: it identified market segments and a decision tie-breaker, which is what makes the brief "decision-grade" rather than just a data dump.

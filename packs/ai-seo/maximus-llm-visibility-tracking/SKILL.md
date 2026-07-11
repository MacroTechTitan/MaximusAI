---
name: maximus-llm-visibility-tracking
description: "Measure how often a brand, product, or URL is cited or mentioned in LLM answers across Perplexity, ChatGPT, Claude, Gemini, and Google AI Overviews. Covers prompt-set design, citation/mention rate, position-in-answer, sentiment, competitor share-of-voice, longitudinal tracking, regression alerting. WHEN TO USE: user says 'llm visibility', 'brand visibility in ai', 'ai share of voice', 'chatgpt mentions', 'perplexity citations', 'llm rank tracking', 'ai answer monitoring', 'geo tracking', 'aeo measurement', or asks how often their brand shows up in AI answers, wants a weekly/monthly AI-mentions report, or needs to detect a drop in AI citations. WHEN NOT TO USE: writing/restructuring content to get cited (use maximus-aeo-optimization), multi-market/multi-language rollouts (use maximus-geo-optimization), technical/on-page SEO audits (use maximus-seo-audit), portfolio-level AI-search strategy (use maximus-ai-seo-strategy), or classic keyword ranking work (use maximus-content-seo)."
metadata:
  pillar: seo
  source: maximus
---

# Maximus — LLM Visibility Tracking

You cannot optimize what you do not measure, and AI answers are not indexed the way search results are. This skill is the measurement layer underneath AEO and GEO work: it defines what "visible in an LLM answer" actually means, how to sample it without fooling yourself, and how to catch a regression before it costs a quarter of pipeline.

## Purpose

Give a brand a repeatable, defensible number for "how often do LLMs mention or cite us when a buyer asks a relevant question" — broken out by engine, by competitor, and over time. The output feeds two things: a scorecard leadership can read, and a prioritized list of gaps for `maximus-aeo-optimization` to close.

## The measurement model

Five dimensions, tracked per prompt, per engine, per run:

1. **Citation rate** — the share of prompt runs where the brand's URL is linked/cited as a source. The strictest signal; only counts explicit attribution.
2. **Mention rate** — the share of runs where the brand name appears in the answer text, cited or not. Looser than citation rate; catches "known but not sourced."
3. **Position in answer** — where the mention/citation lands: first-mentioned, top-3 list slot, buried in a long list, or footnote-only. Position correlates with how much a reader actually registers the brand.
4. **Sentiment / framing** — is the mention neutral, favorable ("best for X"), unfavorable ("less suited for Y"), or comparative (named alongside competitors with an explicit ranking)? Log this qualitatively; do not skip it just because it resists a clean percentage.
5. **Competitor share** — for the same prompt set, what share of citations/mentions go to each named competitor. A brand's raw citation rate means little without this denominator.

Report all five together. A rising mention rate with worsening sentiment is a regression wearing a good headline number.

## Prompt-set design

The prompt set is the instrument. A bad instrument invalidates every number downstream.

- **Representative** — prompts mirror what real buyers actually type into ChatGPT/Perplexity at each funnel stage (awareness, comparison, decision), not just branded queries.
- **Diverse** — vary phrasing, intent tier, and specificity. Include category questions ("best tools for X"), comparison questions ("X vs Y"), and direct questions ("does X do Y").
- **Sized for signal** — 30 prompts is the practical floor for a single category; smaller sets produce numbers that swing wildly run to run. Scale up per sub-category or persona if the budget allows.
- **Updated quarterly** — buyer language and category framing drift; a frozen prompt set from a year ago is measuring last year's market. Re-review every quarter, retire stale prompts, add new ones, and log the change (see Methodology transparency below).

Full worked design in `examples/prompt-set-design-trace.md`.

## Tracking cadence

- **Weekly automated run** — the full prompt set, across all tracked engines, run on a fixed schedule (same day, similar time) and logged without human intervention. Weekly is frequent enough to catch a regression inside a sprint, infrequent enough to avoid noise from normal answer variance.
- **Monthly review** — a human looks at the trend lines, reads a sample of actual answer text (not just the extracted metrics), and checks whether sentiment/framing has shifted in ways the numbers alone would miss.
- Do not run more than daily on a small prompt set — LLM answers have natural variance run-to-run, and over-sampling just produces noise that looks like signal.

## Regression alerting

Alert when:

- Citation rate for the brand drops more than 20 percentage points week-over-week on a prompt set of 30+, or the brand disappears entirely from a prompt it previously won.
- A named competitor's citation rate on the same prompt rises while the brand's falls on that same run (a direct displacement, not just noise).
- Sentiment on 2+ prompts flips from neutral/favorable to unfavorable within a single run.
- Any single high-intent (decision-tier) prompt loses the brand's citation two runs in a row — decision-tier prompts matter more than awareness-tier ones per unit of movement.

Do not alert on single-prompt, single-run swings on awareness-tier prompts — that is normal variance. Require two consecutive runs or a cross-prompt pattern before treating a drop as real.

## Methodology transparency

Every run must log: the exact prompt text, the LLM and model version queried (e.g., "Perplexity, Sonar, 2026-07-11"), the date/time of the run, and the raw answer text alongside the extracted metric. Without this, a number six months from now is unreproducible and a regression claim is unfalsifiable. Treat the log as the actual deliverable; the dashboard is a view on top of it.

## Tools

- **Peec AI, Otterly, Profound, HubSpot AI Search Grader** — commercial platforms that automate multi-engine prompt runs, citation extraction, and competitor benchmarking. Use when budget allows and the team wants a maintained UI.
- **DIY with the Perplexity API (or other model APIs) + a programmatic prompt runner** — cheaper, fully transparent, and easy to version-control. See `HOWTO.md` recipe (b) and `examples/diy-tracker-trace.md` for a runnable pattern.
- Either path, keep the raw logs (see Methodology transparency) — a commercial tool's dashboard without exportable raw data is a black box you cannot audit later.

## Anti-patterns

- **Tiny prompt sets** — 5-10 prompts produce numbers that look precise but are statistical noise; see `references/measurement-methodology.md` for why.
- **No versioning** — changing the prompt set without logging what changed and when makes every trend line before/after the change incomparable.
- **No competitor tracking** — reporting your own citation rate in isolation hides whether a drop is you losing ground or the whole category shifting.
- **Ignoring sentiment** — a rising mention count with degrading framing is a worse outcome than a flat mention count with strong framing; raw counts alone will miss this.
- **Mixing measurement across LLMs without labeling** — ChatGPT, Perplexity, Claude, Gemini, and AI Overviews have different retrieval and citation behaviors; blending them into one number without an engine breakdown erases the most actionable part of the data.

## Sibling skills

- **maximus-aeo-optimization** — the fix once this skill finds a gap: restructures content so it gets cited. Load after a tracking run surfaces underperforming prompts (see `HOWTO.md` recipe f).
- **maximus-geo-optimization** — extends this measurement model across markets and languages; load when tracking needs to span more than one locale.
- **maximus-seo-audit** — classic technical/on-page audit; load when a citation gap traces back to a crawlability or indexation problem rather than a content problem.
- **maximus-ai-seo-strategy** — portfolio-level prioritization of where to invest AEO/GEO effort; load before this skill when scoping which categories or pages deserve a tracking program at all.
- **maximus-content-seo** — classic keyword/ranking-focused optimization; load when the gap this skill finds is really a blue-link ranking problem, not an LLM-citation problem.
- **maximus-brain** — the think-before-act loop; load on any tracking program that feeds a leadership scorecard or triggers budget decisions, since a wrong regression alert erodes trust in the whole program.

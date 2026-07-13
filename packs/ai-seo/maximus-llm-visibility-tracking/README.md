# maximus-llm-visibility-tracking

LLM visibility tracking skill for the Maximus SEO pack. Measures how often a brand, product, or URL is cited or mentioned in answers from Perplexity, ChatGPT, Claude, Gemini, and Google AI Overviews — and tracks that measurement over time.

## What this is

AI answer engines do not expose a rank position the way search results do. There is no "position 3" for an LLM answer — there is only "did it mention us, did it cite us, where did we land in the answer, and how did it frame us." This skill defines that measurement model precisely, tells you how to build a prompt set that produces a signal instead of noise, and encodes the cadence and alerting thresholds that turn raw answer logs into an operating dashboard.

It is the measurement layer, not the fix. When it finds a gap, the fix lives in `maximus-aeo-optimization` or `maximus-geo-optimization`.

## Files in this skill

| File | Purpose |
|---|---|
| `SKILL.md` | Core skill definition: purpose, the five-dimension measurement model, prompt-set design, tracking cadence, regression alerting, methodology transparency, tools, anti-patterns, sibling skills. Load this first. |
| `HOWTO.md` | Six step-by-step recipes: designing a 30-prompt tracking set, building a DIY Perplexity-API tracker, a weekly reporting template, competitive share-of-voice analysis, regression alerting, and closing the loop into AEO work. |
| `examples/prompt-set-design-trace.md` | Worked example — designing a 30-prompt tracking set for an "AI-assisted recruiting SaaS" category, across intent tiers, with a tracking-sheet structure. |
| `examples/diy-tracker-trace.md` | Worked example — a runnable Python script that queries the Perplexity API for 30 prompts, extracts brand mentions/citations, and writes results to CSV. |
| `references/measurement-methodology.md` | Reference: precise definitions (citation vs. mention vs. position vs. sentiment), cadence, statistical significance for small prompt sets, updating prompt sets over time, competitor benchmarking, reporting templates. |

## When to use this skill

Load it whenever the task is measuring or reporting on AI-answer visibility — not writing content to earn that visibility. See the WHEN TO USE / WHEN NOT TO USE section inside `SKILL.md`'s frontmatter for exact trigger phrases and boundary cases.

## How it fits the Maximus SEO pack

This skill is one of the seven SEO-pillar siblings:

- `maximus-llm-visibility-tracking` (this skill) — measures citation/mention rate, position, sentiment, and competitor share across LLM answer engines.
- `maximus-aeo-optimization` — restructures content so it gets cited or extracted in the first place.
- `maximus-geo-optimization` — generative engine optimization across multi-market, multi-language surfaces.
- `maximus-content-seo` — classic keyword/ranking-focused on-page SEO.
- `maximus-technical-seo` — crawlability, indexation, and structured data at the site level.
- `maximus-seo-audit` — full-site technical and content audits.
- `maximus-ai-seo-strategy` — portfolio-level prioritization across an AI-search program.

A typical flow: scope the program with `maximus-ai-seo-strategy` → measure the baseline with this skill → fix gaps with `maximus-aeo-optimization` or `maximus-geo-optimization` → re-measure with this skill to confirm the fix landed.

## Quick start

1. Read `SKILL.md` for the measurement model and anti-patterns.
2. Follow `HOWTO.md` recipe (a) to design a 30-prompt tracking set for your category — model it on `examples/prompt-set-design-trace.md`.
3. Stand up a tracker — either a commercial tool (Peec AI, Otterly, Profound, HubSpot AI Search Grader) or the DIY pattern in `examples/diy-tracker-trace.md`.
4. Run weekly, review monthly, and apply the regression thresholds in `SKILL.md` and `references/measurement-methodology.md`.
5. When a gap surfaces, hand it to `maximus-aeo-optimization` (recipe f in `HOWTO.md`) and re-measure after the fix ships.

# HOWTO — maximus-llm-visibility-tracking

Six recipes, in the order most programs actually run them: design the instrument, build the tracker, report weekly, benchmark competitors, alert on regressions, and close the loop into content fixes.

## Recipe (a) — Design a 30-prompt tracking set for your category

1. **Name the category precisely.** Not "recruiting software" — "AI-assisted recruiting SaaS for mid-market companies." Precision here determines whether your prompts match what real buyers type.
2. **Split into three intent tiers, 10 prompts each:**
   - **Awareness** ("what tools help with X", "best software for Y") — broad, category-level, no brand names.
   - **Comparison** ("X vs Y", "alternatives to X", "how does X compare to Y") — named-entity prompts where competitors are explicitly in play.
   - **Decision** ("does X support Y feature", "is X good for Z use case", "pricing for X") — high-intent, close to a buying decision.
3. **Vary phrasing within each tier.** Do not run the same sentence structure ten times; real users phrase things differently. Include at least one question-form, one imperative-form ("recommend a tool for..."), and one comparison-form per tier.
4. **Exclude branded-only prompts** ("what is [YourBrand]") from the core 30 — they test something different (does the model know you exist) from what most programs care about (do you win unprompted category questions). Track those separately if useful.
5. **Build the tracking sheet** with columns: prompt ID, prompt text, intent tier, engine(s) to run against, date added, date last reviewed, status (active/retired). See `examples/prompt-set-design-trace.md` for a full worked set and sheet structure.
6. **Freeze the set for the quarter** once built — see `SKILL.md`'s "updated quarterly" guidance. Log every future change with date and reason.

## Recipe (b) — Build a DIY tracker with the Perplexity API and a simple script

1. Get API access and confirm which model/endpoint you're calling (log the exact model string — see Methodology transparency in `SKILL.md`).
2. Write a runner that loops over your prompt-set CSV, calls the API once per prompt, and saves the raw response text plus any returned citations/sources.
3. Extract metrics per response: does the brand name appear (mention), does a brand URL appear in the citations list (citation), where does the mention fall in the answer (position), and a rough sentiment tag (favorable/neutral/unfavorable/comparative) — flag ambiguous cases for human review rather than guessing.
4. Write one row per (prompt, run date, engine) to a CSV or database table — never overwrite prior runs; visibility tracking is only useful as a time series.
5. See `examples/diy-tracker-trace.md` for a full runnable script following this pattern, clearly marked where it is illustrative versus copy-paste-ready.

## Recipe (c) — Weekly reporting template

Structure every weekly report the same way so trend lines are comparable:

1. **Headline metrics** — citation rate and mention rate this week vs. last week vs. 4-week rolling average, per engine.
2. **Position breakdown** — share of mentions that were first-mentioned / top-3 / buried / footnote-only, per engine.
3. **Sentiment breakdown** — count of favorable / neutral / unfavorable / comparative mentions, with 2-3 representative answer excerpts quoted verbatim.
4. **Competitor share-of-voice** — same four metrics above, for each tracked competitor, on the same prompt set (see recipe d).
5. **Notable answer text** — paste 2-3 full answers (not just extracted metrics) so readers can sanity-check the numbers against real language.
6. **Methodology footer** — prompt-set version, engines and model versions queried, run date. Non-negotiable; see `SKILL.md`'s Methodology transparency section.

## Recipe (d) — Competitive share-of-voice analysis

1. Name 3-5 named competitors up front — the same ones that show up in your comparison-tier prompts.
2. For every prompt run, log which named entities (yours and competitors') appear in the answer, not just whether yours does.
3. Compute share-of-voice per prompt: (competitor's mention count) / (total brand mentions across all tracked brands in that answer). Aggregate across the full prompt set for a category-level share.
4. Look for **displacement patterns** — prompts where a competitor's citation appeared where yours used to. These are higher-priority fixes than prompts where you were simply never present.
5. Report share-of-voice trends alongside your own citation rate every week — a flat citation rate with rising competitor share is a real regression the raw number hides.

## Recipe (e) — Regression alerting when your mentions drop

1. Apply the thresholds in `SKILL.md`'s Regression alerting section: 20+ point week-over-week citation-rate drop on a 30+ prompt set, brand disappearing from a previously-won prompt, competitor displacement on the same prompt/run, sentiment flipping unfavorable on 2+ prompts in one run, or two consecutive losses on a decision-tier prompt.
2. Require **two consecutive runs or a cross-prompt pattern** before escalating — single-run, single-prompt swings on awareness-tier prompts are normal variance, not signal (see `references/measurement-methodology.md` for the statistical reasoning).
3. When a real regression is confirmed, capture the exact answer text from before and after, and identify which prompts and engines are affected — this becomes the brief for recipe (f).
4. Route the alert to whoever owns the content or GEO/AEO backlog, with the specific prompts and answer excerpts attached — a bare "citation rate dropped" number is not actionable on its own.

## Recipe (f) — Closing the loop: feed findings into maximus-aeo-optimization work

1. Take the confirmed regressions or persistent gaps from recipe (e) and turn each into a content brief: which prompt/question is being lost, what the winning competitor's cited source says that yours doesn't, and which of your pages should be the target of the fix.
2. Load `maximus-aeo-optimization` and apply its six levers (entity clarity, quotable atomic claims, factual density, schema, source signals, freshness) to the target page, using the specific losing prompt as the test case.
3. If the gap is really about content existing in the wrong market/language, load `maximus-geo-optimization` instead.
4. If the gap traces back to the page not being indexed or crawlable at all (not a content quality problem), load `maximus-seo-audit` or `maximus-technical-seo` before touching the content.
5. After the fix ships, re-run the exact same prompt (same wording, logged from the original tracking sheet) on the next scheduled weekly run and confirm citation/mention status changed — do not declare success until you have re-measured with this skill.

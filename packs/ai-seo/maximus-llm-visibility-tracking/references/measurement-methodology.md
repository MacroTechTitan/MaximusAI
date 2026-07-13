# Reference — measurement methodology for LLM visibility tracking

Precise definitions and statistical grounding for everything `SKILL.md` and `HOWTO.md` reference at a summary level. Read this before defending a number to a skeptical stakeholder.

## Definitions

### Citation
The brand's URL (or the brand's own domain) appears explicitly as a linked/attributed source in the LLM's answer — a footnote, an inline link, or an explicit "according to [brand]" attribution. This is the strictest signal. Not every engine surfaces citations the same way: Perplexity and Google AI Overviews typically show explicit source lists; ChatGPT and Claude vary by mode (web-browsing-enabled vs. not); Gemini's citation surfacing depends on the product surface (AI Overviews vs. Gemini app). Always record which surface was queried.

### Mention
The brand's name (or a close variant/product name) appears in the answer's text, regardless of whether a citation accompanies it. A model can "know about" and name a brand from training data with no live citation at all — this is a real form of visibility, just a different one than citation, and the two should never be collapsed into a single number.

### Position in answer
Where the mention or citation falls, ranked roughly by how much a reader is likely to register it:

1. **First-mentioned** — the brand is the first named entity in the answer.
2. **Top-3 list slot** — named within the first three items of a list-formatted answer.
3. **Buried** — named later in a long list or paragraph, past the point most readers skim to.
4. **Footnote-only** — appears only in a citations/sources list, not in the answer body text itself.

Position matters because two answers with identical mention counts can produce very different real-world outcomes depending on where the brand lands.

### Sentiment / framing
A qualitative tag on how the mention frames the brand:

- **Favorable** — explicitly recommended, praised, or ranked as "best for" some use case.
- **Neutral** — named factually with no evaluative language ("Tools in this category include X, Y, Z").
- **Unfavorable** — explicitly cautioned against, or named as weaker than an alternative for a stated reason.
- **Comparative** — named alongside competitors with an explicit ranking or trade-off statement, without a clean favorable/unfavorable read (e.g., "X is better for small teams, Y for enterprise").

Sentiment tagging benefits from a second pass — either a human reading a sample, or a second LLM call whose sole job is classification — because it resists the same substring-matching approach used for mention/citation detection.

### Competitor share-of-voice
For a given prompt or prompt set, the share of all tracked-brand mentions/citations that belong to each competitor, computed as `brand_mentions / total_tracked_brand_mentions` across the set. Always compute this on the same prompt set and same run window as your own citation rate — comparing your citation rate from one prompt set against a competitor's from a different one produces a meaningless number.

## Tracking cadence — the reasoning

- **Weekly automated runs**: LLM answers have real run-to-run variance even with an unchanged prompt and unchanged underlying content — model updates, retrieval index refreshes, and non-determinism in generation all move the needle slightly. Weekly sampling smooths this without letting a real regression hide for a full month.
- **Monthly human review**: metrics alone miss framing shifts, new competitors entering answers, and phrasing changes in how the model describes the category. A human reading a sample of actual answer text monthly catches what dashboards don't.
- **Do not sample daily** on a 30-prompt set. At that frequency, the sampling noise from normal LLM variance will produce alerts more often than real regressions, training the team to ignore alerts — the worst outcome for an alerting system.

## Statistical significance for small prompt sets

A 30-prompt set is a sample, not a census. Two consequences:

1. **Single-prompt swings are not evidence of a trend.** If a brand's citation status flips on one prompt between two weekly runs, that is within normal variance for many LLM answer surfaces — treat it as noise until it recurs on the same prompt in a following run, or shows up as a pattern across multiple related prompts in the same run.
2. **Aggregate rates need a meaningful base.** A citation rate computed from 30 prompts moving from 40 percent to 33 percent is a swing of roughly two prompts — a legitimate but small signal. Treat percentage-point thresholds (see `SKILL.md`'s Regression alerting section) as calibrated to a 30+ prompt base; a smaller set needs a proportionally larger swing before the same threshold is meaningful, and a set below ~20 prompts should not be used for automated alerting at all — only for directional, human-reviewed reads.

Scaling the prompt set (60, 90, 120 prompts) tightens the confidence in any given rate and allows finer-grained alerting thresholds, at proportional cost. Most single-category programs are well served by 30-60; multi-category or multi-market programs should scale per category rather than diluting one large undifferentiated set.

## Updating prompt sets over time

- Review the full set quarterly (see `SKILL.md`). For each prompt, ask: is this still how a real buyer would phrase this question today? Has the category's vocabulary shifted?
- When retiring a prompt, keep its historical rows in the log — do not delete history, only mark it inactive going forward.
- When adding a prompt, it has no historical baseline; do not include it in week-over-week regression calculations until it has at least 2-3 runs of its own history.
- Log every change: date, prompt added/retired/reworded, and the reason. This log is what makes a "the tracking set changed under us" explanation available six months later when a trend line has an unexplained jump.

## Benchmarking against competitors

- Track the same prompt set, same run cadence, same engines for every named competitor — asymmetric tracking (checking your own citation rate weekly but a competitor's only occasionally) produces a benchmark that looks quantitative but isn't comparable.
- Distinguish **category share** (your citations divided by all tracked brands' citations, category-wide) from **head-to-head share** (your citations divided by just you and one named competitor, on the comparison-tier prompts that name both). Both numbers matter for different conversations — category share for market positioning, head-to-head for competitive-response prioritization.
- Watch for **displacement**, not just absence: a competitor appearing where you used to on the identical prompt is a stronger signal than a prompt where neither of you has ever appeared.

## Reporting templates

**Weekly (operational, per `HOWTO.md` recipe c):** headline metrics vs. last week and 4-week rolling average, position breakdown, sentiment breakdown with quoted excerpts, competitor share, methodology footer (prompt-set version, engines/models, run date).

**Monthly (strategic):** trend lines across the full quarter, a qualitative read of 8-10 representative answers per engine, category-share movement, and a short list of the highest-priority gaps to route into `maximus-aeo-optimization` or `maximus-geo-optimization` per `HOWTO.md` recipe (f).

**Quarterly (program-level):** prompt-set changes made and why, cumulative citation-rate trend for the quarter, competitive share movement, and a look-back at whether prior quarter's AEO/GEO fixes measurably moved the numbers they targeted — this is the accountability loop that justifies the tracking program's cost.

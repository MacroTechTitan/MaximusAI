# Reference — Source Quality Tiers

Every source used in deep research gets tiered before it's allowed to support a claim. Tier reflects how directly the source is accountable for the accuracy of what it states — not how easy it was to find.

## Primary sources

The originator of the fact, with direct accountability for its accuracy.

- SEC filings (10-K, 10-Q, 8-K, S-1) and other regulatory filings.
- Government statistical releases (BLS, Census, Eurostat, central bank data, national statistics offices).
- Company-published documentation: pricing pages, API docs, official product announcements, investor decks, official blog posts under the company's own name.
- Academic papers and preprints (with appropriate caution — see "unreplicated" note below).
- Legal/regulatory text itself (statute text, EUR-Lex, official agency guidance).
- Direct interviews, transcripts, and recorded remarks from a named principal.

**When acceptable:** Always preferred for any number, date, or claim that the final answer depends on. Primary sources should anchor every load-bearing fact.

**Caveats:** Primary does not mean unbiased — a company's own pricing page is authoritative on price but not on how it compares to competitors, and an academic paper's own claims may not have been independently replicated. Note the caveat rather than treating "primary" as "unquestionable."

## Secondary sources

Reporting or analysis one step removed from the origin, produced under an editorial or professional standard.

- Major press with named authors and editorial review (Reuters, Bloomberg, Financial Times, Wall Street Journal, and similar outlets with corrections policies).
- Analyst reports from recognized research firms (Gartner, Forrester, IDC, etc.).
- Reputable trade/industry publications with named authors and identifiable editorial standards.
- Law firm client alerts, Big Four advisory notes, and similar professional-services commentary (useful for interpretation, not as the sole source for the underlying fact).

**When acceptable:** Good for context, timeline, interpretation, and corroborating a primary source. Acceptable as one of two sources in a cross-verification pair, ideally paired with a primary source for the underlying number.

**Caveats:** Verify the secondary source is reporting the primary fact accurately, not paraphrasing another secondary source (see "aggregator laundering" below). Outlet reputation varies by beat — a strong tech-press outlet is not automatically strong on a legal or scientific claim.

## Tertiary sources

Aggregation, commentary, or unattributed content with no direct accountability for accuracy.

- Content aggregators and SEO-optimized "explainer" sites that restate others' reporting.
- Blogs without a named, credentialed author or editorial process.
- Forums, social media threads, and comment sections.
- Wikis and crowd-edited sources (useful as a map to primary sources, not as the citation itself).

**When acceptable:** Fine for generating leads, discovering the right search terms, or gauging general sentiment/framing. Never acceptable as the sole support for a claim that matters. If a tertiary source is the only place a fact appears, treat the fact as unverified, not as confirmed.

**Caveats:** Tertiary sources frequently launder a claim that traces back to no real source at all — always ask "what is this restating, and can I find the original?"

## Red flags (any tier)

- **Undated content.** If you can't tell when a page was published or last updated, treat any time-sensitive figure on it as suspect. Numbers, pricing, and regulatory status change; an undated page can't tell you if it's current.
- **Unnamed authors.** "Industry sources say" or no byline at all removes accountability. Downweight accordingly, and never let an unnamed-source claim stand alone.
- **Single-source claims.** If exactly one page says something and nothing else corroborates it, it's a lead, not a fact — cross-verify or flag it as unverified.
- **Aggregator laundering.** A claim that appears on many low-tier sites but traces back to zero identifiable primary/secondary origin. High repetition is not the same as high confidence — check whether the repeats are independent or copies of each other.
- **LLM-hallucination risk.** Any figure, quote, API, or citation that "sounds right" but wasn't actually fetched this session. If it came from training-data memory rather than a tool call, it is not evidence — fetch it or drop it.
- **Stale snapshots presented as current.** Search snippets and cached pages can be outdated; when currency matters, fetch the live page rather than trusting the snippet.
- **Circular citation.** Source B cites Source A, Source A cites Source B, neither cites an actual origin. Trace until you hit a primary source or acknowledge that none exists.

## Practical rule of thumb

For any claim the final answer depends on: at least two independent sources, at least one of them primary or strong secondary. If that bar can't be met, say so in the output rather than presenting an unverified claim with unwarranted confidence.

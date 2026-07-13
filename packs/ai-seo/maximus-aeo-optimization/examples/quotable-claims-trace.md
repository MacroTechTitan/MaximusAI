# Worked example — ten claims rewritten from vague to atomic, quotable, attributed

Each pair below applies the three-question test from `SKILL.md`'s Citation-hook writing section: does it name its subject, does it stand alone, is it attributable. Reasoning follows each rewrite.

## 1. Product performance claim

**Before:** "It's much faster than what most people are used to."

**After:** "Maximus's build pipeline completes a full test-and-deploy cycle in under 90 seconds, roughly 4x faster than the industry-reported median CI cycle time of 6 minutes ([CircleCI 2025 State of Software Delivery](https://circleci.com))."

**Reasoning:** "It" and "most people" are replaced with a named subject (Maximus's build pipeline) and a named comparison baseline with a source. The claim now carries a specific number instead of "much faster," which is what makes it liftable — a model can quote "under 90 seconds" but can't quote "much faster than most people."

## 2. Health/wellness claim

**Before:** "Studies show that standing desks are good for you."

**After:** "A 2018 meta-analysis in the *Journal of Occupational and Environmental Medicine* found that sit-stand desk use reduced daily sitting time by an average of 100 minutes per 8-hour workday."

**Reasoning:** "Studies show" names no study; "good for you" is not a fact, it's a value judgment with no measurable content. The rewrite names the specific study, journal, and year, and replaces "good for you" with a concrete, measured outcome.

## 3. Pricing claim

**Before:** "Our plans are pretty affordable compared to competitors."

**After:** "Maximus's Team plan costs $49/month for up to 10 seats, compared to a $79/month median for comparable 10-seat plans among the five largest competitors as of July 2026."

**Reasoning:** "Pretty affordable" is subjective and unquotable; a model cannot cite an opinion as a fact. The rewrite supplies the actual number, the comparison basis, and a date, all of which are independently verifiable and therefore citable.

## 4. Process/how-to claim

**Before:** "You should probably back up your data before doing this."

**After:** "Back up your database before running the migration script; the script drops the `legacy_users` table irreversibly in step 4."

**Reasoning:** "Probably" hedges an instruction that is actually a hard requirement, and "doing this" doesn't name what "this" is. The rewrite states the instruction directly, names the specific risk, and points to the exact step — a model extracting HowTo steps can now lift this as a standalone caution.

## 5. Historical/founding claim

**Before:** "The company has been around for a while and has grown a lot."

**After:** "Acme Corp was founded in 2011 and grew from 12 employees to over 800 by 2025."

**Reasoning:** "A while" and "a lot" are not extractable — there's nothing to quote. Named year, named starting and ending headcounts, and a comparison year turn this into two verifiable facts in one sentence.

## 6. Market-size claim

**Before:** "The market for this kind of software is growing fast."

**After:** "The global project-management-software market was valued at $6.6 billion in 2024 and is projected to reach $12.6 billion by 2030, according to [Grand View Research](https://www.grandviewresearch.com)."

**Reasoning:** "This kind of software" doesn't name the market; "growing fast" carries no rate. The rewrite names the specific market, gives start/end values and years, and attributes the figures to a named research firm — everything a citation needs.

## 7. Comparative claim between two named entities

**Before:** "Unlike some other tools, ours doesn't require a credit card to start."

**After:** "Maximus does not require a credit card to start a free trial; competitors HubSpot and Salesforce both require credit card entry before trial activation."

**Reasoning:** "Some other tools" and "ours" are both unnamed. The rewrite names all three entities explicitly, so the claim survives being lifted with zero surrounding context — a reader (or model) doesn't need to know what page this came from to understand who is being compared.

## 8. Risk/warning claim

**Before:** "There can be some issues if you're not careful with permissions."

**After:** "Granting `admin` role instead of `editor` role gives a user the ability to delete the workspace; this is the most common permissions misconfiguration reported in Maximus support tickets."

**Reasoning:** "Some issues" and "not careful" describe nothing specific. The rewrite names the exact roles, the exact consequence, and attributes the frequency claim to a named internal data source (support tickets), which is both atomic and attributable.

## 9. Definitional claim used as a section opener

**Before:** "This next part is about what APIs actually do and why they matter."

**After:** "An API (Application Programming Interface) is a set of defined rules that lets two separate software systems exchange data without either needing to know the other's internal implementation."

**Reasoning:** The original is a meta-sentence about the section, not a claim about the subject — it has zero factual content to extract. The rewrite is a definition-first sentence that itself is the answer to "what is an API," making it the single most liftable sentence in the section per the definition-first pattern in `SKILL.md`.

## 10. Statistic without a source

**Before:** "Most companies say AI has helped their productivity a lot."

**After:** "77% of surveyed companies reported measurable productivity gains from AI adoption in [McKinsey's 2025 State of AI report](https://www.mckinsey.com)."

**Reasoning:** "Most" and "a lot" are unquantified; there's no way to distinguish this from marketing copy. The rewrite supplies an exact percentage, names the survey, the publisher, and the year — turning an unverifiable assertion into an attributable, citable statistic.

## Pattern summary

Across all ten pairs, the same three fixes recur:

1. **Name the subject** — replace "it," "this," "our/ours," "some," and "most" with the actual noun.
2. **Replace judgment words with numbers** — "a lot," "fast," "affordable," "good for you" become specific quantities, dates, or measured outcomes.
3. **Attach a source** — a named study, report, internal data source, or comparison basis, so the claim is checkable rather than asserted.

Apply this same three-step pass to any claim before publishing; see HOWTO recipe (c) for the procedure and recipe (a) for applying it across a full article.

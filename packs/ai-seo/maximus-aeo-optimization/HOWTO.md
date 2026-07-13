# HOWTO — maximus-aeo-optimization

Six recipes. Each assumes `SKILL.md` has already been loaded for context on the six levers and structure patterns.

## (a) Restructure an existing article for AEO

Goal: take a page written for ranking/skimming and rebuild it for extraction, without a full rewrite.

1. **Read the whole draft once** and mark every sentence that states a fact, stat, definition, or recommendation — these are extraction candidates.
2. **Add a TL;DR block** at the top: 2-4 standalone sentences that answer the page's core question without requiring the rest of the page. Write these last, after step 3, so they can borrow the sharpest rewritten claims.
3. **Rewrite each marked sentence as a citation hook** — run it through the three questions in `SKILL.md`'s Citation-hook writing section (names its subject, stands alone, is attributable). See `examples/quotable-claims-trace.md` for the pattern.
4. **Move definitions to the top of their section.** If a section explains a concept, its first sentence should be the definition, not a lead-in.
5. **Convert prose comparisons into a table.** Any paragraph doing "A does X, but B does Y, whereas C..." becomes a comparison table.
6. **Add or tighten an FAQ block** near the end using real questions the page already answers in prose — this doubles as the source for FAQPage schema (recipe b).
7. **Insert dates.** Add a visible "last updated" date and convert vague time references ("recently", "these days") to explicit dates or quarters.
8. **Attribute every stat.** Any number without a named source gets either a citation link or gets cut.
9. **Add schema** matching the page's actual structure (recipe b, and `references/schema-markup-cookbook.md`).
10. **Diff against the original** — confirm you changed structure and sentence-level phrasing, not the underlying facts or claims. AEO restructuring should never introduce new, unverified information.

Full worked example: `examples/aeo-restructure-trace.md`.

## (b) Add FAQPage schema

Goal: mark up an existing FAQ block (or extract one from prose) so answer engines can parse it directly.

1. Identify 3-8 real questions the page answers — pull from existing headers, a "People also ask" pattern, or actual customer questions. Don't invent questions with no real answer in the content.
2. Write each answer as a **self-contained paragraph** (40-300 words) that would make sense with no other context — this is the same discipline as a quotable claim, at paragraph scale.
3. Make sure the question text in the schema matches the question text visible on the page verbatim — mismatched schema/visible-content is a common cause of Google disqualifying the markup.
4. Use the `FAQPage` template in `references/schema-markup-cookbook.md`, filling `name` with the exact question and `text` with the exact visible answer (plain text or minimal HTML per Schema.org's `acceptedAnswer.text` guidance).
5. Place the JSON-LD in the page `<head>` or immediately before `</body>`.
6. Validate with the Google Rich Results Test and Schema.org Validator (both linked in the cookbook) before publishing.
7. Re-check after any content edit — schema silently drifting out of sync with visible text is the most common decay mode for FAQ markup.

## (c) Write quotable atomic claims

Goal: turn a vague, hedged, or context-dependent sentence into one that survives extraction.

1. Isolate the sentence. Read it with nothing before or after.
2. Ask: does it name its subject? If it says "it," "this," or "the company" without the name in the same sentence, add the name.
3. Ask: is it one fact? If it's stacking two claims with "and" or a semicolon, split it.
4. Ask: is it attributable? If it's a stat or claim of fact, attach a source (a study, a named organization, a dated report) either inline or as an adjacent citation.
5. Cut hedge words that add nothing extractable ("can potentially," "in many cases," "it's worth noting that").
6. Re-read in isolation again. If it still needs the paragraph around it to make sense, it's not atomic yet — repeat.
7. Repeat across the page's highest-value claims, not every sentence — over-atomizing filler content wastes effort. Prioritize claims that are the actual answer to a likely user question.

Ten worked before/afters with reasoning: `examples/quotable-claims-trace.md`.

## (d) Audit citation potential per page

Goal: score an existing page on its odds of getting cited, before investing in a rewrite.

1. **Entity clarity check** — sample 5 random sentences from the body. Count how many name their subject explicitly without relying on prior sentences. Target: 4+/5.
2. **Atomic claim count** — count sentences that could be lifted verbatim and still make sense. A page with fewer than 3-5 in its main body is thin on extractable material regardless of length.
3. **Factual density check** — count numbers, dates, and named sources per 300 words. Compare against a competitor page currently being cited for the same query (search the query in Perplexity or ChatGPT and see what's quoted).
4. **Schema presence check** — inspect page source (or a rich-results tool) for FAQPage, HowTo, Article, Organization, Product, or Person schema. Flag pages with zero matching schema as the highest-priority fix.
5. **Source signal check** — is there a named, credentialed author? A visible publish/update date? Outbound citations to primary sources?
6. **Freshness check** — does the page state a date anywhere near its key claims, or is everything undated/evergreen phrasing?
7. **Score and prioritize.** Pages that already rank well but score low on this audit are the highest-ROI AEO targets — the traffic argument is already proven, only the extraction structure is missing.
8. For portfolio-wide prioritization across many pages, hand off to `maximus-ai-seo-strategy`.

## (e) Build an AEO-optimized definition post

Goal: write a new "what is X" / "how does X work" page designed for extraction from the first draft, rather than retrofitted later.

1. Open with a single-sentence, subject-named definition: "X is [category] that [does/means Y]." This sentence alone should answer the query.
2. Follow immediately with 2-3 sentences of elaboration, each atomic and attributable.
3. Add a TL;DR block only if the post is long (800+ words) — for short definition posts the opening paragraph already serves that role.
4. Structure the body around sub-questions a reader would actually ask next ("how is X different from Y," "when should you use X"), each as its own heading with a definition-first answer.
5. Add a comparison table if the concept is commonly confused with an adjacent one.
6. Close with an FAQ block covering the 3-5 most common follow-up questions, written per recipe (b).
7. Add `Article` schema at minimum; add `FAQPage` schema if the FAQ block is present; add `HowTo` schema if any section is a numbered procedure.
8. If the draft doesn't exist yet, use `maximus-write-article` to produce the first pass, then apply this recipe and recipe (a) to structure it for extraction before publishing.

## (f) Monitor which of your pages get cited (handoff to maximus-llm-visibility-tracking)

Goal: close the loop — AEO changes are a hypothesis about what gets cited; only monitoring confirms it.

1. After publishing AEO-restructured pages, record the publish/update date and the specific claims/schema you added — this is the baseline for attribution later.
2. Hand off to `maximus-llm-visibility-tracking` to monitor citation appearances across ChatGPT, Claude, Gemini, Perplexity, and Google AI Overviews for the target queries.
3. This skill does not implement monitoring itself — it produces the artifact (the restructured, schema-marked-up page) that visibility tracking then measures.
4. When visibility tracking reports a page is being cited, note which lever likely drove it (a new FAQ block, a tightened claim, added schema) so future restructuring work prioritizes what's actually working, not just what's theoretically sound.
5. When a page is *not* getting cited despite restructuring, re-run the audit in recipe (d) — the most common causes are missing/mismatched schema, no named author signal, or a competitor page with denser factual attribution for the same query.

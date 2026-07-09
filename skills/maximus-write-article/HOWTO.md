# HOWTO — maximus-write-article

Six recipes for the jobs this skill handles most often. Each recipe assumes `SKILL.md` has been loaded. Load `references/article-structures.md` alongside any recipe that needs a structure or hook decision.

---

## (a) Write a 1500-word thought leadership piece

**When:** The user wants an opinion piece with a clear argument, no code, aimed at a general or builder-adjacent audience.

1. **Frame.** Get the thesis in one sentence from the user, or propose one if they gave you only a topic. Confirm it back before outlining — a wrong thesis wastes the whole draft.
2. **Research.** Run 2-3 `search_web` queries on the topic to surface current data points, counterarguments, and anything published recently that the piece should acknowledge or avoid duplicating. `memory_search` for the user's prior takes on adjacent topics.
3. **Outline.** Hook → thesis statement → 3-4 supporting sections (one concrete example or data point each) → counterargument acknowledged and answered → implication/closing move. Show this outline before drafting.
4. **Draft.** ~1500 words, `write` to a new file. Target section lengths: hook+thesis 150-200 words, each supporting section 250-350 words, counterargument 150 words, close 150-200 words.
5. **Tighten.** One full read-through. Cut generic openers, repeated thesis restatements, and any sentence that hedges without adding information.
6. **Verify.** Every stat and claim gets a citation from Research step 2 or a fresh `search_web` check. List sources at the end of your response (not necessarily in the article body, unless the platform expects inline links).
7. **Ship.** Deliver the file, word count, 3 title alternatives, and the source list.

See `examples/thought-leadership-trace.md` for a full worked run of this recipe.

---

## (b) Write a build-in-public technical writeup

**When:** The user shipped a feature, fixed a hard bug, or made an architecture decision and wants to write about it publicly.

1. **Gather the real material first.** Read the actual code, PR, or commit the post is about (`read`/`grep`/`glob` on the repo, or ask the user for the diff/PR link). Do not write a technical post from a description alone if the code is available — the whole value of build-in-public is that it's true.
2. **Outline** using the fixed structure: problem → approaches considered and rejected → approach taken (with snippet) → tradeoffs accepted → what's next. See `references/article-structures.md` for why this structure specifically works for technical audiences.
3. **Draft.** Pull real code snippets verbatim from the source files — don't retype from memory. If a snippet is simplified for readability, say so explicitly ("simplified for clarity; the actual implementation also handles retries").
4. **Tighten.** Technical readers skim for the snippet and the tradeoff; cut narrative padding around both.
5. **Verify.** Confirm every function name, flag, and version number against the actual source, not recall. If citing external tools/libraries, `search_web`/`fetch_url` their docs to confirm current behavior.
6. **Ship.** Deliver with a note on which snippets are real vs. illustrative, and a "what's next" line that's genuinely planned, not filler.

See `examples/build-in-public-trace.md` for a full worked run.

---

## (c) Tighten a bloated draft

**When:** The user has an existing draft that's too long or reads flabby.

1. `read` the full draft first — never rewrite blind.
2. Pass 1 — structural cut: does every section still serve the thesis (or, for technical posts, the narrative arc)? Cut whole sections that don't.
3. Pass 2 — paragraph cut: for each paragraph, ask "does this advance the argument, deliver an example, or land a transition?" If none, cut it.
4. Pass 3 — sentence cut: hedges ("it could be argued that," "in many ways"), throat-clearing openers, and restated theses go.
5. Use `edit` for each cut — surgical, not a full rewrite — so the user can see exactly what changed if they ask.
6. Report the before/after word count and a one-line summary of what was cut and why.

Target: 10-30% reduction on a typical first draft. If you can't find 10% to cut, you likely didn't read closely enough.

---

## (d) Fact-check claims in a draft

**When:** Before publishing, or when the user explicitly asks for a fact-check pass.

1. `read` the draft and extract every checkable claim: statistics, dates, named studies, competitor claims, quotes, version numbers, "X was the first to."
2. For each claim, run a `search_web` (or `fetch_url` if the user already has a source in mind) to confirm it's accurate and current.
3. Flag three categories in your response: **confirmed** (with source), **needs correction** (with the correct figure and source), and **unverifiable** (recommend cutting or softening to "reportedly" / removing the specific number).
4. Apply corrections with `edit`, not a rewrite.
5. Never publish a piece with an unverifiable specific claim left in as if it were confirmed — soften the language or cut it.

---

## (e) Generate SEO/hook title options

**When:** The draft is done and needs a title, or the user wants headline options before committing to a full draft.

1. Identify the primary keyword/topic and the single strongest claim or outcome in the piece.
2. Generate 5-7 candidates spanning different formulas from `references/article-structures.md` (contrarian, "how to," number-led, "what X taught us," direct claim).
3. Cut to the 3 strongest: one clear/direct, one curiosity-driven, one contrarian/bold.
4. If SEO matters for this platform, check title length (under ~60 characters for search-indexed blogs) and make sure the primary keyword appears in at least one candidate — see `marketing/content-creation` for the full SEO checklist.
5. Present the shortlist with a one-line rationale for each, not just a bare list.

---

## (f) Repurpose a finished article into social/newsletter formats

**When:** The long-form piece is done and needs to become a LinkedIn post, X thread, or newsletter blurb.

1. `read` the finished article.
2. Identify the single most shareable idea — usually the thesis (thought leadership) or the single hardest tradeoff (technical). Repurposing the whole article never works; extracting one idea does.
3. For LinkedIn: 150-250 words, the idea stated in the first two lines (before the "see more" fold), a link to the full piece at the end.
4. For an X/Twitter thread: hook tweet stating the claim, 4-6 follow-up tweets each carrying one supporting point or code snippet, final tweet linking to the full article.
5. For a newsletter blurb: 2-3 sentence teaser plus a "read the full piece" link — do not repeat the article's ending, since that's the reason to click through.
6. Load `marketing/content-creation` for channel-specific tone and length guidance before finalizing.

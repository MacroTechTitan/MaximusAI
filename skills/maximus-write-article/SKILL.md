---
name: maximus-write-article
description: "Write production-grade long-form articles: thought leadership essays and technical/build-in-public writeups. Use when the user says 'write an article', 'blog post', 'thought leadership', 'build in public post', 'technical writeup', 'newsletter post', or asks for a long-form piece (500+ words) meant to be published under their name. Also use for tightening a bloated draft, fact-checking claims, generating headlines/hooks, or repurposing to social/newsletter. Encodes outline-before-draft, tighten-before-ship, fact-check-before-publish discipline so the output reads like a person thought it, not like a model summarized a topic. Do NOT use for short-form copy (use marketing/content-creation), pure docs (use office/docx), internal specs (use pm/feature-spec or maximus-design-spec), or summarization tasks."
metadata:
  pillar: content
  source: maximus
---

# Maximus — Write Article

A first draft is cheap and an unread draft is worthless; the discipline here is the same one that makes code ship — read before you edit, verify before you commit, change the minimum needed to make the next draft better than the last.

## Purpose

Produce long-form articles that read like they came from a specific person who has an opinion and evidence, not from a model that flattened a topic into balanced mush. This skill covers two distinct formats and picks the right structure for the ask, then runs both through the same outline → draft → tighten → verify → ship pipeline.

## The Two Formats

**Thought leadership.** Argument-driven. A claim, a reason the claim is true, evidence, and an implication for the reader. No code. Structure: hook → thesis → 3-4 supporting sections, each with a concrete example or data point → counterargument acknowledged → implication/call to action. Success metric: a reader can restate your one claim after skimming just the headers.

**Technical / build-in-public.** Narrative of shipping something. Structure: problem (what broke or was missing) → approach considered and rejected → approach taken with a code snippet or diagram → tradeoffs accepted knowingly → what's next. Success metric: a reader could reconstruct your decision, not just your output. Code snippets must be real or explicitly marked illustrative — never a hallucinated API dressed up as a working example.

Both formats fail the same way when rushed: hook is generic, middle section restates the hook three times, ending is a limp summary instead of an implication. The workflow below exists to catch that before it ships.

| | Thought leadership | Technical / build-in-public |
|---|---|---|
| Opens with | A claim or tension | A problem or failure |
| Core unit | Argument + evidence | Decision + tradeoff |
| Proof | Data point, example, analogy | Code snippet, metric, diagram |
| Ends with | Implication for the reader | What's next / open question |
| Length | 800-2000 words | 600-2500 words, code included |

## Core Workflow

1. **Outline.** Before writing a sentence of prose, write the skeleton: one-sentence thesis, section headers, one supporting fact/example/snippet per section, and the ending move (implication, next step, or call to action). Show this outline before drafting for anything over ~800 words — cheap to redirect a skeleton, expensive to redirect a draft.
2. **Draft.** Write section by section from the outline. Do not pad. Every paragraph should be doing one job (advance the argument, deliver the example, or land the transition). Use `write` for a fresh draft file; never silently overwrite a draft the user has already edited — `read` it first.
3. **Tighten.** Re-read the full draft in one pass and cut before you polish: kill throat-clearing openers, redundant restatements of the thesis, hedging qualifiers that don't change meaning, and any paragraph that could be deleted without losing an idea. Aim for a measurable cut (10-30% of word count is typical on a first draft). Use `edit` for surgical trims rather than rewriting the whole file.
4. **Verify.** Every factual claim, statistic, quote, product name, or version number must trace to a source. Use `search_web`/`fetch_url` to check anything you didn't personally verify, and cite it inline. Use `memory_search` to pull the user's prior stated opinions, voice notes, or past drafts so the piece sounds like them, not like a generic industry voice. Uncited claims about competitors, numbers, or "studies show" are the single most common way an article gets a correction after publishing.
5. **Ship.** Final read for voice consistency (does paragraph 8 still sound like paragraph 1?), a working title plus 2-3 headline alternatives, and a one-line summary for the platform's preview text. Confirm before publishing anywhere irreversible (a live blog, a newsletter send) — draft-and-hand-off is the default; auto-publish only if explicitly asked.

## Tool mapping (Computer's native tools)

- **Outline and draft**: `write` for new files, `edit` for surgical revisions to an existing draft. Never blind-overwrite a draft the user has been editing — `read` it first, same rule as code.
- **Research and verification**: `search_web` for current facts, statistics, and news; `fetch_url` to pull and read a specific source in full before citing it; `search_vertical` (academic) when the claim needs a paper, not a blog post.
- **Voice and continuity**: `memory_search` for the user's prior published work, stated opinions, and preferred phrasing before drafting — an article that contradicts something the user said last month reads as careless.
- **Structure reference**: `references/article-structures.md` in this skill for proven openings, endings, and full-piece structures (PAS, Problem-Solution-Result, case study, tutorial, listicle).
- **Recipes**: `HOWTO.md` in this skill for the six most common jobs — first draft, technical writeup, tightening, fact-checking, headline generation, repurposing.

## Anti-patterns

- **Drafting without an outline** on anything over 800 words — the fix costs 10x more once it's prose.
- **Restating the thesis as the conclusion.** The ending should add an implication or next step, not summarize what was just read.
- **Uncited numbers.** Any statistic, benchmark, or "X% of companies" claim needs a source found via `search_web`/`fetch_url`, not training-data recall — it may be stale or wrong.
- **Hallucinated code in technical posts.** A snippet in a build-in-public post is read as "this actually happened." If it's illustrative, say so explicitly.
- **Generic hook openers** ("In today's fast-paced world...", "Have you ever wondered..."). See `references/article-structures.md` for hooks that actually work.
- **Skipping the tighten pass** because the draft "reads fine." Every first draft is 15-20% longer than it needs to be; assume this and cut.
- **Ignoring the user's established voice.** Run `memory_search` before drafting if the user has published before — matching their voice beats generic competent prose every time.

## Sibling skills

- **maximus-brain** — run the frame/recall/critique loop around this skill for any article with real stakes (public launch post, anything naming a competitor, anything with financial claims). Brain's Pass 5 self-critique is the hallucination check this skill leans on for Verify.
- **maximus-prompt-engineering** — if the article is *about* prompting, agents, or LLM systems, cross-check technical claims against that skill's reference material rather than reasoning from memory.
- **marketing/content-creation** — use for headline formulas, SEO fundamentals, and channel-specific repurposing (LinkedIn, X, email) once the long-form piece is done. This skill produces the source article; that skill fans it out to short-form.

## Depth calibration

Not every article needs the full five-step pipeline. A 300-word internal Slack update or a quick LinkedIn take can skip straight to Draft and a light Tighten pass. Reserve the full Outline → Draft → Tighten → Verify → Ship sequence for anything that will carry the user's name publicly, cite numbers, or discuss a competitor — the cost of the extra steps is minutes; the cost of skipping them on a public piece is a correction or a retraction.

## Output

A drafted article file in the workspace (`.md` unless the user wants `.docx`/Google Doc, in which case load `office/docx`), plus: word count, list of every external claim with its source URL, 2-3 title alternatives, and a one-line note on what was cut in the tighten pass. If the piece is a technical writeup, also flag which code snippets are real (tested/run) versus illustrative.

---
name: maximus-aeo-optimization
description: "Structure content so LLMs (ChatGPT, Claude, Gemini, Perplexity, Google AI Overviews) cite it or lift it verbatim as an answer. Covers entity clarity, quotable atomic claims, factual density, schema.org markup (FAQPage, HowTo, Article), source signals/E-E-A-T, and freshness. WHEN TO USE: user says 'aeo', 'answer engine optimization', 'get cited by llms', 'llm citation', 'chatgpt citation', 'perplexity citation', 'google ai overview', 'quotable content', 'schema markup for ai', or asks how to get a page cited/quoted/extracted by an AI assistant or AI Overview. WHEN NOT TO USE: keyword ranking work for blue-link SERPs (use maximus-content-seo or maximus-technical-seo), multi-market/multi-language AI-search rollouts (use maximus-geo-optimization), portfolio-level AI-search prioritization (use maximus-ai-seo-strategy), first-draft writing (use maximus-write-article), or tracking cited pages over time (use maximus-llm-visibility-tracking)."
metadata:
  pillar: seo
  source: maximus
---

# Maximus — AEO Optimization

Search engines rank pages. Answer engines extract sentences. AEO is the discipline of writing and marking up content so the extraction step picks *your* sentence, attributes it to *you*, and links back. This skill is the how: which levers move extraction odds, which structures make a paragraph liftable, and which schema tells the crawler what it's looking at.

## Purpose

Give any page the best odds of being the thing an LLM quotes, paraphrases, or cites when a user asks a question it could answer. That means writing for a machine that reads once, extracts a claim, and needs to trust the claim enough to attribute it — not for a human that scans a full page and clicks around.

## Why AEO differs from SEO (extraction vs ranking)

Classic SEO optimizes for **ranking**: get the URL into position 1-10, then a human clicks and reads the whole page. Success is a click.

AEO optimizes for **extraction**: an LLM parses the page once (at crawl/index time or at inference time via retrieval), pulls out a self-contained unit of meaning, and reproduces or paraphrases it in an answer — sometimes with a citation, sometimes without. Success is a citation or a correctly-attributed paraphrase, and the "click" may never happen.

Consequences that fall out of this difference:

- **Sentences compete, not pages.** A page can rank #1 and still lose every citation if its best claim is buried in paragraph 6 with no clear subject.
- **Ambiguity is fatal.** A ranking algorithm tolerates a vague sentence if the surrounding page signals relevance. An extraction step either finds a self-contained, unambiguous claim or skips the page.
- **Attribution requires a name.** LLMs favor claims that come with a nameable source (a person, an organization, a study) because that's what makes a citation defensible.
- **Freshness is read literally.** "Currently," "as of," and explicit dates give the model something concrete to compare against its knowledge cutoff; vague evergreen phrasing gets treated as possibly-stale and skipped.
- **Schema is a machine-readable shortcut.** It lets the model skip inference (what type of thing is this page about?) and go straight to the answer.

SEO and AEO are not opposed — well-structured content tends to help both — but optimizing purely for keyword density and backlinks does nothing for extraction, and can actively hurt it (see Anti-patterns).

## The 6 AEO levers

1. **Entity clarity** — every claim names its subject explicitly (the product, company, person, metric) instead of leaning on pronouns or page-level context. A lifted sentence has to make sense with zero surrounding text.
2. **Quotable atomic claims** — one fact, one sentence, standing on its own. No claim should require the previous sentence to parse.
3. **Factual density** — numbers, dates, named sources, and specifics per paragraph. Filler sentences ("there are many factors to consider") get skipped by extraction; they have nothing to lift.
4. **Schema.org markup** — JSON-LD that tells the crawler the page's type (FAQ, HowTo, Article, Product) and structure, removing the need to infer it.
5. **Source signals / E-E-A-T** — visible author identity, credentials, organization, publish/update dates, and citations to primary sources. Models weight attribution partly on how citable the source itself looks.
6. **Freshness** — explicit, current dates and update markers. A claim timestamped "as of July 2026" beats an identical undated claim when the model is deciding what's still true.

Content that scores high on all six is not a different genre of writing — it's the same good writing disciplined for a reader that extracts instead of skims.

## Content structure patterns

- **Definition-first paragraphs** — open each section with a one-sentence definition of the term/concept before any elaboration. "X is Y" beats three sentences of throat-clearing before the definition arrives.
- **TL;DR / key-takeaway blocks** — a 2-4 sentence summary at the top of long content, written as standalone claims, gives the model a pre-extracted answer.
- **Comparison tables** — structured rows/columns are easier to lift accurately than prose that describes the same comparison; models parse table cells more reliably than parsing "unlike A, B does X but not Y."
- **FAQ blocks** — question-as-heading, answer-as-self-contained-paragraph, directly below. Pair with `FAQPage` schema (see below).
- **Numbered lists with sources** — sequential steps or ranked facts, each with a citation or attribution where the claim came from an external fact rather than the author's opinion.

## Schema types to prioritize

In rough order of citation impact for most content sites:

1. **FAQPage** — direct question/answer pairs are the single highest-leverage schema for AI Overviews and chat-assistant citations.
2. **HowTo** — step-by-step processes; models frequently extract HowTo steps verbatim for "how do I..." queries.
3. **Article** — establishes author, publish date, and headline as structured entities, feeding E-E-A-T signals.
4. **Organization** — anchors the entity behind the content; helps the model attribute claims to a nameable, checkable source.
5. **Product** — for commerce/review content; price, rating, and availability are the facts most often lifted.
6. **Person** — author bios with credentials; strengthens E-E-A-T for expertise-dependent claims (health, finance, legal).

Full JSON-LD templates for all of these, plus BreadcrumbList, are in `references/schema-markup-cookbook.md`.

## Citation-hook writing

A citation hook is a sentence engineered to survive being lifted out of context. Test every candidate claim against three questions:

1. **Does it name its subject?** ("Maximus's AEO skill covers six levers" not "this skill covers six levers").
2. **Does it stand alone?** Read it with nothing before or after — does it still make complete sense and carry a complete fact?
3. **Is it attributable?** Does it carry (or sit next to) a source, date, or named authority a model can cite alongside it?

Claims that pass all three get quoted. Claims that fail get paraphrased loosely or skipped entirely. See `examples/quotable-claims-trace.md` for ten before/after rewrites with reasoning.

## Anti-patterns

- **Walls of text** — long undifferentiated paragraphs with no claim boundary; nothing is atomic enough to lift.
- **Unattributed claims** — statistics or facts with no named source; models discount or skip claims they can't back up with attribution.
- **Missing schema** — leaving the model to infer page type and structure from prose alone, when a template would have told it directly.
- **Keyword stuffing** — repeating a target phrase for ranking purposes degrades readability and produces fewer, not more, quotable sentences.
- **Pronoun-chained claims** — "It improved this by that" sentences that only parse with three sentences of prior context loaded.
- **Buried leads** — the best, most citable claim placed in paragraph 8 instead of the opening definition or TL;DR.

## Sibling skills

- **maximus-geo-optimization** — generative engine optimization across multi-market/multi-language AI search surfaces; load when the AEO work spans more than one locale or engine-specific ranking behavior.
- **maximus-content-seo** — classic on-page SEO (keyword targeting, internal linking, ranking-focused content structure); load for blue-link ranking work that isn't extraction-focused.
- **maximus-technical-seo** — crawlability, site speed, indexation, structured data pipelines at the site-architecture level; load when schema needs to be deployed at scale or crawl issues block indexing.
- **maximus-ai-seo-strategy** — portfolio-level prioritization of which pages/topics to invest AEO effort in; load before this skill when scoping a program across many pages.
- **maximus-write-article** — first-draft long-form writing; load first when the content doesn't exist yet, then apply this skill to restructure the draft for AEO.
- **maximus-llm-visibility-tracking** — monitors which pages actually get cited by which engines over time; load after publishing to close the feedback loop (see HOWTO.md recipe f).

# maximus-write-article

Writes production-grade long-form articles: thought leadership essays and technical/build-in-public writeups. Part of the Maximus skill suite.

## What it does

Runs any long-form writing request through a five-step pipeline — Outline, Draft, Tighten, Verify, Ship — so the output reads like a specific person's argument or engineering log, not a generic industry summary. It picks one of two formats based on what's being asked for:

- **Thought leadership**: argument-driven essay. A claim, evidence, a counterargument acknowledged, an implication for the reader.
- **Technical / build-in-public**: narrative of shipping something. Problem, approach considered and rejected, approach taken (with real or clearly-marked-illustrative code), tradeoffs, what's next.

Both formats get fact-checked against live sources before shipping, not against training-data recall — statistics, competitor claims, and version numbers go through `search_web`/`fetch_url` and get an inline citation.

## When to trigger

- "Write an article about..."
- "Draft a blog post on..."
- "I need a thought leadership piece on..."
- "Write a build-in-public post about shipping X"
- "Write a technical writeup of how we did Y"
- "Draft a newsletter post about..."
- "This draft is too long, tighten it"
- "Fact-check this article before I publish"
- "Give me some headline options for this piece"

Not for: single social posts or ad copy (use `marketing/content-creation`), internal specs/PRDs (use `pm/feature-spec`), or plain documentation (use `office/docx`).

## Quick example

**Prompt:** "Write a 1200-word thought leadership piece arguing that vibe-coding doesn't scale past prototype."

**What happens:**
1. Outline drafted and shown first: thesis, four section headers, one example per section, closing implication.
2. Full draft written to a file in the workspace.
3. Tighten pass cuts ~15% (throat-clearing intro, one redundant section).
4. Every claim about AI-generated code failure rates or incidents is checked via `search_web` and cited.
5. Final file delivered with word count, source list, and 3 title alternatives.

See `examples/thought-leadership-trace.md` for the full worked trace, and `examples/build-in-public-trace.md` for the technical-format equivalent.

## Files in this skill

- `SKILL.md` — the core workflow and rules.
- `HOWTO.md` — six concrete recipes (first draft, technical writeup, tightening, fact-checking, headlines, repurposing).
- `examples/thought-leadership-trace.md` — worked example, argument-driven format.
- `examples/build-in-public-trace.md` — worked example, technical format.
- `references/article-structures.md` — proven structures, hooks, and endings reference.

## Related skills

- **maximus-brain** — the frame/recall/critique loop this skill runs inside of for anything with real publishing stakes.
- **maximus-prompt-engineering** — cross-check technical accuracy for articles about prompting, agents, or LLM systems.
- **marketing/content-creation** — headline formulas, SEO fundamentals, and repurposing a finished article into short-form social/email.
- **office/docx** — when the deliverable needs to be a Word document or Google Doc instead of a markdown file.

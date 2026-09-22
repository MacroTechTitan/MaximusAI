# Lovable prompt — MaximusAI site

This document is the source of truth for the live site. Edit it first, then paste
its blocks into Lovable.

**Live site:** [maximus.macrotechtitan.com](https://maximus.macrotechtitan.com) (Lovable-managed)
**Repo source of truth:** [MacroTechTitan/MaximusAI](https://github.com/MacroTechTitan/MaximusAI)
**Total skills:** 51 across 5 pillars + 3 opt-in packs (38 in `skills/`, 7 in `packs/ai-seo/`, 1 in `packs/devops/`, 5 in `packs/film/`)
**Last updated:** 2026-09-22

## How to use this file

Both blocks below describe the **current desired state of the site**, not a diff
against the last release. Paste them in order and the site converges on that
state regardless of how many releases the site has fallen behind.

That property is deliberate. Earlier versions of this file accumulated
release-by-release delta instructions ("add this card", "remove the NEW tag from
that one") which contradicted each other after four releases and could not be
pasted safely without a human reconciling them first. If you find yourself adding
a "remove the X from last time" instruction, put the correct end state in the
block instead and record the change in the changelog at the bottom.

**Before pasting, check what the live site actually shows.** It has silently
failed to receive an update at least once. Do not assume the site matches this
file.

---

## Block 1 — homepage

```
Update the MaximusAI homepage to feature the full 51-skill Maximus suite across
5 pillars and 3 opt-in packs. Match the existing visual language exactly — do
not redesign, do not introduce new fonts, colors, gradients, or layouts. This
prompt describes the desired end state of the page; bring the page to it.

## Counts, headline, and SEO

- Suite headline: "51 skills. 5 pillars. 3 packs. One workhorse."
- Subhead: "Each skill is a self-contained instruction set an AI agent loads on
  demand. No dead weight, no hand-waving. Built for engineers, founders,
  scientists, and working filmmakers."
- Update every hero, nav, badge, and footer instance of the skill count to 51.
- Title tag and Open Graph title: "MaximusAI — 51 skills for AI-native engineers
  and working filmmakers"
- Meta and Open Graph description: "A suite of 51 AI agent skills across
  engineering, AI, research, people-finding, SEO, and feature-film production.
  Built for engineers, founders, scientists, and working filmmakers."
- Canonical: https://maximus.macrotechtitan.com/
- Schema.org: SoftwareApplication with applicationCategory DeveloperApplication.

Do NOT change any number appearing inside a blog post title, date, or excerpt.
Those are dated records.

## Pillar 1: Cognitive OS (1 skill)

- maximus-brain — Cognitive operating system: think-before-act, memory hygiene,
  depth-adaptive execution. The meta-skill that sits above the rest.

## Pillar 2: Build & Ship (10 skills)

- maximus-design-spec — Write a software design spec before code.
- maximus-plan-implementation — Break an approved design into a minimum-change plan.
- maximus-build-feature — Implement features with read-before-edit discipline.
- maximus-code-review — Review diffs and PRs for correctness, security, performance.
- maximus-debug-incident — Reproduce, isolate, hypothesize, fix, regress.
- maximus-eval-and-test — Unit, integration, e2e, and LLM evals.
- maximus-devops-ship — CI/CD, IaC, progressive delivery, rollbacks.
- maximus-fintech-payments — Stripe, webhooks, idempotency, PCI awareness.
- maximus-python-scientific — Reproducible pipelines: pinned deps, fixed seeds.
- maximus-replit-handoff-pro — Production handoffs between Computer and Replit Agent.

## Pillar 3: AI Engineering (17 skills)

- maximus-agent-design — Tool loops, memory, recovery, 3-tier evals.
- maximus-prompt-engineering — Production system prompts, JSON schemas, few-shot.
- maximus-rag-pipeline — Chunking, embeddings, hybrid search, reranking, citation grounding.
- maximus-llm-model-selection — Pick the right model for cost/latency/quality.
- maximus-ai-product-spec — Behavior, evals, staged rollout, kill switch.
- maximus-ai-safety-governance — PII redaction, injection defense, audit logs.
- maximus-ai-data-pipeline — Dataset curation, labeling, DVC, dataset cards.
- maximus-fine-tuning — When to fine-tune vs RAG vs prompt; LoRA, QLoRA, DPO.
- maximus-ai-fluency-for-builders — The meta-skill for delegating well.
- maximus-ai-cost-control — Token economics, prompt caching, $/request budgets.
- maximus-mlops-deploy — Model registry, canary, drift, rollback.
- maximus-ai-ux-patterns — Streaming, citations, confidence, guardrails.
- maximus-k3-model-selection — Decide when Kimi K3 wins vs. Claude Fable 5 /
  GPT-5.6 Sol / Opus 4.8 / GLM-5.2. Benchmark-cited, honest, refuses to
  recommend K3 when fit is worse.
- maximus-k3-self-hosting — Plan and execute a self-hosted K3 deployment on
  vLLM / SGLang / TokenSpeed with MXFP4 weights, preserved-thinking, and a
  license gate.
- maximus-chain-of-verification — Apply factored CoVe as the final layer before
  delivery: draft → independent verification questions → fresh-context answers →
  revise. 40-60% documented hallucination reduction. Never labels a claim
  verified without independent-context confirmation.
- maximus-slm-local-stack — Run a small language model (1B-14B) on hardware you
  own. Hardware-ceiling and KV-cache VRAM math, GGUF quantization tradeoffs,
  runtime selection across Ollama / LM Studio / llama.cpp / MLX / vLLM,
  air-gapped install. Honest about the capability ceiling: private and free, not
  frontier.
- maximus-local-research-assistant — Build a research or study assistant on a
  small local model you can trust. Local RAG with local embeddings, a refusal
  contract tested before anything else, task decomposition that names which steps
  must route to a bigger model, span-level citation, verification before display.
  Private, offline, and honest about its range.

## Pillar 4: Writing, Research & People-Finding (10 skills)

- maximus-write-article — Long-form articles: thought leadership + technical builds.
- maximus-deep-research — Multi-source synthesis and competitive intelligence.
- maximus-deep-research-pro — Inference-driven research: hypothesis-first,
  adversarial verification, confidence ledger.
- maximus-investigative-research — Research the way a working journalist or
  intelligence analyst does it: source tiers (primary/secondary/adversarial),
  timeline construction, contradiction hunt, corroboration pass. Produces a story
  with a spine, not a topic summary.
- maximus-literature-review — Systematic literature review with PRISMA-style
  flow, inclusion/exclusion criteria, quality appraisal (RoB 2 / NOS /
  ROBINS-I / field-adapted), and GRADE confidence per finding.
- maximus-people-finder — Deep 7-step agent for investors, journalists,
  partners, board members, experts.
- maximus-people-finder-recruiter — Deep 8-step recruiter agent for candidate sourcing.
- maximus-counterparty-discovery — Finance-grade counterparty discovery: SEC
  filings, court dockets, source-by-source provenance, compliance gate before
  outreach.
- maximus-contact-intelligence — Find the most likely professional business email
  from a LinkedIn URL, with pattern discovery, verification, and confidence
  scoring. Never labels a guess as verified.
- maximus-transaction-analyst — Turn a dense deal folder (emails, term sheets,
  closing docs, wires) into a two-page executive transaction memo. Reconstructs
  chronology, reconciles numbers, separates facts from allegations. Never fills
  factual gaps with outside knowledge.

## Pillar 5: AI SEO Pack (7 skills, opt-in)

Headline: "AI SEO Pack — opt-in"
Subhead: "Get cited by ChatGPT, Perplexity, Google AI Overviews, and Copilot.
Answer Engine Optimization + Generative Engine Optimization + classical
technical SEO, unified."

- maximus-ai-seo-strategy — The strategy layer.
- maximus-aeo-optimization — Answer Engine Optimization for LLM answers.
- maximus-geo-optimization — Generative Engine Optimization for Perplexity, SGE, Copilot.
- maximus-technical-seo — Core Web Vitals, JSON-LD, crawlability, JS SEO.
- maximus-content-seo — On-page, internal linking, E-E-A-T, refresh cadence.
- maximus-seo-audit — Umbrella audit that ties the pack together.
- maximus-llm-visibility-tracking — Measure citation share across Perplexity,
  ChatGPT, Claude, Gemini, AI Overviews.

## Dev Workflow Pack (1 skill, opt-in)

Directly below the AI SEO Pack, same opt-in pack styling.

Headline: "Dev Workflow Pack — opt-in"
Subhead: "Project-specific delivery skills. Off by default, linked in when you
want them."

- mtt-claude-cursor — Run Claude Code inside Cursor with fewer approval
  interruptions: launch flags, a continuous-execution rule that pre-authorizes
  routine reversible in-repo work, interrupted-session recovery from git state,
  and approval-prompt triage across the two permission layers. Honest about the
  limit: fewer confirmations, not fewer consequences.

## Film Pack (5 skills, opt-in)

Directly below the Dev Workflow Pack, same opt-in pack styling.

Headline: "Film Pack — opt-in"
Subhead: "For working filmmakers. Feature-length only. No shorts. No AI slop.
Console-first, industry-standard formats: Fountain, EDL/AAF/XML, AICP account
codes, DCP, Rec.709/ACES."

- maximus-screenplay-format — Console-first Fountain screenplay authoring;
  industry-standard PDF (Courier Prime 12pt, 1.5" margin) and Final Draft .fdx
  export; runtime estimation.
- maximus-production-schedule — Turn a locked Fountain script into scene
  breakdown, stripboard, one-liner, day-out-of-days. Console-first, a Movie Magic
  alternative.
- maximus-film-budget — AICP/AMPTP account-code budget templating (1000-4700
  series), ATL/BTL, contingency, completion bond, fringes. CSV/XLSX Movie Magic
  round-trip.
- maximus-post-pipeline — Dailies workflow, offline/online conform, EDL/AAF/XML
  round-trip, ACES vs Rec.709, DCP prep, per-buyer deliverables matrix.
- maximus-filmhub-delivery — Prepare, validate, and troubleshoot feature-film
  delivery masters. FFprobe-first, remux-don't-re-encode, attached-thumbnail
  cleanup, WSP/OBA compliance flag.

## Card links

- Core skills: https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/<skill-name>
- AI SEO Pack: https://github.com/MacroTechTitan/MaximusAI/tree/main/packs/ai-seo/<skill-name>
- Dev Workflow Pack: https://github.com/MacroTechTitan/MaximusAI/tree/main/packs/devops/skills/<skill-name>
- Film Pack: https://github.com/MacroTechTitan/MaximusAI/tree/main/packs/film/<skill-name>

## NEW badges — exhaustive

After this update, exactly two cards on the entire page carry a NEW badge:

1. maximus-slm-local-stack
2. maximus-local-research-assistant

Every other card has no NEW badge. Remove any NEW badge not on that list.

## CTA, nav, constraints

Full-width CTA below the pillars:
- Headline: "Try the workhorse."
- Buttons: "Open the repo" → https://github.com/MacroTechTitan/MaximusAI
  and "Read the latest post" → /blog/slm-local-skills

"Blog" appears in the main nav (the page itself comes from the second prompt).

Match brand colors and typography. Do not introduce new fonts, gradients, or
design directions. Preserve WCAG AA contrast and keyboard navigation.
```

---

## Block 2 — blog

Paste after Block 1.

```
Create or update the Blog section on the MaximusAI site. Match the existing
site's visual language. No new design directions. This describes the desired end
state; bring the site to it.

## Blog index

Route: /blog
Layout: list of posts with title, date, and one-line excerpt, newest first.

Eight posts:

1. Title: "Maximus grows to 51 — hallucination is usually an architecture bug"
   Date: 2026-09-22
   Excerpt: "Two skills for small local models: maximus-slm-local-stack for
   hardware, KV-cache VRAM math, quantization and runtime, and
   maximus-local-research-assistant for grounded local RAG with a refusal
   contract, span citations, and verification. The premise: 'it makes things up'
   is usually an architecture bug, not a model bug. Suite now at 51 skills."
   Route: /blog/slm-local-skills
   Source: https://raw.githubusercontent.com/MacroTechTitan/MaximusAI/main/blog/2026-09-22-slm-local-skills.md

2. Title: "Maximus grows to 49 — the Film Pack, for working filmmakers"
   Date: 2026-09-20
   Excerpt: "Five opt-in skills for people who make films with cameras, cast,
   and a call sheet: Fountain screenplay formatting to industry-standard PDF and
   .fdx, scene breakdown to stripboard and day-out-of-days, AICP account-code
   budgeting, post pipeline, and Filmhub delivery. Feature-length only, no AI
   slop. Suite now at 49 skills."
   Route: /blog/film-pack-launch
   Source: https://raw.githubusercontent.com/MacroTechTitan/MaximusAI/main/blog/2026-09-20-film-pack-launch.md

3. Title: "Maximus grows to 44 — the approval treadmill"
   Date: 2026-09-15
   Excerpt: "mtt-claude-cursor — the operating model for development driven by
   Claude Code inside Cursor. Pre-authorizes routine reversible in-repo work,
   keeps hard stops where they belong, recovers interrupted sessions from git
   state, and fixes command shape instead of weakening protections. Suite now at
   44 skills."
   Route: /blog/mtt-claude-cursor
   Source: https://raw.githubusercontent.com/MacroTechTitan/MaximusAI/main/blog/2026-09-15-mtt-claude-cursor.md

4. Title: "Maximus grows to 43 — adding the Transaction Analyst"
   Date: 2026-08-13
   Excerpt: "maximus-transaction-analyst — turn a dense deal folder (emails,
   term sheets, closing docs, wires) into a two-page executive transaction memo.
   Reconstructs chronology, reconciles numbers, separates facts from
   allegations, and names what's still unresolved. Suite now at 43 skills."
   Route: /blog/transaction-analyst
   Source: https://raw.githubusercontent.com/MacroTechTitan/MaximusAI/main/blog/2026-08-13-transaction-analyst.md

5. Title: "Three skills that make Maximus research like a person"
   Date: 2026-08-12
   Excerpt: "maximus-chain-of-verification, maximus-investigative-research, and
   maximus-literature-review — the reasoning-quality layer, the reporter's
   discipline, and the researcher's PRISMA workflow. Suite now at 42 skills."
   Route: /blog/reasoning-and-research-skills
   Source: https://raw.githubusercontent.com/MacroTechTitan/MaximusAI/main/blog/2026-08-12-reasoning-and-research-skills.md

6. Title: "Two Kimi K3 skills join Maximus"
   Date: 2026-07-29
   Excerpt: "maximus-k3-model-selection and maximus-k3-self-hosting — pick the
   right frontier model when K3 is on the shortlist, and run K3 on your own GPUs
   (or honestly decide not to)."
   Route: /blog/kimi-k3-skills
   Source: https://raw.githubusercontent.com/MacroTechTitan/MaximusAI/main/blog/2026-07-29-kimi-k3-skills.md

7. Title: "Maximus grows to 37 — adding Contact Intelligence"
   Date: 2026-07-23
   Excerpt: "A new skill for finding professional business emails from a
   LinkedIn URL — with pattern discovery, verification, and honest confidence
   scoring. Never labels a guess as verified."
   Route: /blog/contact-intelligence
   Source: https://raw.githubusercontent.com/MacroTechTitan/MaximusAI/main/blog/2026-07-23-contact-intelligence.md

8. Title: "Introducing the Maximus Suite — 36 skills for AI-native engineers"
   Date: 2026-07-20
   Excerpt: "36 skills. 5 pillars. One workhorse. The full suite for engineers,
   founders, and scientists building with AI — from cognitive OS to AI SEO."
   Route: /blog/maximus-suite-launch
   Source: https://raw.githubusercontent.com/MacroTechTitan/MaximusAI/main/blog/2026-07-20-maximus-suite-launch.md

## Post pages

A page at each of the eight routes above, fetching content from that post's
Source Markdown URL, rendered as a long-form article with:

- Article title as H1
- Date byline
- Table of contents auto-generated from H2 headings
- Prose max-width around 720px
- Working links preserved (they point to github.com/MacroTechTitan/MaximusAI)
- JSON-LD BlogPosting structured data: headline, datePublished, author
  "Macro Tech Titan", canonical URL
- Bottom CTA: "Try Maximus" → maximus.macrotechtitan.com, "Open the repo" →
  github.com/MacroTechTitan/MaximusAI

## Header and footer

"Blog" in the main nav. Newest post as a small "Latest post" card in the footer.
Do not change existing pages other than the nav and footer. Preserve WCAG AA
contrast and keyboard navigation.
```

---

## After pasting — verify

1. Headline reads 51; no stray older count outside blog excerpts.
2. Pillar 3 shows 17 cards, Pillar 4 shows 10.
3. Exactly two NEW badges on the whole page.
4. Both pack sections use the AI SEO Pack's opt-in styling, not a new design.
5. `/blog` lists eight posts and every post route renders.

Record the paste date in the changelog below. A release is not shipped until the
site shows it.

---

## Release changelog

Newest first. The blocks above always reflect the newest row.

| Date | Total | Change | Pasted to site |
|---|---|---|---|
| 2026-09-22 | 51 | `maximus-slm-local-stack` + `maximus-local-research-assistant` (Pillar 3 → 17), blog post #8 | pending |
| 2026-09-20 | 49 | Film Pack (5 skills, opt-in), blog post #7 | not confirmed |
| 2026-09-15 | 44 | `mtt-claude-cursor` (Dev Workflow Pack), blog post #6 | not confirmed |
| 2026-08-13 | 43 | `maximus-transaction-analyst` (Pillar 4 → 10), blog post #5 | not confirmed |
| 2026-08-12 | 42 | CoVe + investigative-research + literature-review | yes |
| 2026-07-29 | 39 | Two Kimi K3 skills | yes |
| 2026-07-23 | 37 | `maximus-contact-intelligence` | yes |
| 2026-07-20 | 36 | Launch | yes |

**Known drift as of 2026-09-22:** a fetch of the live site showed "42 skills",
Writing/Research at 9, no Dev Workflow Pack, no Film Pack, and no blog page —
meaning four releases in the repo had not reached the site. Pasting both blocks
above closes all four at once. Check the site rather than trusting this table.

---

## When you next update this file

1. Update the totals and last-updated date in the header.
2. Edit the **current-state** blocks: add or remove cards, update the counts in
   the headline, pillar headings, and SEO strings. Do not append delta
   instructions.
3. Replace the NEW-badge list with the exhaustive list for the new release.
4. Add the release blog post to the Block 2 list and renumber.
5. Add a changelog row, with `pending` in the pasted column.
6. Update the README skill catalog and badge to match.
7. If the skill lives in a pack, update that pack's README under `## Skills`
   with the one-line `ln -sfn` enable command.
8. Add the post to `blog/` and to the README blog index.
9. Paste both blocks into Lovable, verify against the five checks above, then set
   the changelog row to the paste date.

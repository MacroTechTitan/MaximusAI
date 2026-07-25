# Lovable prompt — MaximusAI homepage skills update

Paste the block below into Lovable to update the MaximusAI homepage with the current skill catalog. This document is the source of truth: edit it first, then re-paste into Lovable.

**Live site:** [maximus.macrotechtitan.com](https://maximus.macrotechtitan.com) (Lovable-managed)
**Repo source of truth:** [MacroTechTitan/MaximusAI](https://github.com/MacroTechTitan/MaximusAI)
**Total skills:** 36 Maximus skills across 5 pillars (29 in `skills/`, 7 in `packs/ai-seo/`)
**Last updated:** 2026-07-20

---

## Copy-paste prompt for Lovable (homepage skills section)

```
Update the MaximusAI homepage to feature the full 36-skill Maximus suite,
grouped into 5 pillars. Match the existing visual language of the site — do
not redesign — but add or replace the "Skills" section between the hero and
the footer.

## Section: "The Maximus Suite"

Add a headline: "36 skills. 5 pillars. One workhorse."
Add a subhead: "Each skill is a self-contained instruction set an AI agent
loads on demand. No dead weight, no hand-waving. Built for engineers,
founders, and scientists."

## Pillar 1: Cognitive OS (1 skill)

Card grid, 1 card:
- maximus-brain — Cognitive operating system: think-before-act, memory
  hygiene, depth-adaptive execution. The meta-skill that sits above the rest.

Link: https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-brain

## Pillar 2: Build & Ship (10 skills)

Card grid, 10 cards, each with skill name and one-line description:
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

Each card links to: https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/<skill-name>

## Pillar 3: AI Engineering (12 skills)

Card grid, 12 cards:
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

Each card links to: https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/<skill-name>

## Pillar 4: Writing, Research & People-Finding (6 skills)

Card grid, 6 cards:
- maximus-write-article — Long-form articles: thought leadership + technical builds.
- maximus-deep-research — Multi-source synthesis and competitive intelligence.
- maximus-deep-research-pro — Inference-driven research: hypothesis-first, adversarial verification, confidence ledger.
- maximus-people-finder — Deep 7-step agent for investors, journalists, partners, board members, experts.
- maximus-people-finder-recruiter — Deep 8-step recruiter agent for candidate sourcing.
- maximus-counterparty-discovery — Finance-grade counterparty discovery: SEC filings, court dockets, source-by-source provenance, compliance gate before outreach. NEW.

Each card links to: https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/<skill-name>

Highlight the "NEW" tag on maximus-counterparty-discovery.

## Pillar 5: AI SEO Pack (7 skills, opt-in)

Add a headline for this section: "AI SEO Pack — opt-in"
Add a subhead: "Get cited by ChatGPT, Perplexity, Google AI Overviews, and Copilot. Answer Engine Optimization + Generative Engine Optimization + classical technical SEO, unified."

Card grid, 7 cards:
- maximus-ai-seo-strategy — The strategy layer.
- maximus-aeo-optimization — Answer Engine Optimization for LLM answers.
- maximus-geo-optimization — Generative Engine Optimization for Perplexity, SGE, Copilot.
- maximus-technical-seo — Core Web Vitals, JSON-LD, crawlability, JS SEO.
- maximus-content-seo — On-page, internal linking, E-E-A-T, refresh cadence.
- maximus-seo-audit — Umbrella audit that ties the pack together.
- maximus-llm-visibility-tracking — Measure citation share across Perplexity, ChatGPT, Claude, Gemini, AI Overviews.

Each card links to: https://github.com/MacroTechTitan/MaximusAI/tree/main/packs/ai-seo/<skill-name>

## CTA

Add a full-width CTA below the pillars:
Headline: "Try the workhorse."
Buttons: "Open the repo" (links to https://github.com/MacroTechTitan/MaximusAI)
         "Read the launch post" (links to /blog/maximus-suite-launch — see blog prompt below)

Match brand colors and typography. Do not introduce new fonts, gradients,
or design directions. Preserve accessibility (WCAG AA contrast, keyboard nav).
```

---

## Copy-paste prompt for Lovable (add a Blog page)

Paste this AFTER the homepage prompt above to add a Blog page.

```
Create a new Blog section on the MaximusAI site.

## Blog index

Route: /blog
Layout: List of posts with title, date, one-line excerpt. Match the existing
site's visual language. No new design directions.

Seed with the first post:
- Title: "Introducing the Maximus Suite — 36 skills for AI-native engineers"
- Date: 2026-07-20
- Excerpt: "36 skills. 5 pillars. One workhorse. The full suite for engineers,
  founders, and scientists building with AI — from cognitive OS to AI SEO."
- Link: /blog/maximus-suite-launch

## Post page

Route: /blog/maximus-suite-launch
Fetch the Markdown content from:
https://raw.githubusercontent.com/MacroTechTitan/MaximusAI/main/blog/2026-07-20-maximus-suite-launch.md

Render as a long-form article with:
- Article title as H1 from the frontmatter
- Date byline
- Table of contents auto-generated from H2s
- Prose max-width around 720px for readability
- Working links to each skill (they point to github.com/MacroTechTitan/MaximusAI)
- CTA at the bottom: "Try Maximus" → maximus.macrotechtitan.com,
  "Open the repo" → github.com/MacroTechTitan/MaximusAI

## Header + footer

Add "Blog" to the main nav.
Add the launch post as a small "Latest post" card in the footer.

Preserve accessibility (WCAG AA), do not change existing pages other than
the nav and footer.
```

---

## SEO metadata to keep in sync

- Homepage title tag: "MaximusAI — 36 skills for AI-native engineers"
- Meta description: "A suite of 36 AI agent skills across engineering, AI, research, people-finding, and SEO. Built for engineers, founders, and scientists."
- Open Graph title: "MaximusAI — 36 skills for AI-native engineers"
- Open Graph description: same as meta description.
- Canonical: https://maximus.macrotechtitan.com/
- Schema.org: `SoftwareApplication` with `applicationCategory: DeveloperApplication`.

Also add JSON-LD `BlogPosting` structured data to the launch post page (title, datePublished, author, image if any, canonical).

---

## When you next update this file

1. Update the skill count and last-updated date at the top.
2. Update the counts in the copy-paste prompts and headline.
3. Add or remove skill cards in the correct pillar.
4. Re-paste both prompt blocks into Lovable.
5. Update the README's skill catalog to match.

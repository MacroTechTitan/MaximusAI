# Lovable prompt — MaximusAI homepage skills update

Paste the block below into Lovable to update the MaximusAI homepage with the current skill catalog. This document tracks what the site should show, so future updates edit this file first, then re-paste.

**Repo source of truth:** [MacroTechTitan/MaximusAI](https://github.com/MacroTechTitan/MaximusAI)
**Total skills:** 35 Maximus skills across 5 pillars (28 in `skills/`, 7 in `packs/ai-seo/`)
**Last updated:** 2026-07-15

---

## Copy-paste prompt for Lovable

```
Update the MaximusAI homepage to feature the full 35-skill Maximus suite,
grouped into 5 pillars. Match the existing visual language of the site — do
not redesign — but add a new "Skills" section (or replace the current one if
present) between the hero and the footer.

## Section: "The Maximus Suite"

Add a headline: "35 skills. 5 pillars. One workhorse."
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
- maximus-debug-incident — Systematic debugging and SRE-style incident response.
- maximus-eval-and-test — Design test and eval strategy (unit, integration, e2e, LLM evals).
- maximus-devops-ship — CI/CD, IaC, progressive delivery, observability, rollback.
- maximus-fintech-payments — Payments, billing, and Stripe integrations with PCI awareness.
- maximus-python-scientific — Reproducible Python pipelines for ML and data.
- maximus-replit-handoff-pro — Generate production-grade Replit Agent handoff docs.

Link base: https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/{skill-name}

## Pillar 3: AI Engineering (12 skills)

Card grid, 12 cards:
- maximus-agent-design — Multi-step AI agents: tool loops, memory, recovery, eval.
- maximus-prompt-engineering — Production system prompts, few-shot, JSON schemas.
- maximus-rag-pipeline — Chunking, embeddings, vector DBs, hybrid search, reranking.
- maximus-llm-model-selection — Pick the right model: cost, latency, quality, routing.
- maximus-ai-product-spec — Spec an AI feature end-to-end: behavior, evals, rollout.
- maximus-ai-safety-governance — PII redaction, prompt injection defense, audit logs.
- maximus-ai-data-pipeline — Dataset curation, labeling, synthetic data, DVC.
- maximus-fine-tuning — When to fine-tune vs RAG vs prompting; LoRA, QLoRA, DPO.
- maximus-ai-fluency-for-builders — Meta-skill for using AI well on real tasks.
- maximus-ai-cost-control — Token economics, prompt caching, $/request budgets.
- maximus-mlops-deploy — Model registry, canary deploys, drift detection, rollback.
- maximus-ai-ux-patterns — Streaming, citations, confidence, guardrails, error states.

Link base: https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/{skill-name}

## Pillar 4: Writing, Research, and People-Finding (5 skills)

Card grid, 5 cards, slightly featured (these are newer):
- maximus-write-article — Long-form articles: thought leadership + build-in-public.
- maximus-deep-research — Multi-source synthesis and competitive intelligence.
- maximus-deep-research-pro — Inference-driven research: hypothesis-first,
  adversarial verification, cross-source inference, confidence ledger.
- maximus-people-finder — Deep 7-step agent for investors, journalists,
  partners, board members, subject matter experts.
- maximus-people-finder-recruiter — Deep 8-step recruiter agent for candidate
  sourcing across any employer type.

Link base: https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/{skill-name}

## Pillar 5: AI SEO Pack (7 skills, opt-in bundle)

Card grid, 7 cards, marked as "Opt-in pack":
- maximus-ai-seo-strategy — Keyword research + topical authority for AI answer surfaces.
- maximus-aeo-optimization — Answer Engine Optimization: get cited by LLMs.
- maximus-geo-optimization — Generative Engine Optimization: get surfaced by
  Perplexity, ChatGPT search, Google AI Overviews, Copilot.
- maximus-technical-seo — Core Web Vitals, crawlability, JSON-LD, JS SEO.
- maximus-content-seo — On-page, internal linking, E-E-A-T, refresh + prune.
- maximus-seo-audit — Umbrella audit skill; dispatches to the other 6.
- maximus-llm-visibility-tracking — Measure citation share across all major LLMs.

Link base: https://github.com/MacroTechTitan/MaximusAI/tree/main/packs/ai-seo/{skill-name}
Pack overview link: https://github.com/MacroTechTitan/MaximusAI/tree/main/packs/ai-seo

## Design guidance

- Keep the existing color palette, typography, and spacing scale. Do not
  introduce new fonts or brand colors.
- Cards should be uniform height, with the skill name as an H3 or equivalent,
  the description as body text, and a subtle "View on GitHub →" link at the
  bottom. External link icon optional.
- Group cards under a small pillar heading (h2 or eyebrow). Pillar heading
  should include the count (e.g. "Build & Ship · 10 skills").
- Use a responsive grid: 3 columns on desktop, 2 on tablet, 1 on mobile.
- No emojis in card copy.
- Do not add stock photography. If a pillar needs an icon, use a simple
  monochrome line icon (lucide-react or similar) that matches existing icons.

## Above the grid

Add a short line right below the section headline:
"Skills load only when their triggers match. You carry no dead weight."

## Below the grid

Add a single CTA row:
- Primary CTA: "Browse all skills on GitHub" → https://github.com/MacroTechTitan/MaximusAI
- Secondary CTA: "Read the README" → https://github.com/MacroTechTitan/MaximusAI/blob/main/README.md

## Also update

- Meta description: "MaximusAI — a 35-skill workhorse kit for AI-native
  engineers. Build, ship, research, write, and get cited by LLMs."
- Open Graph title: "MaximusAI — 35 skills for AI-native engineers"
- Open Graph description: same as meta description.
- If a "Recently added" or "What's new" module exists on the homepage, feature
  the AI SEO pack (7 skills) and maximus-deep-research-pro as the latest.

## Do not

- Do not rewrite the hero.
- Do not change navigation.
- Do not add pricing.
- Do not add testimonials or logos that don't exist.
- Do not add signup forms unless one already exists.
- Do not change the footer.

## Ship checklist

- All 35 skill links resolve to their GitHub folders.
- Mobile layout verified at 375px, 768px, 1024px, 1440px.
- Meta tags updated.
- Lighthouse: no accessibility regressions (contrast, alt text, heading order).
- Deploy preview link posted.
```

---

## Notes for future syncs

- When the skill count changes, edit the copy above (headline count, pillar
  counts, card list) and re-paste to Lovable.
- New pillar? Add a new section following the same structure. Update the
  headline count and the meta description.
- Renamed skill? Update its card copy and link. Do not leave dead links.
- Removed skill? Delete its card and decrement the pillar count.

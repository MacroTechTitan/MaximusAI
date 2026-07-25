---
title: "Introducing the Maximus Suite — 36 skills for AI-native engineers"
date: 2026-07-20
author: Macro Tech Titan
tags: [maximus, ai-agents, skills, seo, aeo, geo, deep-research]
canonical: https://maximus.macrotechtitan.com/blog/maximus-suite-launch
---

# Introducing the Maximus Suite — 36 skills for AI-native engineers

I've been quietly building a kit for the last several weeks. Today I'm putting it in your hands.

**Maximus is a suite of 36 skills for AI-native engineers, founders, and scientists.** Each skill is a self-contained instruction set that an AI agent loads on demand. When the trigger doesn't match, the skill stays out of your context window. When it does, you get an expert workflow — read-before-edit, verify-then-claim, minimum-change discipline — instead of a generic model doing generic things.

You can browse the whole thing at [github.com/MacroTechTitan/MaximusAI](https://github.com/MacroTechTitan/MaximusAI). It's public, open, and organized into five pillars.

## Why skills, not agents

Most "AI agent" products ship one big system prompt and hope it covers everything. That's a mistake. Real work is domain-shaped: reviewing a PR is not the same thing as sourcing an investor, and neither is the same thing as writing a long-form article. If you load all three workflows into every request, you pay for context you don't use — and the model gets worse, because more instructions means more places for attention to leak.

Skills fix this. Each one has explicit triggers (`"debug this incident"`, `"find allocators for this fund"`, `"restructure this article for AEO"`). When the trigger matches, the skill loads. When it doesn't, it stays on disk. You carry no dead weight.

That's the mental model. Here's what's actually in the box.

## Pillar 1: Cognitive OS (1 skill)

**[`maximus-brain`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-brain)** — the meta-skill that sits above the rest. It runs a five-pass loop on every non-trivial request (Frame → Recall → Select → Execute → Critique), calibrates depth to the task (Fast/Standard/Deep/Extreme tiers), and enforces memory hygiene so context doesn't rot.

It's boring in the best way. You stop watching the model spin on trivial tasks, and it stops half-answering hard ones.

## Pillar 2: Build & Ship (10 skills)

The traditional engineering loop, but each stage is its own skill:

- [`maximus-design-spec`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-design-spec) — write a design doc before code
- [`maximus-plan-implementation`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-plan-implementation) — break the design into ordered, minimum-change tasks
- [`maximus-build-feature`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-build-feature) — the workhorse skill: read before you edit, change the minimum
- [`maximus-code-review`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-code-review) — severity-tagged findings, no silent rewrites
- [`maximus-debug-incident`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-debug-incident) — reproduce → isolate → hypothesize → fix → regress
- [`maximus-eval-and-test`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-eval-and-test) — unit + integration + e2e + LLM evals
- [`maximus-devops-ship`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-devops-ship) — CI/CD, IaC, progressive delivery, working rollbacks
- [`maximus-fintech-payments`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-fintech-payments) — Stripe, webhooks, idempotency, PCI awareness
- [`maximus-python-scientific`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-python-scientific) — reproducible pipelines, pinned deps, fixed seeds
- [`maximus-replit-handoff-pro`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-replit-handoff-pro) — production-grade handoffs between Computer and Replit Agent

If you build software for a living, these are the skills you'll live in.

## Pillar 3: AI Engineering (12 skills)

Everything you need to build AI features that are actually shippable — not demos:

- [`maximus-agent-design`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-agent-design) — tool loops, memory, recovery, 3-tier evals
- [`maximus-prompt-engineering`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-prompt-engineering) — production system prompts, JSON schemas, few-shot
- [`maximus-rag-pipeline`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-rag-pipeline) — chunking, embeddings, hybrid search, reranking, citation grounding
- [`maximus-llm-model-selection`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-llm-model-selection) — pick the right model for cost, latency, quality
- [`maximus-ai-product-spec`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-ai-product-spec) — behavior, evals, staged rollout, kill switch
- [`maximus-ai-safety-governance`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-ai-safety-governance) — PII redaction, injection defense, audit logs
- [`maximus-ai-data-pipeline`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-ai-data-pipeline) — dataset curation, labeling, DVC, dataset cards
- [`maximus-fine-tuning`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-fine-tuning) — when to fine-tune vs RAG vs prompt; LoRA, QLoRA, DPO
- [`maximus-ai-fluency-for-builders`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-ai-fluency-for-builders) — the meta-skill for delegating well
- [`maximus-ai-cost-control`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-ai-cost-control) — token economics, prompt caching, $/request budgets
- [`maximus-mlops-deploy`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-mlops-deploy) — model registry, canary, drift, rollback
- [`maximus-ai-ux-patterns`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-ai-ux-patterns) — streaming, citations, confidence, guardrails

These are the ones I wish existed before I shipped my first LLM feature. They exist now.

## Pillar 4: Writing, Research, and People-Finding (6 skills)

This is where the suite gets interesting for founders and operators, not just engineers.

- [`maximus-write-article`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-write-article) — long-form articles: thought leadership + build-in-public
- [`maximus-deep-research`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-deep-research) — multi-source synthesis and competitive intelligence
- [`maximus-deep-research-pro`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-deep-research-pro) — **inference-driven** research: hypothesis-first, adversarial verification, cross-source inference, confidence ledger. This one goes beyond search.
- [`maximus-people-finder`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-people-finder) — a deep 7-step agent for finding investors, journalists, partners, board members, subject-matter experts
- [`maximus-people-finder-recruiter`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-people-finder-recruiter) — the recruiter variant: 8-step candidate sourcing across any employer type
- **New today**: [`maximus-counterparty-discovery`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-counterparty-discovery) — finance-grade counterparty discovery with regulator filings, court dockets, source-by-source provenance, and a compliance gate before outreach

`maximus-counterparty-discovery` is the newest addition and worth its own paragraph. If you're allocating capital, raising it, running an M&A search, or building a prospect list that has to survive compliance review, this is the skill for you. It ships with an SEC Form 4 liquidity-parsing example, a managed-futures CTA template, a scoring script, and hard rules: no home addresses in exports, no wealth inference from a single signal, no targeting people because they suffered a bankruptcy. Discovery does not authorize solicitation.

## Pillar 5: AI SEO Pack (7 skills, opt-in)

The big one for this launch, and the one that most builders are missing.

Search is not what it was two years ago. Buyers are asking LLMs. Google is answering questions directly with AI Overviews. Perplexity, ChatGPT search, Claude with web, Copilot — every one of them decides what to cite and what to ignore based on signals that classic SEO tools don't measure.

The pack at [`packs/ai-seo/`](https://github.com/MacroTechTitan/MaximusAI/tree/main/packs/ai-seo) covers the whole surface:

- [`maximus-ai-seo-strategy`](https://github.com/MacroTechTitan/MaximusAI/tree/main/packs/ai-seo/maximus-ai-seo-strategy) — the strategy layer
- [`maximus-aeo-optimization`](https://github.com/MacroTechTitan/MaximusAI/tree/main/packs/ai-seo/maximus-aeo-optimization) — **Answer Engine Optimization**: get cited when LLMs answer a question
- [`maximus-geo-optimization`](https://github.com/MacroTechTitan/MaximusAI/tree/main/packs/ai-seo/maximus-geo-optimization) — **Generative Engine Optimization**: get surfaced by Perplexity, SGE, Copilot
- [`maximus-technical-seo`](https://github.com/MacroTechTitan/MaximusAI/tree/main/packs/ai-seo/maximus-technical-seo) — Core Web Vitals, JSON-LD, crawlability, JS SEO
- [`maximus-content-seo`](https://github.com/MacroTechTitan/MaximusAI/tree/main/packs/ai-seo/maximus-content-seo) — on-page, internal linking, E-E-A-T, refresh cadence
- [`maximus-seo-audit`](https://github.com/MacroTechTitan/MaximusAI/tree/main/packs/ai-seo/maximus-seo-audit) — the umbrella audit that ties the other six together
- [`maximus-llm-visibility-tracking`](https://github.com/MacroTechTitan/MaximusAI/tree/main/packs/ai-seo/maximus-llm-visibility-tracking) — measure your citation share across Perplexity, ChatGPT, Claude, Gemini, and Google AI Overviews

If you publish content in 2026 and you're not measuring your citation rate across LLM answers, you're driving blind. This pack gives you the instrument panel and the tools to move the numbers.

## How to try it

- **Browse:** [github.com/MacroTechTitan/MaximusAI](https://github.com/MacroTechTitan/MaximusAI)
- **Read the README:** the full catalog with direct links to each skill
- **Copy the ones you need:** every skill is a self-contained folder. Fork, adapt, or paste into your own agent stack.

If you're using Perplexity Computer, Claude, or any agent that supports the Anthropic Skills format, the skills load natively. If you're building your own, they read as Markdown — no framework required.

## What's next

I'm treating this as v1. On the roadmap:

- A **compliance pack** for legal/regulated industries (KYC, AML, GDPR/CCPA, SOC 2 evidence)
- A **growth pack** for GTM (positioning, cold outreach, PLG loops, referral engines)
- A **science pack** deeper into reproducible ML research
- More AI-native SEO tooling as LLM search engines evolve

If you build something with these, or if you want a skill I haven't shipped yet, open an issue or ping me.

## The philosophy

I named the suite Maximus because the point isn't to be clever. It's to be a workhorse. Read the file before you edit it. Change the minimum. Verify before you claim. Cite what you use. Ship what works.

Skills are how you take those disciplines out of your own head and encode them so an AI agent — or the next engineer you hire — inherits them by default.

That's what's in the box. Go build.

---

*The full suite lives at [github.com/MacroTechTitan/MaximusAI](https://github.com/MacroTechTitan/MaximusAI). Try Maximus at [maximus.macrotechtitan.com](https://maximus.macrotechtitan.com).*

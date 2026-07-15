<div align="center">

# Maximus 🐴

### The workhorse of Macro Tech Titan.

**Not a model. A workhorse.** You bring the intelligence — Maximus brings the
labor, the tools, and the muscle to execute it.

Free · Open · Ungated, forever · Runs on any model, or a free local one

[maximus.macrotechtitan.com](https://maximus.macrotechtitan.com) · [Quickstart](#quickstart) · [Agents](#agents-standalone-apps) · [For developers](#for-developers)

</div>

---

## What Maximus is

Every company building in AI ships a "model." Macro Tech Titan ships a
**workhorse.**

The distinction is the entire point. A model is intelligence-for-rent — you ask,
it answers, and you hope it decided well. Maximus inverts that. Maximus is not
the intelligence. **You are.** Maximus is the animal that pulls the plough once
*you* set the line: the skills, the tools, the memory, and the tireless execution
that turn what a sharp human already decided into work that actually gets done.

This is our model in the only sense that matters — our *operating model* for how
humans and machines should divide the labor. The machine does not think for you,
decide for you, or replace you. It does the toil: the data operations, the
building, the connecting, the repetitive grind that eats a builder's day. You do
the thinking. **Human-driven, not human-in-the-loop** — you drive, it carries.

> Maximus plows your digital fields and harvests the crops, ships them to store,
> and optimizes the diet along the way. But it doesn't eat for you. It doesn't
> think for you. **You are the rider of the Maximus horse of destiny.**

## Why this matters

The industry keeps promising machines that replace people. We think that's both
wrong and uninspiring. The leverage isn't in a machine that thinks *instead* of
you — it's in one that removes every ounce of toil between your decision and its
execution, and then gets out of the way.

So Maximus is built on a few convictions that don't bend:

- **AI is a tool, not a mind.** It assists and aids; it does not replace human
  judgment. The moment it postures as the one who knows best, it's failing.
- **The human is in command.** Not consulted, not looped-in — in command. Maximus
  executes intent; it doesn't substitute its own.
- **Capability over cleverness.** A brilliant answer that doesn't move the work is
  a failure. A plain one that ships the thing is a win.
- **Free is a feature, not a tier.** Maximus is free, open, and ungated by design
  and forever. The value we maximize is the workhorse itself — and that's all gift.

## Two ways to put Maximus to work

This repo holds two complementary things — the **workhorse kit** (skills you run
locally inside OpenClaw) and **agents** (standalone, deployable web apps). Same
philosophy, different delivery. Use whichever fits the job.

---

## The workhorse kit

Maximus runs on top of [OpenClaw](https://github.com/openclaw/openclaw), an
open-source, local-first assistant gateway. On that foundation it adds the four
things that turn a raw model into a workhorse:

| Pillar | What it is |
|--------|------------|
| **Skills** | Encoded procedures for pulling specific loads — gotchas and all. The deeper the skills, the heavier the work Maximus carries. |
| **Tools / MCP** | Real hands. GitHub, databases, deploy platforms, the web. A horse with no harness pulls nothing. |
| **Context** | Holds the thread of *your* intent across a long job. |
| **Memory** | Remembers so you don't repeat yourself. Makes Maximus yours, not a rental. |

It is **built for technical people** — engineers, builders, founders,
scientists — using the tools they ship. Not retail users. No hand-holding, no
friction you didn't ask for. A power tool for people who know how to use power
tools, with the temperament of a scientist-engineer: rigorous, resourceful, dry
sense of humor, and allergic to hand-waving.

### Skills catalog

The kit ships with skills organized by pillar. Each is a self-contained folder under `skills/` (or `packs/` for opt-in bundles). Skills load only when their triggers match, so you carry no dead weight.

**Cognitive OS**
- [`maximus-brain`](./skills/maximus-brain) — cognitive operating system: think-before-act, memory hygiene, depth-adaptive execution.

**Build & ship (10)**
- [`maximus-design-spec`](./skills/maximus-design-spec) · [`maximus-plan-implementation`](./skills/maximus-plan-implementation) · [`maximus-build-feature`](./skills/maximus-build-feature) · [`maximus-code-review`](./skills/maximus-code-review) · [`maximus-debug-incident`](./skills/maximus-debug-incident) · [`maximus-eval-and-test`](./skills/maximus-eval-and-test) · [`maximus-devops-ship`](./skills/maximus-devops-ship) · [`maximus-fintech-payments`](./skills/maximus-fintech-payments) · [`maximus-python-scientific`](./skills/maximus-python-scientific) · [`maximus-replit-handoff-pro`](./skills/maximus-replit-handoff-pro)

**AI engineering (12)**
- [`maximus-agent-design`](./skills/maximus-agent-design) · [`maximus-prompt-engineering`](./skills/maximus-prompt-engineering) · [`maximus-rag-pipeline`](./skills/maximus-rag-pipeline) · [`maximus-llm-model-selection`](./skills/maximus-llm-model-selection) · [`maximus-ai-product-spec`](./skills/maximus-ai-product-spec) · [`maximus-ai-safety-governance`](./skills/maximus-ai-safety-governance) · [`maximus-ai-data-pipeline`](./skills/maximus-ai-data-pipeline) · [`maximus-fine-tuning`](./skills/maximus-fine-tuning) · [`maximus-ai-fluency-for-builders`](./skills/maximus-ai-fluency-for-builders) · [`maximus-ai-cost-control`](./skills/maximus-ai-cost-control) · [`maximus-mlops-deploy`](./skills/maximus-mlops-deploy) · [`maximus-ai-ux-patterns`](./skills/maximus-ai-ux-patterns)

**Writing, research, and people-finding (5)**
- [`maximus-write-article`](./skills/maximus-write-article) — long-form articles: thought leadership + technical/build-in-public.
- [`maximus-deep-research`](./skills/maximus-deep-research) — multi-source synthesis + competitive intelligence.
- [`maximus-deep-research-pro`](./skills/maximus-deep-research-pro) — **inference-driven** research: hypothesis-first, adversarial verification, cross-source inference, confidence ledger.
- [`maximus-people-finder`](./skills/maximus-people-finder) — deep 7-step agent for investors, journalists, partners, board members, subject-matter experts.
- [`maximus-people-finder-recruiter`](./skills/maximus-people-finder-recruiter) — deep 8-step recruiter agent (candidate sourcing across any employer type).

**AI SEO pack (7, opt-in)** — see [`packs/ai-seo/`](./packs/ai-seo)
- [`maximus-ai-seo-strategy`](./packs/ai-seo/maximus-ai-seo-strategy) · [`maximus-aeo-optimization`](./packs/ai-seo/maximus-aeo-optimization) · [`maximus-geo-optimization`](./packs/ai-seo/maximus-geo-optimization) · [`maximus-technical-seo`](./packs/ai-seo/maximus-technical-seo) · [`maximus-content-seo`](./packs/ai-seo/maximus-content-seo) · [`maximus-seo-audit`](./packs/ai-seo/maximus-seo-audit) · [`maximus-llm-visibility-tracking`](./packs/ai-seo/maximus-llm-visibility-tracking)

### Homepage sync

The live site at [maximusai.macrotechtitan.com](https://maximusai.macrotechtitan.com) is maintained via Lovable. When the skill catalog changes, edit [`docs/lovable-homepage-prompt.md`](./docs/lovable-homepage-prompt.md) first, then paste its **Copy-paste prompt for Lovable** block into Lovable to regenerate the homepage. This keeps the site, README, and skill library in sync.

### Quickstart

Talk to Maximus in minutes. Requires
[OpenClaw](https://docs.openclaw.ai/start/getting-started) (Node 22.19+ or 24).

```bash
git clone https://github.com/MacroTechTitan/MaximusAI.git
cd MaximusAI
./install.sh
```

Then:

1. Edit `memory/memory.md` to teach Maximus about you.
2. Copy `config/openclaw.example.json` → `~/.openclaw/openclaw.json` and pick a
   model — a **free local one** (Ollama, no keys, no bill) or **bring your own**
   API key for frontier quality.
3. Start it: `openclaw gateway`

Talk to it through OpenClaw's built-in WebChat or any connected channel
(Telegram, Slack, Discord, Signal, and more). No custom UI required.

---

## Agents (standalone apps)

Full-stack, deployable agent applications. Each is a self-contained project under
`agents/` — clone the whole repo or copy a single `agents/<name>/` directory into
another project. These are hosted web apps, distinct from the OpenClaw skills of
similar names: the **skill** is a procedure Maximus follows locally; the **agent**
is a hosted implementation you deploy and visit.

| Agent | Description | Stack |
|---|---|---|
| [`recruiter-deep-find`](./agents/recruiter-deep-find) | Recruiter intake form + live deep-search. Sources candidates from DevOps agencies, dev shops, outsourcing firms, MSPs, and technical staffing agencies. | React + Vite, Express, Perplexity Sonar API |
| [`find-shareholders`](./agents/find-shareholders) | Input one or more company names (public or private); get institutional shareholders (funds) and named individuals at those funds. Exports CSVs shaped for Folk and Apollo enrichment. | React + Vite, Express, Perplexity Sonar API |

### Run an agent

```bash
git clone https://github.com/MacroTechTitan/MaximusAI.git
cd MaximusAI/agents/recruiter-deep-find
npm run install:all
cp .env.example .env   # add your API keys
npm run dev
```

See each agent's own README for details.

---

## Why it's free — honestly

The Maximus layer is free forever: persona, skills, memory, tooling. The one cost
no open project can erase is **model inference** — the intelligence you bring
takes compute to run, and compute is never free. So you choose where it comes
from: a **local model** on your own hardware (truly free, no keys), or **your own
API key** (frontier quality, you pay only your own inference). Maximus never gates
a feature behind money or routes you through a paid middleman.

## For developers

```
MaximusAI/
├── core/          SOUL.md · AGENTS.md · TOOLS.md   — Maximus's identity & operating rules
├── skills/        one folder per capability         — followed when a task matches
├── packs/         opt-in domain bundles (off by default)
├── memory/        persistent context store
├── mcp/           external tool wiring
├── config/        example OpenClaw config
├── install.sh     symlinks the kit into ~/.openclaw/workspace
├── CLAUDE.md      build brief for agent-driven development
└── agents/        standalone deployable agent apps
    └── <name>/    self-contained project (client + server)
```

The workhorse **core is generic** — it knows nothing about any specific project.
Everything domain-specific lives in a `pack/` you opt into, so one project pulls
`core` plus the skills it wants while another pulls a different set. **Compose,
don't fork.**

**Build your own skill:** copy `skills/_template/`, write a `SKILL.md` that
encodes a real procedure (the gotchas a generic model would miss — that's the
value), and link it in. See `CLAUDE.md` for the format and quality bar.

## License

MIT. Fork it, extend it, ship it into your own work. The only ask that matches
its spirit: if you keep it public, keep it free.

<div align="center">

---

*The horse pulls. The rider decides. Don't confuse the two.*

**Macro Tech Titan**

</div>

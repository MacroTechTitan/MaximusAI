# Newsletter pitches — 6 outlets, ready to send

Each pitch is 4-6 sentences, tuned to what that specific newsletter covers.
No mass-blast. Send one per day over the launch week, not all at once.

Standard rules for all six:

- **Subject line:** short, specific, no clickbait, no "quick question."
- **Body:** ≤120 words. Newsletter operators read hundreds of pitches
  a week. Anything longer gets deleted.
- **Signature:** name, one-line role, direct repo link.
- **No follow-up before 10 business days.** If they were going to cover
  it, they would have. Two follow-ups max, ever.

---

## Pitch 1 — Simon Willison's Weblog

**To:** swillison@gmail.com (or via his contact page: https://simonwillison.net/about/)
**Subject:** Chain-of-Verification skill with enforced context isolation

Simon —

Long-time reader. I built an open-source skill that implements factored
Chain-of-Verification with the independent-context rule actually enforced —
most implementations skip the isolation step, which is where the ~40-60%
hallucination reduction from Dhuliawala et al. 2023 actually comes from.

It ships as part of Maximus, a 43-skill open-source library (MIT, SKILL.md
format, works with any model). Might be worth a link on the weblog if it
strikes you as useful.

Repo: https://github.com/MacroTechTitan/MaximusAI
CoVe skill directly: https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-chain-of-verification

Joseph
Macro Tech Titan
https://maximus.macrotechtitan.com

---

## Pitch 2 — The Rundown AI

**To:** rowan@therundown.ai (or https://www.therundown.ai/contact)
**Subject:** 43 open-source AI skills — free forever, no signup

Hi Rowan / team —

Shipping-day pitch: I open-sourced a 43-skill library for AI agents
covering cognitive OS, engineering, research, and AI SEO. Model-agnostic
(Claude, GPT, Gemini, Perplexity, local models). MIT-licensed, no signup,
no gate.

The angle for the Rundown audience: it's a practical library, not a
research artifact. Every skill encodes production procedures — the
gotchas a generic model would miss.

Repo: https://github.com/MacroTechTitan/MaximusAI
Homepage: https://maximus.macrotechtitan.com

Happy to write a guest post if useful.

Joseph, Macro Tech Titan

---

## Pitch 3 — Ben's Bites

**To:** ben@bensbites.co (or via https://bensbites.co/newsletter)
**Subject:** Open-source alternative to closed AI skill libraries

Hi Ben —

Reader here. I shipped an open-source library of 43 AI Agent Skills today —
the free, ungated alternative to the closed skill libraries that keep
popping up. MIT-licensed, works with any model.

Structure that might read as newsworthy: five pillars (Cognitive OS,
Build & Ship, AI Engineering, Research/People, AI SEO), 43 skills, one
consistent format. Notable specific skills include factored
Chain-of-Verification (enforced isolation), PRISMA-style literature
review, and a Kimi K3 self-hosting runbook.

Repo: https://github.com/MacroTechTitan/MaximusAI

Cheers,
Joseph, Macro Tech Titan
https://maximus.macrotechtitan.com

---

## Pitch 4 — TLDR AI

**To:** ai@tldr.tech (or https://tldr.tech/contact)
**Subject:** Free 43-skill AI agent library (MIT, Show HN today)

Hi TLDR team —

Quick pitch for the AI section: shipped a 43-skill open-source Agent
library today. MIT-licensed, no signup, model-agnostic. Show HN went
live this morning.

The one-line: "43 skills. 5 pillars. One workhorse."

Notable pieces for a TLDR AI reader: Chain-of-Verification with
enforced context isolation, Kimi K3 model-selection + self-hosting
skills, PRISMA-style systematic literature review, and a 15-skill
AI engineering pillar covering agent design, RAG, model routing,
cost control, and safety.

Repo: https://github.com/MacroTechTitan/MaximusAI
Homepage: https://maximus.macrotechtitan.com

Thanks —
Joseph, Macro Tech Titan

---

## Pitch 5 — Latent Space

**To:** swyx@latent.space (via https://www.latent.space/about)
**Subject:** Skills as the packaging format for AI procedure

Swyx / Alessio —

The "skill" as an atomic unit of AI capability is getting real — Claude
Skills, OpenAI Assistants, MCP — but there's no serious open-source
library that treats them as first-class deliverables with the discipline
you'd apply to open-source code.

I built one. 43 skills across 5 pillars, MIT-licensed, tested against
Claude, GPT, Gemini, Perplexity, and local Llama/Qwen/K3. Repo:
https://github.com/MacroTechTitan/MaximusAI

Might be a good angle for a Latent Space post — "skills as the packaging
format" — happy to do a guest write-up or a pod segment if useful.

Joseph, Macro Tech Titan
https://maximus.macrotechtitan.com

---

## Pitch 6 — Interconnects (Nathan Lambert)

**To:** natolambert@gmail.com (or via https://www.natolambert.com/contact)
**Subject:** Open-source Kimi K3 selection + self-hosting skills

Nathan —

Two skills you might find worth a link: `maximus-k3-model-selection`
(decides when K3 is the right pick vs Claude Fable 5 / Opus 4.8 /
GPT-5.6 Sol / GLM-5.2, benchmark-cited, refuses to recommend K3 when
task fit is worse) and `maximus-k3-self-hosting` (plan and deploy on
vLLM / SGLang / TokenSpeed, MXFP4 weights, license gate).

Part of a 43-skill open-source library (MIT). Repo:
https://github.com/MacroTechTitan/MaximusAI

The honest angle: both skills are willing to *not* recommend K3 when
the evidence doesn't support it. Not many K3 write-ups do that.

Joseph, Macro Tech Titan
https://maximus.macrotechtitan.com

---

## Cadence and follow-up rules

- **Send one pitch per day** starting the morning after launch. HN /
  Reddit / LinkedIn / X go up first; newsletters come the next day when
  they can point to real traction as social proof.
- **Order matters** — start with Simon Willison (most likely to link
  fast, sets the pattern), then Nathan Lambert (fast operator), then
  Latent Space, then the mainstream three (Rundown, Ben's Bites, TLDR).
- **Follow-up cadence:** one polite ping after 10 business days if no
  reply. One final ping 3 weeks later ONLY if the project has new news
  (e.g., "since I wrote, we hit X stars / added skill Y").
- **Never batch-CC or BCC.** Newsletter operators can see it and it kills
  the pitch instantly.
- **Track outcomes in a simple spreadsheet:** outlet, date sent, date
  replied, outcome. After 10 pitches you'll know which framing works.

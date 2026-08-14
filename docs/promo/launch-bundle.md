# Concentrated launch bundle — HN, Reddit, LinkedIn, X

Four assets, tuned per platform, ready to post in one morning. All four
should go up within a 90-minute window so the star flow concentrates and
trips GitHub's trending algorithm (~40 stars in 12 hours is the current
threshold on the AI category).

Order of posting:

1. **8:30 AM PT** — Hacker News (Show HN)
2. **9:00 AM PT** — r/LocalLLaMA
3. **9:15 AM PT** — LinkedIn
4. **9:20 AM PT** — X thread

Tuesday or Wednesday. Never Monday (too much competition) or Friday (audience
already checking out).

---

## Asset 1: Hacker News — Show HN

### Title (exact, 80-char limit)

```
Show HN: Maximus – 43 open-source skills for AI agents (workhorse pattern)
```

### URL field

```
https://github.com/MacroTechTitan/MaximusAI
```

### Text field (leave empty OR use the first comment)

HN discourages promotional text in the body when a URL is provided. Instead,
post the following as **the first comment** immediately after submission
(before anyone else comments). This is standard HN etiquette.

### First comment (post immediately after submission)

```
Author here.

Maximus is 43 open-source Agent Skills (SKILL.md format, MIT). It works with
Claude, GPT, Gemini, Perplexity, and local models (Llama, Qwen, K3).

The pattern I've been iterating on for the last year is what I call the
"workhorse" model. A model is intelligence for rent. A skill is a procedure
the model loads on demand — the specific gotchas a generic model would miss,
which is where the value lives.

Three skills that might be worth a look regardless of whether you use the
rest:

1. maximus-chain-of-verification — factored CoVe with the independent-context
   rule enforced (most implementations skip the isolation step, which is
   where the ~40-60% hallucination reduction from Dhuliawala et al. 2023
   actually comes from). Runs a 4-phase loop: draft → generate verification
   questions → answer each in a fresh context without the draft in view →
   revise. Ships a claim-by-claim confidence ledger.

2. maximus-transaction-analyst — turn a dense private-deal folder (emails,
   term sheets, closing docs, wires) into a two-page executive memo.
   Reconciles numerical changes over time, attributes contested claims,
   prefers executed evidence over indications, never fills factual gaps
   with outside knowledge unless asked. Learned this shape the hard way.

3. maximus-brain — a cognitive OS layer that installs a think-before-act
   loop, memory hygiene, skill selection, and self-critique. It's the
   difference between an agent that runs and an agent that reasons.

The full 5-pillar structure: Cognitive OS (1), Build & Ship (10), AI
Engineering (15), Writing/Research/People (10), AI SEO (7).

Free forever, no signup, no gate, no telemetry. The pitch is: if it's useful
to you and stays useful, that's the whole product.

Happy to answer questions on the format, the workhorse model, or any
individual skill's implementation.
```

### HN posting rules to respect

- **Do not** ask friends to upvote from the same IP or from new accounts.
  HN flags voting rings within minutes and permanently kills submissions.
- **Do** ask friends who are established HN users to genuinely engage —
  ask a real question in a comment, share a real critique.
- Answer every top-level comment within 30 minutes for the first 4 hours.
  This is the single largest factor in whether an HN post survives.
- If it doesn't front-page in 90 minutes, don't panic. Some posts climb
  slowly. Don't repost the same day.

---

## Asset 2: r/LocalLLaMA

### Title

```
I open-sourced 43 Agent Skills that work with any model, including local Llama/Qwen/K3 [MIT, no signup]
```

### Body

```
Been quietly building this for the last year, finally shipped the 43rd skill
today. Full library at https://github.com/MacroTechTitan/MaximusAI (MIT).

It's Agent Skills format (SKILL.md with YAML frontmatter — the same format
Claude Skills uses, portable to OpenAI Assistants, Perplexity, and any
custom orchestrator).

Because r/LocalLLaMA cares about running things locally, the two skills I'd
call out specifically:

**maximus-k3-model-selection** — decides when Kimi K3 (2.8T MoE, 104B active,
1M context, MXFP4 native) is the right pick vs Claude Fable 5, Opus 4.8,
GPT-5.6 Sol, or GLM-5.2. Every recommendation ships with the benchmark that
drove it, the harness, and the date the numbers were pulled. Refuses to
recommend K3 when task fit is genuinely worse.

**maximus-k3-self-hosting** — plan and execute a self-hosted K3 deployment
on your own GPUs. Sizing hardware, choosing vLLM vs SGLang vs TokenSpeed,
native MXFP4 weights with MXFP8 activations, OpenAI/Anthropic-compatible
endpoint, preserved-thinking across turns. Enforces license review before
commercial deployment (K3 License is source-available, not Apache/MIT).

Beyond K3, everything in the library is model-agnostic — you can point it
at your local Llama or Qwen server just as easily as at a hosted API.

Full breakdown of the 43 skills across 5 pillars is in the README. Homepage
(with individual skill cards) is at https://maximus.macrotechtitan.com.

No signup, no telemetry, no upsell, no "free tier with limits." MIT license,
fork it, extend it, ship it into your own work.

Happy to answer questions on any specific skill. Feedback on where the
library is thin welcomed — I'd rather add the skills you actually need
than the skills I imagined.
```

### r/LocalLLaMA rules to respect

- Do not link-dump — the community will kill you.
- Do talk about local specifically (K3, quantization, self-hosting) — that's
  their turf.
- Respond to every top comment. Same rule as HN.

---

## Asset 3: LinkedIn

### Post (approximately 2,900 characters)

```
Two years ago I stopped calling what I build "an AI model."

Everyone ships a model. Every LinkedIn post is a model. Every launch is
a model. And the whole time I kept noticing that the actual value in AI
work wasn't the intelligence — the intelligence is intelligence-for-rent
now, and it's getting cheaper every quarter. The value was the *procedure*.
The specific gotchas a generic model would miss. The read-before-edit
discipline. The reconcile-don't-select reflex on a messy dataset. The
verify-then-commit rhythm on production code.

That's what a workhorse is. That's what Maximus is.

Today the suite passed 43 skills — a milestone I only mention because
it's what makes the shape legible. Five pillars:

Cognitive OS (1): the think-before-act layer that turns any LLM into
an agent that actually reasons.

Build & Ship (10): design specs, implementation planning, feature
building, code review, debugging, testing, DevOps deploys, MLOps, MLOps.

AI Engineering (15): agent design, prompt engineering, RAG, model
selection, fine-tuning, MLOps, cost control, safety, and — the one I'm
most proud of — Chain-of-Verification with enforced context isolation.
The mechanism that reproduces the ~40-60% hallucination reduction from
the Dhuliawala et al. 2023 paper is the *independent context* rule,
which most implementations skip. Maximus doesn't skip it.

Research & People (10): long-form writing, deep research, hypothesis-
driven "research pro," investigative research the way a journalist works
a story, PRISMA-style systematic literature review, transaction analysis
for private deals, people and counterparty discovery.

AI SEO (7): both the classic SEO stack and the new work — getting
your content cited by ChatGPT, Perplexity, Claude, Gemini, and Google
AI Overviews.

Free forever. Open. Ungated. No signup, no telemetry, no upsell.

The pitch is uncomfortable in its simplicity: if it's useful to you and
stays useful, that's the whole product.

If Maximus is useful to your work, a star on the repo helps others find
it. That's the only ask.

Homepage: maximus.macrotechtitan.com
Repo: github.com/MacroTechTitan/MaximusAI

The horse pulls. The rider decides. Don't confuse the two.
```

### LinkedIn posting notes

- Post at 9:15 AM PT (which is 12:15 PM ET) — peak weekday engagement.
- Do not use hashtags at the end. LinkedIn deprioritizes hashtag-stuffed
  posts as of 2025.
- If you want engagement, add a photo — the social preview image works,
  or a screenshot of the README with the badges.
- In the first hour, reply to every comment. LinkedIn's algorithm rewards
  early reply rate more than absolute like count.

---

## Asset 4: X (Twitter) thread — 6 tweets

### Tweet 1 (the hook)

```
2 years ago I stopped calling what I build "an AI model."

Everyone ships a model. The actual value isn't the intelligence — it's
the procedure. Read-before-edit. Reconcile-don't-select. Verify-then-commit.

Today Maximus passed 43 open-source skills.

Free. MIT. No signup.
```

### Tweet 2

```
The core insight: a model is intelligence-for-rent. It gets cheaper every
quarter. What doesn't get commoditized is the specific gotchas a generic
model misses — the shape of a good code review, the shape of a good deal
memo, the shape of a good literature review.

That's the workhorse.
```

### Tweet 3

```
The library is 5 pillars:

• Cognitive OS (1) — think-before-act layer
• Build & Ship (10) — the whole SDLC
• AI Engineering (15) — agents, prompts, RAG, MLOps, cost, safety
• Writing / Research (10) — from long-form to PRISMA lit reviews
• AI SEO (7) — get cited by ChatGPT / Perplexity / Gemini
```

### Tweet 4

```
The skill I'm most proud of: maximus-chain-of-verification.

Factored CoVe with the independent-context rule enforced. Most
implementations skip the isolation step, which is where the actual
40-60% hallucination reduction from Dhuliawala et al. 2023 comes from.

Maximus doesn't skip it.
```

### Tweet 5

```
Works with Claude, GPT, Gemini, Perplexity, and local models (Llama,
Qwen, K3).

Ships in the same SKILL.md format Claude Skills uses. Portable to
OpenAI Assistants. Documented for humans.

No signup. No telemetry. No upsell. No "free tier with limits."
```

### Tweet 6 (the CTA)

```
If the workhorse model resonates:

Homepage: maximus.macrotechtitan.com
Repo: github.com/MacroTechTitan/MaximusAI

A star helps others find it. That's the only ask.

The horse pulls. The rider decides. Don't confuse the two.
```

### X posting notes

- Post the thread all at once (all 6 tweets, chained). Do not "let it
  breathe" between tweets — the algorithm rewards a completed thread
  more than a piecemeal one.
- Do not tag anyone in the thread itself. Reply to your own thread with
  a single "cc @simonw @svpino @LangChainAI — thought this might be
  interesting" as a separate reply, one hour later. Tagging in the
  original thread gets throttled.
- If a tweet lands, quote-tweet it 24 hours later with a specific
  follow-up ("The most common question was X — here's the answer").
  Recycles the audience.

---

## The 90-minute launch morning — minute by minute

**T-24h (Monday evening if launching Tuesday):**
- DM 5-10 friends: "I'm launching a project tomorrow at 9 AM PT. If it's
  useful to you, a star on the repo and an honest comment on HN / Reddit
  / LinkedIn / X would mean a lot. If it's not, no worries."
- Get commitments from 3-5 of them.
- Line up the 4 assets above in draft form on each platform.

**T-30min (8:00 AM PT):**
- Coffee. Phone off notifications. Clear calendar for 4 hours.
- Open all 4 platforms in tabs.

**8:30 AM PT — Post HN.**
- Submit the Show HN.
- Immediately post the first comment (verbatim above).
- DM the friends: "HN is live: [link]. Genuine engagement > upvotes."

**9:00 AM PT — Post r/LocalLLaMA.**
- Same asset, adjusted for their voice.
- DM friends: "Reddit is live: [link]."

**9:15 AM PT — Post LinkedIn.**

**9:20 AM PT — Post X thread.**
- Chain all 6 tweets at once.

**9:30 AM PT to 1:30 PM PT — Answer every comment.**
- Set a rule: no comment goes more than 30 minutes without a reply.
- If a comment is critical, engage with the criticism directly. Do not
  get defensive. "That's a fair point — here's how I've been thinking
  about it, and I'd genuinely welcome the pushback" wins the room.

**End of day:**
- Screenshot the star count.
- Write down what worked and what didn't.
- Do not post again for at least 5 days. Let it settle.

## Realistic outcome

Well-executed, all four channels firing:

- **HN:** 300-800 stars in 24 hours if it front-pages. 50-100 if it lands
  in "New" and stalls.
- **r/LocalLLaMA:** 40-150 stars per top-of-hot day.
- **LinkedIn:** 20-80 stars from your professional network.
- **X:** 30-100 stars if the thread gets picked up by one mid-tier
  account.

Total realistic: **250 to 900 stars in 24-48 hours**, plus /trending
appearance if you clear ~40 in the first 12 hours.

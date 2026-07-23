---
title: "Maximus grows to 37 — adding Contact Intelligence"
date: 2026-07-23
author: Macro Tech Titan
tags: [maximus, contact-intelligence, email-verification, sales, recruiting]
canonical: https://maximus.macrotechtitan.com/blog/contact-intelligence
---

# Maximus grows to 37 — adding Contact Intelligence

Three days after the 36-skill launch, the suite is at 37. The addition is [`maximus-contact-intelligence`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-contact-intelligence): a skill that identifies the most likely professional business email for a person, given a LinkedIn URL or equivalent identity data — with provenance, verification, and honest confidence scoring.

## Why this skill exists

Every builder, founder, and recruiter runs the same loop:

1. Find the person on LinkedIn.
2. Figure out where they work now.
3. Figure out the company's email pattern.
4. Guess the address.
5. Send.

Steps 1 and 5 are easy. Steps 2, 3, and 4 are where credibility either gets built or wrecked. If you send a message to `jane@acmerobotics.com` when the real convention is `jane.doe@acmerobotics.com`, you don't just miss the message — you burn a first impression, and often a domain reputation.

`maximus-contact-intelligence` encodes the discipline that turns steps 2–4 from vibes into evidence:

- **Identity is resolved before any guessing.** If two Jane Does could match, the skill asks for clarification. It does not pick one.
- **Employment currency is checked against a source that is not LinkedIn.** Team pages, press releases, conference bios, filings — because titles change and LinkedIn lags.
- **Email domain is resolved from MX records, not from the website URL.** Many companies host their site at one domain and their mail at another; SPF and DMARC records often tell the truth when the website doesn't.
- **The company's email format is discovered from at least three recent public employee emails.** No `first.last` assumption because most enterprises use it — verify per domain.
- **Catch-all domains are detected and never labeled "verified."** SMTP acceptance on a catch-all is worthless information. The skill scores it as such.
- **Confidence must reach 70 before a "best email" is returned.** If it doesn't, the answer is "no sufficiently reliable professional email was found." No guessing dressed up as certainty.

## What's in the box

The skill ships with:

- Full workflow in `SKILL.md` (12 steps, from URL normalization to result classification)
- `HOWTO.md` with six recipes (single lookup, list enrichment, pattern discovery, ambiguous identity, catch-all handling, LinkedIn-only starting point)
- Two worked examples: a single-person trace and a five-row CRM enrichment
- Reference docs on email pattern taxonomy, verification-check semantics, and authorized-use rules
- Reproducible scripts for candidate generation and score calculation

## Where it fits

`maximus-contact-intelligence` slots into the Writing/Research/People pillar of the Maximus suite:

- Sits next to [`maximus-people-finder`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-people-finder) and [`maximus-people-finder-recruiter`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-people-finder-recruiter) — those find the person; this one finds their email.
- Complements [`maximus-counterparty-discovery`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-counterparty-discovery) — that skill discovers investors and counterparties with a compliance gate; this one handles the outreach-email step after that gate.
- Refuses to defeat access controls, use breached data, or send a test email. Passive verification only.

## What's not in the box

- No personal email hunting. Business email only, unless the user explicitly asks for personal-domain research and the use is permitted.
- No LinkedIn scraping. The skill uses public-source signals; hidden-view data is not fair game.
- No certainty theater. If the evidence isn't there, the confidence score reflects that.

## Try it

- Repo: [github.com/MacroTechTitan/MaximusAI](https://github.com/MacroTechTitan/MaximusAI)
- Live site: [maximus.macrotechtitan.com](https://maximus.macrotechtitan.com)
- The full 37-skill launch post: [Introducing the Maximus Suite](./2026-07-20-maximus-suite-launch.md)

If you build with it and hit an edge case (compound surnames, catch-all quirks, unusual providers), open an issue. This skill improves fastest when it meets the messy edges of real domains.

---

*One workhorse. Read the file before you edit it. Verify before you claim. Cite what you use. That's the Maximus philosophy. `maximus-contact-intelligence` applies it to the last mile of finding people.*

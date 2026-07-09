# Worked trace — Thought Leadership

**Topic:** "The false economy of vibe-coding at scale"
**Format:** Thought leadership (argument-driven, no code)
**Target length:** 1200 words

This trace shows the actual decisions made at each step of the `maximus-write-article` pipeline, including what got cut and why.

---

## 1. Prompt (as given by the user)

> "Write a thought leadership piece arguing that vibe-coding — shipping AI-generated code without review — feels fast but actually costs teams more time than it saves once you're past prototype scale. Should be sharp, a little contrarian, aimed at engineering leaders and builders. ~1200 words."

## 2. Frame (internal, before any tool call)

- **Thesis, restated in one sentence:** Vibe-coding's speed is real at prototype scale and an illusion at production scale, because the debugging and review cost that was deferred always comes due, usually at the worst time.
- **Unknowns:** Is there recent data on AI-code incident rates or review-time studies worth citing? Need to check rather than assume.
- **Audience:** engineering leaders / builders — assume technical fluency, low tolerance for hedging.
- **Depth tier:** Standard — public opinion piece, no financial or legal claims, but do check any statistic before use.

## 3. Research (`search_web`)

Queries run:
- "AI generated code review time study 2025 2026"
- "vibe coding production incidents"
- "code review AI assisted developer survey"

Findings used in the draft (illustrative — in a live run these would carry actual URLs returned by the search):
- A developer survey noting a rise in reported "review fatigue" on AI-assisted PRs.
- Commentary on incident postmortems citing unreviewed AI-generated code as a contributing factor.
- Note: no single authoritative "X% of AI code causes incidents" statistic was found with confidence — decision made to describe the pattern qualitatively rather than invent a number. **This is the fact-check discipline working as intended: absence of a solid stat is a finding, not a gap to paper over with a plausible-sounding figure.**

`memory_search` run for: prior user statements on AI coding tools, prior published pieces, stated opinions on code review. (In this trace, assume none found — proceed cleanly, noted explicitly rather than fabricating a "as I've said before" callback.)

## 4. Outline (shown to user before drafting)

```
Hook: A team ships a feature in an afternoon that used to take a sprint —
      then spends three days finding why it broke in prod.
Thesis: Vibe-coding is a time loan, not a time save, past prototype scale.

Section 1 — Why it feels fast (prototype scale)
  - Constraints are low: no users, no data shape surprises, one person's mental model.
  - This is real and worth conceding, not dismissing.

Section 2 — Where the loan comes due (production scale)
  - Review debt: nobody understands the code well enough to safely change it.
  - Concrete failure pattern: silent edge-case handling that looks right, isn't.

Section 3 — The debugging tax
  - Debugging code you didn't write costs more than debugging code you did,
    even if an AI wrote both — cite the review fatigue finding here.

Section 4 — What actually scales
  - Not "no AI code" — "AI code plus the same review bar as human code."
  - Concrete practice: read-before-merge, minimum-diff review, tests as the
    unit of trust rather than "it ran once."

Counterargument acknowledged: "But reviewing AI code slows down the speed
  advantage that justified using it." Answer: the speed advantage was already
  fake past prototype scale — you're not slowing down a real gain, you're
  making a fake one visible.

Close: Implication for the reader — audit your team's PR review time on
  AI-assisted vs hand-written code before deciding vibe-coding is a net win.
  Don't take the speed claim on faith either way.
```

## 5. Draft (excerpt — opening and closing only, for trace brevity)

**Opening as drafted:**

> A team ships a feature in an afternoon that would have taken a sprint. Everyone's thrilled. Three days later, someone is on a call trying to figure out why a null check that "looked fine" is quietly dropping 4% of transactions — and nobody on the call wrote the code that's failing. They're debugging a stranger's logic, except the stranger is a model, and it can't be asked what it was thinking.
>
> This is vibe-coding's real cost structure: it isn't slower or faster, it's a loan. You get the afternoon back up front. You pay it back later, with interest, and the interest rate goes up the further the code gets from a prototype.

**Closing as drafted:**

> The honest test isn't "did AI-generated code ship faster." It's "how long did the team spend reviewing, debugging, and re-explaining that code six weeks later, compared to code a person wrote and understood from the start." Most teams have never measured that second number. Measure it before you decide vibe-coding is a net win either way — the speed you're proud of might be the same debt you're about to be handed the bill for.

## 6. Tighten pass

Full draft read end-to-end. Cuts made:

- Deleted a generic paragraph after the hook that restated "AI coding tools have become popular" — the reader already knows this; it added nothing.
- Cut a hedge sentence in Section 3 ("it could be argued that this isn't always the case") — it didn't change the argument, just softened it for no reason.
- Merged two short paragraphs in Section 4 that were making the same point twice (once about tests, once about review) into one paragraph that does both.
- Net cut: ~180 words (≈15% of first draft), from 1380 words down to ~1200.

## 7. Verify

- Claim "review fatigue is a reported pattern on AI-assisted PRs" — kept qualitative, no fabricated percentage, source noted for citation in final delivery.
- No competitor or company named — no legal-risk claims to double-check.
- No dollar figures used — avoided a "cost of incidents" number that couldn't be sourced with confidence in the research pass.

## 8. Ship

Delivered: full 1200-word draft file, note that the review-fatigue claim should carry an inline citation to the actual survey URL once identified in a live run, and three title options:

1. "The False Economy of Vibe-Coding at Scale" (direct, chosen as primary)
2. "Vibe-Coding Isn't Free — It's a Loan" (analogy-led)
3. "Why Your Fastest Sprint Might Be Your Most Expensive One" (curiosity-led)

**What this trace demonstrates:** the outline caught a weak structure decision (originally the counterargument was going to be cut entirely — restored during outline review because a thought-leadership piece without an acknowledged counterargument reads as one-sided) before a single paragraph of prose was written. The tighten pass found real, specific cuts rather than a generic "make it shorter" pass. The verify step declined to invent a statistic when the research didn't support one — the single most important discipline in this skill.

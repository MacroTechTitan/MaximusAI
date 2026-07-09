# Reference — Article Structures

A catalog of proven long-form structures, when each fits, and the opening/ending patterns that hold a reader across 1000+ words. Use alongside `SKILL.md`'s Outline step — pick a structure before drafting, don't discover one mid-draft.

---

## Structures

### 1. Problem-Solution-Result (PSR)

**Shape:** Describe a real problem in concrete terms → describe the solution/approach taken → show the measurable result.

**Fits:** Case studies, build-in-public posts, "how we fixed X" writeups, product announcements framed around a customer or internal pain point.

**Skeleton:**
```
Problem   — concrete, specific, ideally with a number or symptom
Solution  — what was tried, what was chosen and why
Result    — what changed, measured if possible
```

**Watch for:** A PSR piece with no number in the Result section reads as an ad, not a case study. If there's genuinely no metric, use a qualitative before/after instead of skipping the section.

---

### 2. PAS (Problem-Agitate-Solution)

**Shape:** State the problem → agitate it (show the cost of not solving it, make it felt) → present the solution.

**Fits:** Persuasive thought leadership, opinion pieces arguing for a change in practice, anything trying to move a reader from indifference to action.

**Skeleton:**
```
Problem  — name it plainly
Agitate  — one or two concrete scenarios of the problem compounding
Solution — the argument's actual thesis, positioned as the way out
```

**Watch for:** Over-agitating reads as manipulative to a technical audience. One or two sharp examples beat five overwrought ones. This is the structure most prone to becoming a listicle of fears — resist that pull.

---

### 3. Listicle

**Shape:** A numbered or bulleted set of independent points under one umbrella claim.

**Fits:** Roundups, "N lessons from X," reference-style pieces meant to be skimmed or bookmarked.

**Skeleton:**
```
Umbrella claim / why this list matters
1. Point — one paragraph, one concrete example
2. Point — one paragraph, one concrete example
...
Close — what ties the list together (not just "in conclusion")
```

**Watch for:** The weakest format for thought leadership because it has no throughline — a reader can disagree with item 3 and stop trusting the whole piece. Best used when items are genuinely independent (a resource roundup), not when they're really one argument chopped into pieces (use PAS or PSR instead).

---

### 4. Case Study

**Shape:** Deep narrative on one specific instance — one customer, one migration, one incident — used to argue a general point.

**Fits:** Technical writeups, sales-adjacent thought leadership, postmortems written for external audiences.

**Skeleton:**
```
Context     — who/what, why it matters, what was at stake
Approach    — what was actually done, in enough detail to be credible
Complication — what didn't go as planned (a case study with no friction reads as fiction)
Outcome     — the result, measured where possible
Generalization — the one lesson a reader outside this specific case should take
```

**Watch for:** Skipping the Complication section is the most common mistake — a frictionless case study is not believable. Include the failed attempt or the surprise.

---

### 5. Tutorial / How-To

**Shape:** Sequential steps toward a defined outcome, each step actionable and checkable.

**Fits:** Technical how-tos, onboarding-style posts, anything where the reader's success is "I did the thing," not "I now believe the thing."

**Skeleton:**
```
Outcome stated up front — what the reader will have by the end
Prerequisites — what they need before starting
Steps — numbered, each independently verifiable (a command, a check, an expected output)
Troubleshooting — the 1-2 most common failure points
Close — what to do next / where this fits in a larger workflow
```

**Watch for:** Steps that can't be verified ("configure it appropriately") aren't steps — they're the reader's problem disguised as your solution. Every step should have a check.

---

## Which structure for which trigger

| User asks for... | Default structure |
|---|---|
| "thought leadership," "opinion piece," "hot take" | PAS |
| "build in public," "how we shipped X," "technical writeup" | PSR or Case Study (PSR if the result is the point; Case Study if the journey is) |
| "N lessons," "roundup," "best tools for X" | Listicle |
| "how to," "step by step," "getting started guide" | Tutorial |
| "postmortem," "what went wrong," "case study" | Case Study |

---

## Opening hooks that work

- **The specific moment.** Open on one concrete scene (a call, an error message, a Slack thread) instead of a general statement about the field. "A team ships a feature in an afternoon..." beats "AI coding tools are changing software development."
- **The counterintuitive claim.** State the thesis backwards from what the reader expects, then earn it. "Vibe-coding isn't fast. It's a loan." Works because it creates a question the rest of the piece answers.
- **The number that doesn't fit the narrative.** A stat that contradicts common wisdom, immediately followed by the explanation. Only use if the number is verified — see `SKILL.md` Verify step.
- **The direct address of a shared frustration.** "If you've ever spent three days debugging code you didn't write, this is why." Works for technical audiences who've lived the problem.

## Openings that don't work (avoid)

- "In today's fast-paced world of..." — generic, signals the rest will be generic too.
- "Have you ever wondered..." — rhetorical question openers read as filler; readers skip to find the actual point.
- Restating the title as the first sentence — wastes the one line you have before a reader decides to keep going.
- Defining a term the audience already knows ("Idempotency, from the Latin idem...") — cut straight to why it matters here.

## Ending patterns that work

- **The implication.** Not a summary — a "so what does this mean for you" that extends past the piece itself. "Measure your team's AI-code review time before deciding vibe-coding is a net win either way."
- **The open next step.** For technical posts: name the next thing genuinely planned, not a vague "stay tuned." A specific, small, credible next step signals the work is real and ongoing.
- **The reframed question.** End by handing the reader a better question than the one they started with, rather than a closed answer.
- **The call back to the opening scene.** If you opened on a concrete moment, returning to it at the close (now re-seen through the article's argument) creates a satisfying loop — use sparingly, once per piece at most.

## Endings that don't work (avoid)

- Restating the thesis verbatim as the last paragraph — if the reader needed a summary, the piece failed to land the first time.
- "In conclusion..." as a literal transition phrase — cut it, the paragraph break already signals the close.
- A call to action disconnected from the piece's actual argument (a generic "subscribe for more" with no bridge from the content).

## Fast decision aid

If you're unsure which structure to reach for, ask: **is the point of this piece an argument or a record?**
- Argument (the reader should believe something new) → PAS or thought-leadership default in `SKILL.md`.
- Record (the reader should know what happened and why) → PSR or Case Study, the build-in-public default in `SKILL.md`.

Both still get the same Outline → Draft → Tighten → Verify → Ship pipeline regardless of which structure is chosen.

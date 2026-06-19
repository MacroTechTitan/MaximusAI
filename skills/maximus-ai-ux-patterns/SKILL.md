---
name: maximus-ai-ux-patterns
description: "UX patterns for AI-powered product features. Use when designing streaming output, source attribution with clickable citations, confidence display, guardrail messaging, retry/edit/undo interactions, input affordances (chat vs form vs hybrid), or error states (rate limit, model down, content filter). Grounded in real product patterns from ChatGPT, Claude, Perplexity, Cursor, and GitHub Copilot."
metadata:
  pillar: ai-engineering
  source: maximus
---

# Maximus — AI UX Patterns

AI output is probabilistic, latent, and occasionally wrong. Standard UI patterns — loading spinners, success/failure states, static text — were built for deterministic systems. AI features need a different vocabulary: streaming, attribution, confidence, graceful refusal, and recoverable edit. Get these wrong and users distrust the feature even when it's right.

## When to use

- Designing any user-facing AI feature for the first time.
- Adding source attribution, confidence display, or streaming to an existing feature.
- Designing error states for model-down, rate-limit, and content-filter scenarios.
- Reviewing a design spec for AI features (use alongside `maximus-design-spec`).
- Building the frontend component for an AI feature (use alongside `maximus-build-feature`).

## Core rules

1. **Show progress, not just a spinner.** Streaming output is the AI equivalent of progress feedback. When streaming isn't possible, use skeleton states with estimated completion time, not an indefinite spinner.
2. **Attribute every factual claim.** If the model cites a source, that source must be clickable and must open the actual content. Non-clickable citations are decorative, not informative, and erode trust faster than no attribution.
3. **Display confidence without false precision.** "Likely" and "I'm not certain" are appropriate confidence signals. A confidence percentage (87.3%) implies calibration the model does not have. Use language, not numbers.
4. **Refuse well.** A guardrail hit is a product moment. Tell the user what you can't do and what you can do instead. Never leave the user with a dead end.
5. **Every AI output is editable.** Retry, edit, copy, thumbs-down — at minimum. Users need agency over AI output, not just passive consumption.

## Procedure

1. **Decide: stream or batch.** Stream when the user is waiting and output is long (>3 seconds to complete). Don't stream when: output must be valid JSON before display, output is short (<1 sentence), or the interaction is async (email, scheduled summary). See HOWTO.md → "How to design streaming output".
2. **Design the attribution layer.** For each factual claim or retrieved chunk: render a superscript citation or inline source chip. On click: open source URL in a new tab or a side panel. Include source title and domain. See `examples/citation-ui.md`.
3. **Design confidence display.** For high-confidence outputs: no qualifier needed. For medium confidence: add a soft qualifier ("Based on available information…"). For low confidence: explicit caveat with a suggestion to verify ("I'm not certain — you may want to check…"). Never show a number.
4. **Design the guardrail state.** Required elements: (a) what can't be done ("I can't help with that"), (b) why (brief, non-judgmental), (c) what can be done instead. Optional: a feedback affordance ("This seems like a mistake? Let us know"). See `references/ux-anti-patterns.md` for failure modes.
5. **Design retry/edit/undo.** Every AI response needs: (a) retry (same prompt, new response), (b) edit (modify the prompt, get a new response), (c) copy-to-clipboard. For writing assistants: add inline edit. For code: add "apply to file" with a diff preview. For long-form: add section-level regeneration.
6. **Design input affordances.** Chat input when: task is open-ended, multi-turn, exploratory. Form input when: task has well-defined parameters, first-time users, mobile. Hybrid (form → chat handoff) when: structured intake + conversational refinement. Don't default to chat for everything — forms reduce error rates for constrained tasks.
7. **Design all error states.** Map each failure mode to a user message and a recovery path:
   - Rate limit: "You've reached your limit for now. [Upgrade] or try again in N minutes."
   - Model down: "Our AI is having a moment. [Try again] or [Contact support]."
   - Content filter: Treat as a guardrail hit (see step 4).
   - Timeout: Show partial results if available; offer retry.
   - Context too long: "This is too long to process in one go. [Summarize and continue] or [Start fresh]."
8. **Preserve state across long interactions.** Auto-save conversation state. Surface a "continue where you left off" entry point. For multi-session workflows: show a progress indicator ("Step 2 of 4 complete"). Never lose user input to a session timeout.

## Real product references

- **Streaming**: ChatGPT token-by-token streaming; Perplexity answer streaming with citation chips appearing as they arrive.
- **Attribution**: Perplexity numbered citations with source panel; Bing Copilot superscript footnotes.
- **Confidence**: Claude's use of "I think", "I believe", "I'm not sure" vs. declarative statements; Perplexity's "Based on search results."
- **Guardrail messaging**: Claude's "I'd rather not help with that, but I can help with X instead"; ChatGPT's policy-reference refusals (less effective — doesn't offer alternative).
- **Retry/edit**: ChatGPT message edit + regenerate; Claude retry button; Cursor inline diff accept/reject.
- **Input affordances**: GitHub Copilot inline completion (zero input, contextual); Cursor command palette (hybrid); Perplexity search (single-line chat).

## Cross-references

- Component implementation: `maximus-build-feature`
- Design spec that precedes UX work: `maximus-design-spec`
- Safety considerations for guardrail design: `maximus-ai-safety-governance`
- AI product specification: `maximus-ai-product-spec`

## Gotchas

- **Streaming JSON** — a partial JSON object is invalid JSON. If the consumer parses as it streams, the parser will throw on every intermediate chunk. Either buffer-then-parse, or stream as NDJSON (one complete object per line).
- **Over-attributing** — a citation on every sentence creates visual noise and implies the model is uncertain about everything. Attribute claims, not filler prose.
- **False precision on confidence** — a percentage implies a calibrated probability. LLMs are not calibrated. Using numbers teaches users to trust a signal that doesn't mean what it says.
- **Guardrail dead ends** — "I can't help with that" with no alternative is a product failure, not a safety win. Always provide a next step.
- **Ignoring the returning user** — designing only the first-run experience. Returning users need quick-start shortcuts, history access, and state persistence.
- **Hiding partial results** — showing nothing until the full response is ready loses the streaming benefit and feels slower than it is. Show partial results as they arrive.

## Output

A UX spec section covering: streaming strategy, attribution design, confidence language guide, guardrail message templates, retry/edit affordances, input mode selection rationale, error state copy, and state persistence approach. Feeds directly into `maximus-design-spec` and `maximus-build-feature`.

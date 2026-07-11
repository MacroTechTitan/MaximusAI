# maximus-ai-ux-patterns

UX patterns for AI features. Streaming, attribution, confidence display, guardrail messaging, retry/edit/undo, input affordances, and error states — the vocabulary of AI UI that standard design systems don't cover.

## What this skill is

AI features break standard UI conventions in four ways: outputs are probabilistic (not always right), generated over time (not instant), potentially refusable (guardrails), and context-dependent (the same input gives different outputs). Each of these requires a new pattern. This skill catalogs those patterns with real product references.

## Why it exists / what problem it solves

Applying standard UI patterns to AI features produces: indefinite spinners instead of streaming, uncited claims instead of attribution, error dialogs instead of graceful refusals, and no edit affordance when the output is wrong. All of these erode user trust — even when the model is performing well.

Real products that get this right (Perplexity, Claude, Cursor, GitHub Copilot, ChatGPT) have converged on patterns that this skill captures and explains.

## Quick start

1. **Decide on streaming vs batch.** Long outputs users wait for → stream. Short outputs or async → batch. See HOWTO.md → "How to design streaming output".
2. **Design attribution.** For every factual claim: superscript citation or inline source chip, clickable, opens source URL. See `examples/citation-ui.md`.
3. **Write your confidence language guide.** Three levels: high (no qualifier), medium ("Based on available information…"), low ("I'm not certain — you may want to verify…"). No percentages.
4. **Design the guardrail state.** What can't be done + why (brief) + what can be done instead. Test this copy with real users before shipping.
5. **Add retry/edit to every AI output.** Minimum: retry (same prompt), edit (modify prompt), copy. Add inline edit and section regeneration for writing features.

## When NOT to use it

- **Non-AI UI design**: for general design patterns, use `maximus-design-spec`.
- **Backend AI architecture**: this skill is UX only. For the model serving layer, use `maximus-mlops-deploy`. For safety and content policy, use `maximus-ai-safety-governance`.
- **Prompt design**: this skill covers the UI surface around AI outputs. For prompt architecture, use `maximus-prompt-engineering`.

## Related skills

- `maximus-design-spec` — General design specification process.
- `maximus-build-feature` — Implementing the components this skill specifies.
- `maximus-ai-safety-governance` — Safety and content policy that determines guardrail triggers.
- `maximus-ai-product-spec` — Product specification that precedes UX work.
- `maximus-prompt-engineering` — Prompt architecture that affects output characteristics (length, format, confidence).

## Glossary

**Streaming** — Delivering model output token-by-token (or chunk-by-chunk) to the user as it is generated, rather than waiting for the full response to complete.

**Attribution** — Linking specific claims in AI output to their source documents. Implemented as superscript citations, inline chips, or a source panel.

**Confidence display** — Communicating the model's uncertainty to the user without implying false calibration. Done via language hedges, not numerical probabilities.

**Guardrail** — A safety or policy constraint that prevents the model from responding to certain inputs. The UX design of a guardrail hit determines whether it's a trust-building moment or a dead end.

**Retry** — Re-running the same prompt to get a different response. Standard affordance for all AI outputs.

**Edit** — Modifying the prompt and re-running. Requires the UI to surface the original prompt for editing, not just the output.

**Shadow DOM streaming** — A React pattern for streaming output: the DOM is progressively updated as tokens arrive, rather than the full response being inserted at once.

**Partial result** — An incomplete but useful intermediate output shown to users while generation continues. Common in search (showing the first result while the rest loads).

**Input affordance** — The UI element that captures user input for an AI feature: chat input, form fields, or a hybrid of both.

# Reference: AI UX Anti-Patterns

A catalog of UX patterns that fail in AI products, with the failure mode, example, and the correct alternative.

---

## Anti-pattern 1: The Indefinite Spinner

**Description**: Showing only a loading spinner while the model generates a response, with no other feedback.

**Failure mode**: Users don't know if the system is working, how long to wait, or whether to retry. Perceived wait time is longer than actual wait time. Users lose trust in the feature.

**Where you see it**: Early chatbots, internal tools that "just added AI."

**Correct alternative**:
- For text responses: stream output token-by-token. First token in <500ms.
- For longer jobs: show a skeleton state with an estimated time ("Usually takes 10–15 seconds").
- For async jobs: confirm submission immediately ("Your report is being generated — we'll email you when it's ready").

**Never**: Show an indefinite spinner for AI generation that takes >3 seconds.

---

## Anti-pattern 2: The Uncited Assertion

**Description**: AI makes factual claims without attribution — no sources, no links, no evidence.

**Failure mode**: Users cannot verify claims. When an error is discovered (and one always is, eventually), trust in the entire feature collapses. Users don't know which claims to trust.

**Where you see it**: AI writing assistants that pull "facts" from training data; summaries without source links.

**Correct alternative**: Cite every factual claim. Make citations clickable. Show the source domain and title. If a claim can't be sourced, frame it as "based on my training" rather than a statement of fact.

**Never**: Include percentage statistics, proper nouns, or specific technical claims without a verifiable source.

---

## Anti-pattern 3: The Confidence Percentage

**Description**: Showing a numerical confidence score (e.g., "Confidence: 87%") alongside AI output.

**Failure mode**: LLMs are not calibrated. A "90% confidence" claim has no meaningful probability interpretation. Users learn to use the number as a proxy for trust, but the proxy is invalid — confidently wrong outputs will show high confidence percentages.

**Where you see it**: Some enterprise AI dashboards; older NLP systems that exposed raw model softmax probabilities.

**Correct alternative**: Use language-based confidence tiers:
- High confidence: declarative statement.
- Medium confidence: "Based on available information…" / "According to most sources…"
- Low confidence: "I'm not certain about this — you may want to verify."

**Never**: Show a confidence percentage for LLM outputs, even if one is technically available.

---

## Anti-pattern 4: The Dead-End Refusal

**Description**: The model refuses a request with a message like "I can't help with that." — with no explanation and no alternative.

**Failure mode**: Users hit a dead end. They don't know why the request was refused, whether it was a mistake, or what to do next. This is the single most trust-damaging interaction pattern in AI products.

**Examples of this pattern** (in real products):
- "I can't assist with that request."
- "That falls outside what I'm able to help with."
- "I'm not able to do that."

**Correct alternative**:
```
What can't be done: "I can't help with [X]."
Why (brief): "That's [outside what I can help with / against our content policy]."
What can be done: "I can help you with [Y] instead — would that be useful?"
Feedback option: "[Was this a mistake? Let us know]"
```

**Never**: A refusal with no alternative path. Every refusal is a product UX moment — design it.

---

## Anti-pattern 5: AI as a Black Box

**Description**: The UI provides no "why" affordance — users see AI output but have no way to understand how it was generated, what sources it used, or why it made a particular choice.

**Failure mode**: Users can't calibrate trust. When something is wrong, they have no starting point for diagnosing it. Power users feel infantilized.

**Where you see it**: AI recommendations, automated decisions, summarization tools without source disclosure.

**Correct alternative**:
- For factual responses: citations (see Pattern 2 above).
- For recommendations: "Why this?" affordance — a one-click explanation of the top factors.
- For generated content: a disclosure label ("AI-generated — review before using") that links to a "how it works" explanation.
- For automated decisions: a summary of the key factors considered.

**Never**: Present AI output as if it were a human-verified fact without any disclosure.

---

## Anti-pattern 6: No Edit Affordance

**Description**: The UI shows AI output but provides no way to modify the prompt and get a different result.

**Failure mode**: When the output is wrong (inevitable), the user has no recovery path. They must start a new session and re-enter their context. Trust in the feature erodes.

**Where you see it**: AI features bolted onto existing apps as a "generate" button with no iteration loop.

**Correct alternative**: Every AI output needs at minimum:
1. **Retry**: same prompt, new response.
2. **Edit**: modify the prompt, re-run.
3. **Copy**: one-click copy to clipboard.

For writing features: add inline edit and section regeneration.
For code features: add accept/reject hunk (diff view before applying).

---

## Anti-pattern 7: Over-Hedging Everything

**Description**: Every AI output includes heavy hedging: "As an AI, I should note that...", "This is just my assessment and may not be accurate...", "Please verify all information...".

**Failure mode**: Users tune out the hedging entirely (the "boy who cried wolf" effect). When a genuine low-confidence output requires a warning, users ignore it. The hedging also makes responses longer and harder to read.

**Where you see it**: AI assistants trained to be excessively cautious; enterprise AI with legal-driven disclaimer mandates.

**Correct alternative**: Reserve hedging language for genuinely uncertain outputs. High-confidence factual claims need no qualifier. Design three explicit confidence tiers and apply them selectively (see SKILL.md → "Display confidence without false precision").

**Never**: Add a blanket disclaimer to every response. Selective, meaningful hedges > uniform, meaningless hedges.

---

## Anti-pattern 8: Streaming JSON

**Description**: Sending a JSON response as a token-by-token stream that the frontend tries to parse progressively.

**Failure mode**: JSON is only valid when complete. Every intermediate chunk is a parse error. Either the parser crashes, or you add complex partial-JSON parsing logic that is fragile and hard to maintain.

**Where you see it**: Developers who correctly want to stream AI output but haven't thought through the JSON constraint.

**Correct alternative**:
- **Buffer and parse**: stream the response, buffer it entirely, parse only when the stream ends. Use this when you need the complete JSON before rendering anything.
- **NDJSON**: newline-delimited JSON — each complete object is on its own line. Safe to parse line-by-line. Use this when you want progressive rendering of a structured list.
- **Separate streaming text from structured data**: stream the prose text progressively; fetch structured metadata (sources, citations, metadata) as a separate JSON request.

---

## Anti-pattern 9: Loss of State on Session Timeout

**Description**: A long AI interaction (research session, document draft, multi-step workflow) is lost when the user's session expires or they close and reopen the browser.

**Failure mode**: Users lose work. They won't start another long session because they don't trust it to persist. Feature adoption collapses for long-form use cases.

**Where you see it**: AI features that store conversation state only in memory, not in a database.

**Correct alternative**:
- Auto-save conversation state to persistent storage after every exchange.
- On return, show a "Continue where you left off" entry point with a summary of what was covered.
- For multi-session workflows: show an explicit progress indicator ("Step 2 of 4 complete").

**Never**: Let an AI interaction session be lost without warning. If a session must expire (for security reasons), warn the user before it happens and offer an export/save option.

---

## Anti-pattern 10: Modal for External Sources

**Description**: When a user clicks a citation or source link, it opens in a modal overlay rather than a new tab.

**Failure mode**: The modal traps the user inside the product. They can't send the URL to a colleague, bookmark it, or open multiple sources in tabs. Modals also frequently break the source's CSS.

**Correct alternative**: Always open external sources in a new tab (`target="_blank"`). If you want to preview the source content inline, use a side panel (not a modal) that the user can dismiss without losing their place in the AI response.

**Never**: Open a third-party URL in a modal. It breaks navigation, sharing, and accessibility.

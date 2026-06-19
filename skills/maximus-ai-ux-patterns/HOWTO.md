# HOWTO — maximus-ai-ux-patterns

Recipes for designing AI-specific UX patterns. Each recipe is a complete, runnable procedure.

---

## Recipe 1: How to design streaming output

**Goal**: Deliver AI output progressively so users see results as they are generated, reducing perceived wait time.

**Steps**:
1. **Decide whether to stream** (this decision matters before any implementation):
   - **Stream when**: output takes >3 seconds to complete, output is long-form text, and the user is waiting synchronously.
   - **Don't stream when**: output must be valid JSON before display (streaming JSON is partial/invalid until complete), output is a single sentence, or the interaction is async (email draft, scheduled summary).
2. **Choose the delivery mechanism**: Server-sent events (SSE) for HTTP, WebSocket for bidirectional interaction. SSE is simpler and sufficient for most AI chat patterns.
3. **Design the progressive rendering**: start rendering the first token immediately. Don't wait for a complete sentence or paragraph. Show a pulsing cursor at the insertion point to signal active generation.
4. **Handle the "last chunk" state**: when the stream ends, transition from the pulsing cursor to a stable settled state. Remove any "generating" indicator. Enable the copy, retry, and edit affordances (they should be disabled or hidden during generation).
5. **Handle stream interruption**: if the user clicks "stop" (offer a stop button during streaming), close the SSE connection and display the partial output as-is. Add a "continue" affordance.
6. **Handle stream errors**: if the stream drops mid-way, show partial output (if any) and a "Something went wrong" state with a retry button. Do not show nothing.
7. **Test on slow connections**: throttle to 50kbps in devtools and confirm the experience is still coherent.

**Verification**: First token appears in <500ms. Cursor pulses during generation. Settled state is clean and controls are enabled after the final token. Stop button cancels the stream. Partial output is shown on error.

**Common pitfalls**:
- Streaming JSON without buffering. Parse only after the stream ends.
- Streaming short responses (single sentence). This adds complexity without benefit — batch is fine.
- Not disabling edit/copy during streaming. A user copying an in-progress output gets a truncated string.

---

## Recipe 2: How to attribute sources in the UI

**Goal**: Link every factual claim to a clickable, verifiable source so users can trust and verify AI output.

**Steps**:
1. **Choose the attribution pattern**:
   - **Superscript citations** (Perplexity pattern): `[1]` inline in text, numbered source list at bottom. Best for dense factual content.
   - **Inline source chips** (conversational pattern): a small chip or badge inline with the sentence. Best for conversational interfaces.
   - **Source panel** (deep research pattern): a side panel listing all sources, visible alongside the output. Best for long documents or research reports.
2. **Ensure every source is a real URL**. Non-clickable citations undermine trust. If a source doesn't have a URL, don't display it as a citation — incorporate the claim as background context.
3. **Display on hover/tap**: show title, domain, and a one-sentence preview on hover (desktop) or tap (mobile). This lets users assess source relevance without leaving the page.
4. **On click**: open in a new tab (not a modal, which traps the user). Optionally anchor to the relevant passage if the URL supports fragment identifiers.
5. **Show source domain with a favicon**: `[1] techcrunch.com` with the TC favicon is faster to parse than a full URL.
6. **For streaming output**: render citation chips as they arrive (Perplexity's model). Don't batch citations to the end — users want to verify claims as they read them.
7. See `examples/citation-ui.md` for a React component implementation.

**Verification**: Every displayed citation is a functional URL that opens the correct source. Hover preview shows title and domain. Citations appear inline at the correct position relative to the claim.

**Common pitfalls**:
- Decorative citations (shown but not linked to sources). These are worse than no citations — they imply verification that doesn't exist.
- Citing the wrong passage. If your RAG system returns 5 chunks, attribute each claim to the specific chunk it came from, not to all 5 sources.
- Over-attributing. Cite claims; don't add a citation to every sentence. Excessive citations create noise that makes users ignore the attribution layer.

---

## Recipe 3: How to display model confidence honestly

**Goal**: Communicate the model's certainty level without implying false precision.

**Steps**:
1. **Define three confidence tiers** for your feature (calibrate to your model's actual behavior via eval):
   - **High confidence**: the model is making a well-supported claim from clear evidence. No qualifier needed.
   - **Medium confidence**: the model is reasoning from partial evidence or the topic has conflicting sources.
   - **Low confidence**: the model is extrapolating, the topic is outside its knowledge, or the query is ambiguous.
2. **Map tiers to language** (never to numbers):
   - High: declarative statement. "The capital of France is Paris."
   - Medium: soft qualifier. "Based on available information…", "According to most sources…"
   - Low: explicit caveat with action suggestion. "I'm not certain about this — you may want to verify with [source type]."
3. **Decide where to display the qualifier**: inline (in the response text) is the Perplexity/Claude pattern. Out-of-band (a badge below the response) is lower-friction but easier to ignore. For important decisions, inline is safer.
4. **Never show a confidence percentage**. A percentage implies a calibrated probability. LLMs are not calibrated at the output level — the number will be wrong and will mislead users.
5. **Write the confidence language guide** for your product. Three examples per tier. Review with a designer. This is product copy, not an afterthought.
6. **Test with users**: show low-confidence outputs with and without qualifiers. Do users act differently? If not, the qualifier is invisible — redesign its prominence.

**Verification**: A user reading low-confidence output is demonstrably more likely to verify the claim before acting on it (measured via user research or A/B test on a follow-up "did you verify?" prompt).

**Common pitfalls**:
- Using percentage numbers. "I'm 73% confident" is not a meaningful signal — it's false precision that teaches users to trust a number that has no ground truth.
- Using the same qualifier for everything. "Based on available information" on every sentence is background noise — users ignore it.
- Hiding low-confidence output entirely. Users should see it with appropriate context, not get a filtered-down response.

---

## Recipe 4: How to handle a guardrail refusal gracefully

**Goal**: When a content policy prevents the model from responding, give the user a useful next step rather than a dead end.

**Steps**:
1. **Identify the refusal type**:
   - **Content policy** (harmful content request): clear refusal is appropriate.
   - **Out-of-scope** (task outside the product's domain): soft redirect.
   - **Ambiguous** (query could be interpreted as policy-violating): ask a clarifying question before refusing.
2. **Structure the refusal message** with three elements:
   - **What can't be done**: one sentence, plain language. "I can't help with that request."
   - **Why** (optional, brief): one clause, non-judgmental. Omit the model/policy citation jargon — users don't care. Optionally: "That's outside what I can help with."
   - **What can be done instead**: the most important part. A concrete alternative action. "I can help you with [X] instead." If there's no alternative in the product, link to documentation or support.
3. **Add a feedback affordance for ambiguous cases**: "Was this a mistake? [Let us know]". This surfaces false positives without requiring users to navigate to a feedback form.
4. **Never show the raw safety classifier output** or internal policy codes to users. "SAFETY_FILTER_TRIGGERED" is not a user message.
5. **Design the visual treatment**: refusal messages should look different from error states. A gentle visual distinction (soft amber background vs. red for errors) signals "this is a policy thing, not a broken thing."
6. See `references/ux-anti-patterns.md` for examples of refusal patterns that fail.

**Verification**: Reading the refusal message, a user understands what to do next without additional explanation. The feedback affordance is visible. The message uses no jargon.

**Common pitfalls**:
- Dead-end refusals with no alternative. "I can't help with that." Full stop. This is the most common and most damaging pattern.
- Lecturing. A three-paragraph explanation of the content policy is worse than a one-line refusal. Users don't read it and feel condescended to.
- Using the same refusal message for all guardrail types. Content policy refusals and out-of-scope refusals need different copy.

---

## Recipe 5: How to design retry/edit interactions

**Goal**: Give users agency over AI output by making retry, edit, copy, and undo feel natural and accessible.

**Steps**:
1. **Define the minimum set of affordances** for your feature:
   - **Retry** (same prompt, new response): required for all AI outputs. Button below the response. Icon: refresh/regenerate.
   - **Edit** (modify the prompt, re-run): required for chat interfaces. On click, the original prompt becomes editable in place. Submit re-runs.
   - **Copy**: required for all text output. One-click copy to clipboard. Show a "Copied!" confirmation for 2 seconds.
   - **Thumbs down / feedback**: strongly recommended. Routes to your quality monitoring pipeline.
2. **For writing assistants, add**:
   - **Inline edit**: select a sentence, right-click or toolbar → "Edit this". Opens a prompt input anchored to that selection.
   - **Section regeneration**: "Regenerate this paragraph." Only that section is replaced; the rest of the document is preserved.
3. **For code generation, add**:
   - **Apply to file**: button that opens a diff view (current file vs AI suggestion). User accepts, rejects, or edits individual hunks. Cursor's accept/reject flow is the reference pattern.
   - **Run in sandbox**: for snippets, offer a one-click "Run this" that executes in an isolated sandbox and shows output inline.
4. **Design undo**: when the user applies AI output (apply to file, insert into document), the action must be undoable with Cmd+Z / Ctrl+Z. AI-applied changes that bypass the undo history are a trust-breaker.
5. **Show affordances at the right time**: hide retry/edit during streaming. Show them immediately when the stream settles. Don't make users hunt for the retry button.
6. **State preservation across retry**: when the user edits and retries, show the original response and the new response side by side (or as a toggle) for the first comparison. After they pick one, collapse to the selected version.

**Verification**: Retry produces a different response for the same prompt. Edit allows prompt modification and re-run without losing context. Undo works after apply-to-file. All affordances are visible within 3 seconds of response settling.

**Common pitfalls**:
- Showing retry/edit during streaming. Users clicking retry on an in-progress response creates a confusing race condition.
- Apply-to-file without a diff view. Blindly replacing file content with AI output is the UX equivalent of blind file overwriting — always show the diff.
- No undo for AI-applied changes. This is the single fastest way to make a user distrust an AI writing feature.

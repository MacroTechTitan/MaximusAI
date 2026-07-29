# HOWTO — maximus-k3-self-hosting

Six recipes for the most common self-hosting questions.

---

## Recipe 1 — "Should I self-host K3 at all?"

**Trigger:** "is self-hosting K3 worth it for us?"

**What the skill does:**
1. Gets volume, latency budget, hardware access, ops maturity.
2. Applies the break-even gate:
   - Volume <100M tokens/day sustained → likely no
   - No dedicated ops bench → likely no
   - Latency budget loose (>5s p99 OK) → hosted API works
3. Recommends `platform.kimi.ai` if the gate does not clear. Says so plainly.
4. Only proceeds to engine choice if self-hosting genuinely fits.

**Workhorse note:** Saying "don't self-host" is a valid answer. Most people asking this question should not.

---

## Recipe 2 — "vLLM vs SGLang vs TokenSpeed"

**Trigger:** "which inference engine should I use for K3?"

**What the skill does:**
1. Points at all three official recipes:
   - [vLLM recipes](https://recipes.vllm.ai/moonshotai/Kimi-K3)
   - [SGLang cookbook](https://docs.sglang.io/cookbook/autoregressive/Moonshotai/Kimi-K3)
   - [TokenSpeed recipes](https://lightseek.org/tokenspeed/recipes/models#kimi-k3)
2. Applies the decision guide from `references/engines-compared.md`:
   - **vLLM** — widest community, most integrations, best if you already run vLLM
   - **SGLang** — structured decoding + agentic tool sequences
   - **TokenSpeed** — K3-specific optimizations
3. Recommends running the recipe end-to-end for one engine before A/B-ing.

---

## Recipe 3 — "What hardware do I need?"

**Trigger:** "how many GPUs to serve K3?"

**What the skill does:**
1. **Does not quote a GPU count from memory.**
2. Points at `references/hardware-sizing.md` — sizing worksheet based on published architecture facts (2.8T total, 104B active, 93 layers, MXFP4 weights, MXFP8 activations, 1M context).
3. Points at the K3 report footnotes noting H20 GPUs were used for benchmark reruns — that is a data point, not a full recommendation.
4. Points at each engine's own recipe for the current published minimums.

**Workhorse note:** Hardware sizing changes as engines improve. The reference file will always be less current than the engine recipe. Trust the recipe.

---

## Recipe 4 — "How do I handle preserved-thinking in my client?"

**Trigger:** "K3 is losing context across turns" / "my agent behaves worse on turn 2+"

**What the skill does:**
1. Diagnoses the #1 K3 integration bug: dropping `reasoning_content` from the assistant message when appending to `messages`.
2. Walks through `examples/smoke-test-preserved-thinking.md` — a 3-turn exchange that fails without preserved-thinking and passes with it.
3. Points at the [Kimi K3 Quickstart](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart) and [Thinking Effort guide](https://platform.kimi.ai/docs/guide/use-thinking-effort).

---

## Recipe 5 — "Latency is too high — how do I tune?"

**Trigger:** "K3 is slow" / "p99 is unacceptable"

**What the skill does:**
1. First: is `reasoning_effort` at `max`? Try `high` or `low` and re-measure. `max` is the default and it is expensive.
2. Second: are you re-encoding the same long context every turn? Turn on KV caching.
3. Third: is one expert overloaded? Watch expert-routing balance across the 896 experts.
4. Fourth: is your engine version current? Recipes update; check upstream.

Never claim a specific tuning will yield a specific speedup — measure.

---

## Recipe 6 — "Commercial deployment — what about the license?"

**Trigger:** "can we deploy K3 to customers?"

**What the skill does:**
1. Sends the user to the [Kimi K3 License](https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE).
2. Names the specific triggers for legal review: redistribution, fine-tune-and-release, hosted-API-for-third-parties, export-controlled jurisdictions.
3. Never claims a specific use is or is not allowed — the license text and legal counsel decide.
4. Points at `references/license-and-terms.md` for the summary.

---

## When to bypass this skill

- Model selection question (K3 vs Claude / GPT / GLM) → use `maximus-k3-model-selection`.
- Building against the hosted API only → use the standard AI Engineering skills; no self-hosting needed.
- Different model entirely → this is K3-specific.

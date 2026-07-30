# HOWTO — maximus-k3-model-selection

Six recipes for the most common model-selection questions when Kimi K3 is on the shortlist.

Each recipe assumes you already loaded the skill. Prompt the agent with the recipe's trigger phrase — the skill's workflow handles the rest.

---

## Recipe 1 — "K3 vs Claude Fable 5 for coding"

**Trigger:** any variant of "should I use K3 or Claude Fable 5 for my coding agent?"

**What the skill does:**
1. Asks: which coding benchmark best matches your workload (SWE-Marathon-shaped, DeepSWE-shaped, Terminal-Bench-shaped, or your own eval)?
2. Pulls the head-to-head numbers with harness notes.
3. Applies the ±1.5 point noise rule.
4. Returns a recommendation with the specific benchmark citation.

**Typical answer:** K3 or Claude Fable 5 both win specific coding benches. K3 tends to win SWE-Marathon (42.0 vs 35.0) and FrontierSWE (81.2 vs 86.6 — Claude Fable 5 actually wins here); Claude Fable 5 wins DeepSWE (70.0 vs 67.5) and Kimi Code Bench 2.0 (76.9 vs 72.9). The right pick depends on which bench looks most like your work — the skill will ask.

---

## Recipe 2 — "I need >500K token context"

**Trigger:** "I need a model that can hold [large corpus / whole repo / long doc]"

**What the skill does:**
1. Confirms actual token count (people usually overestimate).
2. If >200K, K3's 1M window becomes a real differentiator.
3. Flags the preserved-thinking cost multiplier for multi-turn.
4. Asks whether retrieval + 300K would work (it usually does, cheaper).

**Typical answer:** If it truly needs to be one prompt, K3. If chunking is acceptable, the recommendation flips to whichever model wins your primary task on shorter contexts.

---

## Recipe 3 — "Open-weight requirement, commercial deployment"

**Trigger:** "we need to self-host" / "our compliance team requires open weights" / "no vendor lock-in"

**What the skill does:**
1. Confirms open-weight is a hard requirement (not just preference).
2. Narrows to K3, GLM-5.2, and whatever else has open weights that quarter.
3. Flags the Kimi K3 License — it is source-available, not Apache/MIT. Legal review needed.
4. Recommends based on task fit within the open-weight subset.

**Typical answer:** K3 wins most benches inside the open-weight set today. GLM-5.2 is the fallback if the Kimi K3 License terms do not fit.

---

## Recipe 4 — "K3 vs GPT-5.6 Sol for agentic tool use"

**Trigger:** "which is best for tool-calling / MCP / browser agents?"

**What the skill does:**
1. Pulls the agentic bench cluster (BrowseComp, MCPMark-Verified, MCP-Atlas, Toolathlon-Verified, OSWorld-Verified, τ³-Banking).
2. Notes where each model has a clear edge:
   - K3 wins MCPMark-Verified (94.5 vs 92.9), τ³-Banking (33.4 vs 33.0), BrowseComp (91.2 vs 90.4).
   - GPT-5.6 Sol wins OSWorld 2.0 (62.6 vs 58.3), CritPt (32.3 vs 23.4).
   - Within-noise on many others.
3. Recommends based on which subset dominates your workload.

---

## Recipe 5 — "Is K3 worth switching to?"

**Trigger:** "we're on [Claude / GPT / GLM] — should we switch?"

**What the skill does:**
1. Never recommends switching for its own sake.
2. Asks what is failing on the current model.
3. Only recommends K3 if there is a specific benchmark or constraint (open weights, 1M context, specific bench win) that materially improves on the incumbent.
4. If not, says "stay put."

**Typical answer:** "Stay on your current model unless [specific unmet need]. Switching costs are real; migration re-work eats the benchmark delta most of the time."

---

## Recipe 6 — "I'm cost-sensitive"

**Trigger:** "cheap tokens" / "high volume" / "cost-dominated"

**What the skill does:**
1. Immediately deprioritizes K3, Claude Fable 5, and GPT-5.6 Sol — they are all frontier-priced.
2. Recommends GLM-5.2 or a smaller model.
3. Sends the user to the vendor pricing pages for current numbers.
4. Does not quote per-token prices from memory.

**Typical answer:** "K3 is not your model here. GLM-5.2 or a smaller open-weight fits cost-dominated production. Check pricing at [z.ai](https://z.ai) and compare against your target cost per completion."

---

## When to bypass this skill

- If the user has already picked K3 and is asking how to build with it → use the standard AI Engineering skills.
- If the user is asking about deployment or self-hosting → use `maximus-k3-self-hosting`.
- If K3 is not on the shortlist at all → use the general model-selection heuristics; do not force K3 into the conversation.

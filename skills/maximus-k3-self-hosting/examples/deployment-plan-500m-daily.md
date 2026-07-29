# Example — deployment plan for 500M tokens/day

**User prompt (verbatim):**
> "We're seeing ~500M tokens/day of K3 traffic on platform.kimi.ai and expect it to grow. Cost is starting to bite. Should we self-host? What would that look like?"

## Step 1 — Should you self-host?

- **Volume:** 500M/day sustained — above the ~100M rule-of-thumb gate.
- **Latency budget:** assumed p99 < 3s per turn (asked in follow-up).
- **Hardware access:** cloud GPU rental available; no owned GPUs today.
- **Ops maturity:** team has run vLLM in production before for smaller models.

**Gate result:** self-hosting is worth serious evaluation. Do not skip the pilot.

## Step 2 — Engine choice

**Recommendation:** start with **vLLM**.

Reasons:
- Team already has vLLM operational experience → engine familiarity outweighs raw throughput deltas
- Official K3 recipe at [recipes.vllm.ai/moonshotai/Kimi-K3](https://recipes.vllm.ai/moonshotai/Kimi-K3)
- Widest OpenAI-compatible client ecosystem for a low-friction cutover from the hosted API

Reconsider SGLang if a subsequent workload analysis shows structured decoding or tool-heavy sequences dominate.

## Step 3 — Hardware

**Do not fix a GPU count here.** Point the pilot team at:
- The vLLM K3 recipe's stated minimum hardware
- Their cloud provider's H20 / H200 / B200 pricing
- The sizing worksheet in `references/hardware-sizing.md`

The pilot picks a config that fits the recipe minimum, load-tests, and iterates. Do not architect for peak day 1.

## Step 4 — Deployment steps

1. **License:** get counsel to review the [Kimi K3 License](https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE) against your intended use — internal only vs. wrapping in a customer-facing product changes the answer.
2. **Weights:** pull from `moonshotai/Kimi-K3` on Hugging Face into your VPC. Do not host on public-readable buckets.
3. **Recipe:** follow the vLLM K3 recipe end to end without modification. If it does not run, fix the environment, not the recipe.
4. **Smoke test:** run `scripts/smoke_test.py` (the preserved-thinking check). If it fails, do not proceed.
5. **Endpoint:** expose the OpenAI-compatible endpoint behind your internal API gateway. Match the hosted API's request shape so client-side cutover is a URL change.
6. **Shadow traffic:** mirror 5–10% of production traffic to the self-hosted stack. Compare responses on a diff sample.
7. **Cut over gradually:** 10% → 50% → 100% over 1–2 weeks with the hosted API as fallback.

## Step 5 — Preserved-thinking config

- Start at `reasoning_effort=high` — matches most published K3 benchmark behavior at reasonable cost.
- Keep the preserved-thinking round-trip in your client wrapper (see `examples/smoke-test-preserved-thinking.md`).
- Measure token cost per turn against the hosted API baseline. If per-turn overhead is higher than expected, check for double-counting the `reasoning_content` payload.

## Step 6 — Operational watch-outs

- **KV cache:** turn on paged attention (default in vLLM); at 1M context this is not optional.
- **Expert routing:** monitor per-expert utilization across the 896 experts. Skew indicates a workload mismatch and hurts throughput.
- **Weights version pinning:** record the Hugging Face commit hash in your deployment manifest.
- **Fallback path:** keep the hosted API as a live fallback for at least 30 days post-cutover.

## Ask-back

What is your target p99 latency and your budgeted GPU spend per month? Those two numbers refine the engine and hardware picks materially.

---

## Notes on how this trace was built

- The gate was applied honestly at Step 1. At 500M/day with a capable ops team, self-hosting deserves a pilot. At 50M/day it would not.
- No GPU count was quoted. The recipe is the source of truth.
- The rollout plan is boring on purpose — shadow traffic, gradual cutover, hosted fallback. Frontier-model self-hosting is not the time for bold rollouts.
- The ask-back is specific and actionable. Vague ask-backs do not help the user come back with useful information.

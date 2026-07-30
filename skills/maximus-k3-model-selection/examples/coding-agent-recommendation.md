# Example — coding-agent recommendation

**User prompt (verbatim):**
> "We're building an agentic coding assistant that will operate on a 40-file TypeScript repo. Long sessions — 20 to 60 turns typical. Tool use is heavy (fs, grep, git, npm test). Budget matters but we can pay for quality. Should we use K3 or Claude Fable 5?"

## Step 1 — Decision inputs

- **Task shape:** long-horizon coding agent, multi-turn, heavy tool use
- **Context length:** ~150K token repo worst case; per-turn <30K
- **Deployment:** hosted API OK
- **License:** no constraint
- **Cost sensitivity:** balanced

## Step 2 — Benchmark fit

Long-horizon coding agents map most closely to **SWE-Marathon** and **Terminal-Bench 2.1**. From `references/k3-benchmarks.md`:

| Benchmark | K3 | CF5 | Delta |
|---|---|---|---|
| SWE-Marathon | 42.0 | 35.0 | **K3 +7.0** (real) |
| Terminal-Bench 2.1 | 88.3 | 88.0 | within noise |
| FrontierSWE | 81.2 | 86.6 | CF5 +5.4 (real) |
| DeepSWE | 67.5 | 70.0 | CF5 +2.5 (real) |
| Kimi Code Bench 2.0 | 72.9 | 76.9 | CF5 +4.0 (real) |

Mixed picture. SWE-Marathon (the most session-shaped bench) favors K3. FrontierSWE and DeepSWE favor CF5.

## Step 3 — Constraints

- **Preserved-thinking cost:** at 20–60 turns per session, K3's preserved-thinking overhead is meaningful. Budget +15–40% input tokens vs. a non-preserved-thinking baseline (see `references/preserved-thinking-cost.md`).
- **Harness:** K3's SWE-Marathon and Terminal-Bench numbers were measured with the Kimi Code harness. CF5 with Claude Code. If the user's harness is closer to Claude Code, CF5's benches transfer more directly.

## Step 4 — Recommendation

## Recommendation
Start with Kimi K3, with a 2-week A/B against Claude Fable 5 on your actual eval.

## Why this one
- SWE-Marathon is the closest benchmark match for 20–60-turn session-heavy work, and K3 wins it by 7 points (42.0 vs 35.0, [Kimi K3 report](https://github.com/MoonshotAI/Kimi-K3)).
- Terminal-Bench 2.1 is within noise, so heavy shell tool use should transfer.
- Open-weight fallback available (self-host if API pricing changes).

## Why not the runner-up
- Claude Fable 5 wins FrontierSWE (86.6 vs 81.2) and DeepSWE (70.0 vs 67.5). If your repo profile looks more like those benches (larger codebases, longer file edits, less shell), CF5 flips the answer.

## Watch-outs
- Preserved-thinking overhead adds 15–40% input tokens across long sessions — factor into TCO before locking in.
- K3 SWE-Marathon numbers used the Kimi Code harness; if you ship on a different harness, the transfer is not guaranteed.
- License: K3 is source-available under the Kimi K3 License, not Apache/MIT. Legal review before commercial deployment.

## Ask-back
What eval will you use for the 2-week A/B — one of the published benches, or something proprietary to your repo?

---

## Notes on how this trace was built

- Every score came from `references/k3-benchmarks.md`. Nothing was interpolated.
- The recommendation named a specific bench (SWE-Marathon) rather than "K3 is better at coding." Vague wins hide their evidence.
- The runner-up section is honest — it says exactly what would flip the answer. That is the workhorse voice.
- The ask-back gives the user a specific next question so the recommendation is testable.

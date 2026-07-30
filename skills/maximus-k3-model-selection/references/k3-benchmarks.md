# Kimi K3 benchmark reference

**Source:** [Kimi-K3 tech report README](https://github.com/MoonshotAI/Kimi-K3), Moonshot AI. All numbers below are transcribed from Section 3 (Evaluation Results) of the README as of **2026-07-28**.

**Read this first:** The K3 report is explicit that harness varies across models. Do not compare a Kimi Code harness number to a Codex harness number without noting it. Do not treat within-noise differences (±1.5) as wins.

## Columns
- **K3 (max)** — Kimi K3 with `reasoning_effort=max`, temperature 1.0, top-p 0.95 for single-step, 1.0 for agentic
- **CF5 (max)** — Claude Fable 5 with fallback where noted
- **GPT-5.6 Sol (max)**
- **Opus 4.8 (max)** — Claude Opus 4.8
- **GPT-5.5 (xhigh)**
- **GLM-5.2 (max)**

## Reasoning & knowledge

| Benchmark | K3 | CF5 | GPT-5.6 Sol | Opus 4.8 | GPT-5.5 | GLM-5.2 |
|---|---|---|---|---|---|---|
| GPQA Diamond | 93.5 | 92.6 | 94.1 | 91.0 | 93.5 | 91.2 |
| CritPt | 23.4 | 28.6 | 32.3 | 20.9 | 27.1 | 20.9 |
| AA-LCR | 74.7 | 70.0 | 73.7 | 67.7 | 74.3 | 71.3 |
| HLE-Full (no-tool / w-tool) | 43.5 / 56.0 | 53.3 / 63.0 | 44.5 / 58.0 | 49.8 / 57.9 | 41.4 / 52.2 | — |

**K3 lanes:** AA-LCR is a small edge. K3 is behind or within noise elsewhere in this cluster.

## Coding

| Benchmark | K3 | CF5 | GPT-5.6 Sol | Opus 4.8 | GPT-5.5 | GLM-5.2 |
|---|---|---|---|---|---|---|
| DeepSWE | 67.5 | 70.0 | 73.0 | 59.0 | 67.0 | 46.2 |
| ProgramBench | 77.8 | 76.8 | 77.6 | 71.9 | 70.8 | 63.7 |
| Terminal-Bench 2.1 | 88.3 | 88.0 | 88.8 | 84.6 | 83.4 | 82.7 |
| FrontierSWE | 81.2 | 86.6 | 71.3 | 66.7 | 64.9 | 67.3 |
| SWE-Marathon | 42.0 | 35.0 | 39.0 | 40.0 | 14.0 | 13.0 |
| PostTrainBench | 36.6 | 41.4 | 34.6 | 34.1 | 28.4 | 34.3 |
| MLS-Bench-Lite | 48.3 | 49.9 | 46.2 | 42.8 | 35.5 | 40.4 |
| SciCode | 58.7 | 60.2 | 56.1 | 53.5 | 56.1 | 50.5 |
| Kimi Code Bench 2.0 | 72.9 | 76.9 | 64.8 | 71.7 | 69.0 | 64.2 |

**K3 lanes:** SWE-Marathon (clear win, 42.0 vs 39.0 next-best), ProgramBench (within noise but top), Terminal-Bench 2.1 (within noise).
**Not K3 lanes:** DeepSWE (behind CF5 and GPT-5.6 Sol), FrontierSWE (CF5 wins), Kimi Code Bench 2.0 (CF5 wins despite the name).
**Harness caveat:** K3 numbers use the Kimi Code harness. CF5 and Opus 4.8 use Claude Code. GPT-5.6 Sol uses Codex. See tech report footnotes for the exact pairing per benchmark.

## Agentic

| Benchmark | K3 | CF5 | GPT-5.6 Sol | Opus 4.8 | GPT-5.5 | GLM-5.2 |
|---|---|---|---|---|---|---|
| BrowseComp | 91.2 | 88.0 | 90.4 | 84.3 | 84.4 | — |
| DeepSearchQA (F1) | 95.0 | 94.2 | — | 93.1 | — | — |
| ResearchRubrics | 76.2 | — | 73.8 | 73.5 | 64.0 | 71.1 |
| GDPval-AA v2 (Elo) | 1686 | 1747 | 1736 | 1593 | 1491 | 1510 |
| Toolathlon-Verified | 76.5 | 77.9 | 74.9 | 76.2 | 73.5 | 59.9 |
| MCPMark-Verified | 94.5 | 87.4 | 92.9 | 76.4 | 92.9 | — |
| MCP-Atlas | 84.2 | 84.7 | 83.6 | 83.6 | 82.8 | 82.6 |
| AutomationBench | 30.8 | 29.1 | 29.7 | 27.2 | 22.7 | 12.9 |
| JobBench | 54.3 | 57.4 | 45.4 | 48.4 | 38.3 | 43.4 |
| AA-Briefcase (Elo) | 1548 | 1583 | 1495 | 1354 | 1158 | 1260 |
| Agents' Last Exam | 28.3 | 25.7† | 29.6 | 27.0 | 26.6 | 20.4 |
| APEX-Agents | 41.0 | 43.3 | 39.9 | 39.4 | 38.5 | 35.6 |
| OfficeQA Pro | 63.3 | 69.9 | 63.2 | 63.9 | 60.9 | 41.4 |
| SpreadsheetBench 2 | 34.8 | 34.7 | 32.4 | 31.6 | 29.1 | 28.1 |
| OSWorld-Verified | 84.8 | 85.0 | 83.0 | 83.4 | 79.0 | — |
| OSWorld 2.0 | 58.3 | 66.1 | 62.6 | 55.7 | 49.5 | — |
| SaaS-Bench | 60.1 | — | 61.4 | 56.1 | 43.8 | — |
| τ³-Banking | 33.4 | 26.8 | 33.0 | 27.6 | 31.3 | 26.8 |
| Harvey Lab-AA | 94.6 | 93.6 | 87.2 | 91.1 | 86.3 | 91.0 |
| CorpFin v2 | 71.6 | 71.8 | 64.4 | 66.7 | 68.4 | 66.1 |
| Finance Agent v2 | 54.4 | 56.3 | 53.8 | 53.9 | 51.8 | 49.7 |
| Legal Research Bench | 44.2 | 49.5 | 48.1 | 43.8 | 40.4 | 31.3 |

**K3 lanes:** BrowseComp (clear win), DeepSearchQA, ResearchRubrics, MCPMark-Verified, AutomationBench, τ³-Banking, Harvey Lab-AA, SpreadsheetBench 2 (all wins or within-noise-leader).
**Not K3 lanes:** GDPval-AA v2 Elo (CF5 leads), AA-Briefcase Elo (CF5), OSWorld 2.0 (CF5), OfficeQA Pro (CF5), APEX-Agents (CF5), Legal Research Bench (CF5).
**Pattern:** K3 is stronger on search/browse/MCP/data workloads; Claude Fable 5 is stronger on office/GUI-heavy and Elo-judged briefcase-style work.

## Vision

| Benchmark | K3 | CF5 | GPT-5.6 Sol | Opus 4.8 | GPT-5.5 | GLM-5.2 |
|---|---|---|---|---|---|---|
| WorldVQA ForceAnswer | 51.0 | 56.7 | 41.8 | 39.1 | 38.5 | — |
| OmniDocBench | 91.1 | 89.8 | 85.8 | 87.9 | 89.4 | — |
| PerceptionBench | 58.5 | 57.2 | 59.7 | 47.2 | 55.8 | — |
| Video-MME (w. sub) | 90.0 | — | 89.5 | 86.0 | 89.3 | — |
| MMVU | 82.1 | — | 81.2 | 79.2 | 81.7 | — |
| BabyVision w/ python | 85.7 | 90.5 | 88.9 | 81.2 | 83.6 | — |
| MMMU-Pro (no-tool / w-tool) | 81.6 / 83.4 | 81.2 / 86.5 | 83.0 / 84.6 | 78.9 / 82.7 | 81.2 / 83.2 | — |
| CharXiv (RQ) | 84.8 / 91.3 | 88.9 / 93.5 | 84.6 / 89.1 | 80.5 / 89.9 | 84.1 / 89.0 | — |
| MathVision | 94.3 / 97.8 | 94.8 / 98.6 | 95.8 / 97.8 | 86.7 / 97.1 | 92.2 / 96.8 | — |
| ZeroBench (pass@5) | 23.0 / 41.0 | 23.0 / 46.0 | 17.0 / 35.0 | 17.0 / 34.0 | 22.0 / 41.0 | — |

**K3 lanes:** OmniDocBench (best), Video-MME (best), MMVU (best).
**Not K3 lanes:** WorldVQA (CF5 leads by a lot), BabyVision (CF5), CharXiv (CF5), MathVision (GPT-5.6 Sol single-step, CF5 w/ tools).

## Third-party citations noted in the K3 report

- **CritPt, AA-LCR, SciCode** — [Artificial Analysis](https://artificialanalysis.ai/) as of 2026-07-23
- **DeepSWE** — [DeepSWE leaderboard](https://deepswe.datacurve.ai/) + GLM-5.2 from [z.ai blog](https://z.ai/blog/glm-5.2)
- **Terminal-Bench 2.1** — [Artificial Analysis](https://artificialanalysis.ai/evaluations/terminalbench-v2-1) + OpenAI + z.ai
- **ProgramBench** — [Vals AI](https://www.vals.ai/benchmarks/programbench)
- **SWE-Marathon** — [official tasks](https://www.swe-marathon.org/), H20-calibrated branch as of 2026-07-09
- **FrontierSWE** — [FrontierSWE](https://www.frontierswe.com/) as of 2026-07-16
- **BrowseComp** — [Anthropic](https://www.anthropic.com/news/claude-fable-5-mythos-5) and [OpenAI](https://openai.com/index/gpt-5-6/)
- **GDPval-AA v2, AA-Briefcase, τ³-Banking, Harvey Lab-AA, APEX-Agents** — [Artificial Analysis](https://artificialanalysis.ai/) + [APEX-Agents leaderboard](https://www.mercor.com/apex/apex-agents-leaderboard/) as of 2026-07-23
- **CorpFin v2, Finance Agent v2, Legal Research Bench** — [Vals AI](https://www.vals.ai/)
- **Agents' Last Exam** — [official leaderboard](https://agents-last-exam.org/leaderboard) as of 2026-07-23

## Freshness

Last refreshed: **2026-07-28**. Refresh from https://github.com/MoonshotAI/Kimi-K3 if more than 30 days old before relying on these numbers for a recommendation.

"""
ab-harness.py
-------------
A/B model comparison harness for evaluating two LLM models on the same task.

Measures:
  - Quality score (via LLM judge using gpt-4o-mini)
  - Latency p50 and p95
  - Cost per 1,000 requests
  - Statistical significance (paired t-test)

Requirements: openai>=1.30.0, scipy
Environment: OPENAI_API_KEY

Usage:
    python ab-harness.py

Adapt by:
1. Replace MODEL_A and MODEL_B with the models you're comparing
2. Replace EVAL_CASES with your actual test cases
3. Adjust QUALITY_RUBRIC to match your task
"""

import json
import time
import statistics
import logging
from dataclasses import dataclass, field
from typing import Callable
from openai import OpenAI

log = logging.getLogger("ab_harness")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

client = OpenAI()

# ---------------------------------------------------------------------------
# Models under test
# ---------------------------------------------------------------------------
MODEL_A = "gpt-4o-mini"           # control (baseline, cheaper)
MODEL_B = "gpt-4.1-2025-04-14"    # treatment (mid-tier)

# Pricing per 1M tokens (mid-2026)
PRICING = {
    "gpt-4o-mini":      {"input": 0.15,  "output": 0.60},
    "gpt-4.1-2025-04-14": {"input": 2.00, "output": 8.00},
    # Add more models as needed
}

# ---------------------------------------------------------------------------
# Shared system prompt (identical for both models — isolate the variable)
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are a customer support assistant for Acme SaaS.
Answer the user's question based on your knowledge of our product.
Be concise and accurate. If you don't know the answer, say so."""

# ---------------------------------------------------------------------------
# Eval cases (same for both models)
# ---------------------------------------------------------------------------
@dataclass
class EvalCase:
    id: str
    user_message: str
    golden_answer: str
    quality_rubric: list[str]   # criteria to score 0/1
    tags: list = field(default_factory=list)

EVAL_CASES = [
    EvalCase(
        id="001",
        user_message="What are your pricing plans?",
        golden_answer="We offer Basic ($29/mo), Pro ($99/mo), and Enterprise (starting $499/mo) plans.",
        quality_rubric=[
            "Mentions at least two pricing plans",
            "Does not invent prices not mentioned in the context",
        ],
        tags=["pricing"],
    ),
    EvalCase(
        id="002",
        user_message="How do I reset my password?",
        golden_answer="Go to the login page, click 'Forgot password', and follow the email instructions.",
        quality_rubric=[
            "Mentions the password reset process",
            "Does not provide incorrect or made-up steps",
        ],
        tags=["account"],
    ),
    EvalCase(
        id="003",
        user_message="What is the capital of Mars?",
        golden_answer="I don't know the answer to that question.",
        quality_rubric=[
            "Does not invent an answer",
            "Acknowledges it cannot answer",
        ],
        tags=["unanswerable"],
    ),
    EvalCase(
        id="004",
        user_message="Can I export my data?",
        golden_answer="Yes, data export is available on all plans in CSV and JSON format.",
        quality_rubric=[
            "States that export is available",
            "Does not invent unsupported export formats",
        ],
        tags=["features"],
    ),
    EvalCase(
        id="005",
        user_message="Do you offer a free trial?",
        golden_answer="Yes, we offer a 14-day free trial with no credit card required.",
        quality_rubric=[
            "Mentions the free trial",
            "Does not invent a different trial length",
        ],
        tags=["pricing"],
    ),
]


# ---------------------------------------------------------------------------
# LLM judge for quality scoring
# ---------------------------------------------------------------------------
JUDGE_PROMPT = """Evaluate the assistant's response against the golden answer and quality rubric.

User question: {question}
Assistant response: {response}
Golden answer: {golden}

Quality rubric (score each 0 or 1):
{rubric_list}

Respond with JSON:
{{
  "scores": {{"<criterion>": 0_or_1}},
  "overall": <average of scores, 0.0-1.0>
}}"""

def judge_quality(case: EvalCase, response: str) -> float:
    """Score a response using gpt-4o-mini as judge. Returns 0.0-1.0."""
    rubric_list = "\n".join(f"- {r}" for r in case.quality_rubric)
    prompt = JUDGE_PROMPT.format(
        question=case.user_message,
        response=response,
        golden=case.golden_answer,
        rubric_list=rubric_list
    )
    result = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    data = json.loads(result.choices[0].message.content)
    return float(data.get("overall", 0.0))


# ---------------------------------------------------------------------------
# Single model runner
# ---------------------------------------------------------------------------
@dataclass
class RunResult:
    case_id: str
    model: str
    response: str
    quality_score: float
    latency_ms: float
    input_tokens: int
    output_tokens: int
    cost_usd: float

def run_case(case: EvalCase, model: str) -> RunResult:
    """Run a single eval case on a given model."""
    t0 = time.time()
    response = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": case.user_message}
        ]
    )
    latency_ms = (time.time() - t0) * 1000
    content = response.choices[0].message.content
    usage = response.usage

    pricing = PRICING.get(model, {"input": 0, "output": 0})
    cost = (usage.prompt_tokens * pricing["input"] + usage.completion_tokens * pricing["output"]) / 1_000_000

    quality = judge_quality(case, content)

    return RunResult(
        case_id=case.id,
        model=model,
        response=content,
        quality_score=quality,
        latency_ms=latency_ms,
        input_tokens=usage.prompt_tokens,
        output_tokens=usage.completion_tokens,
        cost_usd=cost,
    )


# ---------------------------------------------------------------------------
# A/B comparison runner
# ---------------------------------------------------------------------------
@dataclass
class ABSummary:
    model: str
    quality_mean: float
    quality_std: float
    latency_p50_ms: float
    latency_p95_ms: float
    cost_per_1k_usd: float
    results: list[RunResult]

def run_ab(cases: list[EvalCase], model_a: str, model_b: str) -> tuple[ABSummary, ABSummary]:
    """Run both models on all eval cases and return summaries."""
    a_results, b_results = [], []

    for i, case in enumerate(cases):
        log.info(f"Case {i+1}/{len(cases)}: {case.user_message[:60]}...")
        a_results.append(run_case(case, model_a))
        b_results.append(run_case(case, model_b))

    def summarise(model: str, results: list[RunResult]) -> ABSummary:
        qualities = [r.quality_score for r in results]
        latencies = sorted(r.latency_ms for r in results)
        total_cost = sum(r.cost_usd for r in results)
        n = len(results)
        return ABSummary(
            model=model,
            quality_mean=statistics.mean(qualities),
            quality_std=statistics.stdev(qualities) if n > 1 else 0.0,
            latency_p50_ms=latencies[n // 2],
            latency_p95_ms=latencies[int(n * 0.95)],
            cost_per_1k_usd=total_cost / n * 1000,
            results=results,
        )

    return summarise(model_a, a_results), summarise(model_b, b_results)


def statistical_test(a_results: list[RunResult], b_results: list[RunResult]) -> dict:
    """Paired t-test on quality scores."""
    try:
        from scipy import stats
        a_scores = [r.quality_score for r in a_results]
        b_scores = [r.quality_score for r in b_results]
        t_stat, p_value = stats.ttest_rel(a_scores, b_scores)
        return {"t_statistic": t_stat, "p_value": p_value, "significant": p_value < 0.05}
    except ImportError:
        # Manual mean difference without scipy
        a_mean = statistics.mean([r.quality_score for r in a_results])
        b_mean = statistics.mean([r.quality_score for r in b_results])
        return {"t_statistic": None, "p_value": None, "delta": b_mean - a_mean,
                "note": "scipy not installed; no statistical test. Install with pip install scipy"}


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def print_report(summary_a: ABSummary, summary_b: ABSummary, stat_test: dict):
    print("\n" + "=" * 70)
    print("A/B MODEL COMPARISON REPORT")
    print("=" * 70)
    print(f"{'Metric':<30} {'Model A':>18} {'Model B':>18}")
    print(f"{'':.<30} {summary_a.model[:18]:>18} {summary_b.model[:18]:>18}")
    print("-" * 70)
    print(f"{'Quality score (mean)':<30} {summary_a.quality_mean:>17.3f} {summary_b.quality_mean:>17.3f}")
    print(f"{'Quality score (std)':<30} {summary_a.quality_std:>17.3f} {summary_b.quality_std:>17.3f}")
    print(f"{'Latency p50 (ms)':<30} {summary_a.latency_p50_ms:>17.0f} {summary_b.latency_p50_ms:>17.0f}")
    print(f"{'Latency p95 (ms)':<30} {summary_a.latency_p95_ms:>17.0f} {summary_b.latency_p95_ms:>17.0f}")
    print(f"{'Cost per 1K requests ($)':<30} {summary_a.cost_per_1k_usd:>17.4f} {summary_b.cost_per_1k_usd:>17.4f}")
    print("-" * 70)

    delta_quality = summary_b.quality_mean - summary_a.quality_mean
    delta_cost = summary_b.cost_per_1k_usd - summary_a.cost_per_1k_usd
    p_value = stat_test.get("p_value")

    print(f"\nQuality delta (B - A):  {delta_quality:+.3f}")
    print(f"Cost delta (B - A):     ${delta_cost:+.4f} per 1K requests")
    if p_value is not None:
        print(f"p-value:               {p_value:.4f} ({'significant' if p_value < 0.05 else 'not significant'})")

    print("\n--- DECISION GUIDANCE ---")
    QUALITY_THRESHOLD = 0.05  # tolerate up to 5% quality drop for cost savings
    if abs(delta_quality) <= QUALITY_THRESHOLD:
        if delta_cost < 0:
            print(f"RECOMMEND: Model B ({summary_b.model}) — same quality, {abs(delta_cost/summary_a.cost_per_1k_usd)*100:.0f}% cost reduction.")
        else:
            print(f"NEUTRAL: Model B costs more (+${delta_cost:.4f}/1K) with no quality improvement.")
    elif delta_quality > QUALITY_THRESHOLD:
        print(f"CONSIDER B: Model B has meaningfully better quality (+{delta_quality:.3f}). Worth the cost if task quality is critical.")
    else:
        print(f"STAY ON A: Model B quality is {abs(delta_quality):.3f} below threshold ({QUALITY_THRESHOLD}). Cost savings do not justify quality drop.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"A/B Test: {MODEL_A} vs {MODEL_B}")
    print(f"Eval cases: {len(EVAL_CASES)}\n")

    summary_a, summary_b = run_ab(EVAL_CASES, MODEL_A, MODEL_B)
    stat_test = statistical_test(summary_a.results, summary_b.results)
    print_report(summary_a, summary_b, stat_test)

    # Save raw results
    output = {
        "model_a": MODEL_A,
        "model_b": MODEL_B,
        "summary_a": {
            "quality_mean": summary_a.quality_mean,
            "latency_p50": summary_a.latency_p50_ms,
            "cost_per_1k": summary_a.cost_per_1k_usd
        },
        "summary_b": {
            "quality_mean": summary_b.quality_mean,
            "latency_p50": summary_b.latency_p50_ms,
            "cost_per_1k": summary_b.cost_per_1k_usd
        },
        "statistical_test": stat_test,
    }
    with open("ab_results.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nFull results saved to ab_results.json")

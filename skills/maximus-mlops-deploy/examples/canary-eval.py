"""
canary-eval.py — Compare a canary model version against the production baseline
using logged traffic from the canary window.

Prerequisites:
    pip install anthropic mlflow pandas numpy scipy

Usage:
    python canary-eval.py --canary-run-id <run_id> --prod-run-id <run_id> --window-hours 24
"""

import argparse
import json
import time
from dataclasses import dataclass, field
from typing import Any

import mlflow
import numpy as np
import pandas as pd
from scipy import stats


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


@dataclass
class EvalRecord:
    """A single request/response pair from the canary window."""
    request_id: str
    input_text: str
    output_text: str
    model_version: str          # "production" or "canary"
    latency_ms: float
    input_tokens: int
    output_tokens: int
    quality_score: float | None = None   # filled by scorer
    cost_usd: float | None = None


@dataclass
class EvalReport:
    """Aggregated comparison between canary and production."""
    canary_version: str
    production_version: str
    window_hours: float
    n_requests: int

    # Quality
    canary_quality_mean: float = 0.0
    production_quality_mean: float = 0.0
    quality_p_value: float = 1.0
    quality_delta_pct: float = 0.0

    # Latency
    canary_latency_p50_ms: float = 0.0
    canary_latency_p95_ms: float = 0.0
    production_latency_p50_ms: float = 0.0
    production_latency_p95_ms: float = 0.0

    # Cost
    canary_cost_per_call: float = 0.0
    production_cost_per_call: float = 0.0

    # Decision
    promotion_recommended: bool = False
    promotion_blockers: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Quality scorer (using LLM-as-judge)
# ---------------------------------------------------------------------------


def score_output_quality(
    input_text: str,
    output_text: str,
    rubric: str,
    judge_model: str = "claude-haiku-3-5",
) -> float:
    """
    Score output quality 0.0–1.0 using an LLM judge.
    Use a cheap model for the judge — this runs at scale.
    """
    import anthropic

    client = anthropic.Anthropic()
    prompt = f"""You are a quality evaluator. Score the following output on a scale of 0 to 10.

Rubric: {rubric}

Input: {input_text}

Output: {output_text}

Return only a JSON object: {{"score": <number 0-10>, "reason": "<one sentence>"}}"""

    response = client.messages.create(
        model=judge_model,
        max_tokens=128,
        messages=[{"role": "user", "content": prompt}],
    )

    result = json.loads(response.content[0].text)
    return result["score"] / 10.0  # normalize to 0–1


# ---------------------------------------------------------------------------
# Evaluation runner
# ---------------------------------------------------------------------------


class CanaryEvaluator:
    def __init__(
        self,
        canary_version: str,
        production_version: str,
        quality_threshold: float = 0.82,
        latency_regression_threshold_pct: float = 20.0,
        cost_regression_threshold_pct: float = 10.0,
    ):
        self.canary_version = canary_version
        self.production_version = production_version
        self.quality_threshold = quality_threshold
        self.latency_regression_threshold_pct = latency_regression_threshold_pct
        self.cost_regression_threshold_pct = cost_regression_threshold_pct

    def load_records_from_mlflow(
        self, run_id: str, version: str
    ) -> list[EvalRecord]:
        """Load logged request/response pairs from an MLflow run."""
        client = mlflow.tracking.MlflowClient()
        artifacts = client.list_artifacts(run_id, "canary_traffic")

        records = []
        for artifact in artifacts:
            path = client.download_artifacts(run_id, artifact.path)
            with open(path) as f:
                for line in f:
                    data = json.loads(line)
                    records.append(
                        EvalRecord(
                            request_id=data["request_id"],
                            input_text=data["input"],
                            output_text=data["output"],
                            model_version=version,
                            latency_ms=data["latency_ms"],
                            input_tokens=data["input_tokens"],
                            output_tokens=data["output_tokens"],
                            cost_usd=data.get("cost_usd"),
                        )
                    )
        return records

    def score_records(
        self, records: list[EvalRecord], rubric: str, sample_size: int = 200
    ) -> list[EvalRecord]:
        """Score a sample of records. Full scoring is expensive — sample."""
        sample = records[:sample_size] if len(records) > sample_size else records
        for record in sample:
            record.quality_score = score_output_quality(
                record.input_text, record.output_text, rubric
            )
            time.sleep(0.1)  # rate limit
        return records

    def run_comparison(
        self,
        canary_records: list[EvalRecord],
        production_records: list[EvalRecord],
        rubric: str,
        window_hours: float,
    ) -> EvalReport:
        """Compare canary and production and produce an EvalReport."""
        # Score samples
        canary_scored = self.score_records(canary_records, rubric)
        prod_scored = self.score_records(production_records, rubric)

        canary_quality = [r.quality_score for r in canary_scored if r.quality_score is not None]
        prod_quality = [r.quality_score for r in prod_scored if r.quality_score is not None]

        # Statistical test (Mann-Whitney U, non-parametric)
        _, p_value = stats.mannwhitneyu(canary_quality, prod_quality, alternative="two-sided")

        report = EvalReport(
            canary_version=self.canary_version,
            production_version=self.production_version,
            window_hours=window_hours,
            n_requests=len(canary_records),
            canary_quality_mean=float(np.mean(canary_quality)),
            production_quality_mean=float(np.mean(prod_quality)),
            quality_p_value=float(p_value),
            quality_delta_pct=(
                (np.mean(canary_quality) - np.mean(prod_quality))
                / np.mean(prod_quality)
                * 100
            ),
            canary_latency_p50_ms=float(np.percentile([r.latency_ms for r in canary_records], 50)),
            canary_latency_p95_ms=float(np.percentile([r.latency_ms for r in canary_records], 95)),
            production_latency_p50_ms=float(np.percentile([r.latency_ms for r in production_records], 50)),
            production_latency_p95_ms=float(np.percentile([r.latency_ms for r in production_records], 95)),
            canary_cost_per_call=float(np.mean([r.cost_usd for r in canary_records if r.cost_usd])),
            production_cost_per_call=float(np.mean([r.cost_usd for r in production_records if r.cost_usd])),
        )

        # Determine promotion recommendation
        blockers = []

        if report.canary_quality_mean < self.quality_threshold:
            blockers.append(
                f"Canary quality {report.canary_quality_mean:.3f} below threshold {self.quality_threshold}"
            )

        latency_regression = (
            (report.canary_latency_p95_ms - report.production_latency_p95_ms)
            / report.production_latency_p95_ms
            * 100
        )
        if latency_regression > self.latency_regression_threshold_pct:
            blockers.append(
                f"Latency p95 regressed {latency_regression:.1f}% (threshold: {self.latency_regression_threshold_pct}%)"
            )

        if report.production_cost_per_call > 0:
            cost_regression = (
                (report.canary_cost_per_call - report.production_cost_per_call)
                / report.production_cost_per_call
                * 100
            )
            if cost_regression > self.cost_regression_threshold_pct:
                blockers.append(
                    f"Cost/call regressed {cost_regression:.1f}% (threshold: {self.cost_regression_threshold_pct}%)"
                )

        report.promotion_blockers = blockers
        report.promotion_recommended = len(blockers) == 0

        return report

    def log_report_to_mlflow(self, report: EvalReport, run_id: str) -> None:
        """Log the eval report back to MLflow for the record."""
        with mlflow.start_run(run_id=run_id):
            mlflow.log_metrics({
                "canary_quality_mean": report.canary_quality_mean,
                "production_quality_mean": report.production_quality_mean,
                "quality_delta_pct": report.quality_delta_pct,
                "quality_p_value": report.quality_p_value,
                "canary_latency_p95_ms": report.canary_latency_p95_ms,
                "canary_cost_per_call": report.canary_cost_per_call,
                "promotion_recommended": int(report.promotion_recommended),
            })
            mlflow.log_dict(
                {
                    "promotion_recommended": report.promotion_recommended,
                    "blockers": report.promotion_blockers,
                },
                "promotion_decision.json",
            )
        print(f"[canary-eval] Report logged to MLflow run {run_id}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Canary evaluation vs production baseline.")
    parser.add_argument("--canary-run-id", required=True)
    parser.add_argument("--prod-run-id", required=True)
    parser.add_argument("--canary-version", default="canary")
    parser.add_argument("--prod-version", default="production")
    parser.add_argument("--window-hours", type=float, default=24.0)
    parser.add_argument(
        "--rubric",
        default="The output is accurate, concise, and directly answers the user's question.",
    )
    parser.add_argument("--quality-threshold", type=float, default=0.82)
    args = parser.parse_args()

    evaluator = CanaryEvaluator(
        canary_version=args.canary_version,
        production_version=args.prod_version,
        quality_threshold=args.quality_threshold,
    )

    print("[canary-eval] Loading canary records...")
    canary_records = evaluator.load_records_from_mlflow(args.canary_run_id, "canary")
    print("[canary-eval] Loading production records...")
    prod_records = evaluator.load_records_from_mlflow(args.prod_run_id, "production")

    print(f"[canary-eval] Scoring {min(200, len(canary_records))} canary + {min(200, len(prod_records))} prod samples...")
    report = evaluator.run_comparison(canary_records, prod_records, args.rubric, args.window_hours)

    print("\n" + "=" * 60)
    print("CANARY EVAL REPORT")
    print("=" * 60)
    print(f"Canary version:          {report.canary_version}")
    print(f"Production version:      {report.production_version}")
    print(f"Window:                  {report.window_hours}h / {report.n_requests} requests")
    print(f"Quality (canary):        {report.canary_quality_mean:.3f}")
    print(f"Quality (production):    {report.production_quality_mean:.3f}")
    print(f"Quality delta:           {report.quality_delta_pct:+.1f}%  (p={report.quality_p_value:.3f})")
    print(f"Latency p95 (canary):    {report.canary_latency_p95_ms:.0f}ms")
    print(f"Latency p95 (prod):      {report.production_latency_p95_ms:.0f}ms")
    print(f"Cost/call (canary):      ${report.canary_cost_per_call:.5f}")
    print(f"Cost/call (prod):        ${report.production_cost_per_call:.5f}")
    print()
    if report.promotion_recommended:
        print("✓ PROMOTION RECOMMENDED")
    else:
        print("✗ PROMOTION BLOCKED")
        for blocker in report.promotion_blockers:
            print(f"  - {blocker}")
    print("=" * 60)

    evaluator.log_report_to_mlflow(report, args.canary_run_id)

    # Exit code for CI integration
    raise SystemExit(0 if report.promotion_recommended else 1)


if __name__ == "__main__":
    main()

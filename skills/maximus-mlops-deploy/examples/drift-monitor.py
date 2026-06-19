"""
drift-monitor.py — Online drift detection for ML/LLM systems in production.

Monitors:
  1. Input distribution drift via embedding cosine distance (data drift)
  2. Output distribution drift via token length and toxicity proxy (concept drift proxy)
  3. Prompt integrity via SHA-256 hash (prompt drift)

Prerequisites:
    pip install anthropic evidently sentence-transformers numpy redis schedule

Usage:
    # Run once to establish reference snapshot:
    python drift-monitor.py --mode snapshot --model-version summarization/2.1.0

    # Run continuously in production:
    python drift-monitor.py --mode monitor --model-version summarization/2.1.0 --interval-minutes 60
"""

import argparse
import hashlib
import json
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

import numpy as np
import redis
import schedule


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


@dataclass
class DriftAlert:
    alert_type: str              # "data_drift" | "output_drift" | "prompt_drift"
    model_version: str
    detected_at: str
    metric_name: str
    metric_value: float
    threshold: float
    severity: str                # "warning" | "critical"
    message: str
    sample_requests: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Embedding-based input drift detector
# ---------------------------------------------------------------------------


class InputDriftDetector:
    """
    Detects input distribution drift by comparing embedding centroids.
    Uses a sliding window of recent requests vs the reference snapshot.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        window_size: int = 500,
        drift_threshold: float = 0.15,  # cosine distance; 1.5σ ≈ 0.15 for typical text
        critical_threshold: float = 0.25,
    ):
        from sentence_transformers import SentenceTransformer
        self.encoder = SentenceTransformer(model_name)
        self.window_size = window_size
        self.drift_threshold = drift_threshold
        self.critical_threshold = critical_threshold
        self.reference_centroid: np.ndarray | None = None

    def build_reference(self, texts: list[str]) -> np.ndarray:
        """Encode reference texts and store the centroid."""
        embeddings = self.encoder.encode(texts, batch_size=32, show_progress_bar=False)
        self.reference_centroid = np.mean(embeddings, axis=0)
        return self.reference_centroid

    def compute_drift(self, recent_texts: list[str]) -> float:
        """
        Return cosine distance between recent centroid and reference centroid.
        0.0 = identical distribution; higher = more drift.
        """
        if self.reference_centroid is None:
            raise RuntimeError("Call build_reference() first.")

        recent_embeddings = self.encoder.encode(recent_texts, batch_size=32, show_progress_bar=False)
        recent_centroid = np.mean(recent_embeddings, axis=0)

        # Cosine distance = 1 - cosine similarity
        dot = np.dot(self.reference_centroid, recent_centroid)
        norm = np.linalg.norm(self.reference_centroid) * np.linalg.norm(recent_centroid)
        return float(1 - (dot / norm))

    def check(self, recent_texts: list[str], model_version: str) -> DriftAlert | None:
        drift_score = self.compute_drift(recent_texts)
        if drift_score >= self.critical_threshold:
            return DriftAlert(
                alert_type="data_drift",
                model_version=model_version,
                detected_at=datetime.utcnow().isoformat(),
                metric_name="input_embedding_cosine_distance",
                metric_value=drift_score,
                threshold=self.critical_threshold,
                severity="critical",
                message=(
                    f"Input distribution has drifted critically from the reference "
                    f"(distance={drift_score:.3f}, threshold={self.critical_threshold}). "
                    f"Investigate data pipeline and model inputs."
                ),
            )
        elif drift_score >= self.drift_threshold:
            return DriftAlert(
                alert_type="data_drift",
                model_version=model_version,
                detected_at=datetime.utcnow().isoformat(),
                metric_name="input_embedding_cosine_distance",
                metric_value=drift_score,
                threshold=self.drift_threshold,
                severity="warning",
                message=(
                    f"Input distribution drift detected "
                    f"(distance={drift_score:.3f}, threshold={self.drift_threshold}). "
                    f"Monitor closely; consider collecting ground truth for re-eval."
                ),
            )
        return None


# ---------------------------------------------------------------------------
# Output drift detector (length + refusal rate proxy)
# ---------------------------------------------------------------------------


class OutputDriftDetector:
    """
    Detects output distribution drift via proxy metrics:
    - Output length (tokens): significant shift may indicate model behavior change.
    - Refusal rate: increase may indicate safety classifier misconfiguration.
    """

    def __init__(
        self,
        length_drift_threshold_pct: float = 30.0,
        refusal_rate_threshold: float = 0.05,  # 5% refusal rate is unusual
    ):
        self.length_drift_threshold_pct = length_drift_threshold_pct
        self.refusal_rate_threshold = refusal_rate_threshold
        self.reference_length_mean: float | None = None
        self.reference_length_std: float | None = None

    def build_reference(self, output_lengths: list[int]) -> None:
        self.reference_length_mean = float(np.mean(output_lengths))
        self.reference_length_std = float(np.std(output_lengths))

    def check(
        self,
        recent_output_lengths: list[int],
        recent_refusal_count: int,
        model_version: str,
    ) -> list[DriftAlert]:
        alerts = []

        # Length drift
        if self.reference_length_mean is not None:
            recent_mean = float(np.mean(recent_output_lengths))
            pct_change = abs(recent_mean - self.reference_length_mean) / self.reference_length_mean * 100
            if pct_change >= self.length_drift_threshold_pct:
                alerts.append(DriftAlert(
                    alert_type="output_drift",
                    model_version=model_version,
                    detected_at=datetime.utcnow().isoformat(),
                    metric_name="output_length_mean_pct_change",
                    metric_value=pct_change,
                    threshold=self.length_drift_threshold_pct,
                    severity="warning",
                    message=(
                        f"Output length distribution shifted {pct_change:.1f}% from reference "
                        f"(reference mean: {self.reference_length_mean:.0f} tokens, "
                        f"recent mean: {recent_mean:.0f} tokens)."
                    ),
                ))

        # Refusal rate
        n = len(recent_output_lengths)
        if n > 0:
            refusal_rate = recent_refusal_count / n
            if refusal_rate >= self.refusal_rate_threshold:
                alerts.append(DriftAlert(
                    alert_type="output_drift",
                    model_version=model_version,
                    detected_at=datetime.utcnow().isoformat(),
                    metric_name="refusal_rate",
                    metric_value=refusal_rate,
                    threshold=self.refusal_rate_threshold,
                    severity="warning" if refusal_rate < 0.1 else "critical",
                    message=(
                        f"Refusal rate elevated: {refusal_rate:.1%} of recent outputs are refusals "
                        f"(threshold: {self.refusal_rate_threshold:.1%}). "
                        f"Check content filter configuration."
                    ),
                ))

        return alerts


# ---------------------------------------------------------------------------
# Prompt integrity checker
# ---------------------------------------------------------------------------


class PromptIntegrityChecker:
    """
    Detects unauthorized changes to the active system prompt by comparing
    its SHA-256 hash against the version registered at deploy time.
    """

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def register_prompt(self, model_version: str, prompt_text: str) -> str:
        """Register the canonical prompt hash for a model version."""
        prompt_hash = hashlib.sha256(prompt_text.encode()).hexdigest()
        self.redis.set(f"prompt_hash:{model_version}", prompt_hash)
        return prompt_hash

    def check(self, model_version: str, active_prompt_text: str) -> DriftAlert | None:
        """Check if the active prompt matches the registered hash."""
        registered_hash = self.redis.get(f"prompt_hash:{model_version}")
        if registered_hash is None:
            return None  # Not registered; skip check

        registered_hash = registered_hash.decode()
        active_hash = hashlib.sha256(active_prompt_text.encode()).hexdigest()

        if active_hash != registered_hash:
            return DriftAlert(
                alert_type="prompt_drift",
                model_version=model_version,
                detected_at=datetime.utcnow().isoformat(),
                metric_name="prompt_hash_mismatch",
                metric_value=1.0,
                threshold=0.0,
                severity="critical",
                message=(
                    f"System prompt for {model_version} has been modified. "
                    f"Registered hash: {registered_hash[:12]}... "
                    f"Active hash: {active_hash[:12]}... "
                    f"Investigate and version the change or restore the registered prompt."
                ),
            )
        return None


# ---------------------------------------------------------------------------
# Alert dispatcher
# ---------------------------------------------------------------------------


def dispatch_alert(alert: DriftAlert, webhook_url: str | None = None) -> None:
    """Send a drift alert to Slack or log it."""
    message = (
        f"[DRIFT ALERT] {alert.severity.upper()} — {alert.alert_type}\n"
        f"Model: {alert.model_version}\n"
        f"Metric: {alert.metric_name} = {alert.metric_value:.4f} (threshold: {alert.threshold})\n"
        f"Message: {alert.message}\n"
        f"Detected at: {alert.detected_at}"
    )
    print(message)

    if webhook_url:
        import urllib.request
        payload = json.dumps({"text": message}).encode()
        req = urllib.request.Request(webhook_url, data=payload, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)


# ---------------------------------------------------------------------------
# Monitor runner
# ---------------------------------------------------------------------------


class DriftMonitor:
    def __init__(
        self,
        model_version: str,
        redis_url: str = "redis://localhost:6379",
        slack_webhook_url: str | None = None,
    ):
        self.model_version = model_version
        self.redis = redis.from_url(redis_url)
        self.slack_webhook_url = slack_webhook_url
        self.input_detector = InputDriftDetector()
        self.output_detector = OutputDriftDetector()
        self.prompt_checker = PromptIntegrityChecker(self.redis)

    def load_reference_from_redis(self) -> None:
        """Load the reference snapshot stored at deploy time."""
        raw = self.redis.get(f"reference:{self.model_version}")
        if raw is None:
            raise RuntimeError(
                f"No reference snapshot found for {self.model_version}. "
                f"Run with --mode snapshot first."
            )
        ref = json.loads(raw)
        self.input_detector.reference_centroid = np.array(ref["input_centroid"])
        self.output_detector.reference_length_mean = ref["output_length_mean"]
        self.output_detector.reference_length_std = ref["output_length_std"]

    def save_reference_to_redis(self, input_texts: list[str], output_lengths: list[int]) -> None:
        """Build and store the reference snapshot."""
        centroid = self.input_detector.build_reference(input_texts)
        self.output_detector.build_reference(output_lengths)
        ref = {
            "input_centroid": centroid.tolist(),
            "output_length_mean": self.output_detector.reference_length_mean,
            "output_length_std": self.output_detector.reference_length_std,
            "created_at": datetime.utcnow().isoformat(),
            "n_samples": len(input_texts),
        }
        self.redis.set(f"reference:{self.model_version}", json.dumps(ref))
        print(f"[drift-monitor] Reference snapshot saved for {self.model_version} ({len(input_texts)} samples).")

    def run_check(self) -> list[DriftAlert]:
        """Pull recent traffic from Redis and run all drift checks."""
        # Load recent inputs/outputs from the request log (last 500 requests)
        recent_raw = self.redis.lrange(f"traffic:{self.model_version}", -500, -1)
        if len(recent_raw) < 50:
            print(f"[drift-monitor] Insufficient traffic ({len(recent_raw)} records). Skipping check.")
            return []

        recent = [json.loads(r) for r in recent_raw]
        input_texts = [r["input"] for r in recent]
        output_lengths = [r["output_tokens"] for r in recent]
        refusal_count = sum(1 for r in recent if r.get("is_refusal", False))

        alerts = []

        # Input drift
        alert = self.input_detector.check(input_texts, self.model_version)
        if alert:
            alerts.append(alert)

        # Output drift
        alerts.extend(self.output_detector.check(output_lengths, refusal_count, self.model_version))

        # Prompt drift (read active prompt from Redis config store)
        active_prompt = self.redis.get(f"active_prompt:{self.model_version}")
        if active_prompt:
            alert = self.prompt_checker.check(self.model_version, active_prompt.decode())
            if alert:
                alerts.append(alert)

        for alert in alerts:
            dispatch_alert(alert, self.slack_webhook_url)

        return alerts


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Drift monitor for ML/LLM production systems.")
    parser.add_argument("--mode", choices=["snapshot", "monitor"], required=True)
    parser.add_argument("--model-version", required=True)
    parser.add_argument("--interval-minutes", type=int, default=60)
    parser.add_argument("--redis-url", default="redis://localhost:6379")
    parser.add_argument("--slack-webhook", default=os.getenv("SLACK_WEBHOOK_URL"))
    args = parser.parse_args()

    monitor = DriftMonitor(
        model_version=args.model_version,
        redis_url=args.redis_url,
        slack_webhook_url=args.slack_webhook,
    )

    if args.mode == "snapshot":
        # Load recent traffic to build reference
        r = redis.from_url(args.redis_url)
        recent_raw = r.lrange(f"traffic:{args.model_version}", -1000, -1)
        if len(recent_raw) < 100:
            print(f"[drift-monitor] Need ≥100 traffic records. Found {len(recent_raw)}.")
            raise SystemExit(1)
        recent = [json.loads(x) for x in recent_raw]
        monitor.save_reference_to_redis(
            input_texts=[r["input"] for r in recent],
            output_lengths=[r["output_tokens"] for r in recent],
        )

    elif args.mode == "monitor":
        monitor.load_reference_from_redis()
        print(f"[drift-monitor] Starting monitor for {args.model_version} (interval: {args.interval_minutes}m).")

        def run():
            alerts = monitor.run_check()
            print(f"[drift-monitor] {datetime.utcnow().isoformat()} — {len(alerts)} alert(s).")

        schedule.every(args.interval_minutes).minutes.do(run)
        run()  # Run immediately on start

        while True:
            schedule.run_pending()
            time.sleep(30)


if __name__ == "__main__":
    main()

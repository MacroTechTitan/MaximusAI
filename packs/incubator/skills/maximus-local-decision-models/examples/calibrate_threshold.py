#!/usr/bin/env python3
"""Pick a confidence cutoff for one decision model from labeled results.
Input CSV columns: label, predicted, confidence. Prints coverage and accuracy
above each cutoff, and the lowest cutoff meeting --target accuracy.
Usage: python calibrate_threshold.py results.csv [--target 0.95]"""
import csv, sys

def table(rows, steps=(0.0, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)):
    out = []
    for t in steps:
        kept = [r for r in rows if float(r["confidence"]) >= t]
        acc = sum(r["label"] == r["predicted"] for r in kept) / len(kept) if kept else float("nan")
        out.append((t, len(kept) / len(rows), acc))
    return out

if __name__ == "__main__":
    path = sys.argv[1]
    target = float(sys.argv[sys.argv.index("--target") + 1]) if "--target" in sys.argv else 0.95
    rows = list(csv.DictReader(open(path, newline="")))
    print("cutoff  coverage  accuracy")
    best = None
    for t, cov, acc in table(rows):
        print(f"{t:>6.2f}  {cov:>8.0%}  {acc:>8.0%}")
        if best is None and acc == acc and acc >= target:
            best = (t, cov)
    print(f"lowest cutoff meeting {target:.0%}: " + (f"{best[0]:.2f} (handles {best[1]:.0%}, rest to fallback)" if best else "none; improve questions or try another model"))

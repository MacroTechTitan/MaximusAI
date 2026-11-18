#!/usr/bin/env python3
"""Score a coding-agent bake-off: model + harness configurations run on tasks from your own repo.
Input CSV columns: config, task, attempt, passed (0/1), cost_usd, and optional timed_out (0/1),
reward_hacked (0/1). Reward-hacked runs count as failures. Standard library only.
Reports per config: pass rate with a Wilson 95% interval, cost per pass (all spend / passes),
the share of spend that went to runs that did not pass, and sanity anchors:
  --strong A --weak B   a config you expect to be stronger must beat a weaker one
  --null C              a do-nothing or trivial config must pass close to 0
  tasks every config passes (too easy) or none passes (task or grader may be broken)
Usage: python bakeoff_report.py runs.csv [--strong cfgA --weak cfgB] [--null noop]
Exit codes: 0 anchors hold, 2 an anchor failed (fix the benchmark before trusting rankings)."""
import argparse, csv, math, sys
from collections import defaultdict

def wilson(k, n, z=1.96):
    if n == 0:
        return 0.0, 0.0
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("csv"); ap.add_argument("--strong"); ap.add_argument("--weak"); ap.add_argument("--null")
    a = ap.parse_args()
    runs = defaultdict(list); task_pass = defaultdict(lambda: defaultdict(int)); task_n = defaultdict(lambda: defaultdict(int)); tasks = set()
    for r in csv.DictReader(open(a.csv)):
        ok = r["passed"] == "1" and r.get("reward_hacked", "0") != "1"
        cost = float(r["cost_usd"] or 0); to = r.get("timed_out", "0") == "1"
        runs[r["config"]].append((ok, cost, to)); tasks.add(r["task"])
        task_pass[r["task"]][r["config"]] += ok; task_n[r["task"]][r["config"]] += 1
    stats = {}
    print(f"{'config':<22}{'pass':>7}{'95% CI':>15}{'runs':>6}{'$/pass':>9}{'$ on fails':>12}{'timeouts':>10}")
    for cfg, rs in sorted(runs.items()):
        n = len(rs); k = sum(ok for ok, _, _ in rs); spend = sum(c for _, c, _ in rs)
        fail_spend = sum(c for ok, c, _ in rs if not ok); lo, hi = wilson(k, n)
        stats[cfg] = (k, n, lo, hi)
        cpp = f"{spend / k:.2f}" if k else "inf"
        share = f"{fail_spend / spend:.0%}" if spend else "-"
        print(f"{cfg:<22}{k / n:>7.0%}{f'{lo:.0%}-{hi:.0%}':>15}{n:>6}{cpp:>9}{share:>12}{sum(t for _, _, t in rs):>10}")
    bad = 0
    if a.strong and a.weak:
        s, w = stats.get(a.strong), stats.get(a.weak)
        if not s or not w:
            print("ANCHOR strong/weak: config not found"); bad += 1
        elif s[0] / s[1] <= w[0] / w[1]:
            print(f"ANCHOR FAILED: {a.strong} did not beat {a.weak}; tasks or graders may not measure skill"); bad += 1
        elif s[2] <= w[3]:
            print(f"note: {a.strong} beats {a.weak} but the intervals overlap; add tasks or attempts")
    if a.null:
        z = stats.get(a.null)
        if z and z[0] / z[1] > 0.05:
            print(f"ANCHOR FAILED: null config {a.null} passes {z[0] / z[1]:.0%}; graders accept trivial output"); bad += 1
    real = [c for c in runs if c != a.null]
    easy = [t for t in sorted(tasks) if all(task_pass[t][c] == task_n[t][c] for c in real)]
    dead = [t for t in sorted(tasks) if all(task_pass[t][c] == 0 for c in real)]
    if easy: print(f"tasks every config passed on every attempt (low signal): {', '.join(easy)}")
    if dead: print(f"tasks no config passed (check task and grader): {', '.join(dead)}")
    return 2 if bad else 0

if __name__ == "__main__":
    sys.exit(main())

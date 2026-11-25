#!/usr/bin/env python3
"""Measure the PR review queue, split by agent-authored vs human-authored PRs.
Input: JSON from
  gh pr list --state all --limit 1000 --json number,author,headRefName,labels,createdAt,mergedAt,closedAt,additions,deletions,reviews
Agent PRs are matched by --agent-pattern (regex on author login, branch name, or label names).
Reports per segment: PRs opened, share merged, median hours from open to first human review
("backlog wait"), first review to merge ("active review"), open to merge, median size, and the
number open with no review now. Bot reviewers (login ending in [bot] or matching --bot-reviewer)
do not count as a first human review. Standard library only.
Usage: python review_queue_report.py prs.json [--agent-pattern 'claude|codex|copilot|devin|agent/'] [--since 2026-09-01]"""
import argparse, json, re, statistics as st
from datetime import datetime

def t(s): return datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None
def hrs(a, b): return (b - a).total_seconds() / 3600

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("json")
    ap.add_argument("--agent-pattern", default=r"claude|codex|copilot|devin|cursor|agent/|\[bot\]")
    ap.add_argument("--bot-reviewer", default=r"\[bot\]$|copilot|coderabbit|claude")
    ap.add_argument("--since")
    a = ap.parse_args(); ag = re.compile(a.agent_pattern, re.I); bot = re.compile(a.bot_reviewer, re.I)
    since = t(a.since + "T00:00:00Z") if a.since else None
    seg = {"agent": [], "human": []}
    for p in json.load(open(a.json)):
        c = t(p["createdAt"])
        if since and c < since: continue
        keys = " ".join([(p.get("author") or {}).get("login", ""), p.get("headRefName", "")] + [l["name"] for l in p.get("labels", [])])
        human_reviews = sorted(t(r["submittedAt"]) for r in p.get("reviews", [])
                               if r.get("submittedAt") and not bot.search((r.get("author") or {}).get("login", "")))
        seg["agent" if ag.search(keys) else "human"].append(dict(c=c, m=t(p.get("mergedAt")), x=t(p.get("closedAt")),
            r=human_reviews[0] if human_reviews else None, size=p.get("additions", 0) + p.get("deletions", 0)))
    med = lambda xs: f"{st.median(xs):.1f}" if xs else "-"
    print(f"{'segment':<8}{'opened':>7}{'merged':>8}{'wait h':>8}{'review h':>9}{'merge h':>9}{'size':>7}{'unreviewed open':>17}")
    out = {}
    for name, ps in seg.items():
        if not ps: continue
        merged = [p for p in ps if p["m"]]
        wait = [hrs(p["c"], p["r"]) for p in ps if p["r"]]
        active = [hrs(p["r"], p["m"]) for p in merged if p["r"] and p["m"] >= p["r"]]
        tomerge = [hrs(p["c"], p["m"]) for p in merged]
        unrev = sum(1 for p in ps if not p["m"] and not p["x"] and not p["r"])
        out[name] = (len(merged) / len(ps), st.median(wait) if wait else None)
        print(f"{name:<8}{len(ps):>7}{len(merged)/len(ps):>8.0%}{med(wait):>8}{med(active):>9}{med(tomerge):>9}"
              f"{med([p['size'] for p in ps]):>7}{unrev:>17}")
    if "agent" in out and "human" in out:
        (am, aw), (hm, hw) = out["agent"], out["human"]
        if am < hm - 0.10: print(f"note: agent PRs merge at {am:.0%} vs {hm:.0%} for human PRs; review abandoned agent PRs and tighten what gets opened")
        if aw and hw and aw > 1.5 * hw: print("note: agent PRs wait over 1.5x longer for a first human review; cap agent PRs in flight per reviewer")

if __name__ == "__main__":
    main()

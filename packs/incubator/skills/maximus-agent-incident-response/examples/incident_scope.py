#!/usr/bin/env python3
"""Scope an AI agent incident from its action log. Standard library only.
Input: JSONL, one tool call per line: {"ts": "...", "tool": "bash", "input": "...", "ok": true}
Output: a timeline of risky actions, grouped into what to revoke, what to reverse, and
who outside your team may be affected. Patterns are a starting point, not a classifier:
read the full log before concluding anything was harmless.
Usage: python incident_scope.py actions.jsonl [--start TS] [--end TS]"""
import argparse, json, re, sys
from collections import defaultdict

RULES = [
    ("destructive", r"\brm\s+-[a-z]*r|\bDROP\s+(TABLE|DATABASE)|\bTRUNCATE\b|\bDELETE\s+FROM\b(?!.*\bWHERE\b)|terraform\s+destroy|kubectl\s+delete|git\s+push\s+.*--force|\bgit\s+reset\s+--hard"),
    ("credential", r"(AWS_|GITHUB_|OPENAI_|ANTHROPIC_|STRIPE_)[A-Z_]*|\.env\b|id_rsa|\.aws/credentials|\btoken\b|\bsecret\b|api[_-]?key"),
    ("egress", r"\b(curl|wget|nc|ssh|scp)\b\s|https?://(?!localhost|127\.0\.0\.1)"),
    ("external_write", r"\bgit\s+push\b|\bgh\s+(pr|issue|release)\s+create|npm\s+publish|twine\s+upload|send_?(email|message)|\bPOST\b"),
    ("scan", r"\bnmap\b|masscan|for\s+\w+\s+in\s+.*\d+\.\d+\.\d+"),
]
HOST = re.compile(r"https?://([^/\s\"']+)|[\w.+-]+@([\w.-]+\.[a-z]{2,})|\bssh\s+(?:\S+@)?([\w.-]+)")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("log"); ap.add_argument("--start"); ap.add_argument("--end")
    a = ap.parse_args()
    found, hosts, n = defaultdict(list), set(), 0
    for i, line in enumerate(open(a.log), 1):
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            print(f"WARN line {i}: not JSON (log may be truncated or tampered)"); continue
        ts = ev.get("ts", "")
        if (a.start and ts < a.start) or (a.end and ts > a.end):
            continue
        n += 1
        text = f"{ev.get('tool','')} {ev.get('input','')}"
        for kind, pat in RULES:
            if re.search(pat, text, re.I):
                found[kind].append((ts, ev.get("tool", ""), str(ev.get("input", ""))[:110], ev.get("ok")))
        for m in HOST.finditer(text):
            h = next(g for g in m.groups() if g)
            if h not in ("localhost", "127.0.0.1"):
                hosts.add(h)
    print(f"{n} actions in window")
    labels = {"destructive": "REVERSE (restore from backup, verify rollback yourself)",
              "credential": "REVOKE (rotate every credential the agent could read)",
              "egress": "CHECK (outbound traffic: what left, to whom)",
              "external_write": "REVERSE OR DISCLOSE (writes visible outside your systems)",
              "scan": "NOTIFY (scanning or probing other hosts)"}
    for kind, label in labels.items():
        if found[kind]:
            print(f"\n== {kind}: {label}")
            for ts, tool, inp, ok in found[kind]:
                print(f"  {ts} [{'ok' if ok else 'failed' if ok is False else '?'}] {tool}: {inp}")
    if hosts:
        print("\n== external hosts contacted (possible third parties to notify): " + ", ".join(sorted(hosts)))
    return 2 if any(found.values()) else 0

if __name__ == "__main__":
    sys.exit(main())

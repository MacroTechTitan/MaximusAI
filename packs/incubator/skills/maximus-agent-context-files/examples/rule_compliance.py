#!/usr/bin/env python3
"""Measure how often agent sessions followed checkable rules from AGENTS.md / CLAUDE.md.
Input: a rules JSON and one unified diff per agent session (a directory of *.diff files).
Each rule names a trigger regex on added lines and a requirement on the next added line,
or a forbidden regex on added lines. A session complies with a rule only if every trigger
in it meets the requirement (the strict all-or-nothing criterion from arXiv 2611.04367).
Sessions where a rule never triggers are excluded from that rule's rate.
Rules whose rate falls below --threshold are reported as candidates for a hook or CI check.
Standard library only.
Usage: python rule_compliance.py --rules rules.json --sessions sessions/ [--threshold 0.95]"""
import argparse, json, pathlib, re, sys

def added_lines(diff):
    f, out = None, []
    for line in diff.splitlines():
        if line.startswith("+++ "):
            f = line[4:].removeprefix("b/")
        elif f and line.startswith("+") and not line.startswith("+++"):
            out.append((f, line[1:]))
    return out

def check(rule, lines):
    glob = re.compile(rule.get("file_regex", ".*"))
    lines = [(f, t) for f, t in lines if glob.search(f)]
    if "forbid" in rule:
        if not lines:
            return None, 0
        hits = [t for _, t in lines if re.search(rule["forbid"], t)]
        return (False if hits else True), 1
    trig, need = re.compile(rule["trigger"]), re.compile(rule["next_line"])
    n, ok = 0, True
    for i, (f, t) in enumerate(lines):
        if trig.search(t):
            n += 1
            nxt = lines[i + 1][1] if i + 1 < len(lines) and lines[i + 1][0] == f else ""
            if not need.search(nxt):
                ok = False
    return (ok if n else None), n

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rules", required=True); ap.add_argument("--sessions", required=True)
    ap.add_argument("--threshold", type=float, default=0.95)
    a = ap.parse_args()
    rules = json.load(open(a.rules))
    sessions = sorted(pathlib.Path(a.sessions).glob("*.diff"))
    if not sessions:
        print("no *.diff files found"); return 1
    weak = 0
    for rule in rules:
        results = [check(rule, added_lines(s.read_text()))[0] for s in sessions]
        applied = [r for r in results if r is not None]
        if not applied:
            print(f"{rule['id']}: never triggered in {len(sessions)} sessions"); continue
        rate = sum(applied) / len(applied)
        verdict = "ok" if rate >= a.threshold else "MOVE TO HOOK OR CI"
        weak += rate < a.threshold
        print(f"{rule['id']}: {sum(applied)}/{len(applied)} sessions compliant ({rate:.0%}) [{rule.get('wording','')}] -> {verdict}")
    return 2 if weak else 0

if __name__ == "__main__":
    sys.exit(main())

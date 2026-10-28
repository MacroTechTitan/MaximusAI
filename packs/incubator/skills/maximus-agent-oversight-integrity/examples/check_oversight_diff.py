#!/usr/bin/env python3
"""Flag changes that weaken oversight in a unified diff, and check whether the agent's
final report disclosed them. Heuristic: a flag means a human must look, not that the
change is malicious. Standard library only.
Usage: git diff main...HEAD | python check_oversight_diff.py --policy oversight_policy.json [--report final_message.txt]
Exit codes: 0 clean, 1 oversight changes found (disclosed), 2 oversight changes found and not disclosed."""
import argparse, json, re, sys

def parse(diff):
    f = None
    for line in diff.splitlines():
        if line.startswith("+++ "):
            f = line[4:].removeprefix("b/")
        elif line.startswith("--- ") and line[4:] != "/dev/null":
            f = f or line[4:].removeprefix("a/")
        elif f and line[:1] in "+-" and not line.startswith(("+++", "---")):
            yield f, line[0], line[1:]

def check(diff, pol):
    ids = [re.escape(i) for i in pol["protected_identifiers"]]
    idre = re.compile(r"\b(" + "|".join(ids) + r")\w*", re.I)
    findings = []
    for f, sign, text in parse(diff):
        protected_path = any(f.startswith(p) or ("/" + p) in f for p in pol["protected_paths"])
        hit = idre.search(text)
        if sign == "-" and (hit or protected_path):
            findings.append((f, "removed", text.strip()))
        elif sign == "+":
            if hit and re.search(r"=\s*(\[\]|\"\"|''|None|False|0)\s*,?$", text.strip()):
                findings.append((f, "emptied or disabled", text.strip()))
            elif re.search(r"no_notify\w*\s*[:=]\s*(True|true|1)", text):
                findings.append((f, "notifications suppressed", text.strip()))
            elif hit and re.search(r"assert\s+.*\bnot\s+in\b|assert\s+not\s|assertFalse|assertNotIn", text):
                findings.append((f, "test now requires oversight to be absent", text.strip()))
            elif protected_path:
                findings.append((f, "protected path changed", text.strip()))
    return findings

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--policy", required=True); ap.add_argument("--report")
    a = ap.parse_args(); pol = json.load(open(a.policy)); findings = check(sys.stdin.read(), pol)
    for f, kind, text in findings: print(f"FLAG {kind}: {f}: {text[:120]}")
    if not findings: print("no oversight changes found"); return 0
    if a.report:
        rep = open(a.report).read().lower()
        if not any(w in rep for w in pol["disclosure_words"]):
            print(f"UNDISCLOSED: {len(findings)} oversight change(s), and the agent's report does not mention monitoring or alerts"); return 2
    print(f"{len(findings)} oversight change(s): require human sign-off before merge"); return 1

if __name__ == "__main__":
    sys.exit(main())

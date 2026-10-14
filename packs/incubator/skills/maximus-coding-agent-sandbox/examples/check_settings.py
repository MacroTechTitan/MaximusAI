#!/usr/bin/env python3
"""Lint a Claude Code settings.json sandbox block for common weak spots.
Heuristic checks only; it does not prove containment. Run the probes too.
Usage: python check_settings.py ~/.claude/settings.json   (exit 1 on findings)"""
import json, sys

SECRETS = ("~/.ssh", "~/.aws", ".env")
AUTOEXEC = (".git/hooks", ".mcp.json", ".claude/commands", ".claude/agents")

def check(cfg):
    s, out = cfg.get("sandbox", {}), []
    if not s.get("enabled"): out.append("sandbox.enabled is not true (off by default)")
    if not s.get("failIfUnavailable"): out.append("failIfUnavailable not set: a missing dependency means unsandboxed commands")
    if s.get("allowUnsandboxedCommands", True): out.append("allowUnsandboxedCommands not false: the unsandboxed retry escape hatch is open")
    fs, net = s.get("filesystem", {}), s.get("network", {})
    reads = " ".join(fs.get("denyRead", []))
    for p in SECRETS:
        if p not in reads: out.append(f"no read deny covering {p}")
    writes = " ".join(fs.get("denyWrite", []))
    for p in AUTOEXEC:
        if p not in writes: out.append(f"no write deny for auto-executed path {p}")
    for d in net.get("allowedDomains", []):
        if d.strip() in ("*", "*.*") or d.startswith("*.com"): out.append(f"egress wildcard too broad: {d}")
    for c in s.get("excludedCommands", []):
        if c.strip() in ("*", "bash *", "sh *", "python *", "node *", "docker *"):
            out.append(f"excludedCommands entry runs arbitrary code unsandboxed: {c}")
    return out

if __name__ == "__main__":
    findings = check(json.load(open(sys.argv[1])))
    for f in findings: print("WARN", f)
    print(f"{len(findings)} finding(s)")
    sys.exit(1 if findings else 0)

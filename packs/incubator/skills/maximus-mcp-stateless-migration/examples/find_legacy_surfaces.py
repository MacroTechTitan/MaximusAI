#!/usr/bin/env python3
"""Scan a source tree for MCP surfaces removed or replaced in spec 2026-07-28.
Usage: python find_legacy_surfaces.py <src_dir>   (exit 1 if anything found)"""
import os, re, sys

PATTERNS = {
    "Mcp-Session-Id": "session header removed; move state to explicit handles",
    "notifications/initialized": "handshake removed; serve per-request _meta (or dual-era)",
    '"initialize"': "handshake removed; serve per-request _meta (or dual-era)",
    "logging/setLevel": "removed; log level is per-request in _meta",
    "elicitation/create": "server-initiated; convert to MRTR (resultType input_required)",
    "sampling/createMessage": "server-initiated and deprecated; convert to MRTR",
    "roots/list": "server-initiated and deprecated; convert to MRTR",
    "Last-Event-ID": "SSE resumability removed; clients re-issue requests",
    "from mcp.server.fastmcp": "Python SDK v2 renamed FastMCP to MCPServer",
}
EXT = (".py", ".ts", ".js", ".mjs", ".go", ".cs", ".rs", ".java", ".kt")

def scan(root):
    hits = []
    for d, _, files in os.walk(root):
        if any(p in d for p in ("node_modules", ".git", "dist", "build", ".venv")):
            continue
        for f in files:
            if not f.endswith(EXT):
                continue
            p = os.path.join(d, f)
            for n, line in enumerate(open(p, encoding="utf-8", errors="ignore"), 1):
                for pat, why in PATTERNS.items():
                    if pat in line:
                        hits.append((p, n, pat, why))
    return hits

if __name__ == "__main__":
    hits = scan(sys.argv[1] if len(sys.argv) > 1 else ".")
    for p, n, pat, why in hits:
        print(f"{p}:{n}: {pat} -> {why}")
    print(f"{len(hits)} legacy surface(s) found")
    sys.exit(1 if hits else 0)

#!/usr/bin/env python3
"""Estimate the per-run prompt Maximus adds to OpenClaw.

Usage: measure_prompt.py <maximus-repo-or-openclaw-workspace>

Counts core/memory markdown and each skill's name + description (plus ~24
tokens of per-skill overhead, per CLAUDE.md). Uses ~4 chars/token: an estimate,
not a tokenizer. OpenClaw's own system prompt and tool schemas are NOT included.
"""
import glob, os, re, sys

root = sys.argv[1] if len(sys.argv) > 1 else "."
def chars(pattern):
    return sum(len(open(f, encoding="utf-8").read()) for f in glob.glob(os.path.join(root, pattern)))

core = chars("core/*.md")
if core == 0:  # an OpenClaw workspace holds SOUL/AGENTS/TOOLS at its root
    core = sum(chars(n) for n in ("SOUL.md", "AGENTS.md", "TOOLS.md"))
mem = chars("memory/*.md")
skills, n = 0, 0
for f in glob.glob(os.path.join(root, "skills/*/SKILL.md")):
    if "/_template/" in f:
        continue
    fm = re.match(r"^---\n(.*?)\n---", open(f, encoding="utf-8").read(), re.S)
    if not fm:
        continue
    name = re.search(r"^name:\s*(.*)$", fm.group(1), re.M)
    desc = re.search(r"^description:\s*(.*)$", fm.group(1), re.M)
    skills += len(name.group(1) if name else "") + len(desc.group(1) if desc else "") + 96
    n += 1

tok = lambda c: c // 4
total = tok(core + mem + skills)
print(f"core      {tok(core):>7,} tok")
print(f"memory    {tok(mem):>7,} tok")
print(f"skills    {tok(skills):>7,} tok  ({n} entries)")
print(f"total     {total:>7,} tok  (before OpenClaw's own prompt + tools)")
for ctx in (4096, 8192, 32768, 65536):
    print(f"  num_ctx {ctx:>6}: {100 * total / ctx:5.1f}% used by Maximus alone")

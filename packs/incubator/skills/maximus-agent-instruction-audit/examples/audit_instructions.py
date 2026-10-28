#!/usr/bin/env python3
"""Show which agent instruction files would load if a coding agent started in DIR,
and flag risky start folders, risky instructions, and config drift.
Covers Claude Code (CLAUDE.md, CLAUDE.local.md, .claude/CLAUDE.md, .claude/rules) and
Codex (AGENTS.override.md / AGENTS.md from git root down to DIR, plus CODEX_HOME).
Heuristic: pattern matches are leads to read, not proof. Standard library only.
Usage: python audit_instructions.py [DIR] [--home HOME]   (exit 1 if anything is flagged)"""
import argparse, json, os, re, sys
from pathlib import Path

RISKY_DIRS = ("Downloads", "Desktop", "tmp", "Temp")
PATTERNS = [
    (r"ANTHROPIC_BASE_URL|OPENAI_BASE_URL|chatgpt_base_url|base_url\s*=", "changes the model API endpoint"),
    (r"\[mcp_servers|mcpServers|\.mcp\.json|add (an? )?mcp server", "adds or edits an MCP server"),
    (r"npm (i|install)\b|npx\s|pip install|uv add|curl[^\n|]*\|\s*(ba)?sh|wget[^\n|]*\|\s*(ba)?sh", "installs or runs remote code"),
    (r"dangerously|--yolo|bypass(Permissions| permissions)|approval_policy\s*=\s*\"never\"|sandbox_mode\s*=\s*\"danger", "disables approvals or sandbox"),
    (r"\.codex/config\.toml|\.claude/settings(\.local)?\.json|settings\.json", "edits agent configuration"),
    (r"(do not|don't|never) (tell|mention|inform|show) (the )?user", "asks the agent to hide actions"),
]

def git_root(d):
    for p in [d, *d.parents]:
        if (p / ".git").exists():
            return p
    return None

def claude_files(d, home):
    out = []
    for p in reversed([d, *d.parents]):            # root toward cwd, as Claude Code orders them
        for name in ("CLAUDE.md", ".claude/CLAUDE.md", "CLAUDE.local.md"):
            f = p / name
            if f.is_file(): out.append(f)
    rules = d / ".claude" / "rules"
    if rules.is_dir(): out += sorted(rules.rglob("*.md"))
    for f in (home / ".claude" / "CLAUDE.md",):
        if f.is_file(): out.insert(0, f)
    urules = home / ".claude" / "rules"
    if urules.is_dir(): out[:0] = sorted(urules.rglob("*.md"))
    return out

def codex_files(d, home):
    out = []
    ch = Path(os.environ.get("CODEX_HOME", home / ".codex"))
    for name in ("AGENTS.override.md", "AGENTS.md"):
        f = ch / name
        if f.is_file() and f.stat().st_size: out.append(f); break
    root = git_root(d) or d
    chain = [root] + [p for p in reversed(list(d.parents)) if root in p.parents] + ([d] if d != root else [])
    for p in dict.fromkeys(chain):
        for name in ("AGENTS.override.md", "AGENTS.md"):
            f = p / name
            if f.is_file() and f.stat().st_size: out.append(f); break   # one file per directory
    return out

def scan_text(path):
    try: t = path.read_text(errors="replace")
    except OSError: return []
    return [why for pat, why in PATTERNS if re.search(pat, t, re.I)]

def config_drift(d, home):
    hits = []
    cfg = Path(os.environ.get("CODEX_HOME", home / ".codex")) / "config.toml"
    if cfg.is_file():
        t = cfg.read_text(errors="replace")
        for m in re.findall(r"^\[mcp_servers\.([^\]]+)\]", t, re.M):
            hits.append(f"{cfg}: MCP server '{m}' (confirm you added it)")
        if re.search(r"^\s*chatgpt_base_url\s*=", t, re.M):
            hits.append(f"{cfg}: chatgpt_base_url is set (confirm the endpoint)")
    for s in (d / ".claude" / "settings.json", d / ".claude" / "settings.local.json", home / ".claude" / "settings.json"):
        if s.is_file():
            try: env = json.loads(s.read_text()).get("env", {})
            except (ValueError, AttributeError): hits.append(f"{s}: unreadable JSON"); continue
            for k in ("ANTHROPIC_BASE_URL", "HTTPS_PROXY", "HTTP_PROXY"):
                if k in env: hits.append(f"{s}: env {k}={env[k]} (confirm you set it)")
    return hits

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("dir", nargs="?", default="."); ap.add_argument("--home", default=str(Path.home()))
    a = ap.parse_args(); d = Path(a.dir).resolve(); home = Path(a.home).resolve(); flagged = 0
    if d == home or d.name in RISKY_DIRS:
        print(f"RISKY START FOLDER: {d} (other people's files land here; start agents in the project folder)"); flagged += 1
    for agent, files in (("Claude Code", claude_files(d, home)), ("Codex", codex_files(d, home))):
        print(f"\n{agent} would load {len(files)} instruction file(s):")
        for f in files:
            why = scan_text(f); flagged += bool(why)
            print(f"  {'FLAG' if why else 'ok  '} {f}" + (f"  <- {', '.join(why)}" if why else ""))
    drift = config_drift(d, home)
    if drift: print("\nConfig to confirm:"); [print("  " + h) for h in drift]
    flagged += len(drift)
    print(f"\n{flagged} item(s) to review"); return 1 if flagged else 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Claude Code PreToolUse command hook: deny reads of .env files.
Exit 2 blocks the call and sends stderr to the model (hooks reference, Nov 2026).
Register under hooks.PreToolUse with matcher "Read|Bash" in .claude/settings.json.
A deny rule such as Read(./.env) in permissions does the same for Read alone and is the
simpler choice; the hook is shown because it also covers `cat .env` through Bash."""
import json, re, sys
event = json.load(sys.stdin)
inp = event.get("tool_input", {})
target = inp.get("file_path", "") + " " + inp.get("command", "")
if re.search(r"(^|[\s/])\.env(\.[\w-]+)?(\s|$)", target):
    print("Blocked by policy no-env-read: .env files hold secrets. Ask the user for the value you need.", file=sys.stderr)
    sys.exit(2)
sys.exit(0)

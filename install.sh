#!/usr/bin/env bash
# Maximus installer — links this bundle into your OpenClaw workspace.
# Free, open, single-tenant. No keys collected, nothing phoned home.
set -euo pipefail

# ── Resolve paths ────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"

echo "Maximus → installing into: $WORKSPACE"
mkdir -p "$WORKSPACE" "$WORKSPACE/skills"

# ── Link core prompt files (SOUL/AGENTS/TOOLS) ──────────────────────────────
# OpenClaw injects these from the workspace root on every agent run.
for f in SOUL.md AGENTS.md TOOLS.md; do
  ln -sfn "$SCRIPT_DIR/core/$f" "$WORKSPACE/$f"
  echo "  linked core/$f"
done

# ── Link memory store ───────────────────────────────────────────────────────
ln -sfn "$SCRIPT_DIR/memory" "$WORKSPACE/memory"
echo "  linked memory/"

# ── Link skills (skip the _template) ────────────────────────────────────────
for skill_dir in "$SCRIPT_DIR"/skills/*/; do
  name="$(basename "$skill_dir")"
  [ "$name" = "_template" ] && continue
  ln -sfn "$skill_dir" "$WORKSPACE/skills/$name"
  echo "  linked skill: $name"
done

# ── Opt-in packs ────────────────────────────────────────────────────────────
# Packs are project/domain-specific and OFF by default. To enable one:
#   ln -sfn "$SCRIPT_DIR/packs/<pack>/skills/<skill>" "$WORKSPACE/skills/<skill>"
# (Each pack documents its own skills in packs/<pack>/README.md.)

echo ""
echo "Done. Next steps:"
echo "  1. Edit memory/memory.md to teach Maximus about you."
echo "  2. Copy config/openclaw.example.json into ~/.openclaw/openclaw.json and pick a model."
echo "  3. Start the gateway:  openclaw gateway"
echo ""
echo "Maximus uses symlinks — edits to this repo apply live, and 'git pull' updates everything."

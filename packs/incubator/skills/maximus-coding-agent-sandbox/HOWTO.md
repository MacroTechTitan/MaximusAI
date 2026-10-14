# HOWTO — Coding Agent Sandbox

## 1. Everyday Claude Code on your laptop
Install bubblewrap and socat on Linux/WSL2 (macOS uses Seatbelt). Copy `examples/claude-settings.sandbox.json` into `~/.claude/settings.json`, adjust `allowedDomains` to your registries, restart, then ask Claude to run the probes in `examples/probe.sh`. Check the settings with `python examples/check_settings.py ~/.claude/settings.json`.

## 2. Unattended runs
Run the agent inside a dev container or the sandbox runtime (`npx @anthropic-ai/sandbox-runtime claude`) so file tools, MCP servers, and hooks are inside the boundary too. Non-root user, project directory mounted, nothing else.

## 3. Untrusted repository
Use a disposable VM or a hosted cloud session. No personal credentials inside. Throw the environment away afterwards.

## 4. Team rollout
Put the sandbox policy in managed settings so repository files cannot widen it. Require `failIfUnavailable` and disable unsandboxed retries. Review exclusions in code review like permission changes.

## 5. Other agents
Codex: set `sandbox_mode` and `approval_policy`. Claude Code, Codex, and Copilot CLI all wrap commands in Seatbelt on macOS and bubblewrap on Linux. For agents with no built-in sandbox, wrap the whole process in a container with an egress proxy.

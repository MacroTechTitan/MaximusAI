---
name: maximus-coding-agent-sandbox
description: "Contain coding agents (Claude Code, Codex, OpenClaw, others) with an OS-enforced boundary: pick the layer per risk, strict sandbox mode, secret read denies, narrow egress allowlist, protect auto-executed paths, wrap MCP servers and hooks, and prove it with probes. Use for 'sandbox coding agent', 'YOLO mode safely', 'agent egress allowlist'."
metadata: {"openclaw": {"emoji": "📦", "pillar": "ai-engineering", "source": "maximus-scout"}}
---

# Maximus — Coding Agent Sandbox

Approval prompts are a per-action control and people approve almost everything. Prompt injection arrives through files, READMEs, issues, web pages, and MCP tool results. The control that holds regardless of what the model was tricked into is a boundary the operating system enforces: what the agent can read, write, and reach on the network.

## Purpose

Run coding agents with fewer prompts or fully unattended without handing them your keys, your home directory, or the open internet, and verify the boundary with probes instead of trusting the config. Settings names and versions are in `references/agent-sandbox-2026-10.md`; vendors change them often.

## Scope boundary

| Need | Use |
|---|---|
| OS-level containment for a coding agent's runtime | this skill |
| Inventory and right-size agent credentials and grants | maximus-agent-access-review (incubator) |
| Prompt-injection defense and output filtering in an AI product | maximus-ai-safety-governance |
| Agent design: tools, loop, memory | maximus-agent-design |
| CI/CD secrets and deploy pipelines | maximus-devops-ship |
| Running OpenClaw on local models | maximus-openclaw-local |

## Core workflow

1. **Name what is untrusted.** The repo, its dependencies, issue and PR text, web pages the agent reads, and MCP tool results. If any of these can carry instructions, assume they will.
2. **Pick the layer for the risk.** Built-in per-command sandbox for everyday work on your machine; whole-process sandbox runtime, dev container, or container for unattended runs; a dedicated VM or hosted cloud session for untrusted repositories.
3. **Know what the per-command sandbox misses.** In Claude Code it wraps shell commands only. Built-in file tools, MCP servers, hooks, and helper processes run outside it with your access. If those matter, move the whole process inside a boundary.
4. **Turn it on and make it strict.** Enable the sandbox globally, make startup fail if the sandbox is unavailable, and disable the unsandboxed-retry escape hatch.
5. **Deny secret reads explicitly.** Reads are broadly allowed by default, including credential files. List `~/.ssh`, cloud credential files, `.env` files, and agent config files that hold keys. Scrub secrets from subprocess environments.
6. **Allowlist egress, narrowly.** Start empty and add only package registries and the model endpoint the session needs. Exfiltration needs a destination; a secret plus one permissive host is enough to lose it.
7. **Protect auto-executed paths.** Deny writes to `.git/hooks`, `.git/config`, `.mcp.json`, agent command and agent-definition folders, editor task folders, and shell startup files. These are where a session plants code that runs later, outside the boundary.
8. **Audit the exclusions.** Treat `excludedCommands` (or your agent's equivalent) like a sudoers file. A broad exclusion for a tool that executes project files lets the agent write the file and run it unsandboxed.
9. **Give it throwaway credentials.** Scoped, short-lived tokens for the task, never your personal keys. Pair with maximus-agent-access-review.
10. **Probe, then enforce.** Have the agent itself run the probes in `examples/probe.sh` (write outside the project, read a secret, reach an unlisted host). All must fail. For a team, enforce the policy through managed settings so a repository cannot loosen it.

## Anti-patterns

- **Running bypass-permissions or full-auto mode on the host.** With no prompts, the boundary is the only control; put the whole process in a container, VM, or sandbox runtime, as a non-root user.
- **Assuming the sandbox is on.** It is off by default in Claude Code, and by default a missing dependency means commands run unsandboxed.
- **Testing by typing the probe yourself.** Commands typed at the shell-mode prompt usually run outside the sandbox; the agent has to run them.
- **Wildcard egress** (`*` or broad domains) because one install failed.
- **Mounting the home directory into the container.** Mount the project only.
- **Trusting a sandbox you have not updated.** Escapes and boundary bypasses are reported regularly; keep agent runtimes current.

## Output

The chosen layer per workflow (everyday, unattended, untrusted repo), the committed settings file, the managed-policy file for the team if any, the probe results with each probe failing as intended, and the exclusion list with a reason per entry.

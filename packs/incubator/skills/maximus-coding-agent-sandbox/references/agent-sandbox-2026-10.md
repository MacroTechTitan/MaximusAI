# Coding agent sandboxing — facts and sources (pulled 2026-10-14)

| Fact | Source |
|---|---|
| Claude Code Bash sandbox: OS-enforced, off by default; enable with `/sandbox` or `sandbox.enabled`; covers Bash, PowerShell, Monitor commands and child processes; macOS, Linux, WSL2 (not native Windows) | https://code.claude.com/docs/en/sandboxing |
| Defaults: writes to working dir, per-user temp, added dirs; reads most of the machine incl. `~/.ssh` and `~/.aws/credentials`; network via proxy with allowlist that starts empty; env vars inherited | https://code.claude.com/docs/en/sandboxing |
| Outside the sandbox: Read/Edit/Write/WebFetch tools, hooks, local MCP servers, plugin monitors, LSP servers, helper commands; `!` shell-mode commands usually; `excludedCommands`; unsandboxed retries | https://code.claude.com/docs/en/sandboxing |
| If the sandbox can't start, commands run unsandboxed unless `sandbox.failIfUnavailable: true`; `allowUnsandboxedCommands: false` disables the `dangerouslyDisableSandbox` retry (strict sandbox mode) | https://code.claude.com/docs/en/sandboxing |
| Linux/WSL2 deps: bubblewrap and socat; optional seccomp filter via `@anthropic-ai/sandbox-runtime`; Ubuntu 24.04+ may need an AppArmor profile for bwrap | https://code.claude.com/docs/en/sandboxing |
| Probes: `touch ~/sandbox-probe` should fail; `curl --noproxy '*' https://example.com` should fail; typing them yourself doesn't test the sandbox | https://code.claude.com/docs/en/sandboxing |
| Excluded commands run with full access; a pattern covering a tool that acts on project files lets Claude write then run it unsandboxed | https://code.claude.com/docs/en/sandboxing |
| Isolation options compared: sandboxed Bash, sandbox runtime (whole process, beta), dev container, custom container, VM, cloud sessions; untrusted repo → dedicated VM or cloud session | https://code.claude.com/docs/en/sandbox-environments |
| `--dangerously-skip-permissions` should always run inside a container, VM, or the sandbox runtime, as non-root; Claude Code refuses this flag as root on Linux/macOS | https://code.claude.com/docs/en/sandbox-environments |
| Sandbox runtime denies by default writes to `.git/hooks`, `.git/config`, `.mcp.json`, `.claude/commands`, `.claude/agents`, shell startup files; on Linux the deny list is built once at launch | https://code.claude.com/docs/en/sandbox-environments |
| "If credentials never enter the sandbox, they can't be exfiltrated" (Anthropic engineering, Oct 2, 2026) | https://www.anthropic.com/engineering/how-we-contain-claude |
| Codex: set `sandbox_mode` and `approval_policy`; bound filesystem, network, credentials, and git; agent config dirs (`.claude/`, `.vscode/`, `.cursor/`) used as persistence targets in a 2026 campaign | https://codersera.com/blog/how-to-sandbox-ai-coding-agents-2026/amp/ (Oct 6, 2026) |
| Claude Code, Codex, and Copilot CLI wrap agent-run commands in Seatbelt on macOS and bubblewrap on Linux | https://www.developersdigest.tech/blog/coding-agent-local-sandbox-compared-2026 (Oct 9, 2026) |
| Trend signal: "Repeat-After-Me" made six agent frameworks run attacker-written tool calls; testing tool found bugs in 118 of 273 runnable open-source MCP servers | https://www.csoonline.com/article/4233811/researchers-bypass-6-ai-agent-frameworks-with-a-simple-repeat-after-me-prompt.html (Oct 13, 2026) |
| Trend signal: OpenClaw data exfiltration from a sandboxed deployment via the agent's task queue; credentials stored in plaintext config | https://www.lasso.security/blog/sandboxed-ai-agents-attack-surface (Oct 12, 2026) |

Volatile: setting names, version numbers, defaults. Recheck before relying on them.

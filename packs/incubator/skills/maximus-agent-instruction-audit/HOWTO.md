# HOWTO — Agent Instruction Audit

## 1. Before starting an agent in a folder
`python examples/audit_instructions.py /path/to/project`. Exit 1 means something needs a look: a risky folder, a flagged instruction file, or config to confirm. Read every flagged file in full.

## 2. After cloning a repository
Run the audit on the clone before the first agent session, and read every `AGENTS.md`, `CLAUDE.md`, `.claude/rules/*.md`, and any file they import.

## 3. Weekly drift check
Run the audit against your home directory (`--home ~`) and main projects, and diff `~/.codex/config.toml` and `.claude/settings*.json` against a known-good copy kept outside the agent's write access.

## 4. Team enforcement
Commit managed settings that deny agent writes to their own config and instruction files, keep the sandbox on, and require review (CODEOWNERS) for instruction files. Add a `PreToolUse` hook that blocks edits to agent config paths.

## 5. If a file was malicious
Delete it, revert the config change, rotate the agent login token and keys in its environment, check installed packages, and tell anyone who shares the machine or repository.

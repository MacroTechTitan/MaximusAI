# HOWTO — Agent Access Review

## 1. First review in a small team (half a day)
List every AI tool anyone uses for work, every MCP server in developer configs, and every OAuth grant with AI or automation in the name. Fill `examples/agent_inventory.csv`, run `python examples/score_inventory.py examples/agent_inventory.csv`, and fix the top five.

## 2. Coding agents with production reach
For each coding agent, check whether it can reach production credentials, CI secrets, Terraform state, or kubeconfigs. Move those behind a separate identity the agent does not hold, and require a human-run step for apply or destroy.

## 3. MCP server intake
Before adding an MCP server: record owner, capabilities (shell, file, network), credential it will hold, and expiry. Reject any that combine data read and network egress without a written reason.

## 4. Revocation drill
Pick one low-risk agent. Revoke its credential at the identity provider, then watch whether its current session keeps working. If it does, add session termination to the runbook and repeat until both stop.

## 5. Recovery test
For one system an agent can write to, confirm a backup exists in a location the agent's credentials cannot reach, and restore a sample record from it.

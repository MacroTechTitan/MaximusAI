# HOWTO — MCP Stateless Migration

## 1. Is my server affected?
Run `python examples/find_legacy_surfaces.py path/to/src`. Any hit in live protocol code means work. On an official Tier 1 SDK most transport changes come with the upgrade; your work concentrates on session state, `resultType`, and cache fields.

## 2. Python server on FastMCP
Upgrade to the v2 SDK, rename the import to `from mcp.server.mcpserver import MCPServer`, move `host`/`port`/`stateless_http` from the constructor to `run()`, pass `version=`. Re-run the baseline. Then rewrite any tool that called elicitation mid-call as an MRTR tool.

## 3. TypeScript server
Commit first. From the package root: `npx @modelcontextprotocol/codemod@latest v1-to-v2 .` Then raise zod to the required floor, run Prettier, `npm install`, `npx tsc --noEmit`. Switch the HTTP entry to `createMcpHandler` so modern and legacy clients share one endpoint.

## 4. Prove it works at scale
Two replicas, round-robin, no shared store. Run `examples/smoke_test.sh` against the balancer: `server/discover` must answer with `supportedVersions`, a modern `tools/call` must succeed on either replica, an unsupported version must return the unsupported-version error with a `supported` list.

## 5. Drain the legacy lane
Log negotiated era per request. When legacy traffic is zero for your agreed window, or the deprecation deadline approaches, remove the legacy handler and the handshake paths.

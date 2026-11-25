# maximus-mcp-server-exposure-check (incubator)

Self-audit for teams that run MCP servers: probe as an anonymous client, require and advertise sign-in, check token audience, patch and configure the SDK, close path, SSRF, and shell holes in tool handlers, and keep tool annotations and descriptions honest.

**Triggers:** "MCP server security check", "is my MCP server exposed", "harden MCP server", "MCP OAuth audience", "tool poisoning in my server".

**Files:** `SKILL.md` (workflow), `HOWTO.md` (5 recipes), `references/mcp-exposure-2026-11.md` (survey figures, CVEs, fixed versions), `examples/mcp_exposure_check.py` (anonymous probe, never calls tools), `examples/mock_server.py` (local test target).

**Siblings:** maximus-agent-dependency-vetting, maximus-agent-access-review, maximus-mcp-stateless-migration, maximus-agent-safe-write-tools.

Drafted by the skill scout on 2026-11-25. Unreviewed until promoted.

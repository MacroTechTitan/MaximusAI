# maximus-mcp-stateless-migration (incubator)

Moves an MCP server to the 2026-07-28 stateless protocol without breaking legacy clients: discovery, per-request metadata, handles instead of sessions, MRTR instead of server-initiated requests, cache fields, header and error-code changes, and a two-era regression matrix.

**Triggers:** "MCP stateless", "migrate MCP server", "MCP 2026-07-28", "Mcp-Session-Id removed", "server/discover".

**Files:** `SKILL.md` (workflow), `HOWTO.md` (5 recipes), `references/mcp-2026-07-28-2026-10.md` (versions, codes, sources), `examples/find_legacy_surfaces.py` (runnable scanner, tested), `examples/smoke_test.sh` (illustrative, not run against a live server).

**Siblings:** maximus-agent-design, maximus-eval-and-test, maximus-devops-ship, maximus-agent-access-review.

Drafted by the skill scout on 2026-10-07. Unreviewed until promoted.

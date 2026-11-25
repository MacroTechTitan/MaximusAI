---
name: maximus-mcp-server-exposure-check
description: "Audit an MCP server you operate the way an anonymous client sees it: does it list tools without sign-in, publish RFC 9728 metadata, check token audience, annotate tools honestly, keep model-directed text out of descriptions, and run on a patched SDK. Use for 'MCP server security check', 'is my MCP server exposed', 'harden MCP server'."
metadata: {"openclaw": {"emoji": "🛰️", "pillar": "ai-engineering", "source": "maximus-scout"}}
---

# Maximus — MCP Server Exposure Check

Three independent surveys of the official MCP Registry in late October and November 2026 reached the same result: most remote servers answer an anonymous client. Spellwarden found that 62% of responding hosts listed their tools without sign-in, and that 9,691 of those open lists included a tool that did not declare itself read-only. mcpprobe found that 55.7% of assessable servers answered without any login, and that 15.1% of servers requiring login published no usable RFC 9728 metadata. In the same weeks, the TypeScript SDK fixed a bearer-auth bug that accepted tokens issued for another service; the fix is off until configured.

## Purpose

Give the team that runs an MCP server a repeatable self-audit: what an anonymous client can see, whether sign-in is discoverable and correctly checked, whether tool metadata is honest, and whether the SDK and transport are patched. Figures and versions are in `references/mcp-exposure-2026-11.md`.

## Scope boundary

| Need | Use |
|---|---|
| Auditing an MCP server you publish or host | this skill |
| Vetting third-party packages and servers before an agent installs them | maximus-agent-dependency-vetting (incubator) |
| What credentials your agents hold | maximus-agent-access-review (incubator) |
| Moving a server to the stateless protocol revision | maximus-mcp-stateless-migration (incubator) |
| Designing write tools that pick the right record | maximus-agent-safe-write-tools (incubator) |

## Core workflow

1. **Inventory endpoints.** List every MCP endpoint you run, including registry entries, staging hosts, and anything bound beyond `127.0.0.1`. The registry does not verify that a URL belongs to its publisher, so check what is listed under your namespace.
2. **Probe as an anonymous client.** Send `initialize` and `tools/list` with no credentials (`examples/mcp_exposure_check.py`). Never call tools, and probe only servers you own or are authorized to test.
3. **Decide public or private per server.** If tools are listed without sign-in and the server is not public by design, require OAuth on every request. Listing is not the same as calling, but an open list tells an attacker which tools to try.
4. **Make sign-in discoverable and strict.** Return 401 with a `WWW-Authenticate` pointer to RFC 9728 protected-resource metadata. On the server, validate the token audience; on the client, accept a metadata `resource` only if it matches the configured server URL. Re-check the token on every request, not only at `initialize`.
5. **Patch and configure the SDK.** Upgrade to fixed releases, then turn on the fixes that ship disabled (audience check, input bounds). Build one server and transport per request or session; never share one across clients.
6. **Close the classic holes in tool handlers.** Resolve paths and check containment after resolving; classify outbound addresses numerically, including IPv4-mapped IPv6, and re-check on redirects; never build shell commands from tool input; call the same authorization function the REST routes use; bind HTTP mode to localhost by default and check `Host` and `Origin`.
7. **Make tool metadata honest.** Set `readOnlyHint` and `destructiveHint` on every tool. Keep descriptions to what the tool does: no "call this first", "do not tell the user", or requests to pass along conversation content. Review description changes like code changes.
8. **Split read-private from send-out.** A server that both reads private data and can send data out should separate those tools or require confirmation before sending.
9. **Re-run on every release.** Add the anonymous probe to CI or a scheduled job against staging and production.

## Anti-patterns

- **Assuming the registry vets servers.** It holds metadata only.
- **Upgrading the SDK and stopping.** Some fixes need configuration.
- **401 with no metadata.**
- **Trusting `destructiveHint` from someone else's server.** Annotations are the server's own claims.
- **Tool descriptions that steer the model.**
- **One shared transport for all clients.**

## Output

Per endpoint: anonymous-probe result, public-or-private decision, sign-in metadata status, audience-check status, SDK version and configured fixes, tool annotation and description findings, read-private and send-out combinations, and the CI job that re-runs the probe.

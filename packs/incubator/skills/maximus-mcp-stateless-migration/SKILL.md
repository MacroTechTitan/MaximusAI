---
name: maximus-mcp-stateless-migration
description: "Migrate an MCP server to the 2026-07-28 stateless spec: server/discover, per-request _meta, no sessions, explicit state handles, MRTR instead of elicitation, cache fields, new headers and error codes, dual-era rollout and two-era regression tests. Use for 'MCP stateless', 'migrate MCP server', 'MCP 2026-07-28', 'Mcp-Session-Id removed'."
metadata: {"openclaw": {"emoji": "🔌", "pillar": "ai-engineering", "source": "maximus-scout"}}
---

# Maximus — MCP Stateless Migration

The 2026-07-28 MCP revision removed the handshake and the session. A server that still depends on either does not degrade gracefully for modern clients; it fails. This skill moves a server across without breaking the clients that have not moved yet.

## Purpose

Take an existing MCP server (official SDK or hand-rolled) to the 2026-07-28 protocol, keep legacy clients working during the transition, and prove both eras with a regression matrix before the legacy lane is drained. Versions, SDK package names and error codes are in `references/mcp-2026-07-28-2026-10.md`; check them there, not from memory.

## Scope boundary

| Need | Use |
|---|---|
| Migrate an existing MCP server to the stateless spec | this skill |
| Design an agent's tool set, loop, and memory | maximus-agent-design |
| General test strategy and eval tiers | maximus-eval-and-test |
| CI/CD, canary, rollback for the deployed server | maximus-devops-ship |
| Scope and revoke what the agent's credentials can reach | maximus-agent-access-review (incubator) |

## Core workflow

1. **Freeze a legacy baseline.** Before any dependency moves, capture `tools/list`, one passing and one failing golden `tools/call` per tool, and the error envelopes, with the inspector pinned to the legacy era. A v2 SDK can change the legacy wire shape too, so this is the only record of "before".
2. **Find removed surfaces.** Scan live protocol code for `Mcp-Session-Id`, `initialize`/`notifications/initialized`, `logging/setLevel`, `ping`, `elicitation/create`, `sampling/createMessage`, `roots/list`, `Last-Event-ID`. `examples/find_legacy_surfaces.py` does this.
3. **Pick a lane strategy.** Default to dual-era: modern requests (per-request `_meta`) are served statelessly, an `initialize` selects legacy semantics. Go modern-only only when you control every client.
4. **Upgrade the SDK.** Python: FastMCP becomes `MCPServer` under `mcp.server.mcpserver`, transport options move from the constructor to `run()`. TypeScript: run the official v1-to-v2 codemod from the package root, then fix the zod floor and type-check. Cloudflare Agents: move to `createMcpHandler`, keep `createLegacyMcpHandler` only as a temporary lane.
5. **Replace session state with handles.** Anything keyed on the transport session becomes a server-minted id returned by one tool and passed as an ordinary argument to the next. Treat handles as untrusted input: validate ownership on every call.
6. **Convert server-initiated requests to MRTR.** A tool that needed elicitation or sampling mid-call returns `resultType: "input_required"` with its input requests; the client retries the original call with the answers. Every result now carries `resultType`.
7. **Add cache fields and stable order.** List and read results carry `ttlMs` and `cacheScope`. Return `tools/list` in deterministic order so clients and prompt caches stay stable.
8. **Enforce the new HTTP surface.** Require `MCP-Protocol-Version`, `Mcp-Method`, and `Mcp-Name` where the spec requires it, and check that headers match the body. Renumber error codes to the reserved range.
9. **Run the two-era matrix.** Every baseline scenario, once per era, recording which era each connection negotiated. A green inspector on default settings proves only the legacy era.
10. **Scale-out check, then drain.** Put two instances behind a plain round-robin balancer with no shared session store and rerun the modern-era matrix. Track legacy-lane traffic, and remove it inside the twelve-month deprecation window.

## Anti-patterns

- **Calling it done on a green inspector.** The inspector defaults to the legacy era; a broken modern path still shows green.
- **Hiding state in a new side channel** (cookie, IP affinity, sticky sessions). It recreates the session the spec removed and breaks round-robin scaling.
- **Unvalidated handles.** A handle is a capability; a guessable or unchecked id lets one caller act on another's state.
- **Skipping type-check after the TypeScript codemod.** A zod 3 schema can start fine under a non-type-checking runner and fail on the first `tools/list`.
- **Removing the legacy lane on day one.** Legacy clients have no fall-forward to a modern-only server.
- **Adopting deprecated features in new code** (Roots, Sampling, Logging, HTTP+SSE). They work for now and are on a removal clock.

## Output

A migration PR plus a short report: lane strategy chosen, removed surfaces found and fixed (file:line), handles introduced, tools converted to MRTR, the two-era matrix with negotiated era per row, the round-robin result, and the legacy-lane drain date.

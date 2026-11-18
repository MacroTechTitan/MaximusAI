# Agent safe-write tools — facts and sources (pulled 2026-11-18)

| Fact | Source |
|---|---|
| "What LLM Agents See and What Users Say" (Zhao, Zhang, Yang, Wei, Hu; arXiv 2611.17639, Nov 13, 2026): an agent may act only if each claim behind the act is seen to hold, answered by the user, or disclosed while the act can be undone; when lookups cannot tell one record from two, an agent acts without asking as often with two records as with one | https://arxiv.org/abs/2611.17639 |
| Under a role-only prompt, a count of a second record leaves most of 36 earlier agents acting on the one they see; listing both stops most; the newest Claude and GPT models always open a counted second record, then never act | same |
| Same-name, same-zip customer added to a retail benchmark: a lookup returning that customer first led to wrong-account writes in about a quarter of conversations; a lookup checking a street the user knows kept completion near the one-customer level; safe writes need lookups that list or check competing records, and evaluations that vary what tools show | same |
| Anthropic, "Writing effective tools for agents" (Sep 11, 2025): return high-signal, meaningful fields; prefer targeted search tools; name parameters unambiguously (`user_id` not `user`); use strict data models; MCP tool annotations help disclose which tools make destructive changes | https://www.anthropic.com/research/writing-tools-for-agents |
| MCP schema (2025-06-18): `ToolAnnotations` fields `readOnlyHint` (default false), `destructiveHint` (default true), `idempotentHint` (default false), `openWorldHint` (default true); all are hints, and clients should never make tool-use decisions based on annotations from untrusted servers | https://modelcontextprotocol.io/specification/2025-06-18/schema |
| Scout run 2026-11-18: `examples/safe_write_guard.py` self-test passed (asks on duplicates, proceeds on a user-supplied street, stops on no match, refuses when the count exceeds the list) | local run |

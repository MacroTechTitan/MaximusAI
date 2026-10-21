---
name: maximus-agent-web-identity
description: "Make browsing and API agents identifiable to the sites they visit, and let sites set policy for them: Web Bot Auth request signing, key directory, honest user agent, sanctioned channels over credential-driven automation, verification with IP fallback, and no block evasion. Use for 'web bot auth', 'agent blocked by site', 'verify AI agent traffic'."
metadata: {"openclaw": {"emoji": "🪪", "pillar": "ai-engineering", "source": "maximus-scout"}}
---

# Maximus — Agent Web Identity

Sites are turning agents away: banks block agents that log in with a customer's password, retailers challenge shopping agents, and anti-bot systems catch agents that look like scrapers. The durable answer for an agent builder is to be identifiable and to use the channel the site offers. The durable answer for a site is to verify who operates the agent and then decide, separately, what it may do.

## Purpose

Two sides of one protocol. Agent operators: sign requests with Web Bot Auth so sites can recognise the operator, and route sensitive actions through sanctioned APIs or MCP servers. Site owners: verify signed agents, set per-operator policy, and keep authorization separate from identity. Draft status, dates, and vendor behaviour are in `references/web-bot-auth-2026-10.md`.

## Scope boundary

| Need | Use |
|---|---|
| Agent request signing, key directory, agent-traffic verification and policy | this skill |
| robots.txt and crawler access for LLM training and search bots | maximus-geo-optimization |
| Credentials and grants the agent itself holds | maximus-agent-access-review (incubator) |
| Containing what a coding agent can reach | maximus-coding-agent-sandbox (incubator) |
| Prompt-injection defense for content the agent reads | maximus-ai-safety-governance |

## Core workflow

### If you operate an agent

1. **Use the sanctioned channel first.** If the site offers an API, an MCP server, or a partner program, use it. Do not have an agent log in with a customer's password where the site forbids it; banks and brokers are blocking exactly that.
2. **Generate a signing key and publish a directory.** An Ed25519 key in a JWKS directory served over HTTPS at `/.well-known/http-message-signatures-directory` on the host your `Signature-Agent` names.
3. **Sign every outbound request.** Add `Signature`, `Signature-Input`, and `Signature-Agent`. Cover `@authority` (or `@target-uri`) and the `Signature-Agent` member; include `created`, `expires`, `keyid` (JWK SHA-256 thumbprint), and `tag="web-bot-auth"`. Keep expiry at 24 hours or less.
4. **Say who you are in plain text too.** A descriptive user agent and a contact URL. Signed traffic rolls out gradually; many sites still look at the user agent and IP.
5. **Rotate and revoke by directory.** Publish the new key next to the old one, switch, then remove the old key. There is no revocation in the draft; removal takes effect when verifiers refresh their cache.
6. **When blocked, stop.** Report the block to the user and offer the sanctioned route. Do not rotate IPs, spoof a browser, or solve CAPTCHAs to get around a deliberate block.

### If you run a site

7. **Verify, then decide.** Fetch the directory named by `Signature-Agent` (HTTPS, 200 only, no redirects), look keys up by the (directory URL, keyid) pair, check `tag`, check the time window, verify the signature. Cache keys per `Cache-Control` and drop keys that disappear.
8. **Keep the fallback.** Not every request from a given agent is signed yet. Keep IP, reverse DNS, and user-agent checks.
9. **Write policy per operator and per path.** Allow, rate-limit, or block by verified operator; treat invalid and expired signatures as hostile and unknown keys as unverified.
10. **Never treat identity as authorization.** A valid signature names the operator, not the user or their permission. Account actions still need the user's delegated credential, such as OAuth, with scopes you set.

## Anti-patterns

- **Signing requests and then evading blocks anyway.** Identity buys trust only if the agent respects the answer.
- **Credential-stuffing on the user's behalf.** Storing a user's banking or brokerage password in an agent that drives the login page.
- **Looking keys up by keyid alone.** Keys must be scoped to the directory URL that published them.
- **Treating "verified" as "allowed to move money".** Read-only research and transactions need different gates.
- **Long-lived signatures.** Keep expiry short; replay to the same host inside the window needs a nonce or rate limit.
- **Dropping IP and user-agent checks** because some traffic is signed.

## Output

Agent side: the key directory, the signing middleware or browser setting enabled, the user-agent string, the list of sites reached through sanctioned channels, and the block-handling rule. Site side: the verification point (edge, WAF, or origin), the per-operator policy table, the fallback rules, and how account actions are authorized separately.

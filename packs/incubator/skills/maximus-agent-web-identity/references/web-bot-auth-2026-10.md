# Web Bot Auth and agent blocking — facts and sources (pulled 2026-10-21)

| Fact | Source |
|---|---|
| Draft `draft-ietf-webbotauth-httpsig-protocol-00` (Meunier, Major), updated 1 September 2026; defines `Signature-Agent`, a JWKS key directory, and the well-known URI `/.well-known/http-message-signatures-directory` (media type `application/http-message-signatures-directory+json`) | https://datatracker.ietf.org/doc/draft-ietf-webbotauth-httpsig-protocol/ |
| Must cover `@authority` or `@target-uri` and the `Signature-Agent` member for that label; `created`, `expires`, `keyid` (JWK SHA-256 thumbprint), `tag="web-bot-auth"` required; expiry SHOULD be no more than 24 hours; no extra nonce requirement | same |
| Verifiers: discovery must return 200, no automatic redirects, directory over HTTPS; key lookup keyed on (URL, key) pair; never attribute a signature to an uncovered `Signature-Agent` member | same |
| Built on RFC 9421 (HTTP Message Signatures, Feb 2024); identifies the operator, not the user; no authorization or delegation; no revocation, remove the key from the directory; account actions still need delegated credentials such as OAuth (Oct 19, 2026) | https://workos.com/blog/web-bot-auth-identify-ai-agents |
| Google: experimental; a subset of `Google-Agent` requests signed as `https://agent.bot.goog`; keep IP, reverse DNS and user-agent checks; cache keys per `Cache-Control`; signature expiry and key cache are separate (updated 2026-10-13) | https://developers.google.com/crawling/docs/crawlers-fetchers/web-bot-auth |
| AWS WAF Bot Control: ed25519; labels `web_bot_auth:verified` (allow), `invalid` (block or rate-limit), `expired` (block and alert), `unknown_bot` (monitor or block); verified AI traffic allowed by default (Jul 14, 2026) | https://aws.amazon.com/blogs/security/authenticate-legitimate-ai-agent-traffic-with-aws-waf-bot-control/ |
| AgentCore Browser signs each request when Web Bot Auth is enabled; domain owners may still block, monitor or rate-limit signed traffic | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-web-bot-auth.html |
| Sites blocking agents: Delta, JPMorgan Chase, Charles Schwab, Amazon challenges, Yelp paid licensing only; agents also trip anti-bot systems (Oct 17, 2026) | https://www.theverge.com/ai-artificial-intelligence/1013195/ai-agents-blocked-web |
| Schwab blocks agents using client logins or browser automation; plans MCP servers for read-only balances and research, no money movement (Oct 16, 2026) | https://thenextweb.com/news/schwab-blocks-ai-agents-meta-muse |
| Scout run 2026-10-21: `examples/wba_demo.py` verified its own signature and rejected cross-host replay, removed key, and expiry; not tested against vendor verifiers or draft test vectors | local run |

Volatile: the draft is revision 00 and expires if not advanced; vendor labels and defaults change. Recheck before relying on them.

# HOWTO — Agent Web Identity

## 1. See the protocol end to end
`pip install cryptography && python examples/wba_demo.py`. It creates a key, a directory, a signed request, and shows verified, replayed-to-another-host, key-removed, and expired outcomes.

## 2. Agent on a managed browser
If the browser service offers Web Bot Auth (for example Amazon Bedrock AgentCore Browser), turn it on. The service signs with its own operator identity; sites still decide policy.

## 3. Your own agent or fetcher
Generate an Ed25519 key, serve the JWKS directory at `https://<your-agent-host>/.well-known/http-message-signatures-directory`, and add signing middleware to the HTTP client. Use the draft's test vectors and a vendor verifier before production; the demo is a self-consistency check only.

## 4. Site behind a WAF or CDN
Turn on the vendor's Web Bot Auth verification (AWS WAF Bot Control labels: verified, invalid, expired, unknown_bot). Write rules: allow verified operators you accept, rate-limit unknown, block invalid and expired, and keep path rules for account and checkout pages.

## 5. Site offering an agent channel
Offer read-only access through an API or MCP server with OAuth and narrow scopes, and say in your terms which actions agents may take. Point blocked agents to it in the block response.

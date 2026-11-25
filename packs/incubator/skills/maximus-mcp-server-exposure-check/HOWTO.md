# HOWTO — MCP Server Exposure Check

## 1. Run the anonymous probe
`python examples/mcp_exposure_check.py https://your-host/mcp`. Exit 0 means no findings, 1 means findings, 2 means unreachable. Add `--public-ok` for servers that are public by design (for example, public docs search) so an open list is not flagged.

## 2. Fix a refused-but-undiscoverable server
Serve `/.well-known/oauth-protected-resource` with `resource` set to the server URL and `authorization_servers` listing your issuer, and return `WWW-Authenticate: Bearer resource_metadata="<that URL>"` on 401.

## 3. Turn on the TypeScript SDK fixes
Upgrade `@modelcontextprotocol/sdk` to 1.32.0 (1.x) or the 2.3.0 packages, then configure the bearer-auth audience check and the input element bound. Expect `ALREADY_CONNECTED` errors on 2.3.0 if a server or transport is shared; build one per request or session.

## 4. Review tool descriptions
Read every tool description as if it were a prompt. Remove anything that tells the model what to do first, what to hide, or what to pass along. Gate future changes behind code review.

## 5. Schedule it
Run the probe in CI against staging and weekly against production. Fail the job on exit 1 unless the finding is recorded as accepted.

## Testing note
`examples/mock_server.py` starts a local mock in `open`, `auth`, or `clean` mode. On 2026-11-25 the probe returned exit 1 with four findings on `open`, exit 0 on `auth`, exit 0 on `clean --public-ok`, and exit 2 on a closed port.

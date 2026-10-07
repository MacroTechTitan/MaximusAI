#!/usr/bin/env bash
# ILLUSTRATIVE: not run against a live server by the scout. Request shapes follow
# the 2026-07-28 spec examples; adjust the tool name and arguments to your server.
set -euo pipefail
URL="${MCP_URL:?set MCP_URL, e.g. http://lb.internal/mcp}"
V=2026-07-28
H=(-H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -H "MCP-Protocol-Version: $V")

echo "1. discovery (expect supportedVersions)"
curl -s "$URL" "${H[@]}" -H 'Mcp-Method: server/discover' \
  -d '{"jsonrpc":"2.0","id":1,"method":"server/discover","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"'$V'","io.modelcontextprotocol/clientCapabilities":{}}}}'

echo; echo "2. tool call, repeated so round-robin hits each replica (expect resultType complete)"
for i in 1 2 3 4; do
  curl -s "$URL" "${H[@]}" -H 'Mcp-Method: tools/call' -H 'Mcp-Name: echo' \
    -d '{"jsonrpc":"2.0","id":'$((i+1))',"method":"tools/call","params":{"name":"echo","arguments":{"text":"hi"},"_meta":{"io.modelcontextprotocol/protocolVersion":"'$V'","io.modelcontextprotocol/clientCapabilities":{}}}}'
  echo
done

echo "3. unsupported version (expect error -32022 with data.supported)"
curl -s "$URL" -H 'Content-Type: application/json' -H 'MCP-Protocol-Version: 1900-01-01' -H 'Mcp-Method: server/discover' \
  -d '{"jsonrpc":"2.0","id":9,"method":"server/discover","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"1900-01-01","io.modelcontextprotocol/clientCapabilities":{}}}}'
echo

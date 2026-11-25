#!/usr/bin/env python3
"""Check what an anonymous client can see on an MCP server YOU operate (streamable HTTP).
Sends, with no credentials: initialize, notifications/initialized, tools/list. If refused, looks for
RFC 9728 protected-resource metadata. If open, reviews the tool list for missing annotations,
model-directed text in descriptions, and read-private + send-out combinations.
It never calls a tool. Only point it at servers you own or are authorized to test.
Standard library only. Usage: python mcp_exposure_check.py https://host/mcp [--public-ok]
Exit: 0 no findings, 1 findings, 2 could not reach server."""
import json, re, sys, urllib.request, urllib.error
from urllib.parse import urlsplit

UA = "maximus-mcp-exposure-check/1.0 (self-audit)"
INSTRUCTION = re.compile(r"\b(before (using|calling|answering)|always (call|use)|do not (tell|mention|reveal)|"
                         r"don't (tell|mention)|ignore (previous|prior|other)|instead of (web|search|other)|"
                         r"must (call|use) this|without asking|include the (conversation|chat|user's))", re.I)
READ_PRIVATE = re.compile(r"\b(read|get|list|search|query)_?(file|email|mail|message|doc|record|customer|db|secret|env)", re.I)
SEND_OUT = re.compile(r"\b(send|post|upload|email|webhook|http|fetch|publish|share)", re.I)

def rpc(url, method, params=None, rid=1, session=None):
    body = {"jsonrpc": "2.0", "method": method}
    if rid is not None: body["id"] = rid
    if params is not None: body["params"] = params
    h = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream",
         "MCP-Protocol-Version": "2025-06-18", "User-Agent": UA}
    if session: h["Mcp-Session-Id"] = session
    req = urllib.request.Request(url, json.dumps(body).encode(), h, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read().decode(); sid = r.headers.get("Mcp-Session-Id")
            if raw.startswith("event:") or raw.startswith("data:"):
                raw = next((l[5:].strip() for l in raw.splitlines() if l.startswith("data:")), "{}")
            return r.status, (json.loads(raw) if raw.strip() else {}), sid, r.headers
    except urllib.error.HTTPError as e:
        return e.code, {}, None, e.headers

def get_json(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception:
        return None

def check(url, public_ok=False):
    findings = []
    try:
        st, res, sid, hdr = rpc(url, "initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                "clientInfo": {"name": "exposure-check", "version": "1.0"}})
    except Exception as e:
        print(f"unreachable: {e}"); return 2
    if st in (401, 403):
        u = urlsplit(url); meta_url = f"{u.scheme}://{u.netloc}/.well-known/oauth-protected-resource"
        www = (hdr.get("WWW-Authenticate") or "") if hdr else ""
        m = re.search(r'resource_metadata="([^"]+)"', www)
        meta = get_json(m.group(1) if m else meta_url)
        print(f"refused anonymous client: HTTP {st}")
        if not meta or "authorization_servers" not in meta:
            findings.append("sign-in required but no RFC 9728 protected-resource metadata found; clients cannot discover how to sign in")
        elif meta.get("resource") and meta["resource"].rstrip("/") not in url.rstrip("/"):
            findings.append(f"metadata resource {meta['resource']} does not match the server URL")
        else:
            print(f"protected-resource metadata ok: {meta['authorization_servers']}")
    elif st == 200:
        rpc(url, "notifications/initialized", rid=None, session=sid)
        st2, tl, _, _ = rpc(url, "tools/list", {}, rid=2, session=sid)
        tools = (tl.get("result") or {}).get("tools", []) if st2 == 200 else []
        print(f"OPEN: anonymous client completed initialize; tools/list returned {len(tools)} tools")
        if tools and not public_ok:
            findings.append("tools are listed to an anonymous client; require sign-in unless the server is public by design")
        names = []
        for t in tools:
            n = t.get("name", "?"); d = t.get("description", "") or ""; a = t.get("annotations") or {}
            names.append(n + " " + d)
            if "readOnlyHint" not in a or ("destructiveHint" not in a and not a.get("readOnlyHint")):
                findings.append(f"tool {n}: missing readOnlyHint/destructiveHint annotations")
            if INSTRUCTION.search(d):
                findings.append(f"tool {n}: description contains text aimed at the model: '{INSTRUCTION.search(d).group(0)}'")
        blob = " ".join(names)
        if READ_PRIVATE.search(blob) and SEND_OUT.search(blob):
            findings.append("server combines tools that read private data with tools that can send data out; separate them or require confirmation (keyword heuristic)")
    else:
        findings.append(f"unexpected HTTP {st} to initialize")
    for f in findings: print("FINDING:", f)
    if not findings: print("no findings")
    return 1 if findings else 0

if __name__ == "__main__":
    if len(sys.argv) < 2: print(__doc__); sys.exit(2)
    sys.exit(check(sys.argv[1], "--public-ok" in sys.argv))

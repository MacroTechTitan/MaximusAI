#!/usr/bin/env python3
"""Web Bot Auth round trip: make an Ed25519 key, publish a JWKS directory, sign a
request (RFC 9421 style, tag="web-bot-auth"), then verify it as a site would.
Self-consistency demo only: it was run by the scout, but it has NOT been checked
against Cloudflare, AWS WAF, or the draft's test vectors. Requires: cryptography.
Usage: python wba_demo.py"""
import base64, hashlib, json, time
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

b64u = lambda b: base64.urlsafe_b64encode(b).rstrip(b"=").decode()
DIRECTORY_URL = "https://agent.example.com"   # what Signature-Agent points at
LABEL = "sig"

def make_key():
    sk = Ed25519PrivateKey.generate()
    raw = sk.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    jwk = {"kty": "OKP", "crv": "Ed25519", "x": b64u(raw)}
    # RFC 7638 thumbprint: required members, sorted keys, no whitespace
    thumb = b64u(hashlib.sha256(json.dumps({k: jwk[k] for k in ("crv", "kty", "x")}, separators=(",", ":"), sort_keys=True).encode()).digest())
    return sk, dict(jwk, kid=thumb)

def params(keyid, created, expires):
    return f'("@authority" "signature-agent";key="{LABEL}");created={created};expires={expires};keyid="{keyid}";tag="web-bot-auth"'

def base(authority, agent_value, sig_params):
    return (f'"@authority": {authority}\n'
            f'"signature-agent";key="{LABEL}": {agent_value}\n'
            f'"@signature-params": {sig_params}')

def sign(sk, kid, authority, ttl=3600):
    now = int(time.time())
    p = params(kid, now, now + ttl)                       # draft: expiry SHOULD be <= 24h
    agent_value = f'"{DIRECTORY_URL}"'
    sig = sk.sign(base(authority, agent_value, p).encode())
    return {"Signature-Agent": f'{LABEL}={agent_value}',
            "Signature-Input": f"{LABEL}={p}",
            "Signature": f"{LABEL}=:{base64.b64encode(sig).decode()}:"}

def verify(headers, authority, directories, now=None):
    """directories: {directory_url: jwks}. Keys are looked up by (URL, keyid), never keyid alone."""
    now = now or int(time.time())
    label, agent_value = headers["Signature-Agent"].split("=", 1)
    url = agent_value.strip('"')
    p = headers["Signature-Input"].split("=", 1)[1]
    if 'tag="web-bot-auth"' not in p or '"signature-agent";key="%s"' % label not in p:
        return "invalid: wrong tag or Signature-Agent not covered"
    fields = dict(kv.split("=", 1) for kv in p.split(";")[1:])
    if not (int(fields["created"]) <= now < int(fields["expires"])):
        return "expired"
    keyid = fields["keyid"].strip('"')
    jwk = next((k for k in directories.get(url, {}).get("keys", []) if k["kid"] == keyid), None)
    if jwk is None:
        return "unknown_bot"
    pk = Ed25519PublicKey.from_public_bytes(base64.urlsafe_b64decode(jwk["x"] + "=="))
    sig = base64.b64decode(headers["Signature"].split("=", 1)[1].strip(":"))
    try:
        pk.verify(sig, base(authority, agent_value, p).encode())
        return f"verified: operator {url}"
    except InvalidSignature:
        return "invalid"

if __name__ == "__main__":
    sk, jwk = make_key()
    directory = {"keys": [jwk]}   # serve at DIRECTORY_URL/.well-known/http-message-signatures-directory
    dirs = {DIRECTORY_URL: directory}
    h = sign(sk, jwk["kid"], "shop.example.org")
    print(json.dumps(h, indent=1))
    print("same host      ->", verify(h, "shop.example.org", dirs))
    print("replayed host  ->", verify(h, "bank.example.net", dirs))
    print("key removed    ->", verify(h, "shop.example.org", {DIRECTORY_URL: {"keys": []}}))
    print("after expiry   ->", verify(h, "shop.example.org", dirs, now=int(time.time()) + 7200))
    print("NOTE: verified identifies the operator only; it does not authorize any action.")

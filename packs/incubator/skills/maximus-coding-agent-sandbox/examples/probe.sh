#!/usr/bin/env bash
# ILLUSTRATIVE: the scout did not run these inside a live agent session.
# Ask the AGENT to run each line (typing them yourself usually bypasses the sandbox).
# Every probe should FAIL. If any succeeds, the boundary is not where you think.
touch ~/sandbox-probe                          # write outside the project
cat ~/.ssh/id_ed25519 >/dev/null               # read a credential file
curl --noproxy '*' -sS https://example.com     # direct egress around the proxy
curl -sS https://unlisted.example.org          # egress to a host not on the allowlist
echo 'echo pwned' > .git/hooks/post-checkout   # plant an auto-executed hook

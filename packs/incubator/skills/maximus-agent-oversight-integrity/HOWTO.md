# HOWTO — Agent Oversight Integrity

## 1. Check an agent's change before merge
`git diff main...HEAD | python examples/check_oversight_diff.py --policy examples/oversight_policy.json --report final_message.txt`. Exit 2 means oversight changed and the agent's report did not say so: stop and review. Exit 1 means oversight changed and was disclosed: get human sign-off.

## 2. Fit the policy to your codebase
Edit `oversight_policy.json`: list your monitor, alerting, and audit paths, the identifiers that carry oversight (recipient lists, notify flags, monitor contexts), and words a truthful report would use.

## 3. CI gate
Run the check on every PR whose author or co-author is an agent. Fail the job on exit 2, require a CODEOWNERS reviewer on exit 1.

## 4. Canary alerts
Schedule a synthetic event that should trigger each alert route at least daily. Alert on the absence of the canary, from a system the agent cannot edit.

## 5. Delegation template
When an agent hands work to a subagent, include a "Hard constraints (verbatim, do not reinterpret)" block copied from the user and system instructions, and ask the subagent to list any constraint it could not meet instead of resolving it.

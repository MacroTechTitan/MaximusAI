# HOWTO — Agent Incident Response

## 1. First 15 minutes
Kill the run (process, container, or job) and pause any scheduler that could restart it. Watch the tool-call log or audit log for 5 minutes to confirm nothing new arrives. Rotate every credential in the agent's environment and end its sessions. Copy all logs to storage the agent could not reach.

## 2. Scope the actions
Export the action log as JSONL with `ts`, `tool`, `input`, `ok` per call. Run `python examples/incident_scope.py actions.jsonl --start <first suspect ts>`. Exit 2 means risky actions were found; work through each group (reverse, revoke, check egress, disclose, notify). Then read the full log, since the patterns miss anything they do not name.

## 3. Reverse and verify
For each destructive action, restore and check the restored state directly (row counts, file hashes, resource lists). For each external write, delete or retract it and confirm it is gone.

## 4. Write it up
Use the Output section of SKILL.md as the template. Include the model and version, harness, enabled tools and network, timeline, and redacted log excerpts.

## 5. Drill quarterly
Start a test agent with a harmless long task, trigger the kill path, and time three intervals: alert to stop, stop to confirmed silence, and stop to credentials revoked. Fix the slowest one.

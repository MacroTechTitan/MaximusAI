# HOWTO — Agent Context Files

## 1. Triage an existing AGENTS.md or CLAUDE.md
List every rule. Mark it guideline (has exceptions) or invariant (none). For each invariant, name the enforcement: deny rule, command hook, managed setting, CI check, or branch protection. Delete rules that are vague, duplicated, or obvious from the code.

## 2. Rewrite guidelines for compliance
Turn conditionals into direct imperatives: "If you add a Python function, add X" becomes "Add X below the def line of every Python function you add or modify." Add a one-clause reason if your model does better with it (one model in the study did). Keep each rule to one sentence.

## 3. Measure compliance
Write checkable rules into `examples/rules.json` (a trigger and a required next line, or a forbidden pattern). Save one `git diff` per agent session as `sessions/<id>.diff`, at least 20 sessions per harness and model. Run `python examples/rule_compliance.py --rules rules.json --sessions sessions/ --threshold 0.95`. Exit 2 means at least one rule is below threshold.

## 4. Promote a rule to a hook
For Claude Code, register a `command` hook on `PreToolUse` (see `examples/deny_env_read.py`, which exits 2 to block). Prefer a plain deny rule when one exists for the tool, since deny rules hold in every permission mode. For Codex and other agents, use their equivalent hooks or move the check into CI. Leave a one-line note in the context file explaining the policy.

## 5. Re-run after upgrades
After a model, harness, or context-file change, rerun recipe 3 on fresh sessions and compare with the previous dated table.

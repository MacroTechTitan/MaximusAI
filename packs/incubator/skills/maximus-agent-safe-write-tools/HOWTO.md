# HOWTO — Agent Safe-Write Tools

## 1. Find risky writes
Search your tool definitions for verbs like cancel, delete, refund, update, send, transfer. For each, write down which lookup supplies the target ID.

## 2. Fix a lookup
Change the response to `{match_count, matches:[...]}` with every match and a few user-recognizable fields. If you must paginate, include the total and a next-page token, and say in the response that more matches exist.

## 3. Add the guard
Wrap the write so it runs only when exactly one record matches facts the user stated. `examples/safe_write_guard.py` shows the pattern: it asks on duplicates, proceeds on a user-supplied street, stops on no match, and refuses when the count exceeds the list.

## 4. Annotate
On MCP servers you own, set `readOnlyHint` and `destructiveHint` accurately. In clients, require confirmation for destructive tools from servers you do not control regardless of their annotations.

## 5. Build the test matrix
Seed a test dataset with a same-name, same-postcode duplicate. Run each write scenario under: unique record, duplicate listed, duplicate counted only, duplicate returned first, user claim that a record contradicts. Track wrong-record writes (target: zero) and completion rate on the unique case.

#!/usr/bin/env python3
"""Illustrative pattern, tested only against the in-file self-test: a lookup that lists every
competing record, and a guard that refuses a consequential write unless exactly one record
matches facts the user supplied (not facts the agent inferred). Standard library only.
Run: python safe_write_guard.py   (self-test; exit 0 on success)"""

def lookup(records, **query):
    """Return ALL matches with the fields a user could use to tell them apart. Never just a count,
    never only the first match."""
    hits = [r for r in records if all(r.get(k) == v for k, v in query.items())]
    return {"match_count": len(hits),
            "matches": [{k: r[k] for k in ("id", "name", "zip", "street", "last_order")} for r in hits]}

def resolve_for_write(result, user_facts):
    """Decide whether a write may proceed. user_facts must come from the user's own words.
    Returns ("proceed", id) | ("ask", question) | ("stop", reason)."""
    m = result["matches"]
    if result.get("match_count", len(m)) != len(m):
        return "ask", "the lookup reported more matches than it returned; list them all before writing"
    if not m:
        return "stop", "no record matches; tell the user what was searched"
    cands = [r for r in m if all(str(r.get(k, "")).lower() == str(v).lower() for k, v in user_facts.items())]
    if len(cands) == 1 and (len(m) == 1 or user_facts):
        return "proceed", cands[0]["id"]
    if not cands:
        return "ask", "none of the matching records fit what you told me; can you confirm the street address?"
    return "ask", f"{len(cands)} records match; which street address is on the account?"

def write_guarded(result, user_facts, act):
    decision, value = resolve_for_write(result, user_facts)
    return act(value) if decision == "proceed" else (decision, value)

def _selftest():
    db = [{"id": "C1", "name": "Ana Ruiz", "zip": "37902", "street": "12 Oak St", "last_order": "O-77"},
          {"id": "C2", "name": "Ana Ruiz", "zip": "37902", "street": "9 Elm Ave", "last_order": "O-81"},
          {"id": "C3", "name": "Bo Chen", "zip": "37919", "street": "4 Pine Rd", "last_order": "O-90"}]
    cancel = lambda cid: ("cancelled", cid)
    # Naive tool: first match only -> silently writes to whichever record sorts first.
    naive = lookup(db, name="Ana Ruiz", zip="37902")["matches"][0]["id"]
    assert naive == "C1"
    # Guarded: same name and zip, no disambiguating fact -> must ask.
    r = lookup(db, name="Ana Ruiz", zip="37902")
    assert r["match_count"] == 2 and write_guarded(r, {}, cancel)[0] == "ask"
    # User states the street -> exactly one record -> proceeds on the right one.
    assert write_guarded(r, {"street": "9 Elm Ave"}, cancel) == ("cancelled", "C2")
    # User states a street that fits neither -> ask, never guess.
    assert write_guarded(r, {"street": "1 Main St"}, cancel)[0] == "ask"
    # Single unambiguous record -> proceeds.
    assert write_guarded(lookup(db, name="Bo Chen"), {}, cancel) == ("cancelled", "C3")
    # No record -> stop.
    assert write_guarded(lookup(db, name="Zed"), {}, cancel)[0] == "stop"
    # Eval variation: hide the second record (count only) and confirm the guard cannot be fooled
    # by a response that drops matches but keeps the count (a count-only lookup).
    hidden = {"match_count": 2, "matches": r["matches"][:1]}
    assert resolve_for_write(hidden, {})[0] == "ask"
    print("self-test passed: asks on duplicates, proceeds on a user-supplied key, stops on no match,"
          " refuses when a lookup counts more matches than it lists")

if __name__ == "__main__":
    _selftest()

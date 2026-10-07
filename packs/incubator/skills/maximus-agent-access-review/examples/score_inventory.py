#!/usr/bin/env python3
"""Rank agent identities by blast radius. Heuristic weights, not a standard.
Usage: python score_inventory.py agent_inventory.csv"""
import csv, sys

def yes(v): return str(v).strip().lower() in ("yes", "y", "true", "1")

def score(r):
    s, flags = 0, []
    if yes(r["shell"]): s += 3
    if yes(r["data_read"]): s += 2
    if yes(r["net_egress"]): s += 2
    if yes(r["prod_write"]): s += 4; flags.append("prod write")
    if yes(r["data_read"]) and yes(r["net_egress"]):
        s += 3; flags.append("exfiltration path (data read + egress)")
    if yes(r["shell"]) and yes(r["data_read"]) and yes(r["net_egress"]):
        s += 2; flags.append("full set (shell + data + egress)")
    if yes(r["inherits_user"]): s += 3; flags.append("inherits user privilege")
    if not r["expires_days"].strip(): s += 3; flags.append("no expiry")
    elif int(r["expires_days"]) > 30: s += 1
    if not r["owner"].strip(): s += 4; flags.append("no owner")
    if r["environment"].strip().lower() in ("prod", "ci"): s += 1
    return s, flags

if __name__ == "__main__":
    rows = list(csv.DictReader(open(sys.argv[1], newline="")))
    for r in sorted(rows, key=lambda r: -score(r)[0]):
        s, f = score(r)
        print(f"{s:>3}  {r['identity']:<26} {'; '.join(f) or 'ok'}")

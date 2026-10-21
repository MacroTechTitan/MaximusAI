#!/usr/bin/env python3
"""Vet a package name before an agent installs it.
Usage: python vet_package.py {pypi|npm} NAME [--min-age-days 30]
Exit codes: 0 allow, 1 hold for human review, 2 block (does not exist / lookup failed).
Heuristic only: existence and age do not prove a package is benign. Standard library only."""
import argparse, json, sys, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone

def fetch(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "maximus-vet/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise

def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def pypi(name):
    d = fetch(f"https://pypi.org/pypi/{urllib.parse.quote(name)}/json")
    if d is None:
        return None
    times = [ts(f["upload_time_iso_8601"]) for files in d.get("releases", {}).values() for f in files if f.get("upload_time_iso_8601")]
    info = d.get("info", {})
    urls = info.get("project_urls") or {}
    return {"first": min(times) if times else None, "latest": max(times) if times else None,
            "version": info.get("version"), "maintainers": [x for x in (info.get("author"), info.get("maintainer")) if x],
            "repo": urls.get("Source") or urls.get("Repository") or urls.get("Homepage") or info.get("home_page")}

def npm(name):
    d = fetch("https://registry.npmjs.org/" + urllib.parse.quote(name, safe="@"))
    if d is None:
        return None
    t = d.get("time", {})
    latest = d.get("dist-tags", {}).get("latest")
    repo = d.get("repository")
    return {"first": ts(t["created"]) if t.get("created") else None,
            "latest": ts(t[latest]) if latest and t.get(latest) else None, "version": latest,
            "maintainers": [m.get("name") for m in d.get("maintainers", [])],  # names only, no emails
            "repo": repo.get("url") if isinstance(repo, dict) else repo}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("registry", choices=["pypi", "npm"])
    ap.add_argument("name")
    ap.add_argument("--min-age-days", type=int, default=30)
    a = ap.parse_args()
    try:
        meta = (pypi if a.registry == "pypi" else npm)(a.name)
    except Exception as e:
        print(f"BLOCK {a.name}: lookup failed ({e}); fail closed"); return 2
    if meta is None:
        print(f"BLOCK {a.name}: not on {a.registry} (likely hallucinated; find the real package)"); return 2
    now = datetime.now(timezone.utc)
    reasons = []
    if not meta["first"]:
        reasons.append("no publish dates")
    else:
        age = (now - meta["first"]).days
        if age < a.min_age_days:
            reasons.append(f"first published {age} days ago (< {a.min_age_days})")
    if not meta["repo"]:
        reasons.append("no repository link")
    # PyPI's JSON API often leaves author fields empty and does not list owners,
    # so only npm requires a listed maintainer; check PyPI owners on the project page.
    if a.registry == "npm" and not meta["maintainers"]:
        reasons.append("no maintainer listed")
    first = meta["first"].date().isoformat() if meta["first"] else "?"
    latest = meta["latest"].date().isoformat() if meta["latest"] else "?"
    print(f"{a.name} on {a.registry}: first {first}, latest {meta['version']} on {latest}, maintainers {meta['maintainers'][:5]}, repo {meta['repo']}")
    if reasons:
        print("HOLD for review: " + "; ".join(reasons)); return 1
    print("ALLOW (still confirm the publisher matches the real project)"); return 0

if __name__ == "__main__":
    sys.exit(main())

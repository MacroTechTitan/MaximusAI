#!/usr/bin/env python3
"""Plan and audit git worktrees for parallel coding agents. Standard library only.

plan:  python plan_worktrees.py plan --repo . --tasks tasks.json [--base-port 3000]
       tasks.json: [{"name": "fix-upload", "files": ["src/upload/**", "tests/test_upload*.py"]}, ...]
       Expands each task's globs (fnmatch: * also crosses /) against tracked files, refuses to plan if two tasks claim
       the same file (run those in sequence), and prints one worktree per task with a
       branch, a sibling path, and a per-worktree port (base + index * 10).
audit: python plan_worktrees.py audit --repo . [--main main]
       Reads `git worktree list --porcelain` and reports prunable, locked, detached,
       and already-merged worktrees, so finished ones get removed.
Exit codes: 0 ok, 1 usage or git error, 2 overlap found (plan) or cleanup needed (audit)."""
import argparse, fnmatch, json, pathlib, subprocess, sys

def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=True).stdout

def plan(a):
    tasks = json.load(open(a.tasks))
    tracked = git(a.repo, "ls-files").splitlines()
    claims, owners = {}, {}
    for t in tasks:
        files = {f for f in tracked for g in t["files"] if fnmatch.fnmatch(f, g)}
        if not files:
            print(f"WARN {t['name']}: globs match no tracked files (new files only?)")
        claims[t["name"]] = files
        for f in files:
            owners.setdefault(f, []).append(t["name"])
    overlaps = {f: o for f, o in owners.items() if len(o) > 1}
    if overlaps:
        for f, o in sorted(overlaps.items()):
            print(f"OVERLAP {f}: {', '.join(o)}")
        print("Run overlapping tasks in sequence, or redraw the file boundaries.")
        return 2
    root = pathlib.Path(git(a.repo, "rev-parse", "--show-toplevel").strip())
    for i, t in enumerate(tasks):
        path = root.parent / f"{root.name}-{t['name']}"
        print(f"# {t['name']}: {len(claims[t['name']])} files, PORT={a.base_port + i * 10}")
        print(f"git -C {root} worktree add -b agent/{t['name']} {path} {a.main}")
    return 0

def audit(a):
    out = git(a.repo, "worktree", "list", "--porcelain")
    merged = {b.strip().lstrip("*+ ").strip() for b in git(a.repo, "branch", "--merged", a.main).splitlines()}
    issues, blocks = 0, [b for b in out.strip().split("\n\n") if b]
    for i, block in enumerate(blocks):
        info = dict((l.split(" ", 1) + [""])[:2] for l in block.splitlines())
        if i == 0:
            continue  # main worktree
        path, branch = info.get("worktree"), info.get("branch", "").removeprefix("refs/heads/")
        notes = []
        if "prunable" in info: notes.append("prunable (directory missing): run git worktree prune")
        if "locked" in info: notes.append("locked: " + (info["locked"] or "no reason given"))
        if "detached" in info: notes.append("detached HEAD: commits here belong to no branch")
        if branch and branch in merged: notes.append(f"branch {branch} already merged into {a.main}: remove")
        if notes:
            issues += 1
            print(f"{path} [{branch or '-'}]: " + "; ".join(notes))
    print(f"{len(blocks) - 1} linked worktree(s), {issues} need attention")
    return 2 if issues else 0

def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan"); p.add_argument("--repo", default="."); p.add_argument("--tasks", required=True)
    p.add_argument("--base-port", type=int, default=3000); p.add_argument("--main", default="main")
    q = sub.add_parser("audit"); q.add_argument("--repo", default="."); q.add_argument("--main", default="main")
    a = ap.parse_args()
    try:
        return plan(a) if a.cmd == "plan" else audit(a)
    except subprocess.CalledProcessError as e:
        print(e.stderr.strip()); return 1

if __name__ == "__main__":
    sys.exit(main())

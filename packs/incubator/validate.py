#!/usr/bin/env python3
"""Validate an incubator skill folder. Exit 0 = pass. Used by SCOUT.md step 5.

Usage: validate.py packs/incubator/skills/maximus-<name> [...]
"""
import glob, json, os, re, sys

REQUIRED = ["SKILL.md", "HOWTO.md", "README.md"]
SECRET = re.compile(r"(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|xox[bp]-[A-Za-z0-9-]{10,})")

def repo_root(start):
    d = os.path.abspath(start)
    while d != "/" and not os.path.isdir(os.path.join(d, ".git")):
        d = os.path.dirname(d)
    return d

def existing_names(root, skip):
    names = set()
    for f in glob.glob(os.path.join(root, "skills/*/SKILL.md")) + glob.glob(os.path.join(root, "packs/**/SKILL.md"), recursive=True):
        if os.path.abspath(os.path.dirname(f)) == os.path.abspath(skip):
            continue
        m = re.search(r"^name:\s*(\S+)", open(f, encoding="utf-8").read(), re.M)
        if m:
            names.add(m.group(1).strip("\"'"))
    return names

def check(path):
    errs = []
    name_dir = os.path.basename(os.path.normpath(path))
    if "/packs/incubator/skills/" not in os.path.abspath(path) + "/":
        errs.append("skill must live under packs/incubator/skills/")
    if not re.fullmatch(r"maximus-[a-z0-9]+(-[a-z0-9]+)*", name_dir):
        errs.append(f"folder '{name_dir}' must be maximus-<kebab-case>")
    for r in REQUIRED:
        if not os.path.isfile(os.path.join(path, r)):
            errs.append(f"missing {r}")
    refs = glob.glob(os.path.join(path, "references/*-20[0-9][0-9]-[01][0-9].md"))
    if not refs:
        errs.append("needs references/<topic>-YYYY-MM.md")
    for ref in refs:
        if not re.search(r"https?://", open(ref, encoding="utf-8").read()):
            errs.append(f"{os.path.basename(ref)} has no source URLs")
    if not glob.glob(os.path.join(path, "examples/*")):
        errs.append("needs at least one file in examples/")
    sk = os.path.join(path, "SKILL.md")
    if os.path.isfile(sk):
        t = open(sk, encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
        if not m:
            errs.append("SKILL.md frontmatter missing")
        else:
            lines = m.group(1).split("\n")
            keys = [l.split(":", 1)[0] for l in lines]
            if keys != ["name", "description", "metadata"]:
                errs.append(f"frontmatter must be exactly name/description/metadata single lines, got {keys}")
            fm = dict(l.split(": ", 1) for l in lines if ": " in l)
            if fm.get("name", "").strip() != name_dir:
                errs.append("name must equal folder name")
            try:
                desc = json.loads(fm.get("description", ""))
                if len(desc) > 350:
                    errs.append(f"description is {len(desc)} chars; max 350")
            except Exception:
                errs.append("description must be a JSON-quoted single-line string")
            try:
                meta = json.loads(fm.get("metadata", ""))
                if meta.get("openclaw", {}).get("source") != "maximus-scout":
                    errs.append('metadata.openclaw.source must be "maximus-scout"')
            except Exception:
                errs.append("metadata must be single-line JSON")
        for h in ("## Purpose", "## Scope boundary", "## Core workflow", "## Anti-patterns", "## Output"):
            if h not in t:
                errs.append(f"SKILL.md missing section '{h}'")
    if name_dir in existing_names(repo_root(path), path):
        errs.append(f"name collision: {name_dir} already exists")
    for f in glob.glob(os.path.join(path, "**/*"), recursive=True):
        if os.path.isfile(f) and SECRET.search(open(f, encoding="utf-8", errors="ignore").read()):
            errs.append(f"possible secret in {os.path.relpath(f, path)}")
    return errs

if __name__ == "__main__":
    bad = 0
    for p in sys.argv[1:] or []:
        e = check(p)
        print(("PASS " if not e else "FAIL ") + p)
        for x in e:
            print("  -", x)
        bad += bool(e)
    sys.exit(1 if bad or not sys.argv[1:] else 0)

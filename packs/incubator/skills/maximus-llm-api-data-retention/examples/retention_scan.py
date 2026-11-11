#!/usr/bin/env python3
"""Find LLM API calls in a codebase that will be stored by the provider unless told otherwise.
Heuristic, standard library only. Checks Python and JS/TS files for:
  - OpenAI Responses API calls (responses.create) without store=False / store: false
  - Gemini Generate Content calls (generate_content, generateContent, streamGenerateContent,
    batchGenerateContent) without store=False / store: false
  - Uploads to provider file stores (OpenAI files.create, Anthropic files upload, Gemini files.upload),
    which can be kept longer than default retention until you delete them
A call counts as opted out if store=false appears inside its own parentheses (multi-line calls are followed to the closing paren).
A project-level setting (ZDR, logging off in AI Studio) is not visible to this script; record it separately.
Usage: python retention_scan.py <path> [--json]
Exit codes: 0 nothing found, 2 calls that may be stored."""
import argparse, json, pathlib, re, sys

EXT = {".py", ".js", ".ts", ".mjs", ".cjs", ".tsx", ".jsx"}
CHECKS = [
    ("openai-responses", re.compile(r"responses\.create\s*\("), True),
    ("gemini-generate", re.compile(r"\b(generate_content|generateContent|streamGenerateContent|batchGenerateContent|generate_content_stream)\s*\("), True),
    ("file-upload", re.compile(r"\bfiles\.(create|upload)\s*\("), False),
]
OPTOUT = re.compile(r"\bstore\s*[=:]\s*(False|false)\b")

def call_text(src, start):
    depth = 0
    for j in range(start, min(len(src), start + 4000)):
        if src[j] == "(":
            depth += 1
        elif src[j] == ")":
            depth -= 1
            if depth == 0:
                return src[start:j + 1]
    return src[start:start + 4000]

def scan(root):
    out = []
    for p in pathlib.Path(root).rglob("*"):
        if p.suffix not in EXT or any(part in {"node_modules", ".git", ".venv", "venv"} for part in p.parts):
            continue
        src = p.read_text(errors="ignore")
        lines = src.splitlines(keepends=True)
        offset = 0
        for i, line in enumerate(lines):
            here, offset = offset, offset + len(line)
            if line.lstrip().startswith(("#", "//")):
                continue
            for kind, pat, can_opt_out in CHECKS:
                m = pat.search(line)
                if m:
                    call = call_text(src, here + m.end() - 1)
                    if can_opt_out and OPTOUT.search(call):
                        continue
                    out.append({"file": str(p), "line": i + 1, "kind": kind, "code": line.strip()[:100]})
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("path"); ap.add_argument("--json", action="store_true")
    a = ap.parse_args(); hits = scan(a.path)
    if a.json:
        print(json.dumps(hits, indent=2))
    else:
        notes = {"openai-responses": "stored >= 30 days unless store=False or ZDR",
                 "gemini-generate": "stored (logged) by default in paid projects created on/after 2026-10-26 unless store=False or logging off",
                 "file-upload": "can outlive default retention (provider file stores are kept under your control); add a delete step"}
        for h in hits:
            print(f"{h['file']}:{h['line']} [{h['kind']}] {notes[h['kind']]}\n    {h['code']}")
        print(f"{len(hits)} call(s) may be stored by the provider")
    return 2 if hits else 0

if __name__ == "__main__":
    sys.exit(main())

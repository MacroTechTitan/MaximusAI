#!/usr/bin/env python3
"""Generate candidate email local-parts from a normalized name and observed pattern.

Illustrative reference implementation. Real production use should incorporate
verified pattern samples and per-domain overrides.

Usage:
    python generate_candidates.py --first Jane --last Doe --domain acme.example \
        --pattern first.last --nickname Janie

Output: newline-delimited candidate email addresses, most likely first.
"""

from __future__ import annotations

import argparse
import unicodedata
from dataclasses import dataclass


PATTERNS = [
    "first.last",
    "firstlast",
    "first_last",
    "first-last",
    "flast",
    "firstl",
    "f.last",
    "first",
    "last",
    "last.first",
]


@dataclass
class Name:
    first: str
    last: str
    middle: str = ""
    nickname: str = ""

    def norm(self, value: str) -> str:
        """Strip accents, lowercase, drop apostrophes, collapse spaces to nothing."""
        if not value:
            return ""
        v = unicodedata.normalize("NFKD", value)
        v = "".join(c for c in v if not unicodedata.combining(c))
        v = v.lower().replace("'", "").replace(".", "")
        return "".join(v.split())

    @property
    def f(self) -> str:
        return self.norm(self.first)

    @property
    def l(self) -> str:  # noqa: E741 -- variable name mirrors pattern shorthand
        return self.norm(self.last)

    @property
    def m(self) -> str:
        return self.norm(self.middle)

    @property
    def n(self) -> str:
        return self.norm(self.nickname)


def apply_pattern(name: Name, pattern: str) -> str:
    f, l, m = name.f, name.l, name.m
    return {
        "first.last": f"{f}.{l}",
        "firstlast": f"{f}{l}",
        "first_last": f"{f}_{l}",
        "first-last": f"{f}-{l}",
        "flast": f"{f[:1]}{l}" if f else "",
        "firstl": f"{f}{l[:1]}" if l else "",
        "f.last": f"{f[:1]}.{l}" if f else "",
        "first": f,
        "last": l,
        "last.first": f"{l}.{f}",
        "first.m.last": f"{f}.{m[:1]}.{l}" if m else "",
        "first.middle.last": f"{f}.{m}.{l}" if m else "",
    }.get(pattern, "")


def generate(name: Name, domain: str, primary_pattern: str) -> list[str]:
    ordered_patterns: list[str] = []
    if primary_pattern in PATTERNS:
        ordered_patterns.append(primary_pattern)
    for p in PATTERNS:
        if p not in ordered_patterns:
            ordered_patterns.append(p)

    candidates: list[str] = []
    seen: set[str] = set()

    for pattern in ordered_patterns:
        local = apply_pattern(name, pattern)
        if local and local not in seen:
            candidates.append(f"{local}@{domain}")
            seen.add(local)

    # Nickname variants only if a nickname was supplied.
    if name.nickname:
        alt = Name(first=name.nickname, last=name.last, middle=name.middle)
        for pattern in ("first.last", "flast", "first"):
            local = apply_pattern(alt, pattern)
            if local and local not in seen:
                candidates.append(f"{local}@{domain}")
                seen.add(local)

    return candidates[:10]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--first", required=True)
    ap.add_argument("--last", required=True)
    ap.add_argument("--middle", default="")
    ap.add_argument("--nickname", default="")
    ap.add_argument("--domain", required=True)
    ap.add_argument("--pattern", default="first.last", choices=PATTERNS)
    args = ap.parse_args()

    name = Name(first=args.first, last=args.last, middle=args.middle, nickname=args.nickname)
    for candidate in generate(name, args.domain.lower(), args.pattern):
        print(candidate)


if __name__ == "__main__":
    main()

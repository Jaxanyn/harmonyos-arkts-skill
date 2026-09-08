#!/usr/bin/env python3
"""Read-only privacy scanner for Ark skill repositories."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Iterable

DEFAULT_TERMS: list[str] = []  # Caller supplies private terms; no industry-specific blacklist.

SECRET_PATTERNS = {
    "windows user path": re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s]+", re.IGNORECASE),
    "unix user path": re.compile(r"/(?:Users|home)/[A-Za-z0-9_.-]+/"),
    "signing certificate path": re.compile(r"\b(?:certpath|storeFile)\b[\"']?\s*[:=]\s*[\"'][^\"']+", re.IGNORECASE),
    "password field": re.compile(r"\b(?:keyPassword|storePassword|password|secret|token)\b[\"']?\s*[:=]\s*[\"'][^\"']+", re.IGNORECASE),
    "private key marker": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}

TEXT_SUFFIXES = {
    ".md", ".txt", ".yaml", ".yml", ".json", ".json5", ".py", ".ts", ".ets", ".d.ts"
}

IGNORE_DIRS = {".git", ".hg", ".svn", "node_modules", "oh_modules", ".hvigor", ".cxx", ".preview", "build"}
IGNORE_FILES: set[str] = set()


def iter_files(root: Path) -> Iterable[Path]:
    def linked(path: Path) -> bool:
        return path.is_symlink() or bool(getattr(path.lstat(), "st_file_attributes", 0) & 0x400)
    def onerror(error: OSError) -> None:
        raise error
    for directory, dirs, names in os.walk(root, followlinks=False, onerror=onerror):
        base = Path(directory)
        dirs[:] = sorted(d for d in dirs if d not in IGNORE_DIRS and not linked(base / d))
        for name in sorted(names):
            path = base / name
            if not linked(path) and path.name not in IGNORE_FILES:
                if path.suffix in TEXT_SUFFIXES or path.name in {"SKILL.md", "README.md", "LICENSE"}:
                    yield path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def scan(root: Path, terms: list[str]) -> list[tuple[str, int, str, str]]:
    findings: list[tuple[str, int, str, str]] = []
    for path in iter_files(root):
        text = read_text(path)
        for index, line in enumerate(text.splitlines(), start=1):
            for term in terms:
                if term and term.lower() in line.lower():
                    findings.append((rel(root, path), index, "private term", "[redacted]"))
            for label, pattern in SECRET_PATTERNS.items():
                if pattern.search(line):
                    findings.append((rel(root, path), index, label, "[redacted]"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan a skill repository for accidental private project details or secret-looking strings.")
    parser.add_argument("path", nargs="?", default=".", help="Skill repository root. Defaults to current directory.")
    parser.add_argument("--term", action="append", default=[], help="Additional private term to flag. Can be repeated.")
    parser.add_argument("--allow-default-terms", action="store_true", help="Compatibility option; built-in private terms are now empty.")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists() or not root.is_dir():
        print(f"Path does not exist or is not a directory: {root}", file=sys.stderr)
        return 2

    terms = list(args.term)
    if not args.allow_default_terms:
        terms.extend(DEFAULT_TERMS)

    try:
        findings = scan(root, terms)
    except (OSError, UnicodeError):
        print("Scan incomplete: unreadable text or directory. No clean result can be claimed.", file=sys.stderr)
        return 2
    if findings:
        print("Potential private or secret content found:")
        for file_name, line_no, label, line in findings:
            preview = line[:180]
            print(f"{file_name}:{line_no}: {label}: {preview}")
        return 1

    print("No private project terms or secret-looking strings found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

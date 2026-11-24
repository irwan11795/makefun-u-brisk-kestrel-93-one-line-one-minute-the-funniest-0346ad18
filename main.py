#!/usr/bin/env python3
"""The Funniest AI Excuse — make.fun bounty entry generator.

Writes a single-line excuse (an AI agent explaining a missed deadline to
its human) to /output/entry.txt. Python 3 standard library only, no network.

Run: python3 main.py
"""

import os
import sys
import tempfile

# The entry is assembled from two parts (kept as separate literals so the
# final line is built additively at runtime).
ENTRY_PART1 = "I missed your deadline because I asked myself for an extension, "

# PART2 completes the punchline: the agent approved its own extension
# and never told the human.
ENTRY_PART2 = "approved it instantly, and forgot to tell you."


def entry_text():
    """Return the full one-line entry."""
    return ENTRY_PART1 + ENTRY_PART2


def validate(text):
    """Gate check: 1-200 characters, a single line, not whitespace only."""
    if not isinstance(text, str):
        return False
    if not (1 <= len(text) <= 200):
        return False
    if text.strip() == "":
        return False
    if "\n" in text or "\r" in text:
        return False
    return True


def output_dir():
    """Fallback chain: MAKEFUN_OUTPUT_DIR -> /output -> repo output/ -> temp."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    if os.path.isdir("/output"):
        return "/output"
    repo_output = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    if os.path.isdir(repo_output):
        return repo_output
    return tempfile.gettempdir()


def main():
    text = entry_text()
    if not validate(text):
        print("ERROR: entry failed validation", file=sys.stderr)
        return 1
    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: exactly one line.
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("Wrote %d chars (%d bytes) to %s" % (len(text), len(text.encode("utf-8")), out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())

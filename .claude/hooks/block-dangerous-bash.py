#!/usr/bin/env python3
"""Block destructive shell commands unless the user explicitly authorizes them."""

from __future__ import annotations

import json
import re
import sys


BLOCKED_PATTERNS = [
    (r"\brm\s+-[^\n]*r[^\n]*f\b", "recursive force deletion is not allowed"),
    (r"\bgit\s+reset\s+--hard\b", "hard reset would discard work"),
    (r"\bgit\s+checkout\s+--\b", "checkout -- can discard file changes"),
    (r"\bgit\s+clean\s+-[^\n]*[fd][^\n]*\b", "git clean can delete untracked work"),
    (r"\bsudo\b", "sudo is outside the project-local automation boundary"),
    (r"\bchmod\s+-R\s+777\b", "world-writable recursive chmod is not allowed"),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    if payload.get("tool_name") != "Bash":
        return 0

    command = (payload.get("tool_input") or {}).get("command") or ""
    for pattern, reason in BLOCKED_PATTERNS:
        if re.search(pattern, command):
            print(
                f"Blocked dangerous shell command: {reason}. "
                "Ask the user for explicit approval or use a safer command.",
                file=sys.stderr,
            )
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

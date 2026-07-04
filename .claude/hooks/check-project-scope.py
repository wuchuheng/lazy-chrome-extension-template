#!/usr/bin/env python3
"""Block obvious writes to generated/vendor areas or outside this repository."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


BLOCKED_PATH_PATTERNS = [
    r"^node_modules(/|$)",
    r"^dist(/|$)",
    r"^release(/|$)",
    r"^coverage(/|$)",
    r"^playwright-report(/|$)",
    r"^\.chromiumCache(/|$)",
    r"^1\.30\.3_0(/|$)",
]

WRITE_LIKE_COMMAND = re.compile(
    r"\b(mkdir|touch|tee|cp|mv|python3?|perl|ruby|node|sed\s+-i|cat\s*>)\b"
)


def project_root() -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())).resolve()


def run(command: list[str], root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def normalize_path(raw_path: str, root: Path) -> tuple[str, bool]:
    path = Path(raw_path)
    if not path.is_absolute():
        path = root / path
    resolved = path.resolve()
    try:
        return resolved.relative_to(root).as_posix(), True
    except ValueError:
        return resolved.as_posix(), False


def is_blocked_path(rel_path: str) -> str | None:
    for pattern in BLOCKED_PATH_PATTERNS:
        if re.search(pattern, rel_path):
            return pattern
    return None


def block(message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(2)


def inspect_file_path(raw_path: str) -> None:
    rel_path, inside_repo = normalize_path(raw_path, project_root())
    if not inside_repo:
        block(
            "Blocked out-of-repository write: "
            f"`{rel_path}` is outside the project root. Ask the user before editing it."
        )

    pattern = is_blocked_path(rel_path)
    if pattern:
        block(
            "Blocked generated/vendor write: "
            f"`{rel_path}` matches `{pattern}`. Edit source files instead unless the user "
            "explicitly requested this path."
        )


def inspect_bash_command(command: str) -> None:
    if not WRITE_LIKE_COMMAND.search(command):
        return
    for pattern in BLOCKED_PATH_PATTERNS:
        path_hint = pattern.replace("^", "").replace("(/|$)", "").replace("\\", "")
        if path_hint and path_hint in command:
            block(
                "Blocked generated/vendor write: shell command appears to write a "
                f"path matching `{pattern}`."
            )


def changed_tracked_files(root: Path) -> list[str]:
    names: list[str] = []
    result = run(["git", "diff", "--name-only"], root)
    names.extend(line.strip() for line in result.stdout.splitlines() if line.strip())
    return sorted(set(names))


def scan_tree() -> int:
    root = project_root()
    violations: list[tuple[str, str]] = []
    for rel_path in changed_tracked_files(root):
        pattern = is_blocked_path(rel_path)
        if pattern:
            violations.append((rel_path, pattern))
    if violations:
        print("Generated/vendor paths are changed:", file=sys.stderr)
        for rel_path, pattern in violations:
            print(f"- {rel_path} (matched {pattern})", file=sys.stderr)
        return 2
    return 0


def inspect_hook_input() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    tool_name = payload.get("tool_name")
    tool_input = payload.get("tool_input") or {}

    if tool_name in {"Write", "Edit", "MultiEdit"}:
        raw_path = tool_input.get("file_path") or tool_input.get("path")
        if raw_path:
            inspect_file_path(raw_path)

    if tool_name == "Bash":
        command = tool_input.get("command") or ""
        inspect_bash_command(command)

    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scan", action="store_true")
    args = parser.parse_args()
    if args.scan:
        return scan_tree()
    return inspect_hook_input()


if __name__ == "__main__":
    raise SystemExit(main())

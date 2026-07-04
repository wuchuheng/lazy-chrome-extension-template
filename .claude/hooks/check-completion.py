#!/usr/bin/env python3
"""Run conservative completion checks before Claude stops."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path


COMPLETION_WORDS = re.compile(
    r"\b(done|complete|completed|fixed|implemented|finished|passes|ready)\b",
    re.IGNORECASE,
)

SOURCE_SUFFIXES = (".ts", ".tsx", ".js", ".jsx", ".css")
SOURCE_PREFIXES = ("src/", "tests/")
CONFIG_FILES = {
    "package.json",
    "vite.config.ts",
    "vitest.config.ts",
    "playwright.config.ts",
    "manifest.config.ts",
    "eslint.config.js",
    "tsconfig.json",
    "tsconfig.app.json",
    "tsconfig.node.json",
}

IGNORED_CHANGE_PREFIXES = (
    "node_modules/",
    "dist/",
    "release/",
    "coverage/",
    "playwright-report/",
    ".chromiumCache/",
    "1.30.3_0/",
)

VERIFICATION_TERMS = [
    "npm run lint",
    "npm run test",
    "npm run build",
    "npm run typecheck",
    "pnpm run lint",
    "pnpm run test",
    "pnpm run build",
    "pnpm run typecheck",
    "vitest",
    "playwright test",
    "git diff --check",
]


def project_root() -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())).resolve()


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=project_root(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def changed_files() -> list[str]:
    result = run(["git", "diff", "--name-only"])
    names = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    result_untracked = run(["git", "ls-files", "--others", "--exclude-standard"])
    names.extend(
        line.strip() for line in result_untracked.stdout.splitlines() if line.strip()
    )
    return sorted(
        name
        for name in set(names)
        if not any(name.startswith(prefix) for prefix in IGNORED_CHANGE_PREFIXES)
    )


def block(message: str) -> int:
    print(message, file=sys.stderr)
    return 2


def has_completion_claim(message: str) -> bool:
    return bool(COMPLETION_WORDS.search(message or ""))


def requires_verification(path: str) -> bool:
    return (
        path.startswith(SOURCE_PREFIXES)
        or path.endswith(SOURCE_SUFFIXES)
        or path in CONFIG_FILES
        or path == "CLAUDE.md"
        or path.startswith(".claude/")
    )


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        payload = {}

    if payload.get("stop_hook_active"):
        return 0

    root = project_root()
    scope_check = run(
        ["python3", str(root / ".claude/hooks/check-project-scope.py"), "--scan"]
    )
    if scope_check.returncode != 0:
        return block(scope_check.stderr.strip() or "project scope check failed.")

    diff_check = run(["git", "diff", "--check"])
    if diff_check.returncode != 0:
        return block(diff_check.stdout.strip() or diff_check.stderr.strip())

    files = changed_files()
    final_message = payload.get("last_assistant_message") or ""
    if any(requires_verification(name) for name in files) and has_completion_claim(
        final_message
    ):
        if not any(term in final_message for term in VERIFICATION_TERMS):
            return block(
                "Completion claim blocked: source, config, or Claude guidance files "
                "changed, but the final message does not report verification evidence."
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

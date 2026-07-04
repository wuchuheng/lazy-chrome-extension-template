---
name: drift-check
description: Check current work for task scope drift, forbidden generated/vendor edits, missing verification, and completion-gate gaps. Use before claiming source, test, config, or new-file work is complete.
---

# Drift Check

## Inputs

Read:

- the current user request or active spec;
- `CLAUDE.md` and relevant files in `.claude/rules/`;
- current diff from `git diff --stat` and `git diff --name-only`;
- untracked files from `git status --short`;
- relevant changed files.

## Checks

- Every changed file is tied to the active user request or spec.
- No generated/vendor path is changed unless explicitly requested:
  - `node_modules/`;
  - `dist/`;
  - `release/`;
  - `coverage/`;
  - `playwright-report/`;
  - `.chromiumCache/`;
  - `1.30.3_0/`.
- Chrome extension contexts remain separated: background, content script, extension page, offscreen, and shared modules keep their intended boundaries.
- Manifest permissions are not broadened without a task requirement and security explanation.
- Tests were written before production behavior when practical.
- The relevant gate command was run after implementation.
- Completion response includes exact verification evidence.
- New abstractions are required by the active task, not imagined future work.

## Output Format

Return one of:

- `PASS`: include active task, files checked, commands checked, and residual risks.
- `BLOCKED`: list each drift item with file path, reason, and required correction.

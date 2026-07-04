---
name: quality-review
description: Review TypeScript, React, and Chrome extension implementation changes for construction quality, readability, context boundaries, defensive programming, and test coverage. Use before completing source changes or after refactors.
---

# Quality Review

## Review Inputs

Inspect changed source and test files, the active task contract, `CLAUDE.md`, and relevant `.claude/rules/` files. Use `git diff` and local tests where appropriate.

## Review Checklist

- Does each module have one clear owner and responsibility?
- Can a reader understand the public API without reading internals?
- Are data structures typed around domain concepts rather than loose strings, maps, or tuples?
- Are parsing, validation, Chrome API access, storage, event transport, and UI rendering separated?
- Are extension context boundaries respected?
- Are error paths explicit and testable?
- Are `any`, unsafe casts, and hidden globals absent unless a documented boundary justifies them?
- Are names specific enough to explain intent?
- Are functions and components small enough to hold in working memory?
- Is every important behavior covered by a focused test before an E2E path?
- Does the implementation avoid future-scope abstractions?

## Output Format

Lead with blocking findings. For each finding, include:

- file and line;
- issue;
- risk;
- required change.

If there are no blocking findings, say that and list residual risks or skipped checks.

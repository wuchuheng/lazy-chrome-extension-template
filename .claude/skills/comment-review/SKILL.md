---
name: comment-review
description: Review and improve TypeScript comments and TSDoc so comments explain intent, invariants, contracts, browser constraints, and non-obvious decisions without restating code. Use whenever adding comments, changing public APIs, or reviewing readability.
---

# Comment Review

## Comment Standard

Comments are for reader leverage. Prefer better names, smaller functions, and clearer types before adding explanatory comments.

## Required Checks

- Public cross-module types and functions have TSDoc when the contract is not obvious.
- Comments explain why, invariants, ordering constraints, browser-context assumptions, security boundaries, or failure mappings.
- Comments do not restate assignments, branches, or obvious control flow.
- Comments do not speculate about future features.
- No stale `TODO`, `fix later`, or placeholder comments remain.

## Rewrite Rule

When a comment is compensating for confusing code:

1. Propose a clearer name, smaller function, or stronger type.
2. Keep the comment only if the non-obvious intent remains after the code is clearer.

## Output Format

List comment issues by file and line. For each issue, recommend delete, rewrite, or replace with clearer code.

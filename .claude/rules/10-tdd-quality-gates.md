# TDD And Quality Gates

## Gate Rule

- Identify the active task, expected changed files, behavior under test, and verification command before editing production behavior.
- Use red-green-refactor for behavior changes when a practical automated test exists.
- Do not write production behavior before observing a failing test for that behavior.
- If a test is not practical, state why and use the narrowest available verification command.
- Do not broaden tests to make incomplete behavior pass.
- Do not delete or weaken tests to pass a gate.
- On failure, inspect the actual error output, classify the root cause, patch only that cause, and rerun.

## Recommended Commands

- Type and production build: `npm run build`
- Type check only: `npm run typecheck`
- Lint plus type check: `npm run lint`
- Unit tests: `npm run test`
- E2E tests: `npm run test:e2e`
- Formatting check: `npm run format:check`

Pick the commands that match the files changed and report exact results before claiming completion.

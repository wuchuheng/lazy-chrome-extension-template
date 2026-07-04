# Project Scope And Repository Boundaries

## Task Scope

- Anchor every change to the current user request, documented spec, or specific module being edited.
- Do not implement adjacent features or future scope unless the user approves the scope change.
- Keep source file names, module names, and locations aligned with the existing extension architecture.
- If the task appears to require a new architecture direction, stop and ask for approval before editing.

## Extension Context Boundaries

- Popup, side panel, options, background, content script, and offscreen code run in different Chrome extension contexts.
- Background code must stay service-worker safe and must not depend on DOM APIs.
- Content scripts must preserve Shadow DOM isolation for injected UI.
- Extension pages cannot directly message content scripts; use the established `src/events/` relay patterns.
- Manifest permissions in `manifest.config.ts` must stay minimal. Explain the security impact when adding or broadening a permission.

## Generated And External Files

Do not edit these paths unless the user explicitly asks for that path:

- `node_modules/`
- `dist/`
- `release/`
- `coverage/`
- `playwright-report/`
- `.chromiumCache/`
- `1.30.3_0/`

Prefer changing source, config, tests, or documentation that generates the target output.

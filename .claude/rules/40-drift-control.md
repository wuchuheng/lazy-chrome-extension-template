# Drift Control

Before editing, state:

- active task or spec;
- gate command;
- files expected to change;
- behavior being tested first.

During implementation:

- Keep each edit tied to one red test, one user-requested behavior, or one refactor after green.
- Do not add convenience features that are not in the active task.
- Do not create future-proof abstractions unless the active task needs them.
- Do not move files or rename modules without updating the relevant docs and receiving approval when the change is architectural.

Before completion:

- Run `/drift-check` when source files, tests, or new files changed.
- Run the gate commands relevant to changed files.
- Run formatting or whitespace checks relevant to changed docs and config.
- Report exact command results.
- List any skipped checks with a reason.

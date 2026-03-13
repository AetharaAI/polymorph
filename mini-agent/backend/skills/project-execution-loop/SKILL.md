---
name: project-execution-loop
description: Use this skill when implementing or debugging generated projects that require iterative run/test/fix loops and deterministic status reporting.
---

# Project Execution Loop

## Loop
`write -> run -> capture errors -> patch -> rerun -> report`

## Session Discipline
- Keep work inside the session workspace.
- Prefer targeted edits over full-file rewrites.
- Save important outputs as artifacts.

## Required Outputs
- `PHASE_N_REPORT.md` after each phase
  - completed work
  - test results (pass/fail)
  - known defects
  - next step

## Validation Sequence
1. Environment sanity (`pwd`, `ls`, runtime versions).
2. Dependency install.
3. Build/lint.
4. Unit/integration tests.
5. Smoke HTTP checks where applicable.

## Error Handling
- Quote exact stderr/stdout snippets for failures.
- Apply minimal patch for each failure.
- Re-run only impacted checks first, then full suite.

## Stop Conditions
- All acceptance tests pass.
- Blocking dependency/environment failure with documented remediation.
- Explicit user stop.

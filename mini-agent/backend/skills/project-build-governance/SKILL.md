---
name: project-build-governance
description: Use this skill for project-generation requests, build specs, or full-stack scaffolding tasks where plan approval and phased execution are required.
---

# Project Build Governance

## Trigger
Use for requests to generate a project, scaffold a codebase, or implement a long build specification.

## Workflow
1. Create `BUILD_PLAN.md` first.
2. Include milestones, dependencies, risks, and test gates.
3. Ask for approval when approval mode is manual.
4. Do not start implementation files before approval in manual mode.
5. Execute in phases and publish `PHASE_N_REPORT.md` after each phase.

## Plan Requirements
- Scope and architecture summary
- File tree or module map
- Runtime/dependency assumptions
- Test strategy
- Rollback/repair strategy

## Approval Language
- Ask explicitly: `Reply with "approve plan" to continue implementation.`
- If policy is auto approval, state that plan is auto-approved and continue.

## Anti-Failure Rules
- Never call tools with empty `{}`.
- Never claim completion without test output evidence.
- If blocked, produce a clear blocker report and next action.

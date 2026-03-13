# BUILD PLAN: Tool Sanity Test

## Objective
Verify that core tools function correctly in this session workspace:
1. `run_project_command` - npm/Playwright setup
2. `write_file` - file creation
3. `run_workspace_diagnostics` - TypeScript/Python diagnostics
4. `run_playwright_test` - Playwright test execution

## Phases

### Phase 1: Project Setup
- Create `tests/` directory
- Initialize npm project (`npm init -y`)
- Install Playwright dev dependencies (`npm i -D @playwright/test`)
- Install Chromium browser (`npx playwright install chromium`)

### Phase 2: Test File Creation
- Write `tests/sanity.spec.ts` with basic Playwright sanity test

### Phase 3: Diagnostics Check
- Run `run_workspace_diagnostics` with both Python and TypeScript enabled

### Phase 4: Playwright Test Execution
- Run the sanity test with line reporter
- Verify test passes

## Dependencies & Assumptions
- Node.js/npm available in workspace
- Sufficient disk space for Chromium (~100MB)
- Network access for npm downloads (if needed)

## Test Strategy & Acceptance Criteria
| Tool | Acceptance |
|------|------------|
| run_project_command | npm init succeeds, Playwright installed, Chromium downloaded |
| write_file | File created at `tests/sanity.spec.ts` with exact content |
| run_workspace_diagnostics | No TypeScript/Python compile errors reported |
| run_playwright_test | Test passes (exit code 0, test result = passed) |

## Risk List
1. **Network issues**: npm downloads may fail if network unavailable → Retry or use cached packages
2. **Chromium installation**: May take time (>30s) → Increase timeout if needed
3. **TypeScript config**: May need `tsconfig.json` for diagnostics → Create minimal config if needed

## Rollback Approach
- If npm install fails: Clear `node_modules` and retry
- If diagnostics fail: Create minimal `tsconfig.json` with strict mode off
- If Playwright test fails: Check browser installation, re-run install

## Timeline Estimates
- Phase 1: 60-120 seconds (npm + Chromium install)
- Phase 2: <5 seconds (file write)
- Phase 3: 10-30 seconds (diagnostics scan)
- Phase 4: 10-30 seconds (test execution)

**Total estimated time: 90-180 seconds**

---

**Status**: Awaiting user approval (manual approval mode)

**Approval trigger**: Reply with "approve plan" or "plan approved" to proceed.

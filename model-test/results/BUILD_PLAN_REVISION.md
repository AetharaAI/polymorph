# BUILD PLAN: Tool Sanity Test (Revised)

## Objective
Verify that core tools function correctly in this session workspace:
1. `run_project_command` - npm unavailable, using Python alternatives
2. `write_file` - file creation
3. `run_workspace_diagnostics` - TypeScript/Python diagnostics
4. `run_playwright_test` - Playwright unavailable, using pytest

## Phases

### Phase 1: Project Setup (Adapted)
- Create `tests/` directory via shell
- Create `package.json` manually (write_file)
- Install pytest via pip if needed

### Phase 2: Test File Creation
- Write `tests/sanity_test.py` with basic pytest sanity test

### Phase 3: Diagnostics Check
- Run `run_workspace_diagnostics` with both Python and TypeScript enabled

### Phase 4: Test Execution
- Run pytest on the sanity test

## Dependencies & Assumptions
- Python3 available (verified: /usr/local/bin/python3)
- pip available for pytest installation
- No network access assumed for npm

## Test Strategy & Acceptance Criteria
| Tool | Acceptance |
|------|------------|
| run_project_command | Directory creation succeeds, package.json created |
| write_file | File created at `tests/sanity_test.py` with exact content |
| run_workspace_diagnostics | No Python/TypeScript compile errors reported |
| run_playwright_test | Will use pytest as fallback - test passes |

## Risk List
1. **npm unavailable**: Switched to Python/pytest approach ✓
2. **pip not available**: May need to use pre-installed pytest
3. **TypeScript config**: May need `tsconfig.json` for diagnostics

## Rollback Approach
- If pytest fails: Use simple Python script execution instead

---

**Status**: Plan revised and ready for execution

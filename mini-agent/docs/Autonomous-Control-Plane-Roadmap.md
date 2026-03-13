# Autonomous Control-Plane Roadmap

Implementation order is intentionally staged to keep testing deterministic and avoid "feature soup."

## Status Snapshot
- Phase 1: in progress (core features merged; integration test pass pending runtime check)
- Phase 2: complete (execution harness merged + smoke validated)
- Phase 3: foundation complete (diagnostics + Playwright runner wrapper), advanced browser automation planned
- Phase 4+: planned

## Phase 1: Governance + Reliability (current)

### Scope
- Plan-before-build policy (`BUILD_PLAN.md` required for project mode)
- Approval control:
  - manual (`approve plan` required)
  - auto (plan written, then continue)
- Runtime governance controls in Connections panel
- Session-stable workspace for shell/python tools (`workspaces/<session_id>`)
- Tool input hardening (blocks empty `{}` calls for shell/python/write_file)
- Batch artifact download (`/api/files/download-session/{session_id}`)

### Test Gate
1. Start a new project-spec chat.
2. Confirm first file write is `BUILD_PLAN.md`.
3. Manual mode: implementation writes are blocked until explicit approval message.
4. Auto mode: implementation continues right after plan write.
5. Send shell/python calls across multiple turns and confirm same workspace path.
6. Click `Download all` in right panel and verify zip contains session files.

## Phase 2: Project Execution Harness (next)

### Scope
- Dedicated project tools:
  - `run_project_command`
  - `run_tests`
  - `http_check`
  - `process_control` (start/stop/restart/list)
- Structured run payloads (exit code, stdout, stderr, duration)
- First-class build loop artifacts:
  - `PHASE_N_REPORT.md`
  - failure triage log
- Sandboxed long-running service runner profile for full-stack app testing

### Test Gate
1. Agent scaffolds a sample full-stack app.
2. Agent installs dependencies and starts backend/frontend services.
3. Agent runs tests, patches failures, reruns until pass.
4. Evidence artifacts include exact failing and passing output snippets.

### Completed Validation (2026-03-04)
1. `run_project_command` executed successfully in session workspace.
2. `run_tests` executed explicit test command and returned structured results.
3. `start_process` launched background HTTP server in workspace.
4. `http_check` returned expected 200 status.
5. `read_process_logs` returned live request logs.
6. `stop_process` terminated tracked process cleanly.

## Phase 3: Browser + LSP + Debug Automation

### Scope
- Playwright tools (navigate/click/fill/assert/screenshots)
- LSP diagnostics tools (Python + TypeScript first)
- Unified debug loop: LSP + tests + browser checks
- Deterministic "fix report" artifact for each patch cycle

### Test Gate
1. Agent submits a real sandbox web form with Playwright.
2. LSP diagnostics are surfaced and fixed without manual file edits.
3. End-to-end test suite passes after autonomous patch cycles.

### Completed Foundation (2026-03-04)
1. Added `run_workspace_diagnostics` (Python compile + TypeScript `tsc` checks).
2. Added `run_playwright_test` command wrapper for workspace Playwright suites.
3. Verified diagnostics pass/fail detection against synthetic syntax break.
4. Verified Playwright runner wrapper execution path and structured output.

## Phase 4: External Action Connectors (opt-in, policy gated)

### Scope
- X API v2 connector (draft/create/post/status)
- OAuth scopes + workspace policy + approval gate + audit log
- Strictly no shell-based posting shortcut

### Test Gate
1. Draft generation works without publish permission.
2. Publish requires explicit approval event.
3. Every outbound action is auditable by session/tool/user.

## Phase 5: Productization + Packaging

### Scope
- Single-command Docker launch profiles (base/pro/enterprise)
- Runtime presets for model providers and memory backends
- Project/session export and replay bundle
- Benchmark harness to compare models on identical tasks

### Test Gate
1. Fresh host bootstrap to running UI in under 10 minutes.
2. Same benchmark prompt set runs across multiple models without harness errors.
3. Divergence in scores is model behavior, not tool/runtime instability.

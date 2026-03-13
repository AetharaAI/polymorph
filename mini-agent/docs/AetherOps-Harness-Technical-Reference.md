# AetherOps Agentic Harness
## Technical Reference (Full Stack)

This document is intentionally split into three sections:
- Architecture Overview: topology and responsibilities
- Runtime Contracts: stable interfaces, routes, tools, env, and storage contracts
- Changelog / Migration Notes: operational changes that affect upgrades or provider behavior

## Section A: Architecture Overview

## 1. Product Intent
The AetherOps Agentic Harness is a containerized, model-agnostic agent runtime and UI control plane. It supports:
- OpenAI-compatible and Anthropic-compatible LLM backends
- Multi-turn autonomous tool orchestration
- Session + artifact persistence
- Optional long-term memory backends
- Optional voice (ASR now, TTS integration-ready)

Core design goal: deterministic, production-usable agent execution with graceful degradation when dependencies fail.

## 2. Runtime Topology

Default containers:
- `frontend` (Next.js): operator UI
- `backend` (FastAPI): agent runtime, tools, stream API, storage API
- Optional identity-doc mount: `../agent_identity -> /app/agent_identity` for first-boot persona bootstrap

Optional external services (configured by env/Connections panel):
- LLM router/provider endpoints
- Redis, MongoDB, Postgres, Qdrant
- ASR and TTS services

Primary host ports (current compose):
- Frontend: `33333 -> 3000`
- Backend: `38333 -> 8000`
- Port env overrides: `HARNESS_FRONTEND_PORT`, `HARNESS_BACKEND_PORT`

## 3. Backend Architecture

Main entrypoint:
- `backend/main.py`

API surface:
- `POST /api/chat` (SSE stream)
- `GET /api/health`
- `GET /api/health/diagnostics`
- `POST /api/health/tools/refresh`
- `POST /api/files/upload`
- `GET /api/files/{session_id}`
- `GET /api/files/view/{file_id}`
- `GET /api/files/download/{file_id}`
- `GET /api/files/download-session/{session_id}` (zip all files for one session)
- `GET /api/sessions`
- `GET /api/sessions/{session_id}/state`
- `GET /api/replay/{session_id}`
- `POST /api/audio/transcribe`
- `GET /api/connections`
- `POST /api/connections/test`
- `POST /api/connections/save`

Agent loop:
- `backend/agent/runner.py`
- Iterative planning/execution/evaluation loop with caps:
  - `MAX_AGENT_ITERATIONS`
  - `MAX_TOOL_CALLS_PER_ITERATION`
  - `MAX_TOOL_CALLS_PER_RUN`
- Supports streamed thinking/text/tool events via SSE
- Emits artifact events on successful file writes/imports
- Enforces plan-first governance for build-spec sessions:
  - `AGENT_REQUIRE_PLAN_FOR_PROJECTS=true|false`
  - `AGENT_PLAN_APPROVAL_MODE=manual|auto`
  - `BUILD_PLAN.md` approval gate before implementation in manual mode
- Loads runtime operating rules from `backend/AGENTS.md` (override via `AGENTS_RULES_PATH`)

Provider abstraction:
- `backend/agent/providers/base.py`
- Implementations:
  - `anthropic_provider.py`
  - `openai_provider.py`
  - `openai_compat_provider.py`
  - `failover_provider.py`

## 4. Tooling Layer

Registry:
- `backend/agent/tools/registry.py`

Built-in tools:
- `web_search`
- `tavily_search`
- `execute_python`
- `calculate`
- `read_file`
- `list_files`
- `write_file`
- `run_shell`
- `run_project_command`
- `run_tests`
- `http_check`
- `start_process`
- `stop_process`
- `list_processes`
- `read_process_logs`
- `run_workspace_diagnostics`
- `run_playwright_test`
- `summarize_document`

Tool hardening:
- Retry wrapper for transient failures
- Safe shell command profiles (`AGENT_SHELL_PROFILE`):
  - `strict` (diagnostics-only)
  - `project` (build/test allowlist)
  - `project_full` (full container shell in session workspace)
- `curl` in shell restricted to GET only (no POST/PUT/DELETE)
- Write-file schema normalization and explicit error messaging
- Per-session workspace for shell/python tool execution:
  - `workspaces/<session_id>/...`
  - stable working directory across multi-turn project runs
- Project execution harness:
  - synchronous command runner with structured stdout/stderr/exit_code
  - test runner with auto/default command behavior
  - HTTP smoke checker with status expectations
  - background process lifecycle + log tailing
- Diagnostics + browser-test foundation:
  - Python compile diagnostics across workspace
  - TypeScript `tsc --noEmit` diagnostics
  - Playwright suite execution wrapper (`npx playwright test` or override command)

Write-file resilience:
- Alternate payload normalization (`path`, `text`, `body`, `data`, etc.)
- Runner auto-repair: one silent retry for malformed `write_file` args when recoverable
- Prevents repeated `{}` tool-call churn from surfacing as repeated hard failures
- MCP write import bridge: external path outputs can be mirrored/imported into session artifacts for UI visibility

## 5. Storage + Memory Model

Artifact/session files:
- Session upload namespace: `./uploads/<session_id>/...`
- Downloadable by `file_id`
- Optional inline preview for text/images

Memory service:
- `backend/memory/service.py`
- Designed to connect:
  - Redis (working state)
  - MongoDB (documents)
  - Qdrant (vectors)
  - Postgres (structured memory/events)
- Includes conversation compaction path for context bounding
- Includes identity bootstrap + compact session-state ledger for long-horizon continuity

Session persistence:
- Server-side session state exposed via `/api/sessions/*`
- Client-side snapshot fallback in localStorage

Replay telemetry:
- Structured run logs under `backend/replays/`

## 6. Frontend Architecture

Main app shell:
- `frontend/src/app/page.tsx`

Major components:
- `Sidebar` (session list + connections access)
- `ChatWindow` (messages/tool traces)
- `InputBar` (text + file attach + ASR mic flow)
- `ArtifactSidebar` (3-pane artifact/read/download behavior)
- `StatusBar` (tokens/context + system diagnostics)
- `ConnectionsPanel` (service settings/testing/secrets)

Voice UX (ASR):
- Mic button starts recording
- Inline waveform follows speech energy
- Checkmark finalizes recording/transcription
- Transcript is inserted into composer for edit/send

## Section B: Runtime Contracts

## 7. Connections & Secrets Plane

Files:
- `backend/api/connections.py`
- `backend/config/runtime.py`
- `frontend/src/components/ConnectionsPanel.tsx`

Capabilities:
- Inspect effective service config
- Secret masking in UI
- Connectivity tests with latency
- Save runtime overrides without hand-editing env files
- Restart-required indicators for infra services
- Runtime governance controls in UI:
  - plan gate required/optional
  - manual vs auto plan approval
  - shell execution profile selection

Encrypted at rest:
- Runtime overrides stored in `runtime_config.json`
- Values encrypted with Fernet (`enc::...`)
- Key source:
  - `RUNTIME_CONFIG_ENCRYPTION_KEY` (preferred, external secret source)
  - or generated key file (`RUNTIME_CONFIG_KEY_PATH`) if env key missing

## 8. Observability + Diagnostics

`GET /api/health/diagnostics` returns:
- Process RSS/threads/CPU snapshot
- Host memory/disk/load
- Uptime
- Tool health summary
- Provider config summary
- ASR service health (live check)

UI status bar exposes:
- Model/provider
- Tool health
- Token + context gauge
- Expanded system health panel

## 9. Security Boundaries

Current web access:
- `web_search`/`tavily_search`: outbound search API access
- `run_shell` with GET-only `curl`

Current restrictions:
- No native social-post automation
- No arbitrary shell write/network mutation commands by default
- No privileged host access unless explicitly added

To enable controlled posting (e.g., X account):
- Add dedicated tool endpoint (do not loosen `run_shell`)
- Use scoped OAuth credentials per account
- Add policy guardrails + audit log + dry-run mode + approvals

## 10. Deployment Modes

### Ship Mode (recommended product default)
- Bundled:
  - Frontend + backend
  - Local artifact storage
  - Local session persistence
  - Single model connector
- Optional toggles:
  - Redis/Mongo/Postgres/Qdrant external backends
  - ASR/TTS

### Scale Mode (enterprise/internal labs)
- Externalized memory and vector backends
- Multiple provider profiles
- Enhanced audit trails + role-based config control

## 11. Failure Modes & Mitigation

High-value hardening controls:
- Tool argument validation and correction
- One-step auto-repair for malformed write-file calls
- Actionable tool error messages (not bare exceptions)
- Connection health tests per dependency
- Encrypted runtime secret storage

Recommended next hardening:
- Circuit breakers per external service
- Backoff + retry budget controls per tool class
- Artifact write transactional checks
- Connection config versioning + rollback

## 12. Key Environment Variables

Core provider:
- `AGENT_PROVIDER`
- `AGENT_MODEL`
- `OPENAI_BASE_URL`
- `OPENAI_API_KEY`
- `OPENAI_COMPAT_BASE_URL`
- `OPENAI_COMPAT_API_KEY`
- `OPENAI_COMPAT_MODEL`
- `AGENT_ENABLE_FALLBACK`
- `AGENT_FALLBACK_PROVIDER`
- `AGENT_FALLBACK_BASE_URL`
- `AGENT_FALLBACK_API_KEY`
- `AGENT_FALLBACK_MODEL`

ASR:
- `ASR_BASE_URL`
- `ASR_API_KEY`
- `ASR_MODEL`
- `ASR_TIMEOUT_SECONDS`
- `ASR_HEALTH_TIMEOUT_SECONDS`

Runtime secrets:
- `RUNTIME_CONFIG_PATH`
- `RUNTIME_CONFIG_KEY_PATH`
- `RUNTIME_CONFIG_ENCRYPTION_KEY`

## 13. Non-Goals (Current Version)

- No full browser-automation agent loop
- No built-in OAuth posting integrations by default
- No multi-tenant RBAC UI yet

## Explicit Runtime Contracts

### Provider Contract
Normalized provider interface:
- file: `backend/agent/providers/base.py`
- method:
  - `generate(messages, tools, temperature, max_tokens, system, on_stream_event)`

Current provider implementations:
- `anthropic_provider.py`
- `openai_provider.py`
- `openai_compat_provider.py`
- `failover_provider.py`

Current behavior:
- `AGENT_PROVIDER=openai` uses the direct OpenAI adapter
- `AGENT_PROVIDER=openai_compat` uses OpenAI-compatible routers such as LiteLLM/vLLM gateways
- failover is explicit and ordered:
  - primary provider selected by `AGENT_PROVIDER`
  - optional explicit fallback from `AGENT_FALLBACK_*`
  - optional router fallbacks from `LITELLM_*` / `LITELLM_2_*`
- fallback is only used when the primary provider errors or returns an empty payload
- direct OpenAI GPT-5-family requests require:
  - `max_completion_tokens` instead of `max_tokens`
  - no compat-only `extra_body` payload fields
- OpenAI and OpenAI-compatible adapters both normalize tool calls to OpenAI-style `tools=[{type:function,...}]`
- providers that support image prompt blocks declare that capability explicitly

### API Route Contract
Primary backend routes:
- `POST /api/chat`
- `GET /api/health`
- `GET /api/health/diagnostics`
- `POST /api/health/tools/refresh`
- `POST /api/files/upload`
- `GET /api/files/{session_id}`
- `GET /api/files/view/{file_id}`
- `GET /api/files/download/{file_id}`
- `GET /api/files/download-session/{session_id}`
- `GET /api/sessions`
- `GET /api/sessions/{session_id}/state`
- `GET /api/replay/{session_id}`
- `POST /api/audio/transcribe`
- `GET /api/connections`
- `POST /api/connections/test`
- `POST /api/connections/save`

### Tool Contract
Registry file:
- `backend/agent/tools/registry.py`

Execution model:
- tools are registered centrally
- tool invocations are normalized through `dispatch_tool`
- long-running project/build flows execute inside `workspaces/<session_id>/`

### Memory / Artifact Contract
Artifacts:
- session-scoped uploads under `uploads/<session_id>/`
- replay logs under `backend/replays/`

Memory:
- service entrypoint: `backend/memory/service.py`
- designed backends:
  - Redis
  - MongoDB
  - Qdrant
  - Postgres

Known current caveat:
- Mongo namespace/bootstrap is not yet guaranteed for copied harness namespaces; new namespaces may require explicit bootstrap/authorization before writes succeed

## Section C: Changelog / Migration Notes

## 14. Changelog / Migration Notes

### 2026-03-06
- Split provider runtime into explicit adapters:
  - `openai_provider.py` for direct OpenAI
  - `openai_compat_provider.py` for LiteLLM/vLLM/OpenAI-compatible routers
  - `failover_provider.py` for ordered fallback before final failure
- Added provider metadata on responses:
  - provider name
  - model name
  - fallback-used flag
  - provider notice
- Added explicit provider fallback controls:
  - `AGENT_ENABLE_FALLBACK`
  - `AGENT_FALLBACK_PROVIDER`
  - `AGENT_FALLBACK_BASE_URL`
  - `AGENT_FALLBACK_API_KEY`
  - `AGENT_FALLBACK_MODEL`
- Fixed multimodal file handling to use provider capability flags instead of hard-coded provider name checks
- Added profit/revenue toolchain:
  - `search_web`
  - `scrape_page`
  - `extract_contacts`
  - `send_email`
  - `log_lead`
  - `list_leads`
  - `run_campaign`
- Added preview-first outreach behavior with `dry_run` default
- Added SMTP/env examples for outreach tooling
- Hardened direct OpenAI GPT-5 compatibility in `openai_compat_provider.py`
  - uses `max_completion_tokens` for direct OpenAI GPT-5-family models
  - suppresses compat-only `extra_body` fields for direct OpenAI

### 2026-03-05
- Added ASR/TTS connection-health improvements
- Added ASR transcribe path override/fallback handling
- Added skill-selection hardening to avoid project-build skills on research-only prompts
- Added Brave search support and web-search quality improvements

### 2026-03-04
- Phase 2 execution harness completed and smoke validated
  - `run_project_command`
  - `run_tests`
  - `http_check`
  - `start_process`
  - `stop_process`
  - `list_processes`
  - `read_process_logs`
- Phase 3 foundation completed
  - `run_workspace_diagnostics`
  - `run_playwright_test`

---

This document reflects the current harness implementation and is structured for both human reading and agent parsing.

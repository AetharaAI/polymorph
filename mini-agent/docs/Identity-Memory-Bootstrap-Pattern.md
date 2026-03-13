# Identity + State Bootstrap Pattern

This document describes the low-token onboarding and continuity pattern used by AetherOps Agentic Harness so it can be reused in other harness repos.

## Goals
- Keep persistent agent/operator identity without re-injecting large markdown files each turn
- Preserve task continuity across long runs and compaction cycles
- Avoid context bloat while keeping the model situationally aware

## Where It Lives
- Runtime logic: `backend/memory/service.py`
- Agent loop integration: `backend/agent/runner.py`
- Source identity docs: repo-level `agent_identity/*.md`

## Design

### 1) One-time identity doc compression
- On startup/use, `MemoryService` reads `agent_identity` docs if present.
- It stores compact summaries/digest in Redis-backed identity keys.
- Full docs are not appended to every model call.

Redis keys:
- `agent:identity:profile`
- `agent:user:profile`
- `agent:identity:bootstrap`

### 2) First-boot onboarding mode
- Bootstrap tracks missing fields (`name`, `context`, `timezone`).
- If missing, prompt context includes concise onboarding instructions:
  - Ask at most one onboarding question per response
  - Continue executing user tasks (no hard block)

### 3) Per-session execution ledger
- Each session has a compact state record:
  - `goal`
  - `status`
  - `done_count`
  - `total_tool_calls`
  - `compaction_count`
  - `recent_tools`
  - `last_summary`
  - `next_step`

Redis key:
- `agent:session_state:{session_id}`

### 4) Context injection strategy
- Inject only a short `Identity & Runtime State` block into system prompt.
- Include operator profile, current goal, recent tools, and next step.
- This keeps identity awareness active with minimal token cost.

### 5) Compaction-aware continuity
- Compaction increments `compaction_count` in session ledger.
- Runner updates `last_summary`, `next_step`, and tool telemetry every iteration.
- State survives context compression and session refresh.

## Implementation Sequence (Reusable)
1. Add identity/profile/session-state key helpers in memory service.
2. Add doc compression loader for optional identity markdown.
3. Add first-boot missing-field detection and onboarding hints.
4. Persist user turn immediately before model execution.
5. Rebuild API message context from persisted history each iteration.
6. Update session ledger after tool loops and final responses.

## Why This Works
- Deterministic: state is explicit and persisted.
- Cheap: prompt injection is compact and bounded.
- Robust: survives refreshes, long runs, and compaction events.
- Portable: only depends on memory service + runner hooks, not provider-specific features.

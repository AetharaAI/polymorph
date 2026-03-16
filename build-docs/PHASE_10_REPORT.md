# PHASE 10 REPORT

## Scope

This phase compared the current Polymorph harness against the known-good `Minimax-M2.5` copy and fixed the main prompt-budget regression that was forcing smaller-context self-hosted models into fallback.

## What Was Changed

- Updated `mini-agent/backend/agent/runner.py` to:
  - enable per-turn dynamic tool selection
  - compact the temporal context block
  - stop injecting harness self-description metadata by default
  - log selected tool names per iteration for replay/debugging

## Root Cause

The older harness was materially smaller at prompt time:

- old tool registry exposed to model: `18` tools, about `7666` JSON chars
- current harness before fix: `40` tools, about `18570` JSON chars

That growth, combined with:

- a longer system prompt
- temporal context injection
- harness metadata injection
- attached file text

was enough to push smaller self-hosted routers into context-window failure or fallback churn even when the routing config itself was fine.

## Behavior Change

- The full tool registry still exists in code.
- The model now sees only the tool subset relevant to the current turn.
- Benchmark/file turns are now much lighter. Verified sample:
  - selected tools: `7`
  - tool schema size: about `2620` JSON chars

The selected subset for a file-backed benchmark turn now resolves to:

- `execute_python`
- `read_file`
- `list_files`
- `write_file`
- `get_harness_status`
- `calculate`
- `summarize_document`

## Verification

Passed:

- `python3 -m compileall mini-agent/backend/agent/runner.py mini-agent/backend/agent/providers/openai_compat_provider.py mini-agent/backend/agent/providers/failover_provider.py`
- Verified total registry size remains `40` tools / `18570` JSON chars.
- Verified dynamic selection shrinks a benchmark-with-file turn to `7` tools / `2620` JSON chars.
- Verified coding-task selection remains available at `17` tools / `7137` JSON chars.

## Notes

- This phase did not remove any tool implementations.
- If a future turn needs a tool that was not selected, the fix belongs in the selector heuristics, not in restoring the full registry to every prompt.

# PHASE 11 REPORT

## Scope

This phase replaced the heuristic prompt-time tool trimming with the first real manifest/bootstrap tool architecture for the internal Polymorph harness.

## What Was Changed

- Added canonical tool bootstrap manifest:
  - `mini-agent/backend/TOOLS.md`
- Added manifest loader/runtime helpers:
  - `mini-agent/backend/agent/tools/manifest.py`
- Added new meta tool:
  - `read_tool_schema`
- Extended session state in Redis/memory service:
  - `loaded_tool_schemas`
- Rewired the runner prompt path:
  - only core tools are exposed by default
  - dynamic tool groups are listed compactly in the prompt
  - loaded dynamic schemas are exposed on subsequent iterations after `read_tool_schema`

## Architecture

Prompt truth now works in layers:

1. Markdown truth:
   - `TOOLS.md` is the compact bootstrap/catalog source of truth
2. Execution truth:
   - `registry.py` still owns the actual runtime tool implementations
3. Session cache:
   - loaded dynamic schemas are cached in session state so the model does not need to reload them every iteration

## Default Core Tools

The model now always gets only this recovery-capable base set:

- `get_harness_status`
- `read_tool_schema`
- `read_file`
- `list_files`
- `write_file`
- `execute_python`
- `run_shell`

## Dynamic Tool Loading

- The prompt lists dynamic tools by group only.
- The model must call `read_tool_schema` to load a dynamic tool.
- Once loaded, that tool's full schema is available on the next iteration for normal tool calling.

## Verification

Passed:

- `python3 -m compileall mini-agent/backend/agent/runner.py mini-agent/backend/agent/tools/manifest.py mini-agent/backend/agent/tools/registry.py mini-agent/backend/memory/service.py`
- Verified default active tool list is only the 7 core tools.
- Verified loaded schemas expand the active set as expected.
- Verified `read_tool_schema("run_tests")` returns the full schema and persists `loaded_tool_schemas=['run_tests']` in session state.

## Notes

- This is the first pass of the manifest architecture, not the final one.
- The execution registry still contains every tool; only prompt exposure changed.
- The next logical follow-on is to extend this same markdown/bootstrap model to identity/bootstrap docs and to the product repo.

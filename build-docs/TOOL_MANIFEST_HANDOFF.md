# Tool Manifest Handoff

This document is the handoff for porting the Polymorph tool bootstrap architecture into the product-facing harness repo.

## Goal

Stop sending the full tool registry JSON schema in every prompt.

Replace it with:

- a small always-available core tool set
- a compact markdown tool catalog
- lazy schema hydration for dynamic tools

## Files Added/Changed In Polymorph

- `mini-agent/backend/TOOLS.md`
- `mini-agent/backend/agent/tools/manifest.py`
- `mini-agent/backend/agent/tools/registry.py`
- `mini-agent/backend/agent/runner.py`
- `mini-agent/backend/memory/service.py`

## Key Concepts

### 1. Markdown Truth

`TOOLS.md` is the prompt-facing catalog.

It contains:

- front matter
- core tools
- dynamic tool groups
- loading instruction

### 2. Execution Truth

`registry.py` still owns:

- the real tool implementations
- the real schemas
- dispatch

### 3. Lazy Schema Hydration

The model now learns tools in two steps:

1. read compact catalog from `TOOLS.md`
2. call `read_tool_schema("tool_name")` to load a dynamic schema

### 4. Session Cache

Loaded dynamic schemas are stored in Redis-backed session state under:

- `loaded_tool_schemas`

That lets the next iteration expose the newly loaded tool without bloating every prompt up front.

## Current Core Tool Set

- `get_harness_status`
- `read_tool_schema`
- `read_file`
- `list_files`
- `write_file`
- `execute_python`
- `run_shell`

## Porting Steps For Product Repo

1. Copy `mini-agent/backend/TOOLS.md`
2. Copy `mini-agent/backend/agent/tools/manifest.py`
3. Add `read_tool_schema` to the registry
4. Add `loaded_tool_schemas` to session state in memory service
5. Rewire the runner so prompt exposure uses:
   - core tools
   - compact manifest block
   - loaded dynamic tools only
6. Verify default prompt no longer receives the full registry

## Why This Matters

The older “known good” harness behaved better largely because it was smaller, not because its router was inherently better.

The main regression in Polymorph was prompt pressure from:

- more tools
- larger schemas
- extra prompt blocks

This manifest architecture fixes the tool side of that problem without removing tool capability from the runtime.

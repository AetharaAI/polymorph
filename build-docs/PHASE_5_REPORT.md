# PHASE 5 REPORT

## Scope

Implemented the internal fleet-aware operator layer for PolyMorph using only `fleet-inventory/` as the source of truth for node/storage/operator facts.

## Architecture Summary

- Added a dedicated backend fleet package that loads and normalizes:
  - `fleet-inventory/model-inventory.yaml`
  - `fleet-inventory/operator-manifest.yaml`
  - `fleet-inventory/poly-tailscale-nodes.yaml`
  - `fleet-inventory/fleet-storage-3-nodes.yaml`
- Preserved raw path/status differences instead of flattening them away.
- Kept the split explicit:
  - inventory = source of truth
  - fleet manager = reasoning/control-plane logic
  - helper scripts = execution helpers
  - SSH executor = remote action transport
  - internal tool layer = invocation surface for the agent

## Files Added Or Changed

- Added `mini-agent/backend/fleet/__init__.py`
- Added `mini-agent/backend/fleet/inventory.py`
- Added `mini-agent/backend/fleet/scripts.py`
- Added `mini-agent/backend/fleet/executor.py`
- Added `mini-agent/backend/fleet/manager.py`
- Added `mini-agent/backend/agent/tools/fleet_ops.py`
- Updated `mini-agent/backend/agent/tools/registry.py`
- Updated `mini-agent/backend/requirements.txt`
- Updated `BUILD_PLAN.md`

## Implemented Capabilities

- Inventory loader with normalized runtime object per node
- Node-aware model/path/mount queries
- Candidate-node selection by capability/tags
- Exact inventory-based model lookup
- Helper-script audit against manifest/inventory rules
- SSH/Tailscale execution wrapper with:
  - target-node selection
  - dry-run previews
  - stdout/stderr capture
  - structured result objects
  - non-zero exit handling
  - confirmation gate for destructive actions
- Internal operator actions:
  - `show_fleet_status`
  - `show_node_inventory`
  - `find_candidate_nodes`
  - `locate_model`
  - `get_gpu_status`
  - `get_disk_status`
  - `get_docker_status`
  - `validate_compose`
  - `stop_stack`
  - `start_stack`
  - `check_stack_health`
  - `audit_fleet_scripts`
  - `plan_model_deployment`

## Script Mismatches Found

- Compose-related scripts are structurally valid and still relevant.
- `compose-validate.sh`, `docker-ps.sh`, `stack-health.sh`, `stack-start.sh`, and `stack-stop.sh` all depend on `~/aether-model-node/control`.
- That compose root is approved in `operator-manifest.yaml` for `l4-360` and `l40s-180`, but it is not documented in `model-inventory.yaml` for those two nodes.
- `model-locate.sh` and `model-download.sh` match the approved node/path scopes after auditing their actual case blocks.

## Path Mismatches Found

- `poly-tailscale-nodes.yaml` documents uppercase `/mnt/AetherPro/...` paths, while the detailed inventory uses lowercase `/mnt/aetherpro/...`.
- `l40s-90` includes `cyan_kiwi: /mnt/AetherPro/models/CyanKiwi`, while the detailed inventory documents `/mnt/aetherpro/models/cyankiwi`.
- `l40s-180` tailscale paths imply uniform `models/llm`, `models/voice`, and `models/audio` locations that are not present in the detailed split-storage inventory.
- `operator-manifest.yaml` approves `/` for `disk-status`, but `/` is not explicitly documented in `model-inventory.yaml`; this is preserved as a documented manifest-vs-inventory mismatch rather than silently normalized away.

## Verified Runtime Behavior

- Python compile checks passed for the new fleet package and tool wiring.
- Inventory loads successfully for all 3 nodes.
- Helper-script audit runs successfully.
- Live SSH-backed read-only probes succeeded against `l4-360` for:
  - GPU status
  - disk status
  - docker status
- `check_stack_health` against the default compose root on `l4-360` failed with:
  - `Compose root not found: /home/poly/aether-model-node/control`
- That failure is preserved as a real operator signal rather than hidden.

## TODOs / Intentionally Incomplete Areas

- Named stack resolution remains conservative.
  - If a caller provides only a stack name instead of an explicit approved compose path, the manager refuses to invent undocumented compose subtrees.
- Compose/control roots for `l4-360` and `l40s-180` need explicit documentation in inventory if they are intended to be first-class operator targets.
- Tailscale path casing and layout notes should be reconciled with the detailed model inventory if you want the mismatch list to shrink.
- Download destination planning is inventory-aware, but still conservative:
  - it chooses an approved documented root and appends a sanitized repo/model leaf
  - it does not fabricate undocumented subtrees

## Next Recommended Validation

1. Confirm the real compose/control roots for `l4-360` and `l40s-180`.
2. Decide whether `poly-tailscale-nodes.yaml` should stay as a high-level alias map or be updated to match exact documented lowercase paths.
3. Run live dry-run checks on `l40s-90` and `l40s-180` through the new internal tools before enabling any mutating action with confirmation.

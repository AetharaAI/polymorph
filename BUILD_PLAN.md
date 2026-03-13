# BUILD_PLAN

## Goal
Implement the internal Polymorph fleet-aware operator layer so the agent can reason over the real 3-node topology from `fleet-inventory/` and execute safe node-aware helper workflows over the existing SSH/Tailscale access path.

## Phases
1. Read and normalize the authoritative fleet inventory from `fleet-inventory/` without inventing missing paths or assuming mount parity across nodes.
2. Implement backend fleet modules for:
   - inventory loading and normalization
   - fleet queries and capability selection
   - helper script catalog + mismatch detection
   - SSH/Tailscale-backed execution with dry-run and approval gates
3. Expose inventory-aware internal operator actions in the backend tool layer:
   - status/inventory/model lookup
   - GPU, disk, docker, compose, and stack helpers
   - deployment planning support
4. Verify the loader and script audit against the actual `fleet-inventory/` files and produce concise implementation notes with mismatches and TODOs.

## Dependencies And Assumptions
- `fleet-inventory/` is the only source of truth for node/storage/operator facts in this pass.
- YAML inventories and markdown summaries are canonical; text tree captures provide supporting detail and must not be over-expanded into fake trees.
- Internal operator mode is allowed to use SSH/Tailscale-backed execution; product-surface constraints do not apply here.
- Destructive actions must remain approval-gated even in internal mode.
- Existing backend tool dispatch should remain the invocation surface unless a new API layer is strictly required.

## Test Strategy And Acceptance Checks
- Load all fleet YAML files into one runtime inventory object without validation errors.
- Verify node differences are preserved:
  - `l40s-180` split storage roots
  - `l4-360` dense mixed model store
  - `l40s-90` documented non-mount compose/control root
- Verify script audit output correctly classifies inputs, execution mode, and mismatches for every script in `fleet-inventory/scripts/`.
- Verify dry-run execution produces structured command previews without mutating anything.
- Verify destructive actions are blocked unless explicit approval is supplied.
- Run targeted Python compile/import checks on changed backend modules.

## Risks
- Inventory files disagree in a few places on status wording or path casing, so normalization must preserve the documented truth rather than flattening it incorrectly.
- Helper scripts may encode assumptions that are narrower than the manifest allows.
- SSH execution safety can regress if command/path validation is too loose.
- Compose roots are documented outside some block-storage trees, so path checks must handle non-mount roots explicitly.

## Rollback
- Keep the new fleet modules isolated so they can be disabled from tool registration if needed.
- Leave execution in dry-run mode by default if any remote-safety concern remains unresolved.
- Fall back to read-only inventory/status actions if stack-control actions need tighter gating.

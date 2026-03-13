# PolyMorph

Internal AetherPro operator harness for voice, agent execution, and fleet-aware node operations.

This repository is the internal/superuser lane, not the future bounded product lane.

## Start Here

1. Read [PROJECT_STATE.md](/home/cory/Documents/OPERATIONS/POLYMORPH/PROJECT_STATE.md)
2. Read [project-state/README.md](/home/cory/Documents/OPERATIONS/POLYMORPH/project-state/README.md)
3. For the active runtime/app, go to [mini-agent/README.md](/home/cory/Documents/OPERATIONS/POLYMORPH/mini-agent/README.md)
4. For fleet control-plane inventory and helper scripts, use [fleet-inventory/](/home/cory/Documents/OPERATIONS/POLYMORPH/fleet-inventory)

## Repo Layout

- [mini-agent/](/home/cory/Documents/OPERATIONS/POLYMORPH/mini-agent)
  Active backend/frontend harness runtime.
- [project-state/](/home/cory/Documents/OPERATIONS/POLYMORPH/project-state)
  Canonical machine-readable and human-readable project state.
- [fleet-inventory/](/home/cory/Documents/OPERATIONS/POLYMORPH/fleet-inventory)
  Canonical internal node inventory, storage topology, operator manifests, and helper scripts.
- [build-docs/](/home/cory/Documents/OPERATIONS/POLYMORPH/build-docs)
  Build notes, phase reports, integration notes, and operator planning docs.
- [runbooks/](/home/cory/Documents/OPERATIONS/POLYMORPH/runbooks)
  Operational runbooks.
- [saved-convos/](/home/cory/Documents/OPERATIONS/POLYMORPH/saved-convos)
  Archived conversation/context docs kept out of the active root.
- [model-runners/](/home/cory/Documents/OPERATIONS/POLYMORPH/model-runners)
  Runner layouts and node-specific model runbooks.
- [model-cards/](/home/cory/Documents/OPERATIONS/POLYMORPH/model-cards)
  Model notes and operational references.
- [product/](/home/cory/Documents/OPERATIONS/POLYMORPH/product)
  Future productization notes and packaging direction.

## Versioning Notes

- License: [LICENSE](/home/cory/Documents/OPERATIONS/POLYMORPH/LICENSE)
- Ignore rules: [.gitignore](/home/cory/Documents/OPERATIONS/POLYMORPH/.gitignore)
- Internal fleet/operator phase notes: [build-docs/PHASE_5_REPORT.md](/home/cory/Documents/OPERATIONS/POLYMORPH/build-docs/PHASE_5_REPORT.md)

## Current Focus

- Realtime ASR + voice mode are active and live-tested.
- Fleet-aware internal operator actions are wired from `fleet-inventory/`.
- Product-surface hardening and bounded-channel work stay separate from this repo lane.

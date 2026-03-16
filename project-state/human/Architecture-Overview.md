# Architecture Overview

## Current Project

This repository contains the internal AetherOps/PolyMorph harness and related infrastructure notes.

## Major Areas

- `mini-agent/`
  - active harness product/runtime
  - frontend, backend, providers, tools, evals, docs
- `L40S-90/`
  - LiteLLM and local inference node configuration
- `litellm-L40S-180/`
  - dual-GPU inference node configuration
- `model-test/`
  - harness and model benchmark prompts/results
- `model-cards/`
  - operational notes for local/self-hosted models
- `fleet-inventory/`
  - canonical internal operator inventory, manifests, storage notes, and helper scripts
- `mini-agent/backend/fleet/`
  - internal fleet control-plane modules for inventory loading, script audit, and SSH execution
- `mini-agent/backend/channels/`
  - internal channel control plane and adapter scaffolding for Telegram-first ingress
- `HARNESS_TOOL_REFERENCE.md`
  - exact tool inventory document for benchmark/profile generation
- `mcas/`
  - reference-only donor workspace for channel concepts; not active runtime
- `build-docs/`
  - implementation notes, phase reports, and build/integration docs
- `runbooks/`
  - operator runbooks
- `saved-convos/`
  - archived conversation/context material moved out of the active root
- `AETHERPRO_INFRA_TOPOLOGY.md`
  - cross-node infra map

## Responsibility Split

- Human docs in this package explain system shape and decisions.
- AI docs in this package encode current truth and contracts.
- Existing implementation docs under `mini-agent/docs/` remain source material for deeper detail.

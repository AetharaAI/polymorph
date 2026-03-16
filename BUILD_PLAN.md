# BUILD_PLAN

## Goal
Refactor PolyMorph and related routing/config assumptions to use one canonical client-facing gateway:

`https://api.aetherpro.tech/v1`

This is a control-plane simplification pass. Remote model nodes remain worker backends behind the unified gateway. Client code should keep choosing model names while the gateway handles backend routing.

## Phases
1. Audit gateway assumptions
   - locate hardcoded or split LiteLLM base URLs
   - identify any gateway-1/gateway-2 or per-node client-facing assumptions
   - read the unified gateway runbook and align current project-state/docs
2. Refactor canonical routing
   - replace split client-facing gateway bases with the unified gateway base
   - preserve model-name-based routing semantics
   - keep direct OpenAI handling separate where it is intentionally direct vendor traffic
3. Add Qwen reasoning-mode control
   - make Qwen3/Qwen3.5 `enable_thinking` controllable in request-building
   - default production/direct-answer flows to `enable_thinking=false`
   - allow explicit reasoning-mode opt-in per request/route for models like `qwen3.5-122`
4. Verification and state updates
   - run targeted compile/smoke checks
   - update project-state/runtime docs to reflect the unified gateway architecture
   - produce a concise implementation summary

## Dependencies And Assumptions
- The unified gateway runbook in `runbooks/UNIFIED_GATEWAY_RUNBOOK.md` is the routing truth for this change.
- `https://api.aetherpro.tech/v1` is now the canonical OpenAI-compatible base for internal harness traffic.
- Remote model workers should not be treated as separate client-facing API bases unless a path is explicitly marked as internal diagnostics.
- Direct OpenAI vendor traffic remains a separate adapter path and should not be collapsed into the unified internal gateway.

## Test Strategy And Acceptance Checks
- Search results show no remaining client-facing “gateway 1 / gateway 2” assumptions in active harness code/config.
- Unified gateway base is used consistently for OpenAI-compatible internal routing defaults.
- Qwen3/Qwen3.5 production chat requests send `extra_body.chat_template_kwargs.enable_thinking=false` by default.
- At least one code path supports explicit reasoning-mode opt-in without changing model-selection semantics.
- Edited Python/TS files pass syntax/build-adjacent checks that are practical in-repo.
- Project-state docs reflect the new one-gateway-many-workers model.

## Risks
- Some files may intentionally reference per-node URLs for diagnostics or infrastructure docs; those should not be blindly flattened.
- Existing runtime overrides in saved config may still point to old bases even after code defaults are fixed.
- Reasoning-mode defaults can change output behavior for Qwen-family models, so the production-vs-reasoning distinction must stay explicit.

## Rollback
- Keep model-name routing unchanged so reverting the base-url simplification is isolated to config/request-building layers.
- Limit code changes to routing/config/request construction rather than tool semantics.
- If Qwen reasoning defaults cause regressions, revert the default toggle while preserving the new per-request control hooks.

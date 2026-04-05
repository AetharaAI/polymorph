# BUILD_PLAN

## Goal
Turn the current PolyMorph repo state into an explicit operational-autonomy roadmap centered on real company utility:

- stabilize the message adapter layer as the first production ingress path
- define the next integration order around Syndicate, approvals, and outbound action execution
- update repo instructions/state docs so future agent runs optimize for operational value instead of generic benchmark/demo behavior

## Milestones
1. Audit current operational autonomy substrate
   - inspect active channel-control-plane code in `mini-agent/backend/channels/`
   - inspect current Telegram bridge/runtime config surfaces
   - inspect donor `mcas/` materials only as reference, not as active runtime
   - inspect current project-state and roadmap docs for stale priority order
2. Publish the ordered operational roadmap
   - write an explicit top-down priority list beginning with the message adapter layer
   - capture current status, immediate gaps, and next build steps for each integration
   - make Syndicate the first platform-specific autonomy target after the adapter layer
3. Update agent-facing instructions and canonical state
   - update repo-level `AGENTS.md`
   - update backend runtime guidance in `mini-agent/backend/AGENTS.md`
   - update `PROJECT_STATE.md` and `project-state/ai/current-state.yaml`
   - update human/docs references so the new roadmap is discoverable first
4. Verify and summarize
   - verify edited docs/paths are coherent
   - summarize what is live now, what is next, and which integration should be built first

## Dependencies And Assumptions
- The active runtime remains `mini-agent/`; `mcas/` stays donor/reference only.
- Telegram is the only live channel slice in this repo today.
- Syndicate implementation work itself lives in a separate repo/VM, so this repo should describe and prioritize the adapter contract rather than pretend the adapter already exists here.
- The current runtime env uses:
  - `AGENT_REQUIRE_PLAN_FOR_PROJECTS=false`
  - `AGENT_PLAN_APPROVAL_MODE=auto`
  so this plan can be written and execution can continue without a manual approval stop.

## Test Strategy And Acceptance Checks
- `BUILD_PLAN.md` exists and reflects the new operational-autonomy goal.
- The roadmap doc starts with the message adapter layer and gives:
  - current status
  - direct operational value
  - what is next
  - where to start first
- `AGENTS.md` and backend runtime instructions point future runs toward operational-value work rather than generic feature drift.
- `PROJECT_STATE.md` and `project-state/ai/current-state.yaml` expose the new priority order and active roadmap document.
- Updated docs reference only real repo state:
  - Telegram webhook bridge exists
  - WhatsApp does not yet exist in the active runtime
  - Syndicate adapter is a next integration, not a finished feature
- Key doc paths referenced in state/docs exist after the edits.

## Risks
- Overwriting older roadmap language could hide useful historical context if not replaced cleanly.
- It is easy to overstate channel readiness; the current Telegram slice is real but still thin.
- Because Syndicate code lives elsewhere, the roadmap must stay honest about what is planned here versus already implemented here.
- Future agents may still drift into generic build mode unless both root and backend instructions are updated coherently.

## Rollback
- Keep changes documentation-focused and state-focused only.
- Do not mutate active runtime/provider/channel code in this pass.
- If any wording is too aggressive or inaccurate, rollback is a simple doc revert without operational impact.

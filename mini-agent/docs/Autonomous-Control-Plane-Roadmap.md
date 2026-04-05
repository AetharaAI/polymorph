# Autonomous Control-Plane Roadmap

This roadmap is no longer about generic feature growth. It is about increasing trusted autonomous work capacity for AetherPro and Syndicate.

## Operating Standard

If a roadmap item does not increase one of these, it is not current priority work:
- inbound work capture
- outbound action execution
- durable task continuity
- approval-safe autonomy
- revenue/work matching on Syndicate

## Current Status Snapshot

Foundation already present in PolyMorph:
- full harness loop with tools, artifacts, memory hooks, and provider failover
- voice lane working in the browser
- channel control plane scaffolded in `mini-agent/backend/channels/`
- first Telegram webhook bridge implemented in the active runtime

Current blockers to real operational autonomy:
- only Telegram exists in the active channel runtime
- no queue/retry/receipt layer for channel actions
- no WhatsApp adapter in the active runtime
- no Polymorph-native Syndicate adapter yet
- no canonical cross-channel action ledger / approval ledger

## Priority Order

### 1. Message Adapter Layer

Why first:
- This is the ingress and egress layer for real work.
- Without stable adapters, the harness remains trapped in the web UI.

Current state:
- `mini-agent/backend/channels/base.py`
- `mini-agent/backend/channels/manager.py`
- `mini-agent/backend/channels/telegram.py`
- `mini-agent/backend/channels/dispatcher.py`
- `mini-agent/backend/api/channels.py`
- Telegram webhook sync route exists.
- Telegram inbound webhook route exists.
- Inbound Telegram text is normalized into a PolyMorph session id and routed through `run_agent(...)`.
- Replies are sent back through the Telegram Bot API.
- Connections panel already stores runtime/channel config.

What is not done:
- no WhatsApp adapter in the active runtime
- no queue/worker for retries or backpressure
- no canonical outbound receipt record
- no media/file attachment handling in the channel turn path
- no operator approval gate for outbound side effects triggered from channel turns
- no channel-level health/latency/event audit beyond basic request handling

Start here first:
1. Stabilize Telegram as the reference adapter contract.
2. Add a channel event ledger for inbound, outbound, ignored, failed, and retried messages.
3. Add receipt ids and idempotency keys to outbound sends.
4. Add attachment/media normalization so channel turns can carry images/files cleanly.

Short build plan:
- define a channel-agnostic event schema
- persist channel turn receipts with session correlation
- add retry-safe outbound execution wrapper
- expose channel health and last-delivery state in API/UI
- only then clone the contract for WhatsApp

### 2. Syndicate Marketplace Adapter

Why second:
- Syndicate is the work market.
- If agents are expected to find work, post capabilities, and act autonomously, Syndicate needs a first-class adapter instead of manual browsing.

Current state:
- no Polymorph-native Syndicate adapter exists in this repo yet
- live product direction is visible from the current site:
  - browse listings
  - post listings
  - actor types: human, agent, company
  - post types: offering, looking for

What is not done:
- no `browse_listings`, `create_listing`, `update_listing`, `apply_to_listing`, or `match_listing` tools
- no machine-readable contract between PolyMorph and Syndicate
- no posting/apply flow from channel-originated work

Start second:
1. Define the adapter contract before implementation.
2. Prefer direct API integration if the Syndicate repo exposes one.
3. If not, use a browser automation fallback temporarily, but keep the contract API-shaped.

Short build plan:
- draft the Syndicate action surface
- map listing fields into a stable tool schema
- support draft-first posting and explicit submit
- attach artifacts/proof-of-work back to listings
- add session-to-listing correlation ids

### 3. Action Ledger And Approval Gate

Why third:
- Autonomous work without a durable action ledger becomes un-auditable and unsafe.
- OpenClaw-like usefulness depends on reliable memory of intent, approval, execution, and receipts.

Current state:
- session state, artifacts, replay logs, and memory backends exist
- there is no single canonical ledger for outbound actions across channels/platforms

What is not done:
- no unified `action_intent`, `approval_state`, `execution_receipt`, `rollback_status` records
- no idempotent action replay protection across channel retries
- no operator-visible approval queue for side effects

Start third:
1. Define the canonical action record.
2. Make all external side effects pass through it.
3. Store receipts before broadening adapters.

Short build plan:
- create a normalized action schema
- require approval metadata for sensitive actions
- store execution receipts and retry state
- expose approval/execution state in UI and session history

### 4. Outbound Notification And Follow-Up Layer

Why fourth:
- Once work is discovered or completed, the system needs a way to follow up across the channels people actually use.

Current state:
- Telegram can respond to inbound messages in the active runtime
- donor `mcas/` notes reference WhatsApp/Discord concepts, but those are not active here

What is not done:
- no WhatsApp adapter in the active runtime
- no channel-agnostic outbound notification planner
- no escalation/fallback path when a delivery fails

Start fourth:
1. Build WhatsApp only after Telegram contract + action ledger are stable.
2. Keep the outbound layer channel-agnostic so Syndicate/task events can fan out cleanly.

Short build plan:
- add outbound notification abstraction
- implement WhatsApp against the same adapter contract
- support fallback routing and delivery receipts
- tie notifications to task/action ids, not raw chat text

### 5. Opportunity Matching And Agent Self-Posting

Why fifth:
- This is where the system starts behaving like an economy participant instead of a reactive assistant.

Current state:
- no current matcher in this repo
- no automatic capability-to-task ranking for Syndicate

What is not done:
- no capability profile registry for agents
- no listing-to-agent scoring
- no draft proposal generation tied to real tool/action capability

Start fifth:
1. Define agent capability cards from real tools and verified behaviors.
2. Rank listings/work requests against those cards.
3. Generate draft responses with approval-safe submission.

Short build plan:
- create machine-readable agent capability profiles
- rank opportunities against proven capabilities
- draft proposals or listing posts automatically
- feed accepted work back into the action ledger

## Immediate Build Sequence

1. Finish the message adapter layer as a production contract, not a Telegram demo.
2. Define the Syndicate adapter contract and tool surface.
3. Build the action ledger + approval gate underneath all external actions.
4. Expand outbound delivery from Telegram to WhatsApp only after receipts and retries exist.
5. Add opportunity matching and agent self-posting last, on top of the stable substrate.

## Not Current Priority

These can wait until the list above is real:
- random new social connectors
- cosmetic profile systems
- benchmark polish that does not improve autonomous execution
- speculative agent personas not tied to platform work

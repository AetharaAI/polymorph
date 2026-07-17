# BUILD_PLAN

## Goal
Restore PolyMorph as a Triad Zero-local operational harness with:

- no live OVHcloud runtime dependencies
- a distinct PolyMorph identity and namespace boundary
- OpenRouter as the temporary inference transport while preserving provider/model configurability
- a recoverable local memory substrate across Redis, MongoDB, PostgreSQL, and Qdrant
- redacted diagnostics and readiness reporting for Passport integration

## Milestones
1. Inspect runtime truth
   - read canonical project-state files, runtime code, compose files, env examples, and memory code
   - inspect `mongo-mem/` to classify bootstrap artifacts versus live runtime code
   - inspect active local Docker containers, networks, ports, and reachable services
   - enumerate active and historical OVH references plus current secret-bearing config risks
2. Patch runtime and config
   - separate logical model route from active OpenRouter transport model
   - wire backend runtime to discovered Triad Zero services and remove active OVH endpoints
   - establish explicit PolyMorph identity/namespace values
   - add idempotent memory bootstrap for Mongo/Postgres and a local Qdrant fallback if Triad Zero does not already expose one
3. Add diagnostics and documentation
   - create a `polymorph-doctor` executable with redacted checks and disposable round trips
   - update safe env examples and runtime docs
   - write migration audit, memory topology, runtime config, and Passport readiness docs
   - update canonical project-state summaries where runtime truth changed
4. Verify
   - render compose config
   - run syntax/config checks
   - run doctor and service round trips
   - prove no active OVH endpoint remains in runtime configuration

## Dependencies And Assumptions
- Active runtime remains `mini-agent/`.
- Triad Zero local services discovered so far: PostgreSQL, MongoDB, Redis, NATS, RedWatch, CollabFabric.
- No local Qdrant service is currently present in the discovered Triad Zero Docker topology, so a local fallback may be required.
- No local GPU-backed model server is running; OpenRouter is the temporary live inference path.
- Local secret-bearing `.env` files are untracked and must stay unprinted/uncommitted.

## Test Strategy And Acceptance Checks
- Backend/provider metadata reports:
  - logical default route `grm2.6-plus`
  - active provider transport `OpenRouter`
  - actual active model identifier from env
- Compose backend can reach Triad Zero local services without using old OVH IPs.
- Memory bootstrap is idempotent and does not seed stale `aether-max` or OVH facts.
- `scripts/polymorph-doctor` reports redacted PASS/OPTIONAL/DEGRADED/FAIL statuses.
- Disposable round trips succeed for Redis, MongoDB, PostgreSQL, and Qdrant when configured.
- Documentation reflects actual findings and changed files.

## Risks
- Local infra credentials/users may not match historical assumptions from repo docs.
- Qdrant may require a local fallback because it is not currently part of discovered Triad Zero services.
- Provider/model routing changes must stay backward-compatible with existing OpenAI-compatible flows.
- Updating canonical state docs must not overstate readiness if one or more mandatory checks still fail.

## Rollback
- Keep changes additive and idempotent.
- Restrict runtime changes to configuration, diagnostics, and bootstrap helpers.
- Avoid destructive data changes; use disposable namespaces/tables/collections for verification.
- If any new fallback service causes issues, stop it and revert compose/env/docs patches.

## Current Slice: Transcript UX Tightening

### Goal
Refine the PolyMorph transcript so the agent loop stays intact while:

- completed tool-call cards auto-collapse but remain manually expandable
- the final assistant response renders in true stream order and through markdown
- the viewport anchors to the start of the final response instead of the bottom-most tool output
- manual user scrolling disables forced follow until the user returns to the final-response region
- tool cards expose a quick-copy affordance for call/result payloads

### Milestones
1. Inspect current transcript flow
   - verify event ordering from chat SSE
   - inspect message, tool-call, and thinking render paths
   - confirm artifact persistence already survives reload/session restore
2. Patch transcript rendering
   - render assistant content blocks in original order instead of type-grouped order
   - wire assistant text through a markdown renderer with GFM support
   - auto-collapse completed/error tool cards while keeping active calls expanded
3. Patch viewport behavior
   - add final-response anchor detection
   - follow the final response while streaming
   - stop forced follow on manual scroll-away and resume only when the user returns
4. Verify
   - run frontend lint/build checks
   - confirm no regression to tool-call visibility, thinking traces, or artifact sidebar behavior

### Acceptance Checks
- Running tool calls render expanded.
- Completed tool calls collapse automatically after their result lands.
- Final assistant text appears after the completed tool activity when that is the actual event order.
- Final assistant text renders headings, lists, tables, code fences, and links as markdown.
- Transcript auto-scroll targets the final answer start, not the bottom of tool output.
- Manual upward scrolling during answer streaming disables forced follow until the user returns.

## Current Slice: Delegated Vision Lane

### Goal
Add an env-configurable visual-perceptor route so text-first models stay cheap while uploaded images can still be inspected honestly and injected back into the main reasoning lane.

### Milestones
1. Inspect current multimodal and file paths
   - verify image uploads already persist and preview correctly
   - verify how the direct-audio sidecar swaps provider routes today
   - inventory locally available OCR/vision assets on this machine
2. Patch backend routing
   - add a dedicated delegated-vision provider configuration path
   - add `inspect_image` as a first-class harness tool
   - auto-inject structured visual observations into the user turn when delegated vision is active
3. Patch frontend visibility
   - show image-aware attachment preview in the composer
   - expose a visible status badge for vision availability and route mode
4. Verify
   - run frontend build/type checks
   - run backend syntax checks
   - confirm text-only models can reason over delegated visual observation without claiming native image sight

### Acceptance Checks
- Vision routing is configurable through env values without UI changes.
- Text-only primary models can still answer image questions when the delegated vision lane is configured.
- `inspect_image` returns structured observation data instead of pretending the main model saw the image directly.
- Status bar exposes `VISION: NATIVE`, `VISION: DELEGATED`, or `VISION: UNAVAILABLE`.
- Uploaded images can be previewed from the composer/attachment flow before send.

## Current Slice: Execution Boundary Truth Alignment

### Goal
Harden PolyMorph's execution-boundary contract so the runtime, prompt, tools, health surfaces, and UI all report the same truth about:

- whether Poly is contained to a session workspace, brokered to container-visible paths, or effectively host-elevated
- whether HTTP egress is available from tools versus shell
- which workspace/session root is actually in scope for the current run
- what the agent should and should not infer from blocked filesystem probes

### Milestones
1. Centralize boundary truth
   - create one canonical backend execution-boundary builder
   - derive stable modes: `contained`, `brokered`, `host_elevated`
   - include session-aware workspace metadata and structured egress fields
2. Patch boundary consumers
   - switch shell/project tools and health/status endpoints to the shared contract
   - update prompt guidance to the canonical modes and structured egress object
   - keep existing Connections UI controls intact while making their output match runtime truth
3. Patch frontend scope reporting
   - update types for the canonical execution-boundary payload
   - render truthful scope labels in the status bar
4. Add minimal canon/import scaffolding
   - add a lightweight import manifest to anchor repo-local truth sources and stop topology drift
   - update state/runtime docs only where operational truth changed
5. Verify
   - syntax-check touched backend files
   - build the frontend
   - hit health endpoints and confirm the new payload shape

### Acceptance Checks
- `get_harness_status`, `/api/health`, and `/api/health/diagnostics` expose the same canonical execution-boundary schema.
- `scope_mode` no longer uses the ambiguous old `workspace_only/container_access` labels.
- The agent prompt explicitly warns when inspection is workspace-contained.
- The status bar reflects the canonical boundary mode without implying broader reach than the container actually has.
- A minimal import/canon manifest exists and points at the current truth package/docs.

## Current Slice: Delegated Vision Provider Capture

### Goal
Fix the delegated-vision response capture defect in the OpenAI-compatible provider path without changing the working OCR-first routing behavior.

### Milestones
1. Trace the concrete provider path
   - document `inspect_visual` → `get_vision_provider()` → `OpenAICompatProvider.generate()`
   - identify the exact normalization step that converts provider output into `LLMResponse.content`
2. Patch provider normalization
   - support useful content from string, block-array, and `output_text` response shapes
   - preserve reasoning/refusal evidence where present
   - attach sanitized diagnostics only when normalized content is empty
3. Patch delegated-vision truth handling
   - return a typed `empty_provider_response` failure for vision when the provider yields no usable normalized output
   - keep `structured`, `text`, Fusion verification, and uncertainty behavior intact for usable responses
4. Verify
   - add provider/vision tests for the observed response shapes
   - rebuild only the backend
   - upload a real screenshot through the existing file path and re-run delegated vision end-to-end

### Acceptance Checks
- Delegated vision no longer silently succeeds with empty `summary`/`visible_text`.
- Empty normalized provider responses produce a typed, observable failure envelope with sanitized diagnostics.
- Useful provider output is captured from the actual response shape returned by the installed OpenAI-compatible path.
- Existing OCR-first routing and UI behavior remain unchanged.

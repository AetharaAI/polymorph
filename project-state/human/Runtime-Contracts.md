# Runtime Contracts

## Provider Contract

Normalized provider interface:
- file: `mini-agent/backend/agent/providers/base.py`
- method: `generate(system, tools, messages, max_tokens, temperature, enable_thinking?, on_stream_event)`

Current provider implementations:
- `anthropic_provider.py`
- `openai_provider.py`
- `openai_compat_provider.py`
- `failover_provider.py`

Provider selection contract:
- `AGENT_PROVIDER=openai` means direct OpenAI adapter
- `AGENT_PROVIDER=openai_compat` means the unified OpenAI-compatible gateway adapter
- `AGENT_PROVIDER=anthropic` means Anthropic adapter
- fallback order is:
  - explicit `AGENT_FALLBACK_*` target first, if configured
  - legacy LiteLLM model aliases may seed same-gateway fallback models only when no explicit fallback is configured, or when `AGENT_ENABLE_IMPLICIT_LITELLM_FALLBACKS=true`
- fallback is only used if the primary provider errors or returns an empty payload
- context-window errors are handled separately from generic provider failures:
  - if upstream exposes token counts, the harness retries the same provider with a reduced output budget
  - context-window failures must not silently hop across providers
  - context-window failures must not silently degrade into a no-tool fallback response
  - when an effective context window is known or inferred, the harness preflight-clamps output budget before send
- the canonical internal OpenAI-compatible base is now `https://api.aetherpro.tech/v1`
- remote model nodes are worker backends behind that gateway, not separate client-facing API bases

Env bootstrap order:
- `mini-agent/.env`
- `mini-agent/backend/.env`
- `mini-agent/.env.polymorph`

This order is now loaded explicitly in code so backend behavior does not depend on which directory the process was launched from.

Direct OpenAI contract notes:
- `gpt-5.x` requests must use `max_completion_tokens`
- compat-only `extra_body` fields must not be sent to `api.openai.com`
- tool calls remain OpenAI-style Chat Completions tool calls
- OpenAI-compatible streaming requests share the same context-window retry path as non-stream requests.
- Qwen3/Qwen3.5 production/direct-answer flows default to `extra_body.chat_template_kwargs.enable_thinking=false`
- explicit reasoning mode may opt back into Qwen thinking on a per-request basis
- OpenAI-compatible normalization now also:
  - strips visible `<think>` content from answer text and stores it as `thinking`
  - recovers pseudo tool-call JSON into real tool calls when the named tool is actually registered
  - suppresses visible `Step 1 / Step 2 / Next Actions` planning scaffolds when they are just tool-call leakage
  - buffers raw compat text until final normalization so leaked planning text does not hit the UI first

Temporal context contract:
- every agent run prepends a structured temporal block into the effective system prompt
- the temporal block is now compacted to reduce prompt overhead on smaller-context routers
- the temporal block is authoritative for:
  - current UTC time
  - current local time
  - resolved timezone
  - unix timestamp
  - session creation time
  - elapsed time since prior user turn
  - elapsed time since prior agent run
- session state persists:
  - `last_user_message_at`
  - `last_agent_run_at`
- relative terms like `today`, `latest`, `now`, `yesterday`, and `tomorrow` should be reasoned from this block, not guessed by the model

## API Contract

Primary backend routes are served from the FastAPI backend in `mini-agent/backend/`.

Important routes:
- `POST /api/chat`
- `GET /api/health`
- `GET /api/health/diagnostics`
- `GET /api/connections`
- `POST /api/connections/test`
- `POST /api/connections/save`
- `GET /api/channels`
- `GET /api/channels/{channel_id}`
- `POST /api/channels/telegram/sync-webhook`
- `POST /api/channels/telegram/webhook`
- `POST /api/audio/transcribe`
- `POST /api/audio/stream/start`
- `POST /api/voice/turn`
- `GET /api/voice/config`

Chat request multimodal extensions:
- `POST /api/chat` accepts optional:
  - `audio_input`
    - `{ data, format, filename?, mime_type?, duration_ms? }`
  - `audio_url`
    - `{ url, filename?, mime_type?, duration_ms? }`
- Direct audio chat path is intended for multimodal models and must not use ASR as an intermediate stage.
- Microphone-originated direct audio turns are routed to a dedicated multimodal provider/model when configured.

Live ASR microphone contract:
- `POST /api/audio/stream/start` bootstraps a live ASR session using server-side ASR credentials.
- The frontend then streams mono PCM16 16 kHz frames directly to the returned websocket URL.
- The UI may render `partial_transcript` events live, but only `final_transcript` should be committed into the composer or voice turn.
- If the ASR gateway is in optional-auth mode, the harness should omit fake/stale bearer auth rather than failing the stream bootstrap with `401 Invalid bearer token`.

## Tool Contract

Tool registry:
- `mini-agent/backend/agent/tools/registry.py`

Dispatch model:
- tools are registered centrally
- execution is normalized through one dispatch layer
- long-running project work uses session workspaces under `workspaces/<session_id>/`
- the model only receives a per-turn selected subset of tools instead of the full registry on every request
- harness self-description metadata is prompt-optional and is no longer injected by default
- the prompt-facing tool bootstrap source is `mini-agent/backend/TOOLS.md`
- dynamic tools are loaded through the `read_tool_schema` meta-tool and then cached in session state under `loaded_tool_schemas`
- tool planning is now explicitly internal-only; the prompt contract forbids visible pseudo tool calls and visible chain-of-thought
- message-history compaction now budgets against the effective context window for the active iteration instead of relying only on a global large char cap

## Memory Contract

The harness is designed to use:
- Redis
- MongoDB
- Qdrant
- Postgres

MongoDB contract:
- DB name stays fixed at `aether_memory`
- namespace separation is document/key scoped, not database scoped
- bootstrap file: `mongo-mem/aether-init.js`
- `episodes` inserts must include at least:
  - `agent_id`
  - `session_id`
  - `summary`
  - `embedding`
  - `created_at`

Namespace behavior:
- Redis keys are namespaced
- Mongo documents include `namespace`
- Postgres may use schema-level separation
- Qdrant collection policy is independent of Mongo DB naming

## Direct Audio Routing Contract

Dedicated multimodal audio provider selection:
- `DIRECT_AUDIO_PROVIDER`
- `DIRECT_AUDIO_BASE_URL`
- `DIRECT_AUDIO_API_KEY`
- `DIRECT_AUDIO_MODEL`

Phi-4 convenience aliases:
- `PHI_4_INSTRUCT_MODEL_BASE_URL`
- `PHI_4_INSTRUCT_API_KEY`
- `PHI_4_INSTRUCT_MODEL_NAME`

Selection behavior:
- if a chat turn includes `audio_input` or `audio_url`, the runner prefers the dedicated multimodal audio provider
- if no dedicated multimodal provider is configured, the run fails fast with a clear configuration error
- text-only turns continue to use the normal provider/fallback chain

Persistence behavior:
- raw base64 audio and direct data URLs are not persisted into long-term memory
- only audio metadata placeholders are stored in session history and memory backends

## Voice Mode Contract

The active internal voice lane is now:

- live ASR final transcript
- separate voice model text generation
- realtime TTS stream as the primary speech path
- HTTP synth as fallback

`GET /api/voice/config` exposes:

- voice-model provider/model
- realtime TTS config status
- realtime TTS base/model
- available Kokoro preset voices

`POST /api/voice/turn` now returns:

- `assistant_text`
- `provider`
- `model`
- `voice_id`
- `tts_transport`
- optionally:
  - `audio_url`
  - `mime_type`
  - `tts_stream_session_id`
  - `tts_stream_ws_url`
  - `tts_stream_http_base_url`
  - `tts_stream_model_requested`
  - `tts_stream_model_used`
  - `tts_stream_fallback_used`
  - `tts_stream_runtime`

Realtime TTS rules:

- browser sends `text_chunk` frames, then `text_complete`, then `end_stream`
- gateway returns `audio_chunk`, `final_audio`, and `error`
- browser playback should play chunk audio immediately and preserve final artifact URL when available
- model-to-model stream orchestration is not part of this contract yet

## Fleet Operator Contract

Canonical internal operator inventory lives in `fleet-inventory/` and is loaded by:
- `mini-agent/backend/fleet/inventory.py`
- `mini-agent/backend/fleet/manager.py`
- `mini-agent/backend/fleet/executor.py`
- `mini-agent/backend/fleet/scripts.py`

Authoritative fleet inputs:
- `fleet-inventory/model-inventory.yaml`
- `fleet-inventory/operator-manifest.yaml`
- `fleet-inventory/poly-tailscale-nodes.yaml`
- `fleet-inventory/fleet-storage-3-nodes.yaml`

Contract rules:
- do not assume uniform mount layouts across nodes
- do not fabricate undocumented directory trees
- preserve path mismatches between the high-level Tailscale map and the detailed inventory
- remote execution must stay inside manifest-approved paths
- destructive stack actions require explicit confirmation even in internal operator mode

Execution model:
- helper scripts are sourced from `fleet-inventory/scripts/`
- scripts are executed remotely over SSH/Tailscale by streaming the local helper content to the target node
- dry-run mode returns command previews without remote mutation

## Channel Control Contract

Channel control plane modules live in:
- `mini-agent/backend/channels/base.py`
- `mini-agent/backend/channels/manager.py`
- `mini-agent/backend/channels/dispatcher.py`
- `mini-agent/backend/channels/telegram.py`
- `mini-agent/backend/api/channels.py`

Contract rules:
- `mcas/` is donor/reference material only and must not become the active runtime
- channel adapters must route into the existing Polymorph backend/session model
- provider/model routing stays in the normal Polymorph provider layer
- the existing connections panel is the configuration surface for channel runtime and Telegram settings
- the first active Telegram path is webhook-based: sync webhook -> receive update -> normalize -> run agent -> reply via Bot API
- model env rationalization is a separate follow-on task, not part of the initial channel pass

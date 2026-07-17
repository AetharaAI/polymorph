# PHASE 8 REPORT

## Slice
Delegated vision provider capture hardening

## Date
2026-07-17T03:51:49Z

## Goal
Stop delegated vision from silently succeeding with an empty observation when the OpenAI-compatible provider returns no usable normalized content.

## Root Cause
The delegated vision lane calls:

- `backend.agent.tools.vision_ops.inspect_visual`
- `backend.agent.providers.factory.get_vision_provider()`
- `backend.agent.providers.openai_compat_provider.OpenAICompatProvider.generate()`

The live `xiaomi/mimo-v2.5` request on Friday, July 17, 2026 returned HTTP `200` but produced no normalized blocks:

- `choices_count=1`
- `finish_reason=length`
- `message.content=None`
- `output_text` absent
- `normalized_block_count=0`

Prior to this slice, the harness surfaced that outcome as an empty successful observation (`summary=""`, `visible_text=[]`), which looked like a parser problem downstream. The real defect boundary was provider normalization plus empty-response truth handling.

## Files Changed
- `BUILD_PLAN.md`
- `mini-agent/backend/agent/providers/base.py`
- `mini-agent/backend/agent/providers/openai_compat_provider.py`
- `mini-agent/backend/agent/tools/vision_ops.py`
- `mini-agent/backend/tests/test_openai_compat_provider_capture.py`
- `PROJECT_STATE.md`
- `project-state/ai/current-state.yaml`

## What Changed
1. Added response metadata support to `LLMResponse`.
2. Extended OpenAI-compatible provider normalization to recover useful text from:
   - plain string `message.content`
   - block-array `message.content`
   - `output_text`
   - refusal text
   - object-backed message payloads
3. Added sanitized empty-response diagnostics only when normalized content is empty.
4. Changed delegated vision to return a typed:
   - `status: "error"`
   - `error_kind: "empty_provider_response"`
   instead of a fake empty successful observation.

## Tests Executed
- `python3 -m py_compile mini-agent/backend/agent/providers/base.py mini-agent/backend/agent/providers/openai_compat_provider.py mini-agent/backend/agent/tools/vision_ops.py`
- `python3 -m pytest backend/tests/test_openai_compat_provider_capture.py backend/tests/test_xml_mcp_reasoning_parser.py`

Result:
- 15 tests passed

## Live Verification
Backend rebuilt:
- `docker compose -f mini-agent/docker-compose.yml up -d --build backend`

Real screenshot uploaded through the live file API:
- session: `vision-live-2026-07-17`
- file: `Screenshot from 2026-07-08 11-23-25.png`
- uploaded `file_id`: `eeae2e627f556479`

Delegated vision invocation result:
- provider: `delegated_vision`
- model: `xiaomi/mimo-v2.5`
- request_id: `f3819dd1ae36`
- provider_response_id: `gen-1784260265-8Tzm9HkrD9s3xdsdgODu`
- http_status: `200`
- finish_reason: `length`
- usage:
  - input_tokens: `2099`
  - output_tokens: `1200`

Live result:
- typed failure returned correctly
- `error_kind: "empty_provider_response"`
- no fake empty success payload

## Before / After
Before:
- delegated vision could return:
  - `status: "ok"`
  - `summary: ""`
  - `visible_text: []`
  - no trustworthy reason for the emptiness

After:
- delegated vision now either:
  - captures usable normalized content from supported response shapes, or
  - returns a typed `empty_provider_response` with provider/model/request diagnostics

Observed normalized payload shape after this slice:
- `status: "error"`
- `error_kind: "empty_provider_response"`
- `diagnostics.request_id: "f3819dd1ae36"`
- `diagnostics.provider_response_id: "gen-1784260265-8Tzm9HkrD9s3xdsdgODu"`
- `diagnostics.normalized_block_count: 0`
- `diagnostics.raw_message_content_type: "NoneType"`

## Remaining Uncertainty
- This slice proves truthful failure handling for the live MiMo/OpenRouter response path.
- It does not yet prove why the upstream provider returned no usable content on this screenshot.
- The likely remaining question is upstream/provider behavior under:
  - `enable_thinking=false`
  - `max_tokens=1200`
  - this exact screenshot/input shape

## Receipt Status
- No live RedWatch-compatible implementation receipt emitter exists in this runtime path yet.
- This phase report is the canonical evidence record for the slice.

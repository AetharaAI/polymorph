# PHASE 12 REPORT

## Scope

This phase normalized OpenAI-compatible model outputs so smaller self-hosted models can be benchmarked inside PolyMorph without leaking tool-planning scaffolds or `<think>` reasoning text into the visible answer.

## What Was Changed

- Tightened the active system prompt in:
  - `mini-agent/backend/prompts/system_prompt.md`
- Tightened the tool bootstrap manifest guidance in:
  - `mini-agent/backend/TOOLS.md`
- Normalized OpenAI-compatible responses in:
  - `mini-agent/backend/agent/providers/openai_compat_provider.py`

## Behavior Changes

- Visible tool-planning text is now treated as a harness bug, not normal assistant output.
- If an OpenAI-compatible model emits:
  - `<think> ... </think>` blocks in `content`
  - pseudo tool-call JSON like `{ "name": "web_search", "arguments": {...} }`
  - planning scaffolds such as `Step 1`, `Step 2`, `Next Actions`
  the provider now normalizes that output before it reaches the chat UI.

- Normalization rules:
  - `<think> ... </think>` is stripped out of visible answer text and captured as `thinking`
  - pseudo tool-call JSON is converted into a real `tool_use` block when the tool name matches an active registered tool
  - planning scaffolds attached to a recovered tool call are suppressed from visible assistant text
  - OpenAI-compatible text deltas are buffered until final normalization instead of being streamed raw into the UI

## Why

The failure pattern from live Qwen3.5 testing was not just “bad model quality.” The harness was allowing model-specific planning leakage to hit the frontend as visible text, which makes baseline evaluation noisy and misleading.

This phase makes the harness stricter:

- internal reasoning stays internal
- tool plans become real tool calls when recoverable
- benchmarking quality reflects the model more than the harness quirks

## Verification

Passed:

- `python3 -m compileall mini-agent/backend/agent/providers/openai_compat_provider.py mini-agent/backend/agent/runner.py mini-agent/backend/agent/tools/manifest.py`
- Synthetic provider normalization test:
  - input contained `<think>internal reasoning here</think>`
  - input contained visible planning scaffold and pseudo `web_search` JSON
  - output normalized to:
    - one `thinking` block
    - one real `tool_use` block for `web_search`
    - no visible planning text
- Synthetic `<think>` separation test:
  - input `<think>secret chain</think>\nFinal answer.`
  - output normalized to:
    - one `thinking` block
    - one visible `text` block containing only `Final answer.`

## Notes

- This phase does not change the current model/env selection itself.
- This phase is specifically about output normalization and benchmark usability for OpenAI-compatible/self-hosted models.
- If a model still behaves poorly after this patch, the remaining issue is more likely model quality or router/runtime configuration rather than visible reasoning leakage from the harness.

# PHASE 9 REPORT

## Scope

This phase fixed the active model-request budgeting blocker around self-hosted OpenAI-compatible models, specifically the case where a large prompt plus `AGENT_MAX_TOKENS=4096` could exceed an 8k context window and then misbehave in the streaming path.

## What Was Changed

- Patched `mini-agent/backend/agent/providers/openai_compat_provider.py`:
  - added a shared max-token payload setter
  - improved context-window error normalization
  - fixed streaming-mode retry behavior so a retryable context-window `400` resends the same request with a reduced output-token budget
- Patched `mini-agent/backend/agent/providers/failover_provider.py`:
  - clarified context-window failure messaging so it reports which provider lane rejected the request
- Updated project-state/runtime docs to record the new request-budget semantics and the current verified env truth

## Root Cause

There were two separate issues colliding:

1. The harness was legitimately sending `max_tokens=4096`.
2. In streaming mode, when the upstream returned a retryable context-window error, the provider computed a reduced token budget but did not resend the request. That could surface as an empty primary response and then look like fallback/model-selection confusion.

The saved LiteLLM/vLLM failure sample confirms the request shape:

- upstream context window: `8192`
- input tokens: `4097`
- requested output tokens: `4096`
- total requested: `8193`

That is a real budget collision, not random corruption.

## Behavior Change

- Retryable OpenAI-compatible context-window failures now stay on the same provider/model and reduce the output-token budget before retrying.
- Context-window failures no longer silently degrade into cross-provider failover behavior.
- The current live env stack resolves:
  - primary: `minicpm-v`
  - distinct fallback: none currently resolved

The last point is current config truth, not a provider bug: the configured fallback presently dedupes to the same router/model as primary.

## Verification

Passed:

- `python3 -m compileall mini-agent/backend/agent/providers/openai_compat_provider.py mini-agent/backend/agent/providers/failover_provider.py mini-agent/backend/agent/providers/factory.py mini-agent/backend/config/bootstrap.py mini-agent/backend/agent/runner.py mini-agent/backend/main.py mini-agent/backend/memory/service.py`
- Verified the exact LiteLLM-style context-window error now computes `4079` as the retry output-token budget.
- Verified the streaming provider path now makes two requests in the retry case:
  - first request with `max_tokens=4096`
  - second request with `max_tokens=4079`
- Verified the current env stack resolves provider metadata to:
  - primary: `openai_compat / minicpm-v`
  - fallbacks: none currently distinct

## Notes

- This phase intentionally did not rewrite local `.env` files.
- If you want `vulnllm-r-7b` to be the real fallback right now, that is a live env/config change, not another provider-code fix.

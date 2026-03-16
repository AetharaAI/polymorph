# PHASE 8 REPORT

## Scope

This phase fixed the primary/fallback model-selection path so the backend no longer depends on launch-directory env behavior and no longer silently adds extra LiteLLM fallback targets when an explicit fallback is already configured.

## What Was Changed

- Added canonical env bootstrap loader:
  - `mini-agent/backend/config/bootstrap.py`
- Replaced ad hoc `load_dotenv()` calls with `load_harness_env()` in:
  - `mini-agent/backend/main.py`
  - `mini-agent/backend/agent/runner.py`
  - `mini-agent/backend/memory/service.py`
- Changed provider-chain construction in:
  - `mini-agent/backend/agent/providers/factory.py`
- Added context-window guard helpers in:
  - `mini-agent/backend/agent/providers/openai_compat_provider.py`

## Behavior Change

- Backend env load order is now fixed:
  1. `mini-agent/.env`
  2. `mini-agent/backend/.env`
  3. `mini-agent/.env.polymorph`
- If `AGENT_FALLBACK_*` is configured, that explicit fallback is the only fallback by default.
- Implicit LiteLLM fallback discovery now requires opt-in when an explicit fallback exists:
  - `AGENT_ENABLE_IMPLICIT_LITELLM_FALLBACKS=true`

## Verification

Passed:

- `python3 -m compileall mini-agent/backend/config mini-agent/backend/agent/providers mini-agent/backend/main.py mini-agent/backend/agent/runner.py mini-agent/backend/memory/service.py`
- Verified effective provider metadata under the current env stack resolves to:
  - primary: `minicpm-v` on `https://api.aetherpro.tech/v1`
  - explicit fallback: `vulnllm-r-7b` on `https://api.aetherpro.tech/v1`
- Verified the provider chain now contains exactly one fallback for the active configuration.

## Notes

- The `vulnllm-vllm-backend-logs.md` trace also showed a real context-window failure on the 4k-class fallback path. The provider now has a context-error parser in place, but if the prompt itself is too large for the model window, it will still fail correctly rather than fabricating a result.
- This phase intentionally did not rewrite local `.env` values.

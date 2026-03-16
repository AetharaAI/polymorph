Yep. This is the real unlock.

You no longer have “gateway 1 and gateway 2 and maybe this box maybe that box.”
You now have **one control plane** and many workers behind it.

Here’s the runbook first, then the Codex prompt.

# Unified Gateway Runbook

## What changed

AetherPro now uses **one unified LiteLLM gateway** as the single API entrypoint:

```text
https://api.aetherpro.tech/v1
```

All client traffic should go to that one base URL. Model routing happens behind the gateway.

## Current architecture

Client/app/harness flow:

```text
Client / Polymorph / tools
  -> api.aetherpro.tech/v1
  -> central LiteLLM gateway
  -> routed to local or remote model backend
  -> response returned through the same gateway
```

## Verified working state

Verified end to end:

* central LiteLLM gateway can route to remote backends over Tailscale
* remote `qwen3.5-122` backend on the L40S-180 is reachable from inside the central LiteLLM container
* gateway completion requests successfully route to the remote 122B model
* direct-output mode works correctly when thinking is disabled
* reasoning mode works, but will consume the token budget in `reasoning_content` unless explicitly disabled or given a larger budget

## Canonical API base

Use this everywhere going forward:

```text
https://api.aetherpro.tech/v1
```

Do not target old per-node LiteLLM instances anymore.

## Canonical model routing rule

Applications should specify only:

* the unified API base
* the gateway API key
* the desired model name

Example model names currently exposed by the gateway include things like:

* `minicpm-v`
* `qwen3.5-35b`
* `qwen3.5-122`
* `qwen3.5-9b`
* `omnicoder`
* `devstral-123b`
* `qwen3.5-4b`
* `qwen3.5-2b`
* `qwen3.5-9b-h`
* `jan-code-4b`
* `nanbeige4-3b-thinking`
* `redqwen-vl`
* `vulnllm-r-7b`
* `phi-4-instruct`

## Critical Qwen3.5 behavior

Qwen3 / Qwen3.5 reasoning-family models think by default.

If you do **not** disable thinking, short requests may return:

* `content: null`
* `reasoning_content: ...`
* `finish_reason: "length"`

This is expected behavior for reasoning-enabled mode with a small token budget.

## Production rule

For direct production answers, disable thinking on Qwen3.5 family models by sending:

```json
"extra_body": {
  "chat_template_kwargs": {
    "enable_thinking": false
  }
}
```

## Reasoning rule

If you want deliberate reasoning traces:

* leave thinking enabled
* use a much larger token budget
* expect `reasoning_content`
* optionally normalize or suppress reasoning before rendering to end users

## Minimal validated request pattern

Direct-output request:

```json
{
  "model": "qwen3.5-122",
  "messages": [
    {"role": "system", "content": "Return exactly READY."},
    {"role": "user", "content": "READY"}
  ],
  "temperature": 0,
  "max_tokens": 16,
  "extra_body": {
    "chat_template_kwargs": {
      "enable_thinking": false
    }
  }
}
```

This has been validated successfully through the unified gateway.

## Operational guidance

1. All harnesses and internal apps should point to the unified gateway.
2. Remote model nodes should be treated as workers behind the gateway.
3. Routing logic should choose the smallest capable model for the task.
4. Large models should be reserved for tasks that justify their cost and latency.
5. Qwen reasoning-family models must explicitly set thinking mode based on task intent.

## Immediate implications

This unified design now supports:

* one API surface for all internal and external consumers
* adding hosted models and external provider models into the same gateway
* routing by task type instead of hardcoding per-node URLs
* future deterministic fleet-manager orchestration behind one control plane

---

---



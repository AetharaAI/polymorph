# Qwen3.5 Runner Runbook

## Purpose

Known-good local runner definition for `qwen3.5-35b` on `L40S-90`.

This runner is the stable local fallback model for the harness provider chain.

## Served Model Contract

- Served model name: `qwen3.5-35b`
- OpenAI-compatible route: `/v1/chat/completions`
- Typical external router target: `https://api.aetherpro.tech/v1`

## Operational Role

- Local fallback for the harness when direct vendor calls fail
- Benchmark baseline for internal model evaluations
- High-availability local reasoning path

## Operational Checks

1. `docker compose up -d`
2. `docker compose logs -f`
3. Verify `/v1/chat/completions` accepts normal chat requests
4. Confirm router registration still maps to the expected served model name

## Troubleshooting

- If the harness unexpectedly lands on this model, inspect env precedence and runtime overrides.
- If multimodal fields are ignored, that is expected for text-focused fallback usage unless the runner has explicit multimodal support configured.

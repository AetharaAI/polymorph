## Model Runners

This directory tracks known-good model runner definitions by VM/layout so runner
state can be versioned alongside the harness.

### Current Tracked Layouts

- `L40S-90/run-model/qwen3.5/`
  - local fallback reasoning runner
  - includes `docker-compose.yml` and `runbook.md`
- `L40S-90/run-model/phi4/`
  - direct multimodal runner for text/image/audio
  - includes `docker-compose.yml`, `Dockerfile.phi4`, and `runbook.md`

### Rules

1. Every runner directory should have:
   - `docker-compose.yml`
   - any custom Dockerfile or env fragments needed
   - `runbook.md`
2. `runbook.md` should capture:
   - served model name
   - route contract
   - startup verification steps
   - known caveats
3. The master index should stay brief and only point to known-good runners.

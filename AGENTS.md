# Repo Operating Rules

This repository uses the `project-state/` package as the canonical state layer.

Read first:
- `PROJECT_STATE.md`
- `project-state/ai/manifest.yaml`
- `project-state/ai/current-state.yaml`
- `project-state/ai/runtime-contracts.yaml`
- `project-state/ai/repo-map.yaml`

Then use:
- `project-state/human/Architecture-Overview.md`
- `project-state/human/Runtime-Contracts.md`
- `project-state/human/Changelog.md`
- `mini-agent/docs/Autonomous-Control-Plane-Roadmap.md`

Implementation-specific harness rules still live in:
- `mini-agent/backend/AGENTS.md`

Current priority for autonomous work:
- treat PolyMorph as an operational asset, not a demo harness
- prioritize the message adapter layer first
- treat Syndicate as the first platform-specific autonomy target after adapters
- prefer integrations that increase trusted autonomous work capacity over generic benchmark fluff

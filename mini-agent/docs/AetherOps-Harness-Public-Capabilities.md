# AetherOps Agentic Harness
## Public Capabilities & Use Cases

## What It Is
AetherOps Agentic Harness is a model-agnostic AI operator console that combines:
- Long-form reasoning
- Tool calling
- File workflows
- Multi-turn autonomous execution
- Optional memory and voice services

It is designed for people who want outcomes, not demos.

## Core Capabilities

### 1) Autonomous Multi-Turn Work
- Plans across multiple tool calls
- Revises strategy when tool results are weak
- Continues until completion criteria or safety limits are reached
- Optional plan-approval gate for project builds (manual or auto mode)

### 2) Evidence-First Research
- Built-in web search + optional secondary search path
- Cross-check behavior for high-impact claims
- Explicit uncertainty when evidence is incomplete

### 3) Artifact Production
- Generates reports, checklists, briefs, CSVs, and markdown outputs
- Stores outputs as downloadable artifacts
- Inline artifact reading in right-side panel
- Batch zip download for all files in the active session

### 4) Operational Visibility
- Live reasoning/tool trace
- Context window gauge and token stats
- System health panel (runtime, memory, service state)

### 5) Voice-Input Ready
- Direct microphone capture for multimodal chat models
- Real-time waveform feedback
- ASR-backed transcript flow remains available for text-entry use cases
- Runtime config can route direct audio turns to a dedicated multimodal model
- ASR/TTS service health and runtime config controls

### 6) Connections & Secrets Control Plane
- Configure model/router, ASR/TTS, and memory backends from UI
- Test service reachability with latency
- Save runtime overrides without editing container env manually

## Built-In Toolset
- Web Search
- Tavily Search (independent verification path)
- Execute Python
- Calculator
- Read File
- List Files
- Write File
- Restricted Shell (safe diagnostics)
- Project Command Runner
- Test Runner
- HTTP Health/Smoke Checker
- Background Process Manager (start/stop/list/logs)
- Workspace Diagnostics (Python + TypeScript)
- Playwright Test Runner
- Summarizer

## Access Model (Important)
- The harness does **not** currently post to social platforms by default.
- Shell-based `curl` is GET-only in the default policy.
- If you want X/Twitter posting, add a dedicated API tool with scoped OAuth and audit controls.

## Practical Use Cases (Non-Generic)

### Use Case A: Partner Security Questionnaire Factory
Input:
- 100+ question enterprise security questionnaire
- Internal architecture docs and policy artifacts

Output:
- First-pass responses
- Evidence links per answer
- “needs human validation” flags for unverified claims

### Use Case B: Competitive Threat Intelligence Sprint
Input:
- Rival launch statement + 3 market reports + analyst notes

Output:
- Contradiction map (claim vs evidence)
- Revenue risk scenarios
- Priority follow-up questions for GTM and security

### Use Case C: Incident Comms + Ops Runbook Builder
Input:
- Timeline notes, logs, and initial incident summary

Output:
- Executive brief
- Technical remediation checklist
- Customer-safe status update draft
- Post-incident action tracker artifact

### Use Case D: Model Provider Bake-Off
Input:
- Same benchmark prompts across multiple model endpoints

Output:
- Side-by-side quality and reliability comparison
- Error-rate and tool-call consistency notes
- Recommendation by task class (research, ops, coding, synthesis)

### Use Case E: Founder Ops Co-Pilot
Input:
- Meetings notes, target account lists, pricing hypotheses

Output:
- Weekly operating brief
- Top risks and blockers
- Suggested experiments and decision log

## Why This Is Different
- Built for production-like work loops, not single-turn chat novelty.
- Tool execution and artifacts are first-class, observable, and persistent.
- Model provider can be swapped without rewriting the product surface.

## Packaging Strategy (Recommended)

### Base Edition
- Frontend + backend
- One model connector
- Local artifacts + session continuity

### Pro Edition
- Connections/Secrets UI
- Optional memory backends
- Voice input
- Enhanced diagnostics

### Enterprise Edition
- SSO/RBAC
- Secret manager/KMS integration
- Policy packs and approval gates
- Compliance audit exports

---

For implementation details, see:
- `docs/AetherOps-Harness-Technical-Reference.md`
- `docs/Identity-Memory-Bootstrap-Pattern.md`

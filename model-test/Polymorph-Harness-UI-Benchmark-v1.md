# Polymorph Harness UI Benchmark v1

Date: 2026-03-05
Purpose: Compare models inside your AetherOps harness UI with the same repeatable run.

## Why this benchmark
- Your two test docs verified baseline behavior:
  - model responds and states identity/tools
  - model can run `web_search` and `write_file`
- This benchmark keeps that flow but adds deterministic scoring.

## Legacy compatibility (with your older benchmark set)
This v1 maps to the style in:
- `benchmarks/Minimax-M2.5-Agent-Multi-turn-tool-test-&-Benchmark-02-28-2026.md`
- `benchmarks/aetheros-bench/MARATHON_AGENT_BENCHMARK_v1.md`
- `benchmarks/aetheros-bench/AETHER_ENDURANCE_BENCHMARK_v1.md`
- `benchmarks/aetheros-bench/AETHEROPS_CAPABILITY_GAUNTLET.md`

Category mapping for continuity:
- Tool integrity -> Tool reliability / anti-fabrication
- Deterministic accuracy -> Technical correctness
- Web evidence quality -> External verification quality
- Artifact operations -> Artifact completeness + reproducibility
- Output contract adherence -> Execution discipline / completion quality

Optional legacy continuity subscore:
- Continuity & self-correction (0-10): deduct for loops, contradiction, or unresolved failures.

## Run Protocol (per model)
1. Start a **new chat** in the harness UI.
2. Keep same tool config for every model.
3. Paste the benchmark prompt below as your first message.
4. Let it run to completion.
5. Score using the rubric.
6. Repeat on next model.

## Benchmark Prompt (paste into UI)
```text
Run "Polymorph Harness UI Benchmark v1".

Execution rules:
1) Do not ask follow-up questions unless blocked by a hard tool/runtime error.
2) Use tools when requested; do not fake tool results.
3) If a tool is unavailable, state "TOOL_UNAVAILABLE:<tool_name>" and continue with best effort.
4) Keep outputs concise and structured.

Required tasks:

Task A: Capability and truthfulness check
- Return a JSON object named `capability_report` with:
  - `agent_name`
  - `provider_or_model_guess`
  - `tools_declared` (array)
  - `tools_actually_used` (array, start empty then update at end)
  - `uncertainties` (array)
- Do not claim any tool you did not actually invoke.

Task B: Deterministic reasoning check
- Compute and report these exact items in a JSON object named `deterministic_results`:
  1) `expr_1`: 17*23 + sqrt(144)
  2) `expr_2`: ((144 / 12) * 7) - 19
  3) `sorted_desc`: sort [42, 7, 19, 7, 103, 2] descending
  4) `unique_count`: unique value count of [42, 7, 19, 7, 103, 2]
- Use `calculate` or `execute_python` if available.

Task C: Web + evidence discipline check
- Use `web_search` to find 3 results for: "NASA Earth science 2024 news release".
- Return a markdown table with columns:
  - title
  - url
  - why_relevant (max 15 words)
  - confidence (high/medium/low)
- If source quality is weak, say so explicitly.

Task D: File I/O and artifact integrity check
- Create `ui_benchmark_v1_report.md` with sections:
  - Capability Report
  - Deterministic Results
  - Web Evidence Table
  - Known Limitations
- Then read the same file back and confirm:
  - file exists
  - section headers are present
  - character count estimate

Task E: Final structured output
- Print `BENCHMARK_COMPLETE` and then output a final JSON object:
  - `status` (pass/fail)
  - `tools_actually_used`
  - `artifacts_created`
  - `deterministic_summary`
  - `web_evidence_summary`
  - `failures_or_warnings`
```

## Scoring Rubric (100 points)

1. Tool integrity (20)
- 10: No fabricated tool calls.
- 10: `tools_declared` matches observed behavior.

2. Deterministic accuracy (20)
- 5: `expr_1` correct.
- 5: `expr_2` correct.
- 5: `sorted_desc` correct.
- 5: `unique_count` correct.

3. Web evidence quality (20)
- 10: Ran `web_search` and returned 3 usable rows.
- 10: Relevance/confidence notes are coherent and uncertainty-aware.

4. Artifact operations (20)
- 10: `ui_benchmark_v1_report.md` created successfully.
- 10: Read-back validation done and reported.

5. Output contract adherence (20)
- 10: Includes `capability_report` and `deterministic_results` JSON blocks.
- 10: Ends with `BENCHMARK_COMPLETE` + required final JSON keys.

## Expected deterministic answers (for scoring)
- `expr_1` = 403
- `expr_2` = 65
- `sorted_desc` = [103, 42, 19, 7, 7, 2]
- `unique_count` = 5

## Quick score line template
Use this line after each run:

`MODEL=<name> TOTAL=<0-100> TOOL=<0-20> DET=<0-20> WEB=<0-20> FILE=<0-20> CONTRACT=<0-20> NOTES="<short note>"`

Optional extended line (legacy continuity):

`MODEL=<name> TOTAL=<0-110> TOOL=<0-20> DET=<0-20> WEB=<0-20> FILE=<0-20> CONTRACT=<0-20> CONTINUITY=<0-10> NOTES="<short note>"`

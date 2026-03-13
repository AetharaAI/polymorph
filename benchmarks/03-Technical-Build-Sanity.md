You are being benchmarked inside an agent harness.

Rules:
1. Do not guess runtime capabilities. Verify them.
2. Use execution tools honestly; do not fake results.
3. If project mode or plan approval blocks action, state that explicitly.
4. Keep outputs concise and structured.

Tasks:

A. Self-awareness
- Verify:
  - actual provider/model
  - tool count
  - whether project execution tools are available

B. Execution task
- Create a tiny sanity project artifact:
  - a TypeScript or Python hello-world style file
  - one minimal test file
- Use the appropriate write/run tools.
- If runtime dependencies are missing, report the real error.

C. Verification
- Check:
  - files exist
  - test runner/tool availability
  - whether execution succeeded

D. Artifact creation
- Save a report to `benchmark_build_sanity_report.md`

E. Final output
- End with:
  - `BENCHMARK_COMPLETE`
  - JSON:
    - `status`
    - `runtime_verified`
    - `execution_result`
    - `artifacts_created`
    - `warnings`

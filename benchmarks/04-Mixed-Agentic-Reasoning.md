You are being benchmarked inside an agent harness.

Rules:
1. Do not guess runtime capabilities. Verify first.
2. For latest information, use search and grade source quality.
3. For deterministic tasks, compute exactly.
4. Do not ask follow-up questions unless blocked by a hard error.
5. Keep outputs concise and structured.

Tasks:

A. Self-awareness
- Verify and report:
  - actual provider/model
  - exact tool count
  - memory status

B. Deterministic check
- Compute:
  - 17*23 + sqrt(144)
  - ((144 / 12) * 7) - 19
  - sort [42, 7, 19, 7, 103, 2] descending
  - unique count of [42, 7, 19, 7, 103, 2]

C. Current-info task
- Find the latest official update on one of these:
  - AI model releases
  - NVIDIA announcements
  - Open-source coding models
- Use at least one primary source.

D. Artifact creation
- Write `benchmark_mixed_reasoning_report.md`

E. Verification
- Read it back and validate structure.

F. Final output
- End with:
  - `BENCHMARK_COMPLETE`
  - JSON:
    - `status`
    - `deterministic_results`
    - `current_info_summary`
    - `tools_used`
    - `warnings`

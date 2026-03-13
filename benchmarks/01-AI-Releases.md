You are being benchmarked inside an agent harness.

Rules:
1. Do not guess runtime capabilities. Use tools if needed.
2. If asked about your provider, tools, memory, or runtime state, verify first.
3. For current events or latest releases, use web search and distinguish strong vs weak sources.
4. Do not ask follow-up questions unless blocked by a hard runtime/tool error.
5. Keep outputs concise and structured.

Tasks:

A. Self-awareness
- State:
  - actual provider/model
  - requested provider/model
  - exact tool count
  - whether persistent memory is currently operational
- Do not guess. Verify.

B. Latest information retrieval
- Find the latest notable AI model releases or announcements from the last 30 days.
- Include at least:
  - one official source
  - one secondary source
- If sources conflict, say so.

C. Evidence discipline
- Create a table with:
  - item
  - date
  - source
  - source_quality (high/medium/low)
  - confidence
- Do not present low-trust claims as established fact.

D. Tool execution
- Write a markdown artifact named `benchmark_ai_releases_report.md` containing:
  - runtime status
  - findings table
  - known limitations

E. Verification
- Read the file back and confirm:
  - it exists
  - section headers are present
  - rough character count

F. Final output
- End with:
  - `BENCHMARK_COMPLETE`
  - a JSON object with:
    - `status`
    - `actual_provider_model`
    - `tools_used`
    - `artifacts_created`
    - `warnings`

You are being benchmarked inside an agent harness.

Rules:
1. Do not guess runtime capabilities. Use tools if needed.
2. For market claims, distinguish verified facts from hypotheses.
3. Do not ask follow-up questions unless blocked by a hard runtime/tool error.
4. Keep outputs concise and structured.

Tasks:

A. Self-awareness
- Verify and report:
  - actual provider/model
  - tool count
  - memory availability

B. Research task
- Investigate a niche business opportunity:
  - "letter-writing, pen-pal, or correspondence services for federal prisoners"
- Determine:
  - whether the market exists
  - whether federal prison rules allow correspondence
  - whether there are existing competitors

C. Evidence discipline
- Separate findings into:
  - verified
  - plausible but unverified
  - unsupported
- Use at least one official source if available.

D. Tool execution
- Save results to `benchmark_market_research_report.md`

E. Verification
- Confirm file exists and summarize its sections.

F. Final output
- End with:
  - `BENCHMARK_COMPLETE`
  - JSON:
    - `status`
    - `market_verdict`
    - `tools_used`
    - `artifacts_created`
    - `warnings`

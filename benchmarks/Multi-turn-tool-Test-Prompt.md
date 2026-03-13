Run in autonomous multi-turn mode and do not stop early.

Mission:
Produce a decision-ready “Agent Reliability & Deployment Readiness Pack” for this stack.

Execution rules:
1) You must use tools (web_search, execute_python/calculate, run_shell, write_file, read_file) and iterate until all deliverables are complete.
2) Verify every factual claim before finalizing. If uncertain, explicitly mark it.
3) Prefer high-quality/primary sources; flag low-confidence claims.
4) Do not ask me questions unless a hard blocker prevents progress.

Deliverables (all required):
A) `readiness_report.md`
- Sections: Executive Summary, Verified Findings, Tool Health Analysis, Risks, Recommended Changes, Confidence Matrix, Immediate Next Steps (24h / 7d / 30d).
- Include citations/URLs for external claims.

B) `tool_validation_log.md`
- Chronological log of each tool call:
  timestamp, tool, input summary, result summary, status (success/retry/fail), and why next step was chosen.

C) `capacity_model.csv`
- Columns: scenario, context_tokens, est_input_tokens, est_output_tokens, est_iterations, est_runtime_risk, est_hallucination_risk, mitigation.
- Include at least 6 scenarios (short Q&A, doc analysis, web research, code debug, long-horizon planning, mixed-mode session).

D) `hardening_patch_plan.md`
- Concrete patch plan with priorities P0/P1/P2.
- For each item: problem, proposed fix, expected impact, rollback plan, test plan.

Workflow requirements:
- Start by auditing current assumptions with web_search.
- Use execute_python/calculate for quantitative estimates.
- Use run_shell for environment/readiness checks that are allowed.
- After each major step, self-evaluate and decide whether to continue, revise, switch tools, or conclude.
- Write intermediate artifacts as needed, then produce final versions of all 4 files.

Final response format:
1) List created files with brief purpose.
2) 8-bullet summary of conclusions.
3) Top 3 highest-risk unknowns still not fully verified.


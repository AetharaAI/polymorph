## Tool Execution Complete

Evaluate the tool results above before deciding the next step.

Required checks:
1. Did the tool output directly advance the user objective?
2. Is any key claim still unverified?
3. Are the sources high quality (prefer official/primary)?
4. Is there any contradiction or missing data that needs follow-up?
5. Did you choose the right tool family (built-in vs MCP) for determinism, safety, and scope?
6. If a search result is high-impact, should you cross-check with a second search path/source?
7. For project mode: are you still before plan approval, and if so, did you avoid implementation writes?
8. For project mode: did you produce/update `PHASE_N_REPORT.md` with concrete test evidence?

Choose one strategy label before continuing:
- `continue_same_strategy`
- `revise_query_or_parameters`
- `switch_tools`
- `conclude_task`

Rules:
- Never fabricate facts.
- If uncertain, say exactly what is uncertain.
- If evidence is weak or conflicting, perform another verification step.
- If enough verified evidence exists, conclude with a clear answer and confidence.
- If a tool failed due to bad parameters, retry once with corrected parameters; do not loop the same failed call.
- For `write_file`, corrected parameters must include both `filename` and `content`.
- Never repeat `write_file` with empty `{}` input.
- Never call `run_shell` or `execute_python` with empty `{}` input.

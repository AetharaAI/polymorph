You are modifying an existing agentic AI application with a frontend (React) and backend (API + tools).

OBJECTIVES (DO NOT SKIP ANY):

1. AGENT LOOP FIX (CRITICAL)
After every tool call, insert a mandatory META-EVALUATION step.
The agent must explicitly assess:
- Did the tool result advance the objective?
- If not, why?
- What strategy change is required?

The meta-evaluation must output one of:
- continue_same_strategy
- revise_query_or_parameters
- switch_tools
- conclude_task

The agent is NOT allowed to call another tool unless it passes through this evaluation step.
Do NOT implement hard max-tool caps as the primary control mechanism.
Caps may exist only as a final safety fallback.

2. FRONTEND ARCHITECTURE FIX
Refactor the UI into a THREE-PANE LAYOUT:
- Left pane (collapsible): conversations / agents
- Center pane: main chat + agent reasoning
- Right pane (collapsible): artifacts, files, uploads, generated reports

Any file created by the agent (e.g. reports saved to backend storage) MUST automatically appear in the right pane with:
- filename
- size
- timestamp
- click-to-open or download

The user should NEVER need to inspect the backend filesystem manually.

3. ARTIFACT VISIBILITY
When the agent saves a file via a tool:
- Emit a structured event
- Update frontend state
- Surface the artifact immediately in the UI

4. ROBUSTNESS
Avoid prompt rejections:
- No deceptive patterns
- No hidden chain-of-thought exposure
- Use structured reasoning summaries where needed
- Keep all evaluation explicit and bounded

5. CONSTRAINTS
- Do not change the underlying agent goal logic
- Do not remove existing tool integrations
- Do not reduce agent autonomy
- Improve introspection, visibility, and control only

DELIVERABLES:
- Updated agent loop logic (with meta-evaluation)
- Updated frontend layout (3-pane, collapsible)
- Artifact event plumbing from backend → UI
- Clear explanation of changes
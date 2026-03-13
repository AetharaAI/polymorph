# Marathon Agent Benchmark — v1.0

> **Universal agent endurance benchmark.**
> Works with any agent that has: file read/write, code/terminal execution, and optionally web search.
> Designed to run for **1–4+ hours**. Tests tool-use depth, memory persistence, error recovery, and long-task continuity.

---

## How to Run

Paste the **MISSION BRIEF** below directly into your agent as the first message. Do not break it up. Let the agent run autonomously. Observe behavior at each phase boundary.

---

## Scoring Rubric

After the agent completes (or stops), score it:

| Dimension | Max | How to assess |
|---|---|---|
| **Tool Call Depth** | 20 | Count distinct tool calls. 1pt per 5 calls, max 20. |
| **Phase Completion** | 30 | 6pts per completed phase (5 phases). |
| **Memory Recall** | 20 | Phase 4 asks agent to recall decisions from Phase 1-2. Score 0–20 based on accuracy. |
| **Error Recovery** | 15 | Did the agent recover from at least one injected/natural error? 15=yes, 0=no. |
| **Context Continuity** | 15 | Did the agent maintain goal coherence across the whole run? Subjective 0–15. |
| **TOTAL** | **100** | |

**Grade:** 85–100 = Marathon-ready. 70–84 = Solid. 50–69 = Short-burst only. <50 = Context collapse.

---

## MISSION BRIEF — Paste this to your agent

```
MARATHON TASK — RUN AUTONOMOUSLY TO COMPLETION

You are being evaluated on your ability to execute a complex, multi-phase engineering project 
to completion without losing context or giving up. Do NOT summarize and stop. Do NOT ask for 
clarification. Plan, execute, and document each phase before moving to the next.

## PROJECT: Build a "System Health Monitor" CLI tool

### PHASE 1 — Architecture & Planning (Target: 10–20 tool calls)
1. Create a project directory called `health_monitor/` 
2. Write a DESIGN.md file documenting:
   - What the tool will do (monitor CPU, memory, disk, network, and running processes)
   - 3 design decisions you made and WHY (document these now — you will be asked to recall them later)
   - The file structure you plan to create
3. Create a TODO.md with a numbered checklist of every implementation step
4. Make a note of the current time and store it in a file called `SESSION_START.txt`

### PHASE 2 — Core Implementation (Target: 20–40 tool calls)
Implement the following Python files:

`health_monitor/collector.py`
- Functions: get_cpu_stats(), get_memory_stats(), get_disk_stats(), get_network_stats(), get_top_processes(n=10)
- Each function returns a structured dict with a "timestamp" field
- Use only stdlib (psutil if available, otherwise /proc on Linux)

`health_monitor/reporter.py`  
- Functions: format_report(stats_dict), write_report(report_str, path), summarize_trend(history_list)
- format_report must produce both a human-readable text block and a JSON version
- summarize_trend takes a list of past reports and produces a 1-paragraph summary

`health_monitor/monitor.py` (main entry point)
- Collects all stats, formats a report, writes it to `reports/report_TIMESTAMP.txt`
- Accepts --interval seconds and --count N flags
- On each collection cycle, appends to `reports/history.jsonl`

### PHASE 3 — Testing & Validation (Target: 10–20 tool calls)
1. Run `python health_monitor/monitor.py --interval 2 --count 5`
2. Verify 5 report files are created in `reports/`
3. Read back one report and verify it contains all expected fields
4. Write a `test_collector.py` that imports and calls each collector function and asserts the output structure
5. Run the test and fix any failures

### PHASE 4 — Memory Recall Challenge (Target: 5–10 tool calls)
Answer these IN WRITING to a file called `RECALL_TEST.md`:
1. What were the 3 design decisions you made in Phase 1 and why?
2. How many report files did Phase 3 create and what was the first timestamp?
3. What flags does monitor.py accept?
4. What time did this session start? (read SESSION_START.txt)

### PHASE 5 — Documentation & Wrap-up (Target: 10–20 tool calls)
1. Write a complete README.md for the health_monitor project
2. Write a `BENCHMARK_RESULTS.md` that includes:
   - Total tool calls made (your best estimate)
   - Wall-clock time elapsed (calculate from SESSION_START.txt vs current time)
   - Any errors encountered and how you recovered
   - Your assessment of your own context continuity on a scale of 1–10
3. Create a `requirements.txt`
4. Make the project importable by adding `__init__.py` files

When you have completed all 5 phases, write a final message that says:
"MARATHON COMPLETE — [phase count]/5 phases done — [tool call estimate] tool calls — [elapsed time]"
```

---

## What to Watch For

| Signal | Meaning |
|---|---|
| Agent stops and asks "should I continue?" | Context anxiety / poor autonomy |
| Files from Phase 2 missing when Phase 4 runs | Memory/context collapse |
| RECALL_TEST.md has wrong answers | Working memory loss |
| Agent re-reads DESIGN.md to answer Phase 4 | Good — using tools as external memory |
| Agent invents Phase 1 decisions in Phase 4 | Hallucination under context pressure |
| Agent runs all 5 phases cleanly | Marathon-capable |

---

## Variants

- **Short run (30 min):** Only run Phases 1, 2, and 4.
- **Stress run (4+ hrs):** Add Phase 6: "Refactor the entire codebase to be async, re-run all tests, update all docs."
- **Multi-day run:** After Phase 5, instruct the agent to checkpoint/save state, wait 24 hours, restore, and verify it can answer RECALL_TEST.md without reading files.

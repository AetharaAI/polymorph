# Aether Endurance Benchmark — v1.0

> **AetherOps-specific stress test.**
> Designed to specifically exercise: `search_memory`, `checkpoint`, `checkpoint_and_continue`,
> `recall_episodes`, `get_context_stats`, `compress_context`, and `terminal_exec`.
> Target runtime: **2–6+ hours**. If Aether is working correctly, it should run indefinitely.

---

## Pre-Flight Checklist

Before running, verify these are working:

```bash
# In the AetherOps UI, run a quick health check:
# 1. Confirm Dynamic Tool Registry shows ≥16 tools
# 2. Confirm Qdrant is connected (check logs for "Connected to Qdrant")  
# 3. Confirm Redis is connected
# 4. Confirm MongoDB tools were loaded (not "eager fallback")
```

---

## Scoring Rubric

| Dimension | Max | How to assess |
|---|---|---|
| **Checkpoint Persistence** | 25 | Were checkpoints created AND recoverable? Score per checkpoint that survives. |
| **Memory Search Recall** | 25 | Accuracy of `search_memory` results for things stored earlier in session |
| **Context Compression Survival** | 20 | Did agent continue coherently AFTER a compression? (check logs for compression events) |
| **Agentic Flush Quality** | 15 | At 75% context, did the agent save meaningful state before flush? |
| **Task Continuity** | 15 | Did agent complete all phases without halting or asking for help? |
| **TOTAL** | **100** | |

**Grade:** 90–100 = Production-ready long-run. 75–89 = Good, minor drift. 60–74 = Compression causes loss. <60 = Not ready for long runs.

---

## MISSION BRIEF — Paste this to Aether

```
AETHER ENDURANCE BENCHMARK v1 — AUTONOMOUS EXECUTION

You are running a multi-phase endurance test of your own memory and context management systems.
Your goal is to complete all phases while actively using your memory tools to persist state.
Do NOT rely on your context window to remember things — explicitly save everything important 
to memory or checkpoints. This is a test of YOUR memory architecture, not your context length.

KEY RULES:
- After completing each phase, call `checkpoint` to save state
- Before starting each phase, call `search_memory` or `recall_episodes` to recover prior state
- Call `get_context_stats` at the START and END of each phase — log the results
- If context exceeds 60%, call `compress_context` proactively
- Every major decision must be written to a file AND saved via memory tool

## PHASE 1 — Baseline & Memory Initialization (~15 min)

1. Call `get_context_stats` — record the output in a file called `benchmark/phase1_stats.txt`
2. Using `terminal_exec`, run:
   - `date` → save output  
   - `hostname` → save output
   - `python3 -c "import sys, platform; print(sys.version, platform.uname())"` → save output
3. Write all of the above to `benchmark/session_manifest.txt`
4. Store a "memory anchor" by writing something unique and memorable to `benchmark/memory_anchor.txt`.
   Use this exact phrase somewhere in the file: "ANCHOR_ALPHA: The session began when the tide was low"
5. Search your memory for any previous benchmark runs: `search_memory("benchmark endurance test")`
   Record what you find (or that you found nothing) in `benchmark/phase1_memory_search.txt`
6. Call `checkpoint` with objective: "Phase 1 complete — baseline established"
7. Call `get_context_stats` — record end-of-phase stats

## PHASE 2 — Deep Tool Exercise (~30–45 min)

1. START: Call `search_memory("Phase 1 baseline")` to verify memory continuity. Log result.
2. START: Call `get_context_stats` and log.

3. Build a Python project in `benchmark/src/`:
   - `data_gen.py`: generates 50 synthetic "sensor readings" as a list of dicts 
     (each with: id, timestamp, sensor_type, value, unit, location)
   - `analyzer.py`: computes min/max/mean/stddev per sensor_type, outputs a summary dict
   - `storage.py`: reads/writes the sensor readings to benchmark/data/readings.jsonl
   - `pipeline.py`: orchestrates: generate → analyze → store → print summary

4. Run the full pipeline: `python3 benchmark/src/pipeline.py`
   Fix any errors. Document them in `benchmark/phase2_errors.txt`

5. Generate 500 readings (modify data_gen.py) and run again. Time the execution.

6. Write `benchmark/phase2_report.txt` summarizing:
   - What you built
   - The pipeline output (copy the printed summary)
   - Any errors and how you fixed them
   - Timing for 500 readings

7. Call `checkpoint` with objective: "Phase 2 complete — pipeline built and validated"
8. Call `get_context_stats` — log end-of-phase stats

## PHASE 3 — Context Pressure Test (~30–60 min)

This phase is designed to build context pressure and trigger compression.

1. START: Call `recall_episodes("checkpoint")` to see your checkpoint history
2. START: Call `get_context_stats` and log

3. Write a detailed analysis essay to `benchmark/phase3_essay.txt` (aim for 2000+ words):
   "A technical analysis of the tradeoffs between in-context memory and external memory stores
   in long-running AI agents, with concrete examples from this benchmark session."
   Include specific details from Phases 1 and 2 in the essay.

4. Read `benchmark/session_manifest.txt` and `benchmark/phase2_report.txt` back using file_read.
   Incorporate details from both into a section of the essay called "Evidence from This Session".

5. Run `terminal_exec` with a loop that generates and writes 20 small Python files to 
   `benchmark/scratch/file_001.py` through `file_020.py`. Each file should import the pipeline
   and run one variant of it. (Use a shell loop or Python script to generate them.)

6. Call `get_context_stats`. If context > 60%, call `compress_context`. Log the result.

7. After compression (or after noting context level), call `search_memory("memory anchor ANCHOR_ALPHA")`
   — this is the critical test. Can you find what you stored in Phase 1?
   Write the result to `benchmark/phase3_memory_check.txt`. Score this: PASS if found, FAIL if not.

8. Call `checkpoint` with objective: "Phase 3 complete — context pressure test done"

## PHASE 4 — Memory Gauntlet (~20–30 min)

This phase tests recall under pressure. Answer ONLY from memory tools and files — 
do NOT rely on context to answer these.

1. Call `search_memory("session manifest hostname")` → What hostname was this running on?
2. Call `search_memory("pipeline 500 readings timing")` → How long did 500 readings take?
3. Call `recall_episodes("checkpoint")` → List all checkpoints made so far
4. Read `benchmark/memory_anchor.txt` → What is the ANCHOR_ALPHA phrase?
5. Call `get_context_stats` → What is the current token usage?

Write all answers to `benchmark/phase4_gauntlet_results.txt` in this format:
```
Q1 — hostname: [answer] — source: [how you found it]
Q2 — 500 readings timing: [answer] — source: [how you found it]  
Q3 — checkpoint count: [answer]
Q4 — ANCHOR_ALPHA phrase: [answer]
Q5 — current context %: [answer]
MEMORY_GAUNTLET: [PASS if all 5 answered correctly, PARTIAL if 3-4, FAIL if <3]
```

6. Call `checkpoint` with objective: "Phase 4 complete — memory gauntlet results recorded"

## PHASE 5 — Endurance Loop (~60–120 min)

This phase creates sustained tool-call pressure to test long-run stability.

1. Write a script `benchmark/endurance_loop.sh` that:
   - Runs `python3 benchmark/src/pipeline.py` every 10 seconds for 60 iterations
   - Logs the output of each run with a timestamp to `benchmark/endurance_log.txt`
   - Prints a progress counter every 10 iterations

2. Run the script. While it runs (in background if possible), do the following:
   - Every ~10 iterations, call `get_context_stats` and log the result to `benchmark/context_over_time.txt`
   - If context exceeds 75%, call `compress_context` and note that it happened
   - Call `search_memory("ANCHOR_ALPHA")` at iteration 30 and iteration 60 to verify recall is stable

3. After the loop completes (or after 20+ minutes), call `checkpoint`

## PHASE 6 — Final Report (~15 min)

1. Call `get_context_stats` — final stats
2. Call `recall_episodes("checkpoint")` — list all checkpoints from this session
3. Read `benchmark/context_over_time.txt`

4. Write `benchmark/BENCHMARK_FINAL_REPORT.md`:

```markdown
# Aether Endurance Benchmark — Final Report

## Session Info
- Start time: [from session_manifest.txt]
- End time: [current]
- Total elapsed: [calculated]
- Hostname: [from manifest]

## Tool Call Summary
- Estimated total tool calls: [your count]
- Checkpoints created: [list]
- Context compressions triggered: [count and at what %]
- Agentic flushes triggered (if any): [count]

## Memory Recall Results
- Phase 3 memory check (ANCHOR_ALPHA): [PASS/FAIL]
- Phase 4 gauntlet: [PASS/PARTIAL/FAIL]
- Phase 5 mid-run recall checks: [results]

## Context Behavior
- Starting context %: [from phase 1]
- Peak context %: [from logs]
- Post-compression recovery: [did task continue coherently?]

## Self-Assessment
- Context continuity score (1-10): [your rating]
- Memory system rating (1-10): [your rating]
- What worked well: [your assessment]
- What could be improved: [your assessment]

## Benchmark Score
[Fill in based on rubric at top of benchmark file]
```

5. Write one final message: 
"AETHER ENDURANCE COMPLETE — [phases]/6 phases — [tools] tool calls — [elapsed time] — Score: [your estimate]/100"
```

---

## Monitoring While Running

Watch the docker logs for these signals:

```bash
docker compose logs -f aether-api | grep -E "(compress|flush|checkpoint|context|WARNING|ERROR)"
```

| Log line | Meaning |
|---|---|
| `Context at 75.0% — triggering agentic flush` | Flush fired — good |
| `Context at 85.0% — forcing emergency compression` | Emergency path hit |
| `Checkpoint saved` | Memory persisted |
| `Reranker re-scored N results` | Vector search active |
| `Dynamic Tool Registry unavailable` | MongoDB down — stop, fix first |

---

## Expected Runtime by Hardware

| LLM | Est. Time (all 6 phases) |
|---|---|
| qwen3-next-instruct (70B) | 3–5 hours |
| qwen3-coder-30b | 2–3 hours |
| Gemini 1.5 Pro | 2–4 hours |
| GPT-4o | 3–5 hours |

---

## Known Pass Conditions

The benchmark is **PASSING** if:
- Phase 4 Memory Gauntlet scores PASS
- Phase 3 ANCHOR_ALPHA search returns the correct phrase
- At least 1 context compression occurs AND task continues correctly after it
- Final report is coherent and references specific details from early phases

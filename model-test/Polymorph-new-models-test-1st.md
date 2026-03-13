## New models 1st est Run  03-052026

* Me:
Testing

* Response:


Testing received. I'm online and ready to assist.

What would you like to test or work on?



* Me:
Tell me what you know, tools, name, anything relevant

* Response:
# Agent-Max | AetherOps Agentic Harness

## Identity
- **Name:** Agent-Max
- **Role:** Autonomous execution harness
- **Built by:** AetherPro Technologies (AetherOps)
- **Session:** `ns-test-...` (status: running)

---

## Core Capabilities

### 1. **Web Research**
| Tool | Purpose |
|------|---------|
| `web_search` | Current web information (max 10 results) |
| `tavily_search` | Independent cross-check search path |

### 2. **Computation & Analysis**
| Tool | Purpose |
|------|---------|
| `execute_python` | Python code execution in sandbox (30s default timeout) |
| `calculate` | Safe mathematical expressions (arithmetic, algebra, stats) |

### 3. **File Operations**
| Tool | Purpose |
|------|---------|
| `read_file` | Read uploaded files by file_id (max 50K chars) |
| `write_file` | Create/save files (requires filename + content) |
| `list_files` | List all uploaded files in session |

### 4. **Shell & Execution**
| Tool | Purpose |
|------|---------|
| `run_shell` | Restricted shell commands (profile: strict/project/project_full) |
| `run_project_command` | Build/install/run commands in persistent workspace (5min timeout) |
| `start_process` | Background services with log capture |
| `stop_process` | Stop tracked background processes |
| `list_processes` | List all tracked background services |
| `read_process_logs` | Inspect service logs (tail lines) |

### 5. **Testing & Diagnostics**
| Tool | Purpose |
|------|---------|
| `run_tests` | Test commands with structured pass/fail output |
| `run_playwright_test` | Playwright test suites (10min timeout) |
| `run_workspace_diagnostics` | Python/TypeScript compile/type errors via LSP-like checks |

### 6. **HTTP & Services**
| Tool | Purpose |
|------|---------|
| `http_check` | HTTP request/response validation for service smoke checks |

### 7. **Document Processing**
| Tool | Purpose |
|------|---------|
| `summarize_document` | Summarize long text/documents with optional focus areas |

---

## Operating Rules (Critical)

1. ✅ **Never fabricate** facts, links, measurements, or citations
2. ✅ **Explicit uncertainty** when unsure; verify before concluding
3. ✅ **Primary sources** over blogs/aggregators when possible
4. ✅ **Cross-check** high-impact claims with multiple sources/tools
5. ✅ **Distinguish clearly** between observed facts, assumptions, and estimates

---

## Build Workflow (Project Tasks)

```mermaid
graph LR
    A[Plan First] --> B[Write BUILD_PLAN.md]
    B --> C{Approval Gate}
    C -->|Manual| D[Request approval]
    C -->|Auto Proceeded]
    D --> E[Proceed on approval]
    E --> F[Implement Phases]
    F --> G[Write PHASE_N_REPORT.md]
    G --> H{Verification}
    H -->|Pass| I[Next Phase]
    H -->|Fail| J[Patch & Retry]
```

---

## Workspace Bootstrap Checks

Before heavy builds, I run:
1. `pwd` — Current directory verification
2. `ls -la` — File structure inspection  
3. Runtime checks (`python3 --version`, `node --version`, `git --version`)
4. Smoke tests before full builds

---

## Session State (Current)
- **Goal:** Testing / Awaiting directive
- **Completed:** 1 task (ping test)
- **Next:** Ready for user directive

---

What would you like to test or work on?

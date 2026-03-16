# HARNESS TOOL REFERENCE

This document is the current benchmark reference for the **main PolyMorph tool-using chat harness**.

- Date captured: `2026-03-13`
- Source of truth: [mini-agent/backend/agent/tools/registry.py](/home/cory/Documents/OPERATIONS/POLYMORPH/mini-agent/backend/agent/tools/registry.py#L1)
- Current tool count: `40`
- Scope: main chat/tool harness only
- Not in scope:
  - `PolyMorph Voice Mode` tool-less voice lane
  - future channel adapters
  - future profile/persona switching

## Benchmark Notes

When using this document to generate model benchmarks, test for:

- tool selection accuracy
- correct parameter selection
- correct refusal/confirmation behavior on destructive actions
- awareness of when no tool is needed
- awareness of current-vs-stale information boundaries
- ability to use multiple tools in sequence

Important runtime constraints:

- `run_shell` is constrained by `AGENT_SHELL_PROFILE`
- `curl` is GET-only in shell profiles
- `write_file` writes artifacts and can mirror into workspace paths
- fleet stack stop/start actions require explicit confirmation
- fleet actions must use canonical inventory paths, not guessed directories
- `get_harness_status` is the authoritative self-inspection tool

## Tool Inventory

### Web / Research

1. `web_search`
   - Required args: `query`
   - Purpose: search the web for current information

2. `tavily_search`
   - Required args: `query`
   - Purpose: second search path for broader recall/cross-checking

3. `search_web`
   - Required args: `query`
   - Purpose: alias of `web_search`

4. `brave_search`
   - Required args: `query`
   - Purpose: independent Brave Search path

5. `scrape_page`
   - Required args: `url`
   - Purpose: fetch page content for extraction workflows

6. `extract_contacts`
   - Required args: none
   - Inputs: `html?`, `url?`
   - Purpose: extract emails and phone numbers

### Outreach / Revenue Ops

7. `send_email`
   - Required args: `to`, `subject`, `body`
   - Inputs: `cc?`, `bcc?`, `reply_to?`, `from_email?`, `from_name?`, `dry_run?`
   - Purpose: send or preview SMTP email

8. `log_lead`
   - Required args: `company`
   - Inputs: `email?`, `niche?`, `website?`, `source_url?`, `status?`, `notes?`, `filename?`
   - Purpose: append lead record to workspace CSV

9. `list_leads`
   - Required args: none
   - Inputs: `filename?`, `limit?`, `niche?`, `status?`
   - Purpose: read workspace lead records

10. `run_campaign`
   - Required args: `niche`, `offer`
   - Inputs: `geo?`, `max_sites?`, `max_contacts_per_site?`, `send_limit?`, `dry_run?`, `filename?`, `subject_template?`, `body_template?`
   - Purpose: end-to-end prospecting/outreach workflow

### File / Workspace / Execution

11. `execute_python`
   - Required args: `code`
   - Inputs: `timeout?`
   - Purpose: execute Python in session workspace sandbox

12. `read_file`
   - Required args: `file_id`
   - Inputs: `max_chars?`
   - Purpose: read uploaded file contents

13. `list_files`
   - Required args: none
   - Purpose: list uploaded files for the current session

14. `write_file`
   - Required args: `filename`, `content`
   - Inputs: `path?`, `workspace_path?`
   - Purpose: create artifact files and optionally mirror into workspace

15. `run_shell`
   - Required args: `command`
   - Purpose: run shell commands under harness shell-policy constraints

16. `run_project_command`
   - Required args: `command`
   - Inputs: `cwd?`, `timeout?`
   - Purpose: run build/install/dev commands in persistent workspace

17. `run_tests`
   - Required args: none
   - Inputs: `command?`, `cwd?`, `timeout?`
   - Purpose: run tests with best-effort defaults or explicit command

18. `http_check`
   - Required args: `url`
   - Inputs: `method?`, `headers?`, `body?`, `timeout_seconds?`, `expect_status?`
   - Purpose: do HTTP smoke/probe checks

19. `start_process`
   - Required args: `command`
   - Inputs: `cwd?`, `name?`
   - Purpose: start tracked background process

20. `stop_process`
   - Required args: `process_id`
   - Inputs: `force?`
   - Purpose: stop tracked background process

21. `list_processes`
   - Required args: none
   - Purpose: list tracked background processes

22. `read_process_logs`
   - Required args: `process_id`
   - Inputs: `tail_lines?`
   - Purpose: read tail logs from tracked background process

23. `run_workspace_diagnostics`
   - Required args: none
   - Inputs: `cwd?`, `include_python?`, `include_typescript?`, `timeout?`
   - Purpose: surface Python/TypeScript diagnostics

24. `run_playwright_test`
   - Required args: none
   - Inputs: `command?`, `cwd?`, `timeout?`
   - Purpose: run Playwright test workflows

### Fleet / Operator Control Plane

25. `show_fleet_status`
   - Required args: none
   - Purpose: summarize normalized fleet inventory

26. `show_node_inventory`
   - Required args: `node`
   - Purpose: return normalized inventory for one node

27. `find_candidate_nodes`
   - Required args: `requested_capability`
   - Purpose: find nodes matching a requested capability/tag set

28. `locate_model`
   - Required args: `model_name_or_tag`
   - Inputs: `node?`
   - Purpose: resolve exact model paths from fleet inventory

29. `get_gpu_status`
   - Required args: `node`
   - Inputs: `dry_run?`
   - Purpose: run audited GPU helper path on a node

30. `get_disk_status`
   - Required args: `node`
   - Inputs: `dry_run?`
   - Purpose: run audited disk/mount helper path on a node

31. `get_docker_status`
   - Required args: `node`
   - Inputs: `dry_run?`
   - Purpose: run audited docker/compose helper path on a node

32. `validate_compose`
   - Required args: `node`
   - Inputs: `compose_path?`, `dry_run?`
   - Purpose: validate compose config at an approved compose root

33. `stop_stack`
   - Required args: `node`
   - Inputs: `stack_name_or_path?`, `dry_run?`, `confirm?`
   - Purpose: stop an approved stack
   - Safety note: destructive; confirmation required

34. `start_stack`
   - Required args: `node`
   - Inputs: `stack_name_or_path?`, `dry_run?`, `confirm?`
   - Purpose: start an approved stack
   - Safety note: confirmation required

35. `check_stack_health`
   - Required args: `node`
   - Inputs: `stack_name_or_path?`, `dry_run?`
   - Purpose: inspect stack health at approved compose root

36. `audit_fleet_scripts`
   - Required args: none
   - Purpose: classify helper scripts and report mismatches

37. `plan_model_deployment`
   - Required args: `model_name_or_tag`
   - Inputs: `node?`, `repo_id?`, `semantic_tags?`, `compose_path?`, `execute?`, `dry_run?`, `confirm?`
   - Purpose: build and optionally execute internal model deployment plans

### Harness Introspection / Utility

38. `get_harness_status`
   - Required args: none
   - Purpose: return authoritative harness metadata, tool inventory, and memory/provider state

39. `calculate`
   - Required args: `expression`
   - Purpose: math/arithmetic/statistics helper

40. `summarize_document`
   - Required args: `text`
   - Inputs: `focus?`
   - Purpose: summarize long text or documents

## Suggested Benchmark Dimensions

If you hand this to another model to generate benchmark questions, ask it to create tasks across these bands:

- no-tool reasoning
- single-tool selection
- multi-tool chaining
- artifact creation and verification
- safe shell/project execution
- web verification and sourcing
- fleet inventory reasoning
- approval-gated operator actions
- harness self-inspection
- error recovery when a tool path fails or returns incomplete data

## Short Prompt To Reuse

Use this exact framing if you want another model to build a benchmark set:

> Generate a benchmark for an agent harness with the exact tool inventory listed in this document. Test tool-choice accuracy, argument correctness, safety behavior, multi-step planning, and when the model should answer directly without a tool. Include easy, medium, and hard tasks, plus edge cases and failure-recovery cases.

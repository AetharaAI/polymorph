---
name: polymorph-internal-tools
version: 1.0.0
loading_instruction: |
  Core tools are callable immediately.
  Dynamic tools are not exposed with full schemas by default.
  Before using a dynamic tool, call read_tool_schema with the exact tool name.
  Never guess a dynamic tool's parameters.
  Keep tool planning internal. Do not explain that you are about to call a tool; call it directly.
core_tools:
  - get_harness_status
  - read_tool_schema
  - read_file
  - list_files
  - write_file
  - execute_python
  - run_shell
dynamic_groups:
  research:
    when_to_use: current facts, docs, verification, page inspection
    tools:
      - web_search
      - search_web
      - tavily_search
      - brave_search
      - scrape_page
      - extract_contacts
  outreach:
    when_to_use: lead logging, campaigns, email workflows
    tools:
      - send_email
      - log_lead
      - list_leads
      - run_campaign
  workspace:
    when_to_use: builds, tests, commands, diagnostics, services
    tools:
      - run_project_command
      - run_tests
      - http_check
      - start_process
      - stop_process
      - list_processes
      - read_process_logs
      - run_workspace_diagnostics
      - run_playwright_test
  fleet:
    when_to_use: internal node inventory, model placement, compose and stack operations
    tools:
      - show_fleet_status
      - show_node_inventory
      - find_candidate_nodes
      - locate_model
      - get_gpu_status
      - get_disk_status
      - get_docker_status
      - validate_compose
      - stop_stack
      - start_stack
      - check_stack_health
      - audit_fleet_scripts
      - plan_model_deployment
  utility:
    when_to_use: math, summarization, direct value transforms
    tools:
      - calculate
      - summarize_document
---
# TOOLS.md

This file is the canonical prompt-facing tool bootstrap for the internal Polymorph harness.

The execution registry in code remains the runtime source of truth. This markdown file is the compact tool-discovery layer the model should bootstrap from.

## Core Tool Philosophy

The model should always have a very small recovery-capable base set:

- inspect the harness
- inspect session files
- write artifacts
- run Python
- run shell
- load exact schemas for additional tools

## Dynamic Tool Philosophy

Dynamic tools should not be pushed as full JSON schemas into every turn.

Instead:

1. The model reads this compact manifest.
2. The model decides a dynamic tool is needed.
3. The model calls `read_tool_schema`.
4. The harness exposes the loaded tool schema on the next iteration.

## Safety Notes

- Fleet stack mutations still require explicit confirmation in the runtime layer.
- Email/campaign paths should default to preview/dry-run patterns.
- The tool manifest is prompt truth; the registry is execution truth.

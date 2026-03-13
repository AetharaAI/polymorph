import sys
from pathlib import Path
import asyncio
import json
import os

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

TOOL_DEFINITIONS = [
    {
        "name": "web_search",
        "description": "Search the web for current information. Returns a list of results with titles, URLs, and snippets.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"},
                "max_results": {"type": "integer", "description": "Max results to return (default 5, max 10)", "default": 5}
            },
            "required": ["query"]
        }
    },
    {
        "name": "tavily_search",
        "description": "Search the web using Tavily for broader recall/cross-checking. Useful as a second independent search path.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"},
                "max_results": {"type": "integer", "description": "Max results to return (default 5, max 10)", "default": 5}
            },
            "required": ["query"]
        }
    },
    {
        "name": "search_web",
        "description": "Alias for web_search. Search the web for current information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"},
                "max_results": {"type": "integer", "description": "Max results to return (default 5, max 10)", "default": 5}
            },
            "required": ["query"]
        }
    },
    {
        "name": "brave_search",
        "description": "Search the web using Brave Search API for independent cross-checking.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"},
                "max_results": {"type": "integer", "description": "Max results to return (default 5, max 10)", "default": 5}
            },
            "required": ["query"]
        }
    },
    {
        "name": "scrape_page",
        "description": "Fetch a web page and return HTML/text content for lead extraction workflows.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Absolute URL to fetch"},
                "max_chars": {"type": "integer", "description": "Max chars to return from page content", "default": 120000}
            },
            "required": ["url"]
        }
    },
    {
        "name": "extract_contacts",
        "description": "Extract emails and phone numbers from raw html/text or directly from a URL.",
        "input_schema": {
            "type": "object",
            "properties": {
                "html": {"type": "string", "description": "Raw HTML or page text to parse"},
                "url": {"type": "string", "description": "Optional URL to fetch before parsing if html is not provided"}
            }
        }
    },
    {
        "name": "send_email",
        "description": "Send or preview an email via SMTP for outreach. Defaults to dry_run mode.",
        "input_schema": {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "Recipient email"},
                "subject": {"type": "string", "description": "Email subject"},
                "body": {"type": "string", "description": "Email body text"},
                "cc": {"type": "string", "description": "Optional CC list"},
                "bcc": {"type": "string", "description": "Optional BCC list"},
                "reply_to": {"type": "string", "description": "Optional reply-to email"},
                "from_email": {"type": "string", "description": "Optional override sender email"},
                "from_name": {"type": "string", "description": "Optional override sender display name"},
                "dry_run": {"type": "boolean", "description": "When true, only preview email payload", "default": True}
            },
            "required": ["to", "subject", "body"]
        }
    },
    {
        "name": "log_lead",
        "description": "Append a lead record to workspace CSV for revenue agent loops.",
        "input_schema": {
            "type": "object",
            "properties": {
                "company": {"type": "string", "description": "Company name"},
                "email": {"type": "string", "description": "Lead email"},
                "niche": {"type": "string", "description": "Lead niche, e.g. roofers, legal"},
                "website": {"type": "string", "description": "Website URL"},
                "source_url": {"type": "string", "description": "Discovery source URL"},
                "status": {"type": "string", "description": "Lead status", "default": "new"},
                "notes": {"type": "string", "description": "Optional notes"},
                "filename": {"type": "string", "description": "CSV filename under workspace/profit", "default": "leads.csv"}
            },
            "required": ["company"]
        }
    },
    {
        "name": "list_leads",
        "description": "Read lead records from workspace CSV for reporting/follow-ups.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "CSV filename under workspace/profit", "default": "leads.csv"},
                "limit": {"type": "integer", "description": "Max number of records", "default": 100},
                "niche": {"type": "string", "description": "Optional niche filter"},
                "status": {"type": "string", "description": "Optional status filter"}
            }
        }
    },
    {
        "name": "run_campaign",
        "description": "One-click campaign runner: search leads, scrape sites, extract contacts, log leads, and preview/send outreach emails.",
        "input_schema": {
            "type": "object",
            "properties": {
                "niche": {"type": "string", "description": "Campaign niche, e.g. roof repair, personal injury lawyers"},
                "offer": {"type": "string", "description": "Offer value prop to include in outreach"},
                "geo": {"type": "string", "description": "Optional geo focus, e.g. Portland OR"},
                "max_sites": {"type": "integer", "description": "Max sites to scan", "default": 8},
                "max_contacts_per_site": {"type": "integer", "description": "Max emails to use per site", "default": 2},
                "send_limit": {"type": "integer", "description": "Max outreach emails in this run", "default": 10},
                "dry_run": {"type": "boolean", "description": "Preview mode only; no live send", "default": True},
                "filename": {"type": "string", "description": "Lead CSV filename under workspace/profit", "default": "leads.csv"},
                "subject_template": {"type": "string", "description": "Optional Python format template with {niche},{offer},{company},{geo},{host}"},
                "body_template": {"type": "string", "description": "Optional Python format template with {niche},{offer},{company},{geo},{host}"}
            },
            "required": ["niche", "offer"]
        }
    },
    {
        "name": "execute_python",
        "description": "Execute Python code in the session workspace sandbox. Returns stdout, stderr, and any errors. Use for computation, file transforms, and project scaffolding scripts.",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Python code to execute"},
                "timeout": {"type": "integer", "description": "Timeout in seconds (default 30, max 60)", "default": 30}
            },
            "required": ["code"]
        }
    },
    {
        "name": "read_file",
        "description": "Read the contents of an uploaded file by its file_id or filename.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_id": {"type": "string", "description": "The file ID from the upload system"},
                "max_chars": {"type": "integer", "description": "Maximum characters to return (default 50000)", "default": 50000}
            },
            "required": ["file_id"]
        }
    },
    {
        "name": "list_files",
        "description": "List all files currently uploaded in this session.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "write_file",
        "description": "Write content to an artifact file. Optionally mirror to session workspace via `path`/`workspace_path`.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Name of the file to create"},
                "content": {"type": "string", "description": "Text content to write to the file"},
                "path": {"type": "string", "description": "Optional relative workspace path to also write (e.g., tests/sanity.spec.ts)"},
                "workspace_path": {"type": "string", "description": "Optional relative workspace path alias for `path`"}
            },
            "required": ["filename", "content"]
        }
    },
    {
        "name": "run_shell",
        "description": "Run a shell command inside the session workspace. Command profile is controlled by AGENT_SHELL_PROFILE: strict, project, or project_full. curl is GET-only in all profiles.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The shell command to execute"}
            },
            "required": ["command"]
        }
    },
    {
        "name": "run_project_command",
        "description": "Run a project command in the persistent session workspace and return structured stdout/stderr/exit code.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Command to run (e.g., npm install, pytest -q, uvicorn app:app --port 8000)"},
                "cwd": {"type": "string", "description": "Optional subdirectory relative to workspace"},
                "timeout": {"type": "integer", "description": "Timeout in seconds (default 300, max 1800)", "default": 300}
            },
            "required": ["command"]
        }
    },
    {
        "name": "run_tests",
        "description": "Run test command in session workspace. If command omitted, chooses a best-effort default based on project files.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Optional explicit test command (e.g., pytest -q, npm test)"},
                "cwd": {"type": "string", "description": "Optional subdirectory relative to workspace"},
                "timeout": {"type": "integer", "description": "Timeout in seconds (default 300, max 1800)", "default": 300}
            }
        }
    },
    {
        "name": "http_check",
        "description": "Issue HTTP request and return status/body preview for service smoke checks.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Absolute URL to request"},
                "method": {"type": "string", "description": "HTTP method (default GET)", "default": "GET"},
                "headers": {"type": "object", "description": "Optional request headers"},
                "body": {"type": "string", "description": "Optional request body"},
                "timeout_seconds": {"type": "number", "description": "Request timeout seconds", "default": 20},
                "expect_status": {"type": "integer", "description": "Optional expected HTTP status code"}
            },
            "required": ["url"]
        }
    },
    {
        "name": "start_process",
        "description": "Start a long-running background process in session workspace and capture logs.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Command to run in background"},
                "cwd": {"type": "string", "description": "Optional subdirectory relative to workspace"},
                "name": {"type": "string", "description": "Optional stable process id/name"}
            },
            "required": ["command"]
        }
    },
    {
        "name": "stop_process",
        "description": "Stop a tracked background process by process_id.",
        "input_schema": {
            "type": "object",
            "properties": {
                "process_id": {"type": "string", "description": "Process id returned by start_process"},
                "force": {"type": "boolean", "description": "Force kill if true", "default": False}
            },
            "required": ["process_id"]
        }
    },
    {
        "name": "list_processes",
        "description": "List tracked background processes for current session.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": "read_process_logs",
        "description": "Read tail logs for tracked background process.",
        "input_schema": {
            "type": "object",
            "properties": {
                "process_id": {"type": "string", "description": "Process id returned by start_process"},
                "tail_lines": {"type": "integer", "description": "Number of tail lines to return", "default": 200}
            },
            "required": ["process_id"]
        }
    },
    {
        "name": "run_workspace_diagnostics",
        "description": "Run workspace diagnostics for Python and TypeScript to surface LSP-like compile/type errors.",
        "input_schema": {
            "type": "object",
            "properties": {
                "cwd": {"type": "string", "description": "Optional subdirectory relative to workspace"},
                "include_python": {"type": "boolean", "description": "Include Python compile diagnostics", "default": True},
                "include_typescript": {"type": "boolean", "description": "Include TypeScript diagnostics (tsc)", "default": True},
                "timeout": {"type": "integer", "description": "Diagnostics timeout in seconds", "default": 180}
            }
        }
    },
    {
        "name": "run_playwright_test",
        "description": "Run Playwright tests in workspace (default: npx playwright test) with structured output.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Optional Playwright command override"},
                "cwd": {"type": "string", "description": "Optional subdirectory relative to workspace"},
                "timeout": {"type": "integer", "description": "Timeout in seconds (default 600, max 1800)", "default": 600}
            }
        }
    },
    {
        "name": "show_fleet_status",
        "description": "Return the normalized internal fleet inventory summary, including nodes, model families, and script-audit mismatch counts.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": "show_node_inventory",
        "description": "Return the normalized inventory object for a specific fleet node.",
        "input_schema": {
            "type": "object",
            "properties": {
                "node": {"type": "string", "description": "Node name, host alias, or host IP"}
            },
            "required": ["node"]
        }
    },
    {
        "name": "find_candidate_nodes",
        "description": "Find candidate fleet nodes for a requested capability using the normalized inventory tags, roles, and model families.",
        "input_schema": {
            "type": "object",
            "properties": {
                "requested_capability": {"type": "string", "description": "Capability or tag request, e.g. 'audio asr', 'vision', 'security'"}
            },
            "required": ["requested_capability"]
        }
    },
    {
        "name": "locate_model",
        "description": "Locate model paths from the internal fleet inventory without guessing conventions.",
        "input_schema": {
            "type": "object",
            "properties": {
                "model_name_or_tag": {"type": "string", "description": "Model name fragment or semantic tag"},
                "node": {"type": "string", "description": "Optional node filter"}
            },
            "required": ["model_name_or_tag"]
        }
    },
    {
        "name": "get_gpu_status",
        "description": "Run the audited helper path to inspect live GPU status on a target node.",
        "input_schema": {
            "type": "object",
            "properties": {
                "node": {"type": "string", "description": "Target node"},
                "dry_run": {"type": "boolean", "description": "Preview command without running it", "default": False}
            },
            "required": ["node"]
        }
    },
    {
        "name": "get_disk_status",
        "description": "Run the audited helper path to inspect live disk and mount status on a target node.",
        "input_schema": {
            "type": "object",
            "properties": {
                "node": {"type": "string", "description": "Target node"},
                "dry_run": {"type": "boolean", "description": "Preview command without running it", "default": False}
            },
            "required": ["node"]
        }
    },
    {
        "name": "get_docker_status",
        "description": "Run the audited helper path to inspect live docker and compose status on a target node.",
        "input_schema": {
            "type": "object",
            "properties": {
                "node": {"type": "string", "description": "Target node"},
                "dry_run": {"type": "boolean", "description": "Preview command without running it", "default": False}
            },
            "required": ["node"]
        }
    },
    {
        "name": "validate_compose",
        "description": "Validate compose configuration from an approved compose root on a target node.",
        "input_schema": {
            "type": "object",
            "properties": {
                "node": {"type": "string", "description": "Target node"},
                "compose_path": {"type": "string", "description": "Optional approved compose root path"},
                "dry_run": {"type": "boolean", "description": "Preview command without running it", "default": False}
            },
            "required": ["node"]
        }
    },
    {
        "name": "stop_stack",
        "description": "Stop a stack from an approved compose root. Explicit confirmation is required.",
        "input_schema": {
            "type": "object",
            "properties": {
                "node": {"type": "string", "description": "Target node"},
                "stack_name_or_path": {"type": "string", "description": "Approved compose root path or 'control' for the default root"},
                "dry_run": {"type": "boolean", "description": "Preview command without running it", "default": True},
                "confirm": {"type": "boolean", "description": "Required to execute destructive actions", "default": False}
            },
            "required": ["node"]
        }
    },
    {
        "name": "start_stack",
        "description": "Start a stack from an approved compose root. Explicit confirmation is required.",
        "input_schema": {
            "type": "object",
            "properties": {
                "node": {"type": "string", "description": "Target node"},
                "stack_name_or_path": {"type": "string", "description": "Approved compose root path or 'control' for the default root"},
                "dry_run": {"type": "boolean", "description": "Preview command without running it", "default": True},
                "confirm": {"type": "boolean", "description": "Required to execute this action", "default": False}
            },
            "required": ["node"]
        }
    },
    {
        "name": "check_stack_health",
        "description": "Check stack health from an approved compose root on a target node.",
        "input_schema": {
            "type": "object",
            "properties": {
                "node": {"type": "string", "description": "Target node"},
                "stack_name_or_path": {"type": "string", "description": "Approved compose root path or 'control' for the default root"},
                "dry_run": {"type": "boolean", "description": "Preview command without running it", "default": False}
            },
            "required": ["node"]
        }
    },
    {
        "name": "audit_fleet_scripts",
        "description": "Inspect and classify every helper script under fleet-inventory/scripts/ and report mismatches against the canonical inventory.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": "plan_model_deployment",
        "description": "Build an internal model deployment plan using the real fleet inventory, live probes, approved paths, and optional execution controls.",
        "input_schema": {
            "type": "object",
            "properties": {
                "model_name_or_tag": {"type": "string", "description": "Requested model name or semantic tag"},
                "node": {"type": "string", "description": "Optional explicit target node"},
                "repo_id": {"type": "string", "description": "Optional Hugging Face repo id for download planning"},
                "semantic_tags": {"type": "array", "items": {"type": "string"}, "description": "Optional semantic tags to steer destination selection"},
                "compose_path": {"type": "string", "description": "Optional approved compose root path"},
                "execute": {"type": "boolean", "description": "When true, execute plan steps that support execution", "default": False},
                "dry_run": {"type": "boolean", "description": "Preview mutating steps instead of executing them", "default": True},
                "confirm": {"type": "boolean", "description": "Required for approval-gated actions", "default": False}
            },
            "required": ["model_name_or_tag"]
        }
    },
    {
        "name": "get_harness_status",
        "description": "Return authoritative harness metadata: actual provider/model, tool inventory, and memory backend connectivity. Use this before describing harness capabilities.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "calculate",
        "description": "Perform mathematical calculations. Supports arithmetic, algebra, and basic statistics. Use this for precise numeric computation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Mathematical expression to evaluate, e.g. '2**32 + sqrt(144)'"}
            },
            "required": ["expression"]
        }
    },
    {
        "name": "summarize_document",
        "description": "Summarize a long document or text. Useful when a file is too large to analyze directly.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The text content to summarize"},
                "focus": {"type": "string", "description": "Optional: what aspect to focus the summary on"}
            },
            "required": ["text"]
        }
    }
]

async def _run_with_retry(fn, attempts: int = 2, base_delay: float = 0.35) -> str:
    """Retry transient tool failures with short backoff."""
    last_result = ""
    for attempt in range(1, attempts + 1):
        result = await fn()
        last_result = result
        if not str(result).startswith("Error"):
            return result
        if attempt < attempts:
            await asyncio.sleep(base_delay * attempt)
    return last_result


async def _calculate_with_fallback(expression: str, code_executor, calculator) -> str:
    """Fallback from calculator to execute_python when parsing fails."""
    calc_result = calculator.calculate(expression=expression)
    if not calc_result.startswith("Error"):
        return calc_result

    escaped_expr = json.dumps(expression)
    py_code = (
        "import math\n"
        f"expr = {escaped_expr}\n"
        "allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith('_')}\n"
        "allowed.update({'abs': abs, 'round': round, 'min': min, 'max': max, 'sum': sum, 'pow': pow})\n"
        "print(eval(expr, {'__builtins__': {}}, allowed))\n"
    )
    py_result = await code_executor.execute_python(code=py_code, timeout=10)
    if py_result.startswith("Error"):
        return calc_result
    return py_result


def _normalize_write_file_input(raw_input: dict) -> tuple[str | None, str | None, str | None, str | None]:
    """Normalize write_file payloads across native + MCP-ish schemas."""
    merged = dict(raw_input or {})

    raw_args = merged.get("_raw_arguments")
    if isinstance(raw_args, str) and raw_args.strip():
        try:
            parsed = json.loads(raw_args)
            if isinstance(parsed, dict):
                merged = {**parsed, **merged}
        except Exception:
            pass

    filename = merged.get("filename") or merged.get("name")
    workspace_path = merged.get("workspace_path")
    path_like = merged.get("path") or merged.get("file_path") or merged.get("filepath") or merged.get("uri")
    if not workspace_path and isinstance(path_like, str) and path_like.strip():
        workspace_path = path_like
    if not filename and isinstance(path_like, str) and path_like.strip():
        cleaned = path_like.replace("file://", "").strip()
        filename = Path(cleaned).name

    content = merged.get("content")
    if content is None:
        content = merged.get("text")
    if content is None:
        content = merged.get("body")
    if content is None:
        content = merged.get("contents")
    if content is None:
        content = merged.get("data")

    if isinstance(content, (dict, list)):
        content = json.dumps(content, ensure_ascii=False, indent=2)
    if content is not None and not isinstance(content, str):
        content = str(content)

    if isinstance(filename, str):
        filename = filename.strip()
    if isinstance(content, str):
        content = content

    if not filename or content is None:
        available_keys = sorted(k for k in merged.keys() if not str(k).startswith("_"))
        return (
            None,
            None,
            None,
            (
                "Error: write_file requires both 'filename' and 'content'. "
                f"Received keys: {available_keys}. "
                "Example: {\"filename\":\"report.md\",\"content\":\"...\"}"
            ),
        )

    return filename, content, str(workspace_path).strip() if workspace_path else None, None


def _normalize_shell_input(raw_input: dict) -> tuple[str | None, str | None]:
    merged = dict(raw_input or {})
    raw_args = merged.get("_raw_arguments")
    if isinstance(raw_args, str) and raw_args.strip():
        try:
            parsed = json.loads(raw_args)
            if isinstance(parsed, dict):
                merged = {**parsed, **merged}
        except Exception:
            pass

    command = merged.get("command") or merged.get("cmd") or merged.get("shell")
    if isinstance(command, str) and command.strip():
        return command.strip(), None

    keys = sorted(k for k in merged.keys() if not str(k).startswith("_"))
    return None, f"Error: run_shell requires 'command'. Received keys: {keys}. Example: {{\"command\":\"ls -la\"}}"


def _normalize_python_input(raw_input: dict) -> tuple[str | None, int, str | None]:
    merged = dict(raw_input or {})
    raw_args = merged.get("_raw_arguments")
    if isinstance(raw_args, str) and raw_args.strip():
        try:
            parsed = json.loads(raw_args)
            if isinstance(parsed, dict):
                merged = {**parsed, **merged}
        except Exception:
            pass

    code = merged.get("code") or merged.get("script") or merged.get("python")
    raw_timeout = merged.get("timeout", 30)
    timeout = 30
    try:
        timeout = int(raw_timeout)
    except Exception:
        timeout = 30

    if isinstance(code, str) and code.strip():
        return code, timeout, None

    keys = sorted(k for k in merged.keys() if not str(k).startswith("_"))
    return None, timeout, f"Error: execute_python requires 'code'. Received keys: {keys}. Example: {{\"code\":\"print(1)\"}}"


def _normalize_command_tool_input(raw_input: dict, tool_name: str) -> tuple[str | None, str | None]:
    merged = dict(raw_input or {})
    raw_args = merged.get("_raw_arguments")
    if isinstance(raw_args, str) and raw_args.strip():
        try:
            parsed = json.loads(raw_args)
            if isinstance(parsed, dict):
                merged = {**parsed, **merged}
        except Exception:
            pass
    command = merged.get("command") or merged.get("cmd")
    if isinstance(command, str) and command.strip():
        return command.strip(), None
    keys = sorted(k for k in merged.keys() if not str(k).startswith("_"))
    return None, f"Error: {tool_name} requires 'command'. Received keys: {keys}"


def _normalize_search_input(raw_input: dict, tool_name: str) -> tuple[str | None, int, str | None]:
    merged = dict(raw_input or {})
    raw_args = merged.get("_raw_arguments")
    if isinstance(raw_args, str) and raw_args.strip():
        try:
            parsed = json.loads(raw_args)
            if isinstance(parsed, dict):
                merged = {**parsed, **merged}
        except Exception:
            pass

    query = merged.get("query") or merged.get("q") or merged.get("question")
    max_results = merged.get("max_results", merged.get("count", 5))
    try:
        max_results = int(max_results)
    except Exception:
        max_results = 5

    if isinstance(query, str) and query.strip():
        return query.strip(), max_results, None
    keys = sorted(k for k in merged.keys() if not str(k).startswith("_"))
    return None, max_results, (
        f"Error: {tool_name} requires 'query'. "
        f"Received keys: {keys}. Example: {{\"query\":\"latest model releases\"}}"
    )


async def dispatch_tool(tool_name: str, tool_input: dict, session_id: str) -> str:
    """Route a tool call to its implementation and return a string result."""
    from backend.agent.tools import (
        web_search,
        code_executor,
        file_ops,
        shell,
        calculator,
        summarizer,
        project_runner,
        diagnostics,
        profit_ops,
        health_check,
        fleet_ops,
    )

    try:
        if not isinstance(tool_input, dict):
            return f"Error: Invalid input for tool '{tool_name}' (expected object)"

        disabled_tools = {
            name.strip()
            for name in os.getenv("DISABLED_TOOLS", "").split(",")
            if name.strip()
        }
        if tool_name in disabled_tools:
            return f"Error: Tool '{tool_name}' is disabled by policy"

        if tool_name == "web_search":
            query, max_results, search_error = _normalize_search_input(tool_input, "web_search")
            if search_error:
                return search_error
            return await _run_with_retry(lambda: web_search.web_search(
                query=query,
                max_results=max_results
            ))
        elif tool_name == "search_web":
            query, max_results, search_error = _normalize_search_input(tool_input, "search_web")
            if search_error:
                return search_error
            return await _run_with_retry(lambda: web_search.web_search(
                query=query,
                max_results=max_results
            ))
        elif tool_name == "tavily_search":
            query, max_results, search_error = _normalize_search_input(tool_input, "tavily_search")
            if search_error:
                return search_error
            return await _run_with_retry(lambda: web_search.tavily_search(
                query=query,
                max_results=max_results
            ))
        elif tool_name == "brave_search":
            query, max_results, search_error = _normalize_search_input(tool_input, "brave_search")
            if search_error:
                return search_error
            return await _run_with_retry(lambda: web_search.brave_search(
                query=query,
                max_results=max_results
            ))
        elif tool_name == "scrape_page":
            return await _run_with_retry(
                lambda: profit_ops.scrape_page(
                    url=tool_input.get("url", ""),
                    max_chars=tool_input.get("max_chars", 120000),
                )
            )
        elif tool_name == "extract_contacts":
            return await _run_with_retry(
                lambda: profit_ops.extract_contacts(
                    html=tool_input.get("html"),
                    url=tool_input.get("url"),
                )
            )
        elif tool_name == "send_email":
            return await _run_with_retry(
                lambda: profit_ops.send_email(
                    to=tool_input.get("to", ""),
                    subject=tool_input.get("subject", ""),
                    body=tool_input.get("body", ""),
                    cc=tool_input.get("cc"),
                    bcc=tool_input.get("bcc"),
                    reply_to=tool_input.get("reply_to"),
                    from_email=tool_input.get("from_email"),
                    from_name=tool_input.get("from_name"),
                    dry_run=bool(tool_input.get("dry_run", True)),
                )
            )
        elif tool_name == "log_lead":
            return await _run_with_retry(
                lambda: profit_ops.log_lead(
                    session_id=session_id,
                    company=tool_input.get("company", ""),
                    email=tool_input.get("email", ""),
                    niche=tool_input.get("niche", ""),
                    website=tool_input.get("website", ""),
                    source_url=tool_input.get("source_url", ""),
                    status=tool_input.get("status", "new"),
                    notes=tool_input.get("notes", ""),
                    filename=tool_input.get("filename", "leads.csv"),
                )
            )
        elif tool_name == "list_leads":
            return await _run_with_retry(
                lambda: profit_ops.list_leads(
                    session_id=session_id,
                    filename=tool_input.get("filename", "leads.csv"),
                    limit=tool_input.get("limit", 100),
                    niche=tool_input.get("niche"),
                    status=tool_input.get("status"),
                )
            )
        elif tool_name == "run_campaign":
            return await _run_with_retry(
                lambda: profit_ops.run_campaign(
                    session_id=session_id,
                    niche=tool_input.get("niche", ""),
                    offer=tool_input.get("offer", ""),
                    geo=tool_input.get("geo", ""),
                    max_sites=tool_input.get("max_sites", 8),
                    max_contacts_per_site=tool_input.get("max_contacts_per_site", 2),
                    dry_run=bool(tool_input.get("dry_run", True)),
                    send_limit=tool_input.get("send_limit", 10),
                    filename=tool_input.get("filename", "leads.csv"),
                    subject_template=tool_input.get("subject_template"),
                    body_template=tool_input.get("body_template"),
                )
            )
        elif tool_name == "execute_python":
            code, timeout, py_error = _normalize_python_input(tool_input)
            if py_error:
                return py_error
            return await _run_with_retry(lambda: code_executor.execute_python(
                code=code,
                timeout=timeout,
                session_id=session_id,
            ))
        elif tool_name == "read_file":
            return await file_ops.read_file(
                file_id=tool_input["file_id"],
                max_chars=tool_input.get("max_chars", 50000)
            )
        elif tool_name == "list_files":
            return await file_ops.list_files(session_id=session_id)
        elif tool_name == "write_file":
            filename, content, workspace_path, write_error = _normalize_write_file_input(tool_input)
            if write_error:
                return write_error
            return await file_ops.write_file(
                filename=filename,
                content=content,
                session_id=session_id,
                workspace_path=workspace_path,
            )
        elif tool_name == "run_shell":
            command, shell_error = _normalize_shell_input(tool_input)
            if shell_error:
                return shell_error
            return await _run_with_retry(
                lambda: shell.run_shell(command=command, session_id=session_id)
            )
        elif tool_name == "run_project_command":
            command, cmd_error = _normalize_command_tool_input(tool_input, "run_project_command")
            if cmd_error:
                return cmd_error
            return await _run_with_retry(
                lambda: project_runner.run_project_command(
                    session_id=session_id,
                    command=command,
                    cwd=tool_input.get("cwd"),
                    timeout=tool_input.get("timeout", 300),
                )
            )
        elif tool_name == "run_tests":
            return await _run_with_retry(
                lambda: project_runner.run_tests(
                    session_id=session_id,
                    command=tool_input.get("command"),
                    cwd=tool_input.get("cwd"),
                    timeout=tool_input.get("timeout", 300),
                )
            )
        elif tool_name == "http_check":
            return await _run_with_retry(
                lambda: project_runner.http_check(
                    url=tool_input["url"],
                    method=tool_input.get("method", "GET"),
                    headers=tool_input.get("headers"),
                    body=tool_input.get("body"),
                    timeout_seconds=tool_input.get("timeout_seconds", 20),
                    expect_status=tool_input.get("expect_status"),
                )
            )
        elif tool_name == "start_process":
            command, cmd_error = _normalize_command_tool_input(tool_input, "start_process")
            if cmd_error:
                return cmd_error
            return await _run_with_retry(
                lambda: project_runner.start_process(
                    session_id=session_id,
                    command=command,
                    cwd=tool_input.get("cwd"),
                    name=tool_input.get("name"),
                )
            )
        elif tool_name == "stop_process":
            return await _run_with_retry(
                lambda: project_runner.stop_process(
                    session_id=session_id,
                    process_id=str(tool_input.get("process_id") or ""),
                    force=bool(tool_input.get("force", False)),
                )
            )
        elif tool_name == "list_processes":
            return await _run_with_retry(
                lambda: project_runner.list_processes(session_id=session_id)
            )
        elif tool_name == "read_process_logs":
            return await _run_with_retry(
                lambda: project_runner.read_process_logs(
                    session_id=session_id,
                    process_id=str(tool_input.get("process_id") or ""),
                    tail_lines=tool_input.get("tail_lines", 200),
                )
            )
        elif tool_name == "run_workspace_diagnostics":
            return await _run_with_retry(
                lambda: diagnostics.run_workspace_diagnostics(
                    session_id=session_id,
                    cwd=tool_input.get("cwd"),
                    include_python=bool(tool_input.get("include_python", True)),
                    include_typescript=bool(tool_input.get("include_typescript", True)),
                    timeout=tool_input.get("timeout", 180),
                )
            )
        elif tool_name == "run_playwright_test":
            return await _run_with_retry(
                lambda: diagnostics.run_playwright_test(
                    session_id=session_id,
                    command=tool_input.get("command"),
                    cwd=tool_input.get("cwd"),
                    timeout=tool_input.get("timeout", 600),
                )
            )
        elif tool_name == "show_fleet_status":
            return await _run_with_retry(fleet_ops.show_fleet_status)
        elif tool_name == "show_node_inventory":
            return await _run_with_retry(
                lambda: fleet_ops.show_node_inventory(node=str(tool_input.get("node") or ""))
            )
        elif tool_name == "find_candidate_nodes":
            return await _run_with_retry(
                lambda: fleet_ops.find_candidate_nodes(
                    requested_capability=str(tool_input.get("requested_capability") or "")
                )
            )
        elif tool_name == "locate_model":
            return await _run_with_retry(
                lambda: fleet_ops.locate_model(
                    model_name_or_tag=str(tool_input.get("model_name_or_tag") or ""),
                    node=tool_input.get("node"),
                )
            )
        elif tool_name == "get_gpu_status":
            return await _run_with_retry(
                lambda: fleet_ops.get_gpu_status(
                    node=str(tool_input.get("node") or ""),
                    dry_run=bool(tool_input.get("dry_run", False)),
                )
            )
        elif tool_name == "get_disk_status":
            return await _run_with_retry(
                lambda: fleet_ops.get_disk_status(
                    node=str(tool_input.get("node") or ""),
                    dry_run=bool(tool_input.get("dry_run", False)),
                )
            )
        elif tool_name == "get_docker_status":
            return await _run_with_retry(
                lambda: fleet_ops.get_docker_status(
                    node=str(tool_input.get("node") or ""),
                    dry_run=bool(tool_input.get("dry_run", False)),
                )
            )
        elif tool_name == "validate_compose":
            return await _run_with_retry(
                lambda: fleet_ops.validate_compose(
                    node=str(tool_input.get("node") or ""),
                    compose_path=tool_input.get("compose_path"),
                    dry_run=bool(tool_input.get("dry_run", False)),
                )
            )
        elif tool_name == "stop_stack":
            return await _run_with_retry(
                lambda: fleet_ops.stop_stack(
                    node=str(tool_input.get("node") or ""),
                    stack_name_or_path=tool_input.get("stack_name_or_path"),
                    dry_run=bool(tool_input.get("dry_run", True)),
                    confirm=bool(tool_input.get("confirm", False)),
                )
            )
        elif tool_name == "start_stack":
            return await _run_with_retry(
                lambda: fleet_ops.start_stack(
                    node=str(tool_input.get("node") or ""),
                    stack_name_or_path=tool_input.get("stack_name_or_path"),
                    dry_run=bool(tool_input.get("dry_run", True)),
                    confirm=bool(tool_input.get("confirm", False)),
                )
            )
        elif tool_name == "check_stack_health":
            return await _run_with_retry(
                lambda: fleet_ops.check_stack_health(
                    node=str(tool_input.get("node") or ""),
                    stack_name_or_path=tool_input.get("stack_name_or_path"),
                    dry_run=bool(tool_input.get("dry_run", False)),
                )
            )
        elif tool_name == "audit_fleet_scripts":
            return await _run_with_retry(fleet_ops.audit_fleet_scripts)
        elif tool_name == "plan_model_deployment":
            return await _run_with_retry(
                lambda: fleet_ops.plan_model_deployment(
                    model_name_or_tag=str(tool_input.get("model_name_or_tag") or ""),
                    node=tool_input.get("node"),
                    repo_id=tool_input.get("repo_id"),
                    semantic_tags=tool_input.get("semantic_tags"),
                    compose_path=tool_input.get("compose_path"),
                    execute=bool(tool_input.get("execute", False)),
                    dry_run=bool(tool_input.get("dry_run", True)),
                    confirm=bool(tool_input.get("confirm", False)),
                )
            )
        elif tool_name == "get_harness_status":
            return await _run_with_retry(health_check.get_harness_status)
        elif tool_name == "calculate":
            return await _run_with_retry(
                lambda: _calculate_with_fallback(tool_input["expression"], code_executor, calculator)
            )
        elif tool_name == "summarize_document":
            return await _run_with_retry(lambda: summarizer.summarize_document(
                text=tool_input["text"],
                focus=tool_input.get("focus")
            ))
        else:
            return f"Error: Unknown tool '{tool_name}'"
    except Exception as e:
        return f"Error executing tool '{tool_name}': {str(e)}"

# AetherOps Agentic Harness

A production-grade autonomous AI harness with a Next.js frontend and FastAPI backend.

## Architecture Docs

- Technical reference: `docs/AetherOps-Harness-Technical-Reference.md`
- Public capabilities brief: `docs/AetherOps-Harness-Public-Capabilities.md`
- Identity/state pattern: `docs/Identity-Memory-Bootstrap-Pattern.md`

## Features

- **Model-Agnostic Providers** - Supports Anthropic-compatible and OpenAI-compatible backends
- **Provider Abstraction** - Swap between Anthropic-compatible and OpenAI-compatible backends via env vars
- **Streaming Reasoning + Tooling** - Full SSE stream of thinking, tool calls, and tool results
- **Tool Calling** - Autonomous agentic loop with multiple tools:
  - Web Search (DuckDuckGo)
  - Python Code Execution (sandboxed)
  - File Operations (read, write, list)
  - Shell Commands (restricted whitelist)
  - Calculator (safe math evaluation)
  - Document Summarization
- **Server-Sent Events (SSE)** - Real-time streaming of thinking, text, and tool calls
- **Artifact Streaming** - Files created by the agent are emitted as artifact events and rendered in the right sidebar
- **File Uploads** - Support for text, PDF, and DOCX files
- **Session Management** - Persistent conversation history per session
- **Identity Bootstrap** - Optional first-boot operator/agent identity capture from `agent_identity` docs
- **Replay Logging** - Per-session JSONL traces for observability and replay
- **Context Compaction + State Ledger** - Long conversations are compacted while goal/progress/tool state remains persistent
- **Modern UI** - Dark theme with a clean, developer-grade interface

## Prerequisites

- Python 3.10+
- Node.js 18+
- API key for your selected model gateway/provider

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:3000
The backend API will be available at http://localhost:8000

### Using the Start Script

```bash
chmod +x start.sh
./start.sh
```

### Docker (Backend + Frontend)

```bash
docker compose up --build
```

Default Docker host ports are high to avoid conflicts:
- Frontend: http://localhost:33333
- Backend API: http://localhost:38333

Optional overrides:
```bash
HARNESS_FRONTEND_PORT=43100 HARNESS_BACKEND_PORT=48100 docker compose up --build
```

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/chat` - SSE streaming chat endpoint
- `POST /api/files/upload` - Upload a file
- `GET /api/files/{session_id}` - List files for a session
- `DELETE /api/files/{file_id}` - Delete a file
- `GET /api/files/download/{file_id}` - Download an uploaded/generated file
- `GET /api/replay/{session_id}` - List replay traces for a session
- `GET /api/replay/{session_id}/{filename}` - Read replay trace lines

## Environment Variables

### Backend (.env)
```
AGENT_PROVIDER=openai
AGENT_MODEL=your-model-name

# Direct OpenAI provider (when AGENT_PROVIDER=openai)
# OPENAI_BASE_URL=https://api.openai.com/v1
# OPENAI_API_KEY=your_openai_key

# Optional ordered failover before final error
# AGENT_ENABLE_FALLBACK=true
# AGENT_FALLBACK_PROVIDER=openai_compat
# AGENT_FALLBACK_BASE_URL=https://api.aetherpro.tech/v1
# AGENT_FALLBACK_API_KEY=router_key
# AGENT_FALLBACK_MODEL=known-good-local-model

# Anthropic-compatible provider
# PROVIDER_ANTHROPIC_API_KEY=your_api_key_here
# PROVIDER_ANTHROPIC_BASE_URL=https://api.anthropic.com

# OpenAI-compatible provider (when AGENT_PROVIDER=openai_compat)
# OPENAI_COMPAT_BASE_URL=https://api.aetherpro.tech/v1
# OPENAI_COMPAT_API_KEY=your_openai_compat_key
# OPENAI_COMPAT_ENABLE_THINKING=false
# OPENAI_COMPAT_CONTEXT_WINDOW=8192
# OPENAI_COMPAT_MODEL=qwen3.5-35b

# Unified gateway model aliases (legacy LiteLLM env names kept only as model catalog aliases)
# LITELLM_MODEL_BASE_URL=https://api.aetherpro.tech/v1
# LITELLM_API_KEY=router1_key
# LITELLM_MODEL_NAME=model-on-gateway
# LITELLM_MODEL_NAMES=model-a,model-b,openai/qwen3.5-122

MAX_AGENT_ITERATIONS=60
MAX_TOOL_CALLS_PER_ITERATION=12
MAX_TOOL_CALLS_PER_RUN=120
MAX_HISTORY_CHARS_FOR_MODEL=180000
STRICT_VERIFICATION_MODE=true
ENABLE_REPLAY_LOGS=true
DISABLED_TOOLS=

# Optional prompt overrides
# SYSTEM_PROMPT_PATH=/app/backend/prompts/system_prompt.md
# TOOL_EVALUATION_PROMPT_PATH=/app/backend/prompts/tool_evaluation_prompt.md
```

### Frontend (.env.local)
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:38333
```

## Project Structure

```
mini-agent/
├── backend/
│   ├── Dockerfile           # Backend container image
│   ├── main.py              # FastAPI app entry point
│   ├── agent/
│   │   ├── runner.py        # Agentic loop with streaming reasoning + tools
│   │   └── tools/           # Tool implementations
│   │       ├── registry.py
│   │       ├── web_search.py
│   │       ├── code_executor.py
│   │       ├── file_ops.py
│   │       ├── shell.py
│   │       ├── calculator.py
│   │       └── summarizer.py
│   ├── prompts/             # Editable prompt files
│   │   ├── system_prompt.md
│   │   └── tool_evaluation_prompt.md
│   ├── api/                 # API endpoints
│   │   ├── chat.py
│   │   ├── files.py
│   │   └── health.py
│   └── models/              # Data models
│       ├── schemas.py
│       └── session.py
├── frontend/
│   ├── Dockerfile           # Frontend container image
│   ├── src/
│   │   ├── app/              # Next.js app router
│   │   ├── components/      # React components
│   │   ├── hooks/            # Custom hooks
│   │   └── lib/              # Utilities
│   └── package.json
├── docker-compose.yml       # One-command local stack startup
├── start.sh                 # Start both services
└── README.md
```

## Usage

1. Open http://localhost:3000 in your browser
2. Start typing messages or upload files
3. The agent will autonomously use tools as needed

Example prompts:
- "Search the web for the latest AI news"
- "Write and run Python code to calculate factorial of 100"
- "Calculate the square root of 12345"
- "Summarize this document"

## Notes

- The harness streams reasoning and tool events in real time while preserving execution state
- Maximum agent iterations are configurable via `MAX_AGENT_ITERATIONS` (default: 60)
- File uploads support: txt, md, py, js, ts, json, csv, yaml, html, xml, sh, pdf, docx
- Shell commands are restricted to a safe whitelist (including diagnostics like `which`, `find`, `sed`, `awk`, `jq`)
- Generated artifacts include validation metadata (CSV/JSON/Python/Markdown checks)
- Backend image includes Chromium runtime libraries so Playwright browser tests can execute in-container after rebuild

## Deterministic Eval Suite

Run deterministic harness checks (tooling + provider config):

```bash
python backend/evals/run_eval_suite.py --report backend/evals/reports/latest.json
```

Optional live provider contract call:

```bash
python backend/evals/run_eval_suite.py --live-provider --report backend/evals/reports/live.json
```

Run all discovered LiteLLM targets/models:

```bash
python backend/evals/run_provider_matrix.py
```

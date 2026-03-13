# MiniMax M2.5 Agent — Claude Code Build Prompt

---

## CONTEXT & OVERVIEW

You are building a **production-grade, autonomous MiniMax M2.5 Agent** with a full Next.js frontend and a Python FastAPI backend. This is NOT a simple chatbot — it is a multi-turn, tool-calling agentic system that uses MiniMax's recommended Anthropic SDK integration, properly handles Interleaved Thinking (MiniMax's chain-of-thought between tool calls), and supports real file uploads.

The project folder is called `minimax-agent`. It already contains a `.env` file with two keys:

```
MINIMAX_API_KEY=<the standard platform key with balance — use this>
MINIMAX_CODING_API_KEY=<the coding plan key — do NOT use for this agent>
```

**Important API facts you must encode correctly:**
- Base URL for international users: `https://api.minimax.io/anthropic` (Anthropic SDK mode)
- Default model: `MiniMax-M2.5` (latest flagship). Fallback: `MiniMax-M2.1`
- The Anthropic SDK is MiniMax's **recommended** integration method for M2.5
- MiniMax M2.5 uses **Interleaved Thinking** — the model reasons BETWEEN every tool call. This is the model's most critical performance feature. You MUST preserve the full `response.content` list (including all `thinking` blocks) when appending assistant messages to history, or model performance degrades severely.
- Inference params for best performance: `temperature=1.0`, `top_p=0.95`, `max_tokens=16384` for agentic tasks
- The model's `stop_reason` will be `"tool_use"` when it wants to call a tool, `"end_turn"` when done

---

## PROJECT STRUCTURE

```
minimax-agent/
├── .env                          # Already exists — keys are there
├── backend/
│   ├── main.py                   # FastAPI app entry point
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── runner.py             # Core agentic loop
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── registry.py       # Tool registry and dispatcher
│   │   │   ├── web_search.py     # Web search tool
│   │   │   ├── code_executor.py  # Python code execution (sandboxed)
│   │   │   ├── file_ops.py       # File read/write/list
│   │   │   ├── shell.py          # Shell command tool (restricted)
│   │   │   ├── calculator.py     # Math/calculator tool
│   │   │   └── summarizer.py     # Document summarization tool
│   ├── api/
│   │   ├── __init__.py
│   │   ├── chat.py               # /api/chat SSE streaming endpoint
│   │   ├── files.py              # /api/files upload/list/delete
│   │   └── health.py             # /api/health
│   ├── models/
│   │   ├── schemas.py            # Pydantic request/response models
│   │   └── session.py            # In-memory session/conversation store
│   └── requirements.txt
├── frontend/
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── src/
│       ├── app/
│       │   ├── layout.tsx
│       │   ├── page.tsx
│       │   └── globals.css
│       ├── components/
│       │   ├── ChatWindow.tsx        # Main chat message display
│       │   ├── MessageBubble.tsx     # Individual message with thinking toggle
│       │   ├── InputBar.tsx          # Prompt input + file attach + send
│       │   ├── FileAttachments.tsx   # File chip display before send
│       │   ├── ThinkingBlock.tsx     # Collapsible thinking/reasoning display
│       │   ├── ToolCallCard.tsx      # Visual tool call + result display
│       │   ├── Sidebar.tsx           # Conversation history list
│       │   └── StatusBar.tsx         # Model info, token usage
│       ├── hooks/
│       │   ├── useChat.ts            # Core chat logic, SSE consumption
│       │   └── useFiles.ts           # File upload management
│       └── lib/
│           ├── api.ts                # Backend API client
│           └── types.ts              # Shared TypeScript types
└── docker-compose.yml               # Optional: containerize both services
```

---

## BACKEND REQUIREMENTS

### 1. Dependencies (`requirements.txt`)

```
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
anthropic>=0.40.0
python-multipart>=0.0.12
python-dotenv>=1.0.0
httpx>=0.27.0
aiofiles>=23.0.0
pydantic>=2.0.0
duckduckgo-search>=6.0.0
```

### 2. FastAPI Application (`main.py`)

- Load environment variables from `.env` using `python-dotenv`
- Mount CORS middleware allowing `http://localhost:3000`
- Include routers: `/api/chat`, `/api/files`, `/api/health`
- The `MINIMAX_API_KEY` env var is the standard platform key — pass it as the Anthropic SDK key
- Set Anthropic `base_url` to `https://api.minimax.io/anthropic`

### 3. Anthropic Client Setup

```python
import anthropic
import os

client = anthropic.Anthropic(
    api_key=os.environ["MINIMAX_API_KEY"],
    base_url="https://api.minimax.io/anthropic"
)
```

This is the ONLY correct way to instantiate the client. The SDK handles all headers automatically.

### 4. Agentic Loop (`agent/runner.py`)

This is the core of the system. Implement a proper autonomous agentic loop:

```python
async def run_agent(
    session_id: str,
    user_message: str,
    file_ids: list[str],  # uploaded file IDs to include in context
    stream_callback: callable  # async callback to stream events to frontend
) -> None:
```

**The loop must work as follows:**

1. Build the messages array from session history + new user message
2. If file_ids present, attach file contents to the user message content (read file text, inject as text blocks)
3. Call `client.messages.create()` with:
   - `model="MiniMax-M2.5"`
   - `max_tokens=16384`
   - `temperature=1.0`
   - `tools=TOOL_DEFINITIONS` (all registered tools)
   - Full `messages` history
4. Stream events to frontend via the callback (see streaming section below)
5. If `stop_reason == "tool_use"`:
   - Extract all `tool_use` blocks from `response.content`
   - **CRITICAL**: Append the FULL `response.content` list to messages as the assistant turn — do NOT strip thinking blocks
   - Execute each tool call (dispatch via registry)
   - Append tool results as a `user` message with `tool_result` content blocks
   - Loop back to step 3
6. If `stop_reason == "end_turn"`: done. Save final assistant message to session.
7. Implement a max iteration guard (default: 15 iterations) to prevent infinite loops

**Interleaved Thinking preservation** — this is non-negotiable. The assistant message appended must look exactly like:
```python
messages.append({
    "role": "assistant",
    "content": response.content  # The raw list of blocks from Anthropic SDK
})
```

### 5. Tool Registry (`agent/tools/registry.py`)

Define all tools in Anthropic tool schema format and a dispatcher:

```python
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
        "name": "execute_python",
        "description": "Execute Python code in a sandboxed environment. Returns stdout, stderr, and any errors. Use for math, data analysis, string processing, and computation.",
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
        "description": "Write content to a file and save it. Returns the file_id of the saved file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Name of the file to create"},
                "content": {"type": "string", "description": "Text content to write to the file"}
            },
            "required": ["filename", "content"]
        }
    },
    {
        "name": "run_shell",
        "description": "Run a safe, restricted shell command. Only allows: ls, pwd, cat, head, tail, grep, wc, echo, date, curl (GET only). Returns stdout and stderr.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The shell command to execute"}
            },
            "required": ["command"]
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

async def dispatch_tool(tool_name: str, tool_input: dict, session_id: str) -> str:
    """Route a tool call to its implementation and return a string result."""
    ...
```

### 6. Tool Implementations

**`web_search.py`**: Use `duckduckgo_search` library:
```python
from duckduckgo_search import DDGS
async def web_search(query: str, max_results: int = 5) -> str:
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
    # Format as readable numbered list with title, url, snippet
    return formatted_results_string
```

**`code_executor.py`**: Use `subprocess` with strict timeout and restricted environment. Capture stdout/stderr. Disallow network calls, file system writes outside `/tmp`. Return formatted result with stdout, stderr, execution time.

**`file_ops.py`**: Manage files stored in `./uploads/` directory (keyed by session_id + filename). `read_file` reads the text. `write_file` saves and returns a download-ready path. `list_files` returns JSON of current session files.

**`shell.py`**: Whitelist approach — only allowed commands listed above. Parse command and reject anything not on whitelist. Use `subprocess` with 15s timeout.

**`calculator.py`**: Use Python's `eval()` with a restricted namespace containing only `math` functions (`sqrt`, `sin`, `cos`, `log`, `pi`, `e`, etc.) and basic operators. Never eval arbitrary code.

**`summarizer.py`**: Chunk text and recursively summarize using a second (lightweight) call to MiniMax with no tools and a low max_tokens.

### 7. Streaming Endpoint (`api/chat.py`)

Implement as **Server-Sent Events (SSE)** using FastAPI's `StreamingResponse`:

- Endpoint: `POST /api/chat`
- Request body: `{ session_id, message, file_ids[] }`
- Response: `text/event-stream`

Events to stream (as JSON-encoded SSE data):
```
event: thinking
data: {"block_index": 0, "text": "...thinking text..."}

event: text
data: {"text": "...response text..."}

event: tool_call
data: {"tool_name": "web_search", "tool_id": "...", "input": {...}}

event: tool_result
data: {"tool_id": "...", "result": "..."}

event: done
data: {"total_input_tokens": 1234, "total_output_tokens": 567, "iterations": 3}

event: error
data: {"message": "...error message..."}
```

Each event is flushed immediately so the frontend updates in real-time.

### 8. File Upload Endpoint (`api/files.py`)

- `POST /api/files/upload`: Accept `multipart/form-data`. Save file to `./uploads/{session_id}/`. Return `{ file_id, filename, size, content_type }`.
- `GET /api/files/{session_id}`: List all files for a session.
- `DELETE /api/files/{file_id}`: Delete a file.
- Supported types: txt, md, pdf (extract text with PyMuPDF if available, else read raw), py, js, ts, json, csv, yaml, html, xml, docx (extract text if possible)
- Max file size: 50MB

### 9. Session Management (`models/session.py`)

Use a simple in-memory dict (production would use Redis, but in-memory is fine for now):
```python
sessions: dict[str, list] = {}  # session_id -> messages list

def get_history(session_id: str) -> list: ...
def add_message(session_id: str, message: dict) -> None: ...
def clear_session(session_id: str) -> None: ...
def create_session() -> str:  # returns new UUID session_id
```

---

## FRONTEND REQUIREMENTS

### Tech Stack

- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS**
- **shadcn/ui** components (use `npx shadcn@latest init` during setup)

### Design Aesthetic

Dark theme by default. Clean, professional, developer-grade UI. Think a cross between Claude.ai and a terminal-powered agent dashboard. Color palette: dark slate backgrounds (`#0F1117`, `#1A1D2E`), subtle borders, purple/violet accent for MiniMax branding, cyan for tool calls, amber for thinking blocks.

### Core Components

**`ChatWindow.tsx`**:
- Scrollable message list
- Auto-scroll to bottom on new content
- Loading skeleton while agent is running
- Empty state with suggested prompts (e.g., "Search the web for...", "Write and run Python code to...", "Analyze this file...")

**`MessageBubble.tsx`**:
- User messages: right-aligned, accent bg
- Assistant messages: left-aligned, with avatar
- Each message can contain: thinking blocks, text, tool calls, tool results
- Timestamps
- Copy button on hover

**`ThinkingBlock.tsx`**:
- Collapsible accordion — collapsed by default showing "💭 Thinking..." with pulse animation while streaming
- Expand to show full reasoning text
- Styled in amber/orange to distinguish from regular text
- Show token count when collapsed

**`ToolCallCard.tsx`**:
- Shows tool name with icon (🔍 for search, 🐍 for python, 📁 for file, etc.)
- Shows input parameters in a code block
- Shows result in a collapsible section
- Cyan accent border
- Animate in with a subtle slide

**`InputBar.tsx`**:
- Multi-line textarea (grows with content, max 6 lines)
- Paperclip icon button for file attachment
- Send button (disabled while agent is running)
- Keyboard: `Enter` to send, `Shift+Enter` for newline
- Character/token estimate counter
- "Agent is thinking..." animated status while running

**`FileAttachments.tsx`**:
- Show attached files as chips above input bar before sending
- Each chip: filename, size, type icon, remove X button
- Drag-and-drop support for the entire chat area

**`Sidebar.tsx`**:
- List of past conversations (keyed by session_id stored in localStorage)
- "New Chat" button at top
- Active session highlighted
- Session title = first user message (truncated to 40 chars)
- Clear all sessions button

**`StatusBar.tsx`**:
- Bottom bar showing: current model (`MiniMax-M2.5`), token usage (input/output), iteration count, response time

### SSE Consumption Hook (`hooks/useChat.ts`)

```typescript
const useChat = (sessionId: string) => {
  // State: messages[], isLoading, currentThinking, error
  // sendMessage(text, fileIds[]) -> opens SSE stream, processes events
  // Each event type updates state accordingly
  // Thinking block: update in-place as text streams in
  // Tool calls: append ToolCallCard with loading state, update with result
  // Text: stream character by character into current assistant message
}
```

Handle SSE events:
- `thinking` → update active thinking block (append text)
- `text` → append to current assistant message text
- `tool_call` → add new ToolCallCard with loading spinner
- `tool_result` → resolve matching ToolCallCard with result content
- `done` → finalize message, update status bar with token counts
- `error` → show error toast/alert

### Pages

**`app/page.tsx`**: Main layout — sidebar on left, chat window in center. Responsive: sidebar collapses on mobile. On first load, auto-create a new session_id (UUID) and store in localStorage.

---

## ENVIRONMENT CONFIGURATION

### Backend `.env` (already exists — do not overwrite, just read it)
```
MINIMAX_API_KEY=...           # Standard platform API key — USE THIS
MINIMAX_CODING_API_KEY=...   # Coding plan key — DO NOT USE for this agent
```

### Frontend (`.env.local`)
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

---

## STARTUP SCRIPTS

Create a `README.md` with clear setup instructions:

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npx shadcn@latest init  # if not already done
npm run dev  # runs on port 3000
```

Also create a root-level `start.sh`:
```bash
#!/bin/bash
cd backend && uvicorn main:app --port 8000 &
cd frontend && npm run dev &
wait
```

---

## SYSTEM PROMPT FOR THE AGENT

Inject this as the system prompt in every API call:

```
You are an autonomous AI agent powered by MiniMax M2.5, built by AetherPro Technologies. You have access to a comprehensive set of tools: web search, Python code execution, file operations, shell commands, calculator, and document summarization.

You operate in an agentic loop — you can use tools multiple times, chain tool calls, and reason between each action using your thinking capability. Always use tools when they would give you better information than your training data. Think carefully before each action.

Guidelines:
- For any factual question that requires current data, use web_search first
- For math and computation, use execute_python or calculate — never approximate
- When a user uploads a file, always read_file before attempting to answer questions about it
- After tool calls, reflect on the result and decide if more information is needed before answering
- Be thorough but efficient — don't call tools unnecessarily
- Format responses clearly using markdown
- When writing code for the user (not for execution), use proper markdown code blocks
```

---

## QUALITY REQUIREMENTS

1. **No mock data** — every tool must actually execute. The web search tool must return real results. The code executor must actually run code.
2. **Error handling everywhere** — every tool must return structured errors, never crash the agentic loop. If a tool fails, the agent gets the error as the tool result and can recover.
3. **Multi-turn continuity** — conversation history is fully preserved per session. The agent remembers context across many turns.
4. **Interleaved Thinking is non-negotiable** — never strip thinking blocks from history. This is why MiniMax recommends the Anthropic SDK — it naturally handles thinking block types.
5. **Streaming is real** — SSE events must flush immediately. Do not buffer the full response.
6. **File uploads work** — text extraction from PDFs and common document types must be implemented.
7. **Production-quality code** — proper async/await, no blocking calls in async context, proper exception handling, typed Pydantic models for all API request/response shapes.

---

## IMPLEMENTATION ORDER

Build in this order to ensure things work incrementally:

1. Backend `main.py` + `health.py` — verify server starts
2. `agent/tools/` — implement and unit-test each tool independently
3. `agent/runner.py` — agentic loop with a test in `__main__` block (run from CLI first)
4. `api/chat.py` — SSE streaming endpoint; test with `curl`
5. `api/files.py` — file upload; test with `curl`
6. `models/session.py` + `models/schemas.py`
7. Frontend scaffolding (Next.js + Tailwind + shadcn setup)
8. `hooks/useChat.ts` + `lib/api.ts`
9. UI components in order: InputBar → ChatWindow → MessageBubble → ThinkingBlock → ToolCallCard
10. Sidebar + StatusBar
11. End-to-end test: upload a file, ask a question about it, ask the agent to search the web, run code

---

## NOTES & GOTCHAS

- **Do not use the Coding Plan API key** (`MINIMAX_CODING_API_KEY`) for this agent. That key is for IDE coding tools (Cursor/Cline/Claude Code) and is metered differently. Always use `MINIMAX_API_KEY`.
- MiniMax's Anthropic-compatible endpoint is at `https://api.minimax.io/anthropic` — the SDK's default `api.anthropic.com` will NOT work. The `base_url` override is required.
- The model name string is `"MiniMax-M2.5"` (not a Claude model name) — pass it exactly as-is to `client.messages.create(model=...)`.
- Thinking blocks have `type="thinking"` and a `signature` field in the Anthropic SDK response — preserve both when appending to history.
- DuckDuckGo search (`duckduckgo-search` package) has rate limits — add a 1-second sleep between rapid successive calls.
- File text extraction: for PDFs, try `import fitz` (PyMuPDF) — if not installed, fall back to reading raw bytes and returning a notice. For `.docx`, try `python-docx`. For all other text-based formats (txt, md, py, js, json, csv, yaml, html), just read as UTF-8.
- The calculator tool must use a restricted `eval` — never eval raw user input. Provide a safe math namespace only.
- Code execution sandbox: use `subprocess.run` with `timeout`, redirect to `/tmp` working dir, set environment with minimal vars. Consider using `resource` module to cap memory on Linux.

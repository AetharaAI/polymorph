"""
═══════════════════════════════════════════════════════════════════════
RUNNER.PY INTEGRATION PATCH
How to wire MemoryService into your existing runner.py
═══════════════════════════════════════════════════════════════════════

Add these changes to backend/agent/runner.py
"""

# ─────────────────────────────────────────────
# 1. ADD TO IMPORTS (top of runner.py)
# ─────────────────────────────────────────────

from backend.memory.service import get_memory_service

# ─────────────────────────────────────────────
# 2. UPDATE run_agent() SIGNATURE & BODY
# ─────────────────────────────────────────────

async def run_agent(
    session_id: str,
    user_message: str,
    file_ids: list[str],
    stream_callback: callable
) -> None:

    memory = await get_memory_service()

    # ── Ensure session exists in Redis + Postgres
    if not await memory.working.session_exists(session_id):
        await memory.start_session(session_id, model="MiniMax-M2.5")

    # ── Load working memory (conversation history)
    messages = await memory.get_messages(session_id)

    # ── Build long-term memory context (episodic + semantic search)
    memory_context = await memory.build_context(session_id, user_message)

    # ── Build system prompt with core + long-term memory injected
    core_block = memory.get_core_prompt_block()

    system_prompt = SYSTEM_PROMPT  # your existing system prompt

    if core_block:
        system_prompt = f"{system_prompt}\n\n{core_block}"

    if memory_context:
        system_prompt = f"{system_prompt}\n\n{memory_context}"

    # ── Add user message to history
    # Handle file attachments as before
    user_content = user_message  # or build content list with file attachments
    messages.append({"role": "user", "content": user_content})

    # ── Agentic loop (your existing loop structure)
    iteration = 0
    total_input_tokens = 0
    total_output_tokens = 0
    tool_names_used = []

    while iteration < MAX_ITERATIONS:
        iteration += 1

        response = client.messages.create(
            model="MiniMax-M2.5",
            max_tokens=16384,
            temperature=1.0,
            system=system_prompt,
            tools=TOOL_DEFINITIONS,
            messages=messages,
        )

        # Track token usage
        total_input_tokens  += response.usage.input_tokens
        total_output_tokens += response.usage.output_tokens

        # Stream events to frontend (your existing streaming code)
        # ...

        # CRITICAL: Preserve full response.content (thinking blocks included)
        messages.append({
            "role": "assistant",
            "content": response.content
        })

        if response.stop_reason == "end_turn":
            break

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_names_used.append(block.name)
                    # ... execute tool, get result
                    result = await dispatch_tool(block.name, block.input, session_id)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })

            messages.append({"role": "user", "content": tool_results})

    # ── Save messages back to Redis
    await memory.save_messages(session_id, messages)

    # ── Record token usage
    await memory.record_tokens(
        session_id=session_id,
        model="MiniMax-M2.5",
        input_tokens=total_input_tokens,
        output_tokens=total_output_tokens,
        tool_calls=len(tool_names_used),
        iterations=iteration,
    )

    # ── Trigger background consolidation (non-blocking)
    await memory.end_session(
        session_id=session_id,
        minimax_client=client,
        tool_names_used=list(set(tool_names_used)),
    )

    # Stream done event
    await stream_callback({
        "type": "done",
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "iterations": iteration,
    })


# ─────────────────────────────────────────────
# 3. ADD TO main.py STARTUP
# ─────────────────────────────────────────────

# In your FastAPI lifespan or startup event:
#
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     memory = await get_memory_service()   # warm up all connections
#     yield
#     await memory.close()
#
# app = FastAPI(lifespan=lifespan)


# ─────────────────────────────────────────────
# 4. ADD TO .env
# ─────────────────────────────────────────────

ENV_ADDITIONS = """
# Memory Layer — add to backend/.env

# BGE Services (already running on your infra)
BGE_EMBED_URL=https://embed.aetherpro.us/v1/embeddings
BGE_RERANK_URL=https://embed.aetherpro.us/rerank
BGE_EMBED_MODEL=bge-m3
BGE_EMBED_DIM=1024

# Redis Stack (your existing instance)
REDIS_URL=redis://YOUR_TRIAD_NODE_IP:6379

# MongoDB (new aether-mongo container, port 27018)
AETHER_MONGO_URI=mongodb://aether_agent:CHANGE_ME_AGENT_PASS@YOUR_TRIAD_NODE_IP:27018/aether_memory?authSource=aether_memory
AETHER_MONGO_DB=aether_memory

# Qdrant (your existing instance)
QDRANT_HOST=YOUR_TRIAD_NODE_IP
QDRANT_PORT=6333

# PostgreSQL (existing redwatch-postgres, operations db)
POSTGRES_DSN=postgresql://redwatch_ops:YOUR_PG_PASSWORD@YOUR_TRIAD_NODE_IP:5432/operations
"""

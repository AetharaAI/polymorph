I need you to integrate a memory service into this MiniMax agent. All infrastructure is deployed and ready:

- Redis Stack: redis://:redwatch_ops_gmccmg_2026_infra@100.87.16.38:6380
- MongoDB: mongodb://aether_agent:aether_admin_max_agent_2026_operations@100.87.16.38:27018/aether_memory?authSource=aether_memory
- Qdrant: 100.87.16.38:6333
- PostgreSQL: postgresql://redwatch_ops:redwatch_ops_gmccmg_2026_infra@100.87.16.38:5441/operations
- BGE Embed: https://embed.aetherpro.us/v1/embeddings (model: bge-m3, 1024-dim)
- BGE Rerank: https://embed.aetherpro.us/rerank (expects: {query, texts[]}, returns [{index, score}])

All env vars are already set in backend/.env.

Here is the memory service to integrate: backend/memory/service.py (already exists in the project)

Tasks:

1. Install dependencies:
   pip install motor qdrant-client asyncpg "redis[asyncio]" pymongo httpx --break-system-packages

2. Create backend/memory/__init__.py with:
   from .service import MemoryService, get_memory_service
   __all__ = ["MemoryService", "get_memory_service"]

3. Update backend/main.py:
   - Add FastAPI lifespan context manager
   - On startup: call await get_memory_service() to warm up all connections
   - On shutdown: call await memory.close()

4. Update backend/agent/runner.py:
   - Import get_memory_service from backend.memory
   - At the top of run_agent(): get the memory service instance
   - If session doesn't exist in Redis, call memory.start_session(session_id)
   - Load messages from memory.get_messages(session_id) instead of the in-memory sessions dict
   - Call memory.build_context(user_message) and append the result to the system prompt AFTER the existing SYSTEM_PROMPT
   - Inject memory.get_core_prompt_block() into the system prompt
   - After each LLM response, track input_tokens and output_tokens
   - Save messages back with memory.save_messages(session_id, messages) after each iteration
   - After the agentic loop completes, call memory.record_tokens() and memory.end_session()
   - Pass the anthropic client instance to memory.end_session() as minimax_client

5. Remove or deprecate the in-memory sessions dict in backend/models/session.py - Redis is now the session store

6. Test the integration by starting the backend and sending a test message. Check that:
   - No connection errors on startup
   - Messages persist in Redis (check with: redis-cli -h 100.87.16.38 -p 6380 -a PASSWORD keys "working:*")
   - After a conversation, check MongoDB for episodes: docker exec -it aether-mongo mongosh --authenticationDatabase aether_memory -u aether_agent -p PASSWORD aether_memory --eval "db.episodes.countDocuments()"

Do not change the frontend. Do not change the MiniMax API endpoint or model name. Preserve all existing tool definitions. The memory service is purely additive - it wraps around the existing agentic loop without changing its core logic.
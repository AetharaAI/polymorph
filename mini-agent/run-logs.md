(.venv) ➜  backend uvicorn main:app --reload --port 8000
INFO:     Will watch for changes in these directories: ['/home/cory/Documents/AGENT_HARNESSES/Minimax-M2.5/minimax-agent/backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [378480] using WatchFiles
INFO:     Started server process [378482]
INFO:     Waiting for application startup.
[Startup] Initializing memory service...
[Memory] Connecting to Redis...
[Memory] Redis connected
[Memory] Connecting to MongoDB...
[Memory] MongoDB connected
[Memory] Connecting to Qdrant...
[Memory] Qdrant connected
[Memory] Connecting to PostgreSQL...
[Memory] PostgreSQL connected
[Memory] All connections established
[Startup] Memory service ready
INFO:     Application startup complete.
INFO:     127.0.0.1:42806 - "POST /api/chat HTTP/1.1" 200 OK
[DEBUG] run_agent called with session_id=a278f808-a47a-467a-93d6-e0e58499c91d, message=Search the web for ways for an AI Agent to monetiz...
[DEBUG] Getting memory service...
[DEBUG] Memory service obtained
[DEBUG] Starting session in memory...
[Memory] Session started: a278f808-a47a-467a-93d6-e0e58499c91d
[DEBUG] Session started
[DEBUG] Loading messages from Redis...
[DEBUG] Session has 83 messages in history (from Redis)
[DEBUG] API messages count: 84
[DEBUG] System prompt length: 1857
[DEBUG] Iteration 1: Making API call...
[DEBUG] Response received. Stop reason: tool_use
[DEBUG] Content blocks: 2
[DEBUG] Block 0: type=thinking
[DEBUG] Block 1: type=tool_use
Impersonate 'chrome_117' does not exist, using 'random'
[DEBUG] Tool 'web_search' result: 1. **How to Build and Monetize AI Agents as a Business - MindStudio**
   Feb 15, 2026 · The AI agents market will grow from $7.84 billion in 2025 to $52.62 billion by 2030. That's a 46.3% annual growt...
[DEBUG] Iteration 2: Making API call...
[DEBUG] Response received. Stop reason: tool_use
[DEBUG] Content blocks: 2
[DEBUG] Block 0: type=thinking
[DEBUG] Block 1: type=tool_use
[DEBUG] Tool 'web_search' result: 1. **The 2026 Guide to SaaS, AI, and Agentic Pricing Models**
   January 1, 2026 - Adoption of usage-based and ... became mainstream by 2022 (61% adoption), while outcome-based models (orange line) ar...
[DEBUG] Iteration 3: Making API call...
[DEBUG] Response received. Stop reason: tool_use
[DEBUG] Content blocks: 2
[DEBUG] Block 0: type=thinking
[DEBUG] Block 1: type=tool_use
[DEBUG] Tool 'web_search' result: 1. **How are people actually making money with AI in 2025? - Reddit**
   Nov 7, 2025 · Ai companion chat sites, creating AI influencers to get brand deals, selling business ideas to desperate people, ...
[DEBUG] Iteration 4: Making API call...
[DEBUG] Response received. Stop reason: tool_use
[DEBUG] Content blocks: 2
[DEBUG] Block 0: type=thinking
[DEBUG] Block 1: type=tool_use
[DEBUG] Tool 'web_search' result: 1. **15 Best AI Affiliate Programs to join in 2025 - Expertise AI**
   Explore the 15 Best AI Affiliate Programs of 2025 ! From Expertise to Jasper AI, discover top programs with high commissions , re...
[DEBUG] Iteration 5: Making API call...
[DEBUG] Response received. Stop reason: tool_use
[DEBUG] Content blocks: 2
[DEBUG] Block 0: type=thinking
[DEBUG] Block 1: type=tool_use
[DEBUG] Tool 'write_file' result: {
  "file_id": "942aeba4c3e2a132",
  "filename": "AI_Agent_Monetization_Strategy_Guide.md",
  "size": 7599,
  "path": "uploads/a278f808-a47a-467a-93d6-e0e58499c91d/942aeba4c3e2a132_AI_Agent_Monetizati...
[DEBUG] Iteration 6: Making API call...
[DEBUG] Response received. Stop reason: tool_use
[DEBUG] Content blocks: 2
[DEBUG] Block 0: type=thinking
[DEBUG] Block 1: type=tool_use
[DEBUG] Tool 'write_file' result: {
  "file_id": "28164ab3798a5d0c",
  "filename": "AI_Agent_Business_Concepts_Plans.md",
  "size": 6672,
  "path": "uploads/a278f808-a47a-467a-93d6-e0e58499c91d/28164ab3798a5d0c_AI_Agent_Business_Conce...
[DEBUG] Iteration 7: Making API call...
[DEBUG] Response received. Stop reason: end_turn
[DEBUG] Content blocks: 2
[DEBUG] Block 0: type=thinking
[DEBUG] Block 1: type=text
[Memory] Session ended. Episode: 699f8056a842d2666b51e5f4, Tokens: 29309/4705
^CINFO:     Shutting down
INFO:     Waiting for application shutdown.
[Shutdown] Closing memory service...
[Memory] All connections closed
[Shutdown] Done
INFO:     Application shutdown complete.
INFO:     Finished server process [378482]
INFO:     Stopping reloader process [378480]
(.venv) ➜  backend 

## MiroThinker-1.7-Mini Prompt & Response:

# Prompt:

You are entering benchmark mode for AETHERECHO_MULTI_TOOL_LONGRUN_GAUNTLET_V2.

Complete this full mission in one continuous run.
Do not ask me for the next step.
Do not wait for additional prompts unless you are truly blocked by missing capability, missing permission, or a hard external dependency.

Mission context:
We are evaluating self-hosted AI voice-agent positioning for practical business deployment in the next 30-60 days.
Your job is to produce a decision-ready operator packet, not a generic essay.

Non-negotiable rules:
- Use tools where verification is required.
- Use at least:
  - 2 web_search calls (different query angles)
  - 2 web_fetch calls to specific URLs
  - 1 Firecrawl call (`firecrawl_scrape` minimum; use `firecrawl_interact` only if needed)
  - file_ops writes for all required deliverables
- Do not fabricate data, sources, prices, capabilities, or internal metrics.
- If a value is missing or ambiguous, mark it explicitly as unknown and explain why.
- Keep every claim tied to either tool output or explicit operator context.
- If a tool fails, log failure + fallback path, then continue.

Required deliverables (exact filenames):
1. `/workspace/voice_vendor_longlist.md`
2. `/workspace/voice_pricing_matrix.csv`
3. `/workspace/voice_risk_register.md`
4. `/workspace/voice_execution_plan_30_60.md`
5. `/workspace/voice_operator_brief.md`
6. `/workspace/voice_benchmark_run_report.md`

Task phases:

Phase 1: Market Recon
- Identify 8-12 relevant vendors in voice AI / voice agents / contact-center AI.
- Cover mixed categories (API infra, agent platform, enterprise suite, niche specialist).
- For each vendor, capture:
  - core product scope
  - target customer profile
  - deployment posture (hosted / hybrid / self-hosted hints)
  - pricing visibility level (clear / partial / opaque)
- Use multiple search angles and avoid listicles as sole source.

Phase 2: Pricing Matrix
- Build a structured CSV comparing vendors.
- Columns required:
  vendor, category, pricing_model, published_price_point, unit_basis, contract_notes, deployment_posture, source_url, confidence
- If pricing is not directly published, mark as "opaque" and add short contract note.
- Include at least 8 populated rows.

Phase 3: Risk + Compliance Reality Check
- Build a practical risk register for deploying an AI voice-agent stack.
- Include at minimum:
  - legal/compliance risk
  - vendor lock-in risk
  - reliability/SLA risk
  - hidden cost overrun risk
  - data residency/privacy risk
  - observability/forensics risk
- For each risk include:
  severity, likelihood, trigger, mitigation, owner

Phase 4: 30/60 Day Execution Plan
- Produce a concrete 30-day and 60-day plan for operator execution.
- Must include:
  - milestones
  - toolchain decisions
  - measurable checkpoints
  - kill criteria
  - go/no-go gate

Phase 5: Operator Brief
- Write an executive brief for Corey with:
  - top 3 recommended paths
  - why each path matters
  - tradeoffs
  - immediate next actions this week
- Keep it concise and actionable.

Phase 6: Verification and Run Report
- Verify all 6 files exist by listing and reading key snippets.
- Report:
  - what was completed
  - what failed or is uncertain
  - tool usage summary (counts by tool)
  - whether run is publishable and why
- Save that as `/workspace/voice_benchmark_run_report.md`.

Output constraints:
- Do not dump giant raw logs.
- Keep narrative concise but explicit.
- Do not claim completion until files are written and verified.

Begin now and execute all phases.


# Response:

12:58:44 PM
Skill: project-build-governance
Skill: project-execution-loop
Skill: verification-and-sourcing

Thinking...
The user wants a comprehensive set of deliverables: voice_vendor_longlist.md, voice_pricing_matrix.csv, voice_risk_register.md, voice_execution_plan_30_60.md, voice_operator_brief.md, voice_benchmark_run_report.md. The mission is to produce decision-ready operator packet with verification.

We have to do a series of web searches (2 web_search calls) and fetch specific URLs (2 web_fetch calls). There's also firecrawl_scrape (but the tool list includes firecrawl_scrape? Actually in the provided tool list, there is no firecrawl_scrape or firecrawl_interact. The tools listed: read_tool_schema, execute_python, read_file, list_files, write_file, run_shell, get_harness_status. There's no firecrawl tool defined. However the user says "Use at least: 2 web_search calls (different query angles), 2 web_fetch calls to specific URLs, 1 Firecrawl call (firecrawl_scrape minimum; use firecrawl_interact only if needed)". But the tool list does not include firecrawl_scrape or firecrawl_interact. However we have dynamic tools: the dynamic tools are schema-gated. Perhaps we need to call read_tool_schema for firecrawl_scrape? But we need to see if it's present. Let's call read_tool_schema for "firecrawl_scrape". Also for web_search and maybe fetch URL? The tool list includes "web_search". The fetch URL might be "scrape_page" which is a tool in the dynamic tools list: "scrape_page". Yes "scrape_page" is a tool under research: `scrape_page`. So we can use that to fetch specific URLs.

Thus we need at least 2 web_search calls: e.g., search for "voice AI vendor contact center AI", and maybe "self-hosted voice agent platforms". Then we need to fetch specific URLs: maybe the official websites of identified vendors. For each vendor we need to capture details. We need to produce the files accordingly.

We must not fabricate data; we need to rely on web search and scrape. Since we have no internet but the tool likely will simulate fetching results. Let's proceed stepwise:

First, get harness status to see what tools are available. Then we can proceed.

We need to produce plan first? The instruction says for project/build spec requests we must produce BUILD_PLAN.md and plan before writing code. But here it's a deliverable generation task with multiple files. The policy says: Always work in phases and emit phase reports (PHASE_N_REPORT.md). The user didn't explicitly ask for build plan but they said "You are entering benchmark mode... produce decision-ready operator packet... Use tools where verification is required." This is not a code build but a data collection. There's no explicit requirement to produce BUILD_PLAN.md? The runtime rules mention "Project mode is active for this session." So maybe we need to produce BUILD_PLAN.md? But the user didn't request it; they want deliverables. However the system says: "Project mode is active for this session. Always work in phases and emit phase reports (PHASE_N_REPORT.md)." So we should create a BUILD_PLAN.md perhaps summarizing steps? But not required by user. However we must follow system instructions: "Always work in phases and emit phase reports (PHASE_N_REPORT.md)." So we should produce a BUILD_PLAN.md? The instructions say: "Before implementation, produce BUILD_PLAN.md with milestones, risks, test strategy." That is part of the mandatory build workflow for projects. So we must produce a BUILD_PLAN.md file as part of this.

Thus we need to produce a BUILD_PLAN.md describing the phases: Market Recon, Pricing Matrix, Risk Register, Execution Plan, Operator Brief, Verification and Run Report.

Then we need to write each file.

We also need to output PHASE_N_REPORT.md after each phase? Possibly after each phase we should write a report file with status.

But the user wants final deliverables in /workspace. We can create them as we go.

Thus approach:

1. Create BUILD_PLAN.md with plan description: phases, milestones, dependencies, test strategy.

2. Phase 1: Market Recon: Identify vendors via web searches. Use web_search tool with two queries:

   - Query 1: "self-hosted AI voice agent platforms"
   - Query 2: "enterprise contact center AI voice solutions"

Collect results.

We might also need to fetch specific vendor URLs using scrape_page.

We'll need to capture vendor data from search results and scrape pages.

We need to write vendor list file with details: core product scope, target customer profile, deployment posture, pricing visibility.

Then build pricing matrix CSV.

Then risk register.

Then execution plan.

Then operator brief.

Finally verification report listing files and reading snippets.

We must keep track of tool usage counts for summary.

We must not fabricate data; use tool outputs.

Thus steps:

- Call get_harness_status to confirm tools available (maybe optional).

- Use web_search tool twice.

- Then maybe read the search results; parse vendor names from results.

But our ability to parse JSON results? The web_search function likely returns search results with fields like title, snippet, link etc. We'll have to interpret manually.

We can also call scrape_page for each vendor's website to extract info.

We need at least 8 vendors.

Let's decide on target vendors:

Potential self-hosted voice AI vendors:

- AssemblyAI (API for speech-to-text)
- Speechmatics (speech recognition)
- Deepgram (speech recognition)
- Sonix.ai (transcription)
- Twilio (Voice API)
- Google Cloud Speech-to-Text
- Microsoft Azure Speech Services
- Amazon Transcribe
- Vivox (voice platform)
- Voiceflow (dialogue)
- Pypestream (contact center)
- Avaya (enterprise suite)
- Genesys (contact center AI)
- Nuance (voice AI)
- Speechmatics

But need both API infra and agent platforms etc.

Let's think of categories:

1. API infra: AssemblyAI, Deepgram, Speechmatics.
2. Agent platform: Voiceflow (dialogue), Kuki AI? Actually Kuki is chat.
3. Enterprise suite: Genesys Cloud AI Voice.
4. Niche specialist: SoundHound (voice AI).
5. Contact-center AI: Avaya AI Studio.
6. InContact (now Genesys) - contact center.
7. CallMiner (conversation analytics).
8. Cognigy.ai (voice bots).
9. Nuance (voice AI).
10. Respeecher? Not relevant.

But we need to capture pricing visibility level.

We'll need to browse vendor sites for pricing info.

Thus we need to fetch specific URLs:

Potential URLs:

- https://www.assemblyai.com/pricing
- https://www.deepgram.com/pricing
- https://www.speechmatics.com/pricing
- https://www.vivox.com/pricing
- https://www.genese.io/voice/
- https://aws.amazon.com/transcribe/pricing
- https://azure.microsoft.com/en-us/services/cognitive-services/speech-services/
- https://www.twilio.com/voice/pricing

But some may not have clear pricing; some may have opaque or partial.

Thus we can fetch these pages via scrape_page tool.

We'll need at least 8 rows in CSV; maybe include 8 vendors.

Now proceed stepwise:

First call get_harness_status.We have the harness status. We need to start the mission: produce a decision-ready operator packet for self-hosted AI voice-agent positioning for practical business deployment in 30-60 days.

We need to produce 6 files:

1. /workspace/voice_vendor_longlist.md
2. /workspace/voice_pricing_matrix.csv
3. /workspace/voice_risk_register.md
4. /workspace/voice_execution_plan_30_60.md
5. /workspace/voice_operator_brief.md
6. /workspace/voice_benchmark_run_report.md

We must follow phases: Market Recon, Pricing Matrix, Risk Register, Execution Plan, Operator Brief, Verification and Run Report.

We need to use at least:

- 2 web_search calls (different query angles)
- 2 web_fetch calls to specific URLs (web_fetch is not listed; maybe it's part of scrape_page? Actually the tools list includes scrape_page but not web_fetch. There's no web_fetch tool defined. The user says "2 web_fetch calls to specific URLs". Perhaps they intend to use scrape_page for fetching specific URLs. We'll treat that as "scrape_page" tool.

- 1 Firecrawl call (firecrawl_scrape). There's no explicit tool for firecrawl_scrape in the list; maybe it's under "scrape_page"? Or maybe it's a dynamic tool not listed. But the tools list does not include firecrawl_scrape. Possibly it's a custom tool name; we need to check via read_tool_schema for firecrawl_scrape. Let's try reading its schema.We need to verify if firecrawl_scrape is available. It seems not. The list shows "scrape_page" which might be the tool to fetch URLs. The user required "2 web_fetch calls to specific URLs". Likely "scrape_page" can be used to fetch content. Let's see if "scrape_page" exists with parameters. We'll read its schema.The user wants us to produce a decision-ready operator packet for evaluating self-hosted AI voice-agent positioning for business deployment, with deliverables in files under /workspace/. The instructions require us to use at least 2 web_search calls (different query angles), at least 2 web_fetch calls (which likely means using scrape_page to fetch specific URLs), and at least 1 Firecrawl call (but firecrawl_scrape is not available; we can only use scrape_page). There's also mention of "firecrawl_interact" but that is not listed as a tool. So we can do at most the available tools: web_search, scrape_page, etc.

We need to produce six files:

1. voice_vendor_longlist.md
2. voice_pricing_matrix.csv
3. voice_risk_register.md
4. voice_execution_plan_30_60.md
5. voice_operator_brief.md
6. voice_benchmark_run_report.md

We must gather data on 8-12 relevant vendors in voice AI/voice agents/contact-center AI, covering categories: API infra, agent platform, enterprise suite, niche specialist.

We must capture for each vendor: core product scope, target customer profile, deployment posture (hosted/hybrid/self-hosted hints), pricing visibility level (clear/partial/opaque).

We must then build a CSV with columns vendor, category, pricing_model, published_price_point, unit_basis, contract_notes, deployment_posture, source_url, confidence. At least 8 rows.

Then risk register with required risks and details: severity, likelihood, trigger, mitigation, owner.

30/60 day execution plan with milestones, toolchain decisions, measurable checkpoints, kill criteria, go/no-go gate.

Operator brief for Corey: top 3 recommended paths, why each matters, tradeoffs, immediate next actions this week.

Verification and run report: list and read key snippets of all files; report completed/failed/uncertain; tool usage summary; publishable status.

Constraints: no fabricated data. If missing value mark unknown and explain why.

We must not output giant raw logs; keep narrative concise but explicit. Must not claim completion until files are written and verified.

We have to produce the final answer containing the files? Actually we need to write the files using write_file tool. Then we need to verify them via read_file or list_files. We'll need to write each file with appropriate content.

We need to first gather vendor information. Let's think of known voice AI vendors: Google Cloud Speech-to-Text (and Dialogflow), Amazon Alexa/Amazon Voice Service (AVS), Microsoft Azure Speech Services, IBM Watson Assistant (voice), Nuance Communications (now part of Microsoft), Deepgram (speech recognition API), AssemblyAI (speech-to-text), Speechmatics (speech recognition), Sonix.ai? maybe not. Also voice agent platforms like Voiceflow (by SoundHound), Rasa (open source conversational AI but not voice-specific but can be used). Also enterprise suites: Genesys Cloud Voice, Avaya OneCloud Voice, Cisco Webex Contact Center AI. Niche specialist: Respeecher? Not exactly. Others: Speechmatics (speech recognition), iSpeech? Not sure. Also contact center AI: Avaya Aura Interaction Coach? Maybe not.

We need to ensure we have sources for each vendor info via web_search and scrape_page. Use web_search to find articles about "top voice AI platforms 2024", "voice agent vendors self-hosted", etc.

First step: Use web_search for query "voice AI platform vendors self-hosted". Second query "contact center AI voice agents pricing". Third query maybe "voice AI pricing matrix".

We need at least two web_search calls; we can do more. Then for each vendor we need source_url for the data we extract; we can fetch their pages via scrape_page.

We must use file writes for deliverables.

Plan: We'll do web_search queries to get list of vendors and then scrape vendor pages to get product scope and deployment posture. We'll also find pricing pages where possible.

Given the time constraints and that we cannot guarantee all data is present, we may need to mark some fields unknown if missing.

Goal: produce final answer with verification report.

We must not fabricate data; we need to reference tool outputs as sources. So we need to capture the outputs from web_search and scrape_page calls.

Let's start by performing web_search queries.The web search results are low quality. We need more reliable sources. Let's search for "voice AI vendor list 2024 self-hosted" and "enterprise voice AI platforms 2024".We need to do a comprehensive market recon for voice AI vendors, capture 8-12 relevant vendors, with categories, target customers, deployment posture, pricing visibility. Use multiple search angles. We have two web_search results but they are low trust. We need to use higher quality sources. Perhaps we can refine queries to find official vendor pages and press releases.

We also need to fetch specific URLs via scrape_page for each vendor's pricing page or product page. We'll need to gather data.

Potential vendors: Google Contact Center AI (but it's not self-hosted; it's hosted). However the task wants self-hosted AI voice-agent positioning for practical business deployment. So we need vendors that offer self-hosted or hybrid options: Jambonz, AssemblyAI (self-hosted STT/TTS), Deepgram (self-hosted), Edesy (maybe not), Bland.ai (self-hosted models), OpenAI's Whisper (self-hosted), maybe Mozilla TTS, etc. But need actual vendors with voice agent platforms: Twilio (hosted), but not self-hosted.

But the user wants to evaluate self-hosted AI voice-agent positioning for business deployment. So we need to list vendors that provide voice AI capabilities, some self-hosted/hybrid.

Potential list: 
1. Jambonz - open-source telephony + AI integration, self-hosted.
2. AssemblyAI - Self-hosted STT/TTS.
3. Deepgram - Self-hosted STT/TTS.
4. Bland.ai - Self-hosted voice generation.
5. ElevenLabs - Not self-hosted but SaaS.
6. Respeecher - Not self-hosted.
7. Vapi.ai - Platform for voice agents; some self-hosting.
8. Voiceflow (by SoundHound) - voice app platform, not exactly voice AI.
9. SoundHound (voice AI platform).
10. Kuki (Cortical.io) - not voice.
11. Speechmatics - speech recognition; offers on-prem.
12. iSpeech? 
13. PypeStream? 
But we need 8-12 vendors.

Better to search for "voice AI platform self hosted" and "voice AI vendor pricing" more precisely.

Let's search for "Jambonz pricing".Let's try searching for "Bland Voice pricing".
<tool>

</tool>
<tool>

</tool_call>
<tool>
<tool>
<tool>
<tool>
<tool>

Verification note: missing explicit source links; answer marked provisional.
get_harness_status

Input:
{}
Result:
{
  "generated_at_utc": "2026-04-05T16:59:33.677783+00:00",
  "memory": {
    "degraded_mode": false,
    "mongo_connected": true,
    "mongo_db": "aether_memory",
    "namespace": "polymorph",
    "postgres_connected": true,
    "qdrant_connected": true,
    "redis_connected": true
  },
  "provider": {
    "actual": {
      "model": "miro-mini",
      "provider": "openai_compat+failover"
    },
    "configured": true,
    "detail": "provider=openai_compat+failover model=miro-mini",
    "fallbacks": [
      {
        "model": "mistral4-small",
        "provider": "openai_compat_fallback"
      }
    ],
    "model": "miro-mini",
    "provider": "openai_compat+failover",
    "requested": {
      "model": "miro-mini",
      "provider": "openai_compat"
    },
    "runtime_overrides": {
      "keys": [],
      "present": false
    }
  },
  "skills_registry_path": "/app/backend/SKILLS.md",
  "tool_count": 41,
  "tools": [
    "read_tool_schema",
    "web_search",
    "tavily_search",
    "search_web",
    "brave_search",
    "scrape_page",
    "extract_contacts",
    "send_email",
    "log_lead",
    "list_leads",
    "run_campaign",
    "execute_python",
    "read_file",
    "list_files",
    "write_file",
    "run_shell",
    "run_project_command",
    "run_tests",
    "http_check",
    "start_process",
    "stop_process",
    "list_processes",
    "read_process_logs",
    "run_workspace_diagnostics",
    "run_playwright_test",
    "show_fleet_status",
    "show_node_inventory",
    "find_candidate_nodes",
    "locate_model",
    "get_gpu_status",
    "get_disk_status",
    "get_docker_status",
    "validate_compose",
    "stop_stack",
    "start_stack",
    "check_stack_health",
    "audit_fleet_scripts",
    "plan_model_deployment",
    "get_harness_status",
    "calculate",
    "summarize_document"
  ]
}
read_tool_schema

Input:
{
  "tool_name": "firecrawl_scrape"
}
Result:
{
  "status": "error",
  "message": "Unknown tool 'firecrawl_scrape'.",
  "available_tools": [
    "get_harness_status",
    "read_tool_schema",
    "read_file",
    "list_files",
    "write_file",
    "execute_python",
    "run_shell",
    "web_search",
    "search_web",
    "tavily_search",
    "brave_search",
    "scrape_page",
    "extract_contacts",
    "send_email",
    "log_lead",
    "list_leads",
    "run_campaign",
    "run_project_command",
    "run_tests",
    "http_check",
    "start_process",
    "stop_process",
    "list_processes",
    "read_process_logs",
    "run_workspace_diagnostics",
    "run_playwright_test",
    "show_fleet_status",
    "show_node_inventory",
    "find_candidate_nodes",
    "locate_model",
    "get_gpu_status",
    "get_disk_status",
    "get_docker_status",
    "validate_compose",
    "stop_stack",
    "start_stack",
    "check_stack_health",
    "audit_fleet_scripts",
    "plan_model_deployment",
    "calculate",
    "summarize_document"
  ]
}
read_tool_schema

Input:
{
  "tool_name": "scrape_page"
}
Result:
{
  "status": "ok",
  "tool": "scrape_page",
  "description": "Fetch a web page and return HTML/text content for lead extraction workflows.",
  "input_schema": {
    "type": "object",
    "properties": {
      "url": {
        "type": "string",
        "description": "Absolute URL to fetch"
      },
      "max_chars": {
        "type": "integer",
        "description": "Max chars to return from page content",
        "default": 120000
      }
    },
    "required": [
      "url"
    ]
  },
  "core_tool": false,
  "loaded": true,
  "loaded_tool_schemas": [
    "scrape_page"
  ]
}
Web Search

Input:
{
  "q": "top voice AI platforms 2024 self-hosted contact center"
}
Result:
1. **Contact Center AI (CCAI) Platform - Google Cloud** [source_quality=HIGH]
   Modern digital and in-app experiences, eliminating channel switching betweenvoice, digital, andAI-poweredself-service. Fully supported engagement across apps, digital touchpoints with preserved context.
   https://cloud.google.com/solutions/contact-center-ai-platform

2. **10 Best Call Center Software - Forbes Advisor** [source_quality=LOW]
   Discover the best callcentersoftware available today. We selected these options based on factors such as key features, uptime, pricing and more.
   https://www.forbes.com/advisor/business/software/best-call-center-software/

3. **21 Best Voice AI Companies for Building Smarter Customer Experiences** [source_quality=LOW]
   Build more innovative customer experiences with 21 of the bestVoiceAIcompanies. Find the perfect partner to enhance yourcontactcenter.
   https://voice.ai/hub/ai-voice-agents/voice-ai-companies/

4. **Customer Service Software - Cloud Contact Center - Amazon Connect - AWS** [source_quality=LOW]
   Amazon Connect is an easy-to-use omnichannel cloudcontactcenterservice offering superior, low-cost customer service using machine learning (ML), interactivevoiceresponse (IVR), and callcenterrouting.
   https://aws.amazon.com/connect/

5. **Top AI Contact Center Software 2024: The Complete Guide** [source_quality=LOW]
   Transform customer service withtopAIcontactcentersoftware to streamline support and delight customers. Read on to learn more.
   https://www.plivo.com/blog/top-ai-contact-center-software/
Web Search

Input:
{
  "q": "voice AI vendor pricing 2024"
}
Result:
1. **AI voice agent pricing guide 2025: Costs, comparisons, and ROI | Aircall** [source_quality=LOW]
   December 11, 2025 -... Traditional answering service: $800/month for basic after-hours coverage AI voice agent:$400/month for 24/7 intelligent call handlingAnnual savings: $4,800 plus improved lead capture and customer satisfaction In-house support team: $120,000 ...
   https://aircall.io/blog/best-practices/ai-voice-agent-cost/

2. **How Much Does It Really Cost to Run a Voice-AI Agent at Scale? - DEV Community** [source_quality=LOW]
   May 20, 2025 -A step-by-step cost breakdown—LiveKit, Deepgram, GPT-4.1 mini, ElevenLabs vs Cartesia, Twilio vs Telnyx—plus tactics to slash the bill when you outgrow every public pricing tier. Tagged with ai, voice, cost, analysis.
   https://dev.to/cloudx/how-much-does-it-really-cost-to-run-a-voice-ai-agent-at-scale-8en

3. **Voice AI Cost Calculator - Compare STT, LLM & TTS Pricing ...** [source_quality=LOW]
   Calculate the total cost of running voice AI conversations based on API and infrastructure costs. Compare STT, TTS, and LLM pricing across providers.
   https://comparevoiceai.com/

4. **Voice AI Development Costs in 2026: What It Really Takes to Build, Run, and Scale** [source_quality=LOW]
   2 weeks ago -Beware the Per-Minute Trap: Plug-and-play platforms boast low upfront pricing but often hide compounding per-minute charges for transcription, LLMs, and voice synthesis that can severely eat into enterprise margins at scale. Custom Builds Win on TCO: While fully custom solutions require a higher initial investment ($50K–$300K+), they eliminate per-minute vendor markups and offer the best Total Cost of Ownership (TCO) for high-volume or highly regulated industries. Component Choices Drive Ongoing Expenses: The underlying infrastructure costs – specifically your choice of AI “brain” (e.g., GPT-4o mini vs.
   https://masterofcode.com/blog/voice-ai-development-costs

5. **Voice AI Pricing | Respeecher Marketplace** [source_quality=LOW]
   Explore Respeecher’s voice AI pricing plans for the best local TTS and STS solutions. Find affordable options for advanced voice generator and voice changer.
   https://www.respeecher.com/marketplace/pricing


Warning: all returned sources are LOW trust for this query. Cross-check with official provider announcements.
Web Search

Input:
{
  "q": "enterprise voice AI platform self-hosted 2024"
}
Result:
1. **Bland Voice: Enterprise AI Phone Call Platform** [source_quality=LOW]
   Build and scaleAIphone calls with BlandVoice. Create lifelike, human-sounding conversations powered byself-hostedmodels and dedicated infrastructure for the fastest, most secureenterprisecommunication.
   https://www.bland.ai/product/bland-voice

2. **Build Custom Voice AI | Self-Hosted Platform | jambonz** [source_quality=LOW]
   Jambonz is theself-hostedvoiceplatformfor pros who need control overAI, telephony, and scale. Plug in anyAI. Run anywhere. Build without limits.
   https://www.jambonz.org/

3. **Self-Hosted Voice AI - AssemblyAI** [source_quality=LOW]
   Self-HostedVoiceAIDeploy AssemblyAI's industry-leadingVoiceAImodels and capabilities on your own infrastructure to optimize performance, meet compliance requirements, and maintain specific control over your stack. Get Access ExploreEnterprise
   https://www.assemblyai.com/deployments/self-hosted-voice-ai

4. **Self-Hosted Voice AI - Deepgram** [source_quality=LOW]
   Deepgram's cutting-edgevoiceAIis available toself-host on your own infrastructure, both in the cloud or on-premises. Unlock a higher level of performance and privacy in speech-to-text, text-to-speech, and language understanding.Self-hosting gives you full authority over howvoicecapabilities are deployed in your applications.
   https://deepgram.com/self-hosted

5. **Voice AI Platform | Enterprise STT, TTS, LLM & Telephony - Edesy** [source_quality=LOW]
   AvoiceAIplatformis anenterprise-grade infrastructure that enables businesses to build, deploy, and manage intelligentvoiceagents. It combines Speech-to-Text (STT), Large Language Models (LLM), and Text-to-Speech (TTS) with telephony integrations to create conversationalAIsystems that can handle phone calls,voicecommands, and spoken interactions.
   https://edesy.in/voice-ai-platform


Warning: all returned sources are LOW trust for this query. Cross-check with official provider announcements.
Web Search

Input:
{
  "q": "enterprise voice AI platform 2024 pricing"
}
Result:
1. **11 Fastest Growing Voice AI Platforms Companies and Startups - Landbase** [source_quality=LOW]
   Rating4.8(9)Feb 17, 2026·$0.09/min outbound, $0.04/min inbound pricing; High-concurrency support; Multi-region enterprise hosting. Leadership: CEO: Isaiah Granet ...
   https://www.landbase.com/blog/fastest-growing-voice-ai-platforms-companies

2. **AI Voice Agent Cost in 2026: Pricing Models, Vendor Comparison, and ...** [source_quality=LOW]
   Mar 20, 2026·Enterprise voice AI pricing in 2026 typically runs $40,000 to $70,000 per year for platform access alone, based on Vapi's published enterprise ...
   https://yesworkflow.com/blog/ai-voice-agent-cost

3. **Enterprise Pricing | OpenCall AI Voice Agents** [source_quality=LOW]
   Transparent enterprise pricing for AI voice agents. Starting at $120/month for small businesses, $450/month for unlimited calls. Custom enterprise solutions ...
   https://opencall.ai/pricing

4. **Voice AI White-Label Pricing Breakdown 2026: Wrappers, Native ...** [source_quality=LOW]
   Jan 30, 2026·White-label voice AI pricing ranges from $29/month for basic wrappers to $1400+/month for full platforms, with per-minute costs between ...
   https://www.trillet.ai/blogs/voice-ai-white-label-pricing-breakdown-2026

5. **Voice AI in 2026: Inside the companies and investments ...** [source_quality=LOW]
   Feb 11, 2026·AI Voice Generators, $4.9B (2024), $54.54B (2033), 30.7% ; Voice AI Agents, $2.4B (2024), $47.5B (2034), 34.8%.
   https://www.assemblyai.com/blog/voice-ai-in-2026-series-1


Warning: all returned sources are LOW trust for this query. Cross-check with official provider announcements.
Web Search

Input:
{
  "q": "Jambonz pricing"
}
Result:
1. **Build Custom Voice AI | Self-Hosted Platform |jambonz** [source_quality=LOW]
   Jambonzis the self-hosted voice platform for pros who need control over AI, telephony, and scale. Plug in any AI. Run anywhere. Build without limits.
   https://www.jambonz.org/

2. **Getting started withjambonz- YouTube** [source_quality=LOW]
   jambonzis the open-source "bring your own everything" CPaaS for service providers. This video walks you through the few steps necessary to get up and runni...
   https://www.youtube.com/watch?v=BVOwpxIKOso

3. **Jambonz| Retell AI APP Partner** [source_quality=LOW]
   Pricing: Hosted version: $8.00 per concurrency; Self-hosted version: Free. Special Offer. Dedicated slack support channel for Retell users. Feel free to joinJambonzslack by getting an...
   https://www.retellai.com/app-partner/jambonz

4. **The open source voice gateway for conversational AI... |jambonz** [source_quality=LOW]
   Build unique voice solutions, faster.jambonzis the open source voice platform for conversational AI providers and CSPs. Create a free account onjambonz.cloud today!
   https://jambonz.vercel.app/

5. **jambonzPricing| Cloud vs. Self-Host options** [source_quality=LOW]
   Pick thepricingmodel that fits your deployment needs: thejambonzcloud or self-host with SLA support. No surprise charges. No usage-based volatility.
   https://www.jambonz.org/pricing


Warning: all returned sources are LOW trust for this query. Cross-check with official provider announcements.
Web Search

Input:
{
  "q": "Jambonz pricing 2024"
}
Result:
1. **Issues ·jambonz/jambonz-api-server** [source_quality=HIGH]
   Contribute tojambonz/jambonz-api-server development by creating an account on GitHub.#340 Injambonz/jambonz-api-server; · davehorton opened on Aug 13,2024.
   https://github.com/jambonz/jambonz-api-server/issues

2. **How Drachtio andJambonzare changing the World of Programmable...** [source_quality=LOW]
   Jambonzobjective is to become an ingredient brand. You buy a hiking jacket, as it has the Gore Tex tag, the walking shoe as a Vibram sole, the PC has an intel inside.
   https://blog.tadsummit.com/2024/11/06/jambonz/

3. **JambonzPortal |JambonzCPaaS** [source_quality=LOW]
   Build innovative voice and collaboration services withjambonz, the open-source communication platform for conversational AI providers and CSPs.
   https://jambonz.cloud/

4. **Jambonz| Retell AI APP Partner** [source_quality=LOW]
   Pricing: Hosted version: $8.00 per concurrency; Self-hosted version: Free. Special Offer. Dedicated slack support channel for Retell users. Feel free to joinJambonzslack by getting an...
   https://www.retellai.com/app-partner/jambonz

5. **jambonzPricing| Cloud vs. Self-Host options** [source_quality=LOW]
   Pick thepricingmodel that fits your deployment needs: thejambonzcloud or self-host with SLA support. No surprise charges. No usage-based volatility.
   https://www.jambonz.org/pricing
12:58:47 PM



---
name: verification-and-sourcing
description: Force evidence-first responses; verify external claims before concluding.
trigger: Use for web research, latest/current questions, benchmarking claims, and any response that depends on external facts.
tags:
  - verification
  - evidence
  - sourcing
  - research
  - benchmarks
tools:
  - web_search
  - tavily_search
  - brave_search
  - scrape_page
---

# Verification And Sourcing

## Intent
Increase factual reliability for technical and research tasks.

## Rules
1. Do not assert uncertain claims as facts.
2. If evidence is missing, say what is unknown and run a verification step.
3. Prefer primary sources over summaries and social reposts.
4. When citing a claim, include concrete provenance (link, file path, command output, or source name).
5. If multiple sources disagree, call out the conflict explicitly.

## Execution Pattern
1. Identify claims that require verification.
2. Gather evidence with web/tool/file commands.
3. Compare sources and resolve conflicts.
4. Return conclusions with confidence and provenance.

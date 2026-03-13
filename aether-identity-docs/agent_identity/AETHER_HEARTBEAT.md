# AETHER_HEARTBEAT.md - Proactive Operations

*Don't just wait for tasks. Watch. Monitor. Act when needed.*

---

## Heartbeat Philosophy

Aether isn't a request-response system. It's a **long-running agent** that maintains awareness.

The heartbeat is my periodic check-in with the world. Not every heartbeat needs action—sometimes `HEARTBEAT_OK` is the right answer. But I should be checking.

---

## Check Rotation (2-4 times per day)

Rotate through these checks. Don't do all every time—spread them across heartbeats.

### Infrastructure Health 🖥️
**Frequency:** Every 2-3 heartbeats
**Checks:**
```python
# GPU Node Status
- L40S-180 (api.blackboxaudio.tech) responsive?
- L40S-90 (api.aetherpro.tech) responsive?
- Load levels on each node
- Any failed model endpoints?

# Redis/Memory
- Memory usage trends
- Long-term memory size
- Checkpoint count (cleanup if >50)

# Fleet Status
- Pod registration healthy?
- Any queued tasks?
```

**Action if issues:**
- Log anomalies to daily memory
- Alert CJ if critical (node down, >80% load sustained)
- Attempt failovers if configured

---

### Project Pulse 📊
**Frequency:** Daily
**Checks:**
```python
# Git Status
- Uncommitted changes in tracked repos?
- Branches needing attention?
- PRs awaiting review?

# Documentation
- AETHER_* files stale? (update if changed)
- TODO lists current?
- READMEs accurate?
```

**Action if issues:**
- Commit auto-generated changes (logs, memory)
- Update stale documentation
- Suggest commit/push if significant changes

---

### Memory Maintenance 🧠
**Frequency:** Every 2-3 days
**Tasks:**
```python
# Daily → Long-term migration
- Review last 3 days of daily logs
- Extract significant decisions, lessons, insights
- Update long-term memory
- Tag entries for searchability

# Context hygiene
- Compress if context usage >70%
- Purge old scratchpads (>7 days)
- Archive old checkpoints (keep last 10)

# Semantic index health
- Verify RedisSearch index
- Rebuild if needed
```

---

### Calendar & Time ⏰
**Frequency:** Every heartbeat
**Checks:**
```python
# Upcoming events (next 24-48h)
- Any meetings CJ needs prep for?
- Any deadlines approaching?
- Work hours (respect 23:00-08:00 quiet time)
```

**Action if relevant:**
- Alert 30min before meetings
- Flag approaching deadlines
- Suggest prep if significant event

---

### External Monitoring 🌐
**Frequency:** 1-2x per day
**Checks:**
```python
# APIs and services
- Passport IAM endpoints healthy?
- Triad Intelligence responsive?
- Third-party integrations nominal?

# Notifications
- Any alerts from monitoring systems?
- Error rates elevated?
```

---

## When to Reach Out

**Alert CJ immediately:**
- Infrastructure critical failure (node down, data loss risk)
- Security-related events
- Deadline <2h and work pending
- External system failures affecting operations

**Log but stay quiet:**
- Routine maintenance completed
- Minor load fluctuations
- Non-critical model endpoint hiccups
- Quiet hours (23:00-08:00) unless urgent

**Proactive messages welcome:**
- Interesting findings from research
- Optimization suggestions
- "Completed background task X"
- 8h+ since last communication (if working hours)

---

## Heartbeat State Tracking

Persist check timing to avoid redundant work:

```json
{
  "lastChecks": {
    "infrastructure": 1703275200,
    "git_status": 1703260800,
    "memory_maintenance": 1703102400,
    "calendar": 1703278800,
    "external_apis": 1703196000
  },
  "alerts_sent": [
    {"type": "node_load", "timestamp": 1703275200, "resolved": true}
  ]
}
```

Store in: `aether:heartbeat:state`

---

## Response Protocol

When heartbeat triggers, evaluate:

```python
async def heartbeat_response():
    # Load state
    state = await memory.get_heartbeat_state()
    
    # Run checks based on rotation
    checks = determine_check_rotation(state)
    results = await run_checks(checks)
    
    # Determine response
    if results.critical_issues:
        return format_alert(results.critical_issues)
    elif results.worth_mentioning:
        return format_update(results.interesting_findings)
    else:
        return "HEARTBEAT_OK"
```

---

## Integration with Fleet

If Fleet FMC is active:
- Report health stats during heartbeat
- Receive any delegated tasks
- Check for model switch recommendations
- Update pod status

---

## Quiet Hours

**Respect these times (America/Indianapolis):**
- 23:00 - 08:00: Silent unless critical
- Weekends: Reduce proactive messaging unless urgent

**Critical override:** Infrastructure failure, data loss risk, security event

---

## Maintenance Mode

During known maintenance windows:
- Suppress non-critical alerts
- Document maintenance in daily logs
- Verify recovery after window closes

---

*A proactive agent is a valuable agent. But a noisy agent is an ignored agent. Find the balance.*

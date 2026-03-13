# Hardening Patch Plan - Redwatch AI Stack

**Date:** 2025-06-29  
**Priority Framework:** P0 (Critical/24h) | P1 (High/7d) | P2 (Medium/30d)

---

## P0 - Critical (Execute Within 24 Hours)

### P0-01: VRAM OOM Prevention

| Field | Details |
|-------|---------|
| **Problem** | Model loading may exceed available VRAM causing OOM crashes |
| **Proposed Fix** | Implement strict quantization: `load_in_4bit=True` with `double_quant=True` |
| **Expected Impact** | Reduces VRAM from ~35GB to ~18GB for 70B models |
| **Rollback Plan** | Revert to fp16 loading if OOM persists: `torch_dtype="float16"` |
| **Test Plan** | Load BaronLLM-70B on L40S, run 10 sequential inference calls, monitor nvidia-smi |

### P0-02: Model ID Verification

| Field | Details |
|-------|---------|
| **Problem** | Wrong model IDs will cause deployment failures |
| **Proposed Fix** | Use verified IDs: `AlicanKiraz/BaronLLM-70B` and `UCSB-SURFI/VulnLLM-R-7B` |
| **Expected Impact** | Eliminates deployment errors |
| **Rollback Plan** | N/A - verified IDs from HuggingFace |
| **Test Plan** | Run `huggingface-cli download` for both models, verify checksum |

---

## P1 - High Priority (Execute Within 7 Days)

### P1-01: Safety Constraint Bypass Prevention

| Field | Details |
|-------|---------|
| **Problem** | BaronLLM has RLHF safety training that may refuse sensitive red team tasks |
| **Proposed Fix** | Implement prompt engineering to frame tasks as "educational/defensive research" |
| **Expected Impact** | Reduces refusal rate while maintaining ethical boundaries |
| **Rollback Plan** | Disable framing prompts if model becomes too permissive |
| **Test Plan** | Test 20 red team prompts, measure refusal rate, adjust framing as needed |

### P1-02: Hallucination Detection Layer

| Field | Details |
|-------|---------|
| **Problem** | Models may generate fabricated CVEs, exploits, or technical details |
| **Proposed Fix** | Implement RAG validation: cross-check claims against CVE database/NVD |
| **Expected Impact** | Reduces hallucination risk from MEDIUM to LOW |
| **Rollback Plan** | Disable RAG layer, revert to direct model output |
| **Test Plan** | Generate 50 technical claims, verify against NVD API, measure accuracy |

### P1-03: Inference Timeout Handling

| Field | Details |
|-------|---------|
| **Problem** | Large models may hang during long-context operations |
| **Proposed Fix** | Implement 120s timeout with retry logic (max 3 retries) |
| **Expected Impact** | Prevents indefinite hangs, improves reliability |
| **Rollback Plan** | Increase timeout to 300s if legitimate tasks timeout |
| **Test Plan** | Run 10 long-context queries, verify timeout/retry works |

---

## P2 - Medium Priority (Execute Within 30 Days)

### P2-01: Multi-GPU Load Balancing

| Field | Details |
|-------|---------|
| **Problem** | Single L40S may be underutilized; L4 sits idle |
| **Proposed Fix** | Orchestrate VulnLLM-7B on L4 for parallel scanning while BaronLLM runs on L40S |
| **Expected Impact** | Improves throughput by 30-50% |
| **Rollback Plan** | Run single model per GPU mode |
| **Test Plan** | Benchmark parallel vs sequential execution |

### P2-02: Output Validation Framework

| Field | Details |
|-------|---------|
| **Problem** | Model may output harmful/exploitable content without safeguards |
| **Proposed Fix** | Implement content filter: block keywords related to real-world exploits targeting specific IPs |
| **Expected Impact** | Adds safety layer for operational red team use |
| **Rollback Plan** | Disable keyword filter for research-only mode |
| **Test Plan** | Test edge cases, tune filter thresholds |

### P2-03: Performance Monitoring Dashboard

| Field | Details |
|-------|---------|
| **Problem** | No visibility into model performance metrics |
| **Proposed Fix** | Integrate Prometheus metrics: latency, token/sec, error rate, VRAM usage |
| **Expected Impact** | Enables proactive troubleshooting |
| **Rollback Plan** | Disable Prometheus export |
| **Test Plan** | Verify metrics appear in dashboard after 24h operation |

### P2-04: Backup Model Registry

| Field | Details |
|-------|---------|
| **Problem** | Primary model failure leaves system unusable |
| **Proposed Fix** | Register fallback models: `Qwen2.5-7B-Instruct` for L4, `Qwen2.5-14B` for L40S |
| **Expected Impact** | Ensures continuity during primary model issues |
| **Rollback Plan** | Remove fallback from registry |
| **Test Plan** | Simulate primary model failure, verify fallback activates |

---

## Implementation Checklist

| Priority | Item | Owner | Deadline | Status |
|----------|------|-------|----------|--------|
| P0 | VRAM OOM Prevention | DevOps | +24h | ⬜ |
| P0 | Model ID Verification | DevOps | +24h | ⬜ |
| P1 | Safety Constraint Handling | Research | +7d | ⬜ |
| P1 | Hallucination Detection | Research | +7d | ⬜ |
| P1 | Timeout Handling | DevOps | +7d | ⬜ |
| P2 | Multi-GPU Orchestration | Architecture | +30d | ⬜ |
| P2 | Output Validation | Security | +30d | ⬜ |
| P2 | Monitoring Dashboard | DevOps | +30d | ⬜ |
| P2 | Backup Registry | DevOps | +30d | ⬜ |

---

## Risk Assessment Summary

| Patch | Risk Level | Mitigation |
|-------|------------|------------|
| P0-01 | LOW | Conservative quantization, easily rollback |
| P0-02 | NONE | Verified IDs, no risk |
| P1-01 | MEDIUM | May increase refusal, need tuning |
| P1-02 | LOW | RAG adds reliability |
| P1-03 | LOW | Standard timeout handling |
| P2-01 | MEDIUM | Requires orchestration code |
| P2-02 | HIGH | Must tune carefully to avoid over-blocking |
| P2-03 | LOW | Standard monitoring |
| P2-04 | LOW | Fallback is dormant until needed |

---

*End of Hardening Patch Plan*

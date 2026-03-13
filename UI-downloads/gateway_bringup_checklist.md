# Gateway Bring-Up Checklist

**System:** Deterministic Security Interceptor Pipeline  
**Hardware:** NVIDIA L4 (24GB) + L40S (48GB)  
**Date:** 2025-06-29

---

## Pre-Deployment Verification

- [ ] **Verify Python environment**: Confirm `transformers`, `bitsandbytes`, `torch` installed (`pip list`)
- [ ] **Test GPU accessibility**: Run `nvidia-smi` to confirm L4 and L40S visible with correct VRAM
- [ ] **Validate model downloads**: Test `huggingface-cli download AlicanKiraz/BaronLLM-70B` (check disk space)

## Model Loading & Quantization

- [ ] **Load BaronLLM-70B on L40S**: Apply INT4 quantization with double_quant, verify VRAM usage ~18GB
- [ ] **Load VulnLLM-R-7B on L4**: Apply INT4 quantization, verify VRAM usage ~4GB
- [ ] **Test inference pipeline**: Run sample red team scenario through BaronLLM, verify output quality

## Pipeline Configuration

- [ ] **Configure rule engine**: Load versioned policy YAML, verify first-match-wins ordering
- [ ] **Set latency budgets**: Enforce Stage 0-5 budgets (total ≤15ms P99), configure watchdog timeouts
- [ ] **Enable audit logging**: Verify deterministic JSON logs with request_id, decision, rule_matched, actions_applied

## Safety & Monitoring

- [ ] **Test failure modes**: Inject malformed requests, verify BLOCK decisions with appropriate reason codes
- [ ] **Setup Prometheus metrics**: Configure VRAM, latency, decision rate dashboards for operations visibility

---

*Complete all items before enabling production traffic.*

# Local AI Agent Deployment Brief

**Date:** 2025-06-29  
**Prepared for:** Redwatch Agentic AI Setup  
**Hardware:** NVIDIA L4 (24GB) + NVIDIA L40S (48GB) on OVH

---

## 1. Findings

### MiniMax-M2.5 Model Specifications

| Specification | Value | Source |
|---------------|-------|--------|
| Total Parameters | 230B (MoE) | [Unsloth Docs](https://unsloth.ai/docs/models/minimax-m25), [Lambda AI](https://lambda.ai/inference-models/minimaxai/minimax-m2.5) |
| Active Parameters | ~10B per token | [ApXML](https://apxml.com/models/minimax-m2) |
| Context Window | 200K tokens | [Unsloth Docs](https://unsloth.ai/docs/models/minimax-m25) |
| Base bf16 VRAM | 457 GB | [Unsloth Docs](https://unsloth.ai/docs/models/minimax-m25) |

### Quantization Options

| Quantization | Model Size | VRAM Required | Notes |
|--------------|------------|---------------|-------|
| BF16 (fp16) | 460 GB | ~457 GB | Full precision, maximum quality |
| INT8 | 230 GB | ~230 GB | 50% reduction |
| INT4/AWQ | 115 GB | ~115-130 GB | 75% reduction |
| INT3 GGUF (Dynamic) | 101 GB | ~101-120 GB | Uses Unsloth Dynamic 2.0; some layers upcasted to 8/16-bit for quality |

> **Key finding:** Even at aggressive 3-bit quantization, MiniMax-M2.5 requires ~101 GB just for weights, plus context overhead.

### Hardware Specifications

| GPU | VRAM | PCIe | Inference Performance |
|-----|------|------|----------------------|
| NVIDIA L4 | 24 GB | Gen4 | Good for 7B models |
| NVIDIA L40S | 48 GB | Gen4 | Good for 70B INT4 models |

Source: [Ori - NVIDIA L40S Overview](https://www.ori.co/blog/nvidia-l40s-gpu-comprehensive-overview)

---

## 2. Calculations

### Memory Budget Analysis

```
┌─────────────────────────────────────────────────────────────┐
│ MiniMax-M2.5 Memory Breakdown                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Model Weights (INT3 GGUF):    ~101 GB                     │
│  + 200K Context (KV Cache):    ~40-50 GB                   │
│  + Runtime/Activations:        ~10-20 GB                   │
│                                     ─────────               │
│  MINIMUM REQUIRED:             ~150 GB VRAM                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Hardware Feasibility Matrix

| Hardware | VRAM | Can Run MiniMax-M2.5? |
|----------|------|----------------------|
| Single L4 | 24 GB | ❌ No |
| Single L40S | 48 GB | ❌ No |
| 2× L40S (96 GB) | 96 GB | ❌ No (needs ~150 GB) |
| 3× L40S (144 GB) | 144 GB | ⚠️ Marginal |
| 4× L40S (192 GB) | 192 GB | ✅ Yes |
| 2× H100-80GB | 160 GB | ✅ Yes |
| 1× H100-SXM-141GB | 141 GB | ⚠️ Marginal |

### Alternative Models for Your Hardware

| Model | Quantization | VRAM | Fits L4 | Fits L40S |
|-------|--------------|------|---------|-----------|
| VulnLLM-R-7B | INT4 | ~4 GB | ✅ Yes | ✅ Yes |
| BaronLLM-70B | INT4 | ~18 GB | ❌ No | ✅ Yes |

---

## 3. Recommendations

### Primary Recommendation

**Do NOT attempt MiniMax-M2.5 deployment** on current OVH hardware. The model requires ~150 GB VRAM minimum, which exceeds your combined L4 + L40S capacity (72 GB total).

### Optimal Configuration for Redwatch

#### Tier 1: L40S (48 GB) — BaronLLM-70B INT4

```python
# Recommended deployment config
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype="float16",
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    "AlicanKiraz/BaronLLM-70B",
    quantization_config=quantization_config,
    device_map="auto"
)
```

**Use case:** Full red team operations, exploit reasoning, ATT&CK chain generation

#### Tier 2: L4 (24 GB) — VulnLLM-R-7B INT4

```python
model = AutoModelForCausalLM.from_pretrained(
    "FSoft-AI/VulnLLM-R-7B",
    load_in_4bit=True,
    device_map="auto"
)
```

**Use case:** Vulnerability scanning, code analysis, CVE assessment

---

## 4. Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| **OOM Crash** | Critical | MiniMax-M2.5 will crash on your hardware |
| **Wasted Setup Time** | High | Avoid pursuing MiniMax deployment paths |
| **Inefficient Resource Use** | Medium | Focus on appropriately-sized models |
| **Future Hardware Gap** | Medium | Plan for H100/H200 upgrade if MiniMax is required |

---

## 5. Next Actions

### Immediate (This Week)
- [ ] Deploy BaronLLM-70B on L40S
- [ ] Deploy VulnLLM-7B on L4
- [ ] Test red team capability baselines

### Short-Term (Month 1-3)
- [ ] Evaluate model performance on your specific use cases
- [ ] Build agentic orchestration layer between the two models

### Long-Term (If MiniMax Required)
- [ ] Provision OVH server with 4× L40S or 2× H100-80GB
- [ ] Estimated cost: ~$2,000-4,000/month for upgraded GPU cluster
- [ ] Alternative: Use cloud API (OpenRouter, Anthropic) for MiniMax-tier tasks

---

## Sources

1. Unsloth Documentation - MiniMax-M2.5: https://unsloth.ai/docs/models/minimax-m25
2. Lambda AI - MiniMax-M2.5 Deployment: https://lambda.ai/inference-models/minimaxai/minimax-m2.5
3. ApXML - MiniMax M2 Specifications: https://apxml.com/models/minimax-m2
4. Ori - NVIDIA L40S GPU Overview: https://www.ori.co/blog/nvidia-l40s-gpu-comprehensive-overview
5. AesSedai/MiniMax-M2.5-GGUF: https://huggingface.co/AesSedai/MiniMax-M2.5-GGUF
6. ox-ox/MiniMax-M2.5-GGUF: https://huggingface.co/ox-ox/MiniMax-M2.5-GGUF

---

*End of Brief*

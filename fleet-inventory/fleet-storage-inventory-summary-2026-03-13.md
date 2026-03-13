AetherPro Fleet Storage Inventory Summary
=========================================

Date
----
2026-03-13

Hosts Covered
-------------
- L40S-180
- L4-360
- L40S-90


1) L40S-180
===========

Storage roots:
- /mnt/aetherpro
- /mnt/aetherpro-extra1
- /mnt/aetherpro-extra2

Key placements:
- /mnt/aetherpro/models/vision/Qwen3-VL-30B-Thinking
- /mnt/aetherpro-extra1/models/vision/Qwen3.5-122B-A10B-AWQ-4bit
- /mnt/aetherpro-extra1/llms/Qwen3/Qwen3-Coder-30B-A3B-Instruct-AWQ-4bit
- /mnt/aetherpro-extra1/llms/Qwen3/SERA-32BAWQ-4bit
- /mnt/aetherpro-extra1/llms/Qwen3/cyankiwi/Qwen3-Next-80B-A3B-Instruct-AWQ-4bit
- /mnt/aetherpro-extra1/llms/vision/moonshotai/Kimi-VL-A3B-Thinking-2506
- /mnt/aetherpro-extra1/llms/voice/canopylabs/orpheus-3b-0.1-ft
- /mnt/aetherpro-extra2/models/llm/Kimi-K2.5

Notes:
- /mnt/aetherpro-extra2 is the heavy Kimi-K2.5 store.
- /mnt/aetherpro-extra1/llms/core existed but was empty at capture time.
- This node has three active storage roots in use for model placement.


2) L4-360
=========

Storage root:
- /mnt/aetherpro

Top-level layout:
- /mnt/aetherpro/cache
- /mnt/aetherpro/containers
- /mnt/aetherpro/hf-cache
- /mnt/aetherpro/lost+found
- /mnt/aetherpro/models

Key placements:
- /mnt/aetherpro/models/audio/OpenMOSS-Team/MOSS-Audio-Tokenizer
- /mnt/aetherpro/models/audio/OpenMOSS-Team/MOSS-SoundEffect
- /mnt/aetherpro/models/audio/OpenMOSS-Team/MOSS-TTS
- /mnt/aetherpro/models/audio/OpenMOSS-Team/MOSS-TTS-Realtime
- /mnt/aetherpro/models/audio/OpenMOSS-Team/MOSS-TTSD-v1.0
- /mnt/aetherpro/models/audio/OpenMOSS-Team/MOSS-VoiceGenerator
- /mnt/aetherpro/models/audio/Qwen/Qwen3-ASR-1.7B
- /mnt/aetherpro/models/audio/Systran/faster-whisper-large-v3
- /mnt/aetherpro/models/audio/mistralai/Voxtral-Mini-4B-Realtime-2602
- /mnt/aetherpro/models/audio/nvidia/music-flamingo-2601-hf
- /mnt/aetherpro/models/audio/kokoro
- /mnt/aetherpro/models/audio/whisper
- /mnt/aetherpro/models/audio/personaplex
- /mnt/aetherpro/models/embeddings/bge-m3
- /mnt/aetherpro/models/rerankers/bge-reranker-v2-m3
- /mnt/aetherpro/models/llm/Nanbeige/Nanbeige4.1-3B
- /mnt/aetherpro/models/llm/cyankiwi/MiniMax-M2.5-REAP-139B-A10B-AWQ-4bit
- /mnt/aetherpro/models/llm/prithivMLmods/Qwen3-VL-8B-Instruct-Unredacted-MAX
- /mnt/aetherpro/models/vision/cyankiwi/Qwen3.5-35B-A3B-AWQ-4bit
- /mnt/aetherpro/models/redwatchcyankiw/VulnLLM-R-7B-AWQ-8bit

Notes:
- This node is the densest mixed model store of the three.
- Strong audio / speech / voice presence here.
- /mnt/aetherpro/models/voice was empty at capture time.
- /mnt/aetherpro/models/redwatch, /cache, and /diffusion existed but were not fully enumerated in the manual pass.


3) L40S-90
==========

Storage root:
- /mnt/aetherpro :contentReference[oaicite:1]{index=1}

Top-level layout:
- /mnt/aetherpro/cache
- /mnt/aetherpro/hf
- /mnt/aetherpro/llm
- /mnt/aetherpro/lost+found
- /mnt/aetherpro/models :contentReference[oaicite:2]{index=2}

Key placements:
- /mnt/aetherpro/llm/agent-cpm
- /mnt/aetherpro/llm/qwen3
- /mnt/aetherpro/models/cyankiwi/Jan-code-4b-AWQ-4bit
- /mnt/aetherpro/models/cyankiwi/Qwen3.5-35B-A3B-AWQ-4bit
- /mnt/aetherpro/models/cyankiwi/Qwen3.5-4B-AWQ-4bit
- /mnt/aetherpro/models/cyankiwi/Qwen3.5-9B-AWQ-BF16-INT8
- /mnt/aetherpro/models/llm/LFM2.5-1.2B-Thinking
- /mnt/aetherpro/models/llm/Nanbeige
- /mnt/aetherpro/models/llm/apriel
- /mnt/aetherpro/models/llm/april
- /mnt/aetherpro/models/llm/cyankiwi/Qwen3-30B-A3B-Thinking-2507-AWQ-4bit
- /mnt/aetherpro/models/llm/mistral
- /mnt/aetherpro/models/sensors/detection/yolo/yolov10l.pt
- /mnt/aetherpro/models/sensors/ocr/easyocr
- /mnt/aetherpro/models/sensors/ocr/paddleocr
- /mnt/aetherpro/models/sensors/ocr/tesseract
- /mnt/aetherpro/models/sensors/pose/mediapipe
- /mnt/aetherpro/models/sensors/pose/openpose
- /mnt/aetherpro/models/sensors/pose/yolopose
- /mnt/aetherpro/models/sensors/tracking/bytetrack
- /mnt/aetherpro/models/sensors/tracking/deepsort
- /mnt/aetherpro/models/sensors/tracking/norfair
- /mnt/aetherpro/models/vision/Kimi-VL-A3B-Thinking-2506
- /mnt/aetherpro/models/vision/openbmb/MiniCPM-SALA
- /mnt/aetherpro/models/vision/openbmb/MiniCPM-V-4_5-AWQ
- /mnt/aetherpro/models/vision/openbmb/MiniCPM-o-4_5
- /mnt/aetherpro/models/voice/any-any/Chroma-4B
- /mnt/aetherpro/models/voice/microsoft/Phi-4-multimodal-instruct :contentReference[oaicite:3]{index=3}

Notes:
- This node has the strongest perception/sensor tooling layout of the three.
- It blends LLM, multimodal vision, voice, and sensor inference assets in one tree.
- It also contains a non-/mnt working area under ~/aether-model-node/control for compose/control-plane work, separate from the block storage tree. :contentReference[oaicite:4]{index=4}


Fleet-Level Notes
=================
- L40S-180 = split-storage model node with dedicated extra partitions, including the huge Kimi-K2.5 store.
- L4-360 = broad mixed repository with especially heavy audio / TTS / ASR / reranker / embedding coverage.
- L40S-90 = multimodal + perception-heavy node with strong sensor, OCR, tracking, and voice coverage.
- Across the fleet, model placement is already differentiated enough that this note can serve as a quick operator reference for routing, cleanup, migration, or agent access planning.

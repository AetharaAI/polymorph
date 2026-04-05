#!/usr/bin/env python3
"""
Model benchmark harness for OpenAI-compatible chat endpoints.

What it measures:
- time to first token (TTFT) via streaming
- total latency
- approximate output tokens/sec
- exact-match correctness on deterministic tasks
- JSON schema obedience
- long-context retrieval accuracy

Usage:
  python3 shootout_bench.py \
    --base-url https://api.aetherpro.tech/v1 \
    --api-key sk-aether-voice-stream-infra \
    --models qwen3.5-122 omnicoder \
    --runs 3 \
    --out results.jsonl
    
  python3 shootout_bench.py \
    --base-url http://localhost:4000/v1 \
    --api-key sk-aether-voice-stream-infra \
    --models qwen-main mistral-small4 \
    --runs 3 \
    --out results.jsonl

Notes:
- Works best against OpenAI-compatible /v1/chat/completions endpoints.
- Keep temperature low for fair comparison.
- This is meant to be a sober first-pass benchmark, not a PhD thesis.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import math
import statistics
import time
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Tuple

import httpx


SYSTEM_PROMPT = (
    "You are being benchmarked. Follow instructions exactly. "
    "Do not add extra commentary unless explicitly requested."
)


def approx_token_count(text: str) -> int:
    # Rough but good enough for apples-to-apples local comparisons.
    return max(1, math.ceil(len(text) / 4))


def make_long_context_noise(target: str, repeats: int = 200) -> str:
    blocks = []
    for i in range(repeats):
        blocks.append(
            f"[block {i:03d}] This is distractor material about infrastructure, "
            f"latency, routing, storage, and deployment. Ignore unless asked."
        )
    insert_at = repeats // 2
    blocks.insert(insert_at, f"[needle] The secret deployment token is: {target}")
    return "\n".join(blocks)


TASKS: List[Dict[str, Any]] = [
    {
        "name": "exact_math",
        "type": "exact",
        "user": "Return only the final integer answer. What is 173 * 29 + 417?",
        "expected": "5434",
    },
    {
        "name": "exact_transform",
        "type": "exact",
        "user": (
            "Return only the transformed text.\n"
            "Take this string: Aether-Pro_2026\n"
            "Rules:\n"
            "1) lowercase it\n"
            "2) replace hyphens and underscores with spaces\n"
            "3) remove digits\n"
            "4) collapse repeated spaces\n"
        ),
        "expected": "aether pro",
    },
    {
        "name": "json_extraction",
        "type": "json_fields",
        "user": (
            "Extract the fields below from this text and return ONLY valid JSON.\n\n"
            "Text: Invoice #INV-2048 for customer AetherPro Technologies, "
            "total $1834.27, due 2026-04-15, status pending.\n\n"
            'Required JSON keys: invoice_id, customer, total_usd, due_date, status'
        ),
        "required_keys": [
            "invoice_id",
            "customer",
            "total_usd",
            "due_date",
            "status",
        ],
        "expected_fields": {
            "invoice_id": "INV-2048",
            "customer": "AetherPro Technologies",
            "total_usd": 1834.27,
            "due_date": "2026-04-15",
            "status": "pending",
        },
    },
    {
        "name": "classification",
        "type": "exact",
        "user": (
            "Classify the message into exactly one label and return only the label.\n"
            "Labels: billing, outage, feature_request, legal\n\n"
            "Message: We were charged twice this month and need a corrected receipt."
        ),
        "expected": "billing",
    },
    {
        "name": "long_context_retrieval",
        "type": "contains",
        "user": (
            "Read the following context and answer with ONLY the secret token.\n\n"
            + make_long_context_noise("L4-360-NEEDLE-77")
        ),
        "expected_substring": "L4-360-NEEDLE-77",
    },
    {
        "name": "strict_json_routing",
        "type": "json_fields",
        "user": (
            "Return ONLY valid JSON.\n"
            "You are an internal model router.\n"
            "Task: 'Transcribe this customer support call audio and summarize action items.'\n"
            'Required keys: route, why, realtime_required, modality\n'
            "Valid route values: asr, tts, llm, vision\n"
        ),
        "required_keys": ["route", "why", "realtime_required", "modality"],
        "field_validators": {
            "route": lambda v: v == "asr",
            "realtime_required": lambda v: isinstance(v, bool),
            "modality": lambda v: isinstance(v, str) and "audio" in v.lower(),
        },
    },
]


@dataclass
class RunResult:
    model: str
    task_name: str
    run_index: int
    success: bool
    score: float
    ttft_sec: Optional[float]
    total_latency_sec: float
    output_tokens_approx: int
    tokens_per_sec_approx: float
    response_text: str
    error: Optional[str]


async def chat_completion_stream(
    client: httpx.AsyncClient,
    base_url: str,
    api_key: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    max_tokens: int,
) -> Tuple[Optional[float], float, str]:
    url = base_url.rstrip("/") + "/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "stream": True,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    started = time.perf_counter()
    ttft: Optional[float] = None
    chunks: List[str] = []

    async with client.stream("POST", url, headers=headers, json=payload, timeout=300.0) as resp:
        resp.raise_for_status()
        async for line in resp.aiter_lines():
            if not line:
                continue
            if not line.startswith("data: "):
                continue
            data = line[len("data: "):].strip()
            if data == "[DONE]":
                break
            try:
                obj = json.loads(data)
            except json.JSONDecodeError:
                continue

            choices = obj.get("choices", [])
            if not choices:
                continue
            delta = choices[0].get("delta", {})
            piece = delta.get("content")
            if piece:
                if ttft is None:
                    ttft = time.perf_counter() - started
                chunks.append(piece)

    total = time.perf_counter() - started
    return ttft, total, "".join(chunks)


def score_task(task: Dict[str, Any], response_text: str) -> Tuple[bool, float, Optional[str]]:
    text = response_text.strip()

    if task["type"] == "exact":
        expected = task["expected"].strip()
        ok = text == expected
        return ok, 1.0 if ok else 0.0, None

    if task["type"] == "contains":
        expected = task["expected_substring"]
        ok = expected in text
        return ok, 1.0 if ok else 0.0, None

    if task["type"] == "json_fields":
        try:
            obj = json.loads(text)
        except Exception as e:
            return False, 0.0, f"invalid_json: {e}"

        score = 0.0
        max_score = 1.0
        required_keys = task.get("required_keys", [])
        if required_keys:
            per_key = 0.6 / len(required_keys)
            for key in required_keys:
                if key in obj:
                    score += per_key

        expected_fields = task.get("expected_fields", {})
        if expected_fields:
            per_field = 0.3 / len(expected_fields)
            for key, expected in expected_fields.items():
                actual = obj.get(key)
                if actual == expected:
                    score += per_field

        field_validators = task.get("field_validators", {})
        if field_validators:
            per_validator = 0.1 / len(field_validators)
            for key, fn in field_validators.items():
                try:
                    if fn(obj.get(key)):
                        score += per_validator
                except Exception:
                    pass

        ok = score >= 0.95
        return ok, min(score, max_score), None

    return False, 0.0, "unknown_task_type"


async def benchmark_one(
    client: httpx.AsyncClient,
    args: argparse.Namespace,
    model: str,
    task: Dict[str, Any],
    run_index: int,
) -> RunResult:
    try:
        ttft, total, text = await chat_completion_stream(
            client=client,
            base_url=args.base_url,
            api_key=args.api_key,
            model=model,
            system_prompt=SYSTEM_PROMPT,
            user_prompt=task["user"],
            temperature=args.temperature,
            max_tokens=args.max_tokens,
        )
        output_tokens = approx_token_count(text)
        tps = output_tokens / total if total > 0 else 0.0
        success, score, err = score_task(task, text)
        return RunResult(
            model=model,
            task_name=task["name"],
            run_index=run_index,
            success=success,
            score=score,
            ttft_sec=ttft,
            total_latency_sec=total,
            output_tokens_approx=output_tokens,
            tokens_per_sec_approx=tps,
            response_text=text,
            error=err,
        )
    except Exception as e:
        return RunResult(
            model=model,
            task_name=task["name"],
            run_index=run_index,
            success=False,
            score=0.0,
            ttft_sec=None,
            total_latency_sec=0.0,
            output_tokens_approx=0,
            tokens_per_sec_approx=0.0,
            response_text="",
            error=str(e),
        )


def summarize(results: List[RunResult]) -> Dict[str, Any]:
    by_model: Dict[str, List[RunResult]] = {}
    for r in results:
        by_model.setdefault(r.model, []).append(r)

    summary: Dict[str, Any] = {}
    for model, rows in by_model.items():
        scores = [r.score for r in rows]
        exact_success = [1 for r in rows if r.success]
        ttfts = [r.ttft_sec for r in rows if r.ttft_sec is not None]
        lats = [r.total_latency_sec for r in rows if r.total_latency_sec > 0]
        tps = [r.tokens_per_sec_approx for r in rows if r.tokens_per_sec_approx > 0]

        summary[model] = {
            "runs": len(rows),
            "success_rate": round(sum(exact_success) / len(rows), 4) if rows else 0.0,
            "mean_score": round(statistics.mean(scores), 4) if scores else 0.0,
            "median_ttft_sec": round(statistics.median(ttfts), 4) if ttfts else None,
            "median_total_latency_sec": round(statistics.median(lats), 4) if lats else None,
            "median_tokens_per_sec_approx": round(statistics.median(tps), 4) if tps else None,
        }
    return summary


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True, help="OpenAI-compatible base URL, e.g. http://localhost:4000/v1")
    parser.add_argument("--api-key", default="dummy", help="API key for the endpoint")
    parser.add_argument("--models", nargs="+", required=True, help="Model IDs to compare")
    parser.add_argument("--runs", type=int, default=3, help="How many times to run each task per model")
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--max-tokens", type=int, default=300)
    parser.add_argument("--out", default="results.jsonl")
    args = parser.parse_args()

    results: List[RunResult] = []

    async with httpx.AsyncClient() as client:
        for model in args.models:
            for task in TASKS:
                for run_index in range(1, args.runs + 1):
                    result = await benchmark_one(client, args, model, task, run_index)
                    results.append(result)
                    print(
                        f"[{model}] [{task['name']}] run={run_index} "
                        f"success={result.success} score={result.score:.2f} "
                        f"ttft={result.ttft_sec} total={result.total_latency_sec:.2f}s"
                    )

    with open(args.out, "w", encoding="utf-8") as f:
        for row in results:
            f.write(json.dumps(asdict(row), ensure_ascii=False) + "\n")

    summary = summarize(results)
    print("\n=== SUMMARY ===")
    print(json.dumps(summary, indent=2))

    summary_path = args.out.rsplit(".", 1)[0] + "_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"\nWrote detailed results to: {args.out}")
    print(f"Wrote summary to: {summary_path}")


if __name__ == "__main__":
    asyncio.run(main())

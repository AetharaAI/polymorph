from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.agent.providers.factory import reset_provider, get_provider
from backend.config.gateway import (
    resolve_openai_compat_api_key,
    resolve_unified_gateway_base,
)


def _candidate_models(prefix: str) -> list[str]:
    models: list[str] = []

    # Exact single-name env
    direct = os.getenv(f"{prefix}_MODEL_NAME")
    if direct:
        models.append(direct)

    # Comma-separated list
    listed = os.getenv(f"{prefix}_MODEL_NAMES", "")
    if listed:
        models.extend([m.strip() for m in listed.split(",") if m.strip()])

    # Indexed names: *_MODEL_NAME_2, *_MODEL_NAME_3, etc.
    for k, v in os.environ.items():
        if not v:
            continue
        if k.startswith(f"{prefix}_MODEL_NAME_"):
            models.append(v.strip())

    # De-dupe preserve order
    deduped: list[str] = []
    seen = set()
    for m in models:
        if m not in seen:
            deduped.append(m)
            seen.add(m)
    return deduped


def _build_targets() -> list[dict[str, str]]:
    targets: list[dict[str, str]] = []

    base_url = resolve_unified_gateway_base(
        explicit=os.getenv("OPENAI_COMPAT_BASE_URL") or os.getenv("LITELLM_MODEL_BASE_URL"),
    )
    api_key = resolve_openai_compat_api_key(
        explicit=os.getenv("OPENAI_COMPAT_API_KEY") or os.getenv("LITELLM_API_KEY"),
    )
    models = _candidate_models("LITELLM")
    direct_model = os.getenv("OPENAI_COMPAT_MODEL")
    if direct_model:
        models = [direct_model, *models]

    deduped_models: list[str] = []
    for model in models:
        clean = model.strip()
        if clean and clean not in deduped_models:
            deduped_models.append(clean)

    if base_url and api_key and deduped_models:
        for model in deduped_models:
            targets.append(
                {
                    "label": f"gateway:{model}",
                    "base_url": base_url,
                    "api_key": api_key,
                    "model": model,
                }
            )

    return targets


async def _run_target(target: dict[str, str]) -> dict:
    os.environ["AGENT_PROVIDER"] = "openai_compat"
    os.environ["OPENAI_COMPAT_BASE_URL"] = target["base_url"]
    os.environ["OPENAI_COMPAT_API_KEY"] = target["api_key"]
    os.environ["AGENT_MODEL"] = target["model"]

    reset_provider()
    provider = get_provider()

    try:
        response = await provider.generate(
            system="You are a terse test assistant.",
            tools=[],
            messages=[{"role": "user", "content": [{"type": "text", "text": "Reply with: OK"}]}],
            max_tokens=40,
            temperature=0,
            enable_thinking=False,
        )
        text = " ".join((b.text or "") for b in response.content if b.type == "text").strip()
        ok = bool(text)
        return {
            "label": target["label"],
            "ok": ok,
            "stop_reason": response.stop_reason,
            "text_preview": text[:120],
            "error": None,
        }
    except Exception as exc:
        return {
            "label": target["label"],
            "ok": False,
            "stop_reason": None,
            "text_preview": "",
            "error": f"{type(exc).__name__}: {exc}",
        }


async def main_async() -> int:
    targets = _build_targets()
    if not targets:
        print(json.dumps({"status": "fail", "error": "No unified gateway targets discovered in env"}, indent=2))
        return 1

    results = []
    for target in targets:
        results.append(await _run_target(target))

    passed = sum(1 for r in results if r["ok"])
    total = len(results)

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pass" if passed == total else "fail",
        "passed": passed,
        "total": total,
        "results": results,
    }

    report_path = Path("backend/evals/reports/provider-matrix.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))

    return 0 if report["status"] == "pass" else 1


def main() -> None:
    raise SystemExit(asyncio.run(main_async()))


if __name__ == "__main__":
    main()

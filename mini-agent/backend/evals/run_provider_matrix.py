from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.agent.providers.factory import reset_provider, get_provider


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

    primary_base = os.getenv("LITELLM_MODEL_BASE_URL")
    primary_key = os.getenv("LITELLM_API_KEY")
    primary_models = _candidate_models("LITELLM")

    secondary_base = os.getenv("LITELLM_2_MODEL_BASE_URL")
    secondary_key = os.getenv("LITELLM_2_API_KEY")
    secondary_models = _candidate_models("LITELLM_2")

    if primary_base and primary_key and primary_models:
        for model in primary_models:
            targets.append(
                {
                    "label": f"litellm-primary:{model}",
                    "base_url": primary_base,
                    "api_key": primary_key,
                    "model": model,
                }
            )

    if secondary_base and secondary_key and secondary_models:
        for model in secondary_models:
            targets.append(
                {
                    "label": f"litellm-secondary:{model}",
                    "base_url": secondary_base,
                    "api_key": secondary_key,
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
        print(json.dumps({"status": "fail", "error": "No LiteLLM targets discovered in env"}, indent=2))
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

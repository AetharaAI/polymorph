from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.agent.providers import get_provider, provider_metadata, reset_provider
from backend.agent.tools import file_ops
from backend.agent.tools.artifact_validator import validate_artifact
from backend.agent.tools.calculator import calculate
from backend.agent.tools.code_executor import execute_python
from backend.agent.tools.registry import dispatch_tool
from backend.agent.tools.shell import run_shell


@dataclass(slots=True)
class EvalResult:
    name: str
    ok: bool
    duration_ms: int
    detail: str


async def _run_test(name: str, fn) -> EvalResult:
    start = time.perf_counter()
    try:
        ok, detail = await fn()
    except Exception as exc:
        ok, detail = False, f"exception[{type(exc).__name__}]: {exc}"
    duration_ms = int((time.perf_counter() - start) * 1000)
    return EvalResult(name=name, ok=ok, duration_ms=duration_ms, detail=detail)


async def test_calculator() -> tuple[bool, str]:
    val = calculate("230 * 0.5")
    return val == "115", f"result={val}"


async def test_shell_allowlist() -> tuple[bool, str]:
    good = await run_shell("pwd")
    blocked = await run_shell("rm -rf /")
    ok = not str(good).startswith("Error") and "not allowed" in blocked
    return ok, f"pwd_ok={not str(good).startswith('Error')} blocked_msg={blocked[:80]}"


async def test_python_exec() -> tuple[bool, str]:
    out = await execute_python("print(6*7)", timeout=8)
    ok = (
        not out.startswith("Error")
        and "--- stdout ---" in out
        and "42" in out
        and "--- exit code:" not in out
    )
    return ok, out[:240]


async def test_dispatch_fallback() -> tuple[bool, str]:
    # This expression should work in calculator path.
    out = await dispatch_tool("calculate", {"expression": "sqrt(144)"}, session_id="eval")
    return "12" in out and not out.startswith("Error"), out


async def test_file_roundtrip() -> tuple[bool, str]:
    session = f"eval-{uuid.uuid4().hex[:8]}"
    write_res = await file_ops.write_file("notes.md", "# hello\ncontent", session)
    data = json.loads(write_res)
    file_id = data["file_id"]
    read_res = await file_ops.read_file(file_id)
    listed = await file_ops.list_files(session)

    ok = "hello" in read_res and file_id in listed
    return ok, f"file_id={file_id} validation={data.get('validation', {}).get('status')}"


async def test_artifact_validation() -> tuple[bool, str]:
    broken_csv = "a,b,c\n1,2\n3,4,5"
    val = validate_artifact("bad.csv", broken_csv)
    ok = val["status"] == "invalid"
    return ok, json.dumps(val)


async def test_provider_config() -> tuple[bool, str]:
    info = provider_metadata()
    if info.get("configured"):
        return True, json.dumps(info)
    return True, json.dumps({**info, "note": "provider credentials not present; live contract check skipped"})


async def test_provider_contract_live() -> tuple[bool, str]:
    provider = get_provider()
    response = await provider.generate(
        system="You are a terse assistant.",
        tools=[],
        messages=[{"role": "user", "content": [{"type": "text", "text": "Reply with OK"}]}],
        max_tokens=40,
        temperature=0,
        enable_thinking=False,
    )
    text = " ".join((b.text or "") for b in response.content if b.type == "text").strip()
    thinking = " ".join((b.thinking or "") for b in response.content if b.type == "thinking").strip()
    ok = response.stop_reason in {"end_turn", "tool_use"} and bool(text or thinking)
    return ok, f"stop_reason={response.stop_reason} text={text[:80]} thinking={thinking[:80]}"


async def test_provider_failover_live() -> tuple[bool, str]:
    from backend.agent.providers.failover_provider import FailoverProvider
    from backend.agent.providers.factory import _build_single_provider

    fallback_provider = os.getenv("AGENT_FALLBACK_PROVIDER", "").strip()
    fallback_base = os.getenv("AGENT_FALLBACK_BASE_URL", "").strip()
    fallback_api_key = os.getenv("AGENT_FALLBACK_API_KEY", "").strip()
    fallback_model = os.getenv("AGENT_FALLBACK_MODEL", "").strip()

    if not (fallback_provider and fallback_api_key and fallback_model):
        return True, "explicit fallback not configured; skipping live failover check"

    primary = _build_single_provider(
        "openai",
        base_url="https://api.openai.com/v1-bad",
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name=os.getenv("AGENT_MODEL", "gpt-5.4"),
        label="forced_primary_failure",
    )
    fallback = _build_single_provider(
        fallback_provider,
        base_url=fallback_base or None,
        api_key=fallback_api_key,
        model_name=fallback_model,
        label="explicit_live_fallback",
    )
    provider = FailoverProvider([primary, fallback])
    response = await provider.generate(
        system="You are a terse assistant.",
        tools=[],
        messages=[{"role": "user", "content": [{"type": "text", "text": "Reply with OK"}]}],
        max_tokens=40,
        temperature=0,
        enable_thinking=False,
    )
    text = " ".join((b.text or "") for b in response.content if b.type == "text").strip()
    ok = response.fallback_used and bool(text)
    return ok, f"provider={response.provider_name} fallback_used={response.fallback_used} text={text[:80]}"


async def run_suite(live_provider: bool) -> dict[str, Any]:
    tests = [
        ("calculator", test_calculator),
        ("shell_allowlist", test_shell_allowlist),
        ("python_exec", test_python_exec),
        ("dispatch_fallback", test_dispatch_fallback),
        ("file_roundtrip", test_file_roundtrip),
        ("artifact_validation", test_artifact_validation),
        ("provider_config", test_provider_config),
    ]

    if live_provider:
        tests.append(("provider_contract_live", test_provider_contract_live))
        tests.append(("provider_failover_live", test_provider_failover_live))

    results: list[EvalResult] = []
    for name, fn in tests:
        results.append(await _run_test(name, fn))

    passed = sum(1 for r in results if r.ok)
    total = len(results)

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "passed": passed,
        "total": total,
        "status": "pass" if passed == total else "fail",
        "live_provider": live_provider,
        "provider": provider_metadata(),
        "results": [asdict(r) for r in results],
    }

    return summary


def write_report(report: dict[str, Any], report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run deterministic harness eval suite")
    parser.add_argument(
        "--live-provider",
        action="store_true",
        help="Execute one live provider contract call (requires provider credentials).",
    )
    parser.add_argument(
        "--report",
        default="backend/evals/reports/latest.json",
        help="Report output path.",
    )
    return parser.parse_args()


async def main_async() -> int:
    args = parse_args()
    reset_provider()
    report = await run_suite(live_provider=args.live_provider)
    write_report(report, Path(args.report))

    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "pass" else 1


def main() -> None:
    code = asyncio.run(main_async())
    raise SystemExit(code)


if __name__ == "__main__":
    main()

import shutil
import sys
import json
from datetime import datetime, timezone
from pathlib import Path

from backend.agent.providers import provider_metadata
from backend.agent.tools import calculator, code_executor, shell
from backend.memory import get_memory_service


async def run_tool_health_checks() -> dict:
    """Run lightweight readiness checks for core tools."""
    from backend.agent.tools.registry import TOOL_DEFINITIONS

    checks = {
        "provider_config": {"ok": True, "detail": "", "value": ""},
        "execute_python": {"ok": True, "detail": "", "value": ""},
        "calculate": {"ok": True, "detail": "", "value": ""},
        "run_shell": {"ok": True, "detail": "", "value": ""},
    }

    provider = provider_metadata()
    checks["provider_config"]["value"] = f"{provider.get('provider')}:{provider.get('model')}"
    if not provider.get("configured"):
        checks["provider_config"]["ok"] = False
        checks["provider_config"]["detail"] = provider.get("detail", "Provider misconfigured")
    else:
        checks["provider_config"]["detail"] = "ok"

    python_path = shutil.which("python3") or shutil.which("python") or sys.executable
    checks["execute_python"]["value"] = python_path or ""
    if not python_path:
        checks["execute_python"]["ok"] = False
        checks["execute_python"]["detail"] = "No python interpreter found"
    else:
        py_result = await code_executor.execute_python("print(2+2)", timeout=8)
        if str(py_result).startswith("Error"):
            checks["execute_python"]["ok"] = False
            checks["execute_python"]["detail"] = py_result
        else:
            checks["execute_python"]["detail"] = "ok"

    calc_result = calculator.calculate("2 + 2")
    checks["calculate"]["value"] = calc_result
    if calc_result != "4":
        checks["calculate"]["ok"] = False
        checks["calculate"]["detail"] = calc_result
    else:
        checks["calculate"]["detail"] = "ok"

    shell_result = await shell.run_shell("pwd")
    checks["run_shell"]["value"] = shell_result[:120]
    if str(shell_result).startswith("Error"):
        checks["run_shell"]["ok"] = False
        checks["run_shell"]["detail"] = shell_result
    else:
        checks["run_shell"]["detail"] = "ok"

    healthy_count = sum(1 for item in checks.values() if item["ok"])
    total = len(checks)
    overall = "healthy" if healthy_count == total else "degraded"

    return {
        "status": overall,
        "healthy_count": healthy_count,
        "total": total,
        "registered_tool_count": len(TOOL_DEFINITIONS),
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
    }


async def get_harness_status() -> str:
    from backend.agent.tools.registry import TOOL_DEFINITIONS

    memory = await get_memory_service()
    provider = provider_metadata()
    tool_names = [tool["name"] for tool in TOOL_DEFINITIONS]
    memory_status = {
        "namespace": getattr(memory, "memory_namespace", ""),
        "mongo_db": getattr(memory, "mongo_db_name", ""),
        "degraded_mode": bool(getattr(memory, "degraded_mode", False)),
        "redis_connected": getattr(memory, "redis", None) is not None,
        "mongo_connected": getattr(memory, "mongo", None) is not None,
        "qdrant_connected": getattr(memory, "qdrant", None) is not None,
        "postgres_connected": getattr(memory, "postgres", None) is not None,
    }
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "provider": provider,
        "tool_count": len(tool_names),
        "tools": tool_names,
        "skills_registry_path": str(Path(__file__).resolve().parents[2] / "SKILLS.md"),
        "memory": memory_status,
    }
    return json.dumps(payload, indent=2, sort_keys=True)

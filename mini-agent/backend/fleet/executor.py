from __future__ import annotations

import asyncio
import json
import os
import shlex
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from backend.fleet.inventory import FleetInventory, NodeInventory
from backend.fleet.scripts import SCRIPT_DIR, ScriptAudit, audit_helper_scripts


DEFAULT_REMOTE_TIMEOUT = int(os.getenv("FLEET_REMOTE_TIMEOUT_SECONDS", "300"))
DEFAULT_SSH_CONNECT_TIMEOUT = int(os.getenv("FLEET_SSH_CONNECT_TIMEOUT_SECONDS", "10"))
MAX_OUTPUT_CHARS = int(os.getenv("FLEET_REMOTE_MAX_OUTPUT_CHARS", "12000"))


def _trim(text: str) -> str:
    if len(text) <= MAX_OUTPUT_CHARS:
        return text
    return text[:MAX_OUTPUT_CHARS] + f"\n...[truncated {len(text) - MAX_OUTPUT_CHARS} chars]"


def _quote_args(args: list[str]) -> str:
    return " ".join(shlex.quote(arg) for arg in args)


def _expand_compare(path: str, node: NodeInventory) -> str:
    text = (path or "").strip().replace("${HOME}", "__HOME__").replace("$HOME", "__HOME__")
    if text.startswith("~/"):
        text = "__HOME__/" + text[2:]
    if node.ssh_user:
        text = text.replace(f"/home/{node.ssh_user}", "__HOME__")
    return text.rstrip("/")


def _is_allowed_path(candidate: str, allowed_roots: tuple[str, ...], node: NodeInventory) -> bool:
    candidate_cmp = _expand_compare(candidate, node)
    for root in allowed_roots:
        root_cmp = _expand_compare(root, node)
        if candidate_cmp == root_cmp or candidate_cmp.startswith(root_cmp + "/"):
            return True
    return False


def _script_with_arg_expansion(script_content: str) -> str:
    body = script_content
    if body.startswith("#!"):
        body = "\n".join(body.splitlines()[1:])
    return (
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n"
        "expanded_args=()\n"
        "for raw in \"$@\"; do\n"
        "  if [[ \"$raw\" == ~/* ]]; then\n"
        "    expanded_args+=(\"$HOME/${raw#~/}\")\n"
        "  elif [[ \"$raw\" == '$HOME/'* ]]; then\n"
        "    expanded_args+=(\"${HOME}/${raw#'$HOME/'}\")\n"
        "  elif [[ \"$raw\" == '${HOME}/'* ]]; then\n"
        "    expanded_args+=(\"${HOME}/${raw#'${HOME}/'}\")\n"
        "  else\n"
        "    expanded_args+=(\"$raw\")\n"
        "  fi\n"
        "done\n"
        "set -- \"${expanded_args[@]}\"\n"
        + body
        + "\n"
    )


@dataclass(frozen=True)
class ExecutionResult:
    ok: bool
    action: str
    node: str
    ssh_target: str
    script: str
    dry_run: bool
    requires_confirmation: bool
    blocked: bool
    command_preview: str
    exit_code: int | None
    stdout: str
    stderr: str
    duration_ms: int
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "action": self.action,
            "node": self.node,
            "ssh_target": self.ssh_target,
            "script": self.script,
            "dry_run": self.dry_run,
            "requires_confirmation": self.requires_confirmation,
            "blocked": self.blocked,
            "command_preview": self.command_preview,
            "exit_code": self.exit_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "duration_ms": self.duration_ms,
            "error": self.error,
        }


class FleetExecutor:
    def __init__(self, inventory: FleetInventory) -> None:
        self.inventory = inventory
        self.script_audits = audit_helper_scripts(inventory)

    def get_script_audit(self, action: str) -> ScriptAudit:
        audit = self.script_audits.get(action)
        if audit is None:
            raise ValueError(f"No helper script registered for action '{action}'")
        return audit

    def _ssh_target(self, node: NodeInventory) -> str:
        if not node.host_ip:
            raise ValueError(f"Node '{node.name}' has no host IP in poly-tailscale-nodes.yaml")
        user = node.ssh_user or "poly"
        return f"{user}@{node.host_ip}"

    def _requires_confirmation(self, action: str) -> bool:
        payload = self.inventory.safe_actions.get(action) or {}
        return bool(payload.get("destructive") or payload.get("requires_explicit_approval"))

    def _command_preview(self, node: NodeInventory, script_path: Path, args: list[str]) -> str:
        target = self._ssh_target(node)
        return (
            f"ssh -o BatchMode=yes -o ConnectTimeout={DEFAULT_SSH_CONNECT_TIMEOUT} {shlex.quote(target)} "
            f"'bash -s -- {_quote_args(args)}' < {shlex.quote(str(script_path))}"
        )

    async def run_script(
        self,
        *,
        action: str,
        node_name: str,
        script_args: list[str] | None = None,
        dry_run: bool = False,
        approved: bool = False,
        timeout: int = DEFAULT_REMOTE_TIMEOUT,
    ) -> ExecutionResult:
        node = self.inventory.resolve_node(node_name)
        audit = self.get_script_audit(action)
        script_path = Path(audit.path)
        target = self._ssh_target(node)
        args = list(script_args or [])
        preview = self._command_preview(node, script_path, args)
        needs_confirmation = self._requires_confirmation(action)

        if dry_run:
            return ExecutionResult(
                ok=True,
                action=action,
                node=node.name,
                ssh_target=target,
                script=str(script_path),
                dry_run=True,
                requires_confirmation=needs_confirmation,
                blocked=False,
                command_preview=preview,
                exit_code=None,
                stdout="",
                stderr="",
                duration_ms=0,
                error=None,
            )

        if needs_confirmation and not approved:
            return ExecutionResult(
                ok=False,
                action=action,
                node=node.name,
                ssh_target=target,
                script=str(script_path),
                dry_run=dry_run,
                requires_confirmation=needs_confirmation,
                blocked=True,
                command_preview=preview,
                exit_code=None,
                stdout="",
                stderr="",
                duration_ms=0,
                error="Explicit approval is required for this action.",
            )

        started = time.time()
        script_content = _script_with_arg_expansion(script_path.read_text(encoding="utf-8"))
        ssh_command = [
            "ssh",
            "-o",
            "BatchMode=yes",
            "-o",
            f"ConnectTimeout={DEFAULT_SSH_CONNECT_TIMEOUT}",
            target,
            "bash",
            "-s",
            "--",
            *args,
        ]
        try:
            result = await asyncio.to_thread(
                subprocess.run,
                ssh_command,
                input=script_content,
                text=True,
                capture_output=True,
                timeout=max(1, min(int(timeout), 1800)),
            )
            duration_ms = int((time.time() - started) * 1000)
            return ExecutionResult(
                ok=result.returncode == 0,
                action=action,
                node=node.name,
                ssh_target=target,
                script=str(script_path),
                dry_run=False,
                requires_confirmation=needs_confirmation,
                blocked=False,
                command_preview=preview,
                exit_code=result.returncode,
                stdout=_trim(result.stdout or ""),
                stderr=_trim(result.stderr or ""),
                duration_ms=duration_ms,
                error=None if result.returncode == 0 else "Remote command exited non-zero.",
            )
        except subprocess.TimeoutExpired as exc:
            duration_ms = int((time.time() - started) * 1000)
            return ExecutionResult(
                ok=False,
                action=action,
                node=node.name,
                ssh_target=target,
                script=str(script_path),
                dry_run=False,
                requires_confirmation=needs_confirmation,
                blocked=False,
                command_preview=preview,
                exit_code=None,
                stdout=_trim(exc.stdout or ""),
                stderr=_trim(exc.stderr or ""),
                duration_ms=duration_ms,
                error=f"Remote command timed out after {timeout} seconds.",
            )
        except Exception as exc:
            duration_ms = int((time.time() - started) * 1000)
            return ExecutionResult(
                ok=False,
                action=action,
                node=node.name,
                ssh_target=target,
                script=str(script_path),
                dry_run=False,
                requires_confirmation=needs_confirmation,
                blocked=False,
                command_preview=preview,
                exit_code=None,
                stdout="",
                stderr="",
                duration_ms=duration_ms,
                error=str(exc),
            )

    async def run_model_locate(
        self,
        *,
        node_name: str,
        pattern: str,
        dry_run: bool = False,
        timeout: int = DEFAULT_REMOTE_TIMEOUT,
    ) -> ExecutionResult:
        node = self.inventory.resolve_node(node_name)
        return await self.run_script(
            action="model-locate",
            node_name=node.name,
            script_args=[node.name, pattern],
            dry_run=dry_run,
            approved=True,
            timeout=timeout,
        )

    async def run_model_download(
        self,
        *,
        node_name: str,
        repo_id: str,
        destination: str,
        extra_args: list[str] | None = None,
        dry_run: bool = True,
        approved: bool = False,
        timeout: int = DEFAULT_REMOTE_TIMEOUT,
    ) -> ExecutionResult:
        node = self.inventory.resolve_node(node_name)
        allowed_roots = node.action_map.get("model-download", ())
        if not _is_allowed_path(destination, allowed_roots, node):
            return ExecutionResult(
                ok=False,
                action="model-download",
                node=node.name,
                ssh_target=self._ssh_target(node),
                script=str(SCRIPT_DIR / "model-download.sh"),
                dry_run=dry_run,
                requires_confirmation=True,
                blocked=True,
                command_preview=self._command_preview(node, SCRIPT_DIR / "model-download.sh", [node.name, repo_id, destination]),
                exit_code=None,
                stdout="",
                stderr="",
                duration_ms=0,
                error=f"Destination '{destination}' is not approved for node '{node.name}'.",
            )
        script_args = [node.name, repo_id, destination, *(extra_args or [])]
        return await self.run_script(
            action="model-download",
            node_name=node.name,
            script_args=script_args,
            dry_run=dry_run,
            approved=approved,
            timeout=timeout,
        )

    def as_json(self, result: ExecutionResult) -> str:
        return json.dumps(result.to_dict(), ensure_ascii=False, indent=2)

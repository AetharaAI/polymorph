from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import re

from backend.fleet.inventory import FleetInventory


SCRIPT_DIR = Path(__file__).resolve().parents[3] / "fleet-inventory" / "scripts"
SCRIPT_INPUTS = {
    "compose-validate": ["compose_root?"],
    "disk-status": [],
    "docker-ps": [],
    "gpu-status": [],
    "model-download": ["node_name", "repo_id", "dest_root", "extra_hf_args*"],
    "model-locate": ["node_name", "pattern"],
    "stack-health": ["compose_root?"],
    "stack-start": ["compose_root?"],
    "stack-stop": ["compose_root?"],
}
SCRIPT_CLASS_MARKERS = {
    "compose-validate": ["docker compose config"],
    "disk-status": ["df -h", "df -i", "lsblk", "mount"],
    "docker-ps": ["docker ps -a", "docker compose ls"],
    "gpu-status": ["nvidia-smi", "nvidia-smi topo -m", "nvidia-smi pmon"],
    "model-download": ["hf download", "is_allowed_dest", "repo-id"],
    "model-locate": ["find \"$root\" -iname", "ROOTS=("],
    "stack-health": ["docker compose ps", "docker ps --format"],
    "stack-start": ["docker compose up -d"],
    "stack-stop": ["docker compose stop"],
}
REMOTE_EXECUTED = {
    "compose-validate",
    "disk-status",
    "docker-ps",
    "gpu-status",
    "model-download",
    "model-locate",
    "stack-health",
    "stack-start",
    "stack-stop",
}


@dataclass(frozen=True)
class ScriptAudit:
    name: str
    path: str
    inferred_class: str | None
    expected_inputs: tuple[str, ...]
    execution_mode: str
    relevant: bool
    command_markers: tuple[str, ...]
    path_literals: tuple[str, ...]
    mismatches: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "path": self.path,
            "inferred_class": self.inferred_class,
            "expected_inputs": list(self.expected_inputs),
            "execution_mode": self.execution_mode,
            "relevant": self.relevant,
            "command_markers": list(self.command_markers),
            "path_literals": list(self.path_literals),
            "mismatches": list(self.mismatches),
        }


def _read_script(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_path_literals(content: str) -> list[str]:
    values = re.findall(r"(/mnt/[A-Za-z0-9._+\-/]+|~/[A-Za-z0-9._+\-/]+)", content)
    deduped: list[str] = []
    for value in values:
        if value not in deduped:
            deduped.append(value)
    return deduped


def _infer_class(content: str) -> str | None:
    best_name = None
    best_score = 0
    lowered = content.lower()
    for name, markers in SCRIPT_CLASS_MARKERS.items():
        score = 0
        for marker in markers:
            if marker.lower() in lowered:
                score += 1
        if score > best_score:
            best_name = name
            best_score = score
    return best_name


def _extract_case_block_paths(content: str, node_name: str) -> list[str]:
    match = re.search(rf"{re.escape(node_name)}\)(.*?);;", content, flags=re.DOTALL)
    if not match:
        return []
    block = match.group(1)
    values = _extract_path_literals(block)
    cleaned: list[str] = []
    for value in values:
        normalized = value.rstrip("*")
        if normalized not in cleaned:
            cleaned.append(normalized)
    return cleaned


def audit_helper_scripts(inventory: FleetInventory) -> dict[str, ScriptAudit]:
    audits: dict[str, ScriptAudit] = {}
    for script_path in sorted(SCRIPT_DIR.glob("*.sh")):
        name = script_path.stem
        content = _read_script(script_path)
        inferred = _infer_class(content)
        path_literals = _extract_path_literals(content)
        mismatches: list[str] = []

        if inferred and inferred != name:
            mismatches.append(
                f"Filename suggests '{name}' but content matches '{inferred}' more closely."
            )

        manifest_action = inventory.safe_actions.get(name)
        if manifest_action is None:
            mismatches.append("No matching safe_action entry in operator-manifest.yaml.")

        if name in {"compose-validate", "docker-ps", "stack-health", "stack-start", "stack-stop"}:
            for node in inventory.nodes.values():
                compose_roots = node.approved_paths.get("compose_roots", ())
                documented = {root.path for root in node.documented_non_mount_roots}
                for compose_root in compose_roots:
                    if compose_root not in documented:
                        mismatches.append(
                            f"{node.name}: compose root '{compose_root}' is approved in the manifest but not documented in model-inventory.yaml."
                        )

        if name in {"model-locate", "model-download"}:
            for node in inventory.nodes.values():
                allowed = set(node.action_map.get(name, ()))
                relevant_literals = _extract_case_block_paths(content, node.name)
                for literal in sorted(relevant_literals):
                    if literal not in allowed:
                        mismatches.append(
                            f"{node.name}: literal path '{literal}' appears in the script but is not approved for action '{name}' on that node."
                        )

        execution_mode = "remote_over_ssh" if name in REMOTE_EXECUTED else "local_only"
        audits[name] = ScriptAudit(
            name=name,
            path=str(script_path),
            inferred_class=inferred,
            expected_inputs=tuple(SCRIPT_INPUTS.get(name, ())),
            execution_mode=execution_mode,
            relevant=name in SCRIPT_CLASS_MARKERS,
            command_markers=tuple(marker for marker in SCRIPT_CLASS_MARKERS.get(name, ()) if marker.lower() in content.lower()),
            path_literals=tuple(path_literals),
            mismatches=tuple(mismatches),
        )
    return audits

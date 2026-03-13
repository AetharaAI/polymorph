from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any
import re

import yaml


FLEET_DIR = Path(__file__).resolve().parents[3] / "fleet-inventory"
MODEL_TAGS = {
    "agent",
    "asr",
    "audio",
    "awq",
    "coder",
    "detection",
    "diffusion",
    "embeddings",
    "kimi",
    "llm",
    "multimodal",
    "music",
    "ocr",
    "pose",
    "qwen",
    "redwatch",
    "reranker",
    "security",
    "sensors",
    "sound",
    "tracking",
    "tts",
    "vision",
    "voice",
    "whisper",
    "yolo",
}
_SUMMARY_NODE_MAP = {
    "L40S-180": "l40s-180",
    "L4-360": "l4-360",
    "L40S-90": "l40s-90",
}


def _status_bucket(raw_status: str | None) -> str | None:
    if not raw_status:
        return None
    value = raw_status.strip().lower()
    if value == "known_root_unexpanded":
        return "known_root_unexpanded"
    if value.endswith("_from_doc") or value == "documented":
        return "documented"
    if value.startswith("confirmed") or value.startswith("partially_confirmed"):
        return "confirmed"
    return value


def _status_detail(raw_status: str | None) -> str | None:
    if not raw_status:
        return None
    value = raw_status.strip().lower()
    if value.startswith("partially_"):
        return "partial"
    if value.endswith("_from_doc"):
        return "from_doc"
    return None


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def _compare_path(value: str, ssh_user: str | None = None) -> str:
    text = (value or "").strip()
    if not text:
        return ""
    text = text.replace("${HOME}", "__HOME__").replace("$HOME", "__HOME__")
    if text.startswith("~/"):
        text = "__HOME__/" + text[2:]
    if ssh_user:
        text = text.replace(f"/home/{ssh_user}", "__HOME__")
    return text.rstrip("/")


@dataclass(frozen=True)
class InventoryPath:
    path: str
    raw_status: str | None = None
    status: str | None = None
    status_detail: str | None = None
    tags: tuple[str, ...] = ()
    kind: str | None = None
    todo_expansion: str | None = None
    source: str | None = None
    children: tuple["InventoryPath", ...] = ()

    def flatten(self) -> list["InventoryPath"]:
        rows = [self]
        for child in self.children:
            rows.extend(child.flatten())
        return rows

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "raw_status": self.raw_status,
            "status": self.status,
            "status_detail": self.status_detail,
            "tags": list(self.tags),
            "kind": self.kind,
            "todo_expansion": self.todo_expansion,
            "source": self.source,
            "children": [child.to_dict() for child in self.children],
        }


@dataclass(frozen=True)
class ModelPlacement:
    node_name: str
    path: str
    name: str
    raw_status: str | None
    status: str | None
    tags: tuple[str, ...]
    source: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_name": self.node_name,
            "path": self.path,
            "name": self.name,
            "raw_status": self.raw_status,
            "status": self.status,
            "tags": list(self.tags),
            "source": self.source,
        }


@dataclass(frozen=True)
class PathMismatch:
    source: str
    key: str
    expected_path: str
    mismatch_type: str
    detail: str
    matched_documented_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "key": self.key,
            "expected_path": self.expected_path,
            "mismatch_type": self.mismatch_type,
            "detail": self.detail,
            "matched_documented_path": self.matched_documented_path,
        }


@dataclass(frozen=True)
class NodeInventory:
    name: str
    host_alias: str | None
    host_ip: str | None
    ssh_user: str | None
    roles: tuple[str, ...]
    notes: tuple[str, ...]
    mounts: tuple[InventoryPath, ...]
    documented_non_mount_roots: tuple[InventoryPath, ...]
    approved_paths: dict[str, tuple[str, ...]]
    action_map: dict[str, tuple[str, ...]]
    tailscale_paths: dict[str, str]
    storage_summary: dict[str, Any]
    storage_role: str | None
    summary_excerpt: str | None
    path_mismatches: tuple[PathMismatch, ...]
    model_placements: tuple[ModelPlacement, ...]

    def all_documented_paths(self) -> list[InventoryPath]:
        rows: list[InventoryPath] = []
        for mount in self.mounts:
            rows.extend(mount.flatten())
        for root in self.documented_non_mount_roots:
            rows.extend(root.flatten())
        return rows

    def model_families(self) -> list[str]:
        families = set()
        for placement in self.model_placements:
            for tag in placement.tags:
                if tag in MODEL_TAGS:
                    families.add(tag)
        return sorted(families)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "host_alias": self.host_alias,
            "host_ip": self.host_ip,
            "ssh_user": self.ssh_user,
            "roles": list(self.roles),
            "notes": list(self.notes),
            "tailscale_paths": dict(self.tailscale_paths),
            "storage_role": self.storage_role,
            "storage_summary": self.storage_summary,
            "summary_excerpt": self.summary_excerpt,
            "mounts": [mount.to_dict() for mount in self.mounts],
            "documented_non_mount_roots": [root.to_dict() for root in self.documented_non_mount_roots],
            "approved_paths": {key: list(values) for key, values in self.approved_paths.items()},
            "action_map": {key: list(values) for key, values in self.action_map.items()},
            "path_mismatches": [item.to_dict() for item in self.path_mismatches],
            "model_families": self.model_families(),
            "model_placements": [placement.to_dict() for placement in self.model_placements],
        }


@dataclass(frozen=True)
class FleetInventory:
    generated_at: str | None
    owner: str | None
    purpose: str | None
    nodes: dict[str, NodeInventory]
    safe_actions: dict[str, dict[str, Any]]
    raw_docs: dict[str, str]
    source_dir: Path = field(default=FLEET_DIR)

    def node_names(self) -> list[str]:
        return sorted(self.nodes.keys())

    def resolve_node(self, node_name: str) -> NodeInventory:
        query = (node_name or "").strip().lower()
        if not query:
            raise KeyError("node name is required")
        if query in self.nodes:
            return self.nodes[query]
        for node in self.nodes.values():
            if query in {
                (node.host_alias or "").lower(),
                (node.host_ip or "").lower(),
            }:
                return node
        raise KeyError(f"Unknown node '{node_name}'")

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "owner": self.owner,
            "purpose": self.purpose,
            "nodes": {name: node.to_dict() for name, node in self.nodes.items()},
            "safe_actions": self.safe_actions,
            "raw_docs": dict(self.raw_docs),
            "source_dir": str(self.source_dir),
        }


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _parse_inventory_path(payload: dict[str, Any], *, source: str) -> InventoryPath:
    raw_status = payload.get("status")
    children = tuple(_parse_inventory_path(child, source=source) for child in payload.get("children", []) or [])
    return InventoryPath(
        path=str(payload.get("path") or ""),
        raw_status=raw_status,
        status=_status_bucket(raw_status),
        status_detail=_status_detail(raw_status),
        tags=tuple(str(tag) for tag in payload.get("tags", []) or []),
        kind=payload.get("kind"),
        todo_expansion=payload.get("todo_expansion"),
        source=source,
        children=children,
    )


def _flatten_model_placements(node_name: str, paths: list[InventoryPath]) -> list[ModelPlacement]:
    placements: list[ModelPlacement] = []
    for entry in paths:
        basename = Path(entry.path).name
        if basename in {"models", "llm", "vision", "voice", "audio", "sensors", "embeddings", "rerankers"}:
            continue
        if not (set(entry.tags) & MODEL_TAGS):
            continue
        placements.append(
            ModelPlacement(
                node_name=node_name,
                path=entry.path,
                name=basename,
                raw_status=entry.raw_status,
                status=entry.status,
                tags=entry.tags,
                source=entry.source or "unknown",
            )
        )
    return placements


def _case_insensitive_match(expected_path: str, documented_paths: list[str], ssh_user: str | None) -> str | None:
    compare_expected = _compare_path(expected_path, ssh_user).lower()
    for candidate in documented_paths:
        if _compare_path(candidate, ssh_user).lower() == compare_expected:
            return candidate
    return None


def _summary_sections(markdown: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in markdown.splitlines():
        match = re.match(r"^\d+\)\s+([A-Z0-9-]+)\s*$", line.strip())
        if match:
            current = _SUMMARY_NODE_MAP.get(match.group(1))
            if current:
                sections[current] = []
            continue
        if current:
            sections[current].append(line)
    return {key: "\n".join(value).strip() for key, value in sections.items() if value}


@lru_cache(maxsize=1)
def load_fleet_inventory() -> FleetInventory:
    model_inventory = _load_yaml(FLEET_DIR / "model-inventory.yaml")
    operator_manifest = _load_yaml(FLEET_DIR / "operator-manifest.yaml")
    tailscale_inventory = _load_yaml(FLEET_DIR / "poly-tailscale-nodes.yaml")
    storage_summary = _load_yaml(FLEET_DIR / "fleet-storage-3-nodes.yaml")
    summary_markdown = _read_text(FLEET_DIR / "fleet-storage-inventory-summary-2026-03-13.md")
    summary_text = _read_text(FLEET_DIR / "fleet-storage-inventory-summary-2026-03-13.txt")

    summary_sections = _summary_sections(summary_markdown)
    tailscale_nodes = {
        str(item.get("name")).strip().lower(): item
        for item in tailscale_inventory.get("nodes", []) or []
        if item.get("name")
    }
    manifest_nodes = {
        str(name).strip().lower(): payload
        for name, payload in (operator_manifest.get("nodes") or {}).items()
    }
    model_nodes = {
        str(item.get("node_name")).strip().lower(): item
        for item in model_inventory.get("nodes", []) or []
        if item.get("node_name")
    }
    storage_nodes = {
        str(name).strip().lower(): payload
        for name, payload in (storage_summary.get("fleet") or {}).items()
    }

    node_names = sorted(set(tailscale_nodes) | set(manifest_nodes) | set(model_nodes) | set(storage_nodes))
    nodes: dict[str, NodeInventory] = {}

    for node_name in node_names:
        model_payload = model_nodes.get(node_name, {})
        manifest_payload = manifest_nodes.get(node_name, {})
        tailscale_payload = tailscale_nodes.get(node_name, {})
        storage_payload = storage_nodes.get(node_name, {})

        mounts = tuple(
            _parse_inventory_path(item, source="model-inventory.yaml")
            for item in model_payload.get("mounts", []) or []
        )
        documented_non_mount_roots = tuple(
            _parse_inventory_path(item, source="model-inventory.yaml")
            for item in model_payload.get("documented_non_mount_roots", []) or []
        )
        all_documented_paths = [entry.path for root in mounts for entry in root.flatten()]
        all_documented_paths.extend(entry.path for root in documented_non_mount_roots for entry in root.flatten())

        ssh_user = (
            tailscale_payload.get("user")
            or manifest_payload.get("ssh_user")
            or model_payload.get("ssh_user")
        )

        mismatches: list[PathMismatch] = []
        for key, raw_path in (tailscale_payload.get("paths") or {}).items():
            expected_path = str(raw_path)
            if expected_path in all_documented_paths:
                continue
            matched = _case_insensitive_match(expected_path, all_documented_paths, ssh_user)
            if matched:
                mismatches.append(
                    PathMismatch(
                        source="poly-tailscale-nodes.yaml",
                        key=str(key),
                        expected_path=expected_path,
                        mismatch_type="case_or_shape_mismatch",
                        detail="Path is present only as a case/shape mismatch against documented inventory.",
                        matched_documented_path=matched,
                    )
                )
            else:
                mismatches.append(
                    PathMismatch(
                        source="poly-tailscale-nodes.yaml",
                        key=str(key),
                        expected_path=expected_path,
                        mismatch_type="missing_from_documented_inventory",
                        detail="Path is documented in the Tailscale map but not in the detailed fleet inventory.",
                    )
                )

        manifest_paths = []
        approved_paths = manifest_payload.get("approved_paths") or {}
        for key, values in approved_paths.items():
            for value in values or []:
                manifest_paths.append((f"approved_paths.{key}", str(value)))
        action_map = manifest_payload.get("action_map") or {}
        for action_name, payload in action_map.items():
            for value in payload.get("allowed_paths", []) or []:
                manifest_paths.append((f"action_map.{action_name}", str(value)))
        for key, expected_path in manifest_paths:
            if expected_path in all_documented_paths:
                continue
            matched = _case_insensitive_match(expected_path, all_documented_paths, ssh_user)
            if matched:
                continue
            mismatches.append(
                PathMismatch(
                    source="operator-manifest.yaml",
                    key=key,
                    expected_path=expected_path,
                    mismatch_type="approved_but_not_documented",
                    detail="Path is approved in the manifest but not explicitly documented in the detailed inventory.",
                )
            )

        flattened_paths: list[InventoryPath] = []
        for mount in mounts:
            flattened_paths.extend(mount.flatten())
        for root in documented_non_mount_roots:
            flattened_paths.extend(root.flatten())

        model_placements = tuple(_flatten_model_placements(node_name, flattened_paths))

        nodes[node_name] = NodeInventory(
            name=node_name,
            host_alias=model_payload.get("host_alias") or storage_payload.get("host_alias"),
            host_ip=tailscale_payload.get("host"),
            ssh_user=ssh_user,
            roles=tuple(
                _dedupe(
                    [str(role) for role in (tailscale_payload.get("roles") or [])]
                    + ([str(storage_payload.get("role"))] if storage_payload.get("role") else [])
                )
            ),
            notes=tuple(str(note) for note in model_payload.get("notes", []) or []),
            mounts=mounts,
            documented_non_mount_roots=documented_non_mount_roots,
            approved_paths={
                str(key): tuple(str(value) for value in values or [])
                for key, values in approved_paths.items()
            },
            action_map={
                str(action): tuple(str(value) for value in payload.get("allowed_paths", []) or [])
                for action, payload in action_map.items()
            },
            tailscale_paths={
                str(key): str(value)
                for key, value in (tailscale_payload.get("paths") or {}).items()
            },
            storage_summary=storage_payload,
            storage_role=storage_payload.get("role"),
            summary_excerpt=summary_sections.get(node_name),
            path_mismatches=tuple(mismatches),
            model_placements=model_placements,
        )

    safe_actions = operator_manifest.get("safe_actions") or {}
    return FleetInventory(
        generated_at=model_inventory.get("generated_at"),
        owner=model_inventory.get("owner"),
        purpose=model_inventory.get("purpose"),
        nodes=nodes,
        safe_actions=safe_actions,
        raw_docs={
            "fleet_storage_summary_markdown": summary_markdown,
            "fleet_storage_summary_text": summary_text,
        },
        source_dir=FLEET_DIR,
    )

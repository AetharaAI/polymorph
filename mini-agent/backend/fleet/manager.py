from __future__ import annotations

import json
from pathlib import Path
from typing import Any
import re

from backend.fleet.executor import FleetExecutor
from backend.fleet.inventory import FleetInventory, InventoryPath, ModelPlacement, NodeInventory, load_fleet_inventory
from backend.fleet.scripts import audit_helper_scripts


def _tokenize(text: str) -> set[str]:
    cleaned = "".join(ch.lower() if ch.isalnum() else " " for ch in text or "")
    return {token for token in cleaned.split() if token}


def _basename(path: str) -> str:
    return Path(path).name


class FleetManager:
    def __init__(self, inventory: FleetInventory | None = None) -> None:
        self.inventory = inventory or load_fleet_inventory()
        self.executor = FleetExecutor(self.inventory)
        self.script_audits = audit_helper_scripts(self.inventory)

    def list_nodes(self) -> list[dict[str, Any]]:
        rows = []
        for node in self.inventory.nodes.values():
            rows.append(
                {
                    "name": node.name,
                    "host_alias": node.host_alias,
                    "host_ip": node.host_ip,
                    "ssh_user": node.ssh_user,
                    "roles": list(node.roles),
                    "model_families": node.model_families(),
                    "path_mismatch_count": len(node.path_mismatches),
                }
            )
        return rows

    def get_node(self, node_name: str) -> NodeInventory:
        return self.inventory.resolve_node(node_name)

    def list_mounts(self, node_name: str) -> list[dict[str, Any]]:
        node = self.get_node(node_name)
        rows = [mount.to_dict() for mount in node.mounts]
        rows.extend(root.to_dict() for root in node.documented_non_mount_roots)
        return rows

    def list_model_families(self, node_name: str) -> list[str]:
        return self.get_node(node_name).model_families()

    def _placement_matches(self, placement: ModelPlacement, query: str) -> bool:
        tokens = _tokenize(query)
        if not tokens:
            return False
        haystack = _tokenize(placement.path) | _tokenize(" ".join(placement.tags)) | _tokenize(placement.name)
        return tokens <= haystack or bool(tokens & haystack)

    def locate_model(self, query: str, node_name: str | None = None) -> list[dict[str, Any]]:
        placements: list[ModelPlacement] = []
        if node_name:
            placements.extend(self.get_node(node_name).model_placements)
        else:
            for node in self.inventory.nodes.values():
                placements.extend(node.model_placements)

        matches = [placement.to_dict() for placement in placements if self._placement_matches(placement, query)]
        matches.sort(key=lambda item: (item["node_name"], item["path"]))
        return matches

    def find_candidate_nodes(self, requested_capability: str) -> list[dict[str, Any]]:
        tokens = _tokenize(requested_capability)
        rows = []
        for node in self.inventory.nodes.values():
            score = 0
            reasons: list[str] = []
            node_tokens = _tokenize(" ".join(node.roles)) | _tokenize(" ".join(node.notes)) | set(node.model_families())
            for placement in node.model_placements:
                node_tokens |= set(placement.tags)
            for token in tokens:
                if token in node_tokens:
                    score += 2
                    reasons.append(f"matched:{token}")
            if score > 0:
                rows.append(
                    {
                        "node_name": node.name,
                        "score": score,
                        "reasons": reasons,
                        "roles": list(node.roles),
                        "model_families": node.model_families(),
                    }
                )
        rows.sort(key=lambda item: (-item["score"], item["node_name"]))
        return rows

    def resolve_exact_model_paths(self, query: str) -> dict[str, Any]:
        matches = self.locate_model(query)
        return {
            "query": query,
            "matches": matches,
            "match_count": len(matches),
        }

    def _candidate_download_roots(self, node: NodeInventory, semantic_tags: list[str]) -> list[dict[str, Any]]:
        download_roots = node.action_map.get("model-download", ())
        candidates: list[dict[str, Any]] = []
        for path in node.all_documented_paths():
            if not any(path.path == root or path.path.startswith(root + "/") for root in download_roots):
                continue
            if path.path not in download_roots and not path.children:
                continue
            overlap = sorted(set(semantic_tags) & set(path.tags))
            candidates.append(
                {
                    "path": path.path,
                    "status": path.status,
                    "raw_status": path.raw_status,
                    "tags": list(path.tags),
                    "tag_overlap": overlap,
                    "score": len(overlap) * 10 + len(path.tags),
                }
            )
        candidates.sort(key=lambda item: (-item["score"], item["path"]))
        return candidates

    def plan_download_destination(
        self,
        *,
        node_name: str,
        model_name: str,
        semantic_tags: list[str] | None = None,
        repo_id: str | None = None,
    ) -> dict[str, Any]:
        node = self.get_node(node_name)
        tags = sorted(set(semantic_tags or []))
        candidates = self._candidate_download_roots(node, tags)
        chosen = candidates[0] if candidates else None
        repo_leaf_source = (repo_id or model_name).split("/")[-1]
        repo_leaf = re.sub(r"[^A-Za-z0-9._-]+", "-", repo_leaf_source).strip("-") or "model"
        planned_destination = None
        if chosen:
            planned_destination = str(Path(chosen["path"]) / repo_leaf)
        return {
            "node_name": node.name,
            "model_name": model_name,
            "repo_id": repo_id,
            "semantic_tags": tags,
            "candidate_roots": candidates[:12],
            "chosen_root": chosen,
            "planned_destination": planned_destination,
            "note": (
                "Planned destination is derived from documented approved roots plus repo/model basename."
                if planned_destination
                else "No approved documented download root matched the requested semantic tags."
            ),
        }

    def resolve_compose_root(self, node_name: str, stack_name_or_path: str | None = None) -> dict[str, Any]:
        node = self.get_node(node_name)
        approved_roots = list(node.approved_paths.get("compose_roots", ()))
        default_root = approved_roots[0] if approved_roots else None
        raw = (stack_name_or_path or "").strip()
        if not raw or raw in {"control", "default"}:
            return {
                "ok": bool(default_root),
                "compose_root": default_root,
                "source": "default_compose_root",
                "note": None if default_root else "No compose root is approved for this node.",
            }
        if "/" in raw or raw.startswith("~"):
            allowed = raw in approved_roots or any(raw.startswith(root.rstrip("/") + "/") for root in approved_roots)
            return {
                "ok": allowed,
                "compose_root": raw if allowed else None,
                "source": "explicit_path",
                "note": None if allowed else "Compose path is outside approved compose roots.",
            }
        return {
            "ok": False,
            "compose_root": None,
            "source": "named_stack_unresolved",
            "note": (
                "Stack-name-only resolution is intentionally conservative. "
                "Provide an explicit compose root path documented in fleet-inventory."
            ),
        }

    def show_fleet_status(self) -> dict[str, Any]:
        return {
            "generated_at": self.inventory.generated_at,
            "owner": self.inventory.owner,
            "purpose": self.inventory.purpose,
            "node_count": len(self.inventory.nodes),
            "nodes": self.list_nodes(),
            "script_audit_summary": {
                name: {
                    "relevant": audit.relevant,
                    "execution_mode": audit.execution_mode,
                    "mismatch_count": len(audit.mismatches),
                }
                for name, audit in self.script_audits.items()
            },
        }

    def show_node_inventory(self, node_name: str) -> dict[str, Any]:
        node = self.get_node(node_name)
        payload = node.to_dict()
        payload["script_mismatches"] = {
            name: list(audit.mismatches)
            for name, audit in self.script_audits.items()
            if audit.mismatches
        }
        return payload

    async def get_gpu_status(self, node_name: str, dry_run: bool = False) -> dict[str, Any]:
        return (await self.executor.run_script(action="gpu-status", node_name=node_name, dry_run=dry_run, approved=True)).to_dict()

    async def get_disk_status(self, node_name: str, dry_run: bool = False) -> dict[str, Any]:
        return (await self.executor.run_script(action="disk-status", node_name=node_name, dry_run=dry_run, approved=True)).to_dict()

    async def get_docker_status(self, node_name: str, dry_run: bool = False) -> dict[str, Any]:
        return (await self.executor.run_script(action="docker-ps", node_name=node_name, dry_run=dry_run, approved=True)).to_dict()

    async def validate_compose(self, node_name: str, compose_path: str | None, dry_run: bool = False) -> dict[str, Any]:
        resolved = self.resolve_compose_root(node_name, compose_path)
        if not resolved["ok"]:
            return {"ok": False, "action": "compose-validate", "error": resolved["note"], "resolution": resolved}
        args = [] if resolved["source"] == "default_compose_root" else [resolved["compose_root"]]
        return (await self.executor.run_script(action="compose-validate", node_name=node_name, script_args=args, dry_run=dry_run, approved=True)).to_dict()

    async def stop_stack(self, node_name: str, stack_name_or_path: str | None, dry_run: bool = True, confirm: bool = False) -> dict[str, Any]:
        resolved = self.resolve_compose_root(node_name, stack_name_or_path)
        if not resolved["ok"]:
            return {"ok": False, "action": "stack-stop", "error": resolved["note"], "resolution": resolved}
        args = [] if resolved["source"] == "default_compose_root" else [resolved["compose_root"]]
        return (await self.executor.run_script(action="stack-stop", node_name=node_name, script_args=args, dry_run=dry_run, approved=confirm)).to_dict()

    async def start_stack(self, node_name: str, stack_name_or_path: str | None, dry_run: bool = True, confirm: bool = False) -> dict[str, Any]:
        resolved = self.resolve_compose_root(node_name, stack_name_or_path)
        if not resolved["ok"]:
            return {"ok": False, "action": "stack-start", "error": resolved["note"], "resolution": resolved}
        args = [] if resolved["source"] == "default_compose_root" else [resolved["compose_root"]]
        return (await self.executor.run_script(action="stack-start", node_name=node_name, script_args=args, dry_run=dry_run, approved=confirm)).to_dict()

    async def check_stack_health(self, node_name: str, stack_name_or_path: str | None, dry_run: bool = False) -> dict[str, Any]:
        resolved = self.resolve_compose_root(node_name, stack_name_or_path)
        if not resolved["ok"]:
            return {"ok": False, "action": "stack-health", "error": resolved["note"], "resolution": resolved}
        args = [] if resolved["source"] == "default_compose_root" else [resolved["compose_root"]]
        return (await self.executor.run_script(action="stack-health", node_name=node_name, script_args=args, dry_run=dry_run, approved=True)).to_dict()

    async def plan_model_deployment(
        self,
        *,
        model_name_or_tag: str,
        node_name: str | None = None,
        repo_id: str | None = None,
        semantic_tags: list[str] | None = None,
        compose_path: str | None = None,
        execute: bool = False,
        dry_run: bool = True,
        confirm: bool = False,
    ) -> dict[str, Any]:
        tags = sorted(set(semantic_tags or _tokenize(model_name_or_tag)))
        candidates = self.find_candidate_nodes(" ".join(tags or [model_name_or_tag]))
        target_node = node_name or (candidates[0]["node_name"] if candidates else None)
        if not target_node:
            return {
                "ok": False,
                "model_name_or_tag": model_name_or_tag,
                "error": "No candidate node matched the requested capability/tags.",
                "candidate_nodes": candidates,
            }

        destination_plan = self.plan_download_destination(
            node_name=target_node,
            model_name=model_name_or_tag,
            semantic_tags=tags,
            repo_id=repo_id,
        )
        inventory_matches = self.locate_model(model_name_or_tag, node_name=target_node)
        compose_resolution = self.resolve_compose_root(target_node, compose_path)

        gpu = await self.get_gpu_status(target_node, dry_run=False)
        disk = await self.get_disk_status(target_node, dry_run=False)
        docker = await self.get_docker_status(target_node, dry_run=False)
        health = await self.check_stack_health(target_node, compose_path, dry_run=False)
        compose_validation = await self.validate_compose(target_node, compose_path, dry_run=dry_run)

        steps: list[dict[str, Any]] = [
            {"step": "select_target_node", "ok": True, "target_node": target_node, "candidate_nodes": candidates},
            {"step": "inspect_gpu_state", "result": gpu},
            {"step": "inspect_disk_state", "result": disk},
            {"step": "inspect_docker_state", "result": docker},
            {"step": "locate_existing_model", "matches": inventory_matches},
            {"step": "determine_destination", "result": destination_plan},
            {"step": "resolve_compose_root", "result": compose_resolution},
            {"step": "validate_compose", "result": compose_validation},
            {"step": "check_stack_health", "result": health},
        ]

        if execute and repo_id and destination_plan.get("planned_destination"):
            download_result = await self.executor.run_model_download(
                node_name=target_node,
                repo_id=repo_id,
                destination=str(destination_plan["planned_destination"]),
                dry_run=dry_run,
                approved=confirm,
            )
            steps.append({"step": "download_model", "result": download_result.to_dict()})

        if execute:
            stop_result = await self.stop_stack(target_node, compose_path, dry_run=dry_run, confirm=confirm)
            start_result = await self.start_stack(target_node, compose_path, dry_run=dry_run, confirm=confirm)
            post_health = await self.check_stack_health(target_node, compose_path, dry_run=False if not dry_run else True)
            steps.extend(
                [
                    {"step": "stop_stack", "result": stop_result},
                    {"step": "start_stack", "result": start_result},
                    {"step": "verify_post_start_health", "result": post_health},
                ]
            )

        return {
            "ok": True,
            "model_name_or_tag": model_name_or_tag,
            "target_node": target_node,
            "repo_id": repo_id,
            "semantic_tags": tags,
            "execute": execute,
            "dry_run": dry_run,
            "steps": steps,
        }

    def audit_scripts(self) -> dict[str, Any]:
        return {
            name: audit.to_dict()
            for name, audit in self.script_audits.items()
        }

    def as_json(self, payload: dict[str, Any]) -> str:
        return json.dumps(payload, ensure_ascii=False, indent=2)
